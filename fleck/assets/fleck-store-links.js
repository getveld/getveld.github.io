/*
 * Launch switch: replace GOOGLE_PLAY_URL_PENDING below with the verified,
 * public Google Play listing URL. Every Google Play CTA is populated from
 * this single value. Do not use a guessed or authenticated Console URL.
 */
const FLECK_GOOGLE_PLAY_URL = "GOOGLE_PLAY_URL_PENDING";

(function configureStoreLinks() {
  const pending = FLECK_GOOGLE_PLAY_URL === "GOOGLE_PLAY_URL_PENDING";

  document.querySelectorAll("[data-google-play-cta]").forEach((placeholder) => {
    if (pending) {
      placeholder.setAttribute("aria-disabled", "true");
      placeholder.setAttribute("title", "Google Play link will be added after the public listing is verified");
      return;
    }

    const link = document.createElement("a");
    link.className = placeholder.className.replace("button-pending", "").trim();
    link.href = FLECK_GOOGLE_PLAY_URL;
    link.rel = "noopener noreferrer";
    link.textContent = "Get it on Google Play";
    link.setAttribute("data-google-play-cta", "");
    placeholder.replaceWith(link);
  });

  document.querySelectorAll("[data-google-play-link]").forEach((placeholder) => {
    if (pending) {
      placeholder.setAttribute("aria-disabled", "true");
      placeholder.setAttribute("title", "Google Play link will be added after the public listing is verified");
      return;
    }

    const link = document.createElement("a");
    link.className = placeholder.className;
    link.href = FLECK_GOOGLE_PLAY_URL;
    link.rel = "noopener noreferrer";
    link.textContent = placeholder.textContent;
    link.setAttribute("data-google-play-link", "");
    placeholder.replaceWith(link);
  });
})();
