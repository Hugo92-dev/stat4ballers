#!/usr/bin/env python3
"""
Script pour récupérer l'effectif de l'OM en utilisant les statistiques de la saison
"""

import requests
import json
import time
from datetime import datetime, date
from typing import Dict, List, Any, Optional

API_TOKEN = "leBzDfKbRE5k9zEg3FuZE3Hh7XbukODNarOXLoVtPAiAtliDZ19wLu1Wnzi2"
BASE_URL = "https://api.sportmonks.com/v3/football"

LIGUE1_ID = 301
SEASON_2025_26_ID = 25651
OM_TEAM_ID = 44

def make_api_call(endpoint: str, params: dict = None):
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
            print(f"Error {response.status_code}: {response.text[:200]}")
            return None
        
    except Exception as e:
        print(f"Exception: {e}")
        return None

def calculate_age(birth_date_str: str) -> Optional[int]:
    if not birth_date_str:
        return None
    
    try:
        birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d').date()
        today = date.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        return age
    except (ValueError, TypeError):
        return None

def get_om_players_from_season_stats():
    """Récupère les joueurs de l'OM via les statistiques de la saison"""
    print(f"Getting OM players from season {SEASON_2025_26_ID} statistics...")
    
    # Essayer d'obtenir toutes les statistiques de la saison
    print("Trying to get season statistics...")
    stats_data = make_api_call(f"seasons/{SEASON_2025_26_ID}/topscorers")
    
    if stats_data and 'data' in stats_data:
        all_stats = stats_data['data']
        print(f"Found {len(all_stats)} player statistics")
        
        om_players = []
        for stat in all_stats:
            if isinstance(stat, dict):
                # Chercher les stats liées à l'OM
                participant = stat.get('participant', {})
                if participant.get('id') == OM_TEAM_ID:
                    player = stat.get('player', {})
                    if player:
                        om_players.append({
                            'player_id': player.get('id'),
                            'player_name': player.get('display_name'),
                            'stats': stat
                        })
        
        print(f"Found {len(om_players)} OM players in topscorers")
        return om_players
    
    return []

def get_known_om_players():
    """Utilise des joueurs connus de l'OM pour construire l'effectif"""
    print("Using known OM players to build squad...")
    
    # Joueurs connus de l'OM (IDs Sportmonks)
    known_players = [
        95696,  # Kondogbia
        # Ajoutons d'autres IDs si on les trouve
    ]
    
    om_squad = []
    
    for player_id in known_players:
        print(f"\nProcessing player {player_id}...")
        
        player_data = make_api_call(f"players/{player_id}", {
            'include': 'teams;statistics;nationality;position;detailedPosition'
        })
        
        if player_data and 'data' in player_data:
            player = player_data['data']
            
            # Vérifier s'il joue actuellement à l'OM
            teams = player.get('teams', [])
            is_om_player = False
            
            for team in teams:
                if team.get('id') == OM_TEAM_ID:
                    is_om_player = True
                    break
            
            if is_om_player:
                om_squad.append(player)
                print(f"  ✓ {player.get('display_name')} is OM player")
            else:
                print(f"  ✗ {player.get('display_name')} not current OM player")
    
    return om_squad

def search_players_by_team():
    """Essaie de trouver tous les joueurs ayant joué pour l'OM récemment"""
    print("Searching for all OM players...")
    
    # Approche : regarder les fixtures/matchs de l'OM pour trouver les joueurs
    print("Getting OM fixtures...")
    
    # Essayer différents endpoints pour les matchs
    endpoints_to_try = [
        f"teams/{OM_TEAM_ID}/fixtures",
        f"teams/{OM_TEAM_ID}/fixtures/upcoming",
        f"teams/{OM_TEAM_ID}/fixtures/latest"
    ]
    
    for endpoint in endpoints_to_try:
        print(f"\nTrying: {endpoint}")
        fixtures_data = make_api_call(endpoint)
        
        if fixtures_data and 'data' in fixtures_data:
            fixtures = fixtures_data['data']
            print(f"Found {len(fixtures)} fixtures")
            
            # Analyser les compositions d'équipe dans les fixtures
            players_found = set()
            
            for fixture in fixtures[:5]:  # Regarder les 5 premiers matchs
                if isinstance(fixture, dict):
                    lineups = fixture.get('lineups', [])
                    for lineup in lineups:
                        if lineup.get('team_id') == OM_TEAM_ID:
                            formation = lineup.get('formation', {})
                            if formation:
                                # Récupérer les joueurs de la formation
                                for position_group in formation.values():
                                    if isinstance(position_group, list):
                                        for player_info in position_group:
                                            if isinstance(player_info, dict):
                                                player_id = player_info.get('player_id')
                                                if player_id:
                                                    players_found.add(player_id)
            
            print(f"Found {len(players_found)} unique players in lineups")
            
            if players_found:
                return list(players_found)
    
    return []

