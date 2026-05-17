#!/bin/bash

# release.sh - Script de release interactif pour DJ Crate Digger
# Développé avec rigueur par Antigravity pour @qwashenergy (Elkwaet)

echo "=========================================================="
echo "■ DJ CRATE DIGGER - AUTOMATION DE RELEASE ■"
echo "=========================================================="

# 1. Vérification de la propreté du dépôt Git
if [ -n "$(git status --porcelain)" ]; then
    echo "⚠️ Attention : Ton dépôt local contient des changements non commités."
    git status -s
    echo ""
    read -p "❓ Veux-tu continuer quand même ? (y/N) : " continue_dirty
    if [[ ! "$continue_dirty" =~ ^[Yy]$ ]]; then
        echo "❌ Release annulée pour garder le dépôt propre."
        exit 1
    fi
fi

# 2. Détection de la version actuelle
CURRENT_VERSION=$(python3 -c "import sys; sys.path.append('src'); import version; print(version.__version__)" 2>/dev/null)
if [ -z "$CURRENT_VERSION" ]; then
    CURRENT_VERSION="1.1.0"
fi

echo "🏷️ Version actuelle détectée : v$CURRENT_VERSION"

# Suggestion de la version suivante (incrément du patch par défaut)
IFS='.' read -r major minor patch <<< "$CURRENT_VERSION"
NEXT_PATCH=$((patch + 1))
SUGGESTED_VERSION="${major}.${minor}.${NEXT_PATCH}"

read -p "🚀 Entre le numéro de la nouvelle version [$SUGGESTED_VERSION] : " input_version
NEW_VERSION=${input_version:-$SUGGESTED_VERSION}

# Formatage avec 'v' pour les tags git
TAG_NAME="v$NEW_VERSION"

echo "----------------------------------------------------------"
echo "➡️ Préparation de la release $TAG_NAME..."
echo "----------------------------------------------------------"

# 3. Mise à jour de version.py
echo "📝 Mise à jour de src/version.py..."
echo "__version__ = \"$NEW_VERSION\"" > src/version.py

# 4. Mise à jour du tag d'URL dans Formula/cratedig.rb locale
echo "📝 Mise à jour de Formula/cratedig.rb locale..."
sed -i '' "s|archive/refs/tags/v.*\.tar\.gz|archive/refs/tags/$TAG_NAME.tar.gz|g" Formula/cratedig.rb 2>/dev/null || \
sed -i "s|archive/refs/tags/v.*\.tar\.gz|archive/refs/tags/$TAG_NAME.tar.gz|g" Formula/cratedig.rb

# 5. Lancement facultatif des tests
read -p "🧪 Veux-tu lancer les tests pytest avant la release ? (Y/n) : " run_tests
if [[ ! "$run_tests" =~ ^[Nn]$ ]]; then
    echo "Running pytest..."
    pytest
    if [ $? -ne 0 ]; then
        echo "❌ Les tests ont échoué. Release annulée."
        exit 1
    fi
    echo "✅ Tous les tests sont au vert !"
fi

# 6. Commit Git
echo "----------------------------------------------------------"
echo "💾 Commit & Push Git"
echo "----------------------------------------------------------"

read -p "📝 Message du commit [UPDATE: release $TAG_NAME] : " commit_msg
FINAL_COMMIT_MSG=${commit_msg:-"UPDATE: release $TAG_NAME"}

git add src/version.py Formula/cratedig.rb
git commit -m "$FINAL_COMMIT_MSG"

# Récupération de la branche courante
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)

# Double Push de la branche
echo "🚀 Push de la branche $CURRENT_BRANCH vers GitLab (origin)..."
git push origin "$CURRENT_BRANCH"

echo "🚀 Push de la branche $CURRENT_BRANCH vers GitHub (public)..."
git push public "$CURRENT_BRANCH"

# Création et push du Tag
echo "🏷️ Création du tag $TAG_NAME..."
git tag -a "$TAG_NAME" -m "Release $TAG_NAME"

echo "🚀 Push du tag $TAG_NAME vers GitLab (origin)..."
git push origin "$TAG_NAME"

echo "🚀 Push du tag $TAG_NAME vers GitHub (public)..."
git push public "$TAG_NAME"

