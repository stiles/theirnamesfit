import type { APIRoute } from "astro";
import { entries } from "../../lib/data";
import { card } from "../../lib/og";

export function getStaticPaths() {
  return entries.map((entry) => ({ params: { slug: entry.slug }, props: { entry } }));
}

export const GET: APIRoute = async ({ props }) => {
  const { entry } = props as { entry: (typeof entries)[number] };
  const png = await card({ name: entry.name, occupation: entry.occupation, no: entry.no });
  return new Response(new Uint8Array(png), {
    headers: { "content-type": "image/png", "cache-control": "public, max-age=31536000, immutable" },
  });
};