def process_player_data(player_data: Dict) -> Dict:
    """Traite les données d'un joueur selon les spécifications"""
    
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
    height = player_data.get('height')
    weight = player_data.get('weight')
    
    # Nationalité sportive
    nationality_data = player_data.get('nationality', {})
    nationality_name = nationality_data.get('name') if nationality_data else None
    
    # Position
    position_data = player_data.get('position', {})
    position_name = position_data.get('name') if position_data else None
    
    # Position détaillée
    detailed_position_data = player_data.get('detailedPosition', {})
    detailed_position = detailed_position_data.get('name') if detailed_position_data else None
    
    # Numéro de maillot (depuis les équipes)
    jersey_number = None
    teams = player_data.get('teams', [])
    for team in teams:
        if team.get('id') == OM_TEAM_ID and 'pivot' in team:
            jersey_number = team['pivot'].get('jersey_number')
            break
    
    return {
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

def main():
    print("=== Getting OM complete squad ===\n")
    
    all_om_players = []
    
    # 1. Essayer via les statistiques de la saison
    stats_players = get_om_players_from_season_stats()
    if stats_players:
        for stat_player in stats_players:
            player_id = stat_player['player_id']
            if player_id and player_id not in [p.get('id') for p in all_om_players]:
                print(f"\nGetting full data for player {player_id}...")
                full_data = make_api_call(f"players/{player_id}", {
                    'include': 'nationality;position;detailedPosition;teams'
                })
                
                if full_data and 'data' in full_data:
                    processed = process_player_data(full_data['data'])
                    all_om_players.append(processed)
                    print(f"✓ Added: {processed['display_name']}")
                
                time.sleep(1)
    
    # 2. Essayer avec les joueurs connus
    known_players = get_known_om_players()
    for player_data in known_players:
        player_id = player_data.get('id')
        if player_id and player_id not in [p.get('id') for p in all_om_players]:
            processed = process_player_data(player_data)
            all_om_players.append(processed)
            print(f"✓ Added known player: {processed['display_name']}")
    
    # 3. Essayer via les fixtures
    fixture_player_ids = search_players_by_team()
    for player_id in fixture_player_ids:
        if player_id not in [p.get('id') for p in all_om_players]:
            print(f"\nGetting fixture player {player_id}...")
            player_data = make_api_call(f"players/{player_id}", {
                'include': 'nationality;position;detailedPosition;teams'
            })
            
            if player_data and 'data' in player_data:
                processed = process_player_data(player_data['data'])
                all_om_players.append(processed)
                print(f"✓ Added fixture player: {processed['display_name']}")
            
            time.sleep(1)
    
    # Sauvegarder les résultats
    output_data = {
        'team_id': OM_TEAM_ID,
        'team_name': 'Olympique Marseille',
        'season_id': SEASON_2025_26_ID,
        'season_name': '2025/2026',
        'league_id': LIGUE1_ID,
        'league_name': 'Ligue 1',
        'fetched_at': datetime.now().isoformat(),
        'players_count': len(all_om_players),
        'players': all_om_players
    }
    
    output_file = 'om_complete_squad_2025_26.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False, default=str)
    
    print(f"\n=== Summary ===")
    print(f"Team: {output_data['team_name']}")
    print(f"Players found: {len(all_om_players)}")
    print(f"Data saved to: {output_file}")
    
    if all_om_players:
        print(f"\n=== Sample players ===")
        for player in all_om_players[:5]:
            print(f"- {player['display_name']} ({player['position']}) - {player['nationality']} - {player['age']} ans")

if __name__ == "__main__":
    main()