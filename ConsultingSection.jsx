// Consulting — Deep Field band, translucent overlay cards, single primary CTA.
const OfferCard = ({ badge, title, children }) => (
  <div className="offer-card">
    <p className="offer-card__badge">{badge}</p>
    <h3>{title}</h3>
    <p>{children}</p>
  </div>
);

const ConsultingSection = () => (
  <section className="section consulting" id="consulting" data-screen-label="Consulting">
    <div className="consulting__inner">
      <p className="section__label">Consulting</p>
      <h2 className="section__heading">The CIO who&rsquo;s now the builder. That&rsquo;s your consultant.</h2>
      <p className="consulting__lede">Steven spent over a decade as a CIO &mdash; approving or rejecting the exact systems vendors were pitching him. Now he builds them. That&rsquo;s a different kind of consulting.</p>
      <div className="consulting__grid">
        <OfferCard badge="Where most clients start" title="Pilot Implementation">
          A scoped, working AI system deployed for your team in 30&ndash;60 days. You end with something real running in your environment &mdash; not a slide deck. Built with your security and integration requirements as first-class constraints.
        </OfferCard>
        <OfferCard badge="Ongoing support" title="Fractional AI Leadership">
          Monthly strategy and iteration support after implementation. We work with your leadership team regularly &mdash; advising on AI direction, evaluating new tools, and evolving what&rsquo;s been built.
        </OfferCard>
        <OfferCard badge="Start here" title="AI Strategy &amp; Roadmap">
          Not sure where to start? A scoped discovery engagement &mdash; we learn your organization, map AI opportunities, and deliver a prioritized roadmap. The right starting point before committing to implementation.
        </OfferCard>
      </div>
      <div className="consulting__cta">
        <p>Currently accepting a small number of pilot clients at reduced rates &mdash; in exchange for serving as a reference.</p>
        <Button variant="primary" href="mailto:info@getveld.ai">Start the conversation &rarr;</Button>
      </div>
    </div>
  </section>
);

Object.assign(window, { OfferCard, ConsultingSection });
