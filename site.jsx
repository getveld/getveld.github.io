// =========================================================
// Veld website kit — components
// React + JSX, transpiled in-browser by Babel.
// Each component is exported to window so it can be cherry-picked.
// =========================================================

// --- Wordmark ---------------------------------------------------------------
// Two variants:
//   B (primary)   — blade-mark + lowercase "veld" wordmark. Use everywhere by default.
//   A (alternate) — wordmark only. Use when real-estate is tight (favicons, app icons,
//                   dense UI where the mark would shrink below ~14px tall).
// Locked geometry: blades stroke 1.5, length 35% (anchored at bottom).
// Per `Veld Logo Brand Assets Reference`:
//   light bg → blades Deep Field (#23382F), wordmark Deep Field (#23382F)
//   dark bg  → blades Soft Sage (#AAB8AE),  wordmark Soft Sage (#AAB8AE)
function Wordmark({ size = "md", tone = "light", variant = "B", className = "", ...rest }) {
  // Sizes already include the 35% scale-down for the blade-mark.
  // Natural sizes (32 / 22 / 48) × 0.35 = rendered svg dimensions.
  const sizes = {
    sm: { w: 7.7,  h: 11.16, fs: "1rem" },
    md: { w: 11.2, h: 16.24, fs: "1.125rem" },
    lg: { w: 16.8, h: 24.36, fs: "1.5rem" },
  };
  const s = sizes[size] || sizes.md;
  const stroke = tone === "dark" ? "#AAB8AE" : "#23382F";
  const wordColor = tone === "dark" ? "#AAB8AE" : "#23382F";
  return (
    <a className={`wordmark-link ${className}`} {...rest}>
      {variant === "B" && (
        <svg width={s.w} height={s.h} viewBox="11 9 20 29" fill="none" aria-hidden="true">
          <path d="M15 37 Q13 26 21 20" stroke={stroke} strokeWidth="1.5" strokeLinecap="round"/>
          <path d="M27 37 Q29 24 23 10" stroke={stroke} strokeWidth="1.5" strokeLinecap="round"/>
        </svg>
      )}
      <span className={tone === "dark" ? "footer-wordmark" : "wordmark-text"} style={{ fontSize: s.fs, color: wordColor }}>
        veld
      </span>
    </a>
  );
}

// --- GrassField -------------------------------------------------------------
// The decorative 9-blade SVG that lives in the hero. 18% opacity, right-aligned.
function GrassField({ className = "" }) {
  return (
    <svg className={className} viewBox="0 0 800 600" preserveAspectRatio="xMaxYMax meet"
         fill="none" stroke="#5F7768" strokeLinecap="round" aria-hidden="true">
      <path d="M62 600 Q57 478 72 382" strokeWidth="3"/>
      <path d="M122 600 Q155 455 84 342" strokeWidth="3"/>
      <path d="M208 600 C190 498 234 418 200 330" strokeWidth="5"/>
      <path d="M295 600 Q255 450 375 315" strokeWidth="4"/>
      <path d="M378 600 C360 488 415 400 368 288" strokeWidth="7"/>
      <path d="M464 600 Q456 452 482 262" strokeWidth="6"/>
      <path d="M554 600 C525 474 605 385 558 242" strokeWidth="9"/>
      <path d="M660 600 Q622 438 722 220" strokeWidth="11"/>
      <path d="M756 600 Q818 440 722 198" strokeWidth="10"/>
    </svg>
  );
}

// --- Button -----------------------------------------------------------------
function Button({ kind = "primary", children, href, ...rest }) {
  const cls = `btn btn--${kind}`;
  if (href) return <a href={href} className={cls} {...rest}>{children}</a>;
  return <button className={cls} {...rest}>{children}</button>;
}

// --- Type micro-components --------------------------------------------------
const Eyebrow = ({ children, className = "" }) => <p className={`hero__eyebrow ${className}`}>{children}</p>;
const Label   = ({ children, className = "" }) => <p className={`section__label ${className}`}>{children}</p>;

