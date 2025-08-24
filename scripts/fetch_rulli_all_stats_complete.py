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

# Charger le mapping des types
with open('sportmonks_types_mapping.json', 'r', encoding='utf-8') as f:
    TYPE_MAPPING = json.load(f)

player_id = 186418  # Rulli
OM_TEAM_ID = 44

SEASON_IDS = {
    "2025/2026": 25651,
    "2024/2025": 23643,
    "2023/2024": 21779,
}

def parse_value(value: Any) -> Any:
    """Extrait la valeur depuis différents formats de l'API"""
    if isinstance(value, dict):
        # Ordre de priorité pour extraire les valeurs
        for key in ['total', 'goals', 'average', 'percentage', 'count']:
            if key in value:
                return value[key]
        # Si aucune clé connue, prendre la première valeur
        if value:
            return list(value.values())[0]
    return value

def get_all_player_stats_methods(player_id: int, season_id: int, season_name: str) -> Dict[str, Any]:
    """Essaye toutes les méthodes pour récupérer les stats complètes"""
    
    all_stats = {}
    print(f"\n📊 Récupération complète pour {season_name}:")
    print("-" * 60)
    
    # Méthode 1: Endpoint principal avec tous les includes possibles
    print("  1️⃣ Endpoint principal avec includes...")
    url = f"{BASE_URL}/statistics/seasons/players/{player_id}"
    includes = [
        "details",
        "metadata", 
        "position",
        "team",
        "statistics",
        "stats"
    ]
    
    for include in includes:
        params = {
            "seasons": season_id,
            "include": include
        }
        
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
                                    # Garder la valeur max si on a plusieurs sources
                                    if stat_code not in all_stats or (value and value > all_stats.get(stat_code, 0)):
                                        all_stats[stat_code] = value
        except:
            pass
    
    # Méthode 2: Endpoint player avec statistics
    print("  2️⃣ Endpoint player avec statistics...")
    url = f"{BASE_URL}/players/{player_id}"
    params = {
        "include": "statistics.details,statistics.season,position"
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            player_data = data.get("data", {})
            
            if "statistics" in player_data:
                for stat in player_data["statistics"]:
                    if stat.get("season_id") == season_id and stat.get("team_id") == OM_TEAM_ID:
                        if "details" in stat:
                            for detail in stat["details"]:
                                type_id = str(detail.get("type_id"))
                                value = parse_value(detail.get("value", {}))
                                
                                if type_id in TYPE_MAPPING and value is not None:
                                    stat_code = TYPE_MAPPING[type_id]["code"]
                                    if stat_code not in all_stats or (value and value > all_stats.get(stat_code, 0)):
                                        all_stats[stat_code] = value
    except:
        pass
    
    # Méthode 3: Endpoint teams/squad avec statistics
    print("  3️⃣ Endpoint teams/squad avec player statistics...")
    url = f"{BASE_URL}/squads/seasons/{season_id}/teams/{OM_TEAM_ID}"
    params = {
        "include": "player.statistics.details,player.position"
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            for squad_entry in data.get("data", []):
                if squad_entry.get("player_id") == player_id:
                    if "player" in squad_entry and "statistics" in squad_entry["player"]:
                        for stat in squad_entry["player"]["statistics"]:
                            if "details" in stat:
                                for detail in stat["details"]:
                                    type_id = str(detail.get("type_id"))
                                    value = parse_value(detail.get("value", {}))
                                    
                                    if type_id in TYPE_MAPPING and value is not None:
                                        stat_code = TYPE_MAPPING[type_id]["code"]
                                        if stat_code not in all_stats or (value and value > all_stats.get(stat_code, 0)):
                                            all_stats[stat_code] = value
    except:
        pass
    
    # Méthode 4: Fixtures endpoint pour stats par match
    print("  4️⃣ Agrégation depuis les matchs individuels...")
    url = f"{BASE_URL}/fixtures"
    params = {
        "filters": f"teamIds:{OM_TEAM_ID};seasonIds:{season_id}",
        "include": "statistics,events,lineups.player"
    }
    
    match_stats = {
        "penalties_saved": 0,
        "punches": 0,
        "goals_conceded_real": 0,
        "clean_sheets_real": 0,
        "matches_played": 0
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            
            for fixture in data.get("data", []):
                # Vérifier si Rulli a joué
                if "lineups" in fixture:
                    rulli_played = False
                    for lineup in fixture["lineups"]:
                        if lineup.get("player_id") == player_id:
                            rulli_played = True
                            break
                    
                    if rulli_played:
                        match_stats["matches_played"] += 1
                        
                        # Analyser les scores
                        scores = fixture.get("scores", {})
                        if scores:
                            om_is_home = fixture.get("participants", [{}])[0].get("id") == OM_TEAM_ID
                            
                            if om_is_home:
                                goals_against = scores.get("away_score", 0)
                            else:
                                goals_against = scores.get("home_score", 0)
                            
                            match_stats["goals_conceded_real"] += goals_against
                            if goals_against == 0:
                                match_stats["clean_sheets_real"] += 1
                        
                        # Analyser les événements pour penalties
                        if "events" in fixture:
                            for event in fixture["events"]:
                                # Type 83 = Penalty, vérifier si arrêté par Rulli
                                if event.get("type_id") == 83:
                                    # Vérifier le résultat du penalty
                                    if event.get("result") == "missed" or event.get("result") == "saved":
                                        # Vérifier si c'était contre l'OM
                                        if event.get("participant_id") != OM_TEAM_ID:
                                            match_stats["penalties_saved"] += 1
    except Exception as e:
        print(f"      Erreur: {e}")
    
    # Ajouter les stats des matchs si on en a trouvé
    if match_stats["matches_played"] > 0:
        print(f"      ✅ {match_stats['matches_played']} matchs analysés")
        if match_stats["penalties_saved"] > 0:
            all_stats["penalties-saved"] = match_stats["penalties_saved"]
            print(f"      🎯 Penalties arrêtés trouvés: {match_stats['penalties_saved']}")
        if match_stats["clean_sheets_real"] > 0:
            all_stats["cleansheets"] = max(all_stats.get("cleansheets", 0), match_stats["clean_sheets_real"])
    
    # Méthode 5: Player performance endpoint
    print("  5️⃣ Endpoint player performance...")
    url = f"{BASE_URL}/players/{player_id}/seasons/{season_id}"
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            # Parser les données si disponibles
    except:
        pass
    
    print(f"      📊 Total stats récupérées: {len(all_stats)}")
    
    return all_stats

def create_complete_stats_object(stats: Dict[str, Any]) -> Dict[str, Any]:
    """Crée l'objet complet des stats avec toutes les valeurs"""
    return {
        "team": "Olympique Marseille",
        "team_id": OM_TEAM_ID,
        "league": "Ligue 1",
        
        # Stats générales
        "rating": stats.get("rating"),
        "minutes": stats.get("minutes-played", 0),
        "appearences": stats.get("appearances", 0),
        "lineups": stats.get("lineups", 0),
        "captain": stats.get("captain", 0),
        "touches": stats.get("touches", 0),
        
        # Stats gardien
        "saves": stats.get("saves", 0),
        "goals_conceded": stats.get("goals-conceded", 0),
        "clean_sheets": stats.get("cleansheets", stats.get("goalkeeper-cleansheets", 0)),
        "penalties_saved": stats.get("penalties-saved", 0),
        "punches": stats.get("punches", 0),
        "inside_box_saves": stats.get("saves-insidebox", 0),
        
        # Passes
        "passes": stats.get("passes", 0),
        "passes_completed": stats.get("accurate-passes", 0),
        "passes_accuracy": stats.get("accurate-passes-percentage"),
        "key_passes": stats.get("key-passes", 0),
        "crosses": stats.get("total-crosses", 0),
        "crosses_accurate": stats.get("accurate-crosses", 0),
        
        # Défense
        "tackles": stats.get("tackles", 0),
        "blocks": stats.get("blocked-shots", 0),
        "interceptions": stats.get("interceptions", 0),
        "clearances": stats.get("clearances", 0),
        
        # Discipline
        "fouls": stats.get("fouls", 0),
        "fouls_drawn": stats.get("fouls-drawn", 0),
        "yellow_cards": stats.get("yellowcards", 0),
        "red_cards": stats.get("redcards", 0),
        "yellowred_cards": stats.get("yellowred-cards", 0),
        
        # Duels
        "ground_duels": stats.get("ground-duels", 0),
        "ground_duels_won": stats.get("ground-duels-won", 0),
        "aerial_duels": stats.get("aeriels", 0),
        "aerial_duels_won": stats.get("aeriels-won", 0),
        "duels": stats.get("total-duels", 0),
        "duels_won": stats.get("duels-won", 0),
        
        # Dribbles
        "dribbles": stats.get("dribbles-attempted", 0),
        "dribbles_successful": stats.get("dribbles-succeeded", 0),
        
        # Penalties
        "penalties": stats.get("penalties", 0),
        "penalties_won": stats.get("penalties-won", 0),
        "penalties_scored": stats.get("penalties-scored", 0),
        "penalties_missed": stats.get("penalties-missed", 0),
        "penalties_committed": stats.get("penalties-committed", 0),
        
        # Autres
        "offsides": stats.get("offsides", 0),
        "ball_losses": stats.get("dispossessed", 0),
        "ball_recoveries": stats.get("ball-recoveries", 0),
        "mistakes_leading_to_goals": stats.get("error-lead-to-goal", 0),
        
        # Non utilisés pour gardien mais requis
        "goals": stats.get("goals", 0),
        "assists": stats.get("assists", 0),
        "xg": stats.get("expected-goals"),
        "xa": stats.get("expected-assists"),
        "shots": stats.get("shots-total", 0),
        "shots_on_target": stats.get("shots-on-target", 0),
        "hit_woodwork": stats.get("hit-woodwork", 0),
    }

def main():
    print("=" * 80)
    print("RÉCUPÉRATION COMPLÈTE DE TOUTES LES STATS DE RULLI")
    print("=" * 80)
    
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
    
    # Récupérer TOUTES les stats pour chaque saison
    for season_name, season_id in SEASON_IDS.items():
        all_stats = get_all_player_stats_methods(player_id, season_id, season_name)
        
        if all_stats and all_stats.get("appearances", 0) > 0:
            season_key = f"{season_name} (Ligue 1, Olympique Marseille)"
            stats_obj = create_complete_stats_object(all_stats)
            rulli_data["stats"][season_key] = stats_obj
            
            # Afficher les stats clés
            print(f"\n   📈 Résumé {season_name}:")
            print(f"      - Matchs: {stats_obj['appearences']}")
            print(f"      - Minutes: {stats_obj['minutes']}")
            print(f"      - Buts encaissés: {stats_obj['goals_conceded']}")
            print(f"      - Clean sheets: {stats_obj['clean_sheets']}")
            print(f"      - Arrêts: {stats_obj['saves']}")
            print(f"      - Arrêts dans la surface: {stats_obj['inside_box_saves']}")
            print(f"      - Penalties arrêtés: {stats_obj['penalties_saved']}")
            print(f"      - Dégagements du poing: {stats_obj['punches']}")
            print(f"      - Note moyenne: {stats_obj['rating']}")
    
    # Mettre à jour les données
    if rulli_data["stats"]:
        data['186418'] = rulli_data
        
        # Sauvegarder
        with open('om_complete_stats_v2.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print("\n✅ Données de Rulli mises à jour avec TOUTES les méthodes API!")
        
        # Régénérer le fichier TypeScript
        print("\n📝 Régénération du fichier TypeScript...")
        exec(open('generate_om_typescript.py').read())
        
        print("\n✅ Fichier TypeScript mis à jour!")
    else:
        print("\n⚠️ Aucune donnée trouvée pour Rulli")

if __name__ == "__main__":
    main()