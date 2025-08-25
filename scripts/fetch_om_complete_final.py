#!/usr/bin/env python3
"""
Script pour récupérer les données complètes de l'effectif de l'OM
Utilise l'ID correct de l'OM (44) et les IDs de saisons fournis
"""

import requests
import json
import time
import sys
from datetime import datetime, date
from typing import Dict, List, Any, Optional

# Configuration API
API_TOKEN = "leBzDfKbRE5k9zEg3FuZE3Hh7XbukODNarOXLoVtPAiAtliDZ19wLu1Wnzi2"
BASE_URL = "https://api.sportmonks.com/v3/football"

# IDs fournis
LIGUE1_ID = 301
SEASON_2025_26_ID = 25651
SEASON_2024_25_ID = 23643
SEASON_2023_24_ID = 21779

# ID de l'OM
OM_TEAM_ID = 44

def make_api_call(endpoint: str, params: Dict[str, Any] = None) -> Optional[Dict]:
    """Effectue un appel API avec gestion d'erreurs"""
    if params is None:
        params = {}
    
    params['api_token'] = API_TOKEN
    
    try:
        print(f"Calling: {endpoint}")
        response = requests.get(f"{BASE_URL}/{endpoint}", params=params, timeout=30)
        
        if response.status_code == 429:
            print("Rate limit, waiting 60s...")
            time.sleep(60)
            return make_api_call(endpoint, params)
        
        if response.status_code == 200:
            data = response.json()
            print(f"Success: {endpoint}")
            return data
        else:
            print(f"Error {response.status_code}: {response.text[:200]}")
            return None
        
    except Exception as e:
        print(f"Exception: {e}")
        return None

def get_om_squad() -> Optional[List[Dict]]:
    """Récupère l'effectif de l'OM pour la saison actuelle"""
    print(f"Getting OM squad (team ID: {OM_TEAM_ID})...")
    
    # Tester différents endpoints
    endpoints_to_try = [
        f"teams/{OM_TEAM_ID}/players",
        f"teams/{OM_TEAM_ID}/squads",
        f"teams/{OM_TEAM_ID}"
    ]
    
    for endpoint in endpoints_to_try:
        print(f"\nTrying: {endpoint}")
        result = make_api_call(endpoint)
        
        if result and 'data' in result:
            data = result['data']
            
            if isinstance(data, list) and len(data) > 0:
                print(f"Found {len(data)} players")
                return data
            elif isinstance(data, dict):
                # Peut-être que les joueurs sont dans une sous-propriété
                if 'players' in data:
                    players = data['players']
                    print(f"Found {len(players)} players in 'players' key")
                    return players
                elif 'squad' in data:
                    squad = data['squad']
                    print(f"Found {len(squad)} players in 'squad' key")
                    return squad
    
    print("No squad data found")
    return None

def calculate_age(birth_date_str: str) -> Optional[int]:
    """Calcule l'âge à partir de la date de naissance"""
    if not birth_date_str:
        return None
    
    try:
        birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d').date()
        today = date.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        return age
    except (ValueError, TypeError):
        return None

def get_player_complete_data(player_id: int) -> Optional[Dict]:
    """Récupère toutes les données d'un joueur"""
    print(f"Getting player {player_id} details...")
    
    includes = [
        'country', 'nationality', 'city', 'position', 'detailedPosition', 
        'teams', 'statistics'
    ]
    
    params = {
        'include': ';'.join(includes)
    }
    
    data = make_api_call(f"players/{player_id}", params)
    
    if data and 'data' in data:
        return data['data']
    
    return None