// --- Cards ------------------------------------------------------------------
function ProductCard({ tag, title, children }) {
  return (
    <div className="product-card">
      <p className="product-card__tag">{tag}</p>
      <h3>{title}</h3>
      <p>{children}</p>
    </div>
  );
}

function OfferCard({ badge, title, children }) {
  return (
    <div className="offer-card">
      <p className="offer-card__badge">{badge}</p>
      <h3>{title}</h3>
      <p>{children}</p>
    </div>
  );
}

// --- Stat -------------------------------------------------------------------
function Stat({ number, label }) {
  return (
    <div className="stat">
      <div className="stat__number">{number}</div>
      <div className="stat__label">{label}</div>
    </div>
  );
}

// --- SiteHeader -------------------------------------------------------------
function SiteHeader() {
  return (
    <header className="site-header">
      <div className="site-header__inner">
        <Wordmark size="md" tone="light" href="#" />
        <nav className="site-nav">
          <a href="#about">About</a>
          <a href="#products">Products</a>
          <a href="#consulting">Consulting</a>
          <a href="mailto:info@getveld.ai" className="nav-cta">Get in touch</a>
        </nav>
      </div>
    </header>
  );
}

// --- Hero -------------------------------------------------------------------
// Mirrors live getveld.ai (2026-04-29 source of truth): no tagline rendered
// in the hero — the .hero__tagline CSS slot exists but is currently empty.
// Decision Record taglines are ratified-but-not-deployed.
function Hero() {
  return (
    <section className="hero">
      <GrassField className="hero__grass" />
      <div className="hero__inner">
        <Eyebrow>Founded 2026. Perspective 1997.</Eyebrow>
        <h1>We&rsquo;ve been inside a revolution before.</h1>
        <p className="hero__sub">
          Steven Davis started his career at Netscape in 1997, at the dawn of the internet. He spent
          three decades in enterprise IT learning what technology actually delivers &mdash; and what
          just demos well. This moment in AI feels exactly like that one. Veld is built with that
          perspective.
        </p>
        <div className="hero__actions">
          <Button kind="primary" href="mailto:info@getveld.ai">Start the conversation &rarr;</Button>
          <Button kind="ghost" href="#products">See our work</Button>
        </div>
      </div>
    </section>
  );
}

// --- AboutSection -----------------------------------------------------------
function AboutSection() {
  return (
    <section className="section" id="about">
      <div className="about__grid">
        <div className="about__copy">
          <Label>About Veld</Label>
          <h2 className="section__heading">Built by someone who's been the buyer.</h2>
          <p>Most AI companies are built by engineers who've never had to get a system past a procurement team, a security review, or a change management committee.</p>
          <p>Veld was founded by Steven Davis &mdash; a CIO-turned-founder with over a decade as CIO. He's been on the buyer's side of the table. He knows what actually gets deployed &mdash; and what doesn't.</p>
          <p>That means every system we build is designed for the reality of enterprise deployment &mdash; security, compliance, and integration aren't added later. They're the starting point.</p>
        </div>
        <div className="about__stats">
          <Stat number="Three decades" label="in enterprise IT and technology leadership" />
          <Stat number="35" label="Countries — the scale at which we've built and run systems" />
          <Stat number="10+" label="Years as CIO — we know what procurement is going to ask" />
        </div>
      </div>
    </section>
  );
}

// --- ProductsSection --------------------------------------------------------
function ProductsSection() {
  return (
    <section className="section section--alt" id="products">
      <div className="products__inner">
        <Label>Products</Label>
        <h2 className="section__heading" style={{ marginBottom: "1rem" }}>
          Building AI products, not just advising on them.
        </h2>
        <p style={{ color: "var(--veld-moss)", maxWidth: "56ch", marginBottom: "2.5rem" }}>
          Every product we build is a live test of what AI actually delivers. Here's what we're working on.
        </p>
        <div className="products__grid">
          <ProductCard tag="iOS — Coming Soon" title="Fleck AI Journal">
            An AI-powered personal journal. Speak your thoughts; Fleck writes your story.
          </ProductCard>
          <ProductCard tag="In Development" title="Fleck Collective">
            Turns individual contributions from conferences, corporate retreats, and live events into a collective narrative — for every attendee and the organizer. First deployment: June 2026.
          </ProductCard>
          <ProductCard tag="Early Stage · Long-Term Research" title="Virtual Boardroom">
            What does it look like when AI agents aren't tools you prompt, but colleagues you work with — in real meetings, with real roles? We're building toward that.
          </ProductCard>
        </div>
      </div>
    </section>
  );
}

