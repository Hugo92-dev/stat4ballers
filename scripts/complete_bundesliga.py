#!/usr/bin/env python3
"""
Script pour récupérer tous les effectifs de Bundesliga
18 équipes - Saison 2025/2026 (ID: 25646)
"""

import requests
import json
from datetime import datetime, date
from typing import Dict, List, Optional
import time
import os

API_TOKEN = "leBzDfKbRE5k9zEg3FuZE3Hh7XbukODNarOXLoVtPAiAtliDZ19wLu1Wnzi2"
BASE_URL = "https://api.sportmonks.com/v3/football"
BUNDESLIGA_SEASON_ID = 25646

def make_api_call(endpoint: str, params: dict = None) -> Optional[Dict]:
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
    nationality_data = player_data.get('nationality')
    if nationality_data and nationality_data.get('name'):
        return nationality_data.get('name')
    
    country_data = player_data.get('country')
    if country_data and country_data.get('name'):
        return country_data.get('name')
    
    return "Unknown"

def get_bundesliga_teams() -> Dict:
    """Récupère tous les clubs de Bundesliga"""
    print("\n=== Getting Bundesliga teams ===")
    
    teams = {}
    
    standings_response = make_api_call(
        f"standings/seasons/{BUNDESLIGA_SEASON_ID}",
        {'include': 'participant'}
    )
    
    if standings_response and 'data' in standings_response:
        for standing in standings_response['data']:
            participant = standing.get('participant')
            if participant:
                team_id = participant.get('id')
                team_name = participant.get('name')
                if team_id and team_name:
                    # Create clean slug for German teams
                    slug = team_name.lower()
                    
                    # Clean German characters
                    slug = slug.replace('ü', 'u').replace('ö', 'o').replace('ä', 'a').replace('ß', 'ss')
                    
                    # Remove common prefixes/suffixes
                    slug = slug.replace(' fc', '').replace(' cf', '').replace(' ac', '')
                    slug = slug.replace('fc ', '').replace('bv ', '').replace('sv ', '')
                    
                    # Replace spaces and special chars
                    slug = slug.replace(' ', '-').replace('.', '').replace("'", '')
                    
                    # Specific corrections for known teams
                    if 'bayern' in slug and 'münchen' in slug:
                        slug = 'bayern-munich'
                    elif 'borussia' in slug and 'dortmund' in slug:
                        slug = 'borussia-dortmund'
                    elif 'borussia' in slug and 'mönchengladbach' in slug:
                        slug = 'borussia-monchengladbach'
                    elif 'rb leipzig' in team_name.lower():
                        slug = 'rb-leipzig'
                    elif 'bayer' in slug and 'leverkusen' in slug:
                        slug = 'bayer-leverkusen'
                    elif 'eintracht frankfurt' in team_name.lower():
                        slug = 'eintracht-frankfurt'
                    elif 'union berlin' in team_name.lower():
                        slug = 'union-berlin'
                    elif 'werder bremen' in team_name.lower():
                        slug = 'werder-bremen'
                    elif 'vfl wolfsburg' in team_name.lower():
                        slug = 'wolfsburg'
                    elif 'vfb stuttgart' in team_name.lower():
                        slug = 'stuttgart'
                    elif 'tsg hoffenheim' in team_name.lower():
                        slug = 'hoffenheim'
                    elif 'sc freiburg' in team_name.lower():
                        slug = 'freiburg'
                    elif 'fsv mainz' in team_name.lower():
                        slug = 'mainz'
                    elif 'fc augsburg' in team_name.lower():
                        slug = 'augsburg'
                    elif 'fc köln' in team_name.lower():
                        slug = 'koln'
                    elif 'st pauli' in team_name.lower():
                        slug = 'st-pauli'
                    elif 'hamburger sv' in team_name.lower():
                        slug = 'hamburger-sv'
                    elif 'heidenheim' in team_name.lower():
                        slug = 'heidenheim'
                    
                    teams[team_id] = {
                        'name': team_name,
                        'slug': slug
                    }
                    print(f"  Found: {team_name} (ID: {team_id}, slug: {slug})")
    
    return teams

def fetch_player_details_batch(player_ids: List[int], jersey_numbers: Dict[int, int]) -> List[Dict]:
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
        
        time.sleep(0.05)
    
    return players_data

def fetch_team_squad(team_id: int, team_name: str) -> List[Dict]:
    print(f"  Processing {team_name}...")
    
    player_ids = set()
    jersey_numbers = {}
    
    # Get squad with jersey numbers
    squads_response = make_api_call(
        f"squads/seasons/{BUNDESLIGA_SEASON_ID}/teams/{team_id}"
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
    
    # Fetch player details
    players_data = fetch_player_details_batch(list(player_ids), jersey_numbers)
    
    print(f"    -> {len(players_data)} players retrieved")
    return players_data

def save_team_data(team_id: int, team_info: dict, output_dir: str):
    team_file = os.path.join(output_dir, f"{team_info['slug']}.json")
    with open(team_file, 'w', encoding='utf-8') as f:
        json.dump({
            'id': team_id,
            'name': team_info['name'],
            'slug': team_info['slug'],
            'players': team_info['players']
        }, f, indent=2, ensure_ascii=False, default=str)

def main():
    print("=== BUNDESLIGA SQUADS FETCHER 2025/2026 ===")
    
    # Create output directory
    output_dir = 'data/bundesliga_2025_2026'
    os.makedirs(output_dir, exist_ok=True)
    
    # Get all teams
    teams = get_bundesliga_teams()
    
    if not teams:
        print("ERROR: No teams found")
        return
    
    print(f"\nFound {len(teams)} teams")
    
    all_teams_data = {}
    
    # Process each team
    for i, (team_id, team_info) in enumerate(teams.items(), 1):
        print(f"\n[{i}/{len(teams)}] {team_info['name']}")
        
        players = fetch_team_squad(team_id, team_info['name'])
        
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
    print("\n=== Generating TypeScript file ===")
    
    ts_content = "export const bundesligaTeams = [\n"
    
    for team_id, team_info in all_teams_data.items():
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
    
    ts_file = "data/bundesligaTeams.ts"
    with open(ts_file, 'w', encoding='utf-8') as f:
        f.write(ts_content)
    
    print(f"TypeScript file saved: {ts_file}")
    
    print("\n=== BUNDESLIGA COMPLETED ===")
    print(f"Processed {len(all_teams_data)} teams")
    
    for team_id, team_info in all_teams_data.items():
        print(f"  - {team_info['name']}: {len(team_info['players'])} players")

if __name__ == "__main__":
    main()