# 7. Création de la Release GitHub
echo "----------------------------------------------------------"
echo "📦 Création de la Release GitHub"
echo "----------------------------------------------------------"
echo "Attente de propagation de 3 secondes..."
sleep 3

echo "🚀 Publication de la release $TAG_NAME sur GitHub..."
gh release create "$TAG_NAME" --repo "elkwaet/dj-crate-digger" --title "DJ Crate Digger $TAG_NAME" --generate-notes

if [ $? -ne 0 ]; then
    echo "❌ Échec de la création de la release sur GitHub."
    exit 1
fi
echo "✅ Release créée avec succès sur GitHub !"

# 8. Récupération et calcul du SHA256 de l'archive tar.gz
echo "----------------------------------------------------------"
echo "🔒 Calcul du SHA256 du tar.gz public"
echo "----------------------------------------------------------"
TARBALL_URL="https://github.com/elkwaet/dj-crate-digger/archive/refs/tags/$TAG_NAME.tar.gz"
TEMP_TARBALL="/tmp/dj-crate-digger-$NEW_VERSION.tar.gz"

echo "📥 Téléchargement temporaire depuis : $TARBALL_URL..."
curl -L -s -o "$TEMP_TARBALL" "$TARBALL_URL"

if [ ! -f "$TEMP_TARBALL" ] || [ ! -s "$TEMP_TARBALL" ]; then
    echo "❌ Échec du téléchargement de l'archive. Impossible de calculer le SHA256."
    exit 1
fi

echo "🧮 Calcul du hash SHA256..."
if command -v shasum &> /dev/null; then
    SHA256_HASH=$(shasum -a 256 "$TEMP_TARBALL" | awk '{print $1}')
elif command -v sha256sum &> /dev/null; then
    SHA256_HASH=$(sha256sum "$TEMP_TARBALL" | awk '{print $1}')
else
    echo "❌ Outil de hashage introuvable (shasum ou sha256sum). Veuillez calculer le SHA256 manuellement."
    rm -f "$TEMP_TARBALL"
    exit 1
fi

echo "🔑 SHA256 calculé : $SHA256_HASH"
rm -f "$TEMP_TARBALL"

# 9. Clonage et mise à jour du Tap Homebrew
echo "----------------------------------------------------------"
echo "🍺 Mise à jour du Tap Homebrew elkwaet/homebrew-cratedig"
echo "----------------------------------------------------------"
TEMP_TAP_DIR="/tmp/homebrew-cratedig-temp"
rm -rf "$TEMP_TAP_DIR"

echo "📥 Clonage du dépôt du tap..."
git clone git@github.com:elkwaet/homebrew-cratedig.git "$TEMP_TAP_DIR"

if [ $? -ne 0 ]; then
    echo "❌ Échec du clonage du tap Homebrew."
    exit 1
fi

# Création du sous-dossier Formula si absent dans le tap
mkdir -p "$TEMP_TAP_DIR/Formula"

# Copie de la formule mise à jour localement
cp Formula/cratedig.rb "$TEMP_TAP_DIR/Formula/cratedig.rb"

# Remplacement du SHA256 temporaire par le SHA256 réel calculé dans la formule copiée
echo "📝 Injection du SHA256 réel dans la formule..."
sed -i '' "s/REPLACE_WITH_SHA256/$SHA256_HASH/g" "$TEMP_TAP_DIR/Formula/cratedig.rb" 2>/dev/null || \
sed -i "s/REPLACE_WITH_SHA256/$SHA256_HASH/g" "$TEMP_TAP_DIR/Formula/cratedig.rb"

# Push vers le tap
echo "📤 Commit & Push sur le Tap Homebrew..."
cd "$TEMP_TAP_DIR" || exit 1
git add Formula/cratedig.rb
git commit -m "UPDATE: release cratedig $TAG_NAME"
git push origin main

if [ $? -eq 0 ]; then
    echo "=========================================================="
    echo "🎉 FÉLICITATIONS ! RELEASE $TAG_NAME DÉPLOYÉE ET DISTRIBUÉE !"
    echo "=========================================================="
    echo "Les utilisateurs peuvent désormais l'installer ou la mettre à jour :"
    echo "  brew tap elkwaet/cratedig"
    echo "  brew install cratedig"
    echo "=========================================================="
else
    echo "❌ Échec de la mise à jour du Tap Homebrew."
fi

# Nettoyage
rm -rf "$TEMP_TAP_DIR"
