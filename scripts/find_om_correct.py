#!/usr/bin/env python3
"""
Script pour trouver l'OM et récupérer son effectif avec la bonne API
"""

import requests
import json

# Configuration API
API_TOKEN = "leBzDfKbRE5k9zEg3FuZE3Hh7XbukODNarOXLoVtPAiAtliDZ19wLu1Wnzi2"
BASE_URL = "https://api.sportmonks.com/v3/football"

SEASON_2025_26_ID = 25651

def make_api_call(endpoint: str, params: dict = None):
    """Effectue un appel API"""
    if params is None:
        params = {}
    
    params['api_token'] = API_TOKEN
    
    try:
        print(f"Calling: {endpoint}")
        response = requests.get(f"{BASE_URL}/{endpoint}", params=params, timeout=30)
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"Error: {response.text}")
            return None
        
    except Exception as e:
        print(f"Exception: {e}")
        return None

def main():
    # Testons différentes approches pour trouver les équipes
    
    print("=== Recherche de l'OM ===\n")
    
    # 1. Regarder les infos de la saison
    print("1. Infos de la saison 2025/26...")
    season_data = make_api_call(f"seasons/{SEASON_2025_26_ID}")
    
    if season_data and 'data' in season_data:
        season = season_data['data']
        print(f"Saison: {season.get('name')} - Ligue: {season.get('league', {}).get('name')}")
        
        # Essayons avec include pour avoir plus d'infos
        print("\n2. Saison avec participants...")
        season_with_teams = make_api_call(f"seasons/{SEASON_2025_26_ID}", {'include': 'participants'})
        
        if season_with_teams and 'data' in season_with_teams:
            season_data_full = season_with_teams['data']
            participants = season_data_full.get('participants', [])
            
            print(f"Participants trouvés: {len(participants)}")
            
            om_found = None
            for team in participants:
                team_name = team.get('name', '')
                team_id = team.get('id')
                print(f"  - {team_name} (ID: {team_id})")
                
                if 'marseille' in team_name.lower():
                    om_found = team
                    print(f"*** OM TROUVÉ: {team_name} (ID: {team_id}) ***")
            
            if om_found:
                om_id = om_found.get('id')
                print(f"\n3. Test de récupération de l'effectif OM (ID: {om_id})...")
                
                # Testons les différents endpoints pour l'effectif
                endpoints_to_try = [
                    f"teams/{om_id}/squads",
                    f"teams/{om_id}/players", 
                    f"teams/{om_id}/squads/seasons/{SEASON_2025_26_ID}",
                    f"teams/{om_id}"
                ]
                
                for endpoint in endpoints_to_try:
                    print(f"\nTesting: {endpoint}")
                    result = make_api_call(endpoint)
                    if result and 'data' in result:
                        data = result['data']
                        if isinstance(data, list):
                            print(f"  → {len(data)} éléments trouvés")
                            if len(data) > 0:
                                first_item = data[0]
                                print(f"  → Premier élément: {list(first_item.keys()) if isinstance(first_item, dict) else type(first_item)}")
                        else:
                            print(f"  → Type: {type(data)}")
                            if isinstance(data, dict):
                                print(f"  → Clés: {list(data.keys())}")
    
    # Test direct avec un ID d'équipe connu (si on en a un)
    print(f"\n4. Test direct avec ID équipe (exemple: 715515 trouvé chez Kondogbia)...")
    team_test = make_api_call("teams/715515")
    if team_test and 'data' in team_test:
        team_data = team_test['data']
        print(f"Équipe 715515: {team_data.get('name')} (ID: {team_data.get('id')})")

if __name__ == "__main__":
    main()