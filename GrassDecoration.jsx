// Decorative grass field — extracted verbatim from the hero of getveld.ai.
// Default 18% opacity. Pass `as="standalone"` to drop the absolute positioning
// and use it as a regular block element.
const GrassDecoration = ({ opacity = 0.18, stroke = "#5F7768", className = "", style = {} }) => (
  <svg
    className={className}
    style={{ opacity, ...style }}
    viewBox="0 0 800 600"
    preserveAspectRatio="xMaxYMax meet"
    fill="none"
    xmlns="http://www.w3.org/2000/svg"
    stroke={stroke}
    strokeLinecap="round"
  >
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

Object.assign(window, { GrassDecoration });
