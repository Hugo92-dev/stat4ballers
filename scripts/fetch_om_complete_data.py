#!/usr/bin/env python3
"""
Script pour récupérer les données complètes de l'effectif de l'OM depuis l'API Sportmonks
Utilise les bons IDs et endpoints selon les spécifications fournies
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

# ID de l'OM dans Sportmonks (à déterminer)
OM_TEAM_ID = None

def make_api_call(endpoint: str, params: Dict[str, Any] = None) -> Optional[Dict]:
    """Effectue un appel API avec gestion d'erreurs et retry"""
    if params is None:
        params = {}
    
    params['api_token'] = API_TOKEN
    
    try:
        print(f"Calling API: {endpoint}")
        response = requests.get(f"{BASE_URL}/{endpoint}", params=params, timeout=30)
        
        if response.status_code == 429:
            print("Rate limit hit, waiting 60 seconds...")
            time.sleep(60)
            return make_api_call(endpoint, params)
        
        response.raise_for_status()
        data = response.json()
        
        print(f"✓ Success: {endpoint}")
        return data
        
    except requests.exceptions.RequestException as e:
        print(f"✗ Error calling {endpoint}: {e}")
        return None

def find_om_team_id() -> Optional[int]:
    """Trouve l'ID de l'OM dans la saison actuelle"""
    print("Recherche de l'ID de l'OM...")
    
    # Récupérer toutes les équipes de la saison Ligue 1 2025/26
    data = make_api_call(f"seasons/{SEASON_2025_26_ID}/teams")
    
    if not data or 'data' not in data:
        print("Erreur lors de la récupération des équipes")
        return None
    
    teams = data['data']
    for team in teams:
        team_name = team.get('name', '').lower()
        if 'marseille' in team_name or 'olympique marseille' in team_name:
            om_id = team.get('id')
            print(f"✓ OM trouvé: ID={om_id}, Nom={team.get('name')}")
            return om_id
    
    print("✗ OM non trouvé dans la Ligue 1 2025/26")
    return None

def get_team_squad(team_id: int, season_id: int) -> Optional[List[Dict]]:
    """Récupère l'effectif complet d'une équipe pour une saison"""
    print(f"Récupération de l'effectif de l'équipe {team_id} pour la saison {season_id}...")
    
    data = make_api_call(f"teams/{team_id}/squads/seasons/{season_id}")
    
    if not data or 'data' not in data:
        print("Erreur lors de la récupération de l'effectif")
        return None
    
    players = data['data']
    print(f"✓ {len(players)} joueurs trouvés dans l'effectif")
    return players

def get_player_complete_data(player_id: int) -> Optional[Dict]:
    """Récupère toutes les données d'un joueur avec les inclusions nécessaires"""
    print(f"Récupération des données complètes du joueur {player_id}...")
    
    includes = [
        'country', 'nationality', 'city', 'position', 'detailedPosition', 
        'teams', 'statistics', 'transfers', 'pendingTransfers', 
        'lineups', 'sport', 'trophies', 'latest'
    ]
    
    params = {
        'include': ';'.join(includes)
    }
    
    data = make_api_call(f"players/{player_id}", params)
    
    if not data or 'data' not in data:
        print(f"✗ Erreur lors de la récupération du joueur {player_id}")
        return None
    
    player_data = data['data']
    print(f"✓ Données complètes récupérées pour {player_data.get('display_name', 'Unknown')}")
    return player_data

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

