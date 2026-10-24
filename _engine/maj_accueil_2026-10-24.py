# -*- coding: utf-8 -*-
"""Accueil : nouveautés de l'app 2.75 (en production le 24/10/2026), d'après FACTS.md § « App 2.75 ».

Pas de nouvelle carte (la grille de 6 cartes resterait déséquilibrée) : deux phrases ajoutées à des cartes existantes.
  - way_1_desc (carte « Bulle flottante ») : une dictée qui ne peut pas être insérée est gardée quelques minutes.
  - feat_2_desc (carte « 51 langues ») : « Traduire avec DictoKey » dans le menu de sélection d'Android
    (libellé exact de l'app dans chaque langue, res/values-*/strings.xml process_text_translate).
way_1_desc n'existe qu'en en et fr dans translations.js (les autres langues retombent sur le HTML anglais).
Idempotent : refuse d'ajouter une phrase déjà présente.
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FEAT = {"en": " Or select text in most apps and choose “Translate with DictoKey”.",
        "fr": " Ou sélectionnez un texte dans la plupart des applis et choisissez « Traduire avec DictoKey ».",
        "de": " Oder markiere einen Text in den meisten Apps und wähle „Mit DictoKey übersetzen“.",
        "es": " O selecciona un texto en la mayoría de las apps y elige «Traducir con DictoKey».",
        "pt": " Ou selecione um texto na maioria dos apps e escolha “Traduzir com DictoKey”.",
        "ru": " Или выделите текст в большинстве приложений и выберите «Перевести с DictoKey».",
        "th": " หรือเลือกข้อความในแอปส่วนใหญ่ แล้วเลือก “แปลด้วย DictoKey”"}
WAY = {"en": " If a dictation can’t be inserted, the bubble keeps it for a few minutes and offers to insert it in the next field you tap.",
       "fr": " Si une dictée ne peut pas être insérée, la bulle la garde quelques minutes et te propose de l’insérer dans le prochain champ touché."}


def fin_chaine(s, i):
    """Index du ' fermant d'une chaîne JS à apostrophes qui commence à i (contenu), en sautant les \\x."""
    while True:
        c = s[i]
        if c == "\\":
            i += 2
            continue
        if c == "'":
            return i
        i += 1


def ajouter(seg, cle, phrase):
    tete = "  " + cle + ": '"
    assert seg.count(tete) == 1, cle
    deb = seg.index(tete) + len(tete)
    fin = fin_chaine(seg, deb)
    assert phrase not in seg[deb:fin], ("déjà présent", cle)
    return seg[:fin] + phrase + seg[fin:]


def main():
    p = os.path.join(ROOT, "translations.js")
    s = open(p, encoding="utf-8").read()
    debuts = []
    for lg in ["en", "fr", "de", "es", "pt", "ru", "th"]:
        k = s.find("\n" + lg + ": {")
        k = 0 if (k == -1 and s.startswith(lg + ": {")) else k + 1
        assert k >= 0, lg
        debuts.append((k, lg))
    debuts.sort()
    morceaux = [s[:debuts[0][0]]]
    for n, (k, lg) in enumerate(debuts):
        seg = s[k:debuts[n + 1][0] if n + 1 < len(debuts) else len(s)]
        seg = ajouter(seg, "feat_2_desc", FEAT[lg])
        if lg in WAY:
            seg = ajouter(seg, "way_1_desc", WAY[lg])
        morceaux.append(seg)
    out = "".join(morceaux)
    assert len(out) == len(s) + sum(len(x) for x in FEAT.values()) + sum(len(x) for x in WAY.values())
    open(p, "w", encoding="utf-8", newline="").write(out)

    p = os.path.join(ROOT, "index.html")
    h = open(p, encoding="utf-8").read()
    for avant, phrase in (("between any two of the 51 languages.</p>", FEAT["en"]),
                          ("and step back just like on the keyboard.</p>", WAY["en"])):
        assert h.count(avant) == 1, avant
        h = h.replace(avant, avant[:-4] + phrase + "</p>")
    open(p, "w", encoding="utf-8", newline="").write(h)
    print("ok")


if __name__ == "__main__":
    main()
