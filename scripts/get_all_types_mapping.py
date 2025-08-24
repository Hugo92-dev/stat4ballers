import requests
import json
import sys

# Fix pour l'encodage UTF-8 sur Windows
sys.stdout.reconfigure(encoding='utf-8')

API_KEY = "leBzDfKbRE5k9zEg3FuZE3Hh7XbukODNarOXLoVtPAiAtliDZ19wLu1Wnzi2"
BASE_URL = "https://api.sportmonks.com/v3"

headers = {
    "Accept": "application/json",
    "Authorization": API_KEY,
}

print("RÉCUPÉRATION DE TOUS LES TYPES SportMonks")
print("=" * 80)

# Récupérer tous les types (paginés)
all_types = {}
page = 1
has_more = True

while has_more:
    url = f"{BASE_URL}/core/types"
    params = {"per_page": 100, "page": page}
    
    try:
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 200:
            data = response.json()
            
            for type_data in data.get("data", []):
                type_id = type_data["id"]
                all_types[type_id] = {
                    "name": type_data["name"],
                    "code": type_data["code"],
                    "developer_name": type_data["developer_name"],
                    "model_type": type_data["model_type"],
                    "stat_group": type_data.get("stat_group")
                }
            
            # Vérifier s'il y a plus de pages
            pagination = data.get("pagination", {})
            has_more = pagination.get("has_more", False)
            page += 1
            
            print(f"  Page {page-1}: {len(data.get('data', []))} types récupérés")
        else:
            print(f"Erreur {response.status_code}: {response.text[:100]}")
            break
            
    except Exception as e:
        print(f"Exception: {e}")
        break

print(f"\nTotal types récupérés: {len(all_types)}")

# Sauvegarder le mapping
with open('sportmonks_types_mapping.json', 'w', encoding='utf-8') as f:
    json.dump(all_types, f, ensure_ascii=False, indent=2)

print("✅ Mapping sauvegardé dans sportmonks_types_mapping.json")

# Afficher les types importants pour les gardiens
print("\n📊 TYPES IMPORTANTS POUR LES GARDIENS:")
goalkeeper_types = [
    57, 84, 85, 119, 321, 322, 80, 88, 118, 101, 104, 116
]

for type_id in goalkeeper_types:
    if str(type_id) in all_types or type_id in all_types:
        type_info = all_types.get(type_id) or all_types.get(str(type_id))
        print(f"  Type {type_id}: {type_info['name']} ({type_info['code']})")

# Afficher tous les types de statistiques (model_type = 'statistic')
print("\n📈 TOUS LES TYPES DE STATISTIQUES:")
stat_types = {}
for type_id, info in all_types.items():
    if info["model_type"] == "statistic":
        stat_group = info.get("stat_group", "other")
        if stat_group not in stat_types:
            stat_types[stat_group] = []
        stat_types[stat_group].append((type_id, info["name"], info["code"]))

for group, types in sorted(stat_types.items()):
    print(f"\n  {group.upper()}:")
    for type_id, name, code in sorted(types, key=lambda x: x[0]):
        print(f"    {type_id}: {name} ({code})")