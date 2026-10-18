#!/usr/bin/env node
const path = require('path');
let sharp;
try {
  sharp = require('sharp');
} catch (error) {
  console.error('Sharp is not available. Use an equivalent SVG renderer or install the declared development dependency with the user\'s permission.');
  process.exit(3);
}

const [input, output, widthArg = '1672', heightArg = '941'] = process.argv.slice(2);
if (!input || !output) {
  console.error('Usage: render_svg.cjs <input.svg> <output.png> [width] [height]');
  process.exit(2);
}

const width = Number(widthArg);
const height = Number(heightArg);
if (!Number.isInteger(width) || !Number.isInteger(height) || width < 1 || height < 1) {
  console.error('Width and height must be positive integers.');
  process.exit(2);
}

sharp(path.resolve(input), { density: 144 })
  .resize(width, height, { fit: 'fill' })
  .png()
  .toFile(path.resolve(output))
  .then(info => console.log(`Rendered ${info.width}x${info.height}: ${output}`))
  .catch(error => {
    console.error(error.message);
    process.exit(1);
  });
