import requests
import json
from datetime import datetime

API_KEY = "j28l04KZC0LGFAdbxIzdyb8zz253K1YegT5vEUN5taw0dxuNr6U3jtRMmS6C"
BASE_URL = "https://api.sportmonks.com/v3/football"

def make_test_request(endpoint, params=None):
    """Faire une requête test à l'API"""
    url = f"{BASE_URL}{endpoint}"
    if params is None:
        params = {}
    params['api_token'] = API_KEY
    
    print(f"\nTesting: {endpoint}")
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        if 'data' in data:
            if isinstance(data['data'], list):
                print(f"SUCCESS! Found {len(data['data'])} items")
                if data['data']:
                    print(f"First item sample: {json.dumps(data['data'][0], indent=2)[:500]}...")
            else:
                print(f"SUCCESS! Got data")
                print(f"Data sample: {json.dumps(data['data'], indent=2)[:500]}...")
        else:
            print(f"WARNING: Response but no 'data' key: {list(data.keys())}")
            
        return data
    except requests.exceptions.RequestException as e:
        print(f"ERROR: {e}")
        return None

print("=" * 60)
print("TESTING SQUAD ENDPOINTS FOR PSG (ID: 591)")
print("=" * 60)

# Test 1: Squad via squads/teams/{id}
print("\n1. Testing /squads/teams/{id}")
data = make_test_request("/squads/teams/591", {'include': 'player'})

# Test 2: Squad via squads/seasons/{season_id}/teams/{team_id}
print("\n2. Testing /squads/seasons/{season_id}/teams/{team_id}")
# Utilisons la saison 2024/2025 (ID trouvé précédemment)
data = make_test_request("/squads/seasons/23639/teams/591", {'include': 'player'})

# Test 3: Players via teams/{id}/players
print("\n3. Testing /teams/{id}/players")
data = make_test_request("/teams/591/players", {'include': 'position,nationality'})

# Test 4: Squad details via teams/{id} with includes
print("\n4. Testing /teams/{id} with squad include")
data = make_test_request("/teams/591", {'include': 'squad.player'})

# Test 5: Current squad via teams/{id}/current-squad
print("\n5. Testing /teams/{id}/current-squad")
data = make_test_request("/teams/591/current-squad")

# Test 6: Get team with latest includes
print("\n6. Testing /teams/{id} with latest include")
data = make_test_request("/teams/591", {'include': 'latest'})

# Test 7: Search for Marseille and get squad
print("\n7. Testing Marseille (search and squad)")
search_data = make_test_request("/teams/search/marseille")
if search_data and search_data.get('data'):
    marseille_id = search_data['data'][0]['id']
    print(f"Found Marseille with ID: {marseille_id}")
    squad_data = make_test_request(f"/squads/teams/{marseille_id}", {'include': 'player'})