import requests
import json
import sys
from typing import Dict, Any, List

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
        for key in ['total', 'goals', 'average', 'percentage', 'count', 'all']:
            if key in value:
                return value[key]
        if value:
            return list(value.values())[0]
    return value

def get_enhanced_player_stats(player_id: int, season_id: int, season_name: str) -> Dict[str, Any]:
    """Récupère les stats améliorées avec plusieurs méthodes"""
    
    print(f"\n📊 Récupération pour {season_name}...")
    
    # Méthode 1: Stats classiques avec tous les détails
    url = f"{BASE_URL}/statistics/seasons/players/{player_id}"
    params = {"seasons": season_id}
    
    all_stats = {}
    
    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            for item in data.get("data", []):
                if item.get("season_id") == season_id and item.get("team_id") == OM_TEAM_ID:
                    if "details" in item:
                        for detail in item["details"]:
                            type_id = str(detail.get("type_id"))
                            value = parse_value(detail.get("value", {}))
                            
                            if type_id in TYPE_MAPPING and value is not None:
                                stat_code = TYPE_MAPPING[type_id]["code"]
                                all_stats[stat_code] = value
                        
                        print(f"   ✅ {len(all_stats)} statistiques récupérées")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
    
    # Créer l'objet complet
    if all_stats.get("appearances", 0) > 0:
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
            # IMPORTANT: Pour les penalties saved, on va mettre une valeur par défaut
            # car l'API ne les retourne pas correctement
            "penalties_saved": all_stats.get("penalties-saved", all_stats.get("goalkeeper-penalties-saved", 0)),
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
            
            # Discipline
            "fouls": all_stats.get("fouls", 0),
            "fouls_drawn": all_stats.get("fouls-drawn", 0),
            "yellow_cards": all_stats.get("yellowcards", 0),
            "red_cards": all_stats.get("redcards", 0),
            "yellowred_cards": all_stats.get("yellowred-cards", 0),
            
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
    
    return None

def fetch_all_om_players_complete() -> Dict[str, Any]:
    """Récupère tous les joueurs de l'OM avec leurs stats complètes"""
    
    print("=" * 80)
    print("RÉCUPÉRATION COMPLÈTE DE TOUTES LES STATS OM")
    print("=" * 80)
    
    # Récupérer l'effectif actuel
    print("\n📋 Récupération de l'effectif OM...")
    
    url = f"{BASE_URL}/squads/seasons/{SEASON_IDS['2025/2026']}/teams/{OM_TEAM_ID}"
    params = {"include": "player"}
    
    squad = []
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        data = response.json()
        for item in data.get("data", []):
            player_id = item.get("player_id")
            jersey = item.get("jersey_number")
            
            if player_id and "player" in item:
                player_data = item["player"]
                squad.append({
                    "id": player_id,
                    "name": player_data.get("display_name", ""),
                    "position": player_data.get("position", {}).get("name", "") if "position" in player_data else "",
                    "jersey": jersey,
                })
            elif player_id:
                squad.append({
                    "id": player_id,
                    "jersey": jersey,
                })
    
    print(f"✅ {len(squad)} joueurs trouvés")
    
    # Structure pour stocker toutes les données
    all_players_data = {}
    
    # Pour chaque joueur, récupérer les infos complètes
    for idx, player_squad_info in enumerate(squad, 1):
        player_id = player_squad_info["id"]
        
        # Récupérer les infos du joueur si manquantes
        if "name" not in player_squad_info or not player_squad_info.get("name"):
            url = f"{BASE_URL}/players/{player_id}"
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                player = data.get("data", {})
                player_name = player.get("display_name", f"Player_{player_id}")
                player_position = player.get("position", {}).get("name", "") if "position" in player else ""
            else:
                player_name = f"Player_{player_id}"
                player_position = ""
        else:
            player_name = player_squad_info["name"]
            player_position = player_squad_info.get("position", "")
        
        print(f"\n[{idx}/{len(squad)}] {player_name} (ID: {player_id})")
        
        # Créer la structure du joueur
        player_data = {
            "displayName": player_name,
            "position": player_position,
            "jersey": player_squad_info.get("jersey"),
            "stats": {}
        }
        
        # Récupérer les stats pour chaque saison
        has_any_stats = False
        for season_name, season_id in SEASON_IDS.items():
            stats = get_enhanced_player_stats(player_id, season_id, season_name)
            
            if stats:
                season_key = f"{season_name} (Ligue 1, Olympique Marseille)"
                player_data["stats"][season_key] = stats
                has_any_stats = True
                print(f"     ✅ {stats['appearences']} matchs, {stats['goals']} buts")
        
        # Ajouter le joueur aux données seulement s'il a des stats
        if has_any_stats:
            all_players_data[str(player_id)] = player_data
    
    return all_players_data

def main():
    # Récupérer toutes les données
    all_players_data = fetch_all_om_players_complete()
    
    # NOTE IMPORTANTE: Corrections manuelles basées sur les informations fournies
    # L'API SportMonks ne retourne pas correctement certaines stats
    # Voici les corrections connues:
    
    if "186418" in all_players_data:  # Rulli
        print("\n⚠️ Application des corrections connues pour Rulli...")
        # Saison 2024/2025 - 3 penalties arrêtés contre Brest, Lyon et Rennes
        if "2024/2025 (Ligue 1, Olympique Marseille)" in all_players_data["186418"]["stats"]:
            all_players_data["186418"]["stats"]["2024/2025 (Ligue 1, Olympique Marseille)"]["penalties_saved"] = 3
            print("   ✅ Penalties arrêtés corrigé: 3 (Brest, Lyon, Rennes)")
    
    # Sauvegarder les données
    print("\n" + "=" * 80)
    print("💾 Sauvegarde des données...")
    
    with open('om_complete_stats_v2.json', 'w', encoding='utf-8') as f:
        json.dump(all_players_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Données sauvegardées pour {len(all_players_data)} joueurs")
    
    # Générer le fichier TypeScript
    print("\n📝 Génération du fichier TypeScript...")
    exec(open('generate_om_typescript.py').read())
    
    print("\n✅ Fichier TypeScript mis à jour!")
    
    print("\n" + "=" * 80)
    print("🎉 TERMINÉ!")
    print("\nNote: L'API SportMonks a des limitations sur certaines statistiques.")
    print("Les penalties arrêtés de Rulli (3 en 2024/2025) ont été corrigés manuellement")
    print("car l'API ne les retourne pas correctement.")
    print("=" * 80)

if __name__ == "__main__":
    main()