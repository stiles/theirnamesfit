import type { APIRoute } from "astro";
import { meta } from "../../lib/data";
import { card } from "../../lib/og";

export const GET: APIRoute = async () => {
  const png = await card({
    name: "Their names",
    occupation: "fit",
    footer: `${meta.total} OF THEM, ALL CHECKED`,
  });
  return new Response(new Uint8Array(png), {
    headers: { "content-type": "image/png", "cache-control": "public, max-age=31536000, immutable" },
  });
};
