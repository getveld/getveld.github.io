# Fleck cross-platform website launch review

Status: **LOCAL REVIEW HOLD — NOT PUBLISHED**

Prepared: August 8, 2026

Branch: `feat/fleck-android-launch-collateral`

Pull request: https://github.com/getveld/getveld.github.io/pull/2

## Start here

A private localhost preview is served from the repository root at:

- Landing: http://127.0.0.1:8765/fleck/
- FAQ: http://127.0.0.1:8765/fleck/faq/
- Support: http://127.0.0.1:8765/fleck/support.html
- Privacy: http://127.0.0.1:8765/fleck/privacy.html
- Terms: http://127.0.0.1:8765/fleck/terms.html

The server is bound to `127.0.0.1`, so open these URLs on Susan Mac directly or through Screen Sharing. Nothing in this branch has been merged or published.

## Prepared launch state

All five pages are written for Fleck being publicly available on both:

- iPhone through Apple’s App Store; and
- Android through Google Play.

The pages share one stylesheet, one visual system, matching desktop and mobile navigation, and the same footer. Product, support, privacy, subscription, export, deletion, backup, AI-routing, age, and store terminology have been reconciled across the set.

The only intentionally unresolved launch value is the signed-out public Google Play listing URL.

## Google Play URL launch switch

Replace this one value in `fleck/assets/fleck-store-links.js`:

```js
const FLECK_GOOGLE_PLAY_URL = "GOOGLE_PLAY_URL_PENDING";
```

with the verified public HTTPS listing URL. Every direct Google Play CTA is populated from that single value. The top-level **Download** navigation item already points to the shared download section and requires no separate edit.

Do not use a Play Console URL, authenticated URL, guessed package URL, or preapproval testing URL. Verify the final listing signed out before inserting it.

## Final publication sequence

1. Confirm Google Play shows Fleck as publicly available in the intended regions.
2. Open the final listing signed out and copy its stable HTTPS URL.
3. Replace the single placeholder in `fleck/assets/fleck-store-links.js`.
4. Run:

   ```bash
   python3 fleck/scripts/validate-launch-site.py --require-google-play-url
   npx --yes html-validate@10.4.0 \
     fleck/index.html fleck/faq/index.html fleck/support.html \
     fleck/privacy.html fleck/terms.html
   git diff --check
   ```

5. Serve locally and click both store buttons, all header/footer links, and all legal/support links.
6. Obtain Steven’s explicit approval to merge/publish.
7. Merge PR #2 only after that approval.
8. Fetch all five public URLs and both store links after deployment; do not infer publication from a successful merge alone.

## Verification completed for this holding pattern

- Five HTML pages passed `html-validate` with zero errors.
- Shared-shell and local-reference validator passed.
- All five pages and both shared assets returned HTTP 200 from localhost.
- Playwright checked all five pages at 320, 390, 768, 1024, and 1440 CSS pixels: 25 page/viewport combinations.
- Axe checked all five pages at 390 and 1440 CSS pixels against WCAG 2.0/2.1 A and AA rules: zero violations.
- No horizontal overflow, broken images, same-origin request failures, or browser console errors were found.
- Desktop and mobile screenshots were visually reviewed.
- Mobile navigation, current-page markers, the Download anchor, keyboard skip link, and pending CTA accessibility state were exercised in a browser.
- The single-value launch switch was tested with an intercepted nonproduction HTTPS URL; both pending controls became working **Get it on Google Play** links without editing page markup.
- Google Play CTAs remain visibly disabled and labeled **Google Play link pending** until the verified URL is inserted.
- Content was checked against Fleck release source `44351cfd4dff22b1d3653032fa15101738a16174`; the associated app suite passed 230 tests with zero failures during the audit.
- Independent review findings were resolved: deletion copy now covers dependent generated/stale sketch removal, the RevenueCat privacy-data-request route and boundaries are documented, and billing copy relies on store-displayed periods instead of promising fixed monthly/annual options or no weekly option.
- The post-fix independent re-review returned **PASS**.
- `git diff --check` passed.

## Legal review note

The Privacy Policy and Terms have been reconciled to the reviewed app behavior and cross-platform store model. They are product-ready drafts, not legal advice; Veld may still choose to obtain counsel review before publication.
