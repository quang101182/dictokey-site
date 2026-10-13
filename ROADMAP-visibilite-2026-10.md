# DictoKey — Feuille de route visibilité gratuite (octobre 2026)

> **Fichier autosuffisant.** Ouvert le **13/10/2026** sur demande de Quang : *« Qu'est-ce qu'ils font pour se rendre
> visibles ? […] il faut agir. »* Complète le test pub payant (`dictokey/ROADMAP-boost-2026-10.md`, 15→26/10).
> « Fait » = `git log` + cases cochées.

## Le constat (mesuré le 13/10)

- **Visibilité effondrée** : DictoKey cité sur **2/10** recherches de référence (6/10 le 29/05), **0/8** réponses de
  GPT-5.6 et Gemini 3.8 à « best voice typing app Android ». Search Console : **8 clics / 317 impressions en 3 mois**,
  position moyenne 29,6.
- **Le contenu existe déjà** : 9 articles sur `dictokey.com/blog` (best voice keyboard, Wispr Flow alternative,
  Samsung…). Ils ne rankent pas : **trop peu, pas mis à jour, aucun site tiers ne les cite**.
- **Ce que font les concurrents** (enquête du 13/10, sources dans l'historique de session) :

| Concurrent | Ce qui le rend visible | Reproductible par nous ? |
|---|---|---|
| **Yaps** | **244 articles en 8 mois** : « Best… 2026 », ~40 « Alternatives », 30+ pages par métier, 7 langues | ✅ oui (production par Claude) |
| **Voicy** | 1 à 3 articles **par jour** : « Best », « Alternative », « X vs Y », « pricing de X », par métier ; affiliation 25 % | ✅ contenu oui · affiliation plus tard |
| **Wispr Flow** | argent (levées, podcast, presse) + 52 pages par profession, 45 par intégration | 🟡 seulement les pages |
| **Typeless** | lancement **Product Hunt** (#1 iOS, #3 Android) + bouche-à-oreille Reddit ; parrainage 5 $ des deux côtés | ✅ Product Hunt · parrainage plus tard |
| **FUTO** | notoriété du projet mère + Hacker News (346 pts) | ❌ |

⇒ **Les deux petits qui gagnent (Yaps, Voicy) n'ont ni visage ni budget pub : ils gagnent au VOLUME de pages ciblées et
à la RÉGULARITÉ.** C'est exactement ce que nous pouvons faire, techniquement aussi bien qu'eux.

## Le plan

### Phase 1 — Moteur de contenu sur dictokey.com (démarre le 13/10, Claude)
Rythme visé : **3 à 5 pages par semaine**, régulier (pas un déversement d'un coup : signal de spam).
Chaque page : honnête (cite les concurrents, leurs points forts), datée 2026, **tableau comparatif + FAQ en JSON-LD**
(ce que les IA reprennent), lien Play Store avec `utm` pour mesurer, maillage vers les autres pages.

- [ ] **A. « Alternatives » / « vs » côté Android** (intention d'achat la plus forte) : Samsung voice typing alternative ·
      Gboard voice typing alternative (refonte) · Wispr Flow Android alternative (refonte) · SwiftKey voice ·
      FUTO Voice Input vs DictoKey · Typeless Android alternative · Yaps alternative.
- [ ] **B. Pages « accessibilité » par besoin** (notre positionnement Play, et le profil de Curtis) : dyslexie,
      arthrite / douleurs aux mains, tendinite / RSI, basse vision, Parkinson / tremblements, seniors.
- [ ] **C. Mise à jour des 9 articles existants** (date, tableau, FAQ, prix réels, nouveautés v2.71-2.72).
- [ ] Sitemap + soumission Search Console à chaque lot.

### Phase 2 — Être cité ailleurs (semaine du 20/10)
- [ ] **Product Hunt « DictoKey for Android »** : un vrai lancement (compte maker `@se7en82` existant, déjà cité par
      Google). Choisir un mardi-mercredi, préparer visuels + texte. 🔑 Quang : valider la date.
- [ ] **AlternativeTo** : fiche DictoKey comme alternative à Gboard, SwiftKey, Wispr Flow, Samsung Keyboard.
      🔑 nécessite un compte (au nom de l'app, pas de Quang).
- [ ] Annuaires d'outils IA où Voicy est présent (`topai.tools` & co).

### Phase 3 — Après le bilan pub du 27/10
- [ ] **Parrainage** dans l'app (ex. 7 jours Premium offerts aux deux) — demande du code, à décider au bilan.
- [ ] Affiliation : plus tard, gestion fiscale à étudier (EI de Mariia).

## Mesure
- **27/10** (bilan pub) puis **fin novembre** : rejouer les 10 recherches + les 8 questions IA (méthode du 13/10 :
  sous-agent WebSearch + `llm.py openrouter` `openai/gpt-5.6-terra` et `google/gemini-3.8-flash`, avec et sans `:online`).
- Search Console mensuel : clics, impressions, pages qui entrent dans le top 20.
- **Critère** : sans gain d'impressions fin novembre (> 2× les 317 d'août-septembre), on revoit l'approche.

## Pièges
- ⛔ Pas de citation d'utilisateur dans la fiche Play (règle Google : témoignages non attribués interdits).
- ⛔ Pas de faux comparatif qui ne cite personne (l'article « best » de Wispr est une auto-promo : à ne pas imiter).
- ⚠️ Google pénalise le contenu de masse sans valeur : chaque page doit apporter un vrai comparatif ou un vrai cas d'usage.
- Anonymat de Quang : tout se publie au nom de DictoKey / « se7en82 », jamais en son nom.
