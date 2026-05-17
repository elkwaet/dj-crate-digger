import sys
import os
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table

# Ajout du dossier courant au path pour les imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import extractor
import parser
import storage
import main as tui_main

console = Console()

VERSION = "1.1.0"
AUTHOR = "@qwashenergy (Elkwaet)"
LICENSE_HINT = "Copyright (c) 2026 Elkwaet - MIT License"

def show_version() -> None:
    """Affiche la version et les crédits de l'auteur."""
    banner_text = Text()
    banner_text.append("■ DJ CRATE DIGGER ■\n", style="bold white")
    banner_text.append(f"Version : {VERSION}\n", style="white")
    banner_text.append(f"Développé pour la communauté par {AUTHOR}\n", style="italic white")
    banner_text.append(LICENSE_HINT, style="grey50")
    
    console.print(Panel(
        banner_text,
        border_style="white",
        expand=False,
        padding=(1, 3)
    ))

def show_help() -> None:
    """Affiche l'aide d'utilisation de la palette de commandes."""
    table = Table(title="■ COMMANDES DISPONIBLES ■", show_header=True, header_style="bold white", border_style="grey37")
    table.add_column("Commande", style="bold white")
    table.add_column("Description", style="white")
    
    table.add_row("cratedig [tui]", "Lance l'interface interactive TUI en plein écran.")
    table.add_row("cratedig digest <URL>", "Analyse et extrait directement la tracklist d'une vidéo YouTube.")
    table.add_row("cratedig list | crate", "Affiche la liste indexée de toutes les tracklists extraites.")
    table.add_row("cratedig view <ID_ou_slug>", "Affiche le contenu détaillé d'une tracklist spécifiée par son index ou son nom.")
    table.add_row("cratedig delete <ID_ou_slug>", "Supprime définitivement une tracklist du crate.")
    table.add_row("cratedig path", "Affiche le chemin absolu du répertoire crate.")
    table.add_row("cratedig version", "Affiche les informations de version et de crédits.")
    table.add_row("cratedig help", "Affiche ce menu d'aide.")
    
    console.print(table)
    console.print()

def handle_digest(url: str) -> None:
    """Extrait directement une tracklist depuis une URL YouTube."""
    if not url.strip().startswith(('http://', 'https://', 'www.')):
        console.print("[bold red]Erreur :[/bold red] URL YouTube invalide.\n")
        sys.exit(1)
        
    try:
        with console.status("[white]Extraction des données YouTube...[/white] (via yt-dlp)"):
            metadata = extractor.extract_metadata(url)
            tracks, detected = parser.parse_tracklist(metadata['description'])
            filepath = storage.save_tracklist(metadata, tracks, detected)
            
        console.print()
        status_text = "TRACKLIST DÉTECTÉE & EXTRAITE" if detected else "EXTRACTION BRUTE SAUVEGARDÉE"
        console.print(Panel(
            Text(f"✔ {status_text}\n\nFichier : {os.path.basename(filepath)}\nMorceaux : {len(tracks)}", style="bold white"),
            border_style="white",
            expand=False,
            padding=(1, 2)
        ))
        console.print()
        
        # Affichage
        table = Table(show_header=True, header_style="bold white", border_style="grey37")
        table.add_column("Tracklist", style="white")
        for track in tracks:
            table.add_row(track)
            
        console.print(table)
        console.print()
        
    except Exception as e:
        console.print(f"\n[bold red]Erreur lors de l'extraction :[/bold red] {str(e)}\n")
        sys.exit(1)

def resolve_file(target: str) -> str:
    """Résout une cible (index numérique ou début de slug de fichier) vers un chemin absolu de fichier."""
    files = storage.list_extracted_files()
    if not files:
        console.print("[grey50]Le crate est actuellement vide.[/grey50]")
        sys.exit(1)
        
    # Essai de résolution par index
    if target.isdigit():
        idx = int(target) - 1
        if 0 <= idx < len(files):
            return files[idx]['path']
        else:
            console.print(f"[bold red]Erreur :[/bold red] Index {target} hors limites (1 à {len(files)}).\n")
            sys.exit(1)
            
    # Essai de résolution par nom ou slug de fichier
    for f in files:
        if target.lower() in f['name'].lower():
            return f['path']
            
    console.print(f"[bold red]Erreur :[/bold red] Impossible de trouver une tracklist correspondant à '{target}'.\n")
    sys.exit(1)

