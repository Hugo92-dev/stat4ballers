import requests
import json

API_KEY = "j28l04KZC0LGFAdbxIzdyb8zz253K1YegT5vEUN5taw0dxuNr6U3jtRMmS6C"
BASE_URL = "https://api.sportmonks.com/v3/football"

print("=" * 60)
print("DEBUG STRUCTURE API SPORTMONKS")
print("=" * 60)

# 1. Chercher toutes les ligues
print("\n1. TOUTES LES LIGUES FRANCAISES")
url = f"{BASE_URL}/leagues"
params = {
    'api_token': API_KEY,
    'per_page': 100
}

ligue1_id = None
try:
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if 'data' in data:
            for league in data['data']:
                if league.get('country_id') == 17:  # France
                    name = league.get('name', '')
                    if 'Ligue 1' in name or 'France' in name:
                        print(f"  - {name} (ID: {league['id']})")
                        if 'Ligue 1' in name and not 'Women' in name:
                            ligue1_id = league['id']
except Exception as e:
    print(f"Erreur: {e}")

# 2. Si on a trouvé la Ligue 1, chercher la saison actuelle
if ligue1_id:
    print(f"\n2. DETAILS LIGUE 1 (ID: {ligue1_id})")
    url = f"{BASE_URL}/leagues/{ligue1_id}"
    params = {
        'api_token': API_KEY,
        'include': 'currentSeason,seasons'
    }
    
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            if 'data' in data:
                league = data['data']
                print(f"Nom: {league.get('name', 'N/A')}")
                
                # Saison actuelle
                if 'currentSeason' in league and league['currentSeason']:
                    season = league['currentSeason']
                    print(f"\nSaison actuelle:")
                    print(f"  - Nom: {season.get('name', 'N/A')}")
                    print(f"  - ID: {season.get('id', 'N/A')}")
                    print(f"  - Début: {season.get('starting_at', 'N/A')}")
                    print(f"  - Fin: {season.get('ending_at', 'N/A')}")
                    current_season_id = season.get('id')
                
                # Toutes les saisons
                if 'seasons' in league and league['seasons']:
                    print(f"\nDernières saisons:")
                    for s in league['seasons'][-5:]:
                        print(f"  - {s.get('name', 'N/A')} (ID: {s.get('id', 'N/A')}) | Current: {s.get('is_current', False)}")
    except Exception as e:
        print(f"Erreur: {e}")

# 3. Tester directement avec l'ID de saison connu
print("\n3. TEST AVEC SEASON ID CONNU (2024/2025)")

# IDs de saisons possibles pour 2024/2025
possible_seasons = [23148, 23639, 25651, 21638]

for season_id in possible_seasons:
    print(f"\nTest saison {season_id}:")
    
    # Essayer de récupérer l'effectif de Nantes
    url = f"{BASE_URL}/squads/seasons/{season_id}/teams/59"
    params = {
        'api_token': API_KEY,
        'include': 'player'
    }
    
    try:
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            if 'data' in data and isinstance(data['data'], list):
                print(f"  SUCCESS: {len(data['data'])} joueurs pour Nantes")
                if data['data']:
                    player_data = data['data'][0]
                    if 'player' in player_data and player_data['player']:
                        name = player_data['player'].get('common_name', 'Unknown')
                        print(f"  Premier joueur: {name}")
            else:
                print(f"  Pas de données")
        else:
            print(f"  Erreur {response.status_code}")
    except Exception as e:
        print(f"  Exception: {e}")

# 4. Essayer un endpoint fixtures pour voir les joueurs actuels
print("\n4. FIXTURES RECENTS DE NANTES")
url = f"{BASE_URL}/fixtures"
params = {
    'api_token': API_KEY,
    'filters': 'teamId:59',
    'include': 'lineups.player',
    'per_page': 1
}

try:
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if 'data' in data and data['data']:
            fixture = data['data'][0]
            print(f"Match: {fixture.get('name', 'N/A')}")
            
            if 'lineups' in fixture and fixture['lineups']:
                print("Joueurs dans le lineup:")
                for lineup in fixture['lineups'][:5]:
                    if 'player' in lineup and lineup['player']:
                        print(f"  - {lineup['player'].get('common_name', 'Unknown')}")
except Exception as e:
    print(f"Erreur: {e}")