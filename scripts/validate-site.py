#!/usr/bin/env python3
"""Deterministic checks for the Veld corporate trust surface."""
from __future__ import annotations
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse, unquote
import json, re, sys

ROOT = Path(__file__).resolve().parents[1]
PAGES = [
    ROOT / "index.html",
    ROOT / "consulting/index.html",
    ROOT / "about/index.html",
    ROOT / "how-veld-decides/index.html",
    ROOT / "privacy/index.html",
    ROOT / "terms/index.html",
    ROOT / "404.html",
]
REDIRECT_PAGES = [ROOT / "privacy.html", ROOT / "terms.html"]
ALL_PAGES = PAGES + REDIRECT_PAGES
REQUIRED = [
    ROOT / "assets/site.css", ROOT / "robots.txt", ROOT / "sitemap.xml",
    ROOT / "site.webmanifest", ROOT / "CNAME",
    *(ROOT / f"assets/fonts/inter-tight-{w}.ttf" for w in (400,500,600,700)),
    ROOT / "assets/fonts/OFL.txt",
]

class Doc(HTMLParser):
    VOID_ELEMENTS = {
        "area", "base", "br", "col", "embed", "hr", "img", "input", "link",
        "meta", "param", "source", "track", "wbr",
    }

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.tags=[]; self.attrs=[]; self.text=[]; self.articles=[]; self.anchors=[]
        self._article=None; self._anchor=None
        self._hidden_depth = 0
        self._hidden_stack = []
    def handle_starttag(self, tag, attrs):
        data=dict(attrs); self.tags.append(tag); self.attrs.append((tag,data))
        hidden = "hidden" in data or str(data.get("aria-hidden") or "").strip().lower() == "true"
        if tag not in self.VOID_ELEMENTS:
            self._hidden_stack.append(hidden)
            if hidden: self._hidden_depth += 1
        if self._hidden_depth: return
        if tag == "article":
            self._article = {"attrs": data, "text": []}
            self.articles.append(self._article)
        if tag == "a":
            self._anchor = {"attrs": data, "text": []}
            self.anchors.append(self._anchor)
    def handle_endtag(self, tag):
        if not self._hidden_depth:
            if tag == "article": self._article = None
            if tag == "a": self._anchor = None
        if tag not in self.VOID_ELEMENTS and self._hidden_stack:
            if self._hidden_stack.pop(): self._hidden_depth -= 1
    def handle_data(self, data):
        if self._hidden_depth: return
        self.text.append(data)
        if self._article is not None: self._article["text"].append(data)
        if self._anchor is not None: self._anchor["text"].append(data)

def local_target(href: str) -> Path | None:
    if not href or href.startswith(("#","mailto:","tel:","data:")): return None
    parsed=urlparse(href)
    if parsed.scheme or parsed.netloc: return None
    path=unquote(parsed.path)
    candidate=ROOT / path.lstrip("/")
    if path.endswith("/") or not candidate.suffix: candidate /= "index.html"
    return candidate


def css_rules(source: str):
    """Yield (media query, selectors, declarations) for ordinary CSS rules."""
    source = re.sub(r"/\*.*?\*/", "", source, flags=re.DOTALL)

    def walk(block: str, media: str | None = None):
        cursor = 0
        while cursor < len(block):
            brace = block.find("{", cursor)
            if brace < 0:
                return
            prelude = block[cursor:brace].strip()
            depth = 1
            end = brace + 1
            while end < len(block) and depth:
                if block[end] == "{": depth += 1
                elif block[end] == "}": depth -= 1
                end += 1
            content = block[brace + 1:end - 1]
            if prelude.lower().startswith("@media"):
                yield from walk(content, prelude[6:].strip())
            elif not prelude.startswith("@"):
                declarations = []
                for declaration in content.split(";"):
                    if ":" in declaration:
                        name, value = declaration.split(":", 1)
                        declarations.append((name.strip().lower(), value.strip().lower()))
                yield media, [item.strip() for item in prelude.split(",")], declarations
            cursor = end

    yield from walk(source)


def normalized_media(media: str | None) -> str | None:
    return re.sub(r"\s+", "", media.lower()) if media is not None else None


