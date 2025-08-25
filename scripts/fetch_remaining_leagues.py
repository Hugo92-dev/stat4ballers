#!/usr/bin/env python3
"""
Script pour récupérer les 2 championnats restants (Serie A et Bundesliga)
"""

import requests
import json
from datetime import datetime, date
from typing import Dict, List, Optional
import time
import os

API_TOKEN = "leBzDfKbRE5k9zEg3FuZE3Hh7XbukODNarOXLoVtPAiAtliDZ19wLu1Wnzi2"
BASE_URL = "https://api.sportmonks.com/v3/football"

# IDs des saisons 2025/2026 restantes
SEASONS = {
    'serie-a': 25533,
    'bundesliga': 25646
}

def make_api_call(endpoint: str, params: dict = None) -> Optional[Dict]:
    """Fait un appel API avec gestion des erreurs et rate limiting"""
    if params is None:
        params = {}
    
    params['api_token'] = API_TOKEN
    
    try:
        response = requests.get(f"{BASE_URL}/{endpoint}", params=params, timeout=30)
        
        if response.status_code == 429:
            print("Rate limit hit, waiting 60 seconds...")
            time.sleep(60)
            return make_api_call(endpoint, params)
        
        if response.status_code == 200:
            return response.json()
        else:
            return None
        
    except Exception as e:
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
    except:
        return None

def get_nationality_smart(player_data: dict) -> Optional[str]:
    """Récupère la nationalité intelligemment"""
    nationality_data = player_data.get('nationality')
    if nationality_data and nationality_data.get('name'):
        return nationality_data.get('name')
    
    country_data = player_data.get('country')
    if country_data and country_data.get('name'):
        return country_data.get('name')
    
    return "Unknown"

def get_league_teams(league_name: str, season_id: int) -> Dict:
    """Récupère tous les clubs d'un championnat"""
    print(f"\n=== Getting {league_name} teams ===")
    
    teams = {}
    
    standings_response = make_api_call(
        f"standings/seasons/{season_id}",
        {'include': 'participant'}
    )
    
    if standings_response and 'data' in standings_response:
        for standing in standings_response['data']:
            participant = standing.get('participant')
            if participant:
                team_id = participant.get('id')
                team_name = participant.get('name')
                if team_id and team_name:
                    # Create slug
                    slug = team_name.lower()
                    # Clean up slug for all leagues
                    slug = slug.replace(' fc', '').replace(' cf', '').replace(' ac', '')
                    slug = slug.replace(' united', '-united').replace(' city', '-city')
                    slug = slug.replace(' de ', '-').replace(' ', '-')
                    slug = slug.replace('.', '').replace("'", '')
                    
                    teams[team_id] = {
                        'name': team_name,
                        'slug': slug
                    }
                    print(f"  Found: {team_name} (ID: {team_id})")
    
    return teams

def fetch_player_details_batch(player_ids: List[int], jersey_numbers: Dict[int, int]) -> List[Dict]:
    """Récupère les détails de plusieurs joueurs en batch"""
    players_data = []
    
    for player_id in player_ids:
        player_response = make_api_call(f"players/{player_id}", {
            'include': 'nationality;country;position'
        })
        
        if player_response and 'data' in player_response:
            player_data = player_response['data']
            
            nationality = get_nationality_smart(player_data)
            
            position_data = player_data.get('position', {})
            position_name = position_data.get('name') if position_data else 'Unknown'
            
            position_mapping = {
                'Goalkeeper': 'GK',
                'Defender': 'DF',
                'Midfielder': 'MF',
                'Attacker': 'FW'
            }
            
            position_id_mapping = {
                'Goalkeeper': 24,
                'Defender': 25,
                'Midfielder': 26,
                'Attacker': 27
            }
            
            processed_data = {
                'id': player_id,
                'display_name': player_data.get('display_name') or player_data.get('name', 'Unknown'),
                'image_path': player_data.get('image_path'),
                'age': calculate_age(player_data.get('date_of_birth')),
                'height': player_data.get('height'),
                'weight': player_data.get('weight'),
                'nationality': nationality,
                'position': position_mapping.get(position_name, position_name),
                'position_id': position_id_mapping.get(position_name, 26),
                'jersey_number': jersey_numbers.get(player_id),
                'slug': (player_data.get('display_name') or '').lower().replace(' ', '-').replace('.', '').replace("'", '')
            }
            
            players_data.append(processed_data)
        
        time.sleep(0.05)  # Small delay between requests
    
    return players_data

def fetch_team_squad_fast(team_id: int, team_name: str, season_id: int) -> List[Dict]:
    """Version rapide pour récupérer l'effectif d'une équipe"""
    print(f"  Processing {team_name}...")
    
    player_ids = set()
    jersey_numbers = {}
    
    # Get squad with jersey numbers
    squads_response = make_api_call(
        f"squads/seasons/{season_id}/teams/{team_id}"
    )
    
    if squads_response and 'data' in squads_response:
        for squad_entry in squads_response['data']:
            player_id = squad_entry.get('player_id')
            jersey = squad_entry.get('jersey_number')
            if player_id:
                player_ids.add(player_id)
                if jersey:
                    jersey_numbers[player_id] = jersey
    
    if not player_ids:
        print(f"    No players found for {team_name}")
        return []
    
    # Fetch player details in batch
    players_data = fetch_player_details_batch(list(player_ids), jersey_numbers)
    
    print(f"    -> {len(players_data)} players retrieved")
    return players_data

