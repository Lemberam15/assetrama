/* Asset Rama — cinematic market background for the homepage hero (24/09/2026).
   Pure canvas, a few KB — no video file, so page speed and SEO are untouched. */
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

  function rnd(i) { var x = Math.sin(i * 127.1 + 311.7) * 43758.5453; return x - Math.floor(x); }

  var NC = 26, candles = [];
  function initCandles() {
    candles = [];
    for (var i = 0; i < NC; i++) {
      candles.push({
        h: 0.22 + rnd(i) * 0.55,
        up: rnd(i + 80) > 0.42,
        ph: rnd(i + 120) * Math.PI * 2,
        sp: 0.10 + rnd(i + 160) * 0.15
      });
    }
  }

  var t = 0, running = false, raf = 0, visible = true;

  function draw() {
    ctx.clearRect(0, 0, W, H);

    /* moody aurora sky (like the cinematic reference) */
    var a = [
      { x: 0.82 + 0.04 * Math.cos(t * 0.07), y: 0.24 + 0.05 * Math.sin(t * 0.13), r: 0.50, c: "60,201,154", al: 0.09 },
      { x: 0.66 + 0.05 * Math.sin(t * 0.05), y: 0.78 + 0.05 * Math.cos(t * 0.08), r: 0.44, c: "62,120,220", al: 0.05 },
      { x: 0.50 + 0.05 * Math.sin(t * 0.09), y: 0.95 + 0.04 * Math.cos(t * 0.06), r: 0.40, c: "180,70,43", al: 0.04 }
    ];
    for (var i = 0; i < a.length; i++) {
      var b = a[i], R = b.r * Math.max(W, H);
      var g = ctx.createRadialGradient(b.x * W, b.y * H, 0, b.x * W, b.y * H, R);
      g.addColorStop(0, "rgba(" + b.c + "," + b.al + ")");
      g.addColorStop(1, "rgba(" + b.c + ",0)");
      ctx.fillStyle = g;
      ctx.fillRect(0, 0, W, H);
    }

    /* faint chart-paper grid */
    ctx.strokeStyle = "rgba(140,170,165,0.05)";
    ctx.lineWidth = 1;
    for (var y = 60; y < H; y += 60) { ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(W, y); ctx.stroke(); }

    /* gently breathing candlesticks along the bottom */
    var cw = W / (NC + 1), bodyW = Math.max(6, cw * 0.34);
    for (var c = 0; c < NC; c++) {
      var k = candles[c];
      var life = Math.sin(t * k.sp + k.ph);
      var grow = Math.sin(t * 0.08 + c * 0.55) * 0.5 + 0.5;
      var hf = k.h * (0.72 + 0.28 * grow) * (0.85 + 0.15 * life);
      var ch = hf * H * 0.62;
      var cx = cw * (c + 0.5) + cw * 0.5;
      var baseY = H * 1.02;
      var up = (Math.sin(t * 0.05 + c * 1.7) + Math.sin(t * k.sp * 1.3 + k.ph) * 0.6) > 0 ? k.up : !k.up;
      var col = up ? "60,201,154" : "196,86,60";
      var al = 0.08 + 0.05 * ((c / NC) * 0.5 + 0.5);
      ctx.strokeStyle = "rgba(" + col + "," + (al * 0.7) + ")";
      ctx.lineWidth = 2;
      ctx.beginPath(); ctx.moveTo(cx, baseY - ch - 14); ctx.lineTo(cx, baseY); ctx.stroke();
      ctx.fillStyle = "rgba(" + col + "," + al + ")";
      ctx.fillRect(cx - bodyW / 2, baseY - ch, bodyW, ch);
    }

    /* the flowing, gently rising market line */
    var midY = H * 0.56, amp = H * 0.15, PTS = 90;
    ctx.beginPath();
    for (var p = 0; p < PTS; p++) {
      var fx = p / (PTS - 1);
      var drift = Math.sin(fx * 5.1 + t * 0.16) * 0.34 + Math.sin(fx * 11.3 - t * 0.11) * 0.18;
      var py = midY + (drift - 0.62 * fx) * amp;
      if (p === 0) ctx.moveTo(fx * W, py); else ctx.lineTo(fx * W, py);
    }
    ctx.lineJoin = "round";
    ctx.strokeStyle = "rgba(96,201,154,0.08)"; ctx.lineWidth = 7; ctx.stroke();
    ctx.strokeStyle = "rgba(96,201,154,0.30)"; ctx.lineWidth = 2.5; ctx.stroke();

    /* bottom fade so everything melts into the page */
    var fg = ctx.createLinearGradient(0, H * 0.80, 0, H);
    fg.addColorStop(0, "rgba(10,17,20,0)");
    fg.addColorStop(1, "rgba(10,17,20,0.55)");
    ctx.fillStyle = fg;
    ctx.fillRect(0, H * 0.80, W, H * 0.20);
  }

  function frame() {
    if (!running) return;
    if (visible && !document.hidden) { t += 1 / 60; draw(); }
    raf = window.requestAnimationFrame(frame);
  }

  try {
    resize();
    initCandles();
    window.addEventListener("resize", function () { resize(); if (reduce) draw(); }, { passive: true });
    if ("IntersectionObserver" in window) {
      new IntersectionObserver(function (e) { visible = !!e[0].isIntersecting; }, { threshold: 0.02 })
        .observe(canvas.parentElement || canvas);
    }
    if (reduce) { draw(); }
    else { running = true; raf = window.requestAnimationFrame(frame); }
  } catch (e) { /* decorative only — never break the page */ }
})();
