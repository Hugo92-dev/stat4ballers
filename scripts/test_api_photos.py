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
HEADERS = {
    'Authorization': API_KEY  # Sans Bearer
}

# Tester avec l'ID d'un joueur connu
test_player_id = 186418  # Geronimo Rulli

print(f"Test 1: Recuperation directe du joueur {test_player_id}")
url = f"{BASE_URL}/players/{test_player_id}"
params = {'api_token': API_KEY}  # Passer le token en paramètre
response = requests.get(url, params=params)
print(f"Status code: {response.status_code}")

if response.status_code == 200:
    data = response.json()
    if 'data' in data:
        player = data['data']
        print(f"Nom: {player.get('name')}")
        print(f"Image path: {player.get('image_path')}")
        print("Structure complete du joueur:")
        print(json.dumps(player, indent=2))
else:
    print(f"Erreur: {response.text}")

print("\n" + "="*50 + "\n")

# Essayer de récupérer un joueur de l'OM via l'équipe
print("Test 2: Recuperation via l'equipe")

# ID de l'OM
om_id = 44

# Essayer de récupérer l'équipe avec les joueurs
url = f"{BASE_URL}/teams/{om_id}"
params = {'api_token': API_KEY, 'include': 'squad.player'}
response = requests.get(url, params=params)
print(f"Status code: {response.status_code}")

if response.status_code == 200:
    data = response.json()
    if 'data' in data and 'squad' in data['data']:
        squad = data['data']['squad']
        print(f"Nombre de joueurs dans l'effectif: {len(squad)}")
        if squad:
            first_player = squad[0]
            if 'player' in first_player:
                player = first_player['player']
                print(f"Premier joueur: {player.get('name')}")
                print(f"Image path: {player.get('image_path')}")
else:
    print(f"Erreur: {response.text}")