def save_team_data(team_id: int, team_info: dict, output_dir: str):
    """Sauvegarde les données d'une équipe"""
    team_file = os.path.join(output_dir, f"{team_info['slug']}.json")
    with open(team_file, 'w', encoding='utf-8') as f:
        json.dump({
            'id': team_id,
            'name': team_info['name'],
            'slug': team_info['slug'],
            'players': team_info['players']
        }, f, indent=2, ensure_ascii=False, default=str)

def generate_typescript_file(league_name: str, teams_data: Dict) -> str:
    """Génère le fichier TypeScript pour un championnat"""
    
    # Convert league name for export
    export_name = league_name.replace('-', '')
    ts_content = f"export const {export_name}Teams = [\n"
    
    for team_id, team_info in teams_data.items():
        ts_content += f"""  {{
    id: {team_id},
    nom: "{team_info['name']}",
    slug: "{team_info['slug']}",
    players: [\n"""
        
        for player in team_info.get('players', []):
            jersey = player.get('jersey_number', 'null')
            if jersey is None:
                jersey = 'null'
                
            ts_content += f"""      {{
        id: {player['id']},
        nom: "{player['display_name']}",
        displayName: "{player['display_name']}",
        position: "{player['position']}",
        position_id: {player['position_id']},
        numero: {jersey},
        age: "{player['age'] if player['age'] else 'Unknown'}",
        nationalite: "{player['nationality']}",
        taille: {player['height'] if player['height'] else 'null'},
        poids: {player['weight'] if player['weight'] else 'null'},
        image: "{player['image_path'] or 'https://cdn.sportmonks.com/images/soccer/placeholder.png'}",
        playerSlug: "{player['slug']}"
      }},\n"""
        
        ts_content = ts_content.rstrip(',\n') + "\n    ]\n  },\n"
    
    ts_content = ts_content.rstrip(',\n') + "\n];\n"
    
    return ts_content

def process_league(league_name: str, season_id: int):
    print(f"\n{'='*60}")
    print(f"PROCESSING: {league_name.upper()}")
    print(f"{'='*60}")
    
    # Create output directory
    output_dir = f'data/{league_name}_2025_2026'
    os.makedirs(output_dir, exist_ok=True)
    
    # Get all teams
    teams = get_league_teams(league_name, season_id)
    
    if not teams:
        print(f"ERROR: No teams found for {league_name}")
        return
    
    print(f"\nFound {len(teams)} teams")
    
    all_teams_data = {}
    
    # Process each team
    for i, (team_id, team_info) in enumerate(teams.items(), 1):
        print(f"\n[{i}/{len(teams)}] {team_info['name']}")
        
        players = fetch_team_squad_fast(team_id, team_info['name'], season_id)
        
        team_data = {
            'name': team_info['name'],
            'slug': team_info['slug'],
            'players': sorted(players, key=lambda x: (
                x['position_id'],
                x['jersey_number'] if x['jersey_number'] else 999,
                x['display_name']
            ))
        }
        
        # Save individual team file
        save_team_data(team_id, team_data, output_dir)
        
        all_teams_data[team_id] = team_data
        
        # Small pause between teams
        time.sleep(0.5)
    
    # Generate TypeScript file
    print(f"\n=== Generating TypeScript file for {league_name} ===")
    ts_content = generate_typescript_file(league_name, all_teams_data)
    
    ts_file = f"data/{league_name.replace('-', '')}Teams.ts"
    with open(ts_file, 'w', encoding='utf-8') as f:
        f.write(ts_content)
    
    print(f"TypeScript file saved: {ts_file}")
    
    print(f"\n=== {league_name.upper()} COMPLETED ===")
    print(f"Processed {len(all_teams_data)} teams")
    
    for team_id, team_info in all_teams_data.items():
        print(f"  - {team_info['name']}: {len(team_info['players'])} players")
    
    return len(all_teams_data)

def main():
    print("=== REMAINING LEAGUES SQUADS FETCHER 2025/2026 ===")
    
    total_teams = 0
    
    for league_name, season_id in SEASONS.items():
        try:
            teams_count = process_league(league_name, season_id)
            if teams_count:
                total_teams += teams_count
            
            # Pause between leagues
            print(f"\nPausing before next league...")
            time.sleep(2)
            
        except Exception as e:
            print(f"\nERROR processing {league_name}: {e}")
            continue
    
    print("\n" + "="*60)
    print("=== REMAINING LEAGUES COMPLETED ===")
    print(f"Total teams processed: {total_teams}")
    print("="*60)

if __name__ == "__main__":
    main()