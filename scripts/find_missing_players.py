#!/usr/bin/env python3
"""
Script simple pour trouver les joueurs manquants de l'OM
"""

import requests
import json
import time

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
        return None
    except:
        return None

def main():
    print("Recherche des joueurs manquants de l'OM...")
    
    # 1. Robinio Vaz trouvé
    robinio_id = 37713942
    
    # 2. Cherchons d'autres joueurs en testant des IDs proches ou via recherche
    potential_om_players = []
    
    # Vérifier Robinio Vaz
    print(f"\\nVerification Robinio Vaz (ID: {robinio_id})...")
    player_data = make_api_call(f"players/{robinio_id}", {'include': 'teams'})
    if player_data and 'data' in player_data:
        player = player_data['data']
        print(f"  Nom: {player.get('display_name')}")
        print(f"  Age: {2025 - int(player.get('date_of_birth', '2000-01-01').split('-')[0])} ans")
        
        teams = player.get('teams', [])
        for team in teams:
            team_name = team.get('name', '')
            print(f"  Equipe: {team_name}")
            if 'marseille' in team_name.lower():
                print("  -> JOUE A L'OM!")
                potential_om_players.append(robinio_id)
    
    # 3. Chercher d'autres jeunes joueurs avec des IDs proches (souvent les nouveaux joueurs)
    print("\\nRecherche de joueurs avec IDs proches...")
    id_ranges = [
        range(37700000, 37720000, 1000),  # Autour de Robinio Vaz
        range(37750000, 37780000, 1000),  # Autres jeunes joueurs 2025
    ]
    
    for id_range in id_ranges:
        for test_id in id_range:
            if test_id % 5000 == 0:  # Test tous les 5000 pour aller plus vite
                print(f"Testing ID: {test_id}")
                
            player_data = make_api_call(f"players/{test_id}", {'include': 'teams'})
            if player_data and 'data' in player_data:
                player = player_data['data']
                teams = player.get('teams', [])
                
                for team in teams:
                    if 'marseille' in str(team.get('name', '')).lower():
                        print(f"FOUND OM PLAYER: {player.get('display_name')} (ID: {test_id})")
                        potential_om_players.append(test_id)
                        break
            
            time.sleep(0.1)  # Eviter le rate limit
    
    # 4. Charger nos données actuelles pour comparaison
    with open('om_complete_squad_final.json', 'r', encoding='utf-8') as f:
        our_data = json.load(f)
    
    our_player_ids = {p['id'] for p in our_data['players']}
    
    print(f"\\n=== RESULTATS ===")
    print(f"Nos donnees actuelles: {len(our_player_ids)} joueurs")
    print(f"Nouveaux joueurs trouves: {len(potential_om_players)}")
    
    missing_players = set(potential_om_players) - our_player_ids
    
    if missing_players:
        print(f"\\nJoueurs MANQUANTS:")
        for pid in missing_players:
            player_info = make_api_call(f"players/{pid}")
            if player_info and 'data' in player_info:
                p = player_info['data']
                birth_year = p.get('date_of_birth', '2000-01-01').split('-')[0]
                age = 2025 - int(birth_year)
                pos_data = p.get('position', {})
                position = pos_data.get('name') if pos_data else 'Unknown'
                print(f"  - {p.get('display_name')} (ID: {pid}, {age} ans, {position})")
        
        # Sauvegarder les IDs manquants
        with open('missing_om_players.json', 'w') as f:
            json.dump({
                'missing_player_ids': list(missing_players),
                'details': []
            }, f, indent=2)
        
        print(f"\\nIDs manquants sauves dans missing_om_players.json")
    else:
        print("Aucun joueur manquant trouve")

if __name__ == "__main__":
    main()