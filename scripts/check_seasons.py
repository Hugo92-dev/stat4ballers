import requests
import json

API_KEY = "j28l04KZC0LGFAdbxIzdyb8zz253K1YegT5vEUN5taw0dxuNr6U3jtRMmS6C"
BASE_URL = "https://api.sportmonks.com/v3/football"

def make_request(endpoint, params=None):
    if params is None:
        params = {}
    
    params['api_token'] = API_KEY
    
    try:
        response = requests.get(f"{BASE_URL}/{endpoint}", params=params)
        response.raise_for_status()
        
        data = response.json()
        return data.get('data', [])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {endpoint}: {e}")
        return []

# Vérifier les ligues et leurs saisons
leagues_to_check = [
    {"id": 501, "name": "Ligue 1"},
    {"id": 8, "name": "Premier League"},
    {"id": 564, "name": "La Liga"},  
    {"id": 384, "name": "Serie A"},
    {"id": 9, "name": "Bundesliga"}
]

for league in leagues_to_check:
    print(f"\n=== {league['name']} (ID: {league['id']}) ===")
    
    # Récupérer les saisons de cette ligue
    seasons = make_request(f"seasons", {"filters": f"leagues:{league['id']}"})
    
    if seasons:
        print(f"Found {len(seasons)} seasons")
        # Trier par date de fin décroissante pour avoir la plus récente en premier
        seasons.sort(key=lambda x: x.get('ending_at', ''), reverse=True)
        
        for i, season in enumerate(seasons[:3]):  # Top 3 saisons les plus récentes
            print(f"{i+1}. Season ID: {season['id']}, Name: {season['name']}, Ending: {season.get('ending_at', 'N/A')}")
    else:
        print("No seasons found")