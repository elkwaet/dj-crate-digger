import yt_dlp
from typing import Dict, Any

def extract_metadata(url: str) -> Dict[str, Any]:
    """
    Extrait les métadonnées d'une vidéo YouTube (Titre, Description, Date de publication, URL).
    Utilise yt-dlp sous le capot pour une fiabilité maximale.
    """
    ydl_opts = {
        'skip_download': True,
        'quiet': True,
        'no_warnings': True,
        'extract_flat': False,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        # extract_info effectue la requête réseau et extrait le dictionnaire de métadonnées
        info = ydl.extract_info(url, download=False)
        
        # Formatage propre de la date (de YYYYMMDD à YYYY-MM-DD)
        raw_date = info.get('upload_date', '')
        formatted_date = raw_date
        if len(raw_date) == 8:
            formatted_date = f"{raw_date[:4]}-{raw_date[4:6]}-{raw_date[6:]}"
            
        return {
            'title': info.get('title', 'Titre inconnu'),
            'description': info.get('description', ''),
            'upload_date': formatted_date,
            'webpage_url': info.get('webpage_url', url)
        }
