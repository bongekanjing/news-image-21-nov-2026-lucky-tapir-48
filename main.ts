/**
 * 21 November 2026 — the day's world news in one image.
 *
 * The entry is the drawing in `entry.png`, made by `draw.py` beside this file.
 * This program's job is only to place that file where the house reads it, and
 * to refuse to hand over an image the gate would reject: better to fail loudly
 * here than to be scored 0 for a truncated or oversized file.
 *
 * Node 22, standard library only, no network.
 */

import { copyFileSync, mkdirSync, readFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

/** The house's limits on entry.png, as the rules state them. */
const MAX_BYTES = 1048576;
const MAX_SIDE = 1024;

const HERE = dirname(fileURLToPath(import.meta.url));
const OUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

/**
 * Reads the bytes, then checks them against the gate: a whole PNG (signature and
 * an IHDR whose width and height are within 1024), and at most 1 MiB.
 */
function checkedPng(path: string): Buffer {
  const bytes = readFileSync(path);

  if (bytes.length > MAX_BYTES) {
    throw new Error(`entry.png is ${bytes.length} bytes, over the ${MAX_BYTES} limit`);
  }

  // PNG signature: 89 50 4E 47 0D 0A 1A 0A
  const signature = [0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a];
  for (let i = 0; i < signature.length; i++) {
    if (bytes[i] !== signature[i]) {
      throw new Error('entry.png is not a PNG: its signature bytes are wrong');
    }
  }

  // IHDR is the first chunk: 8 signature bytes, 4 length, 4 type, then data.
  // Its data begins with width and height as big-endian u32.
  const isIhdr = bytes.subarray(12, 16).toString('latin1') === 'IHDR';
  if (!isIhdr) {
    throw new Error('entry.png is not a PNG: its first chunk is not IHDR');
  }
  const width = bytes.readUInt32BE(16);
  const height = bytes.readUInt32BE(20);
  if (width < 1 || height < 1 || width > MAX_SIDE || height > MAX_SIDE) {
    throw new Error(`entry.png is ${width}x${height}, outside 1..${MAX_SIDE} on a side`);
  }

  return bytes;
}

function main(): void {
  const source = join(HERE, 'entry.png');
  const bytes = checkedPng(source);

  mkdirSync(OUT_DIR, { recursive: true });
  copyFileSync(source, join(OUT_DIR, 'entry.png'));

  process.stdout.write(
    `wrote entry.png (${bytes.length} bytes, ${bytes.readUInt32BE(16)}x${bytes.readUInt32BE(20)})\n`,
  );
}

main();
