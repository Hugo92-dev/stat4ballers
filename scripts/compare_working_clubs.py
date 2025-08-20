import requests
import json
import sys

# Forcer l'encodage UTF-8 pour Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'replace')

API_KEY = "j28l04KZC0LGFAdbxIzdyb8zz253K1YegT5vEUN5taw0dxuNr6U3jtRMmS6C"
BASE_URL = "https://api.sportmonks.com/v3/football"

print("=" * 60)
print("COMPARAISON DES CLUBS QUI FONCTIONNENT VS CEUX QUI NE FONCTIONNENT PAS")
print("=" * 60)

# Les 4 clubs qui fonctionnent selon l'historique
working_clubs = [
    {'id': 591, 'name': 'PSG'},
    {'id': 44, 'name': 'Marseille'},
    {'id': 79, 'name': 'Lyon'},
    {'id': 6789, 'name': 'Monaco'}
]

# Les clubs problématiques
problem_clubs = [
    {'id': 59, 'name': 'Nantes'},
    {'id': 266, 'name': 'Brest'},
    {'id': 271, 'name': 'Lens'},
    {'id': 690, 'name': 'Lille'}
]

def test_all_endpoints(team_id, team_name):
    """Tester tous les endpoints possibles pour un club"""
    print(f"\n{'='*40}")
    print(f"{team_name} (ID: {team_id})")
    print(f"{'='*40}")
    
    results = {}
    
    # 1. Endpoint simple /squads/teams/{id}
    print("\n1. /squads/teams/{id}:")
    url = f"{BASE_URL}/squads/teams/{team_id}"
    params = {'api_token': API_KEY, 'include': 'player'}
    
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            if 'data' in data and isinstance(data['data'], list):
                squad = data['data']
                print(f"   ✓ {len(squad)} joueurs")
                if squad and 'player' in squad[0]:
                    player = squad[0]['player']
                    print(f"   Premier: {player.get('common_name', 'Unknown')}")
                    results['simple'] = len(squad)
            else:
                print(f"   ✗ Pas de données")
                results['simple'] = 0
        else:
            print(f"   ✗ Erreur {response.status_code}")
            results['simple'] = 0
    except Exception as e:
        print(f"   ✗ Exception: {e}")
        results['simple'] = 0
    
    # 2. Avec saison 25651 (celle qui marchait pour Nantes)
    print("\n2. /squads/seasons/25651/teams/{id}:")
    url = f"{BASE_URL}/squads/seasons/25651/teams/{team_id}"
    
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            if 'data' in data and isinstance(data['data'], list):
                squad = data['data']
                print(f"   ✓ {len(squad)} joueurs")
                if squad and 'player' in squad[0]:
                    player = squad[0]['player']
                    print(f"   Premier: {player.get('common_name', 'Unknown')}")
                    results['season_25651'] = len(squad)
            else:
                print(f"   ✗ Pas de données")
                results['season_25651'] = 0
        else:
            print(f"   ✗ Erreur {response.status_code}")
            results['season_25651'] = 0
    except Exception as e:
        print(f"   ✗ Exception: {e}")
        results['season_25651'] = 0
    
    # 3. Avec saison 23639
    print("\n3. /squads/seasons/23639/teams/{id}:")
    url = f"{BASE_URL}/squads/seasons/23639/teams/{team_id}"
    
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            if 'data' in data and isinstance(data['data'], list):
                squad = data['data']
                print(f"   ✓ {len(squad)} joueurs")
                results['season_23639'] = len(squad)
            else:
                print(f"   ✗ Pas de données")
                results['season_23639'] = 0
        else:
            print(f"   ✗ Erreur {response.status_code}")
            results['season_23639'] = 0
    except Exception as e:
        print(f"   ✗ Exception: {e}")
        results['season_23639'] = 0
    
    return results

# Tester les clubs qui fonctionnent
print("\n\n[OK] CLUBS QUI FONCTIONNENT BIEN:")
for club in working_clubs:
    test_all_endpoints(club['id'], club['name'])

# Tester les clubs problématiques
print("\n\n[PROBLEME] CLUBS PROBLEMATIQUES:")
for club in problem_clubs:
    test_all_endpoints(club['id'], club['name'])

print("\n" + "=" * 60)
print("RECHERCHE D'IDS ALTERNATIFS")
print("=" * 60)

# Rechercher des IDs alternatifs pour les clubs problématiques
for club in problem_clubs:
    print(f"\nRecherche pour '{club['name']}':")
    url = f"{BASE_URL}/teams/search/{club['name']}"
    params = {'api_token': API_KEY}
    
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            if 'data' in data:
                for team in data['data'][:3]:
                    if team.get('country_id') == 17:  # France
                        print(f"  ID: {team['id']} | {team['name']} | Last: {team.get('last_played_at', 'N/A')[:10]}")
    except:
        pass