def handle_list() -> None:
    """Affiche la liste des tracklists existantes sous forme de tableau indexé."""
    files = storage.list_extracted_files()
    if not files:
        console.print("\n[grey50]Aucune tracklist extraite dans ton crate pour le moment.[/grey50]\n")
        return
        
    table = Table(show_header=True, header_style="bold white", border_style="grey37", title="■ CRATE LOCAL ■")
    table.add_column("ID", style="bold white", justify="right")
    table.add_column("Nom du fichier de tracklist", style="white")
    
    for idx, f in enumerate(files, 1):
        table.add_row(str(idx), f['name'])
        
    console.print()
    console.print(table)
    console.print(f"\n[grey50]Total : {len(files)} tracklist(s) extraite(s) dans {storage.CRATE_DIR}[/grey50]\n")

def handle_view(target: str) -> None:
    """Affiche le contenu d'un fichier de tracklist spécifié."""
    filepath = resolve_file(target)
    content = storage.read_file_content(filepath)
    
    console.print()
    console.print(Panel(
        content,
        title=os.path.basename(filepath),
        title_align="left",
        border_style="white"
    ))
    console.print()

def handle_delete(target: str) -> None:
    """Supprime une tracklist spécifiée."""
    filepath = resolve_file(target)
    filename = os.path.basename(filepath)
    
    # Confirmation simple
    confirm = input(f"Es-tu sûr de vouloir supprimer définitivement '{filename}' ? (o/N) : ")
    if confirm.lower() in ('o', 'oui', 'y', 'yes'):
        os.remove(filepath)
        console.print(f"[white]✔ Fichier '{filename}' supprimé avec succès.[/white]")
    else:
        console.print("[grey50]Suppression annulée.[/grey50]")

def handle_path() -> None:
    """Affiche le chemin absolu du dossier crate."""
    console.print(f"[white]Dossier Crate :[/white] {storage.CRATE_DIR}")

def main() -> None:
    """Point d'entrée principal du routeur CLI."""
    if len(sys.argv) < 2:
        # Lancement par défaut du TUI interactif
        tui_main.main()
        return
        
    cmd = sys.argv[1].lower()
    
    if cmd in ("tui", "interactive"):
        tui_main.main()
        
    elif cmd == "digest":
        if len(sys.argv) < 3:
            console.print("[bold red]Erreur :[/bold red] URL manquante pour la commande 'digest'.\n")
            console.print("Usage : cratedig digest <URL>")
            sys.exit(1)
        handle_digest(sys.argv[2])
        
    elif cmd in ("list", "crate"):
        handle_list()
        
    elif cmd == "view":
        if len(sys.argv) < 3:
            console.print("[bold red]Erreur :[/bold red] Cible manquante (ID ou nom de fichier) pour la commande 'view'.\n")
            console.print("Usage : cratedig view <ID_ou_slug>")
            sys.exit(1)
        handle_view(sys.argv[2])
        
    elif cmd == "delete":
        if len(sys.argv) < 3:
            console.print("[bold red]Erreur :[/bold red] Cible manquante (ID ou nom de fichier) pour la commande 'delete'.\n")
            console.print("Usage : cratedig delete <ID_ou_slug>")
            sys.exit(1)
        handle_delete(sys.argv[2])
        
    elif cmd == "path":
        handle_path()
        
    elif cmd == "version":
        show_version()
        
    elif cmd in ("help", "-h", "--help"):
        show_help()
        
    else:
        console.print(f"[bold red]Commande inconnue :[/bold red] '{cmd}'\n")
        show_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
