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

# Charger les données existantes
with open('om_complete_stats_v2.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

def parse_value(value):
    """Extrait la valeur depuis différents formats de l'API"""
    if isinstance(value, dict):
        for key in ['total', 'goals', 'average', 'percentage', 'count']:
            if key in value:
                return value[key]
        if value:
            return list(value.values())[0]
    return value

def get_correct_player_stats(player_id, season_id, season_name):
    """Récupère les stats correctes depuis l'API"""
    url = f"{BASE_URL}/statistics/seasons/players/{player_id}"
    params = {"seasons": season_id}
    
    all_stats = {}
    
    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data_api = response.json()
            for item in data_api.get("data", []):
                if item.get("season_id") == season_id and item.get("team_id") == 44:
                    if "details" in item:
                        for detail in item["details"]:
                            type_id = str(detail.get("type_id"))
                            value = parse_value(detail.get("value", {}))
                            
                            if type_id in TYPE_MAPPING and value is not None:
                                stat_code = TYPE_MAPPING[type_id]["code"]
                                all_stats[stat_code] = value
                        
                        print(f"✅ {season_name} - {len(all_stats)} stats récupérées")
                        
                        # Calcul spécial pour les cartons rouges
                        red_cards = all_stats.get("redcards", 0)  # Type 85
                        yellowred_cards = all_stats.get("yellowred-cards", 0)  # Type 87
                        
                        print(f"   Cartons rouges directs: {red_cards}")  
                        print(f"   Cartons jaune-rouge: {yellowred_cards}")
                        print(f"   Total cartons rouges: {red_cards + yellowred_cards}")
                        
                        return all_stats
    
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    return {}

# Corriger Balerdi
print("CORRECTION DES STATS DE BALERDI:")
print("=" * 60)

balerdi_stats_2024 = get_correct_player_stats(13171199, 23643, "2024/2025")

if balerdi_stats_2024:
    # Mettre à jour les stats de Balerdi
    if "13171199" in data:
        season_key = "2024/2025 (Ligue 1, Olympique Marseille)"
        if season_key in data["13171199"]["stats"]:
            # Corriger les cartons rouges
            current_red = data["13171199"]["stats"][season_key].get("red_cards", 0)
            current_yellowred = data["13171199"]["stats"][season_key].get("yellowred_cards", 0)
            
            new_red = balerdi_stats_2024.get("redcards", 0)
            new_yellowred = balerdi_stats_2024.get("yellowred-cards", 0)
            
            data["13171199"]["stats"][season_key]["red_cards"] = new_red
            data["13171199"]["stats"][season_key]["yellowred_cards"] = new_yellowred
            
            print(f"\n📝 Correction Balerdi 2024/2025:")
            print(f"   Avant: {current_red} rouge, {current_yellowred} jaune-rouge")
            print(f"   Après: {new_red} rouge, {new_yellowred} jaune-rouge")
            print(f"   Total cartons rouges: {new_red + new_yellowred}")

# Vérifier aussi Rulli pour s'assurer qu'il est correct
print("\n\nVÉRIFICATION DES STATS DE RULLI:")
print("=" * 60)

rulli_stats_2024 = get_correct_player_stats(186418, 23643, "2024/2025")

if rulli_stats_2024:
    if "186418" in data:
        season_key = "2024/2025 (Ligue 1, Olympique Marseille)"
        if season_key in data["186418"]["stats"]:
            print(f"\n📊 Stats actuelles Rulli 2024/2025:")
            current_penalties_saved = data["186418"]["stats"][season_key].get("penalties_saved", 0)
            print(f"   Penalties arrêtés: {current_penalties_saved}")
            
            # Vérifier si c'est cohérent avec l'API
            api_penalties = rulli_stats_2024.get("penalties-saved", 0)
            print(f"   API penalties arrêtés: {api_penalties}")
            
            if current_penalties_saved != api_penalties:
                print(f"   ⚠️ Différence détectée, correction nécessaire")
                if api_penalties > 0:
                    data["186418"]["stats"][season_key]["penalties_saved"] = api_penalties
                    print(f"   ✅ Corrigé à {api_penalties}")

# Sauvegarder les corrections
with open('om_complete_stats_v2.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("\n✅ Corrections sauvegardées!")

# Régénérer le fichier TypeScript
print("\n📝 Régénération du fichier TypeScript...")
exec(open('generate_om_typescript.py').read())

print("\n✅ Fichier TypeScript mis à jour!")
print("\n🎉 Les stats devraient maintenant être correctes sur le site!")