"""Search Console : inspecte des URL (et, avec --demander, clique « DEMANDER UNE INDEXATION »). Edge CDP 9223, onglet dédié fermé à la fin.
Usage : python gsc_inspecter.py [--demander] "sc-domain%3Adictokey.com" <url> [<url>...]
Pièges (04/11/2026) : le clic JS .click() ne déclenche RIEN, il faut un vrai clic souris CDP ; chaque demande prend ~1 min ;
l'URL /search-console/inspect?id=... rend un 404, passer par la barre de recherche. Rapport Pages en retard de ~10 j : se fier à l'inspection."""
import json, sys, time, urllib.request
import websocket
sys.stdout.reconfigure(encoding="utf-8")
DEMANDER = "--demander" in sys.argv
args = [a for a in sys.argv[1:] if a != "--demander"]
RES = args[0]
urls = args[1:]
tab = json.load(urllib.request.urlopen(urllib.request.Request("http://127.0.0.1:9223/json/new?about:blank", method="PUT")))
ws = websocket.create_connection(tab["webSocketDebuggerUrl"], suppress_origin=True, timeout=60)
n = 0
def call(m, p=None):
    global n; n += 1
    ws.send(json.dumps({"id": n, "method": m, "params": p or {}}))
    while True:
        r = json.loads(ws.recv())
        if r.get("id") == n: return r.get("result", {})
def ev(e): return call("Runtime.evaluate", {"expression": e, "returnByValue": True}).get("result", {}).get("value")
FIN = ["Cette URL est sur Google", "Cette URL n'est pas sur Google", "L'URL est sur Google", "L'URL n'est pas sur Google", "URL is on Google", "URL is not on Google", "n'est pas disponible"]
out = {}
try:
    for u in urls:
        call("Page.navigate", {"url": f"https://search.google.com/search-console?resource_id={RES}"}); time.sleep(6)
        ok = ev("""(()=>{const i=[...document.querySelectorAll('input')].find(x=>/inspect/i.test((x.getAttribute('aria-label')||'')+(x.placeholder||'')));
                 if(!i) return false; i.focus(); i.value=''; return true;})()""")
        if not ok:
            print(u, "→ barre d'inspection introuvable"); out[u] = None; continue
        call("Input.insertText", {"text": u})
        for t in ("keyDown", "keyUp"):
            call("Input.dispatchKeyEvent", {"type": t, "key": "Enter", "code": "Enter", "windowsVirtualKeyCode": 13})
        txt = ""
        for _ in range(40):
            time.sleep(2); txt = ev("document.body.innerText") or ""
            if any(k in txt for k in FIN): time.sleep(3); txt = ev("document.body.innerText"); break
        demande = "non tentée"
        if DEMANDER:
            pos = ev("""(()=>{const c=[...document.querySelectorAll('*')].filter(x=>x.innerText&&x.innerText.trim()==='DEMANDER UNE INDEXATION'&&x.getBoundingClientRect().width>0);
                     const b=c[c.length-1]; if(!b) return null; b.scrollIntoView({block:'center'}); const r=b.getBoundingClientRect(); return [r.x+r.width/2, r.y+r.height/2];})()""")
            clic = bool(pos)
            if clic:
                time.sleep(1)
                for t in ("mouseMoved", "mousePressed", "mouseReleased"):
                    call("Input.dispatchMouseEvent", {"type": t, "x": pos[0], "y": pos[1], "button": "left", "clickCount": 1})
            demande = "bouton absent"
            if clic:
                demande = "délai dépassé"
                for _ in range(60):
                    time.sleep(3); t2 = ev("document.body.innerText") or ""
                    if "Indexation demandée" in t2 or "indexation demandée" in t2.lower(): demande = "Indexation demandée"; break
                    if "Quota dépassé" in t2 or "quota" in t2.lower() and "dépass" in t2.lower(): demande = "QUOTA dépassé"; break
                ev("""(()=>{const b=[...document.querySelectorAll('[role=button],button,span')].find(x=>x.innerText&&/^(OK|IGNORER|J'AI COMPRIS)$/.test(x.innerText.trim())); if(b) b.click();})()""")
            print("   DEMANDE:", demande, flush=True)
            if demande != "Indexation demandée": open(__import__("os").path.join(__import__("tempfile").gettempdir(), "gsc_dernier_ecran.txt"),"w",encoding="utf-8").write(ev("document.body.innerText") or "")
        lignes = [l.strip() for l in txt.splitlines() if l.strip()]
        out[u] = lignes + ["DEMANDE: " + demande]
        i0 = next((i for i, l in enumerate(lignes) if any(k in l for k in FIN)), None)
        print("=" * 50, u.split("/")[-1])
        print("\n".join("   " + l[:150] for l in (lignes[i0:i0 + 12] if i0 is not None else ["(pas de verdict lu)"])))
finally:
    try: call("Page.close")
    except Exception: pass
    ws.close()
json.dump(out, open(__import__("os").path.join(__import__("tempfile").gettempdir(), "gsc_inspecter_out.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
