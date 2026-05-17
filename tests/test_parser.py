import sys
import os

# Ajout du dossier courant au path pour les imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src import parser

def test_parse_with_timestamps():
    description = """
    Infocus Deep House Mix 2026.
    Check out the tracks below:
    
    00:00 Artist One - First Song
    04:15 Artist Two - Second Song (Original Mix)
    [08:30] Artist Three - Third Song
    (12:45) Artist Four - Fourth Song
    
    Subscribe for more!
    http://youtube.com/mychannel
    """
    
    tracks, detected = parser.parse_tracklist(description)
    
    assert detected is True
    assert len(tracks) == 4
    assert "00:00 Artist One - First Song" in tracks
    assert "04:15 Artist Two - Second Song (Original Mix)" in tracks
    assert "[08:30] Artist Three - Third Song" in tracks
    assert "(12:45) Artist Four - Fourth Song" in tracks
    print("✓ Test avec timestamps réussi !")

def test_parse_with_numbering():
    description = """
    Deep House Selection.
    
    1. Artist A - Track A
    2. Artist B - Track B
    3. Artist C - Track C
    
    Join our Patreon: patreon.com/infocus
    """
    
    tracks, detected = parser.parse_tracklist(description)
    
    assert detected is True
    assert len(tracks) == 3
    assert "1. Artist A - Track A" in tracks
    print("✓ Test avec numérotation réussi !")

def test_parse_fallback_no_tracklist():
    description = """
    Simple vlog video without tracklist.
    Just talking about DJing today.
    No tracklist.
    """
    
    tracks, detected = parser.parse_tracklist(description)
    
    assert detected is False
    assert len(tracks) > 0  # Devrait renvoyer les lignes descriptives brutes pour édition manuelle
    print("✓ Test fallback sans tracklist réussi !")

if __name__ == "__main__":
    print("Lancement des tests du parser...")
    test_parse_with_timestamps()
    test_parse_with_numbering()
    test_parse_fallback_no_tracklist()
    print("Tous les tests du parser ont réussi !")
