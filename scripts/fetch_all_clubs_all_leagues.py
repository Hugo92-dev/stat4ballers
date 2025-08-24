import requests
import json
import sys
import time
from typing import Dict, Any, List
from datetime import datetime

# Fix pour l'encodage UTF-8 sur Windows
sys.stdout.reconfigure(encoding='utf-8')

API_KEY = "leBzDfKbRE5k9zEg3FuZE3Hh7XbukODNarOXLoVtPAiAtliDZ19wLu1Wnzi2"
BASE_URL = "https://api.sportmonks.com/v3/football"

headers = {
    "Accept": "application/json",
    "Authorization": API_KEY,
}

# IDs des saisons PAR LIGUE
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

# Charger le mapping des types
try:
    with open('sportmonks_types_mapping.json', 'r', encoding='utf-8') as f:
        TYPE_MAPPING = json.load(f)
except:
    print("⚠️ Mapping des types non trouvé, création d'un mapping vide")
    TYPE_MAPPING = {}

# Cache pour les équipes et joueurs
TEAM_CACHE = {}
PLAYER_CACHE = {}

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
    """Récupère les infos complètes d'un joueur avec cache"""
    if player_id in PLAYER_CACHE:
        return PLAYER_CACHE[player_id]
    
    url = f"{BASE_URL}/players/{player_id}"
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            player = data.get("data", {})
            
            result = {
                "displayName": player.get("display_name", ""),
                "position": player.get("position", {}).get("name", "") if "position" in player else "",
                "jersey": player.get("jersey_number"),
            }
            PLAYER_CACHE[player_id] = result
            return result
    except:
        pass
    
    return None

def get_league_teams(league_id: int, season_id: int) -> List[int]:
    """Récupère tous les clubs d'une ligue pour une saison"""
    url = f"{BASE_URL}/teams/seasons/{season_id}"
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            teams = []
            for team in data.get("data", []):
                teams.append(team.get("id"))
            return teams
    except:
        pass
    
    return []

def get_team_squad(team_id: int, season_id: int) -> List[Dict]:
    """Récupère l'effectif d'une équipe pour une saison"""
    url = f"{BASE_URL}/squads/seasons/{season_id}/teams/{team_id}"
    params = {"include": "player"}
    
    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            squad = []
            for item in data.get("data", []):
                player_id = item.get("player_id")
                if player_id:
                    squad.append({
                        "id": player_id,
                        "jersey": item.get("jersey_number"),
                    })
            return squad
    except:
        pass
    
    return []

def get_player_stats_all_leagues(player_id: int) -> Dict[str, Any]:
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
                            
            except Exception as e:
                pass  # Silencieux pour éviter le spam
    
    return all_stats

def process_league(league_id: int, league_info: Dict) -> Dict[str, Any]:
    """Traite tous les clubs et joueurs d'une ligue"""
    league_name = league_info["name"]
    print(f"\n{'=' * 80}")
    print(f"📊 TRAITEMENT DE {league_name.upper()}")
    print(f"{'=' * 80}")
    
    all_players_data = {}
    
    # Pour la saison actuelle uniquement (pour récupérer les effectifs)
    current_season = "2025/2026"
    season_id = league_info["seasons"][current_season]
    
    # Récupérer tous les clubs de la ligue
    print(f"\n📋 Récupération des clubs de {league_name} saison {current_season}...")
    teams = get_league_teams(league_id, season_id)
    
    if not teams:
        print(f"⚠️ Aucun club trouvé pour {league_name}")
        return {}
    
    print(f"✅ {len(teams)} clubs trouvés")
    
    # Pour chaque club
    for team_idx, team_id in enumerate(teams, 1):
        team_info = get_team_info(team_id)
        team_name = team_info["name"]
        
        print(f"\n[{team_idx}/{len(teams)}] {team_name}")
        print("-" * 40)
        
        # Récupérer l'effectif du club
        squad = get_team_squad(team_id, season_id)
        
        if not squad:
            print(f"   ⚫ Pas d'effectif disponible")
            continue
        
        print(f"   ✅ {len(squad)} joueurs dans l'effectif")
        
        # Pour chaque joueur de l'effectif
        for player_data in squad:
            player_id = player_data["id"]
            
            # Récupérer les infos du joueur
            player_info = get_player_info(player_id)
            if not player_info:
                continue
            
            player_name = player_info["displayName"]
            
            # Récupérer TOUTES ses stats dans TOUTES les ligues
            all_stats = get_player_stats_all_leagues(player_id)
            
            if all_stats:
                # Créer la structure complète
                all_players_data[str(player_id)] = {
                    "displayName": player_name,
                    "position": player_info["position"],
                    "jersey": player_data.get("jersey") or player_info.get("jersey"),
                    "current_team": team_name,
                    "current_league": league_name,
                    "stats": all_stats
                }
                
                # Compter les clubs différents
                clubs = set()
                for key in all_stats.keys():
                    if "(" in key:
                        club = key.split(", ")[-1].rstrip(")")
                        clubs.add(club)
                
                if len(clubs) > 1:
                    print(f"      🌍 {player_name}: {len(clubs)} clubs")
        
        # Pause pour éviter de surcharger l'API
        time.sleep(0.5)
    
    return all_players_data

def main():
    print("=" * 80)
    print("🌍 RÉCUPÉRATION COMPLÈTE DE TOUS LES JOUEURS DE TOUS LES CHAMPIONNATS")
    print("=" * 80)
    print(f"Début: {datetime.now().strftime('%H:%M:%S')}")
    
    # Traiter chaque ligue
    all_data = {}
    
    for league_id, league_info in ALL_SEASONS.items():
        league_data = process_league(league_id, league_info)
        
        # Fusionner les données
        for player_id, player_data in league_data.items():
            if player_id not in all_data:
                all_data[player_id] = player_data
            else:
                # Fusionner les stats si le joueur existe déjà
                existing_stats = all_data[player_id]["stats"]
                new_stats = player_data["stats"]
                
                for season_key, stats in new_stats.items():
                    if season_key not in existing_stats:
                        existing_stats[season_key] = stats
    
    # Sauvegarder les données
    print("\n" + "=" * 80)
    print("💾 SAUVEGARDE DES DONNÉES...")
    
    output_file = 'all_leagues_complete_stats.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ {len(all_data)} joueurs sauvegardés dans {output_file}")
    
    # Statistiques finales
    print("\n" + "=" * 80)
    print("📊 STATISTIQUES FINALES:")
    print("-" * 60)
    
    # Compter par ligue actuelle
    leagues_count = {}
    for player_data in all_data.values():
        league = player_data.get("current_league", "Unknown")
        leagues_count[league] = leagues_count.get(league, 0) + 1
    
    for league, count in sorted(leagues_count.items()):
        print(f"   {league}: {count} joueurs")
    
    # Joueurs avec plusieurs clubs
    multi_club_players = 0
    for player_data in all_data.values():
        clubs = set()
        for key in player_data.get("stats", {}).keys():
            if "(" in key:
                club = key.split(", ")[-1].rstrip(")")
                clubs.add(club)
        if len(clubs) > 1:
            multi_club_players += 1
    
    print(f"\n   🌍 {multi_club_players} joueurs avec stats dans plusieurs clubs")
    
    print(f"\nFin: {datetime.now().strftime('%H:%M:%S')}")
    print("\n🎉 TERMINÉ - Tous les joueurs de tous les championnats ont été traités!")

if __name__ == "__main__":
    main()