// Products — light alt section. Each card is a small uppercase tag, h3, paragraph.
const ProductCard = ({ tag, title, children }) => (
  <div className="product-card">
    <p className="product-card__tag">{tag}</p>
    <h3>{title}</h3>
    <p>{children}</p>
  </div>
);

const ProductsSection = () => (
  <section className="section section--alt" id="products" data-screen-label="Products">
    <div className="products__inner">
      <p className="section__label">Products</p>
      <h2 className="section__heading" style={{ marginBottom: "1rem" }}>Building AI products, not just advising on them.</h2>
      <p className="products__lede">Every product we build is a live test of what AI actually delivers. Here&rsquo;s what we&rsquo;re working on.</p>
      <div className="products__grid">
        <ProductCard tag="iOS — Coming Soon" title="Fleck AI Journal">
          An AI-powered personal journal. Speak your thoughts; Fleck writes your story.
        </ProductCard>
        <ProductCard tag="In Development" title="Fleck Collective">
          Turns individual contributions from conferences, corporate retreats, and live events into a collective narrative &mdash; for every attendee and the organizer. First deployment: June 2026.
        </ProductCard>
        <ProductCard tag="Early Stage · Long-Term Research" title="Virtual Boardroom">
          What does it look like when AI agents aren&rsquo;t tools you prompt, but colleagues you work with &mdash; in real meetings, with real roles? We&rsquo;re building toward that.
        </ProductCard>
      </div>
    </div>
  </section>
);

Object.assign(window, { ProductCard, ProductsSection });
