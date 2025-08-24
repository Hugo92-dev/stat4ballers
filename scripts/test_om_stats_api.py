import requests
import json
from dotenv import load_dotenv
import os
import sys

# Fix pour l'encodage UTF-8 sur Windows
sys.stdout.reconfigure(encoding='utf-8')

# Charger les variables d'environnement
load_dotenv('../.env.local')
API_KEY = os.getenv('SPORTMONKS_API_TOKEN')

if not API_KEY:
    print("Cle API manquante")
    exit(1)

BASE_URL = "https://api.sportmonks.com/v3/football"

# Test 1: Vérifier l'équipe OM
print("=== TEST 1: Verifier l'equipe OM ===")
url = f"{BASE_URL}/teams/44"
params = {'api_token': API_KEY}
response = requests.get(url, params=params)
print(f"Status: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    if 'data' in data:
        team = data['data']
        print(f"Equipe: {team.get('name')} (ID: {team.get('id')})")

print("\n=== TEST 2: Stats equipe pour saison actuelle ===")
# Essayer avec la saison 2024/2025
season_id = 21792
url = f"{BASE_URL}/squads/seasons/{season_id}/teams/44"
params = {
    'api_token': API_KEY,
    'include': 'player;details.type'
}
response = requests.get(url, params=params)
print(f"URL: {url}")
print(f"Status: {response.status_code}")

if response.status_code == 200:
    data = response.json()
    print(f"Structure de la reponse: {data.keys()}")
    if 'data' in data:
        squad = data['data']
        print(f"Nombre de joueurs: {len(squad) if isinstance(squad, list) else 'Pas une liste'}")
        if squad and len(squad) > 0:
            print("\nPremier joueur:")
            print(json.dumps(squad[0], indent=2))
else:
    print(f"Erreur: {response.text[:500]}")

print("\n=== TEST 3: Stats d'un joueur specifique (Aubameyang ID: 20333643) ===")
player_id = 20333643
url = f"{BASE_URL}/statistics/seasons/players/{player_id}"
params = {
    'api_token': API_KEY,
    'include': 'details.type'
}
response = requests.get(url, params=params)
print(f"URL: {url}")
print(f"Status: {response.status_code}")

if response.status_code == 200:
    data = response.json()
    print(f"Structure de la reponse: {data.keys()}")
    if 'data' in data:
        stats = data['data']
        print(f"Nombre de saisons: {len(stats) if isinstance(stats, list) else 'Pas une liste'}")
        if stats and len(stats) > 0:
            print("\nPremiere saison:")
            print(json.dumps(stats[0], indent=2)[:1000])
else:
    print(f"Erreur: {response.text[:500]}")