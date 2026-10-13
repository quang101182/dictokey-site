# -*- coding: utf-8 -*-
"""Signale des URLs de dictokey.com à IndexNow (Bing, Yandex, Seznam…). Bing alimente la recherche de ChatGPT.
Usage : python _engine/indexnow.py <url> [<url> …]   → affiche le code HTTP (200/202 = accepté)."""
import json, os, sys, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KEY = open(os.path.join(ROOT, "dk-indexnow-key.txt"), encoding="utf-8").read().strip()

def main(urls):
    urls = [u for u in urls if u.startswith("https://dictokey.com/")]
    if not urls: print("aucune URL dictokey.com"); sys.exit(2)
    body = json.dumps({"host": "dictokey.com", "key": KEY,
                       "keyLocation": "https://dictokey.com/dk-indexnow-key.txt", "urlList": urls}).encode()
    req = urllib.request.Request("https://api.indexnow.org/indexnow", data=body,
                                 headers={"Content-Type": "application/json; charset=utf-8"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r: print("IndexNow HTTP", r.status, "-", len(urls), "URL(s)")
    except urllib.error.HTTPError as e:
        print("IndexNow HTTP", e.code, e.read()[:200]); sys.exit(1)

if __name__ == "__main__":
    main(sys.argv[1:])
