# Changelog

Toutes les modifications notables apportées au projet **DJ Crate Digger** seront consignées dans ce fichier. Le format est inspiré de [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/).

---

## [1.0.0] - 2026-05-17

### DOC
- Initialisation du [README.md](file:///Users/elk/.gemini/antigravity/scratch/dj-crate-digger/README.md).
- Création du [CHANGELOG.md](file:///Users/elk/.gemini/antigravity/scratch/dj-crate-digger/CHANGELOG.md).
- Initialisation de la documentation continue dans le répertoire [wiki/](file:///Users/elk/.gemini/antigravity/scratch/dj-crate-digger/wiki/).

### ADD
- Initialisation de la structure du projet Python.
- Création du module d'extraction [src/extractor.py](file:///Users/elk/.gemini/antigravity/scratch/dj-crate-digger/src/extractor.py) basé sur `yt-dlp`.
- Création du module de parsing intelligent [src/parser.py](file:///Users/elk/.gemini/antigravity/scratch/dj-crate-digger/src/parser.py) avec détection de timestamps/numérotations et filtrage anti-spam de la description.
- Création du module de stockage local [src/storage.py](file:///Users/elk/.gemini/antigravity/scratch/dj-crate-digger/src/storage.py) pour la persistance sous `./crate/`.
- Création de l'interface TUI interactive Noir & Blanc [src/main.py](file:///Users/elk/.gemini/antigravity/scratch/dj-crate-digger/src/main.py) avec `questionary` et `rich`.
- Ajout de la suite de tests unitaires [tests/test_parser.py](file:///Users/elk/.gemini/antigravity/scratch/dj-crate-digger/tests/test_parser.py).
- Ajout du test d'intégration réseau [tests/test_integration.py](file:///Users/elk/.gemini/antigravity/scratch/dj-crate-digger/tests/test_integration.py).
