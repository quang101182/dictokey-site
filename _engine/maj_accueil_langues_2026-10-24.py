# -*- coding: utf-8 -*-
"""Accueil : 13 textes jamais traduits en de/es/pt/ru/th (constaté le 24/10/2026 : ils s'affichaient en anglais).

Section « 2 façons de dicter » (ways_*, way_1_*, way_2_title, way_3_*), légendes du haut de page (hero_caption_*) et
deux lignes de la carte des prix (price_free_8, price_prem_8). Traduits depuis en/fr, registre de chaque langue tel
qu'il existe déjà dans translations.js (de : du ; es : tú ; pt : você ; ru : вы). Contenu = FACTS.md (bulle 2.74/2.75,
notification facultative, pas une 3ᵉ façon de dicter). Idempotent : refuse une clé déjà présente.
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BULLE = "\\uD83E\\uDEE7 "
CLAVIER = "\\u2328\\uFE0F "

T = {
 "de": {
  "hero_caption_bubble": BULLE + "Schwebende Blase", "hero_caption_ime": CLAVIER + "Sprachtastatur (IME)",
  "price_free_8": "Schwebende Blase + IME-Tastatur", "price_prem_8": "Alles aus Kostenlos inklusive",
  "ways_label": "2 Wege zu diktieren, plus Kurzbefehle", "ways_title": "Du hast jedes Mal die Wahl.",
  "ways_desc": "Eine Sprach-Engine, zwei unabhängige Wege, sie zu nutzen: Ist einer nicht verfügbar, funktioniert der andere. Die Kurzbefehle in der Benachrichtigung sind ein Bonus.",
  "way_1_badge": "NEU", "way_1_title": "Schwebende Blase",
  "way_1_desc": "Erscheint, sobald du eine Tastatur öffnest. Tippen zum Diktieren, lang drücken zum Übersetzen. Zieh sie auf Übersetzen, Korrigieren oder Emojis, um schon Geschriebenes zu überarbeiten, und geh zurück wie mit der Tastatur. Kann ein Diktat nicht eingefügt werden, behält die Blase es einige Minuten und bietet an, es ins nächste Feld einzufügen, das du antippst.",
  "way_2_title": "Sprachtastatur (IME)", "way_3_title": "Kurzbefehle in der Benachrichtigung (optional)",
  "way_3_desc": "Wenn du Benachrichtigungen erlaubst: Sprache wechseln, Blase ein- oder ausblenden, den Dolmetscher öffnen, die Zwischenablage übersetzen oder dein letztes Diktat kopieren. Zum Diktieren nicht nötig.",
 },
 "es": {
  "hero_caption_bubble": BULLE + "Burbuja flotante", "hero_caption_ime": CLAVIER + "Teclado de voz (IME)",
  "price_free_8": "Burbuja flotante + teclado IME", "price_prem_8": "Todo lo del plan Gratis incluido",
  "ways_label": "2 formas de dictar, más atajos", "ways_title": "Tú eliges, siempre.",
  "ways_desc": "Un mismo motor de voz, dos formas independientes de usarlo: si una no está disponible, la otra funciona. Los atajos de la notificación son un extra.",
  "way_1_badge": "NUEVO", "way_1_title": "Burbuja flotante",
  "way_1_desc": "Aparece cada vez que abres un teclado. Tócala para dictar, mantén pulsado para traducir. Arrástrala sobre Traducir, Corregir o Emojis para retocar lo que ya escribiste, y retrocede como con el teclado. Si un dictado no se puede insertar, la burbuja lo guarda unos minutos y te ofrece insertarlo en el siguiente campo que toques.",
  "way_2_title": "Teclado de voz (IME)", "way_3_title": "Atajos en la notificación (opcional)",
  "way_3_desc": "Si permites las notificaciones: cambiar de idioma, mostrar u ocultar la burbuja, abrir el intérprete, traducir el portapapeles o copiar tu último dictado. No hace falta para dictar.",
 },
 "pt": {
  "hero_caption_bubble": BULLE + "Bolha flutuante", "hero_caption_ime": CLAVIER + "Teclado de voz (IME)",
  "price_free_8": "Bolha flutuante + teclado IME", "price_prem_8": "Tudo do plano Grátis incluído",
  "ways_label": "2 formas de ditar, mais atalhos", "ways_title": "Você escolhe, sempre.",
  "ways_desc": "Um só motor de voz, duas formas independentes de usá-lo: se uma não estiver disponível, a outra funciona. Os atalhos da notificação são um bônus.",
  "way_1_badge": "NOVO", "way_1_title": "Bolha flutuante",
  "way_1_desc": "Aparece sempre que você abre um teclado. Toque para ditar, toque e segure para traduzir. Arraste-a sobre Traduzir, Corrigir ou Emojis para retrabalhar o que você já escreveu, e volte atrás como no teclado. Se um ditado não puder ser inserido, a bolha o guarda por alguns minutos e oferece inseri-lo no próximo campo que você tocar.",
  "way_2_title": "Teclado de voz (IME)", "way_3_title": "Atalhos na notificação (opcional)",
  "way_3_desc": "Se você permitir notificações: trocar de idioma, mostrar ou ocultar a bolha, abrir o intérprete, traduzir a área de transferência ou copiar seu último ditado. Não é necessário para ditar.",
 },
 "ru": {
  "hero_caption_bubble": BULLE + "Плавающий пузырь", "hero_caption_ime": CLAVIER + "Голосовая клавиатура (IME)",
  "price_free_8": "Плавающий пузырь + клавиатура IME", "price_prem_8": "Всё из бесплатного тарифа",
  "ways_label": "2 способа диктовать и ярлыки", "ways_title": "Выбор всегда за вами.",
  "ways_desc": "Один голосовой движок, два независимых способа им пользоваться: если один недоступен, работает другой. Ярлыки в уведомлении — приятный бонус.",
  "way_1_badge": "НОВОЕ", "way_1_title": "Плавающий пузырь",
  "way_1_desc": "Появляется, когда вы открываете клавиатуру. Коснитесь, чтобы диктовать, удерживайте, чтобы перевести. Перетащите его на «Перевести», «Исправить» или «Эмодзи», чтобы доработать уже написанное, и возвращайтесь назад, как на клавиатуре. Если диктовку не удалось вставить, пузырь хранит её несколько минут и предлагает вставить в следующее поле, которого вы коснётесь.",
  "way_2_title": "Голосовая клавиатура (IME)", "way_3_title": "Ярлыки в уведомлении (необязательно)",
  "way_3_desc": "Если вы разрешите уведомления: смена языка, показ или скрытие пузыря, открытие переводчика, перевод буфера обмена или копирование последней диктовки. Для диктовки не нужно.",
 },
 "th": {
  "hero_caption_bubble": BULLE + "บับเบิลลอย", "hero_caption_ime": CLAVIER + "คีย์บอร์ดเสียง (IME)",
  "price_free_8": "บับเบิลลอย + คีย์บอร์ด IME", "price_prem_8": "รวมทุกอย่างในแผนฟรี",
  "ways_label": "2 วิธีในการพิมพ์ด้วยเสียง พร้อมทางลัด", "ways_title": "คุณเลือกได้ทุกครั้ง",
  "ways_desc": "เครื่องมือเสียงเดียวกัน สองวิธีที่ใช้งานแยกกันได้: ถ้าวิธีหนึ่งใช้ไม่ได้ อีกวิธีก็ยังทำงาน ทางลัดในการแจ้งเตือนเป็นของแถม",
  "way_1_badge": "ใหม่", "way_1_title": "บับเบิลลอย",
  "way_1_desc": "ปรากฏทุกครั้งที่คุณเปิดคีย์บอร์ด แตะเพื่อพิมพ์ด้วยเสียง กดค้างเพื่อแปล ลากไปที่ แปล แก้ไข หรือ อีโมจิ เพื่อปรับข้อความที่เขียนไว้แล้ว และย้อนกลับได้เหมือนบนคีย์บอร์ด ถ้าแทรกข้อความที่พูดไม่ได้ บับเบิลจะเก็บไว้สักครู่และเสนอให้แทรกในช่องถัดไปที่คุณแตะ",
  "way_2_title": "คีย์บอร์ดเสียง (IME)", "way_3_title": "ทางลัดในการแจ้งเตือน (ไม่บังคับ)",
  "way_3_desc": "ถ้าคุณอนุญาตการแจ้งเตือน: เปลี่ยนภาษา แสดงหรือซ่อนบับเบิล เปิดล่าม แปลคลิปบอร์ด หรือคัดลอกข้อความที่พูดล่าสุด ไม่จำเป็นสำหรับการพิมพ์ด้วยเสียง",
 },
}


def main():
    p = os.path.join(ROOT, "translations.js")
    s = open(p, encoding="utf-8").read()
    for lg, textes in T.items():
        deb = s.index("\n" + lg + ": {")
        fin = s.find("\n}", deb)
        bloc = s[deb:fin]
        ancre = bloc.index("\n  way_2_desc: '")
        fin_ligne = bloc.index("\n", ancre + 1)
        lignes = ""
        for k, v in textes.items():
            assert ("\n  " + k + ":") not in bloc, (lg, k)
            assert "'" not in v, (lg, k)
            lignes += "\n  " + k + ": '" + v + "',"
        bloc = bloc[:fin_ligne] + lignes + bloc[fin_ligne:]
        s = s[:deb] + bloc + s[fin:]
    open(p, "w", encoding="utf-8", newline="").write(s)
    print("ok")


if __name__ == "__main__":
    main()
