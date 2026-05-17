#!/bin/bash

# Script d'installation locale pour DJ Crate Digger (cratedig)
# Développé pour la communauté par @qwashenergy (Elkwaet)

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BIN_DIR="$HOME/.local/bin"
TARGET_LINK="$BIN_DIR/cratedig"
SHELL_RC_ZSH="$HOME/.zshrc"
SHELL_RC_BASH="$HOME/.bash_profile"
CRATE_DIR="$HOME/dj-crate-digger/crate"

echo "🚀 Préparation de l'installation locale de cratedig..."

# 1. Rendre le script wrapper exécutable
chmod +x "$PROJECT_DIR/bin/cratedig"

# 2. Créer le dossier ~/.local/bin s'il n'existe pas
if [ ! -d "$BIN_DIR" ]; then
    echo "📁 Création du dossier $BIN_DIR..."
    mkdir -p "$BIN_DIR"
fi

# 3. Créer le répertoire persistant pour les crates s'il n'existe pas
if [ ! -d "$CRATE_DIR" ]; then
    echo "📁 Création du répertoire crate persistant dans $CRATE_DIR..."
    mkdir -p "$CRATE_DIR"
fi

# 4. Créer ou mettre à jour le lien symbolique
echo "🔗 Création du lien symbolique dans $BIN_DIR..."
ln -sf "$PROJECT_DIR/bin/cratedig" "$TARGET_LINK"

# 5. Vérifier l'ajout au PATH de l'utilisateur
add_to_path() {
    local rc_file=$1
    if [ -f "$rc_file" ]; then
        if ! grep -q "$BIN_DIR" "$rc_file"; then
            echo "" >> "$rc_file"
            echo "# Ajouté par dj-crate-digger" >> "$rc_file"
            echo "export PATH=\"\$HOME/.local/bin:\$PATH\"" >> "$rc_file"
            echo "✅ Ajout de $BIN_DIR au PATH dans $rc_file"
        else
            echo "✅ $BIN_DIR est déjà dans le PATH de $rc_file"
        fi
    fi
}

add_to_path "$SHELL_RC_ZSH"
add_to_path "$SHELL_RC_BASH"

echo ""
echo "🎉 Installation terminée !"
echo "👉 Tu peux maintenant lancer l'application en tapant la commande : cratedig"
echo "⚠️  Note : Si la commande n'est pas reconnue, redémarre ton terminal ou tape 'source ~/.zshrc'."
