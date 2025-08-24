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

# IDs
balerdi_id = 13171199
rulli_id = 186418
season_id = 23643  # 2024/2025
OM_TEAM_ID = 44

def get_player_raw_stats(player_id, player_name):
    print(f"\n=== {player_name.upper()} (ID: {player_id}) ===")
    print("=" * 60)
    
    url = f"{BASE_URL}/statistics/seasons/players/{player_id}"
    params = {"seasons": season_id}
    
    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            
            for item in data.get("data", []):
                if item.get("season_id") == season_id and item.get("team_id") == OM_TEAM_ID:
                    if "details" in item and len(item["details"]) > 0:
                        
                        print("TOUTES LES STATS BRUTES DE L'API:")
                        print("-" * 40)
                        
                        # Organiser par type de stat
                        discipline_stats = {}
                        key_stats = {}
                        
                        for detail in item["details"]:
                            type_id = str(detail.get("type_id"))
                            value = detail.get("value", {})
                            
                            if type_id in TYPE_MAPPING:
                                type_info = TYPE_MAPPING[type_id]
                                name = type_info["name"]
                                code = type_info["code"]
                                
                                # Extraire la valeur
                                if isinstance(value, dict):
                                    final_value = value.get("total", value.get("goals", value.get("average", value.get("percentage", value))))
                                else:
                                    final_value = value
                                
                                # Séparer par catégories
                                if "card" in name.lower() or "foul" in name.lower() or "red" in name.lower() or "yellow" in name.lower():
                                    discipline_stats[f"Type {type_id}"] = f"{name} = {final_value}"
                                elif type_id in ["321", "322", "119", "118", "84", "85", "87"]:  # Stats importantes
                                    key_stats[f"Type {type_id}"] = f"{name} = {final_value}"
                        
                        print("📊 STATS CLÉS:")
                        for key, stat in sorted(key_stats.items()):
                            print(f"   {stat}")
                        
                        print("\n🃏 DISCIPLINE:")
                        for key, stat in sorted(discipline_stats.items()):
                            print(f"   {stat}")
                        
                        # Rechercher spécifiquement les cartons rouges
                        print("\n🔍 RECHERCHE SPÉCIFIQUE CARTONS ROUGES:")
                        found_red_cards = False
                        for detail in item["details"]:
                            type_id = detail.get("type_id")
                            if type_id in [85, 87, 18]:  # Différents types possibles pour carton rouge
                                found_red_cards = True
                                value = detail.get("value", {})
                                if isinstance(value, dict):
                                    final_value = value.get("total", value.get("goals", value))
                                else:
                                    final_value = value
                                print(f"   ✅ Type {type_id} (Carton rouge) = {final_value}")
                        
                        if not found_red_cards:
                            print("   ⚫ Aucun type de carton rouge trouvé dans l'API")
                            print("   → Cela signifie probablement 0 carton rouge")
                        
                        return True
            
            print("⚠️ Pas de données pour cette saison/équipe")
            return False
        
        else:
            print(f"❌ Erreur API: {response.status_code}")
            return False
    
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

# Vérifier Balerdi
get_player_raw_stats(balerdi_id, "Leonardo Balerdi")

# Vérifier Rulli
get_player_raw_stats(rulli_id, "Geronimo Rulli")

print("\n" + "=" * 80)
print("CONCLUSION:")
print("-" * 60)
print("Si l'API ne retourne pas un type de stat (comme carton rouge),")
print("c'est que la valeur est 0. L'API SportMonks ne retourne que")
print("les statistiques non-nulles.")
print("\nSi vous pensez qu'il y a une erreur, vérifiez:")
print("1. Les matchs officiels comptabilisés par SportMonks")
print("2. Les dates exactes des événements")
print("3. Si l'événement était en Ligue 1 (pas en coupe)")