def normalized_selectors(selectors: list[str]) -> tuple[str, ...]:
    return tuple(re.sub(r"\s+", " ", selector.strip().lower()) for selector in selectors)


def selector_mentions(selector: str, target: str) -> bool:
    return bool(re.search(r"(?<![\w-])" + re.escape(target) + r"(?![\w-])", selector))


def targeted_declarations(rules, target: str, property_name: str):
    for media, selectors, declarations in rules:
        if not any(selector_mentions(selector, target) for selector in selectors):
            continue
        for name, value in declarations:
            if name == property_name:
                yield normalized_media(media), normalized_selectors(selectors), value


errors=[]
for path in REQUIRED + ALL_PAGES:
    if not path.exists(): errors.append(f"missing: {path.relative_to(ROOT)}")
for page in ALL_PAGES:
    if not page.exists(): continue
    doc=Doc(); doc.feed(page.read_text(encoding="utf-8"))
    rel=page.relative_to(ROOT); body=" ".join(doc.text)
    if page in PAGES and page.name != "404.html":
        if doc.tags.count("h1") != 1: errors.append(f"{rel}: expected one h1")
        if not any(t=="a" and a.get("class","").find("skip-link")>=0 for t,a in doc.attrs): errors.append(f"{rel}: missing skip link")
        if not any(t=="main" and a.get("id")=="main" for t,a in doc.attrs): errors.append(f"{rel}: missing main#main")
        canon=[a.get("href") for t,a in doc.attrs if t=="link" and a.get("rel")=="canonical"]
        if len(canon)!=1 or not canon[0].startswith("https://getveld.ai/"): errors.append(f"{rel}: invalid canonical")
    for tag,a in doc.attrs:
        url=a.get("href") if tag in {"a","link"} else a.get("src") if tag in {"img","script"} else None
        target=local_target(url or "")
        if target and not target.exists(): errors.append(f"{rel}: broken local reference {url}")
        if tag=="script": errors.append(f"{rel}: script element is prohibited")
        if tag in {"iframe", "embed", "object"}:
            errors.append(f"{rel}: active content element {tag} is prohibited")
        for name, value in a.items():
            if name.lower().startswith("on"):
                errors.append(f"{rel}: executable HTML attribute {name}")
            if isinstance(value, str) and value.lstrip().lower().startswith("javascript:"):
                errors.append(f"{rel}: javascript URL is prohibited")
        if tag=="link" and "stylesheet" in a.get("rel","") and urlparse(a.get("href","")).netloc: errors.append(f"{rel}: external stylesheet {a['href']}")
    if page not in REDIRECT_PAGES and any(
        tag == "meta" and a.get("http-equiv", "").lower() == "refresh"
        for tag, a in doc.attrs
    ):
        errors.append(f"{rel}: meta refresh is prohibited")
    if page in REDIRECT_PAGES:
        expected_route = f"/{page.stem}/"
        canonical = [
            a.get("href") for tag, a in doc.attrs
            if tag == "link" and a.get("rel", "").lower() == "canonical"
        ]
        refresh = [
            a.get("content", "") for tag, a in doc.attrs
            if tag == "meta" and a.get("http-equiv", "").lower() == "refresh"
        ]
        fallback = [
            anchor for anchor in doc.anchors
            if anchor["attrs"].get("href") == expected_route
            and " ".join(anchor["text"]).strip()
        ]
        refresh_match = re.fullmatch(
            r"\s*0\s*;\s*url\s*=\s*" + re.escape(expected_route) + r"\s*",
            refresh[0],
            flags=re.IGNORECASE,
        ) if len(refresh) == 1 else None
        if (
            canonical != [f"https://getveld.ai{expected_route}"]
            or refresh_match is None
            or len(fallback) != 1
        ):
            errors.append(f"{rel}: invalid compatibility redirect")
    lower=body.lower()
    for phrase in ("ai that pays back", "coming soon", "currently accepting a small number", "west jordan"):
        if phrase in lower: errors.append(f"{rel}: stale/unsafe phrase {phrase!r}")
    claims_scan = lower.replace("does not guarantee savings", "")
    if re.search(r"\b(?:guarantee|guarantees|guaranteed|guaranteeing)\s+(?:savings|roi)\b", claims_scan):
        errors.append(f"{rel}: unsafe positive savings/ROI guarantee")

