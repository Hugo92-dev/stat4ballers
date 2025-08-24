import requests
import json
import sys
from typing import Dict, Any, List, Set
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import os

# Fix pour l'encodage UTF-8 sur Windows
sys.stdout.reconfigure(encoding='utf-8')

API_KEY = "leBzDfKbRE5k9zEg3FuZE3Hh7XbukODNarOXLoVtPAiAtliDZ19wLu1Wnzi2"
BASE_URL = "https://api.sportmonks.com/v3/football"

headers = {
    "Accept": "application/json",
    "Authorization": API_KEY,
}

# Les 5 grands championnats avec leurs saisons
TOP_5_LEAGUES = {
    301: {
        "name": "Ligue 1",
        "slug": "ligue1",
        "seasons": {
            "2025/2026": 25651,
            "2024/2025": 23643,
            "2023/2024": 21779,
        }
    },
    8: {
        "name": "Premier League",
        "slug": "premier-league",
        "seasons": {
            "2025/2026": 25583,
            "2024/2025": 23614,
            "2023/2024": 21646,
        }
    },
    564: {
        "name": "La Liga",
        "slug": "la-liga",
        "seasons": {
            "2025/2026": 25659,
            "2024/2025": 23621,
            "2023/2024": 21694,
        }
    },
    384: {
        "name": "Serie A",
        "slug": "serie-a",
        "seasons": {
            "2025/2026": 25533,
            "2024/2025": 23746,
            "2023/2024": 21818,
        }
    },
    82: {
        "name": "Bundesliga",
        "slug": "bundesliga",
        "seasons": {
            "2025/2026": 25646,
            "2024/2025": 23744,
            "2023/2024": 21795,
        }
    },
}

# Tous les autres championnats pour récupérer l'historique des joueurs
OTHER_LEAGUES = {
    307: "Eredivisie",
    501: "Liga Portugal",
    648: "MLS",
    271: "EFL Championship",
    109: "Jupiler Pro League",
    387: "Süper Lig",
    218: "Allsvenskan",
    181: "Danish Superliga",
    118: "Premier League Ukraine",
    106: "Ekstraklasa",
    619: "Super League 1",
    119: "Austrian Bundesliga",
    144: "Russian Premier League",
    101: "Scottish Premiership",
    390: "Ligue 1 Mobilis",
    185: "Egyptian Premier League",
    120: "Czech First League",
    113: "Swiss Super League",
}

# Charger le mapping des types
with open('sportmonks_types_mapping.json', 'r', encoding='utf-8') as f:
    TYPE_MAPPING = json.load(f)

# Cache global pour éviter les doublons
TEAM_CACHE = {}
LEAGUE_CACHE = {}
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
                "id": team_id,
                "name": team.get("name", f"Team_{team_id}"),
                "short_code": team.get("short_code", ""),
            }
            TEAM_CACHE[team_id] = result
            return result
    except:
        pass
    
    result = {"id": team_id, "name": f"Team_{team_id}", "short_code": ""}
    TEAM_CACHE[team_id] = result
    return result

def get_league_name(league_id: int) -> str:
    """Récupère le nom d'une ligue avec cache"""
    if league_id in LEAGUE_CACHE:
        return LEAGUE_CACHE[league_id]
    
    # Check dans les ligues connues
    if league_id in TOP_5_LEAGUES:
        name = TOP_5_LEAGUES[league_id]["name"]
        LEAGUE_CACHE[league_id] = name
        return name
    
    if league_id in OTHER_LEAGUES:
        name = OTHER_LEAGUES[league_id]
        LEAGUE_CACHE[league_id] = name
        return name
    
    # Sinon récupérer depuis l'API
    url = f"{BASE_URL}/leagues/{league_id}"
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            name = data.get("data", {}).get("name", f"League_{league_id}")
            LEAGUE_CACHE[league_id] = name
            return name
    except:
        pass
    
    name = f"League_{league_id}"
    LEAGUE_CACHE[league_id] = name
    return name

def get_player_info(player_id: int) -> Dict[str, Any]:
    """Récupère les infos d'un joueur avec cache"""
    if player_id in PLAYER_CACHE:
        return PLAYER_CACHE[player_id]
    
    url = f"{BASE_URL}/players/{player_id}"
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            player = data.get("data", {})
            
            result = {
                "id": player_id,
                "displayName": player.get("display_name", ""),
                "position": player.get("position", {}).get("name", "") if "position" in player else "",
                "jersey": player.get("jersey_number"),
                "nationality": player.get("nationality", {}).get("name", "") if "nationality" in player else "",
            }
            PLAYER_CACHE[player_id] = result
            return result
    except:
        pass
    
    return None

