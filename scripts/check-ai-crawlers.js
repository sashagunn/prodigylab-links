#!/usr/bin/env node
/**
 * check-ai-crawlers.js — проверка доступности сайта для AI-краулеров.
 *
 * Что делает: запрашивает живой сайт с user-agent каждого агента и печатает
 * HTTP-код и размер ответа. Разный размер тела у разных агентов означал бы
 * подмену контента по user-agent — этого быть не должно.
 *
 * Что НЕ делает: не говорит, попадём ли мы в ответы ChatGPT или Claude.
 * Это проверка технического доступа, а не видимости.
 *
 * Запуск: npm run check:ai
 */
const https = require('https');

const HOSTS = ['prodigylab.studio', 'scan.prodigylab.studio'];
const PATHS = { 'prodigylab.studio': '/', 'scan.prodigylab.studio': '/' };

const AGENTS = [
  ['OpenAI',     'OAI-SearchBot',     'Mozilla/5.0 (compatible; OAI-SearchBot/1.0; +https://openai.com/searchbot)'],
  ['OpenAI',     'ChatGPT-User',      'Mozilla/5.0 (compatible; ChatGPT-User/1.0; +https://openai.com/bot)'],
  ['OpenAI',     'OAI-AdsBot',        'Mozilla/5.0 (compatible; OAI-AdsBot/1.0; +https://openai.com/searchbot)'],
  ['OpenAI',     'GPTBot',            'Mozilla/5.0 (compatible; GPTBot/1.2; +https://openai.com/gptbot)'],
  ['Anthropic',  'ClaudeBot',         'Mozilla/5.0 (compatible; ClaudeBot/1.0; +claudebot@anthropic.com)'],
  ['Anthropic',  'Claude-User',       'Mozilla/5.0 (compatible; Claude-User/1.0; +Claude-User@anthropic.com)'],
  ['Anthropic',  'Claude-SearchBot',  'Mozilla/5.0 (compatible; Claude-SearchBot/1.0; +Claude-SearchBot@anthropic.com)'],
  ['Perplexity', 'PerplexityBot',     'Mozilla/5.0 (compatible; PerplexityBot/1.0; +https://perplexity.ai/perplexitybot)'],
  ['Perplexity', 'Perplexity-User',   'Mozilla/5.0 (compatible; Perplexity-User/1.0; +https://perplexity.ai/perplexity-user)'],
  ['Microsoft',  'bingbot',           'Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)'],
  ['Google',     'Googlebot',         'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'],
  ['Google',     'Google-Extended',   'Google-Extended'],
  ['Apple',      'Applebot',          'Mozilla/5.0 (compatible; Applebot/0.1; +http://www.apple.com/go/applebot)'],
  ['Meta',       'meta-externalagent','meta-externalagent/1.1'],
];

function fetch(host, path, ua) {
  return new Promise((resolve) => {
    const req = https.request({ hostname: host, path, method: 'GET', headers: { 'User-Agent': ua } }, (res) => {
      let n = 0;
      res.on('data', (c) => (n += c.length));
      res.on('end', () => resolve({ code: res.statusCode, bytes: n }));
    });
    req.on('error', (e) => resolve({ code: 'ERR', bytes: 0, err: e.message }));
    req.setTimeout(15000, () => { req.destroy(); resolve({ code: 'TIMEOUT', bytes: 0 }); });
    req.end();
  });
}

function robotsFor(host) {
  return new Promise((resolve) => {
    https.get(`https://${host}/robots.txt`, (res) => {
      let s = '';
      res.on('data', (c) => (s += c));
      res.on('end', () => resolve(s));
    }).on('error', () => resolve(''));
  });
}

// Грубый, но честный разбор: ищем блок "User-agent: X" и Disallow: / в нём.
function disallowed(robots, agent) {
  const blocks = robots.split(/\n(?=User-agent:)/i);
  for (const b of blocks) {
    const m = /^User-agent:\s*(\S+)/i.exec(b.trim());
    if (!m) continue;
    if (m[1].toLowerCase() !== agent.toLowerCase()) continue;
    return /^\s*Disallow:\s*\/\s*$/im.test(b);
  }
  return null; // отдельного правила нет — действует правило "*"
}

(async () => {
  let problems = 0;
  for (const host of HOSTS) {
    const robots = await robotsFor(host);
    console.log(`\n=== ${host} ===`);
    console.log('провайдер     агент                robots       HTTP   байт');
    const sizes = new Set();
    for (const [prov, agent, ua] of AGENTS) {
      const r = await fetch(host, PATHS[host], ua);
      const d = disallowed(robots, agent);
      const rob = d === true ? 'DISALLOW' : d === false ? 'allow' : 'по «*»';
      const bad = !(r.code === 200 || r.code === 308 || r.code === 301);
      if (bad || d === true) problems++;
      if (r.code === 200) sizes.add(r.bytes);
      console.log(
        `${prov.padEnd(13)} ${agent.padEnd(20)} ${rob.padEnd(12)} ${String(r.code).padEnd(6)} ${r.bytes}` +
        (bad ? '   <-- ПРОВЕРИТЬ' : d === true ? '   <-- закрыт в robots' : '')
      );
    }
    if (sizes.size > 1) {
      console.log(`  !! разный размер ответа у разных агентов (${[...sizes].join(', ')}) — возможна подмена контента`);
      problems++;
    }
  }
  console.log(`\nТребует внимания: ${problems}`);
  console.log('Напоминание: это проверка доступа, а не гарантия цитирования в AI-ответах.');
})();
