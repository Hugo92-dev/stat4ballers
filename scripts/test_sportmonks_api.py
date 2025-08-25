#!/usr/bin/env python3
"""
Script de test pour explorer l'API Sportmonks et trouver les bons endpoints
"""

import requests
import json
import time
import sys

# Configuration API
API_TOKEN = "leBzDfKbRE5k9zEg3FuZE3Hh7XbukODNarOXLoVtPAiAtliDZ19wLu1Wnzi2"
BASE_URL = "https://api.sportmonks.com/v3/football"

# IDs fournis
LIGUE1_ID = 301
SEASON_2025_26_ID = 25651

def make_api_call(endpoint: str, params: dict = None):
    """Effectue un appel API avec gestion d'erreurs"""
    if params is None:
        params = {}
    
    params['api_token'] = API_TOKEN
    
    try:
        print(f"Testing API: {endpoint}")
        response = requests.get(f"{BASE_URL}/{endpoint}", params=params, timeout=30)
        
        if response.status_code == 429:
            print("Rate limit hit, waiting 60 seconds...")
            time.sleep(60)
            return make_api_call(endpoint, params)
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Success - Data keys: {list(data.keys()) if isinstance(data, dict) else 'Not a dict'}")
            return data
        else:
            print(f"Error: {response.text}")
            return None
        
    except Exception as e:
        print(f"Exception: {e}")
        return None

def test_endpoints():
    """Test différents endpoints pour trouver les bonnes structures"""
    
    print("=== Test des endpoints Sportmonks ===\n")
    
    # Test 1: Récupérer les équipes de la Ligue 1 (différentes méthodes)
    print("1. Test récupération équipes Ligue 1...")
    
    # Méthode 1: Par ligue
    print("\n1a. Tentative: leagues/{LIGUE1_ID}/teams")
    result1a = make_api_call(f"leagues/{LIGUE1_ID}/teams")
    
    # Méthode 1b: Par ligue avec saison
    print("\n1b. Tentative: leagues/{LIGUE1_ID}/seasons/{SEASON_2025_26_ID}/teams")
    result1b = make_api_call(f"leagues/{LIGUE1_ID}/seasons/{SEASON_2025_26_ID}/teams")
    
    # Méthode 2: Directement par saison
    print(f"\n1c. Tentative: seasons/{SEASON_2025_26_ID}")
    result1c = make_api_call(f"seasons/{SEASON_2025_26_ID}")
    
    # Méthode 3: Standings (peut contenir les équipes)
    print(f"\n1d. Tentative: seasons/{SEASON_2025_26_ID}/standings")
    result1d = make_api_call(f"seasons/{SEASON_2025_26_ID}/standings")
    
    # Test 2: Si on trouve une équipe, tester l'endpoint joueur directement
    print("\n2. Test direct d'un joueur connu (Kondogbia ID: 95696)...")
    kondogbia_data = make_api_call("players/95696", {
        'include': 'country;nationality;city;position;detailedPosition;teams'
    })
    
    if kondogbia_data and 'data' in kondogbia_data:
        player = kondogbia_data['data']
        print(f"\nKondogbia trouvé:")
        print(f"- Nom: {player.get('display_name')}")
        print(f"- Nationalité ID: {player.get('nationality_id')}")
        print(f"- Position ID: {player.get('position_id')}")
        print(f"- Équipes: {len(player.get('teams', []))}")
        
        # Analyser ses équipes pour trouver l'OM
        teams = player.get('teams', [])
        for team in teams:
            team_name = team.get('name', '')
            print(f"  - Équipe: {team_name} (ID: {team.get('id')})")
            if 'marseille' in team_name.lower():
                om_id = team.get('id')
                print(f"*** OM trouvé! ID: {om_id} ***")
                
                # Test de récupération de l'effectif OM
                print(f"\n3. Test effectif OM (ID: {om_id})...")
                
                # Différentes méthodes pour l'effectif
                print(f"\n3a. Tentative: teams/{om_id}/squads")
                squad1 = make_api_call(f"teams/{om_id}/squads")
                
                print(f"\n3b. Tentative: teams/{om_id}/squads/seasons/{SEASON_2025_26_ID}")
                squad2 = make_api_call(f"teams/{om_id}/squads/seasons/{SEASON_2025_26_ID}")
                
                print(f"\n3c. Tentative: teams/{om_id}/players")
                squad3 = make_api_call(f"teams/{om_id}/players")
                
                return om_id
    
    return None

def main():
    om_id = test_endpoints()
    
    if om_id:
        print(f"\n=== ID de l'OM trouvé: {om_id} ===")
    else:
        print(f"\n=== ID de l'OM non trouvé ===")

if __name__ == "__main__":
    main()