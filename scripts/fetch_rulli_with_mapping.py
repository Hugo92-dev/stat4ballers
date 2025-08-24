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

# IDs des saisons
SEASON_IDS = {
    "2025/2026": 25651,
    "2024/2025": 23643,
    "2023/2024": 21779,
}

def parse_stats_from_details(details):
    """Parse les stats depuis le format details avec type_id"""
    stats = {}
    
    for detail in details:
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
                final_value = list(value.values())[0] if value else 0
        else:
            final_value = value
        
        # Mapper avec le nom de la stat
        if type_id in TYPE_MAPPING:
            stat_code = TYPE_MAPPING[type_id]["code"]
            stats[stat_code] = final_value
    
    return stats

def get_player_season_stats_v2(player_id, season_id, season_name):
    """Récupère et parse correctement les stats"""
    url = f"{BASE_URL}/statistics/seasons/players/{player_id}"
    params = {"seasons": season_id}
    
    print(f"\n📊 Récupération saison {season_name} (ID: {season_id})...")
    
    try:
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 200:
            data = response.json()
            
            # Trouver les stats de la bonne saison
            for item in data.get("data", []):
                if item.get("season_id") == season_id and item.get("has_values"):
                    
                    if "details" in item and len(item["details"]) > 0:
                        # Parser les stats
                        stats = parse_stats_from_details(item["details"])
                        
                        print(f"   ✅ Stats trouvées pour l'OM (équipe ID: {item.get('team_id')})")
                        
                        # Créer l'objet final avec le bon mapping
                        return {
                            "team": "Olympique Marseille",
                            "team_id": 44,
                            "league": "Ligue 1",
                            
                            # Stats générales
                            "rating": stats.get("rating"),
                            "minutes": stats.get("minutes-played", 0),
                            "appearences": stats.get("appearances", 0),
                            "lineups": stats.get("lineups", 0),
                            "captain": stats.get("captain", 0),
                            
                            # Stats gardien spécifiques
                            "saves": stats.get("saves", 0),
                            "goals_conceded": stats.get("goals-conceded", 0),
                            "clean_sheets": stats.get("cleansheets", 0),
                            "penalties_saved": stats.get("penalties-saved", 0),
                            "punches": stats.get("punches", 0),
                            "inside_box_saves": stats.get("saves-insidebox", 0),
                            
                            # Passes
                            "passes": stats.get("passes", 0),
                            "passes_completed": stats.get("accurate-passes", 0),
                            "passes_accuracy": stats.get("passes-accuracy"),
                            "key_passes": stats.get("key-passes", 0),
                            
                            # Défense
                            "tackles": stats.get("tackles", 0),
                            "blocks": stats.get("blocked-shots", 0),
                            "interceptions": stats.get("interceptions", 0),
                            "clearances": stats.get("clearances", 0),
                            
                            # Discipline
                            "fouls": stats.get("fouls-committed", 0),
                            "fouls_drawn": stats.get("fouls-drawn", 0),
                            "yellow_cards": stats.get("yellowcards", 0),
                            "red_cards": stats.get("redcards", 0),
                            "yellowred_cards": stats.get("yellowred-cards", 0),
                            
                            # Duels
                            "ground_duels": stats.get("duels", 0),
                            "ground_duels_won": stats.get("duels-won", 0),
                            "aerial_duels": stats.get("aerial-duels", 0),
                            "aerial_duels_won": stats.get("aerial-duels-won", 0),
                            
                            # Autres
                            "touches": stats.get("touches", 0),
                            "ball_losses": stats.get("dispossessed", 0),
                            "ball_recoveries": stats.get("ball-recoveries", 0),
                            "mistakes_leading_to_goals": stats.get("mistakes-leading-to-goals", 0),
                            "penalties_committed": stats.get("penalties-committed", 0),
                            
                            # Non utilisés pour gardien
                            "goals": 0,
                            "assists": 0,
                            "xg": None,
                            "xa": None,
                            "shots": 0,
                            "shots_on_target": 0,
                            "crosses": 0,
                            "crosses_accurate": 0,
                            "dribbles": 0,
                            "dribbles_successful": 0,
                            "penalties_won": 0,
                            "penalties_scored": 0,
                            "penalties_missed": 0,
                            "penalties": 0,
                            "hit_woodwork": 0,
                            "offsides": 0,
                        }
                    else:
                        print(f"   ⚠️ Pas de détails disponibles")
            
            print(f"   ⚠️ Pas de données pour cette saison")
        else:
            print(f"   ❌ Erreur {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Exception: {e}")
    
    return None

print("=" * 80)
print("RÉCUPÉRATION DES VRAIES STATS DE RULLI AVEC MAPPING CORRECT")
print("=" * 80)

# Charger les données existantes
with open('om_complete_stats_v2.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# ID de Rulli
player_id = 186418

# Créer la structure pour Rulli
rulli_data = {
    "displayName": "Gerónimo Rulli",
    "position": "GK",
    "jersey": 1,
    "stats": {}
}

# Récupérer les vraies stats pour chaque saison
for season_name, season_id in SEASON_IDS.items():
    stats = get_player_season_stats_v2(player_id, season_id, season_name)
    
    if stats and stats.get("appearences", 0) > 0:
        season_key = f"{season_name} (Ligue 1, Olympique Marseille)"
        rulli_data["stats"][season_key] = stats
        
        # Afficher les stats importantes
        print(f"\n   📈 Stats clés {season_name}:")
        print(f"      - Matchs: {stats['appearences']}")
        print(f"      - Minutes: {stats['minutes']}")
        print(f"      - Buts encaissés: {stats['goals_conceded']}")
        print(f"      - Clean sheets: {stats['clean_sheets']}")
        print(f"      - Arrêts: {stats['saves']}")
        print(f"      - Penalties arrêtés: {stats['penalties_saved']}")
        print(f"      - Note moyenne: {stats['rating']}")

# Mettre à jour les données
if rulli_data["stats"]:
    data['186418'] = rulli_data
    
    # Sauvegarder
    with open('om_complete_stats_v2.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print("\n✅ Données de Rulli mises à jour avec les VRAIES stats de l'API!")
    
    # Régénérer le fichier TypeScript
    print("\n📝 Régénération du fichier TypeScript...")
    exec(open('generate_om_typescript.py').read())
    
    print("\n✅ Tout est mis à jour avec les vraies données!")
else:
    print("\n⚠️ Aucune donnée trouvée pour Rulli")