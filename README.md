# Veld corporate website

Static GitHub Pages site for `getveld.ai`.

## Public routes

- `/` — Veld corporate homepage
- `/about/` — founder experience and Veld's operating perspective
- `/consulting/` — workflow-first consulting
- `/how-veld-decides/` — consulting decision method
- `/privacy/` — corporate website privacy policy
- `/terms/` — corporate website terms
- `/fleck/` — Fleck product site and product-specific legal/support pages

The corporate pages are semantic static HTML/CSS with self-hosted Inter Tight fonts. They use no runtime JavaScript, forms, analytics, trackers, cookies, booking widgets, or external font/CDN requests. Fleck remains an independently validated product subtree.

## Local verification

```bash
python3 -m http.server 8766 --bind 127.0.0.1
python3 scripts/validate-site.py
python3 fleck/scripts/validate-launch-site.py --require-google-play-url
npx --yes html-validate@10.4.0 \
  index.html consulting/index.html about/index.html how-veld-decides/index.html \
  privacy/index.html terms/index.html 404.html privacy.html terms.html
git diff --check
```

Then verify every route at desktop and mobile widths, including keyboard navigation, links, images, console/network state, horizontal overflow, metadata, and WCAG A/AA checks.

## Publication

GitHub Pages publishes the root of `main` to `getveld.ai`. Treat merge to `main` as a production deployment. Preserve `CNAME`, the complete `/fleck/` subtree, and a rollback commit before merging. After merge, verify the Pages deployment and fetch/render every public route from the custom domain.
