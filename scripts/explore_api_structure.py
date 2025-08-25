#!/usr/bin/env python3
"""
Script pour explorer la structure de l'API Sportmonks et trouver les bons endpoints
"""

import requests
import json

# Configuration API
API_TOKEN = "leBzDfKbRE5k9zEg3FuZE3Hh7XbukODNarOXLoVtPAiAtliDZ19wLu1Wnzi2"
BASE_URL = "https://api.sportmonks.com/v3/football"

SEASON_2025_26_ID = 25651

def make_api_call(endpoint: str, params: dict = None):
    if params is None:
        params = {}
    
    params['api_token'] = API_TOKEN
    
    try:
        response = requests.get(f"{BASE_URL}/{endpoint}", params=params, timeout=30)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error {response.status_code}: {response.text}")
            return None
        
    except Exception as e:
        print(f"Exception: {e}")
        return None

def main():
    print("=== Exploration de l'API Sportmonks ===\n")
    
    # 1. Explorer l'équipe 715515 (trouvée chez Kondogbia)
    print("1. Exploration de l'équipe 715515...")
    team_data = make_api_call("teams/715515")
    
    if team_data and 'data' in team_data:
        team = team_data['data']
        print(f"Équipe: {team.get('name')} (ID: {team.get('id')})")
        print(f"Fondée: {team.get('founded')}")
        print(f"Pays: {team.get('country', {}).get('name')}")
        print(f"Logo: {team.get('image_path')}")
        
        # Si c'est l'OM, essayons de récupérer les joueurs
        if 'marseille' in team.get('name', '').lower():
            print("\n*** C'EST L'OM! ***")
            om_id = team.get('id')
            
            print(f"\n2. Récupération des joueurs de l'OM (ID: {om_id})...")
            
            # Test de différents endpoints
            endpoints = [
                (f"teams/{om_id}/players", "players"),
                (f"teams/{om_id}/squads", "squads")
            ]
            
            for endpoint, description in endpoints:
                print(f"\n2.{description}: {endpoint}")
                result = make_api_call(endpoint)
                
                if result and 'data' in result:
                    players = result['data']
                    print(f"  → {len(players)} joueurs trouvés")
                    
                    if players:
                        # Analyser le premier joueur
                        first_player = players[0]
                        print(f"  → Premier joueur: {first_player}")
                        
                        # Si c'est un ID de joueur, récupérer ses détails
                        if isinstance(first_player, dict):
                            player_id = first_player.get('player_id') or first_player.get('id')
                            if player_id:
                                print(f"\n3. Détails du premier joueur (ID: {player_id})...")
                                player_details = make_api_call(f"players/{player_id}", {
                                    'include': 'country;nationality;position;detailedPosition'
                                })
                                
                                if player_details and 'data' in player_details:
                                    player = player_details['data']
                                    print(f"  → Nom: {player.get('display_name')}")
                                    print(f"  → Position: {player.get('position', {}).get('name')}")
                                    print(f"  → Nationalité: {player.get('nationality', {}).get('name')}")
                                    print(f"  → Âge: {player.get('date_of_birth')}")
                                    print(f"  → Taille: {player.get('height')} cm")
                                    print(f"  → Photo: {player.get('image_path')}")
    
    # 2. Testons aussi l'autre ID trouvé (1273446)
    print(f"\n4. Test de l'équipe 1273446...")
    team_data2 = make_api_call("teams/1273446")
    
    if team_data2 and 'data' in team_data2:
        team2 = team_data2['data']
        print(f"Équipe: {team2.get('name')} (ID: {team2.get('id')})")

if __name__ == "__main__":
    main()