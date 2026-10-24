# DictoKey — faits vérifiés (SEULE source autorisée pour parler de DictoKey)

> Toute affirmation sur DictoKey dans une page DOIT venir de ce fichier. Si un fait manque ici : ne pas l'écrire.
> Source : description Play en-US en ligne (approuvée par Google le 24/07/2026) + code de l'app v2.72.0 (13/10/2026) ; § « App 2.75 » : code 2.75.3 (24/10/2026).
> Mis à jour : 18/10/2026 (51 langues, moteur ; voir BACKLOG « CORRECTIONS 18/10 »). Ce dossier `_engine/` n'est PAS publié (Jekyll ignore les dossiers en `_`).

## Identité
- Nom : **DictoKey** (fiche Play : « DictoKey: Voice Accessibility »). Éditeur affiché : « DictoKey Team ».
- Play Store : `https://play.google.com/store/apps/details?id=com.dictokey.app`
- Site : `https://dictokey.com` · page accessibilité : `https://dictokey.com/accessibility`
- Plateforme : **Android 10 et plus, toutes marques**, et **DictoKey for Windows** (Windows 10/11 64 bits, page
  `https://dictokey.com/windows/`, depuis le 20/10/2026). Pas d'iOS, pas de Mac.

## DictoKey for Windows (vérifié dans le code dictokey-pc v1.11.0 et sa passerelle, 20/10/2026)
- Raccourci **Ctrl+Alt+Espace** : dicter là où est le curseur (sinon presse-papiers) ; **Ctrl+Alt+T** : dicter + traduire ;
  raccourcis modifiables. Arrêt au 2ᵉ appui ou après quelques secondes de silence.
- Mêmes moteurs et mêmes 51 langues que l'Android (cloud, internet nécessaire), détection auto, traduction, réécriture IA,
  dictionnaire personnel, historique LOCAL (jamais envoyé), zone de notification, démarrage avec Windows, mises à jour auto.
