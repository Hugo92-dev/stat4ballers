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

print("RÉCUPÉRATION COMPLÈTE DE TOUTES LES STATS DE RULLI")
print("=" * 80)

player_id = 186418
seasons = {
    "2025/2026": 25651,
    "2024/2025": 23643,
}

# Charger les données existantes
with open('om_complete_stats_v2.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Créer la structure pour Rulli
rulli_data = {
    "displayName": "Gerónimo Rulli",
    "position": "GK",
    "jersey": 1,
    "stats": {}
}

for season_name, season_id in seasons.items():
    print(f"\n📊 Saison {season_name}:")
    
    url = f"{BASE_URL}/statistics/seasons/players/{player_id}"
    params = {"seasons": season_id}
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        api_data = response.json()
        
        for item in api_data.get("data", []):
            if item.get("season_id") == season_id and item.get("has_values"):
                
                if "details" in item and len(item["details"]) > 0:
                    # Parser TOUTES les stats
                    stats_dict = {}
                    
                    for detail in item["details"]:
                        type_id = str(detail.get("type_id"))
                        value = detail.get("value", {})
                        
                        # Extraire la valeur
                        if isinstance(value, dict):
                            final_value = value.get("total", value.get("goals", value.get("average", value.get("percentage", 0))))
                        else:
                            final_value = value
                        
                        # Mapper avec le code de la stat
                        if type_id in TYPE_MAPPING:
                            stat_code = TYPE_MAPPING[type_id]["code"]
                            stats_dict[stat_code] = final_value
                    
                    # Créer l'objet stats complet avec TOUTES les valeurs
                    season_stats = {
                        "team": "Olympique Marseille",
                        "team_id": 44,
                        "league": "Ligue 1",
                        
                        # Stats générales
                        "rating": stats_dict.get("rating"),
                        "minutes": stats_dict.get("minutes-played", 0),
                        "appearences": stats_dict.get("appearances", 0),
                        "lineups": stats_dict.get("lineups", 0),
                        "captain": stats_dict.get("captain", 0),
                        "touches": stats_dict.get("touches", 0),
                        
                        # Stats gardien
                        "saves": stats_dict.get("saves", 0),
                        "goals_conceded": stats_dict.get("goals-conceded", 0),
                        "clean_sheets": stats_dict.get("cleansheets", stats_dict.get("goalkeeper-cleansheets", 0)),
                        "penalties_saved": stats_dict.get("penalties-saved", 0),  # Type 113
                        "punches": stats_dict.get("punches", 0),
                        "inside_box_saves": stats_dict.get("saves-insidebox", 0),
                        
                        # Passes
                        "passes": stats_dict.get("passes", 0),
                        "passes_completed": stats_dict.get("accurate-passes", 0),
                        "passes_accuracy": stats_dict.get("accurate-passes-percentage"),
                        "key_passes": stats_dict.get("key-passes", 0),
                        "crosses": stats_dict.get("total-crosses", 0),
                        "crosses_accurate": stats_dict.get("accurate-crosses", 0),
                        
                        # Défense
                        "tackles": stats_dict.get("tackles", 0),
                        "blocks": stats_dict.get("blocked-shots", 0),
                        "interceptions": stats_dict.get("interceptions", 0),
                        "clearances": stats_dict.get("clearances", 0),
                        
                        # Discipline
                        "fouls": stats_dict.get("fouls", 0),
                        "fouls_drawn": stats_dict.get("fouls-drawn", 0),
                        "yellow_cards": stats_dict.get("yellowcards", 0),
                        "red_cards": stats_dict.get("redcards", 0),
                        "yellowred_cards": stats_dict.get("yellowred-cards", 0),
                        
                        # Duels
                        "ground_duels": stats_dict.get("ground-duels", 0),
                        "ground_duels_won": stats_dict.get("ground-duels-won", 0),
                        "aerial_duels": stats_dict.get("aeriels", 0),
                        "aerial_duels_won": stats_dict.get("aeriels-won", 0),
                        "duels": stats_dict.get("total-duels", 0),
                        "duels_won": stats_dict.get("duels-won", 0),
                        
                        # Autres
                        "ball_losses": stats_dict.get("dispossessed", 0),
                        "ball_recoveries": stats_dict.get("ball-recoveries", 0),
                        "mistakes_leading_to_goals": stats_dict.get("error-lead-to-goal", 0),
                        "penalties_committed": stats_dict.get("penalties-committed", 0),
                        
                        # Non utilisés pour gardien mais on les met quand même
                        "goals": stats_dict.get("goals", 0),
                        "assists": stats_dict.get("assists", 0),
                        "xg": stats_dict.get("expected-goals"),
                        "xa": stats_dict.get("expected-assists"),
                        "shots": stats_dict.get("shots-total", 0),
                        "shots_on_target": stats_dict.get("shots-on-target", 0),
                        "dribbles": stats_dict.get("dribbles-attempted", 0),
                        "dribbles_successful": stats_dict.get("dribbles-succeeded", 0),
                        "penalties_won": stats_dict.get("penalties-won", 0),
                        "penalties_scored": stats_dict.get("penalties-scored", 0),
                        "penalties_missed": stats_dict.get("penalties-missed", 0),
                        "penalties": stats_dict.get("penalties", 0),
                        "hit_woodwork": stats_dict.get("hit-woodwork", 0),
                        "offsides": stats_dict.get("offsides", 0),
                    }
                    
                    # Ajouter à la structure
                    season_key = f"{season_name} (Ligue 1, Olympique Marseille)"
                    rulli_data["stats"][season_key] = season_stats
                    
                    # Afficher les stats clés
                    print(f"  ✅ Stats récupérées:")
                    print(f"     - Matchs: {season_stats['appearences']}")
                    print(f"     - Minutes: {season_stats['minutes']}")
                    print(f"     - Buts encaissés: {season_stats['goals_conceded']}")
                    print(f"     - Clean sheets: {season_stats['clean_sheets']}")
                    print(f"     - Arrêts: {season_stats['saves']}")
                    print(f"     - Penalties arrêtés: {season_stats['penalties_saved']}")
                    print(f"     - Note: {season_stats['rating']}")
                    
                    # Vérifier si on a le type 113 dans les données
                    has_type_113 = False
                    for detail in item["details"]:
                        if detail.get("type_id") == 113:
                            has_type_113 = True
                            print(f"     ⚠️ Type 113 trouvé avec valeur: {detail.get('value')}")
                    
                    if not has_type_113:
                        print(f"     ⚠️ Type 113 (penalties-saved) NON présent dans les données")

# Mettre à jour les données
data['186418'] = rulli_data

# Sauvegarder
with open('om_complete_stats_v2.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("\n✅ Données de Rulli mises à jour!")

# Régénérer le fichier TypeScript
print("\n📝 Régénération du fichier TypeScript...")
exec(open('generate_om_typescript.py').read())

print("\n✅ Fichier TypeScript mis à jour!")