#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de test rapide pour rafraîchir uniquement l'Olympique Lyonnais
"""

import requests
import json
import sys
import os
from datetime import datetime

# Fix pour l'encodage UTF-8 sur Windows
sys.stdout.reconfigure(encoding='utf-8')

API_KEY = "leBzDfKbRE5k9zEg3FuZE3Hh7XbukODNarOXLoVtPAiAtliDZ19wLu1Wnzi2"
BASE_URL = "https://api.sportmonks.com/v3/football"

headers = {
    "Accept": "application/json",
    "Authorization": API_KEY,
}

# Charger le mapping des types SportMonks
with open('sportmonks_types_mapping.json', 'r', encoding='utf-8') as f:
    TYPES_MAPPING = json.load(f)

def get_position_name(type_id):
    """Obtient le nom de la position à partir de l'ID SportMonks"""
    if type_id:
        for category, positions in TYPES_MAPPING.items():
            if str(type_id) in positions:
                return positions[str(type_id)]
    return "Joueur"

def fetch_lyon_data():
    """Récupère les données de l'Olympique Lyonnais"""
    
    print("🔄 Récupération des données de l'Olympique Lyonnais...")
    
    # ID de Lyon
    lyon_id = 79
    season_id = 25651  # Saison 2025/2026
    
    # 1. Récupérer les infos du club
    print("📊 Récupération des informations du club...")
    club_url = f"{BASE_URL}/teams/{lyon_id}"
    params = {
        "api_token": API_KEY,
        "include": "venue"
    }
    
    response = requests.get(club_url, headers=headers, params=params)
    if response.status_code != 200:
        print(f"❌ Erreur lors de la récupération du club: {response.status_code}")
        return False
    
    club_data = response.json()['data']
    print(f"✅ Club récupéré: {club_data['name']}")
    
    # 2. Récupérer l'effectif
    print("\n📊 Récupération de l'effectif...")
    squad_url = f"{BASE_URL}/squads/teams/{lyon_id}"
    params = {
        "api_token": API_KEY,
        "include": "player"
    }
    
    response = requests.get(squad_url, headers=headers, params=params)
    if response.status_code != 200:
        print(f"❌ Erreur lors de la récupération de l'effectif: {response.status_code}")
        return False
    
    squad_data = response.json()['data']
    print(f"✅ {len(squad_data)} joueurs trouvés")
    
    # 3. Traiter les données des joueurs
    players = []
    for item in squad_data:
        if not item.get('player'):
            continue
            
        player = item['player']
        
        # Position
        position = get_position_name(player.get('position_id'))
        
        # Statistiques simplifiées pour le test
        stats = {"goals": 0, "assists": 0, "yellow_cards": 0, "red_cards": 0, "minutes_played": 0}
        
        player_data = {
            "id": player['id'],
            "name": player['name'],
            "display_name": player.get('display_name', player['name']),
            "position": position,
            "jersey_number": item.get('jersey_number'),
            "age": datetime.now().year - int(player['date_of_birth'][:4]) if player.get('date_of_birth') else None,
            "date_of_birth": player.get('date_of_birth'),
            "nationality": player.get('nationality', {}).get('name') if player.get('nationality') else None,
            "height": player.get('height'),
            "weight": player.get('weight'),
            "image_path": player.get('image_path'),
            "statistics": stats,
            "market_value": None
        }
        
        players.append(player_data)
        print(f"  • {player_data['display_name']} ({position}) - {stats['goals']} buts")
    
    # 4. Sauvegarder les données
    output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "ligue1_2025_2026")
    os.makedirs(output_dir, exist_ok=True)
    
    output_file = os.path.join(output_dir, "lyon.json")
    
    # Structure finale
    final_data = {
        "id": lyon_id,
        "name": club_data['name'],
        "short_name": club_data.get('short_code', 'OL'),
        "founded": club_data.get('founded'),
        "logo_path": club_data.get('image_path'),
        "venue": {
            "name": club_data.get('venue', {}).get('name') if club_data.get('venue') else None,
            "capacity": club_data.get('venue', {}).get('capacity') if club_data.get('venue') else None,
            "city": club_data.get('venue', {}).get('city', {}).get('name') if club_data.get('venue') and club_data['venue'].get('city') else None,
        } if club_data.get('venue') else None,
        "players": players,
        "last_updated": datetime.now().isoformat()
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(final_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Données sauvegardées dans: {output_file}")
    print(f"📊 Total: {len(players)} joueurs")
    
    # Afficher un résumé
    goalscorers = sorted([p for p in players if p['statistics']['goals'] > 0], 
                        key=lambda x: x['statistics']['goals'], reverse=True)[:3]
    
    if goalscorers:
        print("\n🥇 Top buteurs:")
        for p in goalscorers:
            print(f"  • {p['display_name']}: {p['statistics']['goals']} buts")
    
    return True

if __name__ == "__main__":
    try:
        success = fetch_lyon_data()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        sys.exit(1)