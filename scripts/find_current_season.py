import requests
import json
from datetime import datetime

API_KEY = "j28l04KZC0LGFAdbxIzdyb8zz253K1YegT5vEUN5taw0dxuNr6U3jtRMmS6C"
BASE_URL = "https://api.sportmonks.com/v3/football"

print("=" * 60)
print("RECHERCHE DE LA SAISON ACTUELLE LIGUE 1")
print("=" * 60)

# 1. Chercher la ligue Ligue 1
print("\n1. RECHERCHE DE LA LIGUE 1")
url = f"{BASE_URL}/leagues"
params = {
    'api_token': API_KEY,
    'filters': 'countryId:17',  # France
    'include': 'currentSeason'
}

try:
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if 'data' in data:
            for league in data['data']:
                if 'Ligue 1' in league.get('name', ''):
                    print(f"\nTrouvé: {league['name']}")
                    print(f"ID: {league['id']}")
                    if 'currentSeason' in league and league['currentSeason']:
                        season = league['currentSeason']
                        print(f"Saison actuelle: {season.get('name', 'N/A')}")
                        print(f"Season ID: {season.get('id', 'N/A')}")
                        current_season_id = season.get('id')
except Exception as e:
    print(f"Erreur: {e}")

# 2. Essayer de récupérer les équipes de la saison actuelle
print("\n2. EQUIPES DE LA SAISON ACTUELLE")
if 'current_season_id' in locals():
    url = f"{BASE_URL}/seasons/{current_season_id}/teams"
    params = {'api_token': API_KEY}
    
    try:
        response = requests.get(url, params=params)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            if 'data' in data:
                teams = data['data']
                print(f"Équipes trouvées: {len(teams)}")
                
                # Afficher quelques équipes
                print("\nÉquipes de Ligue 1:")
                for team in teams[:5]:
                    print(f"  - {team.get('name', 'N/A')} (ID: {team.get('id', 'N/A')})")
    except Exception as e:
        print(f"Erreur: {e}")

# 3. Tester l'effectif avec la saison actuelle
print("\n3. TEST EFFECTIF AVEC SAISON ACTUELLE")

test_teams = [
    {'id': 59, 'name': 'Nantes'},
    {'id': 266, 'name': 'Brest'},
    {'id': 591, 'name': 'PSG'}
]

if 'current_season_id' in locals():
    for team in test_teams:
        print(f"\n{team['name']}:")
        
        # Essayer /squads/seasons/{season_id}/teams/{team_id}
        url = f"{BASE_URL}/squads/seasons/{current_season_id}/teams/{team['id']}"
        params = {
            'api_token': API_KEY,
            'include': 'player'
        }
        
        try:
            response = requests.get(url, params=params)
            print(f"  Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                if 'data' in data:
                    squad = data['data']
                    print(f"  Joueurs: {len(squad)}")
                    
                    if squad and len(squad) > 0:
                        # Afficher 3 joueurs
                        print("  Exemples:")
                        for player_data in squad[:3]:
                            if 'player' in player_data and player_data['player']:
                                player = player_data['player']
                                name = player.get('common_name', player.get('display_name', 'Unknown'))
                                print(f"    - {name}")
                else:
                    # Essayer de comprendre la structure de la réponse
                    print(f"  Réponse: {json.dumps(data, indent=2)[:300]}")
        except Exception as e:
            print(f"  Erreur: {e}")

# 4. Chercher d'autres endpoints possibles
print("\n4. AUTRES ENDPOINTS POSSIBLES")

# Essayer transfers pour voir les joueurs actuels
print("\nTransferts récents de Nantes:")
url = f"{BASE_URL}/transfers"
params = {
    'api_token': API_KEY,
    'filters': 'teamIn:59',
    'include': 'player',
    'per_page': 5
}

try:
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if 'data' in data:
            print(f"Transferts trouvés: {len(data['data'])}")
            for transfer in data['data'][:3]:
                if 'player' in transfer and transfer['player']:
                    print(f"  - {transfer['player'].get('common_name', 'Unknown')} (Date: {transfer.get('date', 'N/A')})")
except Exception as e:
    print(f"Erreur: {e}")