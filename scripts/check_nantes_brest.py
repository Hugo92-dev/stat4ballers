import requests
import json
import sys

# Forcer l'encodage UTF-8 pour Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'replace')

API_KEY = "j28l04KZC0LGFAdbxIzdyb8zz253K1YegT5vEUN5taw0dxuNr6U3jtRMmS6C"
BASE_URL = "https://api.sportmonks.com/v3/football"

def test_endpoint(endpoint, params=None):
    """Tester un endpoint de l'API"""
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
                print(f"  SUCCESS: {len(data['data'])} items")
                if data['data'] and len(data['data']) > 0:
                    # Afficher le premier joueur pour vérification
                    first = data['data'][0]
                    if 'player' in first and first['player']:
                        player = first['player']
                        name = player.get('common_name', player.get('display_name', 'Unknown'))
                        print(f"  Premier joueur: {name}")
                        print(f"  Date de début: {first.get('start', 'N/A')}")
            else:
                print(f"  SUCCESS: Got data")
        else:
            print(f"  WARNING: No 'data' key in response")
            
        return data
    except requests.exceptions.RequestException as e:
        print(f"  ERROR: {e}")
        return None

print("=" * 60)
print("VERIFICATION NANTES ET BREST")
print("=" * 60)

# IDs trouvés précédemment
teams_to_check = [
    {'id': 59, 'name': 'FC Nantes', 'correct_id': None},
    {'id': 266, 'name': 'Stade Brestois', 'correct_id': None}
]

print("\n1. RECHERCHE DES VRAIS IDs")
print("-" * 40)

# Rechercher Nantes
print("\nRecherche 'Nantes':")
url = f"{BASE_URL}/teams/search/nantes"
params = {'api_token': API_KEY}
response = requests.get(url, params=params)
if response.status_code == 200:
    data = response.json()
    if 'data' in data:
        for team in data['data'][:5]:
            if team.get('country_id') == 17:  # France
                last_played = team.get('last_played_at', 'N/A')
                if last_played != 'N/A':
                    last_played = last_played[:10]
                print(f"  ID: {team['id']} | {team['name']} | Founded: {team.get('founded', '?')} | Last: {last_played}")

# Rechercher Brest
print("\nRecherche 'Brest':")
url = f"{BASE_URL}/teams/search/brest"
response = requests.get(url, params=params)
if response.status_code == 200:
    data = response.json()
    if 'data' in data:
        for team in data['data'][:5]:
            if team.get('country_id') == 17:  # France
                last_played = team.get('last_played_at', 'N/A')
                if last_played != 'N/A':
                    last_played = last_played[:10]
                print(f"  ID: {team['id']} | {team['name']} | Founded: {team.get('founded', '?')} | Last: {last_played}")

print("\n2. TEST DES ENDPOINTS SQUAD")
print("-" * 40)

# Tester différents endpoints pour Nantes (ID: 59)
print("\n[NANTES - ID: 59]")
test_endpoint("/squads/teams/59", {'include': 'player'})

# Tester différents endpoints pour Brest (ID: 266)
print("\n[BREST - ID: 266]")
test_endpoint("/squads/teams/266", {'include': 'player'})

print("\n3. TEST AVEC SAISON ACTUELLE")
print("-" * 40)

# Tester avec la saison 2024/2025
season_ids = [23639, 25651, 23148]  # Différentes saisons possibles

for season_id in season_ids:
    print(f"\n[Test avec season_id: {season_id}]")
    
    # Nantes
    print(f"Nantes avec saison {season_id}:")
    test_endpoint(f"/squads/seasons/{season_id}/teams/59", {'include': 'player'})
    
    # Brest
    print(f"Brest avec saison {season_id}:")
    test_endpoint(f"/squads/seasons/{season_id}/teams/266", {'include': 'player'})

print("\n4. TEST ENDPOINT TEAMS AVEC SQUAD INCLUDE")
print("-" * 40)

# Essayer un autre format d'include
print("\n[Nantes - teams endpoint avec squad]")
test_endpoint("/teams/59", {'include': 'squad.player'})

print("\n[Brest - teams endpoint avec squad]")
test_endpoint("/teams/266", {'include': 'squad.player'})