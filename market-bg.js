/* Asset Rama — cinematic light background for the homepage hero (v2, 24/09/2026).
   Pure canvas atmosphere: slow drifting light fields, cinematic vignette, floor shadow.
   No objects, no chart props — the premium look of film lighting, not clip-art.
   A few KB, no video file, page speed and SEO untouched. */
(function () {
  "use strict";
  var canvas = document.getElementById("market-bg");
  if (!canvas || !canvas.getContext) return;
  var ctx = canvas.getContext("2d");
  if (!ctx) return;
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  var W = 0, H = 0;
  function resize() {
    var hero = canvas.parentElement || document.querySelector(".hero");
    W = hero.clientWidth; H = hero.clientHeight;
    var dpr = Math.min(window.devicePixelRatio || 1, 1.5);
    canvas.width = Math.round(W * dpr); canvas.height = Math.round(H * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  }

  var t = 0, running = false, raf = 0, visible = true;

  /* Light fields, lit like the reference footage: key light upper-right,
     deep blue fill low, faint warm rim on the far edge. They breathe and
     drift so slowly it feels like cloud movement, not animation. */
  var FIELDS = [
    { x: 0.80, y: 0.24, r: 0.55, c: "58,196,150", a: 0.11, sx: 0.020, sy: 0.013, px: 0.0, py: 0.0 },
    { x: 0.64, y: 0.88, r: 0.62, c: "46,98,196",  a: 0.07, sx: 0.015, sy: 0.010, px: 1.7, py: 0.8 },
    { x: 0.95, y: 0.68, r: 0.40, c: "200,130,64", a: 0.040, sx: 0.017, sy: 0.012, px: 3.1, py: 2.2 }
  ];

  function draw() {
    ctx.clearRect(0, 0, W, H);
    var m = Math.max(W, H);
    for (var i = 0; i < FIELDS.length; i++) {
      var f = FIELDS[i];
      var x = (f.x + 0.030 * Math.sin(t * f.sx + f.px)) * W;
      var y = (f.y + 0.040 * Math.cos(t * f.sy + f.py)) * H;
      var R = f.r * m;
      var g = ctx.createRadialGradient(x, y, 0, x, y, R);
      g.addColorStop(0, "rgba(" + f.c + "," + f.a + ")");
      g.addColorStop(0.55, "rgba(" + f.c + "," + (f.a * 0.42).toFixed(3) + ")");
      g.addColorStop(1, "rgba(" + f.c + ",0)");
      ctx.fillStyle = g;
      ctx.fillRect(0, 0, W, H);
    }
    /* Cinematic vignette: quiet corners, the eye led to the headline. */
    var v = ctx.createRadialGradient(W * 0.42, H * 0.46, Math.min(W, H) * 0.30, W * 0.42, H * 0.46, m * 0.80);
    v.addColorStop(0, "rgba(7,12,14,0)");
    v.addColorStop(1, "rgba(7,12,14,0.38)");
    ctx.fillStyle = v;
    ctx.fillRect(0, 0, W, H);
    /* Floor shadow so the hero melts into the page below. */
    var fg = ctx.createLinearGradient(0, H * 0.78, 0, H);
    fg.addColorStop(0, "rgba(10,17,20,0)");
    fg.addColorStop(1, "rgba(10,17,20,0.50)");
    ctx.fillStyle = fg;
    ctx.fillRect(0, H * 0.78, W, H * 0.22);
  }

  function frame() {
    if (!running) return;
    if (visible && !document.hidden) { t += 1 / 60; draw(); }
    raf = window.requestAnimationFrame(frame);
  }

  try {
    resize();
    window.addEventListener("resize", function () { resize(); if (reduce) draw(); }, { passive: true });
    if ("IntersectionObserver" in window) {
      new IntersectionObserver(function (e) { visible = !!e[0].isIntersecting; }, { threshold: 0.02 })
        .observe(canvas.parentElement || canvas);
    }
    if (reduce) { draw(); }
    else { running = true; raf = window.requestAnimationFrame(frame); }
  } catch (e) { /* decorative only — never break the page */ }
})();
