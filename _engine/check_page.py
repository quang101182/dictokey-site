# -*- coding: utf-8 -*-
"""Contrôle d'une page de blog dictokey.com AVANT publication. Exit 0 = publiable, 1 = bloquer.
Usage : python _engine/check_page.py blog/<slug>.html
Vérifie : structure SEO, JSON-LD valide (Article, BreadcrumbList, FAQPage), FAQ HTML == FAQ JSON-LD,
tableau comparatif, sources datées, lien Play avec utm, liens internes existants, sitemap + index du blog,
longueur, et les formulations INTERDITES par FACTS.md."""
import html
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# (motif regex, raison) — miroir des interdits de FACTS.md
INTERDITS = [
    (r"\bno[- ]tracking\b", "« no tracking » interdit (statistiques anonymes dans l'app)"),
    (r"\b(every|all) apps?\b", "« toutes les apps » interdit : écrire « most apps »"),
    (r"\b(cures?|heals?|doctor[- ]recommended|clinically)\b", "affirmation médicale interdite"),
    (r"\bMAI[- ]?Transcribe|\bAzure\b|\bGroq\b|whisper-large", "ne pas nommer le fournisseur de transcription"),
    (r"\bmillions? of users\b|\b\d[\d,.]*\+? (downloads|installs)\b", "aucun chiffre d'installs"),
    (r"\b(Quang|Mariia|Safonova|Soukhasing|se7en82)\b", "aucun nom de personne / compte personnel"),
]
NEGATION = re.compile(r"\b(no|not|neither|nor|never|without|requires?)\b|n't", re.I)


def fail(msgs):
    print("ÉCHEC :")
    for m in msgs:
        print("  -", m)
    sys.exit(1)


def main(path):
    errs = []
    if not os.path.isfile(path):
        fail([f"fichier introuvable : {path}"])
    src = open(path, encoding="utf-8").read()
    slug = os.path.basename(path)
    url = f"https://dictokey.com/blog/{slug}"

    gabarits = [
        ("title (20-75 car.)", r"<title>[^<]{20,75}</title>"),
        ("meta description (70-200 car.)", r'<meta name="description" content="[^"]{70,200}"'),
        ("canonical", r'<link rel="canonical" href="' + re.escape(url) + '"'),
    ]
    for nom, rx in gabarits:
        if not re.search(rx, src):
            errs.append(f"{nom} absent ou hors gabarit")
    if len(re.findall(r"<h1[\s>]", src)) != 1:
        errs.append("il faut exactement un <h1>")

    types, faq_ld = [], []
    for bloc in re.findall(r'<script type="application/ld\+json">(.*?)</script>', src, re.S):
        try:
            d = json.loads(bloc)
        except Exception as e:
            errs.append(f"JSON-LD invalide : {e}")
            continue
        types.append(d.get("@type"))
        if d.get("@type") == "FAQPage":
            faq_ld = [q["name"].strip() for q in d.get("mainEntity", [])]
        if d.get("@type") == "Article":
            if d.get("author", {}).get("name") not in ("DictoKey Team",):
                errs.append("auteur de l'Article ≠ DictoKey")
            if d.get("mainEntityOfPage") != url:
                errs.append("Article.mainEntityOfPage ≠ URL canonique")
    for t in ("Article", "BreadcrumbList", "FAQPage"):
        if t not in types:
            errs.append(f"JSON-LD {t} manquant")
    if not 4 <= len(faq_ld) <= 8:
        errs.append(f"FAQ JSON-LD : {len(faq_ld)} questions (4 à 8 attendues)")

    corps = re.sub(r"<script.*?</script>|<style.*?</style>", "", src, flags=re.S)
    texte = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", corps)))
    # même texte, mais coupé à chaque fin de bloc : une phrase ne se colle jamais à un titre voisin
    blocs = re.sub(r"</(h[1-6]|p|li|td|th|div|summary|dt|dd)>", " .\n", corps, flags=re.I)
    texte_phrases = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", blocs)))
    for q in faq_ld:
        if re.sub(r"\s+", " ", html.unescape(q)) not in texte:
            errs.append(f"question FAQ absente du HTML visible : {q[:60]}")

    if "<table" not in src:
        errs.append("tableau comparatif manquant")
    if not re.search(r"Checked on 20\d\d-\d\d-\d\d", texte):
        errs.append("section Sources sans « Checked on YYYY-MM-DD »")
    if "play.google.com/store/apps/details?id=com.dictokey.app" not in src or "utm_campaign" not in src:
        errs.append("lien Play Store avec utm manquant")

    # liens internes : relatifs (autre-article.html, ../accessibility/) ou absolus dictokey.com
    valides = 0
    for h in set(re.findall(r'href="([^"#?]+)"', src)):
        if h.startswith("https://dictokey.com"):
            h = h[len("https://dictokey.com"):]
        elif h.startswith(("http", "mailto:")):
            continue
        rel = h.lstrip("/")
        if rel.startswith("../"):
            rel = rel[3:]
        elif not rel.startswith(("blog/", "accessibility")) and rel.endswith(".html"):
            rel = "blog/" + rel
        cible = os.path.join(ROOT, rel)
        if os.path.isdir(cible):
            cible = os.path.join(cible, "index.html")
        if rel in ("", "blog/index.html"):
            continue
        if os.path.exists(cible):
            if rel != f"blog/{slug}":
                valides += 1
        elif rel.endswith(".html") or rel.startswith("accessibility"):
            errs.append(f"lien interne mort : {h}")
    if valides < 2:
        errs.append(f"{valides} lien(s) interne(s) valide(s) : 2 minimum")

    mots = len(re.findall(r"[A-Za-z][A-Za-z'’-]+", texte))
    if not 800 <= mots <= 2200:
        errs.append(f"longueur {mots} mots (800 à 2200)")

    for rx, raison in INTERDITS:
        m = re.search(rx, texte, re.I)
        if m:
            errs.append(f"formulation interdite « {m.group(0)} » : {raison}")
    for phrase in re.split(r"(?<=[.!?])\s+", texte_phrases):
        if phrase.rstrip().endswith("?"):
            continue  # une question de FAQ n'affirme rien
        if re.search(r"\bDictoKey\b", phrase) and re.search(r"\boffline\b", phrase, re.I) and not NEGATION.search(phrase):
            errs.append(f"DictoKey présenté comme hors ligne : « {phrase[:90]} »")

    sm = open(os.path.join(ROOT, "sitemap.xml"), encoding="utf-8").read()
    if f"<loc>{url}</loc>" not in sm:
        errs.append("page absente du sitemap.xml")
    if not sm.rstrip().endswith("</urlset>"):
        errs.append("sitemap.xml mal fermé")
    idx = open(os.path.join(ROOT, "blog", "index.html"), encoding="utf-8").read()
    if f'href="{slug}"' not in idx:
        errs.append("page absente de blog/index.html")

    if errs:
        fail(errs)
    print(f"OK : {slug} — {mots} mots, {len(faq_ld)} questions FAQ, {valides} liens internes")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    main(sys.argv[1])
