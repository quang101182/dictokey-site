# -*- coding: utf-8 -*-
"""Blog dictokey.com (22/10/2026) : corrige les affirmations FONCTIONNELLES devenues fausses avec l'app 2.74
(audit du 22/10, vérifié dans le code) — bulle (pilule langue | micro, panneau Traduire / Corriger / Emojis,
Précédent / Suivant), clavier SANS touches lettres (keyboard_dictokey.xml), traduction au clavier = bouton Traduire,
Interprète = écran dédié. Chaque phrase doit être trouvée au moins une fois, sinon rien n'est écrit.
Usage : python _engine/maj_blog_2026-10-22.py   (depuis la racine du site)"""
import sys

R = {
 "blog/best-floating-voice-dictation-android-2026.html": [
  ("It's a draggable microphone overlay that sits above most apps on your phone. Tap once &mdash; the bubble pulses, you speak, and transcribed (and optionally translated) text lands in the field you were looking at.",
   "It's a small two-part pill (language | mic) that sits above most apps on your phone. Tap the mic, speak, and the transcribed text lands in the field you were looking at; long-press to get it translated. Drag the bubble onto Translate, Correct or Emojis to rework what is already written, or step back like on a keyboard."),
  ("<li><strong>Voice correction requires the keyboard, not the bubble.</strong> You can say \"replace X with Y\" inside the DictoKey keyboard, but the floating bubble itself currently focuses on insertion, not mid-text editing.</li>",
   "<li><strong>Spoken corrections need the keyboard.</strong> Saying \"replace X with Y\" works inside the DictoKey keyboard; the bubble edits text through its panel instead (Translate, Correct, Emojis, Previous / Next).</li>"),
  ("voice correction tied to the keyboard rather than the bubble", "spoken corrections tied to the keyboard"),
 ],
 "blog/best-voice-keyboard-android-2026.html": [
  ("This works inside most apps, no copy-paste.", "It opens as its own full-screen mode, made for talking face to face."),
  ("<li><strong>QWERTY layout is intentionally minimal.</strong> If you switch frequently between voice and tap-typing, you may prefer to keep Gboard installed alongside for swipe and emoji.</li>",
   "<li><strong>It is a voice-only keyboard.</strong> There are no letter keys: keep Gboard or your usual keyboard for tap-typing and swipe, and switch with one tap.</li>"),
  ("If your voice keyboard also offers a floating bubble (DictoKey does), enable it from the app's main screen. You will be asked to grant \"Display over other apps\" permission. Once granted, a small microphone bubble follows you across every screen &mdash; tap it to dictate without even opening the keyboard.",
   "If your voice keyboard also offers a floating bubble (DictoKey does), choose it during the first setup or turn it on from the app's main screen. Android asks for the \"Display over other apps\" and Accessibility permissions. The bubble then appears whenever a keyboard opens &mdash; tap it to dictate, with your usual keyboard still in place."),
 ],
 "blog/best-voice-dictation-apps-android-2026.html": [
  ("<li>Relatively new app, so the traditional keyboard (non-voice) typing experience is still maturing</li>",
   "<li>No letter keys: it is a voice keyboard, so you keep your usual keyboard for tap-typing</li>"),
 ],
 "blog/ai-keyboard-for-multilingual-users.html": [
  ("you fall back to basic typing.", "you switch back to your usual keyboard for typing."),
  ("<li><strong>Traditional typing experience is basic:</strong> DictoKey's physical keyboard mode is functional but less refined than Gboard or SwiftKey's swipe/prediction features.</li>",
   "<li><strong>No tap-typing:</strong> DictoKey is a voice keyboard without letter keys, so keep Gboard or SwiftKey for swipe and word prediction.</li>"),
 ],
 "blog/how-to-translate-text-on-android-keyboard.html": [
  ("You select source and target languages, press the microphone, speak, and the translated text appears in the text field.",
   "You select source and target languages, press the Translate button on the keyboard (or long-press the bubble), speak, and the translated text appears in the text field."),
  ("<h4>Press the microphone and speak</h4>", "<h4>Press Translate and speak</h4>"),
  ("<p>Tap the microphone button and speak naturally in English.", "<p>Tap the Translate button and speak naturally in English."),
 ],
}

ecrits = {}
for f, paires in R.items():
    s = open(f, encoding="utf-8", newline="").read()
    for a, b in paires:
        if a not in s:
            sys.exit(f"ARRÊT (rien écrit) : {f} : introuvable {a[:70]!r}")
        s = s.replace(a, b)
    ecrits[f] = s
for f, s in ecrits.items():
    open(f, "w", encoding="utf-8", newline="").write(s)
    print("ok", f)
