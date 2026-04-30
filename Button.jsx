// Buttons. Three variants matching the source CSS:
//   primary  — chalk on deep-field   (hero CTAs, consulting CTA)
//   ghost    — moss outline on dark  (hero secondary)
//   navCta   — deep-field on chalk   (header)
const Button = ({ variant = "primary", href, children, onClick, ...rest }) => {
  const cls = {
    primary: "btn btn--primary",
    ghost:   "btn btn--ghost",
    navCta:  "nav-cta",
  }[variant] ?? "btn";

  if (href) return <a href={href} className={cls} onClick={onClick} {...rest}>{children}</a>;
  return <button type="button" className={cls} onClick={onClick} {...rest}>{children}</button>;
};

Object.assign(window, { Button });
