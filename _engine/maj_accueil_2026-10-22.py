# -*- coding: utf-8 -*-
"""Applique la correction de l'accueil du 22/10/2026 (audit vs app 2.74.10) :
  1. translations.js : textes de _engine/accueil_2026-10-22.json (en, fr) + _trad.json (de, es, pt, ru, th) ;
     price_prem_1 des 5 autres langues = leur « 30 … par jour » avec 1000 (elles disaient « illimité ») ;
  2. index.html : texte anglais par défaut des mêmes clés, données structurées (JSON-LD), note Play 4.9 ;
  3. prix partout : 4.99 -> 4.79 (prix Play réel depuis mars), « 42 % » -> « 39 % » (34,99 / (4,79 x 12)).
Échoue (sans rien écrire) si un motif attendu ne tombe pas le bon nombre de fois.
Usage : python _engine/maj_accueil_2026-10-22.py   (depuis la racine du site)"""
import json, re, sys

CRLF = {}


def lire(p):
    """Lit en fins de ligne normalisées (\n) ; ecrire() restaure celles d'origine (le site est en CRLF par endroits)."""
    s = open(p, encoding="utf-8", newline="").read()
    CRLF[p] = "\r\n" in s
    return s.replace("\r\n", "\n")


def ecrire(p, s):
    open(p, "w", encoding="utf-8", newline="").write(s.replace("\n", "\r\n") if CRLF[p] else s)

ICI = "_engine/"
TXT = json.load(open(ICI + "accueil_2026-10-22.json", encoding="utf-8"))
TRAD = json.load(open(ICI + "accueil_2026-10-22_trad.json", encoding="utf-8"))
LANGS = {"en": TXT["en"], "fr": TXT["fr"], **{l: TRAD[l] for l in ("de", "es", "pt", "ru", "th")}}
for l, d in LANGS.items():
    assert set(d) == set(TXT["en"]), (l, set(TXT["en"]) ^ set(d))


def js(v):
    return "'" + v.replace("\\", "\\\\").replace("'", "\\'") + "'"


def stop(msg):
    sys.exit("ARRÊT (rien écrit) : " + msg)


# ── 1. translations.js ──
tr = lire("translations.js")
blocs = list(re.finditer(r"^([a-z]{2}): \{$", tr, re.M))
assert [b.group(1) for b in blocs] == ["en", "fr", "de", "es", "pt", "ru", "th"], [b.group(1) for b in blocs]
morceaux = []
for i, b in enumerate(blocs):
    fin = blocs[i + 1].start() if i + 1 < len(blocs) else len(tr)
    morceaux.append((b.group(1), b.start(), fin))
neuf = tr[:blocs[0].start()]
for lang, deb, fin in morceaux:
    bloc = tr[deb:fin]
    vals = dict(LANGS[lang])
    if lang not in ("en", "fr"):
        m = re.search(r"^  price_free_1: '([^\n]*)',$", bloc, re.M)
        if not m or "30" not in m.group(1):
            stop(f"{lang} price_free_1 introuvable")
        vals["price_prem_1"] = m.group(1).replace("30", "<strong>1000</strong>", 1)
    for k, v in vals.items():
        pat = re.compile(r"^  " + re.escape(k) + r": '(?:[^'\\]|\\.)*',?$", re.M)
        hits = pat.findall(bloc)
        if len(hits) > 1:
            stop(f"{lang}.{k} : {len(hits)} lignes")
        if hits:
            bloc = pat.sub(lambda m, k=k, v=v: f"  {k}: {js(v)}," if m.group(0).endswith(",") else f"  {k}: {js(v)}", bloc)
        else:   # clé absente dans cette langue : ajoutée en tête du bloc
            bloc = bloc.replace(f"{lang}: {{\n", f"{lang}: {{\n  {k}: {js(v)},\n", 1)
    neuf += bloc
tr = neuf

# ── 2. index.html : texte par défaut (anglais) des clés traduites ──
idx = lire("index.html")
for k, v in TXT["en"].items():
    pat = re.compile(r'(data-i18n="' + re.escape(k) + r'"[^>]*>)(.*?)(</(?:p|li|h3|span|div|summary|button)>)', re.S)
    n = len(pat.findall(idx))
    if n == 0:
        continue   # clé seulement côté JS
    if n > 1:
        stop(f"index.html {k} : {n} éléments")
    idx = pat.sub(lambda m, v=v: m.group(1) + v + m.group(3), idx)

# ── 3. données structurées + note + prix ──
REMPL = [
    ('"softwareVersion": "2.61.7"', '"softwareVersion": "2.74.10"', 1),
    ("(formal, casual, concise, expanded)", "(clean, formal, concise, expanded)", 2),
    ('"GDPR-compliant, no personal data stored"', '"GDPR-compliant, no recordings stored"', 1),
    ("Premium monthly — 1000 dictations/day + AI rewriting + Interpreter mode",
     "Premium monthly — 1,000 dictations/day + unlimited Interpreter mode", 1),
    ("unlocks 1000 dictations/day, AI rewriting, and Interpreter mode.",
     "raises the limit to 1,000 dictations/day and makes Interpreter mode unlimited (free users can try it 3 times a day).", 1),
    ("Audio is processed and immediately discarded — no personal data stored.",
     "Audio is processed and immediately discarded — no recordings stored.", 1),
    ("DictoKey does not store audio, transcriptions, or personal data. The app uses anonymous device identifiers for quota tracking only.",
     "DictoKey does not store audio recordings. The app uses a device identifier to count the daily quota, plus anonymous usage statistics; the privacy policy lists exactly what is kept.", 1),
    (" — features comparable to Wispr Flow Android (Early Access, 100+ languages).", " — features comparable to Wispr Flow on Android.", 1),
    ("The Free tier resets every day at midnight, so you always start fresh.",   # FAQ JSON-LD (le corps est déjà remplacé)
     "The Free tier resets every day at midnight UTC.", 1),
    ("a system-wide floating bubble that works in any app without switching keyboards",
     "a floating bubble that works across your apps without switching keyboards", 1),
    ('"name": "Se7en Vision AI"', '"name": "DictoKey Team"', 2),
    ("<strong>5.0</strong>", "<strong>4.9</strong>", 1),
]
for a, b, n in REMPL:
    c = idx.count(a)
    if c != n:
        stop(f"index.html {a[:60]!r} : {c} au lieu de {n}")
    idx = idx.replace(a, b)

def prix(s, nom):
    s2 = s.replace("€4.99", "€4.79").replace("4,99 €", "4,79 €").replace('"price": "4.99"', '"price": "4.79"')
    s2 = re.sub(r"\b42( ?)%", r"39\1%", s2)
    if re.search(r"4[.,]99(?!\d)", s2.replace("34.99", "").replace("34,99", "")):
        stop(f"{nom} : un 4.99 / 4,99 reste")
    return s2

tr, idx = prix(tr, "translations.js"), prix(idx, "index.html")
ecrire("translations.js", tr)
ecrire("index.html", idx)
print("ok : translations.js (7 langues) + index.html")
