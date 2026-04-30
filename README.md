# Veld site — publish-ready bundle

Drop this entire folder's contents at the root of `getveld/getveld.github.io` (replacing the existing `index.html` and adding `assets/icons/`).

## What's in here

```
index.html              ← entry point
colors_and_type.css     ← brand tokens + Inter Tight import
site.css                ← layout & component styles
site.jsx                ← React app (loaded by Babel in-browser)
App.jsx                 ← root component
*.jsx                   ← section components (Hero, About, Products, etc.)
site.webmanifest        ← PWA manifest
assets/icons/           ← favicon, app icons (16/32/180/192/512 + SVG + maskable)
```

## What changed vs. the live site

1. **Tagline updated** — copy now says _"AI that pays back."_ (the locked tagline as of 2026-04-29).
2. **Favicon set wired up** — was a placeholder before; now serves Strategy A (deep-field bg + chalk blade-mark) at every standard size.
3. **Theme color** — `#23382F` (deep field) for browser chrome on mobile.
4. **PWA manifest** — proper icons for Android home-screen install.

## Sanity check before pushing

Open `index.html` locally — the page should render with the blade-mark favicon visible in the browser tab.

## Notes

- The site uses in-browser Babel transformation (the React + Babel CDN scripts in `<head>`). This is fine for a brochure site at this traffic level; if/when you precompile, the JSX files compile straight to JS with no other changes.
- No build step required. Push as-is.
