#!/usr/bin/env python3
"""Validate the Fleck launch-ready static pages without external dependencies."""

from __future__ import annotations

import argparse
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

FLECK_ROOT = Path(__file__).resolve().parents[1]
SITE_ROOT = FLECK_ROOT.parent
PAGES = [
    FLECK_ROOT / "index.html",
    FLECK_ROOT / "faq" / "index.html",
    FLECK_ROOT / "support.html",
    FLECK_ROOT / "privacy.html",
    FLECK_ROOT / "terms.html",
]
STORE_LINKS = FLECK_ROOT / "assets" / "fleck-store-links.js"
SUPPORT_EMAIL = "fleck-support@getveld.ai"
STALE_LAUNCH_LANGUAGE = (
    "not publicly available",
    "being prepared for google play",
    "android preview",
    "coming soon",
    "iphone only",
    "ios only",
    "weekly subscription",
    "monthly or annual subscriptions",
)
REQUIRED_TRUTH_CLAIMS = {
    "fleck/faq/index.html": ("dependent sketch", "privacy data request"),
    "fleck/support.html": ("dependent sketch", "privacy data request"),
    "fleck/privacy.html": ("dependent sketch", "privacy data request"),
}


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.counts: dict[str, int] = {}
        self.refs: list[str] = []
        self.ids: set[str] = set()
        self.duplicate_ids: set[str] = set()
        self.current_page_links = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.counts[tag] = self.counts.get(tag, 0) + 1
        values = dict(attrs)
        element_id = values.get("id")
        if element_id:
            if element_id in self.ids:
                self.duplicate_ids.add(element_id)
            self.ids.add(element_id)
        if values.get("aria-current") == "page":
            self.current_page_links += 1
        for attr in ("href", "src"):
            value = values.get(attr)
            if value:
                self.refs.append(value)


def local_target(reference: str) -> Path | None:
    if not reference.startswith("/"):
        return None
    path = urlparse(reference).path
    target = SITE_ROOT / path.lstrip("/")
    return target / "index.html" if path.endswith("/") else target


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--require-google-play-url", action="store_true")
    args = parser.parse_args()
    failures: list[str] = []

    combined = ""
    for page in PAGES:
        text = page.read_text(encoding="utf-8")
        combined += "\n" + text
        parsed = PageParser()
        parsed.feed(text)
        relative = page.relative_to(SITE_ROOT)
        for tag in ("header", "main", "footer"):
            if parsed.counts.get(tag) != 1:
                failures.append(f"{relative}: expected exactly one <{tag}>")
        if parsed.counts.get("nav", 0) < 3:
            failures.append(f"{relative}: missing desktop, mobile, or footer navigation")
        if parsed.duplicate_ids:
            failures.append(f"{relative}: duplicate IDs {sorted(parsed.duplicate_ids)}")
        if "/fleck/assets/fleck-site.css" not in text:
            failures.append(f"{relative}: shared stylesheet missing")
        if "Voice-first private journaling for iPhone and Android." not in text:
            failures.append(f"{relative}: shared footer tagline missing")
        for phrase in REQUIRED_TRUTH_CLAIMS.get(relative.as_posix(), ()):
            if phrase not in text.lower():
                failures.append(f"{relative}: required truth claim missing: {phrase}")
        expected_mailto = f"mailto:{SUPPORT_EMAIL}"
        mailto_refs = [reference for reference in parsed.refs if reference.lower().startswith("mailto:")]
        if expected_mailto not in mailto_refs:
            failures.append(f"{relative}: missing product support link {expected_mailto}")
        if SUPPORT_EMAIL not in text:
            failures.append(f"{relative}: missing visible product support address {SUPPORT_EMAIL}")
        for reference in mailto_refs:
            if reference != expected_mailto:
                failures.append(f"{relative}: unexpected product email link {reference}")
        for reference in parsed.refs:
            target = local_target(reference)
            if target is not None and not target.exists():
                failures.append(f"{relative}: missing local reference {reference}")
                continue
            fragment = urlparse(reference).fragment
            if target is not None and fragment and target.exists():
                target_parser = PageParser()
                target_parser.feed(target.read_text(encoding="utf-8"))
                if fragment not in target_parser.ids:
                    failures.append(f"{relative}: missing fragment target {reference}")

    lowered = combined.lower()
    for phrase in STALE_LAUNCH_LANGUAGE:
        if phrase in lowered:
            failures.append(f"stale prelaunch language remains: {phrase!r}")

    script = STORE_LINKS.read_text(encoding="utf-8")
    match = re.search(r'const FLECK_GOOGLE_PLAY_URL = "([^"]+)";', script)
    if not match:
        failures.append("Google Play URL configuration assignment missing")
    else:
        value = match.group(1)
        if args.require_google_play_url:
            parsed_url = urlparse(value)
            if parsed_url.scheme != "https" or not parsed_url.netloc:
                failures.append("verified HTTPS Google Play URL is required")
        elif value != "GOOGLE_PLAY_URL_PENDING":
            parsed_url = urlparse(value)
            if parsed_url.scheme != "https" or not parsed_url.netloc:
                failures.append("configured Google Play URL is not a valid HTTPS URL")

    if script.count('const FLECK_GOOGLE_PLAY_URL = "') != 1:
        failures.append("expected exactly one Google Play URL configuration assignment")

    if failures:
        print("Fleck launch-site validation: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    state = "public URL configured" if args.require_google_play_url else "holding pattern allowed"
    print(f"Fleck launch-site validation: PASS ({len(PAGES)} pages; {state})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