def process_player_data(player_data: Dict) -> Dict:
    """Traite les données d'un joueur pour extraire toutes les informations requises"""
    
    # Informations de base
    player_id = player_data.get('id')
    display_name = player_data.get('display_name') or player_data.get('name', 'Unknown')
    common_name = player_data.get('common_name', display_name)
    firstname = player_data.get('firstname', '')
    lastname = player_data.get('lastname', '')
    full_name = player_data.get('name', f"{firstname} {lastname}".strip())
    
    # Photo
    image_path = player_data.get('image_path')
    
    # Âge et mensurations
    birth_date = player_data.get('date_of_birth')
    age = calculate_age(birth_date) if birth_date else None
    height = player_data.get('height')  # en cm
    weight = player_data.get('weight')  # en kg
    
    # Nationalité sportive
    nationality_data = player_data.get('nationality', {})
    nationality = nationality_data.get('name') if nationality_data else None
    nationality_id = nationality_data.get('id') if nationality_data else None
    
    # Pays de naissance
    country_data = player_data.get('country', {})
    country = country_data.get('name') if country_data else None
    
    # Position
    position_data = player_data.get('position', {})
    position_name = position_data.get('name') if position_data else None
    position_id = player_data.get('position_id')
    
    # Position détaillée
    detailed_position_data = player_data.get('detailedPosition', {})
    detailed_position = detailed_position_data.get('name') if detailed_position_data else None
    detailed_position_id = player_data.get('detailed_position_id')
    
    # Numéro de maillot (depuis les équipes actuelles)
    jersey_number = None
    teams = player_data.get('teams', [])
    if teams:
        # Chercher l'équipe actuelle (normalement la première)
        current_team = teams[0] if teams else None
        if current_team and 'pivot' in current_team:
            jersey_number = current_team['pivot'].get('jersey_number')
    
    # Ville de naissance
    city_data = player_data.get('city', {})
    birth_city = city_data.get('name') if city_data else None
    
    # Statistiques (pour référence)
    statistics = player_data.get('statistics', [])
    
    processed_data = {
        'id': player_id,
        'display_name': display_name,
        'common_name': common_name,
        'name': full_name,
        'firstname': firstname,
        'lastname': lastname,
        'image_path': image_path,
        'age': age,
        'birth_date': birth_date,
        'height': height,  # cm
        'weight': weight,  # kg
        'nationality': nationality,
        'nationality_id': nationality_id,
        'country': country,
        'birth_city': birth_city,
        'position': position_name,
        'position_id': position_id,
        'detailed_position': detailed_position,
        'detailed_position_id': detailed_position_id,
        'jersey_number': jersey_number,
        'statistics_count': len(statistics) if statistics else 0,
        'raw_data': player_data  # Garder toutes les données brutes pour référence
    }
    
    return processed_data

def main():
    """Fonction principale"""
    print("=== Récupération des données complètes de l'OM ===\n")
    
    # 1. Trouver l'ID de l'OM
    global OM_TEAM_ID
    OM_TEAM_ID = find_om_team_id()
    
    if not OM_TEAM_ID:
        print("Impossible de trouver l'ID de l'OM. Arrêt du script.")
        sys.exit(1)
    
    # 2. Récupérer l'effectif actuel (saison 2025/26)
    squad = get_team_squad(OM_TEAM_ID, SEASON_2025_26_ID)
    
    if not squad:
        print("Impossible de récupérer l'effectif de l'OM. Arrêt du script.")
        sys.exit(1)
    
    # 3. Traiter chaque joueur
    complete_players_data = []
    
    for i, squad_player in enumerate(squad):
        player_id = squad_player.get('player_id')
        if not player_id:
            print(f"Joueur {i+1}: ID manquant, ignoré")
            continue
        
        print(f"\n--- Joueur {i+1}/{len(squad)} (ID: {player_id}) ---")
        
        # Récupérer les données complètes
        player_data = get_player_complete_data(player_id)
        
        if player_data:
            processed = process_player_data(player_data)
            complete_players_data.append(processed)
            print(f"✓ {processed['display_name']} - {processed['position']} - {processed['nationality']}")
        else:
            print(f"✗ Erreur pour le joueur {player_id}")
        
        # Pause pour éviter le rate limiting
        time.sleep(1)
    
    # 4. Sauvegarder les données
    output_data = {
        'team_id': OM_TEAM_ID,
        'team_name': 'Olympique Marseille',
        'season_id': SEASON_2025_26_ID,
        'season_name': '2025/2026',
        'fetched_at': datetime.now().isoformat(),
        'players_count': len(complete_players_data),
        'players': complete_players_data
    }
    
    # Sauvegarde dans le répertoire racine
    output_file = '../om_complete_squad_2025_26.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False, default=str)
    
    print(f"\n=== Résumé ===")
    print(f"Équipe: {output_data['team_name']} (ID: {OM_TEAM_ID})")
    print(f"Saison: {output_data['season_name']} (ID: {SEASON_2025_26_ID})")
    print(f"Joueurs traités: {len(complete_players_data)}")
    print(f"Données sauvegardées dans: {output_file}")
    
    # Affichage d'un échantillon
    if complete_players_data:
        print(f"\n=== Échantillon (Premier joueur) ===")
        sample = complete_players_data[0]
        for key, value in sample.items():
            if key != 'raw_data':
                print(f"{key}: {value}")

if __name__ == "__main__":
    main()