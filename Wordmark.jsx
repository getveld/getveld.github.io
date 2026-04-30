// Veld lockup — Variant B (blade + wordmark) is primary; Variant A (wordmark only)
// is the alternate for tight real-estate (favicons, app icons, dense UI).
//
// Locked geometry: canonical two-blade paths (unchanged), stroke 1.5,
// rendered at 35% of natural size relative to the wordmark. The "natural"
// header size is 32×46 viewBox-1:1; we render at 32 × 0.35 = ~11×16.
const Wordmark = ({ size = "header", variant = "B", as = "a", href = "#", style }) => {
  // each preset: w/h are the rendered SVG dimensions (already 35%-scaled).
  // textCls drives wordmark font-size via existing CSS classes.
  const sizes = {
    header: { w: 11.2, h: 16.24, stroke: "#23382F", textCls: "wordmark-text",  cls: "wordmark-link"     },
    footer: { w: 7.7,  h: 11.16, stroke: "#AAB8AE", textCls: "footer-wordmark", cls: "footer-brand-link" },
  };
  const s = sizes[size] ?? sizes.header;
  const Tag = as;
  return (
    <Tag href={href} className={s.cls} style={style}>
      {variant === "B" && (
        <svg width={s.w} height={s.h} viewBox="11 9 20 29" fill="none" aria-hidden="true">
          <path d="M15 37 Q13 26 21 20" stroke={s.stroke} strokeWidth="1.5" strokeLinecap="round"/>
          <path d="M27 37 Q29 24 23 10" stroke={s.stroke} strokeWidth="1.5" strokeLinecap="round"/>
        </svg>
      )}
      <span className={s.textCls}>veld</span>
    </Tag>
  );
};

Object.assign(window, { Wordmark });