home=(ROOT/"index.html").read_text(encoding="utf-8")
home_doc = Doc(); home_doc.feed(home)
home_text = " ".join(home_doc.text)
home_hrefs = [anchor["attrs"].get("href", "") for anchor in home_doc.anchors]
for required in ("independent technology company", "25 years"):
    if required.lower() not in home_text.lower(): errors.append(f"index.html: missing {required!r}")
for required in ("/fleck/", "/consulting/", "steven@getveld.ai"):
    if not any(required.lower() in href.lower() for href in home_hrefs):
        errors.append(f"index.html: missing {required!r}")
work_articles = [
    article for article in home_doc.articles
    if "work-panel" in article["attrs"].get("class", "").split()
]
article_text = [" ".join(article["text"]) for article in work_articles]
consulting_articles = [i for i, text in enumerate(article_text) if "Consulting" in text]
fleck_articles = [i for i, text in enumerate(article_text) if "Fleck: AI Journal" in text]
if (
    len(consulting_articles) != 1
    or len(fleck_articles) != 1
    or consulting_articles[0] > fleck_articles[0]
):
    errors.append("index.html: Consulting must precede Fleck in the What We Do DOM order")
fleck_copy = article_text[fleck_articles[0]].lower() if len(fleck_articles) == 1 else ""
for required in ("privacy", "human control", "support", "reliability", "product operating experience", "not a consulting case study"):
    if required not in fleck_copy: errors.append(f"index.html Fleck evidence: missing {required!r}")
css=(ROOT/"assets/site.css").read_text(encoding="utf-8")
rules = list(css_rules(css))
mobile_media = "(max-width:940px)"
work_grid_declarations = list(targeted_declarations(rules, ".work-grid", "grid-template-columns"))
desktop_work_grid = [item for item in work_grid_declarations if item[0] != mobile_media]
mobile_work_grid = [item for item in work_grid_declarations if item[0] == mobile_media]
if desktop_work_grid != [(None, (".work-grid",), "3fr 2fr")]:
    errors.append("site.css: What We Do desktop columns must be approximately 60/40")
if mobile_work_grid != [(mobile_media, (".work-grid",), "1fr")]:
    errors.append("site.css: What We Do mobile columns must collapse to one column")
mobile_text_link = list(targeted_declarations(rules, ".text-link", "min-height"))
expected_text_link_selectors = (
    ".mobile-panel a", ".footer-links a", ".hero-actions a", ".page-hero-actions a",
    ".contact-band a", ".text-link",
)
if mobile_text_link != [(mobile_media, expected_text_link_selectors, "44px")]:
    errors.append("site.css: mobile .text-link min-height must be at least 44px")
consulting=(ROOT/"consulting/index.html").read_text(encoding="utf-8")
consulting_doc=Doc(); consulting_doc.feed(consulting)
consulting_text=" ".join(consulting_doc.text)
consulting_hrefs=[anchor["attrs"].get("href", "") for anchor in consulting_doc.anchors]
for required in ("not a free audit", "no change", "paid assessment", "does not guarantee savings"):
    if required.lower() not in consulting_text.lower(): errors.append(f"consulting: missing {required!r}")
if consulting_text.lower().count("not a free audit") != 1:
    errors.append("consulting: defensive buyer-facing copy repeats 'not a free audit'")
for forbidden in ("will not manufacture social proof", "not presented as proof of consulting-client outcomes"):
    if forbidden in (home_text + consulting_text).lower():
        errors.append(f"defensive buyer-facing copy: {forbidden!r}")
for required in (
    "Steven Davis", "work directly with Steven", "25 years", "more than a decade",
    "CIO", "security", "procurement", "compliance", "reliability", "integrations",
    "change management", "ROI",
):
    if required.lower() not in consulting_text.lower(): errors.append(f"consulting founder: missing {required!r}")
