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

# IDs des saisons PAR LIGUE (données fournies par l'utilisateur)
ALL_SEASONS = {
    # Ligue 1
    301: {
        "name": "Ligue 1",
        "seasons": {
            "2025/2026": 25651,
            "2024/2025": 23643,
            "2023/2024": 21779,
        }
    },
    # Premier League
    8: {
        "name": "Premier League",
        "seasons": {
            "2025/2026": 25583,
            "2024/2025": 23614,
            "2023/2024": 21646,
        }
    },
    # La Liga
    564: {
        "name": "La Liga",
        "seasons": {
            "2025/2026": 25659,
            "2024/2025": 23621,
            "2023/2024": 21694,
        }
    },
    # Serie A
    384: {
        "name": "Serie A",
        "seasons": {
            "2025/2026": 25533,
            "2024/2025": 23746,
            "2023/2024": 21818,
        }
    },
    # Bundesliga
    82: {
        "name": "Bundesliga",
        "seasons": {
            "2025/2026": 25646,
            "2024/2025": 23744,
            "2023/2024": 21795,
        }
    },
}

# ID de l'équipe OM
OM_TEAM_ID = 44

# Charger le mapping des types
with open('sportmonks_types_mapping.json', 'r', encoding='utf-8') as f:
    TYPE_MAPPING = json.load(f)

# Cache pour les équipes
TEAM_CACHE = {}

def parse_value(value: Any) -> Any:
    """Extrait la valeur depuis différents formats de l'API"""
    if isinstance(value, dict):
        for key in ['total', 'goals', 'average', 'percentage', 'count']:
            if key in value:
                return value[key]
        if value:
            return list(value.values())[0]
    return value

def get_team_info(team_id: int) -> Dict[str, str]:
    """Récupère les infos d'une équipe avec cache"""
    if team_id in TEAM_CACHE:
        return TEAM_CACHE[team_id]
    
    url = f"{BASE_URL}/teams/{team_id}"
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            team = data.get("data", {})
            result = {
                "name": team.get("name", f"Team_{team_id}"),
                "short_code": team.get("short_code", ""),
            }
            TEAM_CACHE[team_id] = result
            return result
    except:
        pass
    
    result = {"name": f"Team_{team_id}", "short_code": ""}
    TEAM_CACHE[team_id] = result
    return result

def get_player_info(player_id: int) -> Dict[str, Any]:
    """Récupère les infos complètes d'un joueur"""
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
    except:
        pass
    
    return None

