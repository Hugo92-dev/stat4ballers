#!/usr/bin/env python3

import requests
import json

API_TOKEN = "leBzDfKbRE5k9zEg3FuZE3Hh7XbukODNarOXLoVtPAiAtliDZ19wLu1Wnzi2"
BASE_URL = "https://api.sportmonks.com/v3/football"

SEASON_2025_26_ID = 25651

def make_api_call(endpoint, params=None):
    if params is None:
        params = {}
    
    params['api_token'] = API_TOKEN
    
    try:
        response = requests.get(f"{BASE_URL}/{endpoint}", params=params)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error {response.status_code} for {endpoint}")
            return None
        
    except Exception as e:
        print(f"Exception for {endpoint}: {e}")
        return None

def main():
    print("Searching for OM in different ways...\n")
    
    # 1. Essayer d'obtenir les équipes via fixtures
    print("1. Trying via fixtures...")
    fixtures_data = make_api_call(f"seasons/{SEASON_2025_26_ID}/fixtures")
    
    if fixtures_data and 'data' in fixtures_data:
        fixtures = fixtures_data['data']
        print(f"Found {len(fixtures)} fixtures")
        
        # Analyser quelques fixtures pour trouver des équipes
        teams_found = set()
        for fixture in fixtures[:10]:  # Regarder les 10 premiers
            participants = fixture.get('participants', [])
            for participant in participants:
                team_name = participant.get('name', '')
                team_id = participant.get('id')
                if team_name and team_id:
                    teams_found.add((team_id, team_name))
                    print(f"  Team: {team_name} (ID: {team_id})")
                    
                    if 'marseille' in team_name.lower():
                        print(f"  *** FOUND OM: {team_name} (ID: {team_id}) ***")
                        
                        # Test récupération de l'effectif
                        print(f"\n2. Getting OM squad (ID: {team_id})...")
                        
                        # Tester différents endpoints pour l'effectif
                        endpoints = [
                            f"teams/{team_id}/players",
                            f"teams/{team_id}/squads",
                            f"teams/{team_id}"
                        ]
                        
                        for endpoint in endpoints:
                            print(f"\nTrying: {endpoint}")
                            result = make_api_call(endpoint)
                            
                            if result and 'data' in result:
                                data = result['data']
                                print(f"Success! Type: {type(data)}")
                                
                                if isinstance(data, list):
                                    print(f"  {len(data)} items found")
                                    if len(data) > 0:
                                        first_item = data[0]
                                        print(f"  First item keys: {list(first_item.keys()) if isinstance(first_item, dict) else type(first_item)}")
                                        
                                        # Si c'est des joueurs, récupérer le premier
                                        if isinstance(first_item, dict):
                                            player_id = first_item.get('player_id') or first_item.get('id')
                                            if player_id:
                                                print(f"\n3. Getting first player details (ID: {player_id})...")
                                                player_data = make_api_call(f"players/{player_id}", {
                                                    'include': 'nationality;position;detailedPosition'
                                                })
                                                
                                                if player_data and 'data' in player_data:
                                                    player = player_data['data']
                                                    print(f"  Player: {player.get('display_name')}")
                                                    print(f"  Position: {player.get('position', {}).get('name')}")
                                                    print(f"  Nationality: {player.get('nationality', {}).get('name')}")
                                                    print(f"  Height: {player.get('height')} cm")
                                                    print(f"  Image: {player.get('image_path')}")
                                elif isinstance(data, dict):
                                    print(f"  Dict keys: {list(data.keys())}")
                        
                        return team_id
        
        print(f"\nTotal teams found in fixtures: {len(teams_found)}")
    
    print("\nOM not found")
    return None

if __name__ == "__main__":
    main()