# -*- coding: utf-8 -*-
"""Page /windows/ (22/10/2026) : les liens vers Google Play passaient les UTM en paramètres d'URL (&utm_source=…),
que Google Play NE transmet PAS à l'app → l'Install Referrer était vide, les installs venues de cette page
n'étaient attribuées à rien. Forme correcte (celle de l'accueil) : &referrer=<UTM encodés>.
Corrige le bouton « Also on Android » et RÉGÉNÈRE le QR code (SVG intégré) avec le bon lien.
Contenus distincts pour la mesure (install_attribution.content) : winbtn / winqr.
Usage : python _engine/maj_windows_referrer.py   (depuis la racine du site)"""
import re, sys, io
import qrcode, qrcode.image.svg

F = "windows/index.html"
BASE = "https://play.google.com/store/apps/details?id=com.dictokey.app&referrer="
REF = "utm_source%3Ddictokey-site%26utm_medium%3Dweb%26utm_campaign%3Dwindows%26utm_content%3D"
s = open(F, encoding="utf-8", newline="").read()

ancien_btn = "https://play.google.com/store/apps/details?id=com.dictokey.app&amp;utm_source=dictokey-site&amp;utm_medium=web&amp;utm_campaign=windows-page\""
if s.count(ancien_btn) != 1:
    sys.exit("ARRÊT : bouton introuvable")
s = s.replace(ancien_btn, (BASE + REF + "winbtn").replace("&", "&amp;") + '"')

# QR : même taille d'affichage, mêmes attributs d'accessibilité que l'ancien
m = re.search(r'<svg role="img" aria-label="QR code: DictoKey on Google Play".*?</svg>', s, re.S)
if not m:
    sys.exit("ARRÊT : QR introuvable")
qr = qrcode.QRCode(border=2, error_correction=qrcode.constants.ERROR_CORRECT_M)
qr.add_data(BASE + REF + "winqr"); qr.make(fit=True)
buf = io.BytesIO(); qr.make_image(image_factory=qrcode.image.svg.SvgPathImage).save(buf)
svg = buf.getvalue().decode("utf-8")
svg = svg[svg.index("<svg"):]
svg = svg.replace("<svg ", '<svg role="img" aria-label="QR code: DictoKey on Google Play" '
                  'style="width:140px;height:140px;background:#fff;border-radius:8px" ', 1)
s = s[:m.start()] + svg + s[m.end():]
open(F, "w", encoding="utf-8", newline="").write(s)
print("ok", F)
