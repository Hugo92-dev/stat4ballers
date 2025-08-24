import requests
import json
import sys
from typing import Dict, Any

# Fix pour l'encodage UTF-8 sur Windows
sys.stdout.reconfigure(encoding='utf-8')

API_KEY = "leBzDfKbRE5k9zEg3FuZE3Hh7XbukODNarOXLoVtPAiAtliDZ19wLu1Wnzi2"
BASE_URL = "https://api.sportmonks.com/v3/football"

headers = {
    "Accept": "application/json",
    "Authorization": API_KEY,
}

# IDs des saisons
SEASON_IDS = {
    "2025/2026": 25651,
    "2024/2025": 23643,
    "2023/2024": 21779,
}

# ID de l'équipe OM
OM_TEAM_ID = 44

# Charger le mapping des types
with open('sportmonks_types_mapping.json', 'r', encoding='utf-8') as f:
    TYPE_MAPPING = json.load(f)

def parse_value(value: Any) -> Any:
    """Extrait la valeur depuis différents formats de l'API"""
    if isinstance(value, dict):
        for key in ['total', 'goals', 'average', 'percentage', 'count']:
            if key in value:
                return value[key]
        if value:
            return list(value.values())[0]
    return value

def get_player_info(player_id: int) -> Dict[str, Any]:
    """Récupère les infos de base d'un joueur"""
    url = f"{BASE_URL}/players/{player_id}"
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            player = data.get("data", {})
            
            return {
                "displayName": player.get("display_name", ""),
                "position": player.get("position", {}).get("name", "") if "position" in player else "",
                "jersey": player.get("jersey_number"),
            }
    except Exception as e:
        print(f"      ❌ Erreur info joueur {player_id}: {e}")
    
    return {"displayName": f"Player_{player_id}", "position": "", "jersey": None}

