import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src import extractor
from src import parser
from src import storage

def main():
    # URL d'une vidéo YouTube avec une tracklist claire (ici, un mix de Deep House de la chaîne 'Infocus' ou similaire)
    # Pour le test, on utilise une URL de DJ set stable
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Rick Astley - Never Gonna Give You Up (universally available)
    
    print(f"Tentative d'extraction pour l'URL : {url}")
    try:
        metadata = extractor.extract_metadata(url)
        print("✓ Métadonnées extraites avec succès !")
        print(f"Titre : {metadata['title']}")
        print(f"Date de publication : {metadata['upload_date']}")
        print(f"Longueur de la description : {len(metadata['description'])} caractères")
        
        tracks, detected = parser.parse_tracklist(metadata['description'])
        print(f"✓ Parsing de la tracklist terminé. Détectée ? {detected}")
        print(f"Nombre de morceaux trouvés : {len(tracks)}")
        
        if len(tracks) > 0:
            print("Premiers morceaux :")
            for t in tracks[:5]:
                print(f"  - {t}")
                
        filepath = storage.save_tracklist(metadata, tracks, detected)
        print(f"✓ Sauvegardé dans : {filepath}")
        
        assert os.path.exists(filepath)
        print("✓ Validation du fichier sauvegardé réussie !")
        
    except Exception as e:
        print(f"✗ Échec du test d'intégration : {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
