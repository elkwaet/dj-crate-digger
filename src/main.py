import sys
import os
import questionary
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table

# Ajout du dossier courant au path pour les imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import extractor
import parser
import storage

# Console Rich globale avec thème sobre (Noir & Blanc, gris)
console = Console()

def show_welcome_banner() -> None:
    """
    Affiche une bannière d'accueil minimaliste et premium.
    """
    banner_text = Text()
    banner_text.append("■ DJ CRATE DIGGER ■\n", style="bold white")
    banner_text.append("Outil d'extraction de tracklists YouTube pour DJs", style="italic grey50")
    
    console.print(Panel(
        banner_text,
        border_style="grey50",
        expand=False,
        padding=(1, 3)
    ))
    console.print()

def format_tracklist_table(tracks: list[str]) -> Table:
    """
    Formate la tracklist sous forme de tableau sobre.
    """
    table = Table(show_header=True, header_style="bold white", border_style="grey37")
    table.add_column("Piste / Info", style="white")
    
    for idx, track in enumerate(tracks, 1):
        table.add_row(track)
        
    return table

def handle_new_extraction() -> None:
    """
    Gère la saisie d'un nouveau lien et lance l'extraction de la tracklist.
    """
    url = questionary.text(
        "Saisis l'URL de la vidéo YouTube :",
        validate=lambda text: True if text.strip().startswith(('http://', 'https://', 'www.')) else "Veuillez entrer une URL valide."
    ).ask()
    
    if not url:
        return
        
    try:
        # Affichage d'un loader élégant
        with console.status("[white]Extraction des données YouTube...[/white] (via yt-dlp)"):
            metadata = extractor.extract_metadata(url)
            tracks, detected = parser.parse_tracklist(metadata['description'])
            filepath = storage.save_tracklist(metadata, tracks, detected)
            
        # Rendu du succès
        console.print()
        status_text = "TRACKLIST DÉTECTÉE & EXTRAITE" if detected else "EXTRACTION BRUTE SAUVEGARDÉE"
        status_color = "bold white"
        
        console.print(Panel(
            Text(f"✔ {status_text}\n\nFichier : {os.path.basename(filepath)}\nTracks : {len(tracks)}", style=status_color),
            border_style="white",
            expand=False,
            padding=(1, 2)
        ))
        console.print()
        
        # Affichage d'un aperçu
        console.print("[bold white]Aperçu de la tracklist :[/bold white]")
        console.print(format_tracklist_table(tracks[:15]))
        if len(tracks) > 15:
            console.print(f"[grey50]... et {len(tracks) - 15} autres lignes (consultables dans le fichier).[/grey50]")
        console.print()
        
        questionary.press_any_key_to_continue("Appuie sur une touche pour revenir au menu principal...").ask()
        
    except Exception as e:
        console.print(f"\n[bold red]Erreur lors de l'extraction :[/bold red] {str(e)}\n")
        questionary.press_any_key_to_continue("Appuie sur une touche pour continuer...").ask()

def handle_browse_crate() -> None:
    """
    Permet de parcourir les tracklists existantes.
    """
    files = storage.list_extracted_files()
    if not files:
        console.print("\n[grey50]Aucune tracklist extraite dans ton crate pour le moment.[/grey50]\n")
        questionary.press_any_key_to_continue("Appuie sur une touche pour continuer...").ask()
        return
        
    choices = [f['name'] for f in files]
    choices.append("← Retour")
    
    selected_file_name = questionary.select(
        "Choisis une tracklist à consulter :",
        choices=choices
    ).ask()
    
    if selected_file_name == "← Retour" or not selected_file_name:
        return
        
    selected_file = next(f for f in files if f['name'] == selected_file_name)
    content = storage.read_file_content(selected_file['path'])
    
    console.print()
    console.print(Panel(
        content,
        title=selected_file_name,
        title_align="left",
        border_style="white"
    ))
    console.print()
    
    # Actions sur le fichier
    action = questionary.select(
        "Action :",
        choices=["← Revenir à la liste", "❌ Supprimer cette tracklist"]
    ).ask()
    
    if action == "❌ Supprimer cette tracklist":
        confirm = questionary.confirm("Es-tu sûr de vouloir supprimer cette tracklist ?").ask()
        if confirm:
            os.remove(selected_file['path'])
            console.print("[white]Fichier supprimé.[/white]")
            
    # Relance le parcours récursivement s'il n'a pas quitté
    if action != "← Revenir à la liste":
        handle_browse_crate()

def main() -> None:
    """
    Boucle principale de l'application TUI.
    """
    while True:
        console.clear()
        show_welcome_banner()
        
        choice = questionary.select(
            "Que veux-tu faire ?",
            choices=[
                "🔍 Analyser une nouvelle vidéo YouTube",
                "📂 Parcourir les tracklists locales (Crate)",
                "🚪 Quitter"
            ]
        ).ask()
        
        if choice == "🔍 Analyser une nouvelle vidéo YouTube":
            handle_new_extraction()
        elif choice == "📂 Parcourir les tracklists locales (Crate)":
            handle_browse_crate()
        elif choice == "🚪 Quitter" or not choice:
            console.clear()
            console.print("[white]Bon set ! À bientôt.[/white] ⚡")
            break

if __name__ == "__main__":
    main()
