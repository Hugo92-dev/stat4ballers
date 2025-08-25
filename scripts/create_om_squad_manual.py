#!/usr/bin/env python3
"""
Script pour créer manuellement l'effectif de l'OM avec les joueurs connus
et récupérer leurs données complètes via l'API
"""

import requests
import json
import time
from datetime import datetime, date

API_TOKEN = "leBzDfKbRE5k9zEg3FuZE3Hh7XbukODNarOXLoVtPAiAtliDZ19wLu1Wnzi2"
BASE_URL = "https://api.sportmonks.com/v3/football"

OM_TEAM_ID = 44
SEASON_2025_26_ID = 25651
LIGUE1_ID = 301

def make_api_call(endpoint, params=None):
    if params is None:
        params = {}
    
    params['api_token'] = API_TOKEN
    
    try:
        response = requests.get(f"{BASE_URL}/{endpoint}", params=params, timeout=30)
        
        if response.status_code == 429:
            print("Rate limit, waiting 60s...")
            time.sleep(60)
            return make_api_call(endpoint, params)
        
        if response.status_code == 200:
            return response.json()
        else:
            return None
        
    except Exception as e:
        return None

def calculate_age(birth_date_str):
    if not birth_date_str:
        return None
    
    try:
        birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d').date()
        today = date.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        return age
    except:
        return None

def get_player_complete_data(player_id):
    """Récupère les données complètes d'un joueur"""
    print(f"Getting player {player_id}...")
    
    player_data = make_api_call(f"players/{player_id}", {
        'include': 'nationality;position;detailedPosition;country;city'
    })
    
    if player_data and 'data' in player_data:
        return player_data['data']
    return None

def process_player_data(player_data):
    """Traite les données selon les spécifications"""
    
    # Informations de base
    player_id = player_data.get('id')
    display_name = player_data.get('display_name') or player_data.get('name', 'Unknown')
    common_name = player_data.get('common_name', display_name)
    firstname = player_data.get('firstname', '')
    lastname = player_data.get('lastname', '')
    
    # Photo
    image_path = player_data.get('image_path')
    
    # Age et mensurations
    birth_date = player_data.get('date_of_birth')
    age = calculate_age(birth_date) if birth_date else None
    height = player_data.get('height')
    weight = player_data.get('weight')
    
    # Nationalite sportive (pas le pays de naissance)
    nationality_data = player_data.get('nationality', {})
    nationality_name = nationality_data.get('name') if nationality_data else None
    
    # Position
    position_data = player_data.get('position', {})
    position_name = position_data.get('name') if position_data else 'Unknown'
    
    # Position detaillee
    detailed_position_data = player_data.get('detailedPosition', {})
    detailed_position = detailed_position_data.get('name') if detailed_position_data else None
    
    # Numero de maillot (on va utiliser des numeros plausibles pour l'OM)
    jersey_number = None
    
    processed = {
        'id': player_id,
        'display_name': display_name,
        'common_name': common_name,
        'name': display_name,
        'firstname': firstname,
        'lastname': lastname,
        'image_path': image_path,
        'age': age,
        'birth_date': birth_date,
        'height': height,
        'weight': weight,
        'nationality': nationality_name,
        'position': position_name,
        'detailed_position': detailed_position,
        'jersey_number': jersey_number,
        'slug': display_name.lower().replace(' ', '-').replace('.', '').replace("'", '') if display_name else None
    }
    
    return processed

def main():
    print("=== Creating OM squad manually ===\n")
    
    # Joueurs connus de l'OM (IDs Sportmonks)
    # Commençons avec Kondogbia qu'on sait être dans l'équipe
    known_om_players = [
        95696,  # Geoffrey Kondogbia
        # Ajoutons d'autres IDs si on les trouve dans les données existantes
    ]
    
    # Cherchons dans nos données existantes d'autres joueurs de l'OM
    print("Checking existing data for more OM players...")
    try:
        # Lire les données existantes si elles existent
        with open('om_players_complete_data.json', 'r', encoding='utf-8') as f:
            existing_data = json.load(f)
            if 'players' in existing_data:
                for player in existing_data['players']:
                    player_id = player.get('id')
                    if player_id and player_id not in known_om_players:
                        known_om_players.append(player_id)
                        print(f"Added from existing data: {player.get('display_name')} (ID: {player_id})")
    except:
        print("No existing data found, using only known players")
    
    complete_players_data = []
    
    # Traiter chaque joueur connu
    for i, player_id in enumerate(known_om_players):
        print(f"\n--- Player {i+1}/{len(known_om_players)} (ID: {player_id}) ---")
        
        player_data = get_player_complete_data(player_id)
        
        if player_data:
            processed = process_player_data(player_data)
            complete_players_data.append(processed)
            print(f"Success: {processed['display_name']} - {processed['position']} - {processed['nationality']} - {processed['age']} ans")
        else:
            print(f"Failed to get data for player {player_id}")
        
        time.sleep(1)  # Eviter le rate limiting
    
    # Sauvegarder les donnees
    output_data = {
        'team_id': OM_TEAM_ID,
        'team_name': 'Olympique Marseille',
        'season_id': SEASON_2025_26_ID,
        'season_name': '2025/2026',
        'league_id': LIGUE1_ID,
        'league_name': 'Ligue 1',
        'fetched_at': datetime.now().isoformat(),
        'players_count': len(complete_players_data),
        'players': complete_players_data
    }
    
    output_file = 'om_complete_squad_2025_26.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False, default=str)
    
    print(f"\n=== Summary ===")
    print(f"Team: {output_data['team_name']}")
    print(f"Players processed: {len(complete_players_data)}")
    print(f"Data saved to: {output_file}")
    
    # Affichage détaillé de chaque joueur
    if complete_players_data:
        print(f"\n=== Complete player list ===")
        for player in complete_players_data:
            print(f"\nPlayer: {player['display_name']}")
            print(f"  Position: {player['position']} ({player['detailed_position']})")
            print(f"  Nationality: {player['nationality']}")
            print(f"  Age: {player['age']} ans")
            print(f"  Height: {player['height']} cm")
            print(f"  Photo: {player['image_path']}")
            print(f"  Jersey: #{player['jersey_number'] or 'N/A'}")
    
    return output_data

if __name__ == "__main__":
    result = main()
    
    # Afficher un exemple de données pour verification
    if result and result['players']:
        print(f"\n=== Example data structure ===")
        sample_player = result['players'][0]
        for key, value in sample_player.items():
            print(f"{key}: {value}")
