#!/usr/bin/env python3

import requests
import json
import sys

API_TOKEN = "leBzDfKbRE5k9zEg3FuZE3Hh7XbukODNarOXLoVtPAiAtliDZ19wLu1Wnzi2"
BASE_URL = "https://api.sportmonks.com/v3/football"

def make_api_call(endpoint, params=None):
    if params is None:
        params = {}
    
    params['api_token'] = API_TOKEN
    
    try:
        response = requests.get(f"{BASE_URL}/{endpoint}", params=params)
        
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"Error {response.status_code}: {response.text}")
            return None
        
    except Exception as e:
        print(f"Exception: {e}")
        return None

def test_team(team_id):
    print(f"\n=== Testing team {team_id} ===")
    
    # Récupérer les infos de l'équipe
    team_data = make_api_call(f"teams/{team_id}")
    
    if team_data and 'data' in team_data:
        team = team_data['data']
        team_name = team.get('name')
        print(f"Team name: {team_name}")
        print(f"Founded: {team.get('founded')}")
        print(f"Short code: {team.get('short_code')}")
        
        if team_name and 'marseille' in team_name.lower():
            print("*** THIS IS OM! ***")
            
            # Récupérer l'effectif
            print("\nGetting squad...")
            squad_data = make_api_call(f"teams/{team_id}/players")
            
            if squad_data and 'data' in squad_data:
                players = squad_data['data']
                print(f"Found {len(players)} players")
                
                # Analyser quelques joueurs
                for i, player_data in enumerate(players[:3]):
                    player_id = None
                    if isinstance(player_data, dict):
                        player_id = player_data.get('player_id') or player_data.get('id')
                    elif isinstance(player_data, (int, str)):
                        player_id = player_data
                    
                    if player_id:
                        print(f"\nPlayer {i+1}: ID {player_id}")
                        
                        # Récupérer les détails
                        player_details = make_api_call(f"players/{player_id}")
                        if player_details and 'data' in player_details:
                            player = player_details['data']
                            print(f"  Name: {player.get('display_name')}")
            
            return True
        else:
            print(f"Not OM (name: {team_name})")
    
    return False

def main():
    # Tester les deux IDs trouvés chez Kondogbia
    team_ids = [1273446, 715515]
    
    om_found = False
    for team_id in team_ids:
        if test_team(team_id):
            om_found = True
            break
    
    if not om_found:
        print("\nOM not found in the tested teams")
        
        # Test avec un autre joueur connu de l'OM
        print("\n=== Testing another OM player ===")
        # Rabiot (si il est à l'OM) ou un autre joueur français récent
        other_players = [95696]  # Kondogbia encore pour debug
        
        for player_id in other_players:
            print(f"\nTesting player {player_id}...")
            player_data = make_api_call(f"players/{player_id}", {
                'include': 'teams'
            })
            
            if player_data and 'data' in player_data:
                player = player_data['data']
                print(f"Player: {player.get('display_name')}")
                
                teams = player.get('teams', [])
                print(f"Teams: {len(teams)}")
                for team in teams:
                    print(f"  Team ID: {team.get('id')}")

if __name__ == "__main__":
    main()