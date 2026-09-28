#!/usr/bin/env node
/* Automated carousel renderer + DOM AUDIT.
 * Renders cards with Chromium and audits them INSIDE the browser:
 * out-of-bounds elements, text overflow, content/footer collisions,
 * disclaimer presence. Writes audit.json. Exit code 1 if any card fails. */
const puppeteer = require('puppeteer-core');
const fs = require('fs');

(async () => {
  const htmlPath = process.argv[2];
  const outdir = process.argv[3] || 'carousel_build';
  fs.mkdirSync(outdir, {recursive: true});
  const browser = await puppeteer.launch({
    executablePath: '/usr/local/bin/chromium-headless-shell',
    args: ['--no-sandbox', '--disable-gpu', '--hide-scrollbars', '--force-device-scale-factor=1', '--allow-file-access-from-files']
  });
  const page = await browser.newPage();
  await page.setViewport({width: 1100, height: 1400});
  await page.goto('file://' + htmlPath, {waitUntil: 'networkidle0'});
  await page.evaluateHandle('document.fonts.ready');
  await new Promise(r => setTimeout(r, 400));

  // ---- DOM AUDIT ----
  const audit = await page.evaluate(() => {
    const result = {cards: [], pass: true};
    document.querySelectorAll('.card').forEach((card, ci) => {
      const cr = card.getBoundingClientRect();
      const issues = [];
      card.querySelectorAll('.inner *').forEach(el => {
        if (el.classList.contains('glow') || el.classList.contains('steps')) return;
        const t = (el.textContent || '').trim();
        const r = el.getBoundingClientRect();
        if (!t || r.width === 0 || r.height === 0) return;
        if (r.left < cr.left - 1 || r.right > cr.right + 1 || r.top < cr.top - 1 || r.bottom > cr.bottom + 1)
          issues.push(`OUT-OF-BOUNDS ${el.tagName}.${el.className}: "${t.slice(0, 24)}"`);
        if (el.scrollWidth > el.clientWidth + 3 && el.clientWidth > 0)
          issues.push(`TEXT-OVERFLOW ${el.tagName}.${el.className}: "${t.slice(0, 24)}"`);
      });
      const foot = card.querySelector('.pagefoot');
      const footTop = foot ? foot.getBoundingClientRect().top : cr.bottom;
      let contentBottom = 0;
      card.querySelectorAll('.inner > *').forEach(el => {
        if (el.classList.contains('pagefoot')) return;
        contentBottom = Math.max(contentBottom, el.getBoundingClientRect().bottom);
      });
      const gap = Math.round(footTop - contentBottom);
      if (gap < 12) issues.push(`CONTENT-FOOTER GAP ${gap}px < 12px`);
      const site = card.querySelector('.site');
      if (!site || !/educational only/i.test(site.textContent)) issues.push('DISCLAIMER-MISSING');
      if (issues.length) result.pass = false;
      result.cards.push({card: ci + 1, gap, issues});
    });
    result.width = document.querySelector('.card').getBoundingClientRect().width;
    result.height = document.querySelector('.card').getBoundingClientRect().height;
    return result;
  });
  fs.writeFileSync(outdir + '/audit.json', JSON.stringify(audit, null, 1));

  const cards = await page.$$('.card');
  for (let i = 0; i < cards.length; i++)
    await cards[i].screenshot({path: `${outdir}/card_${i + 1}.png`});
  await browser.close();
  console.log(JSON.stringify(audit, null, 1));
  process.exit(audit.pass ? 0 : 2);
})();