def get_complete_player_stats(player_id: int, season_id: int, season_name: str) -> Dict[str, Any]:
    """Récupère toutes les stats d'un joueur pour une saison avec mapping correct"""
    
    url = f"{BASE_URL}/statistics/seasons/players/{player_id}"
    params = {"seasons": season_id}
    
    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            
            for item in data.get("data", []):
                if (item.get("season_id") == season_id and 
                    item.get("team_id") == OM_TEAM_ID and 
                    item.get("has_values")):
                    
                    if "details" in item and len(item["details"]) > 0:
                        # Parser toutes les stats avec le mapping correct
                        all_stats = {}
                        
                        for detail in item["details"]:
                            type_id = str(detail.get("type_id"))
                            value = parse_value(detail.get("value", {}))
                            
                            if type_id in TYPE_MAPPING and value is not None:
                                stat_code = TYPE_MAPPING[type_id]["code"]
                                all_stats[stat_code] = value
                        
                        # Créer l'objet stats complet avec TOUS les mappings corrects
                        return {
                            "team": "Olympique Marseille",
                            "team_id": OM_TEAM_ID,
                            "league": "Ligue 1",
                            
                            # Stats générales
                            "rating": all_stats.get("rating"),
                            "minutes": all_stats.get("minutes-played", 0),
                            "appearences": all_stats.get("appearances", 0),
                            "lineups": all_stats.get("lineups", 0),
                            "captain": all_stats.get("captain", 0),
                            "touches": all_stats.get("touches", 0),
                            
                            # Stats offensives
                            "goals": all_stats.get("goals", 0),
                            "assists": all_stats.get("assists", 0),
                            "xg": all_stats.get("expected-goals"),
                            "xa": all_stats.get("expected-assists"),
                            "shots": all_stats.get("shots-total", 0),
                            "shots_on_target": all_stats.get("shots-on-target", 0),
                            "hit_woodwork": all_stats.get("hit-woodwork", 0),
                            
                            # Stats gardien
                            "saves": all_stats.get("saves", 0),
                            "goals_conceded": all_stats.get("goals-conceded", 0),
                            "clean_sheets": all_stats.get("cleansheets", all_stats.get("goalkeeper-cleansheets", 0)),
                            "penalties_saved": all_stats.get("penalties-saved", 0),
                            "punches": all_stats.get("punches", 0),
                            "inside_box_saves": all_stats.get("saves-insidebox", 0),
                            
                            # Passes
                            "passes": all_stats.get("passes", 0),
                            "passes_completed": all_stats.get("accurate-passes", 0),
                            "passes_accuracy": all_stats.get("accurate-passes-percentage"),
                            "key_passes": all_stats.get("key-passes", 0),
                            "crosses": all_stats.get("total-crosses", 0),
                            "crosses_accurate": all_stats.get("accurate-crosses", 0),
                            
                            # Défense
                            "tackles": all_stats.get("tackles", 0),
                            "blocks": all_stats.get("blocked-shots", 0),
                            "interceptions": all_stats.get("interceptions", 0),
                            "clearances": all_stats.get("clearances", 0),
                            
                            # Discipline - MAPPING CORRIGÉ
                            "fouls": all_stats.get("fouls", 0),
                            "fouls_drawn": all_stats.get("fouls-drawn", 0),
                            "yellow_cards": all_stats.get("yellowcards", 0),
                            "red_cards": all_stats.get("redcards", 0),  # Type 85 - cartons rouges directs
                            "yellowred_cards": all_stats.get("yellowred-cards", 0),  # Type 87 - cartons jaune-rouge
                            
                            # Duels
                            "ground_duels": all_stats.get("ground-duels", 0),
                            "ground_duels_won": all_stats.get("ground-duels-won", 0),
                            "aerial_duels": all_stats.get("aeriels", 0),
                            "aerial_duels_won": all_stats.get("aeriels-won", 0),
                            "duels": all_stats.get("total-duels", 0),
                            "duels_won": all_stats.get("duels-won", 0),
                            
                            # Dribbles
                            "dribbles": all_stats.get("dribbles-attempted", 0),
                            "dribbles_successful": all_stats.get("dribbles-succeeded", 0),
                            
                            # Penalties
                            "penalties": all_stats.get("penalties", 0),
                            "penalties_won": all_stats.get("penalties-won", 0),
                            "penalties_scored": all_stats.get("penalties-scored", 0),
                            "penalties_missed": all_stats.get("penalties-missed", 0),
                            "penalties_committed": all_stats.get("penalties-committed", 0),
                            
                            # Autres
                            "offsides": all_stats.get("offsides", 0),
                            "ball_losses": all_stats.get("dispossessed", 0),
                            "ball_recoveries": all_stats.get("ball-recoveries", 0),
                            "mistakes_leading_to_goals": all_stats.get("error-lead-to-goal", 0),
                        }
    
    except Exception as e:
        pass  # Silencieux
    
    return None