// --- ConsultingSection ------------------------------------------------------
function ConsultingSection() {
  return (
    <section className="section consulting" id="consulting">
      <div className="consulting__inner">
        <Label>Consulting</Label>
        <h2 className="section__heading">The CIO who's now the builder. That's your consultant.</h2>
        <p style={{ color: "var(--veld-soft-sage)", maxWidth: "56ch", marginTop: "0.5rem" }}>
          Steven spent over a decade as a CIO &mdash; approving or rejecting the exact systems vendors were pitching him. Now he builds them. That's a different kind of consulting.
        </p>
        <div className="consulting__grid">
          <OfferCard badge="Where most clients start" title="Pilot Implementation">
            A scoped, working AI system deployed for your team in 30–60 days. You end with something real running in your environment — not a slide deck. Built with your security and integration requirements as first-class constraints.
          </OfferCard>
          <OfferCard badge="Ongoing support" title="Fractional AI Leadership">
            Monthly strategy and iteration support after implementation. We work with your leadership team regularly — advising on AI direction, evaluating new tools, and evolving what's been built.
          </OfferCard>
          <OfferCard badge="Start here" title="AI Strategy & Roadmap">
            Not sure where to start? A scoped discovery engagement — we learn your organization, map AI opportunities, and deliver a prioritized roadmap. The right starting point before committing to implementation.
          </OfferCard>
        </div>
        <div className="consulting__cta">
          <p>Currently accepting a small number of pilot clients at reduced rates &mdash; in exchange for serving as a reference.</p>
          <Button kind="primary" href="mailto:info@getveld.ai">Start the conversation &rarr;</Button>
        </div>
      </div>
    </section>
  );
}

// --- ContactBar -------------------------------------------------------------
function ContactBar() {
  return (
    <div className="contact-bar">
      <p>
        Questions? Reach us at{" "}
        <a href="mailto:info@getveld.ai">info@getveld.ai</a>
        {" "}&mdash; our AI agent manages this inbox, with Steven in the loop on everything that matters.
      </p>
    </div>
  );
}

// --- SiteFooter -------------------------------------------------------------
function SiteFooter() {
  return (
    <footer className="site-footer">
      <div className="site-footer__inner">
        <div className="footer-brand">
          <Wordmark size="sm" tone="dark" href="#" className="footer-brand-link" />
          <p>Founded 2026</p>
        </div>
        <div className="footer-links">
          <a href="mailto:info@getveld.ai">info@getveld.ai</a>
          <a href="/privacy.html">Privacy Policy</a>
          <a href="/terms.html">Terms of Service</a>
        </div>
      </div>
      <div className="footer-bottom">&copy; 2026 Veld, LLC. All rights reserved.</div>
    </footer>
  );
}

// --- App --------------------------------------------------------------------
function App() {
  return (
    <React.Fragment>
      <SiteHeader />
      <Hero />
      <AboutSection />
      <hr className="divider" />
      <ProductsSection />
      <ConsultingSection />
      <ContactBar />
      <SiteFooter />
    </React.Fragment>
  );
}

// expose for cherry-picking
Object.assign(window, {
  Wordmark, GrassField, Button, Eyebrow, Label,
  ProductCard, OfferCard, Stat,
  SiteHeader, Hero, AboutSection, ProductsSection,
  ConsultingSection, ContactBar, SiteFooter, App
});

ReactDOM.createRoot(document.getElementById("root")).render(<App />);
