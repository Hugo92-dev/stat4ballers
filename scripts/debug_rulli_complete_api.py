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

player_id = 186418  # Rulli
season_id = 23643   # 2024/2025

print("ANALYSE COMPLÈTE DES STATS DE RULLI 2024/2025")
print("=" * 80)

# Test 1: Stats de base
print("\n1️⃣ ENDPOINT STATS DE BASE:")
print("-" * 60)
url = f"{BASE_URL}/statistics/seasons/players/{player_id}"
params = {"seasons": season_id}
response = requests.get(url, headers=headers, params=params)

if response.status_code == 200:
    data = response.json()
    for item in data.get("data", []):
        if item.get("season_id") == season_id and item.get("team_id") == 44:
            print(f"✅ Données trouvées pour l'OM")
            print(f"   has_values: {item.get('has_values')}")
            
            if "details" in item:
                # Chercher spécifiquement les penalties
                penalty_types = [113, 1509, 326, 83]  # Différents codes possibles pour penalties
                punches_types = [59]  # Punches
                
                print(f"\n   🎯 RECHERCHE PENALTIES ET PUNCHES:")
                for detail in item["details"]:
                    type_id = detail.get("type_id")
                    if type_id in penalty_types or type_id in punches_types:
                        value = detail.get("value")
                        type_info = TYPE_MAPPING.get(str(type_id), {"name": "Unknown", "code": "unknown"})
                        print(f"      Type {type_id} ({type_info['name']}): {value}")
                
                # Compter le nombre total de types
                all_types = [d.get("type_id") for d in item["details"]]
                print(f"\n   📊 Total types retournés: {len(all_types)}")
                
                # Afficher TOUS les types pour voir ce qu'on reçoit
                print("\n   📋 TOUS LES TYPES REÇUS:")
                for detail in sorted(item["details"], key=lambda x: x.get("type_id", 0)):
                    type_id = str(detail.get("type_id"))
                    value = detail.get("value")
                    if type_id in TYPE_MAPPING:
                        type_info = TYPE_MAPPING[type_id]
                        # Extraire la valeur
                        if isinstance(value, dict):
                            val = value.get("total", value.get("goals", value.get("average", value)))
                        else:
                            val = value
                        if val and val != 0:  # N'afficher que les valeurs non nulles
                            print(f"      {type_id:4} | {type_info['name'][:30]:30} | {val}")

# Test 2: Endpoint spécifique gardien
print("\n\n2️⃣ ENDPOINT GARDIEN SPÉCIFIQUE:")
print("-" * 60)
url = f"{BASE_URL}/players/{player_id}"
params = {"include": "statistics.details"}
response = requests.get(url, headers=headers, params=params)

if response.status_code == 200:
    data = response.json()
    if "statistics" in data.get("data", {}):
        print("✅ Stats trouvées via l'endpoint player")
        stats = data["data"]["statistics"]
        if isinstance(stats, list):
            for stat in stats:
                if stat.get("season_id") == season_id:
                    print(f"   Saison 2024/2025 trouvée")
                    if "details" in stat:
                        print(f"   Nombre de détails: {len(stat['details'])}")

# Test 3: Vérifier les matchs où il a arrêté des penalties
print("\n\n3️⃣ RECHERCHE DES MATCHS AVEC PENALTIES ARRÊTÉS:")
print("-" * 60)
print("Vous avez mentionné: Brest, Lyon et Rennes")
print("Recherchons ces matchs dans l'historique...")

# Récupérer les matchs de l'OM en 2024/2025
url = f"{BASE_URL}/fixtures"
params = {
    "filters": f"teamIds:{44};seasonIds:{season_id}",
    "include": "events"
}
response = requests.get(url, headers=headers, params=params)

if response.status_code == 200:
    data = response.json()
    matches_with_penalties = []
    
    for match in data.get("data", []):
        home = match.get("name", "").split(" vs ")[0] if " vs " in match.get("name", "") else ""
        away = match.get("name", "").split(" vs ")[1] if " vs " in match.get("name", "") else ""
        
        # Chercher si c'est contre Brest, Lyon ou Rennes
        opponents = ["Brest", "Lyon", "Rennes"]
        for opponent in opponents:
            if opponent.lower() in home.lower() or opponent.lower() in away.lower():
                if "events" in match:
                    for event in match["events"]:
                        if event.get("type_id") == 83:  # Penalty
                            matches_with_penalties.append({
                                "match": match.get("name"),
                                "date": match.get("starting_at"),
                                "event": event
                            })
    
    if matches_with_penalties:
        print("✅ Matchs avec penalties trouvés:")
        for m in matches_with_penalties[:5]:
            print(f"   - {m['match']} ({m['date']})")

# Test 4: Essayer avec des includes différents
print("\n\n4️⃣ TEST AVEC DIFFÉRENTS INCLUDES:")
print("-" * 60)

includes_to_test = [
    "statistics.details",
    "statistics",
    "position",
    "detailedposition"
]

url = f"{BASE_URL}/statistics/seasons/players/{player_id}"
for include in includes_to_test:
    params = {
        "seasons": season_id,
        "include": include
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Include '{include}': {len(str(response.text))} caractères de réponse")

print("\n" + "=" * 80)
print("CONCLUSION:")
print("Si les penalties arrêtés ne sont pas dans les données, il y a peut-être:")
print("1. Un problème avec l'API SportMonks qui ne retourne pas ces stats")
print("2. Un endpoint différent à utiliser pour les stats détaillées")
print("3. Un paramètre 'include' spécifique nécessaire")