def get_player_stats_all_leagues(player_id: int, player_name: str) -> Dict[str, Any]:
    """Récupère les stats d'un joueur dans TOUTES les ligues"""
    
    all_stats = {}
    
    # Pour chaque ligue
    for league_id, league_info in ALL_SEASONS.items():
        league_name = league_info["name"]
        
        # Pour chaque saison de cette ligue
        for season_name, season_id in league_info["seasons"].items():
            url = f"{BASE_URL}/statistics/seasons/players/{player_id}"
            params = {"seasons": season_id}
            
            try:
                response = requests.get(url, headers=headers, params=params)
                if response.status_code == 200:
                    data = response.json()
                    
                    for item in data.get("data", []):
                        if item.get("season_id") == season_id and item.get("has_values"):
                            team_id = item.get("team_id")
                            
                            # Récupérer les infos de l'équipe
                            team_info = get_team_info(team_id)
                            
                            if "details" in item and len(item["details"]) > 0:
                                # Parser toutes les stats
                                parsed_stats = {}
                                
                                for detail in item["details"]:
                                    type_id = str(detail.get("type_id"))
                                    value = parse_value(detail.get("value", {}))
                                    
                                    if type_id in TYPE_MAPPING and value is not None:
                                        stat_code = TYPE_MAPPING[type_id]["code"]
                                        parsed_stats[stat_code] = value
                                
                                # Créer l'objet stats complet
                                stats_obj = {
                                    "team": team_info["name"],
                                    "team_id": team_id,
                                    "league": league_name,
                                    
                                    # Stats générales
                                    "rating": parsed_stats.get("rating"),
                                    "minutes": parsed_stats.get("minutes-played", 0),
                                    "appearences": parsed_stats.get("appearances", 0),
                                    "lineups": parsed_stats.get("lineups", 0),
                                    "captain": parsed_stats.get("captain", 0),
                                    "touches": parsed_stats.get("touches", 0),
                                    
                                    # Stats offensives
                                    "goals": parsed_stats.get("goals", 0),
                                    "assists": parsed_stats.get("assists", 0),
                                    "xg": parsed_stats.get("expected-goals"),
                                    "xa": parsed_stats.get("expected-assists"),
                                    "shots": parsed_stats.get("shots-total", 0),
                                    "shots_on_target": parsed_stats.get("shots-on-target", 0),
                                    "hit_woodwork": parsed_stats.get("hit-woodwork", 0),
                                    
                                    # Stats gardien
                                    "saves": parsed_stats.get("saves", 0),
                                    "goals_conceded": parsed_stats.get("goals-conceded", 0),
                                    "clean_sheets": parsed_stats.get("cleansheets", parsed_stats.get("goalkeeper-cleansheets", 0)),
                                    "penalties_saved": parsed_stats.get("penalties-saved", 0),
                                    "punches": parsed_stats.get("punches", 0),
                                    "inside_box_saves": parsed_stats.get("saves-insidebox", 0),
                                    
                                    # Passes
                                    "passes": parsed_stats.get("passes", 0),
                                    "passes_completed": parsed_stats.get("accurate-passes", 0),
                                    "passes_accuracy": parsed_stats.get("accurate-passes-percentage"),
                                    "key_passes": parsed_stats.get("key-passes", 0),
                                    "crosses": parsed_stats.get("total-crosses", 0),
                                    "crosses_accurate": parsed_stats.get("accurate-crosses", 0),
                                    
                                    # Défense
                                    "tackles": parsed_stats.get("tackles", 0),
                                    "blocks": parsed_stats.get("blocked-shots", 0),
                                    "interceptions": parsed_stats.get("interceptions", 0),
                                    "clearances": parsed_stats.get("clearances", 0),
                                    
                                    # Discipline
                                    "fouls": parsed_stats.get("fouls", 0),
                                    "fouls_drawn": parsed_stats.get("fouls-drawn", 0),
                                    "yellow_cards": parsed_stats.get("yellowcards", 0),
                                    "red_cards": parsed_stats.get("redcards", 0),
                                    "yellowred_cards": parsed_stats.get("yellowred-cards", 0),
                                    
                                    # Duels
                                    "ground_duels": parsed_stats.get("ground-duels", 0),
                                    "ground_duels_won": parsed_stats.get("ground-duels-won", 0),
                                    "aerial_duels": parsed_stats.get("aeriels", 0),
                                    "aerial_duels_won": parsed_stats.get("aeriels-won", 0),
                                    "duels": parsed_stats.get("total-duels", 0),
                                    "duels_won": parsed_stats.get("duels-won", 0),
                                    
                                    # Dribbles
                                    "dribbles": parsed_stats.get("dribbles-attempted", 0),
                                    "dribbles_successful": parsed_stats.get("dribbles-succeeded", 0),
                                    
                                    # Penalties
                                    "penalties": parsed_stats.get("penalties", 0),
                                    "penalties_won": parsed_stats.get("penalties-won", 0),
                                    "penalties_scored": parsed_stats.get("penalties-scored", 0),
                                    "penalties_missed": parsed_stats.get("penalties-missed", 0),
                                    "penalties_committed": parsed_stats.get("penalties-committed", 0),
                                    
                                    # Autres
                                    "offsides": parsed_stats.get("offsides", 0),
                                    "ball_losses": parsed_stats.get("dispossessed", 0),
                                    "ball_recoveries": parsed_stats.get("ball-recoveries", 0),
                                    "mistakes_leading_to_goals": parsed_stats.get("error-lead-to-goal", 0),
                                }
                                
                                # Créer la clé de saison
                                season_key = f"{season_name} ({league_name}, {team_info['name']})"
                                all_stats[season_key] = stats_obj
                                
                                # Afficher trouvé
                                if stats_obj["appearences"] > 0:
                                    print(f"      ✅ {season_key}: {stats_obj['appearences']} matchs, {stats_obj['goals']} buts")
                            
            except Exception as e:
                pass  # Silencieux pour éviter le spam
    
    return all_stats

