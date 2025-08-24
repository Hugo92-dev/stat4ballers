import requests
import json
import sys
import time

# Fix pour l'encodage UTF-8 sur Windows
sys.stdout.reconfigure(encoding='utf-8')

API_KEY = "C3Wid19g74gH2DUPrtoJPpRx8w7obNSgSWpBD8rIoq66HJCEjxFSe3OwCJHF"
BASE_URL = "https://api.sportmonks.com/v3/football"

# Headers pour l'API
headers = {
    "Accept": "application/json",
    "Authorization": API_KEY,
}

# IDs des saisons pour tous les championnats
ALL_SEASON_IDS = {
    # Ligue 1
    21779: {"league": "Ligue 1", "year": "2023/2024"},
    23643: {"league": "Ligue 1", "year": "2024/2025"},
    25651: {"league": "Ligue 1", "year": "2025/2026"},
    # Liga
    21694: {"league": "Liga", "year": "2023/2024"},
    23642: {"league": "Liga", "year": "2024/2025"}, 
    25650: {"league": "Liga", "year": "2025/2026"},
    # Premier League
    21781: {"league": "Premier League", "year": "2023/2024"},
    23645: {"league": "Premier League", "year": "2024/2025"},
    25653: {"league": "Premier League", "year": "2025/2026"},
    # Serie A
    22037: {"league": "Serie A", "year": "2023/2024"},
    23644: {"league": "Serie A", "year": "2024/2025"},
    25652: {"league": "Serie A", "year": "2025/2026"},
    # Bundesliga
    21687: {"league": "Bundesliga", "year": "2023/2024"},
    23641: {"league": "Bundesliga", "year": "2024/2025"},
    25649: {"league": "Bundesliga", "year": "2025/2026"},
}

def get_player_stats(player_id, season_id, team_id=None):
    """Récupère les stats d'un joueur pour une saison"""
    url = f"{BASE_URL}/statistics/seasons/players/{player_id}"
    params = {
        "seasons": season_id,
        "include": "details,teams",
    }
    
    # Si on cherche pour une équipe spécifique
    if team_id:
        params["filters"] = f"teamID:{team_id}"
    
    try:
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 200:
            data = response.json()
            if data and "data" in data and len(data["data"]) > 0:
                stats = data["data"][0]
                
                # Récupérer l'équipe
                team_name = "Unknown"
                team_id = None
                if "teams" in stats and len(stats["teams"]) > 0:
                    team_name = stats["teams"][0].get("name", "Unknown")
                    team_id = stats["teams"][0].get("id")
                
                # Récupérer les details
                details = stats.get("details", [])
                if details and len(details) > 0:
                    detail = details[0]
                    
                    # Créer l'objet stat
                    return {
                        "team": team_name,
                        "team_id": team_id,
                        "league": ALL_SEASON_IDS[season_id]["league"],
                        "rating": detail.get("rating"),
                        "minutes": detail.get("minutes", 0) or 0,
                        "appearences": detail.get("games", {}).get("appearences", 0) or 0,
                        "lineups": detail.get("games", {}).get("lineups", 0) or 0,
                        "captain": detail.get("games", {}).get("captain", 0) or 0,
                        "goals": detail.get("goals", {}).get("overall", 0) or 0,
                        "assists": detail.get("goals", {}).get("assists", 0) or 0,
                        "xg": detail.get("xg"),
                        "xa": detail.get("xa"),
                        "saves": detail.get("goalkeeper", {}).get("saves", 0) or 0,
                        "goals_conceded": detail.get("goalkeeper", {}).get("goals_conceded", 0) or 0,
                        "clean_sheets": detail.get("goalkeeper", {}).get("cleansheets", 0) or 0,
                        "punches": detail.get("goalkeeper", {}).get("punches", 0) or 0,
                        "inside_box_saves": detail.get("goalkeeper", {}).get("inside_box_saves"),
                        "shots": detail.get("shots", {}).get("overall", 0) or 0,
                        "shots_on_target": detail.get("shots", {}).get("on_target", 0) or 0,
                        "passes": detail.get("passes", {}).get("overall", 0) or 0,
                        "passes_completed": detail.get("passes", {}).get("completed", 0) or 0,
                        "passes_accuracy": detail.get("passes", {}).get("accuracy"),
                        "key_passes": detail.get("passes", {}).get("key_passes", 0) or 0,
                        "crosses": detail.get("crosses", {}).get("overall", 0) or 0,
                        "crosses_accurate": detail.get("crosses", {}).get("accurate", 0) or 0,
                        "dribbles": detail.get("dribbles", {}).get("attempts", 0) or 0,
                        "dribbles_successful": detail.get("dribbles", {}).get("dribbled_past", 0) or 0,
                        "fouls": detail.get("fouls", {}).get("overall", 0) or 0,
                        "fouls_drawn": detail.get("fouls", {}).get("drawn", 0) or 0,
                        "yellow_cards": detail.get("cards", {}).get("yellow_cards", 0) or 0,
                        "red_cards": detail.get("cards", {}).get("red_cards", 0) or 0,
                        "tackles": detail.get("defensive", {}).get("tackles", 0) or 0,
                        "blocks": detail.get("defensive", {}).get("blocks", 0) or 0,
                        "interceptions": detail.get("defensive", {}).get("interceptions", 0) or 0,
                        "clearances": detail.get("defensive", {}).get("clearances", 0) or 0,
                        "penalties_won": detail.get("penalties", {}).get("won", 0) or 0,
                        "penalties_scored": detail.get("penalties", {}).get("scored", 0) or 0,
                        "penalties_missed": detail.get("penalties", {}).get("missed", 0) or 0,
                        "penalties_committed": detail.get("penalties", {}).get("committed", 0) or 0,
                        "penalties": detail.get("penalties", {}).get("scored", 0) or 0,
                        "hit_woodwork": detail.get("hit_woodwork", 0) or 0,
                        "offsides": detail.get("offsides", 0) or 0,
                        "ground_duels": detail.get("duels", {}).get("ground", {}).get("overall", 0) or 0,
                        "ground_duels_won": detail.get("duels", {}).get("ground", {}).get("won", 0) or 0,
                        "aerial_duels": detail.get("duels", {}).get("aerial", {}).get("overall", 0) or 0,
                        "aerial_duels_won": detail.get("duels", {}).get("aerial", {}).get("won", 0) or 0,
                        "ball_losses": detail.get("ball_losses", 0) or 0,
                        "ball_recoveries": detail.get("ball_recoveries", 0) or 0,
                        "yellowred_cards": detail.get("cards", {}).get("yellowred_cards", 0) or 0,
                        "mistakes_leading_to_goals": detail.get("mistakes_leading_to_goals", 0) or 0,
                        "touches": detail.get("touches", 0) or 0,
                        "crosses_accuracy": None,  # Calculé après
                    }
                    
        elif response.status_code == 429:
            print(f"⏱️ Rate limit atteinte, pause de 65 secondes...")
            time.sleep(65)
            return get_player_stats(player_id, season_id)
            
    except Exception as e:
        print(f"❌ Erreur pour le joueur {player_id} saison {season_id}: {e}")
    
    return None