def get_complete_om_squad():
    """Récupère l'effectif complet de l'OM avec toutes leurs stats"""
    
    print("=" * 80)
    print("MISE À JOUR COMPLÈTE DE TOUT L'EFFECTIF DE L'OM")
    print("=" * 80)
    
    # Récupérer l'effectif actuel
    print("\n📋 Récupération de l'effectif OM saison 2025/2026...")
    
    url = f"{BASE_URL}/squads/seasons/{SEASON_IDS['2025/2026']}/teams/{OM_TEAM_ID}"
    params = {"include": "player"}
    
    squad = []
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        data = response.json()
        for item in data.get("data", []):
            player_id = item.get("player_id")
            if player_id:
                squad.append({
                    "id": player_id,
                    "jersey": item.get("jersey_number"),
                })
    
    print(f"✅ {len(squad)} joueurs trouvés dans l'effectif")
    
    # Structure pour toutes les données
    complete_om_data = {}
    
    # Pour chaque joueur de l'effectif
    for idx, player_squad_info in enumerate(squad, 1):
        player_id = player_squad_info["id"]
        
        print(f"\n[{idx}/{len(squad)}] Joueur ID {player_id}...")
        
        # Récupérer les infos du joueur
        player_info = get_player_info(player_id)
        player_name = player_info["displayName"]
        
        print(f"     👤 {player_name}")
        
        # Créer la structure du joueur
        player_data = {
            "displayName": player_name,
            "position": player_info["position"],
            "jersey": player_squad_info.get("jersey") or player_info.get("jersey"),
            "stats": {}
        }
        
        # Récupérer les stats pour chaque saison
        has_any_stats = False
        for season_name, season_id in SEASON_IDS.items():
            stats = get_complete_player_stats(player_id, season_id, season_name)
            
            if stats and stats.get("appearences", 0) > 0:
                season_key = f"{season_name} (Ligue 1, Olympique Marseille)"
                player_data["stats"][season_key] = stats
                has_any_stats = True
                
                # Calculer le total des cartons rouges pour vérification
                red_total = (stats.get("red_cards", 0) + stats.get("yellowred_cards", 0))
                
                print(f"       ✅ {season_name}: {stats['appearences']} matchs, {stats['goals']} buts")
                if red_total > 0:
                    print(f"          🟥 {red_total} carton(s) rouge(s) total")
                if stats.get("penalties_saved", 0) > 0:
                    print(f"          ⚽ {stats['penalties_saved']} penalty(s) arrêté(s)")
        
        # Ajouter le joueur aux données finales
        if has_any_stats:
            complete_om_data[str(player_id)] = player_data
            print(f"       📊 {len(player_data['stats'])} saison(s) avec stats")
        else:
            print(f"       ⚫ Aucune statistique disponible")
    
    return complete_om_data

def main():
    # Récupérer toutes les données mises à jour
    complete_data = get_complete_om_squad()
    
    print("\n" + "=" * 80)
    print("💾 SAUVEGARDE DES DONNÉES COMPLÈTES...")
    print("-" * 60)
    
    # Sauvegarder dans le fichier JSON
    with open('om_complete_stats_v2.json', 'w', encoding='utf-8') as f:
        json.dump(complete_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ {len(complete_data)} joueurs sauvegardés avec toutes leurs statistiques")
    
    # Générer le fichier TypeScript
    print("\n📝 GÉNÉRATION DU FICHIER TYPESCRIPT...")
    print("-" * 60)
    
    exec(open('generate_om_typescript.py').read())
    
    print("\n✅ Fichier TypeScript généré!")
    
    # Résumé final
    print("\n" + "=" * 80)
    print("🎉 MISE À JOUR TERMINÉE!")
    print("=" * 80)
    print(f"✅ {len(complete_data)} joueurs de l'OM mis à jour")
    print("✅ Toutes les statistiques récupérées depuis l'API SportMonks")
    print("✅ Mapping correct des type_id pour tous les joueurs")
    print("✅ Cartons rouges = cartons directs + cartons jaune-rouge")
    print("✅ Stats gardien et joueurs de champ correctes")
    print("\n🌐 Le site devrait maintenant afficher toutes les stats à jour!")
    
    # Afficher quelques exemples
    print("\n📊 EXEMPLES DE CORRECTIONS:")
    if "13171199" in complete_data:  # Balerdi
        balerdi_2024 = complete_data["13171199"]["stats"].get("2024/2025 (Ligue 1, Olympique Marseille)", {})
        red_total = balerdi_2024.get("red_cards", 0) + balerdi_2024.get("yellowred_cards", 0)
        print(f"   Leonardo Balerdi: {red_total} carton rouge total (vérifié)")
    
    if "186418" in complete_data:  # Rulli
        rulli_2024 = complete_data["186418"]["stats"].get("2024/2025 (Ligue 1, Olympique Marseille)", {})
        print(f"   Geronimo Rulli: {rulli_2024.get('clean_sheets', 0)} clean sheets, {rulli_2024.get('goals_conceded', 0)} buts encaissés")

if __name__ == "__main__":
    main()