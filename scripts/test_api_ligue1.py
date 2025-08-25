#!/usr/bin/env python3
"""
Test rapide de l'API pour Ligue 1
"""

import requests
import json

API_TOKEN = "leBzDfKbRE5k9zEg3FuZE3Hh7XbukODNarOXLoVtPAiAtliDZ19wLu1Wnzi2"
BASE_URL = "https://api.sportmonks.com/v3/football"
LIGUE1_SEASON_ID = 25651

def test_api():
    """Test simple de l'API"""
    
    print("=== Test API Ligue 1 ===")
    
    # Test 1: Récupérer les équipes
    print("\n1. Test récupération des équipes...")
    
    try:
        response = requests.get(
            f"{BASE_URL}/standings/seasons/{LIGUE1_SEASON_ID}",
            params={
                'api_token': API_TOKEN,
                'include': 'participant'
            },
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            teams = []
            
            if 'data' in data:
                for standing in data['data']:
                    participant = standing.get('participant')
                    if participant:
                        teams.append({
                            'id': participant.get('id'),
                            'name': participant.get('name')
                        })
                
                print(f"  [OK] {len(teams)} équipes trouvées:")
                for team in teams[:5]:  # Afficher les 5 premières
                    print(f"    - {team['name']} (ID: {team['id']})")
                
                return teams
            else:
                print("  [ERREUR] Pas de données")
        else:
            print(f"  [ERREUR] Status code: {response.status_code}")
            print(f"  Response: {response.text[:200]}")
    
    except Exception as e:
        print(f"  [ERREUR] Exception: {e}")
    
    return []

if __name__ == "__main__":
    teams = test_api()
    print(f"\nTotal: {len(teams)} équipes")