if "/about/" not in consulting_hrefs: errors.append("consulting founder: missing '/about/'")
for required in (
    "chambers", "advisers", "owner-led businesses", "educational session", "clinic",
    "one workflow", "simple fixes", "automation", "AI", "evidence", "safe first test",
    "practical education", "not a product pitch", "individual audit", "member or attendee list", "only by consent",
    "20-minute partner-fit conversation",
):
    if required.lower() not in consulting_text.lower(): errors.append(f"consulting partner capability: missing {required!r}")
for required in (
    "brings substantial operating experience", "early in publishing measured consulting outcomes",
    "names and results appear only after measurement and permission",
):
    if required.lower() not in consulting_text.lower(): errors.append(f"consulting evidence standard: missing {required!r}")
about_path=ROOT/"about/index.html"
if about_path.exists():
    about=about_path.read_text(encoding="utf-8")
    about_doc=Doc(); about_doc.feed(about)
    about_text=" ".join(about_doc.text)
    for required in (
        "Steven Davis", "25 years", "more than a decade", "CIO", "security", "procurement",
        "compliance", "reliability", "integrations", "change management", "ROI",
        "hands-on", "Veld products", "agent-supported systems", "workflow-first",
    ):
        if required.lower() not in about_text.lower(): errors.append(f"about: missing {required!r}")
    for forbidden in ("$1m", "$250m", "35 countries", "linkedin"):
        if forbidden in about_text.lower(): errors.append(f"about: prohibited claim or link {forbidden!r}")
    if any(tag == "img" for tag, _ in about_doc.attrs): errors.append("about: founder photo is prohibited")
method=(ROOT/"how-veld-decides/index.html").read_text(encoding="utf-8")
method_doc=Doc(); method_doc.feed(method)
method_text=" ".join(method_doc.text)
method_hrefs=[anchor["attrs"].get("href", "") for anchor in method_doc.anchors]
for required in ("Steven", "owner-led businesses", "Workflow Triage"):
    if required.lower() not in method_text.lower(): errors.append(f"method close: missing {required!r}")
if not any(href.lower().startswith("mailto:steven@getveld.ai") for href in method_hrefs):
    errors.append("method close: missing 'mailto:steven@getveld.ai'")
for page in (
    ROOT/"index.html", ROOT/"consulting/index.html", ROOT/"about/index.html",
    ROOT/"how-veld-decides/index.html", ROOT/"privacy/index.html", ROOT/"terms/index.html",
):
    if page.exists():
        page_doc=Doc(); page_doc.feed(page.read_text(encoding="utf-8"))
        about_links=[anchor for anchor in page_doc.anchors if anchor["attrs"].get("href") == "/about/"]
        if len(about_links) < 2:
            errors.append(f"{page.relative_to(ROOT)}: About missing from corporate navigation/footer")
sitemap=(ROOT/"sitemap.xml").read_text(encoding="utf-8")
if "https://getveld.ai/about/" not in sitemap: errors.append("sitemap: missing /about/ route")
privacy=(ROOT/"privacy/index.html").read_text(encoding="utf-8")
privacy_doc=Doc(); privacy_doc.feed(privacy)
privacy_text=" ".join(privacy_doc.text)
for required in ("does not currently provide an account", "does not currently add site-controlled analytics", "Fleck Privacy Policy", "Google Workspace"):
    if required.lower() not in privacy_text.lower(): errors.append(f"privacy: missing {required!r}")
terms=(ROOT/"terms/index.html").read_text(encoding="utf-8")
terms_doc=Doc(); terms_doc.feed(terms)
terms_text=" ".join(terms_doc.text)
for required in ("does not create a consulting relationship", "separate written agreement", "Fleck Terms of Use"):
    if required.lower() not in terms_text.lower(): errors.append(f"terms: missing {required!r}")

manifest=json.loads((ROOT/"site.webmanifest").read_text(encoding="utf-8"))
if "AI that pays back" in manifest.get("description",""): errors.append("manifest: stale positioning")
if (ROOT/"CNAME").read_text().strip() != "getveld.ai": errors.append("CNAME changed")

if errors:
    print(json.dumps({"ok":False,"errors":errors},indent=2)); sys.exit(1)
print(json.dumps({"ok":True,"pages_checked":len(ALL_PAGES),"required_files":len(REQUIRED)},indent=2))
