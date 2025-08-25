#!/usr/bin/env python3
"""
Script pour corriger les URLs des images des joueurs
"""

import requests
import json

API_TOKEN = "leBzDfKbRE5k9zEg3FuZE3Hh7XbukODNarOXLoVtPAiAtliDZ19wLu1Wnzi2"
BASE_URL = "https://api.sportmonks.com/v3/football"

# Joueurs avec images problématiques
problem_players = {
    95696: "Geoffrey Kondogbia",
    95694: "Adrien Rabiot",
    130063: "Pol Lirola", 
    37541144: "Bilal Nadir",
    433458: "Amine Gouiri"
}

def get_player_image(player_id):
    """Récupère l'URL correcte de l'image d'un joueur"""
    try:
        response = requests.get(
            f"{BASE_URL}/players/{player_id}",
            params={'api_token': API_TOKEN},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            if 'data' in data:
                image_path = data['data'].get('image_path')
                return image_path
        return None
    except:
        return None

def main():
    print("=== Correction des images des joueurs ===\n")
    
    corrections = {}
    
    for player_id, name in problem_players.items():
        print(f"Récupération image pour {name} (ID: {player_id})...")
        image_url = get_player_image(player_id)
        
        if image_url:
            print(f"  [OK] Trouvé: {image_url}")
            corrections[player_id] = image_url
        else:
            print(f"  [FAIL] Non trouvé - utiliser placeholder")
            corrections[player_id] = "https://cdn.sportmonks.com/images/soccer/placeholder.png"
    
    print("\n=== Corrections à appliquer ===")
    for player_id, url in corrections.items():
        print(f"{problem_players[player_id]}: {url}")
    
    # Sauvegarder les corrections
    with open('image_corrections.json', 'w') as f:
        json.dump(corrections, f, indent=2)
    
    print("\nCorrections sauvegardées dans image_corrections.json")

if __name__ == "__main__":
    main()