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

print("RECHERCHE DES TYPES MANQUANTS POUR RULLI")
print("=" * 80)

# Types importants à vérifier
important_types = {
    113: "Penalties Saved",
    194: "Cleansheets", 
    195: "Goalkeeper Cleansheets",
    321: "Appearances",
    322: "Lineups",
    119: "Minutes Played",
    57: "Saves",
    88: "Goals Conceded",
}

player_id = 186418
season_id = 23643  # 2024/2025

print(f"\nAnalyse saison 2024/2025 (où Rulli a 5 clean sheets):")
print("-" * 60)

url = f"{BASE_URL}/statistics/seasons/players/{player_id}"
params = {"seasons": season_id}
response = requests.get(url, headers=headers, params=params)

if response.status_code == 200:
    data = response.json()
    
    for item in data.get("data", []):
        if item.get("season_id") == season_id and item.get("has_values"):
            
            # Récupérer tous les type_id présents
            present_types = set()
            if "details" in item:
                for detail in item["details"]:
                    present_types.add(detail.get("type_id"))
            
            print(f"\n✅ Types présents dans les données:")
            for type_id in sorted(present_types):
                if type_id in important_types:
                    print(f"  Type {type_id}: {important_types[type_id]}")
            
            print(f"\n❌ Types MANQUANTS (non retournés par l'API):")
            for type_id, name in important_types.items():
                if type_id not in present_types:
                    print(f"  Type {type_id}: {name}")
            
            print(f"\nNombre total de types retournés: {len(present_types)}")

print("\n" + "=" * 80)
print("CONCLUSION:")
print("-" * 60)
print("Si des types importants sont manquants (comme cleansheets ou penalties-saved),")
print("cela signifie probablement que l'API ne retourne que les stats non-nulles.")
print("\nPour avoir TOUTES les stats, il faudrait peut-être utiliser un autre endpoint")
print("ou un paramètre 'include' spécifique dans la requête.")