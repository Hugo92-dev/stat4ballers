import requests
import json
import sys

# Fix pour l'encodage UTF-8 sur Windows
sys.stdout.reconfigure(encoding='utf-8')

# NOUVELLE API KEY
API_KEY = "leBzDfKbRE5k9zEg3FuZE3Hh7XbukODNarOXLoVtPAiAtliDZ19wLu1Wnzi2"
BASE_URL = "https://api.sportmonks.com/v3/football"

headers = {
    "Accept": "application/json",
    "Authorization": API_KEY,
}

print("DEBUG: Test de récupération des stats de Rulli")
print("=" * 80)

# Test 1: Info du joueur
player_id = 186418
print(f"\n1. Informations du joueur (ID: {player_id}):")
url = f"{BASE_URL}/players/{player_id}"
response = requests.get(url, headers=headers)
if response.status_code == 200:
    data = response.json()
    if data and "data" in data:
        player = data["data"]
        print(f"   Nom: {player.get('display_name')}")
        print(f"   Position: {player.get('detailed_position', {}).get('name')}")
        print(f"   Équipe ID: {player.get('team_id')}")
else:
    print(f"   Erreur {response.status_code}: {response.text[:100]}")

# Test 2: Stats pour la saison 2025/2026
print(f"\n2. Stats saison 2025/2026 (ID: 25651):")
url = f"{BASE_URL}/statistics/seasons/players/{player_id}"
params = {"seasons": 25651}
response = requests.get(url, headers=headers, params=params)

if response.status_code == 200:
    data = response.json()
    print(f"   Réponse brute (500 premiers caractères):")
    print(json.dumps(data, indent=2, ensure_ascii=False)[:500])
    
    if data and "data" in data and len(data["data"]) > 0:
        stats = data["data"][0]
        print(f"\n   Structure des données:")
        print(f"   Clés disponibles: {list(stats.keys())}")
        
        # Afficher quelques valeurs
        print(f"\n   Valeurs trouvées:")
        print(f"   - minutes: {stats.get('minutes')}")
        print(f"   - games: {stats.get('games')}")
        print(f"   - goalkeeper: {stats.get('goalkeeper')}")
else:
    print(f"   Erreur {response.status_code}: {response.text[:200]}")

# Test 3: Essai avec un autre endpoint
print(f"\n3. Test avec endpoint /players/{player_id}/statistics:")
url = f"{BASE_URL}/players/{player_id}/statistics"
params = {"filters": "seasons:25651"}
response = requests.get(url, headers=headers, params=params)

if response.status_code == 200:
    data = response.json()
    print(f"   Réponse: {json.dumps(data, indent=2, ensure_ascii=False)[:500]}")
else:
    print(f"   Erreur {response.status_code}: {response.text[:200]}")