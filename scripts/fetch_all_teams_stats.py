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
        for key in ['total', 'goals', 'average', 'percentage', 'count']:
            if key in value:
                return value[key]
        if value:
            return list(value.values())[0]
    return value

def get_team_info(team_id: int) -> Dict[str, str]:
    """Récupère les infos d'une équipe"""
    url = f"{BASE_URL}/teams/{team_id}"
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            team = data.get("data", {})
            return {
                "name": team.get("name", "Unknown Team"),
                "short_code": team.get("short_code", ""),
            }
    except:
        pass
    
    return {"name": f"Team_{team_id}", "short_code": ""}

def get_league_info(league_id: int) -> str:
    """Récupère le nom d'une ligue"""
    url = f"{BASE_URL}/leagues/{league_id}"
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            league = data.get("data", {})
            return league.get("name", f"League_{league_id}")
    except:
        pass
    
    return f"League_{league_id}"

def get_player_all_teams_stats(player_id: int, player_name: str) -> Dict[str, Any]:
    """Récupère les stats d'un joueur pour TOUTES ses équipes sur les 3 saisons"""
    
    print(f"\n👤 {player_name} (ID: {player_id})")
    print("-" * 40)
    
    all_seasons_stats = {}
    
    for season_name, season_id in SEASON_IDS.items():
        # Récupérer TOUTES les stats du joueur pour cette saison (toutes équipes)
        url = f"{BASE_URL}/statistics/seasons/players/{player_id}"
        params = {"seasons": season_id}
        
        try:
            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 200:
                data = response.json()
                
                # Parser toutes les équipes où il a joué cette saison
                for item in data.get("data", []):
                    if item.get("season_id") == season_id and item.get("has_values"):
                        team_id = item.get("team_id")
                        league_id = item.get("league_id")
                        
                        # Récupérer les infos de l'équipe et de la ligue
                        team_info = get_team_info(team_id)
                        league_name = get_league_info(league_id) if league_id else "Unknown League"
                        
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
                            
                            # Créer la clé de saison avec équipe et ligue
                            season_key = f"{season_name} ({league_name}, {team_info['name']})"
                            all_seasons_stats[season_key] = stats_obj
                            
                            print(f"   ✅ {season_name} - {team_info['name']} ({league_name}): {stats_obj['appearences']} matchs, {stats_obj['goals']} buts")
                            
        except Exception as e:
            print(f"   ❌ Erreur pour la saison {season_name}: {e}")
    
    return all_seasons_stats

def main():
    print("=" * 80)
    print("RÉCUPÉRATION DES STATS DE TOUS LES CLUBS POUR LES JOUEURS DE L'OM")
    print("=" * 80)
    
    # Charger les données actuelles
    with open('om_complete_stats_v2.json', 'r', encoding='utf-8') as f:
        current_data = json.load(f)
    
    # Exemples de joueurs qui ont joué ailleurs
    important_players = {
        "95694": "Adrien Rabiot",  # Juventus 2023/2024
        "1744": "Pierre-Emile Højbjerg",  # Tottenham/autres
        "31739": "Pierre-Emerick Aubameyang",  # Chelsea/autres
        "20333643": "Mason Greenwood",  # Manchester United/Getafe
        "608285": "Angel Gomes",  # Lille
        "537332": "Timothy Weah",  # Lille
        "335521": "Facundo Medina",  # Lens
    }
    
    # Mettre à jour chaque joueur
    for player_id, player_name in important_players.items():
        all_stats = get_player_all_teams_stats(int(player_id), player_name)
        
        if all_stats:
            # Mettre à jour ou créer le joueur
            if player_id in current_data:
                # Conserver les infos existantes
                current_data[player_id]["stats"] = all_stats
            else:
                # Créer nouvelles données
                current_data[player_id] = {
                    "displayName": player_name,
                    "position": "",
                    "jersey": None,
                    "stats": all_stats
                }
            
            print(f"   📊 Total: {len(all_stats)} saison(s)/équipe(s)")
    
    # Sauvegarder les données mises à jour
    print("\n" + "=" * 80)
    print("💾 SAUVEGARDE DES DONNÉES...")
    
    with open('om_complete_stats_v2.json', 'w', encoding='utf-8') as f:
        json.dump(current_data, f, ensure_ascii=False, indent=2)
    
    print("✅ Données sauvegardées!")
    
    # Régénérer le fichier TypeScript
    print("\n📝 Génération du fichier TypeScript...")
    exec(open('generate_om_typescript.py').read())
    
    print("\n✅ Fichier TypeScript généré!")
    
    print("\n" + "=" * 80)
    print("🎉 TERMINÉ!")
    print("Les joueurs ont maintenant leurs stats de TOUS les clubs où ils ont joué!")

if __name__ == "__main__":
    main()