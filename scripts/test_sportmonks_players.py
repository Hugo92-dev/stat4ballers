import requests
import json

API_KEY = "j28l04KZC0LGFAdbxIzdyb8zz253K1YegT5vEUN5taw0dxuNr6U3jtRMmS6C"
base_url = "https://api.sportmonks.com/v3/football"

def test_endpoint(endpoint, params=None):
    """Test un endpoint spécifique"""
    if params is None:
        params = {}
    params['api_token'] = API_KEY
    
    try:
        url = f"{base_url}{endpoint}"
        print(f"\nTesting: {endpoint}")
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        # Afficher la structure de la réponse
        if isinstance(data, dict):
            print(f"Response keys: {list(data.keys())}")
            if 'data' in data:
                if isinstance(data['data'], list):
                    print(f"Data is a list with {len(data['data'])} items")
                    if data['data']:
                        print(f"First item keys: {list(data['data'][0].keys())}")
                        # Afficher le premier joueur
                        first_item = data['data'][0]
                        print(f"\nFirst player:")
                        print(f"  Name: {first_item.get('name', 'N/A')}")
                        print(f"  Display Name: {first_item.get('display_name', 'N/A')}")
                        print(f"  Position ID: {first_item.get('position_id', 'N/A')}")
                        print(f"  Date of Birth: {first_item.get('date_of_birth', 'N/A')}")
                        print(f"  Nationality ID: {first_item.get('nationality_id', 'N/A')}")
                elif isinstance(data['data'], dict):
                    print(f"Data is a dict with keys: {list(data['data'].keys())}")
        
        return data
        
    except Exception as e:
        print(f"Error: {e}")
        return None

# PSG ID trouvé: 591
psg_id = 591

print("=" * 60)
print("TESTING VARIOUS ENDPOINTS TO GET PSG PLAYERS")
print("=" * 60)

# Test 1: Essayer l'endpoint players avec filtre team
print("\nTEST 1: Get players filtered by team")
data = test_endpoint("/players", {"filters": f"teams:{psg_id}", "per_page": 5})

# Test 2: Essayer l'endpoint squads/teams
print("\n" + "=" * 60)
print("TEST 2: Get squad by team ID")
data = test_endpoint(f"/squads/teams/{psg_id}")

# Test 3: Essayer l'endpoint teams avec include=players
print("\n" + "=" * 60)
print("TEST 3: Get team with players included")
data = test_endpoint(f"/teams/{psg_id}", {"include": "players"})

# Test 4: Essayer de trouver la saison actuelle de Ligue 1
print("\n" + "=" * 60)
print("TEST 4: Get current season for Ligue 1")
data = test_endpoint("/seasons", {
    "filters": "leagues:301;is_current:true",
    "per_page": 1
})

if data and 'data' in data and data['data']:
    current_season_id = data['data'][0]['id']
    print(f"\nFound current season ID: {current_season_id}")
    
    # Test 5: Obtenir l'effectif de PSG pour la saison actuelle
    print("\n" + "=" * 60)
    print("TEST 5: Get PSG squad for current season")
    data = test_endpoint(f"/squads/seasons/{current_season_id}/teams/{psg_id}")
    
    # Test 6: Alternative - obtenir les joueurs par saison et équipe
    print("\n" + "=" * 60)
    print("TEST 6: Get players by season and team")
    data = test_endpoint("/players", {
        "filters": f"teams:{psg_id};seasons:{current_season_id}",
        "per_page": 30
    })