def main():
    print("=" * 80)
    print("RÉCUPÉRATION COMPLÈTE : TOUTES LES LIGUES POUR TOUS LES JOUEURS")
    print("=" * 80)
    
    # Récupérer l'effectif actuel de l'OM (saison Ligue 1 2025/2026)
    print("\n📋 Récupération de l'effectif OM...")
    
    url = f"{BASE_URL}/squads/seasons/{ALL_SEASONS[301]['seasons']['2025/2026']}/teams/{OM_TEAM_ID}"
    params = {"include": "player"}
    
    squad_ids = []
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        data = response.json()
        for item in data.get("data", []):
            player_id = item.get("player_id")
            jersey = item.get("jersey_number")
            if player_id:
                squad_ids.append({"id": player_id, "jersey": jersey})
    
    print(f"✅ {len(squad_ids)} joueurs trouvés")
    
    # Nouvelle structure de données
    complete_data = {}
    
    # Pour chaque joueur de l'effectif
    for idx, player_data in enumerate(squad_ids, 1):
        player_id = player_data["id"]
        
        print(f"\n[{idx}/{len(squad_ids)}] Joueur ID {player_id}...")
        
        # Récupérer les infos du joueur
        player_info = get_player_info(player_id)
        if not player_info:
            continue
        
        player_name = player_info["displayName"]
        print(f"   👤 {player_name}")
        
        # Récupérer TOUTES ses stats dans TOUTES les ligues
        all_stats = get_player_stats_all_leagues(player_id, player_name)
        
        if all_stats:
            # Créer la structure complète
            complete_data[str(player_id)] = {
                "displayName": player_name,
                "position": player_info["position"],
                "jersey": player_data.get("jersey") or player_info.get("jersey"),
                "stats": all_stats
            }
    
    # Sauvegarder les données
    print("\n" + "=" * 80)
    print("💾 SAUVEGARDE...")
    
    with open('om_complete_stats_v2.json', 'w', encoding='utf-8') as f:
        json.dump(complete_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ {len(complete_data)} joueurs sauvegardés!")
    
    # Générer le fichier TypeScript
    print("\n📝 Génération du fichier TypeScript...")
    exec(open('generate_om_typescript.py').read())
    
    print("\n✅ Fichier TypeScript généré!")
    
    # Vérifications spécifiques
    print("\n" + "=" * 80)
    print("📊 VÉRIFICATIONS DES JOUEURS AVEC STATS HORS LIGUE 1:")
    print("-" * 60)
    
    examples = {
        "95694": "Adrien Rabiot",
        "20333643": "Mason Greenwood",
        "1744": "Pierre-Emile Højbjerg",
        "31739": "Pierre-Emerick Aubameyang",
        "608285": "Angel Gomes",
    }
    
    for pid, name in examples.items():
        if pid in complete_data:
            stats = complete_data[pid]["stats"]
            non_ligue1 = []
            for key in stats.keys():
                if "Ligue 1" not in key:
                    non_ligue1.append(key)
            
            if non_ligue1:
                print(f"\n✅ {name}:")
                for season in non_ligue1:
                    print(f"   - {season}")
            else:
                print(f"\n⚫ {name}: Seulement Ligue 1")
    
    print("\n🎉 TERMINÉ - Stats récupérées dans les 5 grandes ligues européennes!")

if __name__ == "__main__":
    main()