/* ============================================================
   ASSET RAMA — premium scroll-reveal (vfx.js)
   Progressive enhancement, ~1.4 KB, no libraries.
   QC rules:
   - This script is the ONLY thing that hides elements (by adding
     .vfx-reveal). If it never loads, nothing is ever hidden.
   - After each element finishes revealing, all vfx classes and
     the inline delay are removed, so hover transitions return to
     their original speed.
   - Honours prefers-reduced-motion (exits immediately).
   - Capped at 80 elements, one observer, unobserved after reveal.
   ============================================================ */
(function () {
  "use strict";
  if (window.matchMedia &&
      window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  if (!("IntersectionObserver" in window)) return;

  var els = Array.prototype.slice.call(
    document.querySelectorAll(".card, .panel")
  ).slice(0, 80);
  if (!els.length) return;

  var counts = Object.create(null);
  els.forEach(function (el) {
    el.classList.add("vfx-reveal");
    var key = el.parentElement ? el.parentElement.className || "root" : "root";
    counts[key] = (counts[key] || 0) + 1;
    /* small stagger inside each grid, never longer than ~280ms */
    el.style.transitionDelay =
      Math.min(((counts[key] - 1) % 4) * 70, 280) + "ms";
  });

  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (!e.isIntersecting) return;
      var el = e.target;
      io.unobserve(el);
      el.classList.add("vfx-in");
      /* clean up so the page behaves 100% natively afterwards */
      setTimeout(function () {
        el.style.transitionDelay = "";
        el.classList.remove("vfx-reveal", "vfx-in");
      }, 750);
    });
  }, { threshold: 0.1, rootMargin: "0px 0px -6% 0px" });

  els.forEach(function (el) { io.observe(el); });
})();
