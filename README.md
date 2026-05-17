# ■ DJ Crate Digger ■

> Outil TUI d'extraction et de structuration automatique de tracklists YouTube pour DJs.

**DJ Crate Digger** est une application en ligne de commande (CLI/TUI) conçue spécifiquement pour les DJs afin de rationaliser la recherche musicale à partir de sets YouTube. Il extrait, nettoie et stocke localement les tracklists de manière structurée sans nécessiter de clé d'API Google Cloud.

---

## ⚡ Caractéristiques clés

*   **Extraction robuste sans clé API** : Utilise le moteur `yt-dlp` pour interroger l'API interne de YouTube. Rapide, gratuit, sans quotas.
*   **Parsing intelligent (Regex Engine)** : Repère et isole les timestamps (`00:00`, `[01:23]`, etc.) et la numérotation séquentielle des pistes.
*   **Anti-Spam intégré** : Élimine automatiquement les publicités, liens d'autopromotion (Patreon, Instagram, Spotify, etc.) et lignes inutiles de la description brute.
*   **TUI premium Noir & Blanc** : Interface interactive élégante et minimaliste construite avec `rich` et `questionary`.
*   **Stockage centralisé persistant** : Enregistre automatiquement les tracklists formatées dans des fichiers `.txt` locaux sous `~/dj-crate-digger/crate/` nommés au format strict `YYYY-MM-DD(HHhMM)_[slug].txt`.
*   **Exécution globale** : Palette de commandes complète accessible de n'importe quel répertoire avec la commande globale `cratedig`.

---

## 🛠️ Installation

### Option 1 : Via Homebrew (Recommandé 🍺)

C'est la méthode la plus simple pour installer, mettre à jour et exécuter `cratedig` de manière isolée sans se soucier des dépendances Python globales :

```bash
# Ajouter le Tap Homebrew
brew tap elkwaet/cratedig

# Installer DJ Crate Digger
brew install cratedig
```

### Option 2 : Installation manuelle globale (sans sudo)

Si tu n'utilises pas Homebrew ou si tu souhaites contribuer au développement :

1.  **Cloner le dépôt dans ton espace de travail (ex: `~/PROJ-DEV/`)** :
    ```bash
    git clone https://gitlab.com/elkwaet/dj-crate-digger.git
    cd dj-crate-digger
    ```

2.  **Lancer le script d'installation locale** :
    ```bash
    ./install.sh
    ```
    Ce script va automatiquement :
    *   Rendre le wrapper `bin/cratedig` exécutable.
    *   Créer le lien symbolique `~/.local/bin/cratedig` pointant vers le projet.
    *   Créer le dossier persistant global `~/dj-crate-digger/crate/`.
    *   Ajouter `~/.local/bin` à ton `PATH` dans ton `~/.zshrc` ou `~/.bash_profile` (si ce n'est pas déjà fait).

3.  **Recharger ton terminal** :
    ```bash
    source ~/.zshrc
    ```

---

## 🚀 Palette de commandes (`cratedig`)

Tu peux lancer la commande `cratedig` depuis n'importe quel dossier de ta machine :

```bash
# Lancement de l'interface interactive TUI en plein écran
cratedig

# Ou explicitement
cratedig tui
```

### Commandes CLI directes :

*   **🔍 Analyser une nouvelle vidéo** :
    ```bash
    cratedig digest <URL_YOUTUBE>
    ```
    Extrait instantanément la tracklist, l'affiche dans un tableau premium et la sauvegarde dans ton crate.

*   **📂 Lister tes tracklists** :
    ```bash
    cratedig list
    # ou
    cratedig crate
    ```
    Affiche la liste indexée de toutes les tracklists existantes.

*   **📖 Consulter une tracklist** :
    ```bash
    cratedig view <ID_ou_slug>
    ```
    Affiche le contenu détaillé (ex: `cratedig view 1` pour le fichier le plus récent ou `cratedig view lesinfocus`).

*   **❌ Supprimer une tracklist** :
    ```bash
    cratedig delete <ID_ou_slug>
    ```
    Demande une confirmation et supprime définitivement le fichier du crate.

*   **📍 Localiser le stockage** :
    ```bash
    cratedig path
    ```
    Affiche le chemin absolu du répertoire crate global (`~/dj-crate-digger/crate/`).

*   **ℹ️ Version & Crédits** :
    ```bash
    cratedig version
    ```

---

## 📂 Structure du projet

```text
├── bin/
│   └── cratedig         # Script wrapper de lancement global
├── src/
│   ├── cli.py           # Routeur de la palette de commandes CLI
│   ├── main.py          # Point d'entrée TUI interactif
│   ├── extractor.py     # Logique d'extraction via yt-dlp
│   ├── parser.py        # Logique de parsing de tracklist et anti-spam
│   └── storage.py       # Logique de stockage persistant global (~/dj-crate-digger/crate)
├── tests/
│   ├── test_parser.py   # Tests unitaires du moteur de parsing
│   └── test_integration.py # Test d'intégration réel avec YouTube
├── wiki/                # Documentation détaillée du projet
├── install.sh           # Script d'installation locale non-root
├── requirements.txt     # Dépendances Python
├── LICENSE              # Licence MIT du projet
└── README.md
```

---

## ⚖️ Licence

Ce projet est sous licence MIT. Libres droits de modification et d'utilisation.

---
Développé pour la communauté par **@qwashenergy**.
