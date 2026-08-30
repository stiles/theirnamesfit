import { defineConfig } from "astro/config";
import sitemap from "@astrojs/sitemap";

export default defineConfig({
  site: "https://theirnames.fit",
  trailingSlash: "never",
  build: { format: "file" },
  // The register moved onto the homepage; /names was its own page in the first build.
  redirects: { "/names": "/" },
  integrations: [
    sitemap({
      filter: (page) => !page.includes("/random"),
    }),
  ],
  devToolbar: { enabled: false },
});
