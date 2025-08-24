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

# Mapping des ligues connues
LEAGUE_NAMES = {
    301: "Ligue 1",
    8: "Premier League",
    564: "La Liga",
    384: "Serie A",
    82: "Bundesliga",
    307: "Eredivisie",
    501: "Liga Portugal",
    648: "MLS",
    271: "EFL Championship",
}

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

def get_team_info(team_id: int) -> Dict[str, str]:
    """Récupère les infos d'une équipe"""
    # Cache pour éviter de refaire la même requête
    if not hasattr(get_team_info, "cache"):
        get_team_info.cache = {}
    
    if team_id in get_team_info.cache:
        return get_team_info.cache[team_id]
    
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
            get_team_info.cache[team_id] = result
            return result
    except:
        pass
    
    result = {"name": f"Team_{team_id}", "short_code": ""}
    get_team_info.cache[team_id] = result
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

def get_all_player_stats_complete(player_id: int) -> Dict[str, Any]:
    """Récupère TOUTES les stats d'un joueur pour toutes ses équipes"""
    
    all_seasons_stats = {}
    
    for season_name, season_id in SEASON_IDS.items():
        url = f"{BASE_URL}/statistics/seasons/players/{player_id}"
        params = {"seasons": season_id}
        
        try:
            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 200:
                data = response.json()
                
                for item in data.get("data", []):
                    if item.get("season_id") == season_id and item.get("has_values"):
                        team_id = item.get("team_id")
                        league_id = item.get("league_id")
                        
                        # Récupérer les infos de l'équipe
                        team_info = get_team_info(team_id)
                        league_name = LEAGUE_NAMES.get(league_id, f"League_{league_id}")
                        
                        if "details" in item and len(item["details"]) > 0:
                            # Parser toutes les stats
                            all_stats = {}
                            
                            for detail in item["details"]:
                                type_id = str(detail.get("type_id"))
                                value = parse_value(detail.get("value", {}))
                                
                                if type_id in TYPE_MAPPING and value is not None:
                                    stat_code = TYPE_MAPPING[type_id]["code"]
                                    all_stats[stat_code] = value
                            
                            # Créer l'objet stats complet
                            stats_obj = {
                                "team": team_info["name"],
                                "team_id": team_id,
                                "league": league_name,
                                
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
                            
                            # Créer la clé de saison
                            season_key = f"{season_name} ({league_name}, {team_info['name']})"
                            all_seasons_stats[season_key] = stats_obj
                            
        except:
            pass
    
    return all_seasons_stats

def main():
    print("=" * 80)
    print("MISE À JOUR COMPLÈTE : TOUS LES JOUEURS, TOUTES LES ÉQUIPES")
    print("=" * 80)
    
    # Récupérer l'effectif actuel de l'OM
    print("\n📋 Récupération de l'effectif OM...")
    
    url = f"{BASE_URL}/squads/seasons/{SEASON_IDS['2025/2026']}/teams/{OM_TEAM_ID}"
    params = {"include": "player"}
    
    squad_ids = []
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        data = response.json()
        for item in data.get("data", []):
            player_id = item.get("player_id")
            if player_id:
                squad_ids.append(player_id)
    
    print(f"✅ {len(squad_ids)} joueurs trouvés")
    
    # Nouvelle structure de données
    complete_data = {}
    
    # Pour chaque joueur de l'effectif
    for idx, player_id in enumerate(squad_ids, 1):
        print(f"\n[{idx}/{len(squad_ids)}] Joueur ID {player_id}...")
        
        # Récupérer les infos du joueur
        player_info = get_player_info(player_id)
        if not player_info:
            continue
        
        player_name = player_info["displayName"]
        print(f"   👤 {player_name}")
        
        # Récupérer TOUTES ses stats (toutes équipes)
        all_stats = get_all_player_stats_complete(player_id)
        
        if all_stats:
            # Créer la structure complète
            complete_data[str(player_id)] = {
                "displayName": player_name,
                "position": player_info["position"],
                "jersey": player_info["jersey"],
                "stats": all_stats
            }
            
            # Afficher un résumé
            for season_key, stats in all_stats.items():
                if stats["appearences"] > 0:
                    print(f"      ✅ {season_key}: {stats['appearences']} matchs, {stats['goals']} buts")
    
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
    
    # Exemples de vérification
    print("\n" + "=" * 80)
    print("📊 EXEMPLES DE JOUEURS AVEC PLUSIEURS CLUBS:")
    print("-" * 60)
    
    examples = {
        "95694": "Adrien Rabiot",
        "608285": "Angel Gomes",
        "335521": "Facundo Medina",
        "20333643": "Mason Greenwood",
    }
    
    for pid, name in examples.items():
        if pid in complete_data:
            stats = complete_data[pid]["stats"]
            clubs = set()
            for key in stats.keys():
                if "(" in key:
                    club = key.split(", ")[-1].rstrip(")")
                    clubs.add(club)
            
            if len(clubs) > 1:
                print(f"✅ {name}: {len(clubs)} clubs différents")
                for club in clubs:
                    print(f"   - {club}")
    
    print("\n🎉 TERMINÉ - Tous les joueurs ont leurs stats de TOUS leurs clubs!")

if __name__ == "__main__":
    main()