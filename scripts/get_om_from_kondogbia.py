#!/usr/bin/env python3

import requests
import json

API_TOKEN = "leBzDfKbRE5k9zEg3FuZE3Hh7XbukODNarOXLoVtPAiAtliDZ19wLu1Wnzi2"
BASE_URL = "https://api.sportmonks.com/v3/football"

def make_api_call(endpoint, params=None):
    if params is None:
        params = {}
    
    params['api_token'] = API_TOKEN
    
    try:
        response = requests.get(f"{BASE_URL}/{endpoint}", params=params, timeout=30)
        
        if response.status_code == 200:
            return response.json()
        else:
            return None
        
    except Exception as e:
        return None

def main():
    print("Getting Kondogbia data...")
    
    # Récupérer Kondogbia avec ses équipes
    kondogbia_data = make_api_call("players/95696", {
        'include': 'teams'
    })
    
    if kondogbia_data and 'data' in kondogbia_data:
        player = kondogbia_data['data']
        print(f"Player: {player.get('display_name')}")
        
        teams = player.get('teams', [])
        print(f"Teams found: {len(teams)}")
        
        for i, team in enumerate(teams):
            team_id = team.get('id')
            print(f"\nTeam {i+1}: ID {team_id}")
            
            # Récupérer les détails de l'équipe
            team_details = make_api_call(f"teams/{team_id}")
            
            if team_details and 'data' in team_details:
                team_info = team_details['data']
                team_name = team_info.get('name', 'Unknown')
                print(f"  Name: {team_name}")
                
                if 'marseille' in team_name.lower():
                    print(f"  *** FOUND OM: {team_name} (ID: {team_id}) ***")
                    
                    # Récupérer l'effectif
                    print(f"  Getting squad for team {team_id}...")
                    
                    squad = make_api_call(f"teams/{team_id}/players")
                    
                    if squad and 'data' in squad:
                        players = squad['data']
                        print(f"  Squad size: {len(players)} players")
                        
                        # Sauvegarder les IDs des joueurs
                        player_ids = []
                        for squad_player in players:
                            if isinstance(squad_player, dict):
                                player_id = squad_player.get('player_id') or squad_player.get('id')
                                if player_id:
                                    player_ids.append(player_id)
                        
                        print(f"  Player IDs found: {len(player_ids)}")
                        
                        # Sauvegarder dans un fichier
                        output = {
                            'om_team_id': team_id,
                            'om_team_name': team_name,
                            'player_ids': player_ids
                        }
                        
                        with open('../om_player_ids.json', 'w') as f:
                            json.dump(output, f, indent=2)
                        
                        print(f"  Saved to om_player_ids.json")
                        return team_id
    
    return None

if __name__ == "__main__":
    main()