def process_player_data(player_data: Dict, squad_info: Dict = None) -> Dict:
    """Traite les données d'un joueur pour extraire toutes les informations requises"""
    
    # Informations de base
    player_id = player_data.get('id')
    display_name = player_data.get('display_name') or player_data.get('name', 'Unknown')
    common_name = player_data.get('common_name', display_name)
    firstname = player_data.get('firstname', '')
    lastname = player_data.get('lastname', '')
    
    # Photo
    image_path = player_data.get('image_path')
    
    # Âge et mensurations
    birth_date = player_data.get('date_of_birth')
    age = calculate_age(birth_date) if birth_date else None
    height = player_data.get('height')  # en cm
    weight = player_data.get('weight')  # en kg
    
    # Nationalité sportive (pas le pays de naissance)
    nationality_data = player_data.get('nationality', {})
    nationality_name = nationality_data.get('name') if nationality_data else None
    nationality_id = nationality_data.get('id') if nationality_data else None
    
    # Position
    position_data = player_data.get('position', {})
    position_name = position_data.get('name') if position_data else None
    position_id = player_data.get('position_id')
    
    # Position détaillée
    detailed_position_data = player_data.get('detailedPosition', {})
    detailed_position = detailed_position_data.get('name') if detailed_position_data else None
    detailed_position_id = player_data.get('detailed_position_id')
    
    # Numéro de maillot
    jersey_number = None
    
    # D'abord essayer depuis squad_info si disponible
    if squad_info:
        jersey_number = squad_info.get('jersey_number')
    
    # Sinon essayer depuis les équipes
    if not jersey_number:
        teams = player_data.get('teams', [])
        for team in teams:
            if team.get('id') == OM_TEAM_ID and 'pivot' in team:
                jersey_number = team['pivot'].get('jersey_number')
                break
    
    # Ville de naissance
    city_data = player_data.get('city', {})
    birth_city = city_data.get('name') if city_data else None
    
    processed_data = {
        'id': player_id,
        'display_name': display_name,
        'common_name': common_name,
        'name': display_name,  # Utiliser display_name comme nom principal
        'firstname': firstname,
        'lastname': lastname,
        'image_path': image_path,
        'age': age,
        'birth_date': birth_date,
        'height': height,
        'weight': weight,
        'nationality': nationality_name,  # Nationalité sportive
        'nationality_id': nationality_id,
        'birth_city': birth_city,
        'position': position_name,
        'position_id': position_id,
        'detailed_position': detailed_position,
        'detailed_position_id': detailed_position_id,
        'jersey_number': jersey_number,
        'slug': display_name.lower().replace(' ', '-').replace('.', '').replace("'", '') if display_name else None
    }
    
    return processed_data

def main():
    """Fonction principale"""
    print("=== Récupération des données complètes de l'OM ===\n")
    print(f"Team ID: {OM_TEAM_ID}")
    print(f"Season ID: {SEASON_2025_26_ID}")
    
    # 1. Récupérer l'effectif de l'OM
    squad = get_om_squad()
    
    if not squad:
        print("Impossible de récupérer l'effectif de l'OM")
        sys.exit(1)
    
    # 2. Traiter chaque joueur
    complete_players_data = []
    
    for i, squad_player in enumerate(squad):
        # Extraire l'ID du joueur selon la structure
        player_id = None
        squad_info = {}
        
        if isinstance(squad_player, dict):
            player_id = squad_player.get('player_id') or squad_player.get('id')
            squad_info = squad_player
        elif isinstance(squad_player, (int, str)):
            player_id = int(squad_player)
        
        if not player_id:
            print(f"Player {i+1}: No ID found, skipping")
            continue
        
        print(f"\n--- Player {i+1}/{len(squad)} (ID: {player_id}) ---")
        
        # Récupérer les données complètes
        player_data = get_player_complete_data(player_id)
        
        if player_data:
            processed = process_player_data(player_data, squad_info)
            complete_players_data.append(processed)
            print(f"Success: {processed['display_name']} - {processed['position']} - {processed['nationality']}")
        else:
            print(f"Failed to get data for player {player_id}")
        
        # Pause pour éviter le rate limiting
        time.sleep(1)
    
    # 3. Sauvegarder les données
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
    
    # Sauvegarder 
    output_file = 'om_complete_squad_2025_26.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False, default=str)
    
    print(f"\n=== Summary ===")
    print(f"Team: {output_data['team_name']} (ID: {OM_TEAM_ID})")
    print(f"Season: {output_data['season_name']} (ID: {SEASON_2025_26_ID})")
    print(f"Players processed: {len(complete_players_data)}")
    print(f"Data saved to: {output_file}")
    
    # Affichage d'échantillons
    if complete_players_data:
        print(f"\n=== Sample (First 3 players) ===")
        for i, player in enumerate(complete_players_data[:3]):
            print(f"\nPlayer {i+1}:")
            print(f"  Name: {player['display_name']}")
            print(f"  Position: {player['position']}")
            print(f"  Detailed Position: {player['detailed_position']}")
            print(f"  Nationality: {player['nationality']}")
            print(f"  Age: {player['age']}")
            print(f"  Height: {player['height']} cm")
            print(f"  Jersey: #{player['jersey_number']}")
            print(f"  Photo: {player['image_path']}")

if __name__ == "__main__":
    main()