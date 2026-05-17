import os
import re
from datetime import datetime
from typing import List, Dict, Any

# Chemin absolu du dossier crate dans le HOME de l'utilisateur (centralisé)
CRATE_DIR = os.path.expanduser('~/dj-crate-digger/crate')

def ensure_crate_dir() -> None:
    """
    S'assure que le répertoire crate existe.
    """
    if not os.path.exists(CRATE_DIR):
        os.makedirs(CRATE_DIR)

def slugify(text: str) -> str:
    """
    Convertit un titre en un slug sûr pour un nom de fichier.
    """
    # Remplacement des caractères non alphanumériques par des underscores
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '_', text)
    # Suppression des underscores en début/fin et doublons
    text = re.sub(r'_+', '_', text).strip('_')
    # Limite à 50 caractères pour éviter des noms de fichiers trop longs
    return text[:50]

def save_tracklist(metadata: Dict[str, Any], tracks: List[str], detected: bool) -> str:
    """
    Sauvegarde la tracklist dans un fichier au format .txt structuré.
    Retourne le chemin absolu du fichier créé.
    """
    ensure_crate_dir()
    
    # Date et heure actuelles pour le nom du fichier et les métadonnées
    now = datetime.now()
    date_file_str = now.strftime('%Y-%m-%d(%Hh%M)')
    analysis_date_str = now.strftime('%Y-%m-%d %H:%M')
    title_slug = slugify(metadata.get('title', 'video'))
    
    filename = f"{date_file_str}_{title_slug}.txt"
    filepath = os.path.join(CRATE_DIR, filename)
    
    # Contenu structuré
    content_lines = [
        "==================================================",
        "DJ CRATE DIGGER - EXTRACTED TRACKLIST",
        "==================================================",
        f"Titre de la vidéo   : {metadata.get('title')}",
        f"Lien YouTube        : {metadata.get('webpage_url')}",
        f"Date de publication : {metadata.get('upload_date')}",
        f"Date d'analyse      : {analysis_date_str}",
        "==================================================",
        "",
    ]
    
    if detected:
        content_lines.append("TRACKLIST DÉTECTÉE :")
    else:
        content_lines.append("EXTRACTION BRUTE (Aucune tracklist structurée détectée d'office) :")
        
    content_lines.append("--------------------------------------------------")
    for track in tracks:
        content_lines.append(track)
    content_lines.append("--------------------------------------------------")
    
    # Écriture dans le fichier
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(content_lines))
        
    return filepath

def list_extracted_files() -> List[Dict[str, str]]:
    """
    Retourne la liste de tous les fichiers de tracklists extraits
    sous forme de dictionnaires avec le nom de fichier et le chemin absolu,
    classés par date de modification décroissante.
    """
    ensure_crate_dir()
    files = []
    for entry in os.scandir(CRATE_DIR):
        if entry.is_file() and entry.name.endswith('.txt'):
            files.append({
                'name': entry.name,
                'path': entry.path,
                'mtime': entry.stat().st_mtime
            })
            
    # Tri par date de modification décroissante (les plus récents en premier)
    files.sort(key=lambda x: x['mtime'], reverse=True)
    
    # Retourne uniquement les infos utiles
    return [{'name': f['name'], 'path': f['path']} for f in files]

def read_file_content(filepath: str) -> str:
    """
    Lit et retourne le contenu complet d'un fichier de tracklist.
    """
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    return "Fichier introuvable."
