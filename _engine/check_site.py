# -*- coding: utf-8 -*-
"""Garde-fou SITE ENTIER de dictokey.com : aucune page publiée ne doit contredire FACTS.md.
Exit 0 = site propre, 1 = au moins une affirmation interdite, 2 = usage.

Pourquoi (récidive du 18-19/10/2026) : FACTS.md a été corrigé (moteur, 51 langues) mais rien ne revérifiait
les pages DÉJÀ en ligne ; check_page.py ne contrôle que la page qu'on publie. Résultat : 31 pages fausses.
Règle d'entretien : quand un fait change dans FACTS.md, on ajoute ICI la règle correspondante — le
contrôle relit alors tout le site d'un coup (CI GitHub à chaque push + chaque jour, cf .github/workflows).

Usage :
  python _engine/check_site.py            rapport par fichier, exit 1 si violation
  python _engine/check_site.py --detail   + chaque occurrence avec son contexte
Exception légitime (ex. un CONCURRENT qui utilise Whisper) : ajouter une ligne dans _engine/site_allow.txt
« fichier | extrait exact du contexte » — elle est relue par un humain, jamais ajoutée en masse.
"""
import html
import os
import re
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXCLUS = {"privacy.html"}  # la politique DOIT nommer les sous-traitants (Microsoft, Groq) : obligation légale
DOSSIERS_EXCLUS = {"_engine", ".git", ".github", "node_modules"}

# (motif, raison) — miroir des faits de FACTS.md. ⚠️ À compléter à CHAQUE changement de FACTS.md.
REGLES = [
    (r"(?<![\d.,#/:-])\b52\b(?![\d.,%:/])(?:\s|-|&nbsp;| )*\+?(?:\s|-)*[^\W\d_]", "« 52 » langues : FACTS dit 51"),
    (r"whisper", "moteur Whisper : faux depuis le 03/10/2026 (et ne pas nommer le fournisseur)"),
    (r"open\s?ai", "OpenAI : faux pour DictoKey depuis le 03/10/2026"),
    (r"\bgroq\b", "Groq : ne pas nommer le fournisseur"),
    (r"\bMAI[- ]?Transcribe|\bAzure\b", "ne pas nommer le fournisseur de transcription"),
    (r"in our (own )?test(s|ing)?\b|our (own )?(benchmark|measurements?)\b", "chiffre « mesuré par nous » jamais mesuré"),
    (r"\b9[0-9](\.\d)?\s?[-–]\s?9[0-9](\.\d)?\s?%", "pourcentage de précision non mesuré"),
    (r"\bword error rate\b[^.]{0,40}\d|\bWER\b[^.]{0,25}\d|\d(\.\d)?\s?% (WER|word error)", "taux d'erreur chiffré non mesuré"),
    (r"GDPR[- ]hosting|EU[- ]hosting|hosted in the EU|EU servers|servers? in the EU", "hébergement UE non garanti par FACTS"),
    (r"\bno[- ]tracking\b|sans (aucun )?suivi|kein Tracking", "« no tracking » interdit (statistiques anonymes)"),
    (r"\boffline\b|hors[- ]ligne", "DictoKey présenté comme hors ligne"),
    (r"\b(cures?|heals?|doctor[- ]recommended|clinically proven)\b", "affirmation médicale interdite"),
    (r"\bmillions? of users\b|\b\d[\d,.]*\+? (downloads|installs)\b", "aucun chiffre d'installs"),
    (r'"aggregateRating"|"reviewCount"|"ratingValue"', "note déclarée dans le JSON-LD : figée ou inventée (FACTS : aucune note)"),
    (r"nocode-?flow", "signature = « DictoKey Team » (NoCodeFlow arrêté le 16/09/2026)"),
    # 22/10/2026 : depuis l'app 2.74.4 la bulle LIT le champ actif (Précédent / Suivant, espace) et l'envoie sur
    # Traduire / Corriger / Emojis -> ces formules sont devenues fausses (FACTS § Confidentialité).
    (r"accessibility (permission|service)[^.]{0,40}\b(only|solely)\b[^.]{0,30}\b(show|display)|"
     r"\b(only|solely) (used )?to (show|display) the bubble and insert|"
     r"(does not|doesn't|never) read(s)? (or record )?(the )?screen( content)?|"
     r"(does not|doesn't|never) transmit(s)? accessibility data|"
     r"sert uniquement à afficher la bulle|ne lit (pas|jamais) (l'|le contenu de l')écran",
     "accessibilité : la bulle lit le champ actif depuis 2.74.4 (FACTS § Confidentialité)"),
    # 22/10/2026 : contredit privacy.html §4-5 (identifiant d'appareil pour le quota, statistiques d'usage anonymes).
    (r"(collects?|stores?|stored|collected) no personal data|no personal data (is )?(stored|collected)|"
     r"aucune donnée personnelle|keine personenbezogenen Daten|ningún dato personal|nenhum dado pessoal",
     "« aucune donnée personnelle » : faux (privacy.html §4-5) — écrire « no recordings stored »"),
    (r"\bQWERTZ\b|\bDvorak\b|\bAZERTY\b", "le clavier DictoKey n'a pas de touches lettres (keyboard_dictokey.xml)"),
    # 23/10/2026 : prix 7,99 €/mois et 59,99 €/an depuis la hausse du 23/10 ; Premium = 1 000 dictées/jour, jamais « illimité ».
    # Ciblé sur DictoKey / Premium / Interprète : les pages comparatives citent légitimement l'offre illimitée d'un concurrent.
    (r"(?<![\d.,])(4[.,][79]9|34[.,]99)\s?(€|eur|euros?)|€\s?(4[.,][79]9|34[.,]99)(?![\d])|-\s?(39|42)\s?%|about \$5(/| per | a )mo", "prix DictoKey : 7,99 €/mois et 59,99 €/an, -37 % (FACTS § Prix, hausse du 23/10)"),
    (r"(premium|dictokey)\W+(\w+\W+){0,6}?(unlimited|illimit\w*|ilimitad\w*|unbegrenzt\w*)|"
     r"(?<!free )unlimited (dictations?|interpreter)|(dictées?|interprète) illimit|illimit\w* (dictées?|interprète)",
     "Premium = 1 000 dictées/jour, jamais « illimité » (FACTS § Prix)"),
    (r"\bformal,\s*casual\b|\bcasual,\s*(concise|expanded)\b|décontracté","styles de réécriture : clean / formal / concise / expanded (pas « casual »)"),
]
# Règles dont une QUESTION (« Does it work offline? ») ou une phrase NÉGATIVE (« No. DictoKey needs internet ») est juste.
REGLES_NUANCEES = {r"\boffline\b|hors[- ]ligne"}
NEGATION = re.compile(r"\b(no|not|never|without|needs?|requires?|non|pas|jamais|nécessite|besoin|nein|benötigt|"
                      r"requiere|necesita|requer|precisa|não)\b|n't", re.I)


