"""Иконки соцсетей для подвала. Один список — в BUSINESS_FACTS.json.

Иконки рисуем сами, без шрифтовых наборов и внешних библиотек: восемь
маленьких SVG дешевле, чем ещё один сторонний запрос на каждой странице.
Формы простые и узнаваемые; фирменные цвета не используем — в подвале они
спорят с версткой, а узнаются иконки и монохромными.
"""
import html as H
import json
import os

КОРЕНЬ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open(os.path.join(КОРЕНЬ, "BUSINESS_FACTS.json"), encoding="utf-8") as f:
    СЕТИ = (json.load(f).get("identity") or {}).get("socials") or []

_О = ('xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="18" height="18" '
      'fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" '
      'stroke-linejoin="round" aria-hidden="true"')

ИКОНКИ = {
 "instagram": f'<svg {_О}><rect x="3" y="3" width="18" height="18" rx="5"/>'
              '<circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor"/></svg>',
 "facebook":  f'<svg {_О}><path d="M15 3h-2.5A3.5 3.5 0 0 0 9 6.5V9H7v3h2v9h3v-9h2.5l.5-3H12V6.5a1 1 0 0 1 1-1h2z"/></svg>',
 "youtube":   f'<svg {_О}><rect x="2.5" y="5.5" width="19" height="13" rx="4"/>'
              '<path d="M10.5 9.5v5l4.5-2.5z"/></svg>',
 "tiktok":    f'<svg {_О}><path d="M14 3v11.5a3.5 3.5 0 1 1-3-3.46"/>'
              '<path d="M14 6.2A5 5 0 0 0 19 9"/></svg>',
 "threads":   f'<svg {_О}><path d="M16 8.6C15.2 7 13.8 6.2 12 6.2c-3 0-5 2.3-5 5.8s2 5.8 5 5.8c2.6 0 4.3-1.4 4.6-3.3"/>'
              '<path d="M9.6 13.1c0-1.3 1.2-2 2.7-2 2 0 3.3 1 3.3 2.6 0 1.8-1.5 2.8-3.2 2.8-1.4 0-2.3-.7-2.3-1.7"/></svg>',
 "x":         f'<svg {_О}><path d="M4 4l16 16M20 4L4 20"/></svg>',
 "telegram":  f'<svg {_О}><path d="M21 4.5L2.8 11.3l5.3 1.8L19 6.6l-8.2 8.2.4 5 2.6-3.6 4.3 3.1z"/></svg>',
 "linkedin":  f'<svg {_О}><rect x="3" y="3" width="18" height="18" rx="3"/>'
              '<path d="M7.5 10.5v6M7.5 7.5v.01M11.5 16.5v-3.2a1.8 1.8 0 0 1 3.6 0v3.2"/></svg>',
}

CSS = """
/* Соцсети в подвале: восемь иконок одной строкой, без подписей. Подписи
   удлиняют подвал вдвое и ничего не добавляют — иконки узнаются. */
.soc{display:flex;flex-wrap:wrap;gap:6px;margin:14px 0 0}
.soc a{display:inline-flex;align-items:center;justify-content:center;width:38px;height:38px;
 border:1px solid var(--line);border-radius:999px;color:var(--ink2);text-decoration:none}
.soc a:hover{color:var(--accent);border-color:var(--accent)}
"""


def блок(заголовок: str = "") -> str:
    """Строка иконок со ссылками. Пустая строка, если сетей в фактах нет."""
    if not СЕТИ:
        return ""
    ссылки = "".join(
        f'<a href="{H.escape(с["url"])}" target="_blank" rel="noopener me" '
        f'aria-label="{H.escape(с["name"])}" title="{H.escape(с["name"])}">'
        f'{ИКОНКИ.get(с.get("icon",""), "")}</a>'
        for с in СЕТИ if ИКОНКИ.get(с.get("icon", "")))
    шапка = f'<span class="mono" style="display:block;margin-bottom:6px">{H.escape(заголовок)}</span>' if заголовок else ""
    return f'<div class="soc-wrap">{шапка}<div class="soc">{ссылки}</div></div>'