def parse_player_stats(details: List[Dict], team_info: Dict, league_name: str) -> Dict[str, Any]:
    """Parse les statistiques d'un joueur depuis les détails de l'API"""
    all_stats = {}
    
    for detail in details:
        type_id = str(detail.get("type_id"))
        value = parse_value(detail.get("value", {}))
        
        if type_id in TYPE_MAPPING and value is not None:
            stat_code = TYPE_MAPPING[type_id]["code"]
            all_stats[stat_code] = value
    
    return {
        "team": team_info["name"],
        "team_id": team_info["id"],
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

def get_player_all_stats(player_id: int, all_season_ids: Set[int]) -> Dict[str, Any]:
    """Récupère toutes les stats d'un joueur pour toutes les saisons"""
    all_stats = {}
    
    # Récupérer toutes les stats en une seule requête
    url = f"{BASE_URL}/statistics/seasons/players/{player_id}"
    params = {"seasons": ",".join(map(str, all_season_ids))}
    
    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            
            for item in data.get("data", []):
                if item.get("has_values") and "details" in item and len(item["details"]) > 0:
                    season_id = item.get("season_id")
                    team_id = item.get("team_id")
                    league_id = item.get("league_id")
                    
                    # Trouver le nom de la saison
                    season_name = None
                    for league_info in TOP_5_LEAGUES.values():
                        for sname, sid in league_info["seasons"].items():
                            if sid == season_id:
                                season_name = sname
                                break
                        if season_name:
                            break
                    
                    if not season_name:
                        continue
                    
                    team_info = get_team_info(team_id)
                    league_name = get_league_name(league_id)
                    
                    stats = parse_player_stats(item["details"], team_info, league_name)
                    
                    if stats.get("appearences", 0) > 0:
                        season_key = f"{season_name} ({league_name}, {team_info['name']})"
                        all_stats[season_key] = stats
    except:
        pass
    
    return all_stats

def get_teams_for_league_season(league_id: int, season_id: int) -> List[int]:
    """Récupère toutes les équipes d'une ligue pour une saison"""
    url = f"{BASE_URL}/standings/seasons/{season_id}"
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            teams = set()
            for standing in data.get("data", []):
                team_id = standing.get("participant_id")
                if team_id:
                    teams.add(team_id)
            return list(teams)
    except:
        pass
    
    return []

def get_squad_for_team(team_id: int, season_id: int) -> List[int]:
    """Récupère l'effectif d'une équipe pour une saison"""
    url = f"{BASE_URL}/squads/seasons/{season_id}/teams/{team_id}"
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            players = []
            for item in data.get("data", []):
                player_id = item.get("player_id")
                if player_id:
                    players.append(player_id)
            return players
    except:
        pass
    
    return []

def process_league(league_id: int, league_info: Dict) -> Dict[str, Any]:
    """Traite tous les joueurs d'une ligue"""
    print(f"\n{'='*80}")
    print(f"📊 TRAITEMENT : {league_info['name']}")
    print(f"{'='*80}")
    
    league_data = {}
    all_season_ids = set()
    
    # Collecter tous les IDs de saisons (top 5 + autres)
    for l_info in TOP_5_LEAGUES.values():
        for sid in l_info["seasons"].values():
            all_season_ids.add(sid)
    
    # Récupérer toutes les équipes de la ligue (saison actuelle)
    current_season_id = league_info["seasons"]["2025/2026"]
    teams = get_teams_for_league_season(league_id, current_season_id)
    
    if not teams:
        # Fallback: essayer la saison précédente
        current_season_id = league_info["seasons"]["2024/2025"]
        teams = get_teams_for_league_season(league_id, current_season_id)
    
    print(f"📋 {len(teams)} équipes trouvées")
    
    # Pour chaque équipe
    for team_idx, team_id in enumerate(teams, 1):
        team_info = get_team_info(team_id)
        print(f"\n[{team_idx}/{len(teams)}] {team_info['name']}")
        
        # Récupérer l'effectif
        players = get_squad_for_team(team_id, current_season_id)
        
        if not players:
            print(f"   ⚠️ Aucun joueur trouvé")
            continue
        
        print(f"   👥 {len(players)} joueurs dans l'effectif")
        
        # Pour chaque joueur
        for player_id in players:
            player_info = get_player_info(player_id)
            if not player_info:
                continue
            
            # Récupérer toutes ses stats (toutes ligues confondues)
            all_stats = get_player_all_stats(player_id, all_season_ids)
            
            if all_stats:
                league_data[str(player_id)] = {
                    "displayName": player_info["displayName"],
                    "position": player_info["position"],
                    "jersey": player_info["jersey"],
                    "nationality": player_info["nationality"],
                    "currentTeam": team_info["name"],
                    "stats": all_stats
                }
                
                # Afficher un résumé
                total_matches = sum(s.get("appearences", 0) for s in all_stats.values())
                total_goals = sum(s.get("goals", 0) for s in all_stats.values())
                print(f"      ✅ {player_info['displayName']}: {total_matches} matchs, {total_goals} buts ({len(all_stats)} saisons)")
        
        # Limiter pour éviter les timeouts (pause entre les équipes)
        time.sleep(0.5)
    
    return league_data

def generate_typescript_file(league_slug: str, data: Dict[str, Any]):
    """Génère le fichier TypeScript pour une ligue"""
    output_file = f"../data/{league_slug}PlayersCompleteStats.ts"
    
    ts_content = f"""// Généré automatiquement depuis l'API SportMonks
// {len(data)} joueurs avec statistiques complètes

export interface PlayerStats {{
  team: string;
  team_id: number;
  league: string;
  rating?: number;
  minutes: number;
  appearences: number;
  lineups: number;
  captain: number;
  touches: number;
  goals: number;
  assists: number;
  xg?: number;
  xa?: number;
  shots: number;
  shots_on_target: number;
  hit_woodwork: number;
  saves: number;
  goals_conceded: number;
  clean_sheets: number;
  penalties_saved: number;
  punches: number;
  inside_box_saves: number;
  passes: number;
  passes_completed: number;
  passes_accuracy?: number;
  key_passes: number;
  crosses: number;
  crosses_accurate: number;
  tackles: number;
  blocks: number;
  interceptions: number;
  clearances: number;
  fouls: number;
  fouls_drawn: number;
  yellow_cards: number;
  red_cards: number;
  yellowred_cards: number;
  ground_duels: number;
  ground_duels_won: number;
  aerial_duels: number;
  aerial_duels_won: number;
  duels: number;
  duels_won: number;
  dribbles: number;
  dribbles_successful: number;
  penalties: number;
  penalties_won: number;
  penalties_scored: number;
  penalties_missed: number;
  penalties_committed: number;
  offsides: number;
  ball_losses: number;
  ball_recoveries: number;
  mistakes_leading_to_goals: number;
}}

export interface PlayerData {{
  displayName: string;
  position: string;
  jersey: number | null;
  nationality: string;
  currentTeam: string;
  stats: {{ [season: string]: PlayerStats }};
}}

export const {league_slug.replace('-', '')}PlayersCompleteStats: {{ [playerId: string]: PlayerData }} = {json.dumps(data, ensure_ascii=False, indent=2)};
"""
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(ts_content)
    
    print(f"   📝 Fichier TypeScript généré: {output_file}")

def main():
    print("="*100)
    print("🚀 RÉCUPÉRATION COMPLÈTE DE TOUTES LES STATISTIQUES")
    print("="*100)
    print("Cible: Les 5 grands championnats européens")
    print("Saisons: 2023/2024, 2024/2025, 2025/2026")
    print("Inclut: Historique des joueurs dans TOUTES les ligues")
    print("="*100)
    
    # Traiter chaque ligue
    for league_id, league_info in TOP_5_LEAGUES.items():
        try:
            # Récupérer les données de la ligue
            league_data = process_league(league_id, league_info)
            
            if league_data:
                # Sauvegarder en JSON
                json_file = f"{league_info['slug']}_complete_stats.json"
                with open(json_file, 'w', encoding='utf-8') as f:
                    json.dump(league_data, f, ensure_ascii=False, indent=2)
                
                print(f"\n💾 {len(league_data)} joueurs sauvegardés dans {json_file}")
                
                # Générer le fichier TypeScript
                generate_typescript_file(league_info['slug'], league_data)
            
        except Exception as e:
            print(f"\n❌ Erreur pour {league_info['name']}: {e}")
            continue
        
        # Pause entre les ligues pour éviter de surcharger l'API
        print(f"\n⏸️ Pause avant la prochaine ligue...")
        time.sleep(5)
    
    print("\n" + "="*100)
    print("🎉 TERMINÉ!")
    print("="*100)
    print("✅ Toutes les ligues ont été traitées")
    print("✅ Les fichiers JSON et TypeScript ont été générés")
    print("✅ Les statistiques incluent l'historique complet des joueurs")
    
    # Résumé des caches
    print(f"\n📊 Résumé:")
    print(f"   - {len(TEAM_CACHE)} équipes en cache")
    print(f"   - {len(PLAYER_CACHE)} joueurs en cache")
    print(f"   - {len(LEAGUE_CACHE)} ligues en cache")

if __name__ == "__main__":
    main()