#!/usr/bin/env node
/**
 * inject-entity-schema.js — Organization + WebSite JSON-LD из BUSINESS_FACTS.json.
 *
 * Зачем: факты о компании должны жить в одном месте. Меняешь BUSINESS_FACTS.json,
 * запускаешь `npm run schema` — разметка на всех языковых главных обновляется сама.
 * Руками JSON-LD в HTML не править: следующий запуск затрёт.
 *
 * Блок помечен маркерами ENTITY-SCHEMA:START / END и заменяется целиком.
 * LocalBusiness намеренно НЕ выпускается: у компании нет публичного адреса,
 * а этот тип требует address. Ставить его с выдуманным адресом = врать в разметке.
 */
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const F = JSON.parse(fs.readFileSync(path.join(ROOT, 'BUSINESS_FACTS.json'), 'utf8'));
const ORIGIN = 'https://prodigylab.studio';

const START = '<!-- ENTITY-SCHEMA:START (генерируется scripts/inject-entity-schema.js из BUSINESS_FACTS.json — руками не править) -->';
const END = '<!-- ENTITY-SCHEMA:END -->';

const PAGES = [
  { file: 'index.html',    url: `${ORIGIN}/`,    lang: 'ru' },
  { file: 'en/index.html', url: `${ORIGIN}/en/`, lang: 'en' },
  { file: 'es/index.html', url: `${ORIGIN}/es/`, lang: 'es' },
  { file: 'pt/index.html', url: `${ORIGIN}/pt/`, lang: 'pt' },
  { file: 'de/index.html', url: `${ORIGIN}/de/`, lang: 'de' },
];

const sameAs = [
  F.contact.instagram,
  F.contact.facebook,
  F.contact.telegram,
].filter(Boolean);

function organization(lang) {
  const org = {
    '@context': 'https://schema.org',
    '@type': 'ProfessionalService',
    '@id': `${ORIGIN}/#organization`,
    name: F.identity.name,
    legalName: F.identity.legalName,
    url: F.identity.url,
    logo: F.identity.logo,
    image: F.identity.logo,
    slogan: lang === 'ru' ? F.identity.slogan_ru : F.identity.slogan_en,
    description: lang === 'ru' ? F.identity.description_ru : F.identity.description_en,
    telephone: F.contact.businessPhone,
    sameAs,
    // Компания работает удалённо, публичного офиса нет — поэтому areaServed есть,
    // а address отсутствует. Это осознанно, а не пропуск.
    areaServed: F.geography.areaServed.map((n) => ({ '@type': 'Country', name: n })),
    knowsLanguage: F.geography.languages,
    hasOfferCatalog: {
      '@type': 'OfferCatalog',
      name: 'Services',
      itemListElement: F.services.map((s) => ({
        '@type': 'Offer',
        url: `${ORIGIN}/${s.slug}/`,
        priceCurrency: 'USD',
        price: String(s.startingPrice),
        priceSpecification: {
          '@type': 'PriceSpecification',
          priceCurrency: 'USD',
          minPrice: s.startingPrice,
          valueAddedTaxIncluded: false,
        },
        itemOffered: { '@type': 'Service', name: s.name_en, url: `${ORIGIN}/${s.slug}/` },
      })),
    },
  };
  return org;
}

function website(page) {
  return {
    '@context': 'https://schema.org',
    '@type': 'WebSite',
    '@id': `${ORIGIN}/#website`,
    url: page.url,
    name: F.identity.name,
    inLanguage: page.lang,
    publisher: { '@id': `${ORIGIN}/#organization` },
  };
}

let changed = 0;
for (const page of PAGES) {
  const file = path.join(ROOT, page.file);
  if (!fs.existsSync(file)) { console.log(`  пропуск (нет файла): ${page.file}`); continue; }
  let html = fs.readFileSync(file, 'utf8');

  const block =
    `${START}\n` +
    `<script type="application/ld+json">\n${JSON.stringify(organization(page.lang), null, 1)}\n</script>\n` +
    `<script type="application/ld+json">\n${JSON.stringify(website(page), null, 1)}\n</script>\n` +
    `${END}`;

  const re = new RegExp(`${START.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}[\\s\\S]*?${END}`);
  if (re.test(html)) {
    html = html.replace(re, block);
  } else {
    // первая вставка — перед </head>
    if (!/<\/head>/i.test(html)) { console.log(`  !! нет </head>: ${page.file}`); continue; }
    html = html.replace(/<\/head>/i, `${block}\n</head>`);
  }
  fs.writeFileSync(file, html);
  console.log(`  ✓ ${page.file}`);
  changed++;
}
console.log(`Entity-разметка обновлена на ${changed} страницах из BUSINESS_FACTS.json`);