- Interface **anglais et français** (suit la langue de Windows, réglable).
- **Gratuit** : 2 000 mots/semaine, sans compte. **Premium** : **9,99 €/mois TTC**, essai 7 j (carte demandée), sans
  limite de mots par semaine (« fair use »). ⛔ Ne JAMAIS chiffrer le plafond d'audio mensuel : c'est un garde-fou de coût
  volontairement non annoncé (`dictokey-pc/gateway/src/quota.js`, « l'annoncer inviterait à le longer »). Abonnement **séparé** de l'Android. Paiement **Polar**, clé par e-mail.
- Installeur **non signé** par un certificat Microsoft → SmartScreen « Windows a protégé votre PC » (Informations
  complémentaires → Exécuter quand même). Les MISES À JOUR sont signées et vérifiées par l'app.
- ⛔ Pas de Firebase ni de statistiques dans l'app Windows : ne pas lui attribuer les données Firebase de l'Android.

## Ce que fait l'app (fonctions réelles)
- **Deux façons indépendantes de dicter** : un clavier Android standard (IME, navigable au lecteur d'écran) **et** une
  **bulle de dictée flottante** au-dessus de n'importe quelle app. Si l'une n'est pas disponible, l'autre fonctionne.
- **Mode Clean** : ponctuation et majuscules rétablies automatiquement → un message dicté n'a pas besoin d'être retouché.
- **Réécriture IA** du texte dicté et **traduction en temps réel**. **51 langues** (vérifié 18/10/2026 : `data/Language.kt` liste 52 entrées dont « auto » ; l'app affiche « x/51 »). ⛔ Ne plus écrire « 52 ».
- **Bulle réglable** : taille, opacité, position ancrée, activable app par app.
- **La bulle (refonte de l'app 2.74, vérifiée sur la 2.74.10 le 22/10/2026)** : une pilule à deux moitiés, langue | micro.
  Toucher le micro = dicter ; appui long = dicter puis traduire (réglable). Toucher la moitié langue = un menu : langue de
  dictée et de traduction (inversion en un geste), style, Emojis, copier la dernière dictée, Interprète, traduire le
  presse-papiers. **Glisser la bulle** fait apparaître un panneau : Précédent · Traduire · Corriger · Emojis · Suivant —
  lâcher la bulle dessus agit sur le texte déjà écrit dans le champ (Précédent / Suivant = retour arrière comme au clavier).
  EN : « Drag the bubble onto Translate, Correct or Emojis to rework what you already wrote, and step back like on the keyboard. »
- **Notification : FACULTATIVE**, pas nécessaire pour dicter (raccourcis : langues, afficher/masquer la bulle, Interprète,
  traduire le presse-papiers, recopier la dernière dictée). ⛔ Ne pas la présenter comme une 3ᵉ façon de dicter.
- **Mode Interprète** : pour une conversation orale entre deux langues (écran dédié, `ui/InterpreterActivity.kt` ; cité
  dans la fiche Play fr-FR « un mode Interprète pour les conversations orales »). Ajouté le 19/10/2026.
- **App 2.75 (en production le 24/10/2026, vérifié dans le code 2.75.3)** :
  - **Une dictée n'est plus perdue** : si elle ne peut pas être insérée (clavier baissé pendant la dictée, champ quitté,
    réseau revenu après coup), le texte est gardé et une pastille « Insérer » apparaît au prochain champ touché ; un
    toucher l'insère. Une dictée qui a échoué faute de réseau peut être réessayée. Gardé **en mémoire seulement, 5 minutes**
    (`PendingDictationHolder.kt`, `RetryAudioHolder.kt`). Jamais pour un champ mot de passe ou une app sensible.
    EN : « If a dictation can't be inserted, DictoKey keeps it for a few minutes and offers to insert it in the next field you tap. »
    ⛔ Ne pas écrire « sauvegardée » / « saved forever » / « backed up » (5 min, en mémoire) ; jamais d'insertion automatique.
  - **« Traduire avec DictoKey »** (EN « Translate with DictoKey ») : sélectionner un texte dans une app → menu de
    sélection d'Android → la traduction s'affiche dans une carte posée sur l'app (copier, ou remplacer la sélection quand
    l'app le permet) (`ui/ProcessTextTranslateActivity.kt`). ⛔ Ne pas dire si c'est gratuit ou Premium.
  - Réglages de la bulle réorganisés (réglages plus clairs). ⛔ Ne pas nommer de réglage précis sans le vérifier dans l'app.
- **Correction vocale** : dans le clavier, un appui long sur le bouton de dictée permet de DIRE la correction à apporter
  au texte (`api/CorrectApi.kt`, `ime/DictoKeyIME.kt`). Ajouté le 19/10/2026.
- **Détection automatique de la langue** : option « Auto-detect » dans le choix de langue (`data/Language.kt`). Ajouté le 19/10/2026.
- ⛔ Pour ces trois fonctions, ne PAS écrire si elles sont gratuites ou Premium (non vérifié au 19/10/2026).
  → **Exception vérifiée le 22/10/2026 pour l'Interprète** (passerelle v1.10.0, app 2.74) : les utilisateurs gratuits ont
  un **essai de 3 échanges par jour** ; au-delà, Premium. EN : « Free users can try the Interpreter 3 times a day. »
- **Coexiste avec TalkBack** (la bulle ne dispute pas le contrôle de l'écran au lecteur d'écran).
- **Sans compte** : aucun formulaire d'inscription pour commencer.
- **Apps sensibles bloquées automatiquement** : banques, gestionnaires de mots de passe, portefeuilles crypto.
- Fonctionne **dans la plupart des apps** (⛔ ne jamais écrire « toutes les apps » : les apps sensibles sont exclues).
- Reconnaissance vocale **dans le cloud** (connexion internet nécessaire). ⛔ Ne jamais écrire « hors ligne »/« offline ».
  ⛔ Ne pas nommer le fournisseur de transcription. ⛔ Ne jamais écrire « Whisper », « Groq », « OpenAI » à propos de
  DictoKey : faux depuis le 03/10/2026 (moteur Microsoft MAI-Transcribe-2 pour presque toutes les langues).

## Prix (HAUSSE du 23/10/2026 ~23:00, décision Quang : alignement sur le marché — vérifié dans Play Console)
- **Gratuit** avec une limite quotidienne de dictées (**30 par jour** au moment de la rédaction).
- **Premium** : **7,99 €/mois** ou **59,99 €/an** (≈ -37 %), **7 jours d'essai gratuit** sur les deux formules
  pour les nouveaux abonnés. Play affiche le prix en monnaie locale (USA 7,49 $/mois et 54,99 $/an hors taxes,
  UK 6,49 £ / 49,99 £, Canada 9,99 CAD / 77,99 CAD, Australie 11,99 AUD / 86,99 AUD) : en anglais écrire
  « about $7.50/month » / « about $55 per year », jamais un prix en dollars présenté comme exact.
  ⛔ Anciens prix, FAUX pour un nouvel abonné : 4,99 € / -42 % (avant octobre) et 4,79 € / 34,99 € / -39 % (jusqu'au
  23/10/2026). Les abonnés d'avant le 23/10 gardent leur ancien prix (Play) : ne pas en parler sur le site.
- **Premium = 1 000 dictées par jour**, et le Mode Interprète est inclus. ⛔ Ne JAMAIS écrire « illimité » / « unlimited »
  à propos de DictoKey (dictées ou Interprète) : il y a une limite quotidienne, même en Premium (passerelle :
  `TIERS.premium.daily = 1000`). EN : « Premium: 1,000 dictations a day, Interpreter Mode included. »

## Confidentialité (formulations AUTORISÉES uniquement)
- « Conforme RGPD » / « GDPR compliant » · « aucun enregistrement conservé » / « no recordings stored » · « no ads ».
- ⛔ **Ne jamais écrire « no tracking »** (l'app embarque des statistiques d'usage anonymes).
- Accessibilité (corrigé le 22/10/2026, app 2.74.10 — l'ancienne formule « sert UNIQUEMENT à afficher la bulle et
  insérer le texte ; ne lit pas l'écran » est FAUSSE depuis la 2.74.4) : la permission sert à afficher la bulle, à
  insérer le texte dicté et à LIRE LE CHAMP ACTIF sur le téléphone (Précédent / Suivant, espace avant une dictée).
  Ce texte ne quitte le téléphone que si l'utilisateur lâche la bulle sur Traduire, Corriger ou Emojis, et n'est pas
  conservé. Elle n'enregistre pas les frappes et ne surveille pas l'activité. Champs mot de passe et apps sensibles
  (banque, gestionnaires de mots de passe, portefeuilles crypto) : bloqués.
  Formulation EN autorisée : « The Accessibility permission shows the bubble, inserts your dictated text and reads the
  active field on your phone (for Previous / Next and spacing); that text is sent only when you drop the bubble on
  Translate, Correct or Emojis, and it is not stored. »
  ⛔ Ne plus écrire : « only to show the bubble and insert », « does not read the screen / screen content »,
  « does not transmit accessibility data » (`check_site.py` les refuse).

## Publics (positionnement officiel = accessibilité d'abord)
Motricité réduite / mains peu mobiles · tremblements, Parkinson · arthrite, tendinite (RSI), douleurs chroniques ·
dyslexie, TDAH · toute personne qui écrit plus vite en parlant.
⛔ Ne pas cibler « basse vision » / « malvoyants » / « aveugles » comme public (retiré du site le 24/07, absent de la fiche
Play — décision 18/10/2026). Décrire la compatibilité TalkBack comme une FONCTION, jamais comme un public visé.

## Interdits absolus
- ⛔ Aucun témoignage ou citation d'utilisateur (même anonymisé), aucune note/avis inventé, aucun chiffre d'installs.
- ⛔ Aucune affirmation médicale (« soigne », « recommandé par les médecins »). Écrire « peut aider », « réduit la frappe ».
- ⛔ Aucun nom de personne de l'équipe. Signature : « DictoKey Team ».
- ⛔ Pas de dénigrement : citer les points forts des concurrents, honnêtement.
