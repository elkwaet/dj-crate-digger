# Guide d'utilisation - DJ Crate Digger

Ce guide t'explique comment exploiter pleinement **DJ Crate Digger** pour enrichir ton crate musical.

---

## 1. Démarrer l'application

Lance la commande suivante dans ton terminal :

```bash
cd /Users/elk/.gemini/antigravity/scratch/dj-crate-digger
.venv/bin/python src/main.py
```

L'application démarre sur un menu interactif Noir & Blanc épuré. Utilise les **flèches directionnelles** de ton clavier pour naviguer et la touche **Entrée** pour valider ton choix.

---

## 2. Analyser un DJ set ou un Mix

1. Sélectionne option **`🔍 Analyser une nouvelle vidéo YouTube`**.
2. Copie et colle l'URL de la vidéo YouTube de ton choix (ex: `https://www.youtube.com/watch?v=dQw4w9WgXcQ`).
3. Valide en appuyant sur **Entrée**.
4. Le système va extraire la description de la vidéo, repérer les morceaux de la tracklist et filtrer automatiquement tous les spams publicitaires (liens Instagram, Patreon, Soundcloud, etc.).
5. **Résultat** : Un message de succès apparaît avec un aperçu des 15 premiers morceaux de la tracklist. Un fichier texte formaté est instantanément enregistré dans ton dossier local `./crate/`.

---

## 3. Parcourir ton Crate local

1. Sélectionne l'option **`📂 Parcourir les tracklists locales (Crate)`**.
2. La liste de toutes tes tracklists extraites s'affiche, classées de la plus récente à la plus ancienne.
3. Choisis-en une pour l'afficher instantanément à l'écran dans un panneau élégant.
4. **Actions rapides** :
   - **← Revenir à la liste** : Pour retourner aux autres tracklists.
   - **❌ Supprimer cette tracklist** : Supprime définitivement le fichier physique de ton disque après confirmation.

---

## 4. Exploiter tes tracklists (.txt)

Chaque tracklist stockée dans `./crate/` est un fichier texte brut formaté de la façon suivante :

```text
==================================================
DJ CRATE DIGGER - EXTRACTED TRACKLIST
==================================================
Titre de la vidéo   : [Titre exact de la vidéo]
Lien YouTube        : [URL de la vidéo]
Date de publication : [Date originale d'upload]
Date d'analyse      : [Date de ton extraction]
==================================================

TRACKLIST DÉTECTÉE :
--------------------------------------------------
00:00 Morceau 1
05:12 Morceau 2
...
--------------------------------------------------
```

Tu peux ouvrir ces fichiers dans n'importe quel éditeur de texte, les importer dans ton logiciel de DJing (Rekordbox, Serato, Traktor) ou les copier-coller dans tes notes.
