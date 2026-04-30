// Sticky chalk header — vertical lockup on the left, nav + CTA on the right.
const SiteHeader = () => (
  <header className="site-header">
    <div className="site-header__inner">
      <Wordmark size="header" href="#top" />
      <nav className="site-nav">
        <a href="#about">About</a>
        <a href="#products">Products</a>
        <a href="#consulting">Consulting</a>
        <Button variant="navCta" href="mailto:info@getveld.ai">Get in touch</Button>
      </nav>
    </div>
  </header>
);

Object.assign(window, { SiteHeader });
