// node render.js in.html out.pdf  — HTML (1280x720 px слайды) -> PDF 960x540 pt
const { chromium } = require(process.env.PWCORE || 'playwright-core');
const path = require('path');
(async () => {
  const [inp, out] = process.argv.slice(2);
  const browser = await chromium.launch({ executablePath: process.env.CHROME || '/opt/pw-browsers/chromium-1194/chrome-linux/chrome', args: ['--no-sandbox'] });
  const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
  await page.goto('file://' + path.resolve(inp));
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(300);
  // проверка переполнения: любой блок, вылезающий за слайд
  const bad = await page.evaluate(() => {
    const res = [];
    document.querySelectorAll('.slide').forEach((s, i) => {
      const sr = s.getBoundingClientRect();
      s.querySelectorAll('*').forEach(el => {
        const r = el.getBoundingClientRect();
        if (r.width && (r.bottom > sr.bottom + 1 || r.right > sr.right + 1)) res.push(`slide ${i + 1}: <${el.tagName.toLowerCase()} class="${el.className && el.className.baseVal === undefined ? el.className : ''}"> bottom=${Math.round(r.bottom - sr.top)}`);
      });
      // пересечение левой колонки с панелью / нижним краем
      const left = s.querySelector('.left');
      if (left) { const r = left.getBoundingClientRect(); if (r.bottom - sr.top > 704) res.push(`slide ${i + 1}: .left bottom=${Math.round(r.bottom - sr.top)}`); }
    });
    return res;
  });
  if (bad.length) console.log('OVERFLOW:\n' + bad.slice(0, 20).join('\n')); else console.log('no overflow');
  await page.pdf({ path: out, width: '1280px', height: '720px', printBackground: true, preferCSSPageSize: true });
  await browser.close();
})();
