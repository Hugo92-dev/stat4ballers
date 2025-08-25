#!/usr/bin/env python3
"""
Script pour récupérer l'effectif de l'OM via la ligue
"""

import requests
import json
import time

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
        print(f"Calling: {endpoint}")
        response = requests.get(f"{BASE_URL}/{endpoint}", params=params, timeout=30)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error {response.status_code}: {response.text[:200]}")
            return None
        
    except Exception as e:
        print(f"Exception: {e}")
        return None

def main():
    print("=== Getting OM squad via league data ===\n")
    
    # 1. Essayer d'obtenir les données via la ligue
    print("1. Trying league endpoint...")
    league_data = make_api_call(f"leagues/{LIGUE1_ID}")
    
    if league_data and 'data' in league_data:
        league = league_data['data']
        print(f"League: {league.get('name')}")
    
    # 2. Essayer seasons avec différents includes
    print("\n2. Trying season with includes...")
    includes = ['teams', 'participants', 'standings', 'fixtures']
    
    for include in includes:
        print(f"\nTrying include: {include}")
        season_data = make_api_call(f"seasons/{SEASON_2025_26_ID}", {
            'include': include
        })
        
        if season_data and 'data' in season_data:
            season = season_data['data']
            print(f"Success with include: {include}")
            
            # Chercher les données des équipes/participants
            for key in [include, include[:-1]]:  # Essayer singulier aussi
                if key in season:
                    items = season[key]
                    print(f"Found {len(items)} {key}")
                    
                    # Chercher l'OM
                    for item in items:
                        if isinstance(item, dict):
                            item_name = item.get('name', '')
                            item_id = item.get('id')
                            
                            if 'marseille' in item_name.lower() or item_id == OM_TEAM_ID:
                                print(f"*** FOUND OM: {item_name} (ID: {item_id}) ***")
                                
                                # Si c'est dans standings, il peut y avoir des infos d'équipe
                                if 'participant' in item:
                                    participant = item['participant']
                                    print(f"Participant: {participant.get('name')}")
                                
                                return
    
    # 3. Approche directe : utiliser l'ID 44 pour récupérer l'équipe et ses statistiques
    print(f"\n3. Direct team info (ID: {OM_TEAM_ID})...")
    team_data = make_api_call(f"teams/{OM_TEAM_ID}")
    
    if team_data and 'data' in team_data:
        team = team_data['data']
        print(f"Team: {team.get('name')}")
        print(f"Founded: {team.get('founded')}")
        print(f"Short code: {team.get('short_code')}")
        
        # Essayer avec des includes
        print(f"\n4. Team with includes...")
        includes = ['players', 'squad', 'statistics', 'transfers']
        
        for include in includes:
            print(f"\nTrying team include: {include}")
            team_with_include = make_api_call(f"teams/{OM_TEAM_ID}", {
                'include': include
            })
            
            if team_with_include and 'data' in team_with_include:
                team_full = team_with_include['data']
                
                if include in team_full:
                    data = team_full[include]
                    print(f"Found {include}: {len(data) if isinstance(data, list) else type(data)}")
                    
                    if isinstance(data, list) and len(data) > 0:
                        print(f"First item: {data[0] if isinstance(data[0], dict) else data[0]}")
    
    # 4. Essayer de récupérer des joueurs spécifiques de l'OM
    print(f"\n5. Testing known OM players...")
    known_om_players = [95696]  # Kondogbia
    
    for player_id in known_om_players:
        print(f"\nPlayer {player_id}:")
        player_data = make_api_call(f"players/{player_id}", {
            'include': 'teams;statistics'
        })
        
        if player_data and 'data' in player_data:
            player = player_data['data']
            print(f"  Name: {player.get('display_name')}")
            
            # Chercher les stats par équipe/saison
            statistics = player.get('statistics', [])
            print(f"  Statistics: {len(statistics)} seasons")
            
            for stat in statistics:
                if isinstance(stat, dict):
                    team_id = stat.get('team_id')
                    season_id = stat.get('season_id')
                    print(f"    Season {season_id}, Team {team_id}")
                    
                    if team_id == OM_TEAM_ID:
                        print(f"    *** OM season found! Season: {season_id} ***")

if __name__ == "__main__":
    main()