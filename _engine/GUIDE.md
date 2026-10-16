# Moteur de contenu dictokey.com — mode d'emploi (pour l'agent planifié ET pour Claude en session)

> Lancé le 13/10/2026. Objectif : regagner la visibilité Google + IA (2/10 recherches, 0/8 IA au 13/10) par le
> VOLUME et la RÉGULARITÉ, comme Yaps (244 articles en 8 mois) et Voicy (1-3/jour). Rythme : **1 page par exécution,
> du lundi au vendredi** (accéléré le 16/10/2026, au lieu de lun/mer/ven). Ce dossier `_engine/` n'est pas publié (Jekyll ignore les dossiers en `_`).

## Une exécution = exactement ceci, dans l'ordre

1. `git pull`. Lire `FACTS.md` (seule source sur DictoKey), ce guide, `BACKLOG.md`, `LOG.md`.
2. Prendre la **première ligne `[ ]`** de `BACKLOG.md` (ignorer les `[!]`). Une seule page par exécution. Si tout est
   coché : ne rien publier, écrire « backlog vide » dans `LOG.md`, commit, fin.
3. **Recherche concurrents (si la page en cite)** : WebSearch/WebFetch pour chaque concurrent cité. Ne retenir QUE des
   faits vus CE JOUR-LÀ sur une source officielle (site ou aide de l'éditeur, fiche Play Store) ou de presse 2026. Une
   page officielle non datée mais consultée le jour même est valable : c'est la mention « Checked on » qui la date.
   Prix, plateformes, limites : si non trouvé → ne pas l'écrire (« — » dans le tableau). Garder les URLs pour « Sources ».
4. **Écrire la page** dans `blog/<slug>.html` en anglais (marché visé : US/UK/CA/AU), en reprenant **uniquement la MISE
   EN PAGE de `blog/samsung-voice-typing-alternative.html`** (page de référence validée le 13/10) : même `<head>`, mêmes
   blocs JSON-LD (`Article`, `BreadcrumbList`, `FAQPage`), même CSS inline, même en-tête/pied, même bouton Play.
   ⛔ **Ne JAMAIS recopier une affirmation d'un ancien article** : plusieurs contiennent des formulations périmées ou
   interdites (« every app », fonctions absentes de FACTS). Le fond vient de FACTS.md et des sources du jour, point.
   Obligatoire dans chaque page :
   - un `<h1>` qui reprend la requête visée telle qu'un humain la tape ;
   - une **réponse directe en 2-3 phrases** juste sous le `<h1>` (c'est ce que les IA citent) ;
   - un **tableau comparatif** (`<table>`) honnête, DictoKey inclus, avec les points forts des autres ;
   - « Who should pick what » : quand choisir un concurrent plutôt que DictoKey (crédibilité) ;
   - une **FAQ de 4 à 6 questions**, identique dans le HTML et dans le JSON-LD `FAQPage` ;
   - une section **Sources** avec les URLs consultées et la date « Checked on YYYY-MM-DD » ;
   - le lien Play, EXACTEMENT (dans le HTML, `&` s'écrit `&amp;`) :
     `https://play.google.com/store/apps/details?id=com.dictokey.app&referrer=utm_source%3Ddictokey-site%26utm_medium%3Dblog%26utm_campaign%3D<slug>%26utm_content%3D<emplacement>`
     avec `<emplacement>` ∈ `intro`, `table`, `cta-bottom` (un lien par emplacement) ;
   - 2 à 4 **liens internes** vers d'autres articles du blog et vers `/accessibility` ;
   - `article:published_time` et `dateModified` = date du jour ; auteur JSON-LD = Organization « DictoKey Team ».
   Longueur : **le contrôle fait foi : 800 à 2 200 mots comptés sur la page entière** (menu, tableau, FAQ compris) ;
   viser ~1 300. Pas de remplissage : chaque paragraphe doit apporter un fait ou un conseil concret.
5. **Ajouter la page** : une carte en tête de `blog/index.html` (même format que les cartes existantes) et une entrée
   `<url>` dans `sitemap.xml` **juste avant `</urlset>`** (`lastmod` = date du jour, `changefreq` monthly, `priority` 0.8).
   Pour une **refonte** : modifier la page en place, mettre à jour `dateModified` + `article:modified_time` + `lastmod`.
6. **Contrôle** : `PYTHONIOENCODING=utf-8 python _engine/check_page.py blog/<slug>.html`. S'il échoue → corriger → relancer. **Ne jamais
   publier une page qui échoue.** Après 3 échecs : abandonner la page, la marquer `[!]` dans le BACKLOG avec la raison,
   ne rien publier, commit du BACKLOG + LOG seulement.
7. Cocher la ligne `[x]` dans `BACKLOG.md`, ajouter une ligne à `LOG.md` (toutes les colonnes, dont **Sources**).
   Si une source contredit un ancien article du site (prix, fonction), le noter sur la ligne REFONTE concernée du BACKLOG.
8. `git add blog/<slug>.html blog/index.html sitemap.xml _engine/BACKLOG.md _engine/LOG.md` (rien d'autre), commit
   `Contenu : <titre>`, `git push` sur la branche par défaut (GitHub Pages publie en 1-2 min).
9. **Signaler à Bing/IndexNow** : `python _engine/indexnow.py https://dictokey.com/blog/<slug>.html https://dictokey.com/blog/ https://dictokey.com/sitemap.xml`
   (Bing alimente la recherche de ChatGPT). Dans `LOG.md`, la colonne IndexNow vaut « après push » : le code HTTP figure
   dans le résumé final de l'exécution (pas de commit supplémentaire pour le reporter).

## Règles de fond
- **Tout fait sur DictoKey vient de `FACTS.md`.** Tout fait sur un concurrent vient d'une source vue ce jour-là.
- **Honnêteté** : citer les forces des concurrents (Gboard gratuit et intégré, Wispr très bon en réécriture, FUTO
  hors ligne et open source…). Une page qui ne cite que nous ne sera ni crue ni citée.
- **Accessibilité** : ton respectueux, pas de pathos, pas de promesse médicale (« can help », jamais « cures »).
- **Pas de doublon** : vérifier qu'aucune page existante ne vise déjà la même requête (`grep -l` sur `blog/`).
  Si oui → faire une refonte de l'existante au lieu d'en créer une.
- **Anonymat** : aucun nom de personne, aucune mention de l'éditeur réel, aucun lien vers un compte personnel.
- **Ne jamais toucher** : `index.html` (accueil), `privacy.html`, `accessibility/`, `CNAME`, `translations.js`,
  les fichiers `.bak`, ni `_engine/FACTS.md` (seul Claude en session le met à jour).
