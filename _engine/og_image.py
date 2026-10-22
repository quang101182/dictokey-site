# -*- coding: utf-8 -*-
"""Image de partage dictokey.com (og:image / twitter:image), 1200x630 — v2, 22/10/2026.
L'ancienne (03/04) était une capture d'écran ratée (barre de défilement, bandes noires), en français sur un site anglais,
annonçait « 52 langues » (FACTS : 51) et montrait un QR code inutile dans un aperçu de partage.
Source de la capture : dictokey/playstore-assets-en-2026-10/raw/E2_bubble.png (app 2.74.10, 22/10).
Usage : python _engine/og_image.py   (écrit og-image.png à la racine du site)"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1200, 630
SRC = r"D:\Download\02-Apps-Web\Repo-github\dictokey\playstore-assets-en-2026-10\raw\E2_bubble.png"
B, R = "C:/Windows/Fonts/segoeuib.ttf", "C:/Windows/Fonts/segoeui.ttf"
TOP, BOT = (30, 27, 75), (55, 48, 140)          # indigo de l'icône (comme les captures Play)
ACCENT, VERT = (165, 170, 255), (52, 211, 153)

im = Image.new("RGB", (W, H)); d = ImageDraw.Draw(im)
for y in range(H):
    t = y / (H - 1); d.line([(0, y), (W, y)], fill=tuple(int(a + (b - a) * t) for a, b in zip(TOP, BOT)))
im = im.convert("RGBA"); d = ImageDraw.Draw(im)

x = 70
d.text((x, 92), "DictoKey", font=ImageFont.truetype(B, 64), fill=ACCENT)
y = 190
for ligne in ("When typing is hard,", "write with your voice."):
    d.text((x, y), ligne, font=ImageFont.truetype(B, 54), fill="white"); y += 66
y += 22
d.text((x, y), "A floating voice bubble and a voice keyboard", font=ImageFont.truetype(R, 30), fill=(220, 222, 255)); y += 42
d.text((x, y), "for Android · 51 languages · translation", font=ImageFont.truetype(R, 30), fill=(220, 222, 255)); y += 70
# pastille « Free on Google Play »
f = ImageFont.truetype(B, 28); txt = "Free on Google Play"
tw = d.textlength(txt, font=f)
d.rounded_rectangle([x, y, x + tw + 90, y + 62], 31, fill=(255, 255, 255, 235))
d.polygon([(x + 28, y + 17), (x + 28, y + 45), (x + 52, y + 31)], fill=VERT)
d.text((x + 66, y + 13), txt, font=f, fill=(30, 27, 75))

# capture de l'app, recadrée sur la conversation + la bulle (sans barre d'état ni barre d'adresse)
cap = Image.open(SRC).convert("RGB").crop((0, 160, 720, 1180))
ph = 520; pw = int(cap.width * ph / cap.height)
cap = cap.resize((pw, ph), Image.LANCZOS)
masque = Image.new("L", cap.size, 0); ImageDraw.Draw(masque).rounded_rectangle([0, 0, pw, ph], 34, fill=255)
cx, cy = W - pw - 80, (H - ph) // 2
ombre = Image.new("RGBA", im.size, (0, 0, 0, 0))
ImageDraw.Draw(ombre).rounded_rectangle([cx, cy + 16, cx + pw, cy + ph + 16], 34, fill=(0, 0, 0, 130))
im = Image.alpha_composite(im, ombre.filter(ImageFilter.GaussianBlur(22)))
im.paste(cap, (cx, cy), masque)
im.convert("RGB").save(r"D:\Download\02-Apps-Web\Repo-github\dictokey-site\og-image.png", optimize=True)
print("og-image.png", im.size, "capture", (pw, ph))
