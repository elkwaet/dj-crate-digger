# Architecture technique - DJ Crate Digger

Ce document détaille l'architecture globale de l'application **DJ Crate Digger (Phase 1)** et les interactions entre ses composants.

---

## 1. Vue d'ensemble du flux de données

Le schéma suivant montre comment une URL YouTube saisie par l'utilisateur est transformée en un fichier tracklist structuré et stocké localement :

```text
  [ Utilisateur ]
         │
         ▼ (Saisit l'URL)
   [ src/main.py ]  ◄── (Affiche le menu et les statuts TUI via Rich/Questionary)
         │
         ▼ (Envoie l'URL)
[ src/extractor.py ] ◄── (Exécute yt-dlp de façon interne sans clé API)
         │
         ▼ (Retourne Titre, Date, Description brute)
  [ src/parser.py ]  ◄── (Regex Engine : extrait timestamps/numéros + filtre spams)
         │
         ▼ (Retourne la liste des morceaux nettoyés)
  [ src/storage.py ] ◄── (Écrit le fichier structuré dans `./crate/`)
         │
         ▼ (Sauvegarde locale)
   [ Fichier .txt ]
```

---

## 2. Rôle des composants

### 2.1. Interface TUI (`src/main.py`)
- Fournit l'expérience interactive utilisateur.
- Utilise `questionary` pour la saisie clavier (menus à flèches, champs texte) afin de simplifier la navigation.
- Utilise `rich` pour appliquer une charte graphique premium **Noir & Blanc** (Nuances de gris, bordures simples, tableaux structurés).

### 2.2. Extracteur (`src/extractor.py`)
- Utilise la bibliothèque Python `yt-dlp`.
- Configure `YoutubeDL` pour extraire uniquement le dictionnaire JSON (`skip_download=True`), garantissant une extraction en moins de 3 secondes.
- Retourne uniquement les champs essentiels : `title`, `description`, `upload_date`, et `webpage_url`.

### 2.3. Parser (`src/parser.py`)
- Analyse la description ligne par ligne.
- Applique des expressions régulières pour détecter :
  - Les timestamps : `HH:MM:SS` ou `MM:SS` (avec ou sans crochets/parenthèses).
  - Les numérotations séquentielles en début de ligne (`01.`, `2 -`, etc.).
- Filtre activement les lignes d'autopromotion et spams de réseaux sociaux via une liste noire de mots-clés (`http`, `@username`, `patreon`, `instagram`, etc.).

### 2.4. Stockage (`src/storage.py`)
- Sécurise la création du dossier `./crate/` à la racine du projet.
- Convertit le titre de la vidéo en un "slug" de nom de fichier propre.
- Enregistre le résultat sous la forme `YYYY-MM-DD_[Slug_Titre].txt`.
- Gère la lecture et la suppression des fichiers depuis le TUI.

---

## 3. Choix techniques notables

- **Aucune dépendance lourde de base de données** : Le stockage au format `.txt` simple et humainement lisible répond parfaitement à la philosophie "Crate" (comme un dossier physique de vinyles dans lequel le DJ pioche).
- **Indépendance réseau** : L'utilisation de `yt-dlp` en bibliothèque locale évite l'utilisation d'APIs tierces payantes ou limitées par des clés secrètes.
