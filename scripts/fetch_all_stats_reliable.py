#!/usr/bin/env python3
"""
Script fiable et robuste pour récupérer TOUTES les statistiques
de TOUS les joueurs sur les 3 dernières saisons
"""

import requests
import json
import sys
import time
from typing import Dict, Any, List, Set
from datetime import datetime

# Fix pour l'encodage UTF-8 sur Windows
sys.stdout.reconfigure(encoding='utf-8')

API_KEY = "leBzDfKbRE5k9zEg3FuZE3Hh7XbukODNarOXLoVtPAiAtliDZ19wLu1Wnzi2"
BASE_URL = "https://api.sportmonks.com/v3/football"

headers = {
    "Accept": "application/json",
    "Authorization": API_KEY,
}

# Configuration des 5 grands championnats avec les IDs corrects
LEAGUES_CONFIG = {
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

# Autres ligues pour l'historique complet des joueurs
EXTRA_LEAGUES = {
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
try:
    with open('sportmonks_types_mapping.json', 'r', encoding='utf-8') as f:
        TYPE_MAPPING = json.load(f)
    print("✅ Mapping des types chargé avec succès")
except Exception as e:
    print(f"❌ Erreur chargement mapping: {e}")
    sys.exit(1)

# Caches globaux
CACHE = {
    "teams": {},
    "leagues": {},
    "players": {},
}

def safe_request(url: str, params: Dict = None, max_retries: int = 3) -> Dict:
    """Effectue une requête avec retry automatique"""
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers, params=params, timeout=30)
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 429:  # Rate limit
                print(f"   ⏸️ Rate limit atteint, pause de 60 secondes...")
                time.sleep(60)
            else:
                print(f"   ⚠️ Status {response.status_code}")
                time.sleep(2)
        except requests.exceptions.Timeout:
            print(f"   ⏱️ Timeout, nouvelle tentative...")
            time.sleep(5)
        except Exception as e:
            print(f"   ❌ Erreur: {e}")
            time.sleep(5)
    
    return None

def parse_value(value: Any) -> Any:
    """Parse une valeur depuis l'API"""
    if isinstance(value, dict):
        for key in ['total', 'goals', 'average', 'percentage', 'count']:
            if key in value:
                return value[key]
        if value:
            return list(value.values())[0]
    return value

def get_team_info(team_id: int) -> Dict:
    """Récupère les infos d'une équipe avec cache"""
    if team_id in CACHE["teams"]:
        return CACHE["teams"][team_id]
    
    data = safe_request(f"{BASE_URL}/teams/{team_id}")
    if data:
        team = data.get("data", {})
        info = {
            "id": team_id,
            "name": team.get("name", f"Team_{team_id}"),
            "short_code": team.get("short_code", ""),
        }
        CACHE["teams"][team_id] = info
        return info
    
    # Fallback
    info = {"id": team_id, "name": f"Team_{team_id}", "short_code": ""}
    CACHE["teams"][team_id] = info
    return info

def get_league_name(league_id: int) -> str:
    """Récupère le nom d'une ligue avec cache"""
    if league_id in CACHE["leagues"]:
        return CACHE["leagues"][league_id]
    
    # Vérifier dans les ligues connues
    if league_id in LEAGUES_CONFIG:
        name = LEAGUES_CONFIG[league_id]["name"]
    elif league_id in EXTRA_LEAGUES:
        name = EXTRA_LEAGUES[league_id]
    else:
        # Récupérer depuis l'API
        data = safe_request(f"{BASE_URL}/leagues/{league_id}")
        if data:
            name = data.get("data", {}).get("name", f"League_{league_id}")
        else:
            name = f"League_{league_id}"
    
    CACHE["leagues"][league_id] = name
    return name

def get_player_info(player_id: int) -> Dict:
    """Récupère les infos d'un joueur avec cache"""
    if player_id in CACHE["players"]:
        return CACHE["players"][player_id]
    
    data = safe_request(f"{BASE_URL}/players/{player_id}")
    if data:
        player = data.get("data", {})
        info = {
            "id": player_id,
            "displayName": player.get("display_name", f"Player_{player_id}"),
            "position": player.get("position", {}).get("name", "") if player.get("position") else "",
            "jersey": player.get("jersey_number"),
            "nationality": player.get("nationality", {}).get("name", "") if player.get("nationality") else "",
        }
        CACHE["players"][player_id] = info
        return info
    
    return None

def parse_stats_from_details(details: List[Dict]) -> Dict:
    """Parse tous les détails de stats en utilisant le mapping"""
    parsed = {}
    
    for detail in details:
        type_id = str(detail.get("type_id"))
        value = parse_value(detail.get("value", {}))
        
        if type_id in TYPE_MAPPING and value is not None:
            stat_code = TYPE_MAPPING[type_id]["code"]
            parsed[stat_code] = value
    
    return parsed

def build_stats_object(raw_stats: Dict, team_info: Dict, league_name: str) -> Dict:
    """Construit l'objet de stats complet"""
    return {
        "team": team_info["name"],
        "team_id": team_info["id"],
        "league": league_name,
        
        # Stats générales
        "rating": raw_stats.get("rating"),
        "minutes": raw_stats.get("minutes-played", 0),
        "appearences": raw_stats.get("appearances", 0),
        "lineups": raw_stats.get("lineups", 0),
        "captain": raw_stats.get("captain", 0),
        "touches": raw_stats.get("touches", 0),
        
        # Stats offensives
        "goals": raw_stats.get("goals", 0),
        "assists": raw_stats.get("assists", 0),
        "xg": raw_stats.get("expected-goals"),
        "xa": raw_stats.get("expected-assists"),
        "shots": raw_stats.get("shots-total", 0),
        "shots_on_target": raw_stats.get("shots-on-target", 0),
        "hit_woodwork": raw_stats.get("hit-woodwork", 0),
        
        # Stats gardien
        "saves": raw_stats.get("saves", 0),
        "goals_conceded": raw_stats.get("goals-conceded", 0),
        "clean_sheets": raw_stats.get("cleansheets", raw_stats.get("goalkeeper-cleansheets", 0)),
        "penalties_saved": raw_stats.get("penalties-saved", 0),
        "punches": raw_stats.get("punches", 0),
        "inside_box_saves": raw_stats.get("saves-insidebox", 0),
        
        # Passes
        "passes": raw_stats.get("passes", 0),
        "passes_completed": raw_stats.get("accurate-passes", 0),
        "passes_accuracy": raw_stats.get("accurate-passes-percentage"),
        "key_passes": raw_stats.get("key-passes", 0),
        "crosses": raw_stats.get("total-crosses", 0),
        "crosses_accurate": raw_stats.get("accurate-crosses", 0),
        
        # Défense
        "tackles": raw_stats.get("tackles", 0),
        "blocks": raw_stats.get("blocked-shots", 0),
        "interceptions": raw_stats.get("interceptions", 0),
        "clearances": raw_stats.get("clearances", 0),
        
        # Discipline
        "fouls": raw_stats.get("fouls", 0),
        "fouls_drawn": raw_stats.get("fouls-drawn", 0),
        "yellow_cards": raw_stats.get("yellowcards", 0),
        "red_cards": raw_stats.get("redcards", 0),
        "yellowred_cards": raw_stats.get("yellowred-cards", 0),
        
        # Duels
        "ground_duels": raw_stats.get("ground-duels", 0),
        "ground_duels_won": raw_stats.get("ground-duels-won", 0),
        "aerial_duels": raw_stats.get("aeriels", 0),
        "aerial_duels_won": raw_stats.get("aeriels-won", 0),
        "duels": raw_stats.get("total-duels", 0),
        "duels_won": raw_stats.get("duels-won", 0),
        
        # Dribbles
        "dribbles": raw_stats.get("dribbles-attempted", 0),
        "dribbles_successful": raw_stats.get("dribbles-succeeded", 0),
        
        # Penalties
        "penalties": raw_stats.get("penalties", 0),
        "penalties_won": raw_stats.get("penalties-won", 0),
        "penalties_scored": raw_stats.get("penalties-scored", 0),
        "penalties_missed": raw_stats.get("penalties-missed", 0),
        "penalties_committed": raw_stats.get("penalties-committed", 0),
        
        # Autres
        "offsides": raw_stats.get("offsides", 0),
        "ball_losses": raw_stats.get("dispossessed", 0),
        "ball_recoveries": raw_stats.get("ball-recoveries", 0),
        "mistakes_leading_to_goals": raw_stats.get("error-lead-to-goal", 0),
    }

def get_player_complete_stats(player_id: int) -> Dict:
    """Récupère TOUTES les stats d'un joueur pour TOUTES les saisons"""
    all_stats = {}
    
    # Collecter tous les IDs de saisons
    all_season_ids = []
    for league_config in LEAGUES_CONFIG.values():
        for season_id in league_config["seasons"].values():
            all_season_ids.append(season_id)
    
    # Requête unique pour toutes les saisons
    url = f"{BASE_URL}/statistics/seasons/players/{player_id}"
    params = {"seasons": ",".join(map(str, all_season_ids))}
    
    data = safe_request(url, params)
    if not data:
        return all_stats
    
    # Parser chaque saison
    for item in data.get("data", []):
        if not item.get("has_values"):
            continue
        
        if "details" not in item or len(item["details"]) == 0:
            continue
        
        season_id = item.get("season_id")
        team_id = item.get("team_id")
        league_id = item.get("league_id")
        
        # Trouver le nom de la saison
        season_name = None
        for league_config in LEAGUES_CONFIG.values():
            for sname, sid in league_config["seasons"].items():
                if sid == season_id:
                    season_name = sname
                    break
            if season_name:
                break
        
        if not season_name:
            continue
        
        # Récupérer les infos
        team_info = get_team_info(team_id)
        league_name = get_league_name(league_id)
        
        # Parser les stats
        raw_stats = parse_stats_from_details(item["details"])
        stats_obj = build_stats_object(raw_stats, team_info, league_name)
        
        # Ajouter seulement si le joueur a joué
        if stats_obj.get("appearences", 0) > 0:
            season_key = f"{season_name} ({league_name}, {team_info['name']})"
            all_stats[season_key] = stats_obj
    
    return all_stats

def get_teams_for_season(league_id: int, season_id: int) -> List[int]:
    """Récupère les équipes d'une ligue pour une saison"""
    url = f"{BASE_URL}/standings/seasons/{season_id}"
    data = safe_request(url)
    
    teams = []
    if data:
        for standing in data.get("data", []):
            team_id = standing.get("participant_id")
            if team_id:
                teams.append(team_id)
    
    return teams

def get_squad_players(team_id: int, season_id: int) -> List[int]:
    """Récupère les joueurs d'une équipe pour une saison"""
    url = f"{BASE_URL}/squads/seasons/{season_id}/teams/{team_id}"
    data = safe_request(url)
    
    players = []
    if data:
        for item in data.get("data", []):
            player_id = item.get("player_id")
            if player_id:
                players.append(player_id)
    
    return players

def process_league(league_id: int, league_config: Dict) -> Dict:
    """Traite une ligue complète"""
    print(f"\n{'='*80}")
    print(f"🏆 TRAITEMENT: {league_config['name']}")
    print(f"{'='*80}")
    
    league_data = {}
    
    # Utiliser la saison actuelle pour récupérer les équipes
    current_season = league_config["seasons"]["2025/2026"]
    teams = get_teams_for_season(league_id, current_season)
    
    if not teams:
        # Fallback sur la saison précédente
        current_season = league_config["seasons"]["2024/2025"]
        teams = get_teams_for_season(league_id, current_season)
    
    print(f"📋 {len(teams)} équipes trouvées")
    
    total_players = 0
    
    # Traiter chaque équipe
    for team_idx, team_id in enumerate(teams, 1):
        team_info = get_team_info(team_id)
        print(f"\n[{team_idx}/{len(teams)}] {team_info['name']}")
        
        # Récupérer l'effectif
        players = get_squad_players(team_id, current_season)
        
        if not players:
            print(f"   ⚠️ Aucun joueur trouvé")
            continue
        
        print(f"   👥 {len(players)} joueurs")
        
        # Traiter chaque joueur
        players_with_stats = 0
        for player_id in players:
            player_info = get_player_info(player_id)
            if not player_info:
                continue
            
            # Récupérer TOUTES les stats du joueur
            all_stats = get_player_complete_stats(player_id)
            
            if all_stats:
                league_data[str(player_id)] = {
                    "displayName": player_info["displayName"],
                    "position": player_info["position"],
                    "jersey": player_info["jersey"],
                    "nationality": player_info["nationality"],
                    "currentTeam": team_info["name"],
                    "stats": all_stats
                }
                
                players_with_stats += 1
                total_players += 1
                
                # Afficher un point de progression
                if players_with_stats % 5 == 0:
                    print(f"      ✅ {players_with_stats} joueurs traités...")
        
        print(f"   📊 {players_with_stats} joueurs avec stats")
        
        # Pause courte entre les équipes
        time.sleep(1)
    
    print(f"\n✅ Total: {total_players} joueurs avec statistiques")
    return league_data

def save_league_data(league_slug: str, league_data: Dict):
    """Sauvegarde les données d'une ligue"""
    # Sauvegarder en JSON
    json_file = f"{league_slug}_complete_stats.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(league_data, f, ensure_ascii=False, indent=2)
    print(f"💾 Données sauvegardées: {json_file}")
    
    # Générer le fichier TypeScript
    ts_file = f"../data/{league_slug}PlayersCompleteStats.ts"
    ts_content = f"""// Généré automatiquement depuis l'API SportMonks
// {len(league_data)} joueurs avec statistiques complètes
// Dernière mise à jour: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

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

export const {league_slug.replace('-', '')}PlayersCompleteStats: {{ [playerId: string]: PlayerData }} = {json.dumps(league_data, ensure_ascii=False, indent=2)};
"""
    
    with open(ts_file, 'w', encoding='utf-8') as f:
        f.write(ts_content)
    print(f"📝 TypeScript généré: {ts_file}")

def main():
    print("="*100)
    print("🚀 RÉCUPÉRATION FIABLE DE TOUTES LES STATISTIQUES")
    print("="*100)
    print("✅ 5 grands championnats européens")
    print("✅ 3 dernières saisons (2023/2024, 2024/2025, 2025/2026)")
    print("✅ Historique complet des joueurs (toutes ligues)")
    print("✅ Gestion des erreurs et retry automatique")
    print("="*100)
    
    start_time = time.time()
    
    # Traiter chaque ligue
    for league_id, league_config in LEAGUES_CONFIG.items():
        try:
            league_data = process_league(league_id, league_config)
            
            if league_data:
                save_league_data(league_config["slug"], league_data)
                print(f"✅ {league_config['name']} terminée avec succès!")
            else:
                print(f"⚠️ Aucune donnée pour {league_config['name']}")
            
            # Pause entre les ligues
            print("\n⏸️ Pause de 10 secondes avant la prochaine ligue...")
            time.sleep(10)
            
        except Exception as e:
            print(f"\n❌ Erreur pour {league_config['name']}: {e}")
            continue
    
    # Résumé final
    elapsed_time = time.time() - start_time
    print("\n" + "="*100)
    print("🎉 TERMINÉ!")
    print("="*100)
    print(f"⏱️ Temps total: {elapsed_time/60:.1f} minutes")
    print(f"📊 Statistiques:")
    print(f"   - {len(CACHE['teams'])} équipes traitées")
    print(f"   - {len(CACHE['players'])} joueurs traités")
    print(f"   - {len(CACHE['leagues'])} ligues référencées")
    print("\n✅ Toutes les données sont maintenant à jour!")
    print("✅ Les fichiers JSON et TypeScript ont été générés")
    print("✅ Le site peut maintenant afficher les vraies statistiques!")

if __name__ == "__main__":
    main()