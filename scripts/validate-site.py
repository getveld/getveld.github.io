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
    ROOT / "how-veld-decides/index.html",
    ROOT / "privacy/index.html",
    ROOT / "terms/index.html",
    ROOT / "404.html",
]
REQUIRED = [
    ROOT / "assets/site.css", ROOT / "robots.txt", ROOT / "sitemap.xml",
    ROOT / "site.webmanifest", ROOT / "CNAME",
    *(ROOT / f"assets/fonts/inter-tight-{w}.ttf" for w in (400,500,600,700)),
    ROOT / "assets/fonts/OFL.txt",
]

class Doc(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.tags=[]; self.attrs=[]; self.text=[]
    def handle_starttag(self, tag, attrs):
        data=dict(attrs); self.tags.append(tag); self.attrs.append((tag,data))
    def handle_data(self, data): self.text.append(data)

def local_target(href: str) -> Path | None:
    if not href or href.startswith(("#","mailto:","tel:","data:")): return None
    parsed=urlparse(href)
    if parsed.scheme or parsed.netloc: return None
    path=unquote(parsed.path)
    candidate=ROOT / path.lstrip("/")
    if path.endswith("/") or not candidate.suffix: candidate /= "index.html"
    return candidate

errors=[]
for path in REQUIRED + PAGES:
    if not path.exists(): errors.append(f"missing: {path.relative_to(ROOT)}")
for page in PAGES:
    if not page.exists(): continue
    doc=Doc(); doc.feed(page.read_text(encoding="utf-8"))
    rel=page.relative_to(ROOT); body=" ".join(doc.text)
    if page.name != "404.html":
        if doc.tags.count("h1") != 1: errors.append(f"{rel}: expected one h1")
        if not any(t=="a" and a.get("class","").find("skip-link")>=0 for t,a in doc.attrs): errors.append(f"{rel}: missing skip link")
        if not any(t=="main" and a.get("id")=="main" for t,a in doc.attrs): errors.append(f"{rel}: missing main#main")
        canon=[a.get("href") for t,a in doc.attrs if t=="link" and a.get("rel")=="canonical"]
        if len(canon)!=1 or not canon[0].startswith("https://getveld.ai/"): errors.append(f"{rel}: invalid canonical")
    for tag,a in doc.attrs:
        url=a.get("href") if tag in {"a","link"} else a.get("src") if tag in {"img","script"} else None
        target=local_target(url or "")
        if target and not target.exists(): errors.append(f"{rel}: broken local reference {url}")
        if tag=="script" and a.get("src") and urlparse(a["src"]).netloc: errors.append(f"{rel}: external script {a['src']}")
        if tag=="link" and "stylesheet" in a.get("rel","") and urlparse(a.get("href","")).netloc: errors.append(f"{rel}: external stylesheet {a['href']}")
    lower=body.lower()
    for phrase in ("ai that pays back", "coming soon", "currently accepting a small number", "west jordan"):
        if phrase in lower: errors.append(f"{rel}: stale/unsafe phrase {phrase!r}")
    claims_scan = lower.replace("does not guarantee savings", "")
    if re.search(r"\b(?:guarantee|guarantees|guaranteed|guaranteeing)\s+(?:savings|roi)\b", claims_scan):
        errors.append(f"{rel}: unsafe positive savings/ROI guarantee")

home=(ROOT/"index.html").read_text(encoding="utf-8")
for required in ("independent technology company", "/fleck/", "/consulting/", "25 years", "steven@getveld.ai"):
    if required.lower() not in home.lower(): errors.append(f"index.html: missing {required!r}")
consulting=(ROOT/"consulting/index.html").read_text(encoding="utf-8")
for required in ("not a free audit", "no change", "paid assessment", "does not guarantee savings"):
    if required.lower() not in consulting.lower(): errors.append(f"consulting: missing {required!r}")
privacy=(ROOT/"privacy/index.html").read_text(encoding="utf-8")
for required in ("does not currently provide an account", "does not currently add site-controlled analytics", "Fleck Privacy Policy", "Google Workspace"):
    if required.lower() not in privacy.lower(): errors.append(f"privacy: missing {required!r}")
terms=(ROOT/"terms/index.html").read_text(encoding="utf-8")
for required in ("does not create a consulting relationship", "separate written agreement", "Fleck Terms of Use"):
    if required.lower() not in terms.lower(): errors.append(f"terms: missing {required!r}")

manifest=json.loads((ROOT/"site.webmanifest").read_text(encoding="utf-8"))
if "AI that pays back" in manifest.get("description",""): errors.append("manifest: stale positioning")
if (ROOT/"CNAME").read_text().strip() != "getveld.ai": errors.append("CNAME changed")

if errors:
    print(json.dumps({"ok":False,"errors":errors},indent=2)); sys.exit(1)
print(json.dumps({"ok":True,"pages_checked":len(PAGES),"required_files":len(REQUIRED)},indent=2))
