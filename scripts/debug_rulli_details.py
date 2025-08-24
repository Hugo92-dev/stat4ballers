import requests
import json
import sys

# Fix pour l'encodage UTF-8 sur Windows
sys.stdout.reconfigure(encoding='utf-8')

API_KEY = "leBzDfKbRE5k9zEg3FuZE3Hh7XbukODNarOXLoVtPAiAtliDZ19wLu1Wnzi2"
BASE_URL = "https://api.sportmonks.com/v3/football"

headers = {
    "Accept": "application/json",
    "Authorization": API_KEY,
}

print("DEBUG DÉTAILLÉ: Stats de Rulli saison 2025/2026")
print("=" * 80)

player_id = 186418
season_id = 25651

url = f"{BASE_URL}/statistics/seasons/players/{player_id}"
params = {"seasons": season_id}
response = requests.get(url, headers=headers, params=params)

if response.status_code == 200:
    data = response.json()
    
    # Trouver les données de la saison 25651
    for item in data["data"]:
        if item.get("season_id") == season_id:
            print(f"\nSaison trouvée: {season_id}")
            print(f"has_values: {item.get('has_values')}")
            print(f"team_id: {item.get('team_id')}")
            print(f"jersey_number: {item.get('jersey_number')}")
            
            if "details" in item and len(item["details"]) > 0:
                detail = item["details"][0]
                print(f"\nContenu de details[0]:")
                print(json.dumps(detail, indent=2, ensure_ascii=False))
            else:
                print("\nPas de details dans cette entrée")
                
print("\n" + "=" * 80)
print("Même test pour 2024/2025 (ID: 23643):")

season_id = 23643
params = {"seasons": season_id}
response = requests.get(url, headers=headers, params=params)

if response.status_code == 200:
    data = response.json()
    
    for item in data["data"]:
        if item.get("season_id") == season_id:
            print(f"\nSaison trouvée: {season_id}")
            print(f"has_values: {item.get('has_values')}")
            
            if "details" in item and len(item["details"]) > 0:
                detail = item["details"][0]
                print(f"\nStats clés:")
                print(f"  - Minutes: {detail.get('minutes')}")
                print(f"  - Matchs: {detail.get('games', {}).get('appearences')}")
                print(f"  - Buts encaissés: {detail.get('goalkeeper', {}).get('goals_conceded')}")
                print(f"  - Clean sheets: {detail.get('goalkeeper', {}).get('cleansheets')}")
                print(f"  - Arrêts: {detail.get('goalkeeper', {}).get('saves')}")