# Charger les données existantes
with open('om_complete_stats_v2.json', 'r', encoding='utf-8') as f:
    existing_data = json.load(f)

# Rulli
player_id = 186418
player_name = "Gerónimo Rulli"

print(f"\n📊 Récupération des stats de {player_name} (ID: {player_id})")

# Créer la structure pour Rulli
rulli_data = {
    "displayName": "Gerónimo Rulli",
    "position": "GK",
    "jersey": 1,
    "stats": {}
}

# Récupérer les stats pour chaque saison
# Pour l'OM (team_id = 44)
om_seasons = [25651, 23643, 21779]  # Ligue 1 saisons
other_seasons = [21694, 23642]  # Liga pour Villarreal
stats_found = False

# D'abord chercher à l'OM
for season_id in om_seasons:
    season_info = ALL_SEASON_IDS[season_id]
    print(f"  Vérification {season_info['year']} ({season_info['league']}) avec l'OM...")
    
    stats = get_player_stats(player_id, season_id, team_id=44)  # 44 = OM
    
    if stats and stats.get("appearences", 0) > 0:
        # Calculer la précision des centres
        if stats["crosses"] and stats["crosses"] > 0:
            stats["crosses_accuracy"] = (stats["crosses_accurate"] / stats["crosses"]) * 100
        
        season_key = f"{season_info['year']} ({season_info['league']}, {stats['team']})"
        rulli_data["stats"][season_key] = stats
        print(f"    ✅ Trouvé: {stats['appearences']} matchs avec {stats['team']}")
        stats_found = True
    else:
        # S'il n'a pas joué mais fait partie de l'équipe
        season_key = f"{season_info['year']} ({season_info['league']}, Olympique Marseille)"
        if season_info['year'] in ["2025/2026", "2024/2025"]:
            # Il était à l'OM ces saisons, mettre des null pour indiquer qu'on n'a pas les données
            rulli_data["stats"][season_key] = {k: None for k in ["rating", "minutes", "appearences", "lineups", "goals", "assists", "saves", "clean_sheets", "goals_conceded"]}
            print(f"    ⚠️ Pas de données trouvées pour cette saison à l'OM")

# Chercher dans d'autres équipes (Villarreal pour 2023/2024)
for season_id in other_seasons:
    season_info = ALL_SEASON_IDS[season_id]
    print(f"  Vérification {season_info['year']} ({season_info['league']}) autres clubs...")
    
    stats = get_player_stats(player_id, season_id)  # Sans filtre d'équipe
    
    if stats and stats.get("appearences", 0) > 0:
        # Calculer la précision des centres
        if stats["crosses"] and stats["crosses"] > 0:
            stats["crosses_accuracy"] = (stats["crosses_accurate"] / stats["crosses"]) * 100
        
        season_key = f"{season_info['year']} ({season_info['league']}, {stats['team']})"
        rulli_data["stats"][season_key] = stats
        print(f"    ✅ Trouvé: {stats['appearences']} matchs avec {stats['team']}")
        stats_found = True

# Ajouter aux données existantes
existing_data[str(player_id)] = rulli_data

# Sauvegarder
with open('om_complete_stats_v2.json', 'w', encoding='utf-8') as f:
    json.dump(existing_data, f, ensure_ascii=False, indent=2)

print(f"\n✅ Données de {player_name} ajoutées et fichier mis à jour!")

# Afficher un résumé
if stats_found:
    print(f"\n📈 Résumé pour {player_name}:")
    for season_key, stats in rulli_data["stats"].items():
        if stats and stats.get("appearences"):
            print(f"  - {season_key}: {stats['appearences']} matchs, {stats.get('clean_sheets', 0)} clean sheets")