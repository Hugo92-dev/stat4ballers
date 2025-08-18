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

# Chercher toutes les saisons récentes (2023-2024, 2024-2025)
print("Searching for current seasons...")

# Essayer de récupérer toutes les saisons et filtrer par nom
seasons = make_request("seasons")

print(f"Total seasons found: {len(seasons)}")

# Filtrer les saisons 2024-2025 et 2023-2024
current_seasons = []
for season in seasons:
    season_name = season.get('name', '')
    if '2024' in season_name or '2023' in season_name:
        current_seasons.append(season)

print(f"Current seasons (2023/2024): {len(current_seasons)}")

# Grouper par ligue
leagues_dict = {}
for season in current_seasons:
    season_id = season['id']
    season_name = season['name']
    
    # Récupérer les détails de la saison avec les ligues
    season_details = make_request(f"seasons/{season_id}", {"include": "league"})
    
    if season_details and 'league' in season_details:
        league = season_details['league']
        league_name = league['name']
        league_id = league['id']
        
        if league_name not in leagues_dict:
            leagues_dict[league_name] = []
        
        leagues_dict[league_name].append({
            'season_id': season_id,
            'season_name': season_name,
            'league_id': league_id
        })

# Afficher les ligues principales
target_leagues = ["Ligue 1", "Premier League", "La Liga", "Serie A", "Bundesliga"]
for league_name in target_leagues:
    print(f"\n=== {league_name} ===")
    if league_name in leagues_dict:
        for season_info in leagues_dict[league_name]:
            print(f"Season: {season_info['season_name']}, ID: {season_info['season_id']}, League ID: {season_info['league_id']}")
    else:
        print("No current season found")

print("\nAll leagues with current seasons:")
for league_name, seasons in leagues_dict.items():
    if len(seasons) > 0:
        print(f"{league_name}: {seasons[0]['season_name']} (Season ID: {seasons[0]['season_id']}, League ID: {seasons[0]['league_id']})")