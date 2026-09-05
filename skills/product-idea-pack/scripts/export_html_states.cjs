#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const { pathToFileURL } = require('url');
let chromium;
try {
  ({ chromium } = require('playwright'));
} catch (error) {
  console.error('Playwright is not available. Use an equivalent browser capture tool or install the declared development dependency with the user\'s permission.');
  process.exit(3);
}

const [
  input,
  outputDirectory,
  slug = 'prototype-screen',
  viewportSpec = '1672x941',
  captureMode = 'auto'
] = process.argv.slice(2);
if (!input || !outputDirectory) {
  console.error('Usage: export_html_states.cjs <prototype.html> <output-directory> [slug] [WIDTHxHEIGHT] [auto|product|page|viewport]');
  process.exit(2);
}

const viewportMatch = /^(\d+)x(\d+)$/.exec(viewportSpec);
if (!viewportMatch) {
  console.error(`Invalid viewport: ${viewportSpec}. Use WIDTHxHEIGHT, for example 390x844.`);
  process.exit(2);
}
const viewport = { width: Number(viewportMatch[1]), height: Number(viewportMatch[2]) };
if (viewport.width < 240 || viewport.height < 240) {
  console.error(`Viewport is too small: ${viewportSpec}.`);
  process.exit(2);
}
if (!['auto', 'product', 'page', 'viewport'].includes(captureMode)) {
  console.error(`Invalid capture mode: ${captureMode}. Use auto, product, page or viewport.`);
  process.exit(2);
}

const inputPath = path.resolve(input);
const outputPath = path.resolve(outputDirectory);
if (!fs.existsSync(inputPath)) {
  console.error(`Prototype not found: ${inputPath}`);
  process.exit(2);
}
fs.mkdirSync(outputPath, { recursive: true });

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({
    viewport,
    colorScheme: 'light',
    deviceScaleFactor: 1
  });
  const errors = [];
  page.on('pageerror', error => errors.push(error.message));
  await page.goto(pathToFileURL(inputPath).href);
  await page.evaluate(() => {
    window.scrollTo(0, 0);
    document.documentElement.dataset.exportMode = 'true';
    if (document.activeElement instanceof HTMLElement) document.activeElement.blur();
  });

  const stateCount = await page.locator('[data-stage-button]').count();
  if (stateCount < 1) throw new Error('No [data-stage-button] controls found.');

  for (let index = 0; index < stateCount; index += 1) {
    await page.evaluate(position => {
      const control = document.querySelector(`[data-stage-button="${position}"]`);
      if (!control) throw new Error(`Missing stage control ${position}`);
      control.click();
      window.scrollTo(0, 0);
    }, index);
    await page.waitForTimeout(80);
    await page.evaluate(() => {
      window.scrollTo(0, 0);
      document.documentElement.scrollTop = 0;
      document.body.scrollTop = 0;
      const root = document.querySelector('[data-prototype-root]');
      if (root) root.scrollTop = 0;
      if (document.activeElement instanceof HTMLElement) document.activeElement.blur();
    });
    await page.waitForTimeout(40);
    await page.evaluate(() => window.scrollTo(0, 0));
    const filename = `${slug}-${String(index + 1).padStart(2, '0')}.png`;
    const outputFile = path.join(outputPath, filename);
    const product = page.locator('[data-prototype-capture]').first();
    const hasProductCapture = await product.count() > 0;
    if (captureMode === 'product' || (captureMode === 'auto' && hasProductCapture)) {
      if (!hasProductCapture) throw new Error('Capture mode product requires [data-prototype-capture].');
      await product.screenshot({ path: outputFile });
    } else if (captureMode === 'viewport') {
      await page.screenshot({ path: outputFile });
    } else {
      await page.screenshot({ path: outputFile, fullPage: true });
    }
  }

  if (errors.length) throw new Error(`Page errors: ${errors.join('; ')}`);
  await browser.close();
  console.log(`Exported ${stateCount} states at ${viewportSpec} (${captureMode}) to ${outputPath}`);
})().catch(error => {
  console.error(error.message);
  process.exit(1);
});
