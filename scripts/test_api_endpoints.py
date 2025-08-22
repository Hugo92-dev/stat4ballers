import requests
import json

API_KEY = 'leBzDfKbRE5k9zEg3FuZE3Hh7XbukODNarOXLoVtPAiAtliDZ19wLu1Wnzi2'
BASE_URL = 'https://api.sportmonks.com/v3/football'

headers = {
    'Authorization': f'{API_KEY}',
    'Accept': 'application/json'
}

# ID de Rulli
player_id = 186418

print("Test des différents endpoints pour Rulli (ID: 186418)")
print("=" * 60)

# 1. Essayer avec l'endpoint player direct
print("\n1. Endpoint /players/{id}")
url = f'{BASE_URL}/players/{player_id}'
response = requests.get(url, headers=headers)
print(f"URL: {url}")
print(f"Status: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"Player: {data['data'].get('display_name')}")
    print(f"Position: {data['data'].get('position_id')}")

# 2. Essayer avec includes statistics
print("\n2. Endpoint /players/{id}?include=statistics")
url = f'{BASE_URL}/players/{player_id}?include=statistics'
response = requests.get(url, headers=headers)
print(f"URL: {url}")
print(f"Status: {response.status_code}")
if response.status_code == 200:
    with open('rulli_stats.json', 'w', encoding='utf-8') as f:
        json.dump(response.json(), f, indent=2, ensure_ascii=False)
    print("Données sauvegardées dans rulli_stats.json")
    
    data = response.json()
    stats = data['data'].get('statistics', [])
    print(f"Nombre de saisons trouvées: {len(stats)}")
    
    # Afficher les saisons disponibles
    if stats:
        print("\nSaisons disponibles:")
        for stat in stats[:5]:  # Afficher les 5 premières
            print(f"  - Season ID: {stat.get('season_id')}")
            has_values = stat.get('has_values', False)
            print(f"    Has values: {has_values}")
            if has_values:
                details = stat.get('details', [])
                if details:
                    print(f"    Details available: {len(details)} entries")

# 3. Essayer avec l'endpoint team/players pour l'OM
print("\n3. Endpoint /teams/85/players (OM)")
url = f'{BASE_URL}/teams/85/players?include=player.statistics'
response = requests.get(url, headers=headers)
print(f"URL: {url}")
print(f"Status: {response.status_code}")

# 4. Essayer l'endpoint seasons/teams pour obtenir les stats de l'équipe
print("\n4. Endpoint /seasons/21646/teams/85 (OM saison 2024/25)")
url = f'{BASE_URL}/seasons/21646/teams/85?include=statistics'
response = requests.get(url, headers=headers)
print(f"URL: {url}")
print(f"Status: {response.status_code}")