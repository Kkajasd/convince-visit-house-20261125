// Convince the AI Judge to Visit Your House — entry program.
//
// The entry is a single image of an invitation letter. This program builds
// it from scratch on every run: it invokes the deterministic renderer
// (tools/draw_letter.py — Pillow plus the vendored DejaVu Serif fonts, no
// network, no clock, no randomness beyond a fixed seed) and copies the
// rendered entry.png to the output directory, so repeated runs write
// byte-identical output.
import { execFileSync } from "node:child_process";
import { mkdirSync, readFileSync, statSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const renderer = join(here, "tools", "draw_letter.py");
const source = join(here, "entry.png");
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const target = join(outDir, "entry.png");

// Render the letter in place (deterministic: fixed layout, fixed fonts).
execFileSync("python3", [renderer], { cwd: here, stdio: "inherit" });

const bytes = readFileSync(source);
if (!isPng(bytes)) {
  throw new Error("generated entry.png is not a PNG file");
}
mkdirSync(outDir, { recursive: true });
writeFileSync(target, bytes);
if (statSync(target).size !== bytes.length) {
  throw new Error("copied entry.png size mismatch");
}
console.log(`Wrote ${target} (${bytes.length} bytes)`);

// Guard: the generated file must start with the PNG signature, so a
// truncated or wrong-format image fails loudly instead of shipping.
function isPng(buf: Buffer): boolean {
  const sig = [0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a];
  return sig.every((b, i) => buf[i] === b);
}
