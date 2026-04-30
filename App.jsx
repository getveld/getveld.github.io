// Top-level site composition.
const Site = () => (
  <>
    <SiteHeader />
    <Hero />
    <AboutSection />
    <hr className="divider" />
    <ProductsSection />
    <ConsultingSection />
    <ContactBar />
    <SiteFooter />
  </>
);

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(<Site />);
