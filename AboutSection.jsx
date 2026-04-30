// Stat block — 2px Moss left rule, semibold number, small moss label.
const Stat = ({ number, label }) => (
  <div className="stat">
    <div className="stat__number">{number}</div>
    <div className="stat__label">{label}</div>
  </div>
);

const AboutSection = () => (
  <section className="section" id="about" data-screen-label="About">
    <div className="about__grid">
      <div className="about__copy">
        <p className="section__label">About Veld</p>
        <h2 className="section__heading">Built by someone who&rsquo;s been the buyer.</h2>
        <p>Most AI companies are built by engineers who&rsquo;ve never had to get a system past a procurement team, a security review, or a change management committee.</p>
        <p>Veld was founded by Steven Davis &mdash; a CIO-turned-founder with over a decade as CIO. He&rsquo;s been on the buyer&rsquo;s side of the table. He knows what actually gets deployed &mdash; and what doesn&rsquo;t.</p>
        <p>That means every system we build is designed for the reality of enterprise deployment &mdash; security, compliance, and integration aren&rsquo;t added later. They&rsquo;re the starting point.</p>
      </div>
      <div className="about__stats">
        <Stat number="Three decades" label="in enterprise IT and technology leadership" />
        <Stat number="35"            label="Countries — the scale at which we've built and run systems" />
        <Stat number="10+"           label="Years as CIO — we know what procurement is going to ask" />
      </div>
    </div>
  </section>
);

Object.assign(window, { Stat, AboutSection });
