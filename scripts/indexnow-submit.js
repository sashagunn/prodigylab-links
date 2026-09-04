#!/usr/bin/env node
/**
 * indexnow-submit.js — отправка URL в IndexNow (Bing / Yandex / Seznam / Naver).
 *
 * Режимы:
 *   node scripts/indexnow-submit.js                 # только изменённые страницы (по хэшу содержимого)
 *   node scripts/indexnow-submit.js --all           # все индексируемые URL из sitemap.xml
 *   node scripts/indexnow-submit.js --dry           # показать, что было бы отправлено
 *   node scripts/indexnow-submit.js https://... ... # конкретные URL
 *
 * Логика «не слать без необходимости»:
 *   состояние хранится в .indexnow-state.json (url → sha1 содержимого страницы).
 *   URL уходит в IndexNow только если хэш изменился или URL новый.
 *
 * Логи: logs/indexnow/YYYY-MM-DD.jsonl (и успехи, и ошибки).
 */
const fs = require('fs');
const path = require('path');
const https = require('https');
const crypto = require('crypto');

const ROOT = path.resolve(__dirname, '..');
const ORIGIN = 'https://prodigylab.studio';
const HOST = 'prodigylab.studio';
const STATE = path.join(ROOT, '.indexnow-state.json');
const LOGDIR = path.join(ROOT, 'logs', 'indexnow');

// ---- ключ ----
function findKey() {
  const files = fs.readdirSync(ROOT).filter((f) => /^[a-f0-9]{8,128}\.txt$/i.test(f));
  if (!files.length) {
    throw new Error('Не найден файл ключа IndexNow (<key>.txt) в корне. Запусти: npm run indexnow:key');
  }
  const key = path.basename(files[0], '.txt');
  const content = fs.readFileSync(path.join(ROOT, files[0]), 'utf8').trim();
  if (content !== key) throw new Error(`Файл ${files[0]} должен содержать ровно ключ: ${key}`);
  return key;
}

// ---- какие URL вообще индексируемые (берём из sitemap — он уже фильтрует noindex) ----
function sitemapUrls() {
  const xml = fs.readFileSync(path.join(ROOT, 'sitemap.xml'), 'utf8');
  return [...xml.matchAll(/<loc>([^<]+)<\/loc>/g)].map((m) => m[1]);
}

function localFileFor(url) {
  let p = url.replace(ORIGIN, '');
  if (p === '/' || p === '') p = '/index.html';
  else if (p.endsWith('/')) p += 'index.html';
  const f = path.join(ROOT, p.replace(/^\//, ''));
  return fs.existsSync(f) ? f : null;
}

function sha1(s) { return crypto.createHash('sha1').update(s).digest('hex'); }

function log(entry) {
  fs.mkdirSync(LOGDIR, { recursive: true });
  const file = path.join(LOGDIR, new Date().toISOString().slice(0, 10) + '.jsonl');
  fs.appendFileSync(file, JSON.stringify({ ts: new Date().toISOString(), ...entry }) + '\n');
}

function post(key, urlList) {
  const body = JSON.stringify({
    host: HOST,
    key,
    keyLocation: `${ORIGIN}/${key}.txt`,
    urlList,
  });
  return new Promise((resolve) => {
    const req = https.request(
      { hostname: 'api.indexnow.org', path: '/indexnow', method: 'POST',
        headers: { 'Content-Type': 'application/json; charset=utf-8', 'Content-Length': Buffer.byteLength(body) } },
      (res) => {
        let data = '';
        res.on('data', (c) => (data += c));
        res.on('end', () => resolve({ status: res.statusCode, body: data.slice(0, 400) }));
      }
    );
    req.on('error', (e) => resolve({ status: 'ERR', body: String(e.message) }));
    req.write(body);
    req.end();
  });
}

(async () => {
  const args = process.argv.slice(2);
  const dry = args.includes('--dry');
  const all = args.includes('--all');
  const explicit = args.filter((a) => a.startsWith('http'));

  const key = findKey();
  const state = fs.existsSync(STATE) ? JSON.parse(fs.readFileSync(STATE, 'utf8')) : {};

  let candidates = explicit.length ? explicit : sitemapUrls();
  let toSend = [];
  const nextState = { ...state };

  if (explicit.length || all) {
    toSend = candidates;
    for (const u of candidates) {
      const f = localFileFor(u);
      if (f) nextState[u] = sha1(fs.readFileSync(f, 'utf8'));
    }
  } else {
    for (const u of candidates) {
      const f = localFileFor(u);
      if (!f) { toSend.push(u); continue; }              // нет локального файла — шлём на всякий случай
      const h = sha1(fs.readFileSync(f, 'utf8'));
      if (state[u] !== h) { toSend.push(u); nextState[u] = h; }
    }
    // URL, которые исчезли из sitemap, чистим из состояния
    for (const u of Object.keys(nextState)) if (!candidates.includes(u)) delete nextState[u];
  }

  if (!toSend.length) {
    console.log('IndexNow: изменений нет — ничего не отправляю.');
    log({ event: 'skip', reason: 'no-changes', candidates: candidates.length });
    return;
  }

  console.log(`IndexNow: к отправке ${toSend.length} URL`);
  toSend.forEach((u) => console.log('  ' + u));
  if (dry) { console.log('(--dry: ничего не отправлено)'); return; }

  // IndexNow принимает до 10 000 URL за раз; шлём пачками по 500
  let ok = true;
  for (let i = 0; i < toSend.length; i += 500) {
    const batch = toSend.slice(i, i + 500);
    const res = await post(key, batch);
    const good = res.status === 200 || res.status === 202;
    if (!good) ok = false;
    console.log(`  → HTTP ${res.status} для ${batch.length} URL ${res.body ? '· ' + res.body : ''}`);
    log({ event: good ? 'submit-ok' : 'submit-error', status: res.status, count: batch.length, urls: batch, response: res.body });
  }

  if (ok) fs.writeFileSync(STATE, JSON.stringify(nextState, null, 2));
  else console.log('Были ошибки — состояние не обновлено, следующий запуск повторит отправку.');
})();
