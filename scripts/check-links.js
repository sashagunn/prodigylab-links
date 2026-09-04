#!/usr/bin/env node
/**
 * check-links.js — битые внутренние ссылки и базовая гигиена страниц.
 * Работает по локальным файлам, сеть не нужна. Запуск: npm run check:links
 */
const fs = require('fs');
const path = require('path');
const ROOT = path.resolve(__dirname, '..');

function walk(dir, acc = []) {
  for (const n of fs.readdirSync(dir)) {
    if (n === 'node_modules' || n === '.git') continue;
    const full = path.join(dir, n);
    if (fs.statSync(full).isDirectory()) walk(full, acc);
    else if (n.endsWith('.html')) acc.push(path.relative(ROOT, full));
  }
  return acc;
}

const files = walk(ROOT).sort();
const broken = [];
const noH1 = [];
const multiH1 = [];
const targets = new Map();

for (const f of files) {
  const html = fs.readFileSync(path.join(ROOT, f), 'utf8');
  const h1 = (html.match(/<h1[\s>]/g) || []).length;
  if (h1 === 0) noH1.push(f);
  if (h1 > 1) multiH1.push(`${f} (${h1})`);
  for (const m of html.matchAll(/href="(\/[^"#?]*)"/g)) {
    if (!targets.has(m[1])) targets.set(m[1], []);
    targets.get(m[1]).push(f);
  }
}

for (const [t, from] of targets) {
  let rel = t.replace(/^\//, '');
  if (rel === '') rel = 'index.html';
  else if (t.endsWith('/')) rel += 'index.html';
  if (!fs.existsSync(path.join(ROOT, rel))) broken.push([t, from]);
}

console.log(`Проверено страниц: ${files.length}, уникальных внутренних ссылок: ${targets.size}`);
if (broken.length) {
  console.log(`\nБИТЫЕ ССЫЛКИ (${broken.length}):`);
  for (const [t, from] of broken) console.log(`  ${t}\n     ссылаются: ${from.join(', ')}`);
} else console.log('Битых внутренних ссылок нет.');
if (noH1.length) console.log(`\nБез <h1> (${noH1.length}): ${noH1.join(', ')}`);
if (multiH1.length) console.log(`\nНесколько <h1> (${multiH1.length}): ${multiH1.join(', ')}`);
process.exit(broken.length ? 1 : 0);