def phrase_autour(t, i, j):
    deb = max(t.rfind(c, 0, i) for c in ".!?\n'\"") + 1
    fins = [k for k in (t.find(c, j) for c in ".!?\n'\"") if k != -1]
    fin = min(fins) if fins else len(t)
    return t[deb:fin + 1]


def fichiers():
    """Uniquement ce que GitHub Pages publie = les fichiers suivis par git (un brouillon local non suivi n'est pas en ligne)."""
    try:
        suivis = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True, check=True).stdout.split("\n")
    except Exception:
        suivis = [os.path.relpath(os.path.join(d, f), ROOT).replace("\\", "/") for d, _, fs in os.walk(ROOT) for f in fs]
    for rel in suivis:
        if not rel or rel in EXCLUS or rel.split("/")[0] in DOSSIERS_EXCLUS or not rel.endswith((".html", ".js")):
            continue
        yield rel


def texte_publie(rel, src):
    """Ce que voit un lecteur ou un moteur : texte, attributs lus (content/alt/title/aria-label), JSON-LD, chaînes JS."""
    if rel.endswith(".js"):
        return src
    src = re.sub(r"<!--.*?-->|<style.*?</style>|<svg.*?</svg>", " ", src, flags=re.S | re.I)
    attrs = " ".join(re.findall(r'\b(?:content|alt|title|aria-label|placeholder)="([^"]*)"', src))
    corps = re.sub(r"<[^>]+>", " ", src)
    return html.unescape(corps + " \n " + attrs)


def autorisations():
    p = os.path.join(ROOT, "_engine", "site_allow.txt")
    out = []
    if os.path.exists(p):
        for l in open(p, encoding="utf-8"):
            l = l.strip()
            if l and not l.startswith("#") and "|" in l:
                f, extrait = (x.strip() for x in l.split("|", 1))
                out.append((f, extrait))
    return out


def violations(rel, allow=None):
    """Liste (raison, contexte) des affirmations contraires à FACTS.md dans UN fichier publié (aussi appelé par check_page.py)."""
    allow = autorisations() if allow is None else allow
    t = texte_publie(rel, open(os.path.join(ROOT, rel), encoding="utf-8").read())
    out = []
    for rx, raison in REGLES:
        for m in re.finditer(rx, t, re.I):
            if rx in REGLES_NUANCEES:
                ph = phrase_autour(t, m.start(), m.end())
                # seule une phrase qui parle de DictoKey compte : « FUTO works offline » est un fait sur un concurrent
                if ph.rstrip().endswith("?") or NEGATION.search(ph) or not re.search(r"dicto ?key", ph, re.I):
                    continue
            ctx = re.sub(r"\s+", " ", t[max(0, m.start() - 70):m.end() + 70])
            # « fichier | extrait » : ce contexte précis ; « fichier | regle:<motif exact> » : toute la règle
            # pour ce fichier (ex. un article SUR Whisper en tant que modèle tiers). Les deux sont relus à la main.
            if any(f == rel and (e in ctx or e == "regle:" + rx) for f, e in allow):
                continue
            out.append((raison, ctx))
    return out


def main(detail):
    allow = autorisations()
    par_fichier = {}
    for rel in sorted(fichiers()):
        v = violations(rel, allow)
        if v:
            par_fichier[rel] = v
    total = sum(len(v) for v in par_fichier.values())
    for rel, v in par_fichier.items():
        print(f"❌ {rel} : {len(v)}")
        if detail:
            for raison, ctx in v:
                print(f"     [{raison}] …{ctx}…")
    if total:
        print(f"ÉCHEC : {total} affirmation(s) contraire(s) à FACTS.md dans {len(par_fichier)} fichier(s)")
        return 1
    print("OK : aucune page publiée ne contredit FACTS.md")
    return 0


if __name__ == "__main__":
    if any(a not in ("--detail",) for a in sys.argv[1:]):
        print(__doc__)
        sys.exit(2)
    sys.exit(main("--detail" in sys.argv))
