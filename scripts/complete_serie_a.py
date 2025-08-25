#!/usr/bin/env python3
"""
Script pour compléter la Serie A - équipes manquantes
"""

import requests
import json
from datetime import datetime, date
from typing import Dict, List, Optional
import time
import os

API_TOKEN = "leBzDfKbRE5k9zEg3FuZE3Hh7XbukODNarOXLoVtPAiAtliDZ19wLu1Wnzi2"
BASE_URL = "https://api.sportmonks.com/v3/football"
SERIE_A_SEASON_ID = 25533

# Équipes manquantes
MISSING_TEAMS = {
    113: {"name": "Milan", "slug": "milan"},
    8513: {"name": "Bologna", "slug": "bologna"},
    2714: {"name": "Sassuolo", "slug": "sassuolo"},
    398: {"name": "Parma", "slug": "parma"},
    43: {"name": "Lazio", "slug": "lazio"}
}

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

def fetch_team_squad(team_id: int, team_name: str) -> List[Dict]:
    print(f"  Processing {team_name}...")
    
    player_ids = set()
    jersey_numbers = {}
    
    squads_response = make_api_call(
        f"squads/seasons/{SERIE_A_SEASON_ID}/teams/{team_id}"
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
    
    print(f"    -> {len(players_data)} players retrieved")
    return players_data

def main():
    print("=== COMPLETING SERIE A (5 missing teams) ===")
    
    output_dir = 'data/serie-a_2025_2026'
    
    for team_id, team_info in MISSING_TEAMS.items():
        print(f"\n[{team_info['name']}] Team ID: {team_id}")
        
        players = fetch_team_squad(team_id, team_info['name'])
        
        team_data = {
            'id': team_id,
            'name': team_info['name'],
            'slug': team_info['slug'],
            'players': sorted(players, key=lambda x: (
                x['position_id'],
                x['jersey_number'] if x['jersey_number'] else 999,
                x['display_name']
            ))
        }
        
        # Save team file
        team_file = os.path.join(output_dir, f"{team_info['slug']}.json")
        with open(team_file, 'w', encoding='utf-8') as f:
            json.dump(team_data, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"    Saved to: {team_file}")
        
        time.sleep(1)
    
    print("\n=== SERIE A COMPLETION DONE ===")
    print("Now regenerating complete Serie A TypeScript file...")
    
    # Load all Serie A teams and regenerate TypeScript
    all_teams = {}
    
    for filename in os.listdir(output_dir):
        if filename.endswith('.json'):
            with open(os.path.join(output_dir, filename), 'r', encoding='utf-8') as f:
                team_data = json.load(f)
                all_teams[team_data['id']] = team_data
    
    # Generate TypeScript file
    ts_content = "export const serieATeams = [\n"
    
    for team_id, team_info in all_teams.items():
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
    
    ts_file = "data/serieATeams.ts"
    with open(ts_file, 'w', encoding='utf-8') as f:
        f.write(ts_content)
    
    print(f"TypeScript file updated: {ts_file}")
    print(f"Total Serie A teams: {len(all_teams)}")

if __name__ == "__main__":
    main()