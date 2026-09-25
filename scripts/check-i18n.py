#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Полнота переводов. Английский — источник истины.

Падает (код 1), если в ru/es/pt/de:
  * отсутствует обязательный ключ, который есть в английском;
  * перевод пустой или состоит из пробелов;
  * появился ключ, которого нет в английском.

Запуск: npm run i18n   (входит в npm run all, поэтому сборка падает сама)
"""
import os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'scripts'))
LANGS = ("ru", "es", "pt", "de")
SRC = "en"


def check_home() -> list[str]:
    """scripts/home_content.py — словарь L[lang][ключ]."""
    import home_content as HC
    errs: list[str] = []
    if SRC not in HC.L:
        return [f"home: нет источника «{SRC}»"]
    base = HC.L[SRC]
    for lang in LANGS:
        if lang not in HC.L:
            errs.append(f"home · {lang}: локаль целиком отсутствует")
            continue
        cur = HC.L[lang]
        for key, ref in base.items():
            if key not in cur:
                errs.append(f"home · {lang} · {key}: ключ отсутствует")
                continue
            val = cur[key]
            if isinstance(ref, str):
                if not str(val).strip():
                    errs.append(f"home · {lang} · {key}: пустой перевод")
            elif isinstance(ref, (list, tuple)):
                # блоки одинаковой длины: 6 проблем, 3 шага, 6 фактов
                if not isinstance(val, (list, tuple)) or len(val) != len(ref):
                    errs.append(f"home · {lang} · {key}: структура не совпадает "
                                f"({len(val) if hasattr(val,'__len__') else '?'} вместо {len(ref)})")
                    continue
                for i, item in enumerate(val):
                    flat = [item] if isinstance(item, str) else list(item)
                    for piece in flat:
                        if isinstance(piece, str) and not piece.strip():
                            errs.append(f"home · {lang} · {key}[{i}]: пустая строка")
                        if isinstance(piece, (list, tuple)):
                            for p in piece:
                                if not str(p).strip():
                                    errs.append(f"home · {lang} · {key}[{i}]: пустой пункт списка")
        for key in cur:
            if key not in base:
                errs.append(f"home · {lang} · {key}: ключа нет в английском (лишний)")
    return errs


def check_diagnostic() -> list[str]:
    """app/diagnostic.py в репозитории бота — словарь S[ключ][lang]."""
    bot = os.path.expanduser("~/ProdigyLAB/smmbot")
    path = os.path.join(bot, "app", "diagnostic.py")
    if not os.path.exists(path):
        print("  (диагностика: репозиторий бота недоступен — пропуск)")
        return []
    ns: dict = {}
    src = open(path, encoding="utf-8").read()
    start = src.find("S: dict[str, dict[str, str]] = {")
    end = src.find("\ndef _(", start)
    if start < 0 or end < 0:
        return ["diagnostic: не нашёл словарь S"]
    exec(compile(src[start:end], "S", "exec"), ns)
    S = ns["S"]
    errs: list[str] = []
    for key, row in S.items():
        if SRC not in row or not str(row[SRC]).strip():
            errs.append(f"diagnostic · {SRC} · {key}: нет исходной строки")
        for lang in LANGS:
            if lang not in row:
                errs.append(f"diagnostic · {lang} · {key}: ключ отсутствует")
            elif not str(row[lang]).strip():
                errs.append(f"diagnostic · {lang} · {key}: пустой перевод")
        for lang in row:
            if lang not in (SRC,) + LANGS:
                errs.append(f"diagnostic · {lang} · {key}: неизвестная локаль")
    return errs


if __name__ == "__main__":
    errs = check_home() + check_diagnostic()
    if errs:
        print(f"\n✗ Переводы неполные — {len(errs)} проблем:\n")
        for e in errs:
            print(f"  {e}")
        print("\nАнглийский — источник истины. Сборка остановлена.")
        sys.exit(1)
    import home_content as HC
    print(f"✓ Переводы полные: {len(HC.L)} локалей главной + диагностика")
