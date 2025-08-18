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
                        print(f"First item: {json.dumps(data['data'][0], indent=2)[:500]}...")
                elif isinstance(data['data'], dict):
                    print(f"Data is a dict with keys: {list(data['data'].keys())}")
                    print(f"Data sample: {json.dumps(data['data'], indent=2)[:500]}...")
        
        return data
        
    except Exception as e:
        print(f"Error: {e}")
        if hasattr(e, 'response') and e.response:
            print(f"Response: {e.response.text[:500]}")
        return None

# Test 1: Info sur la Ligue 1
print("=" * 60)
print("TEST 1: Get Ligue 1 info with includes")
data = test_endpoint("/leagues/301", {"include": "currentSeason,seasons"})

# Test 2: Chercher les saisons de la Ligue 1
print("\n" + "=" * 60)
print("TEST 2: Get seasons for Ligue 1")
data = test_endpoint("/leagues/301/seasons")

# Test 3: Chercher toutes les saisons
print("\n" + "=" * 60)
print("TEST 3: Get all seasons filtered by league")
data = test_endpoint("/seasons", {"filters": "leagues:301", "per_page": 5})

# Test 4: Chercher une équipe spécifique (PSG)
print("\n" + "=" * 60)
print("TEST 4: Search for PSG team")
data = test_endpoint("/teams/search/paris", {"per_page": 5})

# Test 5: Si on trouve PSG, obtenir son effectif
if data and 'data' in data and data['data']:
    psg_id = None
    for team in data['data']:
        if 'paris' in team.get('name', '').lower() and 'saint' in team.get('name', '').lower():
            psg_id = team['id']
            print(f"\nFound PSG with ID: {psg_id}")
            break
    
    if psg_id:
        print("\n" + "=" * 60)
        print("TEST 5: Get PSG squad")
        data = test_endpoint(f"/teams/{psg_id}/squad")