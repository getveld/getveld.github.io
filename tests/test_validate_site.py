from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ValidateSiteRegressionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.site = Path(self.temp_dir.name) / "site"
        shutil.copytree(ROOT, self.site, ignore=shutil.ignore_patterns(".git", "__pycache__"))

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def run_validator(self) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(self.site / "scripts/validate-site.py")],
            cwd=self.site,
            text=True,
            capture_output=True,
            check=False,
        )

    def replace(self, relative_path: str, old: str, new: str) -> None:
        path = self.site / relative_path
        source = path.read_text(encoding="utf-8")
        self.assertIn(old, source)
        path.write_text(source.replace(old, new, 1), encoding="utf-8")

    def assert_validator_rejects(self, message: str) -> None:
        result = self.run_validator()
        self.assertNotEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn(message, result.stdout + result.stderr)

    def test_redirect_requires_meta_refresh(self) -> None:
        self.replace(
            "privacy.html",
            '<meta http-equiv="refresh" content="0;url=/privacy/">',
            "",
        )
        self.assert_validator_rejects("privacy.html: invalid compatibility redirect")

    def test_redirect_requires_human_readable_fallback_anchor(self) -> None:
        self.replace(
            "terms.html",
            '<a href="/terms/">getveld.ai/terms/</a>',
            '<a href="/terms/"></a>',
        )
        self.assert_validator_rejects("terms.html: invalid compatibility redirect")

    def test_redirect_rejects_nonzero_delay(self) -> None:
        self.replace(
            "privacy.html",
            'content="0;url=/privacy/"',
            'content="2;url=/privacy/"',
        )
        self.assert_validator_rejects("privacy.html: invalid compatibility redirect")

    def test_redirect_rejects_disagreeing_targets(self) -> None:
        self.replace(
            "terms.html",
            'content="0;url=/terms/"',
            'content="0;url=/privacy/"',
        )
        self.assert_validator_rejects("terms.html: invalid compatibility redirect")

    def test_redirect_requires_exactly_one_canonical(self) -> None:
        self.replace(
            "privacy.html",
            '<link rel="canonical" href="https://getveld.ai/privacy/">',
            '<link rel="canonical" href="https://getveld.ai/privacy/">' * 2,
        )
        self.assert_validator_rejects("privacy.html: invalid compatibility redirect")

    def test_redirect_requires_exactly_one_meta_refresh(self) -> None:
        self.replace(
            "terms.html",
            '<meta http-equiv="refresh" content="0;url=/terms/">',
            '<meta http-equiv="refresh" content="0;url=/terms/">' * 2,
        )
        self.assert_validator_rejects("terms.html: invalid compatibility redirect")

    def test_meta_refresh_is_prohibited_on_content_pages(self) -> None:
        self.replace(
            "index.html",
            "</head>",
            '<meta http-equiv="refresh" content="0;url=https://example.com"></head>',
        )
        self.assert_validator_rejects("index.html: meta refresh is prohibited")

    def test_executable_event_handler_attribute_is_prohibited(self) -> None:
        self.replace("index.html", "<body>", '<body onload="alert(1)">')
        self.assert_validator_rejects("index.html: executable HTML attribute onload")

    def test_iframe_srcdoc_is_prohibited(self) -> None:
        self.replace(
            "index.html",
            "</main>",
            '<iframe srcdoc="&lt;script&gt;alert(1)&lt;/script&gt;"></iframe></main>',
        )
        self.assert_validator_rejects("index.html: active content element iframe is prohibited")

    def test_javascript_url_is_prohibited(self) -> None:
        self.replace(
            "privacy.html",
            '<a href="/privacy/">',
            '<a href="javascript:alert(1)">',
        )
        self.assert_validator_rejects("privacy.html: javascript URL is prohibited")

    def test_ordinary_links_remain_allowed(self) -> None:
        result = self.run_validator()
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_swapped_work_articles_are_not_spoofed_by_comment_text(self) -> None:
        path = self.site / "index.html"
        source = path.read_text(encoding="utf-8")
        consulting_start = source.index('<article class="work-panel work-panel--dark">')
        fleck_start = source.index('<article class="work-panel">', consulting_start)
        consulting = source[consulting_start:fleck_start]
        fleck_end = source.index("</article>", fleck_start) + len("</article>")
        fleck = source[fleck_start:fleck_end]
        decoy = '<!-- panel-kicker">Consulting -->'
        swapped = source[:consulting_start] + decoy + fleck + consulting + source[fleck_end:]
        path.write_text(swapped, encoding="utf-8")
        self.assert_validator_rejects(
            "index.html: Consulting must precede Fleck in the What We Do DOM order"
        )

    def test_later_desktop_work_grid_override_is_rejected(self) -> None:
        css = self.site / "assets/site.css"
        css.write_text(
            css.read_text(encoding="utf-8")
            + "\n/* .work-grid{grid-template-columns:3fr 2fr} */\n"
            + ".work-grid{grid-template-columns:1fr 1fr}\n",
            encoding="utf-8",
        )
        self.assert_validator_rejects(
            "site.css: What We Do desktop columns must be approximately 60/40"
        )

    def test_more_specific_desktop_work_grid_override_is_rejected(self) -> None:
        css = self.site / "assets/site.css"
        css.write_text(
            css.read_text(encoding="utf-8")
            + "\n.shell .work-grid{grid-template-columns:1fr 1fr}\n",
            encoding="utf-8",
        )
        self.assert_validator_rejects(
            "site.css: What We Do desktop columns must be approximately 60/40"
        )

    def test_unmatched_important_decoy_cannot_mask_bad_work_grid_override(self) -> None:
        css = self.site / "assets/site.css"
        css.write_text(
            css.read_text(encoding="utf-8")
            + "\n@media(min-width:1000px){"
            + ".work-grid{grid-template-columns:1fr 1fr}"
            + "#unused .work-grid{grid-template-columns:3fr 2fr!important}}\n",
            encoding="utf-8",
        )
        self.assert_validator_rejects(
            "site.css: What We Do desktop columns must be approximately 60/40"
        )

    def test_applicable_min_width_work_grid_override_is_rejected(self) -> None:
        css = self.site / "assets/site.css"
        css.write_text(
            css.read_text(encoding="utf-8")
            + "\n@media(min-width:1000px){.work-grid{grid-template-columns:1fr 1fr}}\n",
            encoding="utf-8",
        )
        self.assert_validator_rejects(
            "site.css: What We Do desktop columns must be approximately 60/40"
        )

    def test_mobile_work_grid_requires_one_column(self) -> None:
        self.replace(
            "assets/site.css",
            ".work-grid{grid-template-columns:1fr}.offer-flow",
            ".work-grid{grid-template-columns:1fr 1fr}.offer-flow",
        )
        self.assert_validator_rejects(
            "site.css: What We Do mobile columns must collapse to one column"
        )

    def test_mobile_text_links_have_44px_minimum_height(self) -> None:
        self.replace(
            "assets/site.css",
            ".contact-band a,.text-link{min-height:44px",
            ".contact-band a{min-height:44px",
        )
        self.assert_validator_rejects(
            "site.css: mobile .text-link min-height must be at least 44px"
        )

    def test_more_specific_mobile_text_link_height_override_is_rejected(self) -> None:
        css = self.site / "assets/site.css"
        css.write_text(
            css.read_text(encoding="utf-8")
            + "\n@media(max-width:940px){.page-hero .text-link{min-height:20px}}\n",
            encoding="utf-8",
        )
        self.assert_validator_rejects(
            "site.css: mobile .text-link min-height must be at least 44px"
        )

    def test_commented_out_founder_section_is_rejected(self) -> None:
        path = self.site / "consulting/index.html"
        source = path.read_text(encoding="utf-8")
        start = source.index('<section class="section section--paper"><div class="shell founder-block">')
        end = source.index("</section>", start) + len("</section>")
        path.write_text(
            source[:start] + "<!--" + source[start:end] + "-->" + source[end:],
            encoding="utf-8",
        )
        self.assert_validator_rejects("consulting founder: missing 'Steven Davis'")

    def test_hidden_founder_section_is_rejected(self) -> None:
        self.replace(
            "consulting/index.html",
            '<section class="section section--paper"><div class="shell founder-block">',
            '<section class="section section--paper" hidden><div class="shell founder-block">',
        )
        self.assert_validator_rejects("consulting founder: missing 'Steven Davis'")

    def test_buyer_copy_avoids_defensive_phrasing(self) -> None:
        self.replace(
            "consulting/index.html",
            "Veld is early in publishing measured consulting outcomes.",
            "Veld is early in publishing measured consulting outcomes and will not manufacture social proof.",
        )
        self.assert_validator_rejects("defensive buyer-facing copy")


if __name__ == "__main__":
    unittest.main()
