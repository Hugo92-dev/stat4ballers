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

# Charger le mapping des types
with open('sportmonks_types_mapping.json', 'r', encoding='utf-8') as f:
    TYPE_MAPPING = json.load(f)

print("ANALYSE COMPLÈTE DE TOUS LES TYPE_ID DE RULLI")
print("=" * 80)

player_id = 186418

# Pour chaque saison, afficher TOUS les type_id et leurs valeurs
seasons = {
    "2025/2026": 25651,
    "2024/2025": 23643,
}

for season_name, season_id in seasons.items():
    print(f"\n📊 Saison {season_name} (ID: {season_id}):")
    print("-" * 60)
    
    url = f"{BASE_URL}/statistics/seasons/players/{player_id}"
    params = {"seasons": season_id}
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        data = response.json()
        
        for item in data.get("data", []):
            if item.get("season_id") == season_id and item.get("has_values"):
                
                if "details" in item and len(item["details"]) > 0:
                    # Organiser par catégorie
                    stats_by_group = {}
                    
                    for detail in item["details"]:
                        type_id = str(detail.get("type_id"))
                        value = detail.get("value", {})
                        
                        # Extraire la valeur
                        if isinstance(value, dict):
                            if "total" in value:
                                final_value = value["total"]
                            elif "goals" in value:
                                final_value = value["goals"]
                            elif "average" in value:
                                final_value = value["average"]
                            elif "percentage" in value:
                                final_value = value["percentage"]
                            else:
                                final_value = str(value)
                        else:
                            final_value = value
                        
                        # Obtenir les infos du type
                        if type_id in TYPE_MAPPING:
                            type_info = TYPE_MAPPING[type_id]
                            name = type_info["name"]
                            code = type_info["code"]
                            group = type_info.get("stat_group", "other")
                            
                            if group not in stats_by_group:
                                stats_by_group[group] = []
                            
                            stats_by_group[group].append({
                                "id": type_id,
                                "name": name,
                                "code": code,
                                "value": final_value
                            })
                        else:
                            if "unknown" not in stats_by_group:
                                stats_by_group["unknown"] = []
                            stats_by_group["unknown"].append({
                                "id": type_id,
                                "name": f"Unknown_{type_id}",
                                "code": f"unknown_{type_id}",
                                "value": final_value
                            })
                    
                    # Afficher par groupe
                    for group in ["overall", "offensive", "defensive", "other", "unknown"]:
                        if group in stats_by_group:
                            print(f"\n  {group.upper()}:")
                            for stat in sorted(stats_by_group[group], key=lambda x: x["name"]):
                                print(f"    {stat['id']:4} | {stat['name']:30} | {stat['code']:25} | {stat['value']}")
                    
                    # Chercher spécifiquement les penalties
                    print(f"\n  🎯 RECHERCHE PENALTIES:")
                    for detail in item["details"]:
                        type_id = str(detail.get("type_id"))
                        if type_id in TYPE_MAPPING:
                            type_info = TYPE_MAPPING[type_id]
                            if "penalt" in type_info["name"].lower() or "penalt" in type_info["code"].lower():
                                value = detail.get("value", {})
                                if isinstance(value, dict):
                                    final_value = value.get("total", value.get("goals", value))
                                else:
                                    final_value = value
                                print(f"    Type {type_id}: {type_info['name']} ({type_info['code']}) = {final_value}")

print("\n" + "=" * 80)
print("VÉRIFICATION: Y a-t-il un type pour 'penalties saved' ou 'penalties arrêtés' ?")
print("-" * 60)

# Chercher dans tout le mapping
penalty_types = []
for type_id, info in TYPE_MAPPING.items():
    if "penalt" in info["name"].lower() and ("save" in info["name"].lower() or "stop" in info["name"].lower() or "arrêt" in info["name"].lower()):
        penalty_types.append((type_id, info["name"], info["code"]))

if penalty_types:
    print("Types trouvés pour penalties arrêtés:")
    for type_id, name, code in penalty_types:
        print(f"  Type {type_id}: {name} ({code})")
else:
    print("❌ Aucun type trouvé pour 'penalties saved' dans le mapping")
    print("\nRecherche élargie pour tous les types avec 'penalty':")
    for type_id, info in TYPE_MAPPING.items():
        if "penalt" in info["name"].lower():
            print(f"  Type {type_id}: {info['name']} ({info['code']})")