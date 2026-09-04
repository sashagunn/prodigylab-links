#!/usr/bin/env node
/**
 * generate-sitemap.js — строит sitemap.xml из файлов репозитория.
 *
 * Правила (заданы аудитом):
 *  - включаются ТОЛЬКО реально существующие HTML-страницы;
 *  - страницы с <meta name="robots" ... noindex> исключаются АВТОМАТИЧЕСКИ;
 *  - служебные/приватные пути исключаются по DENY;
 *  - lastmod берётся из даты последнего git-коммита файла (fallback — mtime);
 *  - canonical у страницы должен совпадать с её URL, иначе страница пропускается
 *    (чтобы в карту не попадали дубли).
 *
 * Запуск: node scripts/generate-sitemap.js   (или npm run sitemap)
 */
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const ROOT = path.resolve(__dirname, '..');
const ORIGIN = 'https://prodigylab.studio';

// пути, которые никогда не попадают в карту
const DENY = [
  /^node_modules\//,
  /^index_dark_backup\.html$/,
  /^newdesign\.html$/,          // дубль главной (noindex)
  /^pricecard-/,                // внутренняя шпаргалка по прайсу
  /^scripts\//,
  /^reports\//,
  /^logs\//,
];

// приоритеты: первое совпадение выигрывает
const PRIORITY = [
  [/^$/,                              '1.0', 'weekly'],   // главная
  [/^(en|es|pt|de)\/$/,               '0.9', 'weekly'],
  [/^prodigybot\/$/,                  '0.9', 'monthly'],
  [/^(en|es|pt|de)\/prodigybot\/$/,   '0.8', 'monthly'],
  [/^(en|es|pt|de)\/pricing\/$/,      '0.8', 'monthly'],
  // Entity-страницы: как AI и поиск понимают, что это за компания
  [/^about\/$/,                        '0.9', 'monthly'],
  [/^services\/$/,                     '0.9', 'monthly'],
  [/^scan\/$/,                         '0.9', 'monthly'],
  [/^case-studies\/$/,                 '0.8', 'monthly'],
  // SEO-посадочные под услуги (корневые слаги)
  [/^(shopify-development|shopify-redesign|website-development|website-redesign|ai-chatbot|ai-automation|meta-ads-management|google-ads-management)\/$/, '0.8', 'monthly'],
  [/^(shopify-audit|website-audit|conversion-rate-optimization|ecommerce-consulting|business-operations|business-consulting-usa)\/$/,                    '0.8', 'monthly'],
  [/^russian-[a-z-]+\/$/,             '0.7', 'monthly'],   // русскоязычные посадочные
  [/^services\//,                     '0.8', 'monthly'],
  [/^content-standard\/$/,            '0.7', 'yearly'],
  [/^(en|es|pt|de)\/content-standard\/$/, '0.6', 'yearly'],
  [/^musiclab\//,                     '0.3', 'yearly'],   // арт-проект намеренно понижен
  [/privacy\/$/,                      '0.3', 'yearly'],
];

function walk(dir, acc = []) {
  for (const name of fs.readdirSync(dir)) {
    const full = path.join(dir, name);
    const rel = path.relative(ROOT, full);
    if (DENY.some((re) => re.test(rel.replace(/\\/g, '/')))) continue;
    const st = fs.statSync(full);
    if (st.isDirectory()) walk(full, acc);
    else if (name.endsWith('.html')) acc.push(rel.replace(/\\/g, '/'));
  }
  return acc;
}

function urlFor(rel) {
  if (rel === 'index.html') return ORIGIN + '/';
  if (rel.endsWith('/index.html')) return ORIGIN + '/' + rel.slice(0, -'index.html'.length);
  return ORIGIN + '/' + rel;
}

function pathKey(rel) {
  if (rel === 'index.html') return '';
  if (rel.endsWith('/index.html')) return rel.slice(0, -'index.html'.length);
  return rel;
}

function lastmod(rel) {
  try {
    const d = execSync(`git log -1 --format=%cI -- "${rel}"`, { cwd: ROOT, stdio: ['ignore', 'pipe', 'ignore'] })
      .toString().trim();
    if (d) return d.slice(0, 10);
  } catch (_) {}
  return new Date(fs.statSync(path.join(ROOT, rel)).mtime).toISOString().slice(0, 10);
}

const skipped = [];
const entries = [];

for (const rel of walk(ROOT).sort()) {
  const html = fs.readFileSync(path.join(ROOT, rel), 'utf8');

  // 1) noindex — исключаем автоматически
  const robots = /<meta[^>]+name=["']robots["'][^>]*content=["']([^"']*)["']/i.exec(html);
  if (robots && /noindex/i.test(robots[1])) { skipped.push([rel, 'noindex']); continue; }

  // 2) canonical должен указывать на сам себя (иначе это дубль)
  const url = urlFor(rel);
  const canon = /<link[^>]+rel=["']canonical["'][^>]*href=["']([^"']+)["']/i.exec(html);
  if (canon) {
    const c = canon[1].replace(/\/$/, '');
    if (c.replace(/\/$/, '') !== url.replace(/\/$/, '')) { skipped.push([rel, `canonical→${canon[1]}`]); continue; }
  }

  const key = pathKey(rel);
  const rule = PRIORITY.find(([re]) => re.test(key));
  entries.push({
    url,
    lastmod: lastmod(rel),
    priority: rule ? rule[1] : '0.5',
    changefreq: rule ? rule[2] : 'monthly',
  });
}

entries.sort((a, b) => Number(b.priority) - Number(a.priority) || a.url.localeCompare(b.url));

const xml =
  `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n` +
  entries.map((e) =>
    `  <url>\n    <loc>${e.url}</loc>\n    <lastmod>${e.lastmod}</lastmod>\n` +
    `    <changefreq>${e.changefreq}</changefreq>\n    <priority>${e.priority}</priority>\n  </url>`
  ).join('\n') +
  `\n</urlset>\n`;

fs.writeFileSync(path.join(ROOT, 'sitemap.xml'), xml);

console.log(`sitemap.xml: ${entries.length} URL`);
for (const e of entries) console.log(`  ${e.priority}  ${e.lastmod}  ${e.url}`);
if (skipped.length) {
  console.log(`\nисключено (${skipped.length}):`);
  for (const [rel, why] of skipped) console.log(`  ${rel} — ${why}`);
}
