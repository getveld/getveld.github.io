# Veld corporate site launch review

Status: **PUBLICATION CANDIDATE — INTERNAL QA AND INDEPENDENT RE-REVIEWS PASSED**

Prepared: August 22, 2026
Production base: `3afc03b431c4a021c07b97335152d3312d75b5dd`
Candidate branch: `feat/corporate-trust-surface-20260822`

## Scope

- Replace the root holding page with a corporate-first Veld homepage.
- Add `/consulting/` and `/how-veld-decides/`.
- Replace unfinished root legal placeholders with narrowly scoped corporate Website Privacy and Website Terms pages.
- Preserve Fleck and its product-specific pages unchanged.
- Remove runtime CDN dependencies from the corporate pages and self-host the licensed Inter Tight font.
- Add canonical metadata, CSP/referrer metadata, `robots.txt`, `sitemap.xml`, a custom 404 page, and legacy legal-route redirects.

## Verified local gates

- `python3 scripts/validate-site.py` — PASS; 6 corporate pages and 10 required-file groups.
- `python3 fleck/scripts/validate-launch-site.py --require-google-play-url` — PASS; five Fleck pages and verified public Google Play destination.
- `html-validate` — PASS for the five corporate routes, custom 404, and two legacy redirects.
- Browser QA — PASS across 25 corporate page/viewport combinations at 320, 390, 768, 1024, and 1440 CSS pixels.
- Axe WCAG 2.0/2.1 A/AA — zero violations at 390 and 1440 CSS pixels for every corporate route.
- Browser console/network — no errors, failed requests, external corporate-page requests, broken images, or horizontal overflow.
- Keyboard QA — skip link is the first focus target; mobile menu opens by keyboard and exposes all required destinations.
- Same-origin crawl — 24 linked pages/resources returned HTTP 200 locally.
- `git diff --cached --check` — PASS.
- Added-line secret/privacy scan — PASS; no secret patterns, personal Gmail address, local user path, or internal execution metadata.

The first browser harness run was a setup failure because Axe requires a browser context rather than `browser.newPage()`. The harness was corrected before product results were recorded. A later full-page run timed out while waiting on lazy Fleck images; Fleck was removed from the new corporate-page harness because its dedicated validator and prior cross-platform QA already cover that unchanged subtree. The final corporate matrix passed.

## Visual review

Desktop and mobile contact sheets were inspected. The homepage reads as a company surface first, with distinct product and consulting lanes below the fold. Consulting remains one click from global navigation. No publication-blocking hierarchy, responsiveness, readability, alignment, or generic AI-design defects were observed.

## Independent review closure

- The first exact-candidate visual/accessibility review found one blocker: the original single-color keyboard focus ring was below 3:1 against light and moss surfaces. It was replaced with a dual chalk/deep-field ring. Focused re-review measured at least one ring boundary above 3:1 on chalk, white, moss, deep-field, and graphite surfaces and returned **PASS**.
- The first exact-candidate legal/privacy/security review found one blocker: Website Terms overbroadly disclaimed an obligation to secure inquiry material. The clause now limits the boundary to contractual confidentiality, links personal-information handling to the Privacy Policy, and warns against sending sensitive data. Focused re-review found no remaining contradiction and returned **PASS**.
- Reviewers made no file changes. Both focused verdicts were bound to the corrected staged candidate at production base `3afc03b431c4a021c07b97335152d3312d75b5dd`.

## Privacy and legal boundary

- Root Privacy covers only the corporate site and pre-engagement inquiries.
- Root Terms govern website use only and do not create or govern a consulting engagement.
- Fleck retains its product-specific Privacy Policy and Terms.
- Corporate pages contain no form, analytics, cookies, tracking pixels, chat, session replay, or booking embed.
- Legal pages are operationally reconciled drafts, not legal advice; Veld may still choose counsel review.

## Rollback

A full source archive of the production base contains 58 paths and has SHA-256:

`ab506321b5e842ff415babfd0cc538ae3c55ba8e98d8439eb87729c20d33ce5e`

Before merge, re-fetch `main`. After merge, verify GitHub Pages completion and the live custom domain. If a material defect appears, revert the publication commit and repeat live readback.

## Remaining release sequence

1. Commit, push, open a PR, and verify GitHub checks.
2. Merge under Steven's explicit publication authorization.
3. Verify every live route, metadata field, legal page, link, asset, and responsive render from `getveld.ai`.
