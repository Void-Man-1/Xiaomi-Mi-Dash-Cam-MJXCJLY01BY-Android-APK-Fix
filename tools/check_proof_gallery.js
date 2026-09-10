const { chromium } = require('playwright');
const assert = require('node:assert/strict');
const fs = require('node:fs');

(async () => {
  fs.mkdirSync('proof-audit', { recursive: true });
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  const locales = ['/', '/pl/', '/uk/', '/de/', '/ru/'];
  const widths = [1440, 1024, 820, 390];

  for (const locale of locales) {
    for (const width of widths) {
      await page.setViewportSize({ width, height: 1000 });
      await page.goto(`http://127.0.0.1:8000${locale}`, { waitUntil: 'domcontentloaded' });
      await page.locator('.proof-section').scrollIntoViewIfNeeded();
      const result = await page.evaluate(() => {
        const gallery = document.querySelector('.gallery');
        const video = document.querySelector('.evidence-video video');
        const shots = [...document.querySelectorAll('.gallery .shot')];
        const stage = document.querySelector('.video-stage');
        const wrap = document.querySelector('.proof-section .wrap');
        const stageRect = stage.getBoundingClientRect();
        const wrapRect = wrap.getBoundingClientRect();
        return {
          viewport: document.documentElement.clientWidth,
          pageWidth: document.documentElement.scrollWidth,
          videoCount: document.querySelectorAll('.evidence-video video').length,
          controls: video?.controls,
          source: video?.querySelector('source')?.src || '',
          poster: video?.poster || '',
          cols: getComputedStyle(gallery).gridTemplateColumns.split(' ').filter(Boolean).length,
          shotWidths: shots.map(s => Math.round(s.getBoundingClientRect().width)),
          fits: shots.map(s => getComputedStyle(s.querySelector('img')).objectFit),
          captions: shots.map(s => getComputedStyle(s.querySelector('.shot-caption')).position),
          stageInsideWrap: stageRect.left >= wrapRect.left - 1 && stageRect.right <= wrapRect.right + 1,
        };
      });

      assert.ok(result.pageWidth <= result.viewport + 1, `${locale}@${width}: page overflow`);
      assert.equal(result.videoCount, 1, `${locale}@${width}: embedded video missing`);
      assert.equal(result.controls, true, `${locale}@${width}: controls missing`);
      assert.ok(result.source.endsWith('poco-f6-android16-v2.0.0-full-camera-test.mp4'));
      assert.ok(result.poster.endsWith('poco-f6-android16-v2.0.0-video-poster.jpg'));
      assert.equal(result.cols, width <= 820 ? 1 : 3, `${locale}@${width}: gallery columns`);
      assert.ok(Math.max(...result.shotWidths) - Math.min(...result.shotWidths) <= 1, `${locale}@${width}: unequal cards`);
      assert.ok(result.fits.every(v => v === 'contain'), `${locale}@${width}: screenshot cropping`);
      assert.ok(result.captions.every(v => v === 'static'), `${locale}@${width}: overlay caption`);
      assert.ok(result.stageInsideWrap, `${locale}@${width}: video escapes container`);
      console.log(`${locale} ${width}px OK`);
    }
  }

  await page.setViewportSize({ width: 1440, height: 1000 });
  await page.goto('http://127.0.0.1:8000/', { waitUntil: 'domcontentloaded' });
  await page.locator('.proof-section').scrollIntoViewIfNeeded();
  const video = page.locator('.evidence-video video');
  await video.evaluate(v => new Promise((resolve, reject) => {
    if (v.readyState >= 1) return resolve();
    const timer = setTimeout(() => reject(new Error('video metadata timeout')), 20000);
    v.addEventListener('loadedmetadata', () => { clearTimeout(timer); resolve(); }, { once: true });
    v.addEventListener('error', () => { clearTimeout(timer); reject(new Error('video load error')); }, { once: true });
    v.load();
  }));
  const media = await video.evaluate(v => ({ readyState: v.readyState, duration: v.duration, videoWidth: v.videoWidth, videoHeight: v.videoHeight }));
  assert.ok(media.readyState >= 1 && media.duration > 0 && media.videoWidth > 0 && media.videoHeight > 0, `invalid video metadata ${JSON.stringify(media)}`);
  console.log(`VIDEO OK ${media.videoWidth}x${media.videoHeight} ${media.duration.toFixed(2)}s`);
  await page.locator('.proof-section').screenshot({ path: 'proof-audit/proof-desktop.png' });

  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto('http://127.0.0.1:8000/', { waitUntil: 'domcontentloaded' });
  await page.locator('.proof-section').scrollIntoViewIfNeeded();
  await page.locator('.proof-section').screenshot({ path: 'proof-audit/proof-mobile.png' });

  await browser.close();
})().catch(err => { console.error(err); process.exit(1); });
