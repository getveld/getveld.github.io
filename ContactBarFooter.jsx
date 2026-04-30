// Moss strip — sits between the consulting band and the footer as a punctuation mark.
const ContactBar = () => (
  <div className="contact-bar">
    <p>Questions? Reach us at <a href="mailto:info@getveld.ai">info@getveld.ai</a> &mdash; our AI agent manages this inbox, with Steven in the loop on everything that matters.</p>
  </div>
);

const SiteFooter = () => (
  <footer className="site-footer">
    <div className="site-footer__inner">
      <div className="footer-brand">
        <Wordmark size="footer" />
        <p>Founded 2026</p>
      </div>
      <div className="footer-links">
        <a href="mailto:info@getveld.ai">info@getveld.ai</a>
        <a href="#privacy">Privacy Policy</a>
        <a href="#terms">Terms of Service</a>
      </div>
    </div>
    <div className="footer-bottom">&copy; 2026 Veld, LLC. All rights reserved.</div>
  </footer>
);

Object.assign(window, { ContactBar, SiteFooter });
