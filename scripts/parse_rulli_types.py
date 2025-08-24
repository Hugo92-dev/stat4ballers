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

# Mapping connu des type_id (à compléter)
TYPE_MAPPING = {
    57: "Arrêts (saves)",
    84: "Buts encaissés",
    85: "Clean sheets",
    # À découvrir...
}

print("ANALYSE COMPLÈTE: Tous les type_id de Rulli")
print("=" * 80)

player_id = 186418

# Pour la saison 2025/2026
season_id = 25651
print(f"\n📊 Saison 2025/2026 (ID: {season_id}):")

url = f"{BASE_URL}/statistics/seasons/players/{player_id}"
params = {"seasons": season_id}
response = requests.get(url, headers=headers, params=params)

if response.status_code == 200:
    data = response.json()
    
    for item in data["data"]:
        if item.get("season_id") == season_id and item.get("has_values"):
            print(f"  Matchs trouvés pour équipe ID: {item.get('team_id')}")
            
            if "details" in item and len(item["details"]) > 0:
                print(f"  Nombre de stats: {len(item['details'])}")
                
                # Analyser chaque stat
                stats_dict = {}
                for detail in item["details"]:
                    type_id = detail.get("type_id")
                    value = detail.get("value", {})
                    
                    # Extraire la valeur (peut être dans 'total', 'goals', etc.)
                    if isinstance(value, dict):
                        if "total" in value:
                            final_value = value["total"]
                        elif "goals" in value:
                            final_value = value["goals"]
                        elif "average" in value:
                            final_value = value["average"]
                        else:
                            final_value = value
                    else:
                        final_value = value
                    
                    stats_dict[type_id] = final_value
                    
                    # Afficher avec le nom si connu
                    name = TYPE_MAPPING.get(type_id, f"Type_{type_id}")
                    print(f"    - {name}: {final_value}")
                
                # Stats importantes pour un gardien
                print(f"\n  📈 Stats clés gardien:")
                print(f"    - Arrêts (type 57): {stats_dict.get(57, 'N/A')}")
                print(f"    - Buts encaissés (type 84): {stats_dict.get(84, 'N/A')}")
                print(f"    - Clean sheets (type 85): {stats_dict.get(85, 'N/A')}")
                print(f"    - Minutes (type ?): {stats_dict.get(79, 'N/A')}")
                print(f"    - Matchs (type ?): {stats_dict.get(115, 'N/A')}")

# Pour la saison 2024/2025
season_id = 23643
print(f"\n📊 Saison 2024/2025 (ID: {season_id}):")

params = {"seasons": season_id}
response = requests.get(url, headers=headers, params=params)

if response.status_code == 200:
    data = response.json()
    
    for item in data["data"]:
        if item.get("season_id") == season_id and item.get("has_values"):
            
            if "details" in item and len(item["details"]) > 0:
                print(f"  Nombre de stats: {len(item['details'])}")
                
                # Analyser les 10 premières stats
                for i, detail in enumerate(item["details"][:10]):
                    type_id = detail.get("type_id")
                    value = detail.get("value", {})
                    
                    if isinstance(value, dict):
                        if "total" in value:
                            final_value = value["total"]
                        else:
                            final_value = str(value)
                    else:
                        final_value = value
                    
                    print(f"    - Type {type_id}: {final_value}")