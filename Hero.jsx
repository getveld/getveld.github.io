// Hero — Deep Field surface, right-aligned grass field, eyebrow + h1 + sub + actions.
const Hero = () => (
  <section className="hero" id="top">
    <GrassDecoration className="hero__grass" />
    <div className="hero__inner">
      <p className="hero__eyebrow">Founded 2026. Perspective 1997.</p>
      <h1>We&rsquo;ve been inside a revolution before.</h1>
      <p className="hero__sub">
        Steven Davis started his career at Netscape in 1997, at the dawn of the internet.
        He spent three decades in enterprise IT learning what technology actually delivers
        &mdash; and what just demos well. This moment in AI feels exactly like that one.
        Veld is built with that perspective.
      </p>
      <div className="hero__actions">
        <Button variant="primary" href="mailto:info@getveld.ai">Start the conversation &rarr;</Button>
        <Button variant="ghost" href="#products">See our work</Button>
      </div>
    </div>
  </section>
);

Object.assign(window, { Hero });
