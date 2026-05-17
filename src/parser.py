import re
from typing import List, Tuple

# Liste de mots-clés typiques de spam/autopromotion à exclure des tracklists
SPAM_KEYWORDS = [
    r'http[s]?://',
    r'www\.',
    r'\.com\b',
    r'\.net\b',
    r'@\w+',
    r'subscribe',
    r'follow me',
    r'instagram',
    r'facebook',
    r'twitter',
    r'soundcloud',
    r'spotify',
    r'patreon',
    r'merch',
    r'paypal',
    r'support the channel',
    r'donations',
    r'booking',
    r'email',
    r't-shirt',
    r'buy my',
    r'tracklist created by',
]

def is_spam_line(line: str) -> bool:
    """
    Détermine si une ligne contient des éléments d'autopromotion ou de spam.
    """
    line_lower = line.lower()
    for pattern in SPAM_KEYWORDS:
        if re.search(pattern, line_lower):
            return True
    return False

def clean_track_line(line: str) -> str:
    """
    Nettoie légèrement la ligne de tracklist en supprimant les espaces superflus et
    en harmonisant les tirets.
    """
    # Remplacement des tirets spéciaux (en-dash, em-dash) par un tiret standard
    line = re.sub(r'[\u2013\u2014\u2015]', '-', line)
    # Suppression des espaces blancs en début/fin de ligne
    return line.strip()

def parse_tracklist(description: str) -> Tuple[List[str], bool]:
    """
    Analyse la description brute et extrait la tracklist.
    Retourne un tuple : (liste_des_pistes_nettoyées, tracklist_detectee_bool).
    Si aucune tracklist n'est détectée avec certitude, renvoie la description brute
    nettoyée des lignes vides pour édition manuelle.
    """
    lines = description.split('\n')
    extracted_tracks = []
    
    # Regex pour détecter les timestamps : 01:23, 1:23:45, [01:23], (1:23)
    timestamp_pattern = re.compile(r'(?:[\[\(]?\b\d{1,2}:\d{2}(?::\d{2})?\b[\]\)]?)')
    
    # Regex pour détecter une numérotation séquentielle de début de ligne : "01.", "1 -", "02)"
    numbering_pattern = re.compile(r'^\s*[\[\(]?\d{1,3}(?:[\.\-\)\s]+|\b)\s*')
    
    # Étape 1 : Analyse ligne par ligne
    for line in lines:
        cleaned = clean_track_line(line)
        if not cleaned:
            continue
            
        # On ignore le spam évident de toute façon
        if is_spam_line(cleaned):
            continue
            
        # Si la ligne contient un timestamp ou une numérotation et semble être une piste
        has_timestamp = bool(timestamp_pattern.search(cleaned))
        has_numbering = bool(numbering_pattern.match(cleaned))
        
        # Une ligne contenant un tiret entouré d'espaces est souvent une piste (Artiste - Titre)
        has_hyphen = '-' in cleaned
        
        if (has_timestamp or has_numbering) and len(cleaned) > 5:
            extracted_tracks.append(cleaned)
        elif has_hyphen and len(cleaned) > 10 and not has_timestamp:
            # Fallback heuristique si c'est une ligne de type "Artist - Track" sans timestamp
            # On vérifie qu'elle ne ressemble pas à un titre de section
            if not cleaned.lower().startswith(('tracklist', 'track list', 'playlist', 'mix by')):
                extracted_tracks.append(cleaned)
                
    # Étape 2 : Si on a trouvé au moins 3 pistes, on considère qu'on a une tracklist valide
    if len(extracted_tracks) >= 3:
        return extracted_tracks, True
        
    # Étape 3 : Si aucune tracklist structurée n'est identifiée, on renvoie les lignes non-vides
    # et non-spam pour édition manuelle par l'utilisateur.
    fallback_lines = []
    for line in lines:
        cleaned = clean_track_line(line)
        if cleaned and not is_spam_line(cleaned):
            fallback_lines.append(cleaned)
            
    return fallback_lines, False
