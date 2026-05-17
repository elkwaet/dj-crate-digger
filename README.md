# ■ DJ Crate Digger ■

> Outil TUI d'extraction et de structuration automatique de tracklists YouTube pour DJs.

**DJ Crate Digger** est une application en ligne de commande (CLI/TUI) conçue spécifiquement pour les DJs afin de rationaliser la recherche musicale à partir de sets YouTube. Il extrait, nettoie et stocke localement les tracklists de manière structurée sans nécessiter de clé d'API Google Cloud.

---

## ⚡ Caractéristiques clés

*   **Extraction robuste sans clé API** : Utilise le moteur `yt-dlp` pour interroger l'API interne de YouTube. Rapide, gratuit, sans quotas.
*   **Parsing intelligent (Regex Engine)** : Repère et isole les timestamps (`00:00`, `[01:23]`, etc.) et la numérotation séquentielle des pistes.
*   **Anti-Spam intégré** : Élimine automatiquement les publicités, liens d'autopromotion (Patreon, Instagram, Spotify, etc.) et lignes inutiles de la description brute.
*   **TUI premium Noir & Blanc** : Interface interactive élégante et minimaliste construite avec `rich` et `questionary`.
*   **Stockage structuré (Crate)** : Enregistre automatiquement les tracklists formatées dans des fichiers `.txt` locaux sous `./crate/` nommés par date et titre de la vidéo.

---

## 🛠️ Installation

1.  **Cloner le dépôt** :
    ```bash
    git clone [repo-url]
    cd dj-crate-digger
    ```

2.  **Créer l'environnement virtuel & installer les dépendances** :
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```

---

## 🚀 Utilisation

Lance le TUI interactif en une commande :

```bash
.venv/bin/python src/main.py
```

### Options du menu principal :
- **🔍 Analyser une nouvelle vidéo** : Saisis simplement l'URL d'une vidéo YouTube (ex: DJ Set, podcast, mix) et observe l'extraction.
- **📂 Parcourir les tracklists locales** : Affiche la liste des tracklists de ton crate local triées par date. Tu peux les lire directement ou les supprimer.
- **🚪 Quitter** : Quitte l'application proprement.

---

## 📂 Structure du projet

```text
├── crate/               # Dossier de stockage des tracklists (.txt)
├── src/
│   ├── main.py          # Point d'entrée & Interface TUI interactive
│   ├── extractor.py     # Logique d'extraction via yt-dlp
│   ├── parser.py        # Logique de parsing de tracklist et anti-spam
│   └── storage.py       # Logique de persistance et lecture des fichiers
├── tests/
│   ├── test_parser.py   # Tests unitaires du moteur de parsing
│   └── test_integration.py # Test d'intégration réel avec YouTube
├── wiki/                # Documentation détaillée du projet
├── requirements.txt     # Dépendances Python
└── README.md
```

---

## ⚖️ Licence

Ce projet est sous licence MIT. Libre à toi de le forker et de l'améliorer !
