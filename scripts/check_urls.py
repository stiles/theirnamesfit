#!/usr/bin/env python3
"""Check that every source URL in the master dataset resolves.

Writes data/url_check.csv with one row per (id, column, url, status). Status is an HTTP
code, or a short error string. Wikipedia URLs are additionally checked against the API so a
soft-404 (an article that does not exist) is not reported as a live page.
"""

from __future__ import annotations

import csv
import json
import ssl
import time
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MASTER = ROOT / "data" / "aptronyms.csv"
OUT = ROOT / "data" / "url_check.csv"

URL_COLUMNS = ["person_source_url", "name_source_url", "discovery_source_url"]
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36"
CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE


def wikipedia_title(url: str) -> tuple[str, str] | None:
    parsed = urllib.parse.urlparse(url)
    if not parsed.netloc.endswith("wikipedia.org") or "/wiki/" not in parsed.path:
        return None
    title = urllib.parse.unquote(parsed.path.split("/wiki/", 1)[1]).replace("_", " ")
    title = title.split("#", 1)[0]
    return parsed.netloc, title


def api_query(host: str, titles: list[str], attempts: int = 5) -> dict:
    """One API call, retried with backoff. Wikimedia throttles bursts, and a throttled
    batch must not be recorded as fifty dead articles."""
    api = (
        f"https://{host}/w/api.php?action=query&format=json&redirects=1&titles="
        + urllib.parse.quote("|".join(titles))
    )
    delay = 2.0
    for attempt in range(attempts):
        req = urllib.request.Request(api, headers={"User-Agent": UA})
        try:
            with urllib.request.urlopen(req, timeout=60, context=CTX) as resp:
                return json.load(resp)
        except Exception:  # noqa: BLE001
            if attempt == attempts - 1:
                raise
            time.sleep(delay)
            delay *= 2
    raise RuntimeError("unreachable")


def check_wikipedia_batch(host: str, titles: list[str]) -> dict[str, str]:
    """Resolve up to 50 titles in one API call. Returns title -> status."""
    data = api_query(host, titles)

    query = data.get("query", {})
    # Requested title -> title the API actually reported on.
    alias = {t: t for t in titles}
    for norm in query.get("normalized", []):
        alias[norm["from"]] = norm["to"]
    for redir in query.get("redirects", []):
        for src, dst in list(alias.items()):
            if dst == redir["from"]:
                alias[src] = redir["to"]

    resolved: dict[str, str] = {}
    for page in query.get("pages", {}).values():
        resolved[page.get("title", "")] = "wiki-missing" if "missing" in page else "200"
    return {t: resolved.get(alias[t], "wiki-unresolved") for t in titles}


def encode(url: str) -> str:
    """Percent-encode non-ASCII path and query bytes. urllib cannot send them raw."""
    parts = urllib.parse.urlsplit(url)
    return urllib.parse.urlunsplit(
        (
            parts.scheme,
            parts.netloc.encode("idna").decode("ascii") if not parts.netloc.isascii() else parts.netloc,
            urllib.parse.quote(parts.path, safe="/%:@&=+$,~"),
            urllib.parse.quote(parts.query, safe="/%:@&=+$,~?"),
            parts.fragment,
        )
    )


def check(url: str) -> str:
    target = encode(url)
    for method in ("HEAD", "GET"):
        req = urllib.request.Request(target, method=method, headers={"User-Agent": UA})
        try:
            with urllib.request.urlopen(req, timeout=30, context=CTX) as resp:
                return str(resp.status)
        except urllib.error.HTTPError as exc:
            if method == "HEAD" and exc.code in (403, 405, 501):
                continue
            return str(exc.code)
        except Exception as exc:  # noqa: BLE001
            if method == "HEAD":
                continue
            return f"error:{type(exc).__name__}"
    return "error:unknown"


def main() -> None:
    rows = list(csv.DictReader(MASTER.open(encoding="utf-8")))
    jobs: list[tuple[str, str, str, str]] = []
    for row in rows:
        for col in URL_COLUMNS:
            url = row.get(col, "").strip()
            if url:
                jobs.append((row["id"], row["full_name"], col, url))

    # Cache identical URLs; the same Wikipedia page backs many rows.
    cache: dict[str, str] = {}
    unique = sorted({j[3] for j in jobs})
    print(f"{len(jobs)} url references, {len(unique)} unique")

    # Wikipedia gets batched through the API: 50 titles per call, sequential, so we
    # neither hammer the API nor mistake a soft 404 for a live article.
    wiki_by_host: dict[str, dict[str, list[str]]] = {}
    other: list[str] = []
    for url in unique:
        parsed = wikipedia_title(url)
        if parsed:
            host, title = parsed
            wiki_by_host.setdefault(host, {}).setdefault(title, []).append(url)
        else:
            other.append(url)

    for host, titles in wiki_by_host.items():
        keys = list(titles)
        print(f"  {host}: {len(keys)} titles")
        for i in range(0, len(keys), 50):
            chunk = keys[i : i + 50]
            try:
                statuses = check_wikipedia_batch(host, chunk)
            except Exception:  # noqa: BLE001
                # Fall back to one title at a time so a single bad title in the batch
                # cannot take the other forty-nine down with it.
                statuses = {}
                for title in chunk:
                    try:
                        statuses.update(check_wikipedia_batch(host, [title]))
                    except Exception as exc:  # noqa: BLE001
                        statuses[title] = f"wiki-error:{type(exc).__name__}"
                    time.sleep(0.5)
            for title, status in statuses.items():
                for url in titles[title]:
                    cache[url] = status
            time.sleep(0.5)

    print(f"  other hosts: {len(other)} urls")
    with ThreadPoolExecutor(max_workers=8) as pool:
        for url, status in zip(other, pool.map(check, other)):
            cache[url] = status

    with OUT.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(["id", "full_name", "column", "url", "status"])
        for rid, name, col, url in jobs:
            writer.writerow([rid, name, col, url, cache[url]])

    bad = [(u, s) for u, s in cache.items() if s != "200"]
    print(f"{len(cache) - len(bad)} ok, {len(bad)} problem urls")
    for url, status in sorted(bad, key=lambda x: x[1]):
        print(f"  {status:22} {url}")


if __name__ == "__main__":
    main()
