import requests
import json
import sys
from typing import Dict, Any, Optional

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
        # Ordre de priorité pour extraire les valeurs
        for key in ['total', 'goals', 'average', 'percentage']:
            if key in value:
                return value[key]
        # Si aucune clé connue, prendre la première valeur
        if value:
            return list(value.values())[0]
    return value

def parse_stats_from_details(details: list) -> Dict[str, Any]:
    """Parse les stats depuis le format details avec type_id"""
    stats = {}
    
    for detail in details:
        type_id = str(detail.get("type_id"))
        raw_value = detail.get("value", {})
        value = parse_value(raw_value)
        
        # Mapper avec le code de la stat
        if type_id in TYPE_MAPPING:
            stat_code = TYPE_MAPPING[type_id]["code"]
            stats[stat_code] = value
    
    return stats

def get_om_squad_players() -> list:
    """Récupère la liste des joueurs de l'OM pour la saison actuelle"""
    url = f"{BASE_URL}/squads/seasons/{SEASON_IDS['2025/2026']}/teams/{OM_TEAM_ID}"
    params = {"include": "player"}
    
    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            players = []
            
            for item in data.get("data", []):
                player_id = item.get("player_id")
                if player_id and "player" in item:
                    player_data = item["player"]
                    players.append({
                        "id": player_id,
                        "name": player_data.get("display_name", ""),
                        "position": player_data.get("position", {}).get("name", ""),
                        "jersey": item.get("jersey_number"),
                    })
                elif player_id:
                    # Si pas d'info incluse, on garde juste l'ID
                    players.append({
                        "id": player_id,
                        "name": f"Player_{player_id}",
                        "position": "",
                        "jersey": item.get("jersey_number"),
                    })
            
            return players
    except Exception as e:
        print(f"Erreur récupération effectif: {e}")
    
    return []

def get_player_info(player_id: int) -> Optional[Dict[str, Any]]:
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
        print(f"      ❌ Erreur info: {e}")
    
    return None

def get_player_season_stats(player_id: int, season_id: int) -> Optional[Dict[str, Any]]:
    """Récupère les stats d'un joueur pour une saison"""
    url = f"{BASE_URL}/statistics/seasons/players/{player_id}"
    params = {"seasons": season_id}
    
    try:
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 200:
            data = response.json()
            
            # Trouver les stats de la bonne saison pour l'OM
            for item in data.get("data", []):
                if (item.get("season_id") == season_id and 
                    item.get("team_id") == OM_TEAM_ID and 
                    item.get("has_values")):
                    
                    if "details" in item and len(item["details"]) > 0:
                        # Parser les stats
                        parsed_stats = parse_stats_from_details(item["details"])
                        
                        # Créer l'objet stats complet
                        return {
                            "team": "Olympique Marseille",
                            "team_id": OM_TEAM_ID,
                            "league": "Ligue 1",
                            
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
    except Exception as e:
        pass  # Silencieux pour éviter le spam
    
    return None

def main():
    print("=" * 80)
    print("RÉCUPÉRATION AUTOMATIQUE DE TOUTES LES STATS OM DEPUIS L'API")
    print("=" * 80)
    
    # Récupérer l'effectif actuel
    print(f"\n📋 Récupération de l'effectif OM...")
    
    squad = get_om_squad_players()
    
    if not squad:
        print("❌ Impossible de récupérer l'effectif")
        return
    
    print(f"✅ {len(squad)} joueurs trouvés dans l'effectif")
    
    # Structure pour stocker toutes les données
    all_players_data = {}
    
    # Pour chaque joueur
    for idx, player_squad_info in enumerate(squad, 1):
        player_id = player_squad_info["id"]
        
        # Récupérer les infos complètes du joueur
        print(f"\n[{idx}/{len(squad)}] Joueur ID {player_id}...", end=" ")
        player_info = get_player_info(player_id)
        
        if not player_info:
            print("❌ Pas d'info")
            continue
            
        player_name = player_info["displayName"]
        print(f"👤 {player_name}")
        
        # Créer la structure du joueur
        player_data = {
            "displayName": player_name,
            "position": player_info["position"] or player_squad_info.get("position", ""),
            "jersey": player_squad_info.get("jersey") or player_info.get("jersey"),
            "stats": {}
        }
        
        # Récupérer les stats pour chaque saison
        has_any_stats = False
        for season_name, season_id in SEASON_IDS.items():
            stats = get_player_season_stats(player_id, season_id)
            
            if stats and stats.get("appearences", 0) > 0:
                season_key = f"{season_name} (Ligue 1, Olympique Marseille)"
                player_data["stats"][season_key] = stats
                has_any_stats = True
                print(f"     ✅ {season_name}: {stats['appearences']} matchs")
        
        # Ajouter le joueur aux données seulement s'il a des stats
        if has_any_stats:
            all_players_data[str(player_id)] = player_data
        else:
            print(f"     ⚫ Aucune statistique")
    
    # Sauvegarder les données
    print("\n" + "=" * 80)
    print("💾 Sauvegarde des données...")
    
    with open('om_complete_stats_api.json', 'w', encoding='utf-8') as f:
        json.dump(all_players_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Données sauvegardées pour {len(all_players_data)} joueurs avec des statistiques")
    
    # Générer le fichier TypeScript
    print("\n📝 Génération du fichier TypeScript...")
    
    # Code pour générer le fichier TS
    ts_content = """// Auto-generated from SportMonks API
// Last updated: """ + str(__import__('datetime').datetime.now()) + """

export interface PlayerStats {
  displayName: string;
  position: string;
  jersey: number | null;
  stats: {
    [season: string]: {
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
    };
  };
}

export const omPlayersCompleteStats: { [key: string]: PlayerStats } = """ + json.dumps(all_players_data, ensure_ascii=False, indent=2) + ";"
    
    with open('../data/omPlayersCompleteStats.ts', 'w', encoding='utf-8') as f:
        f.write(ts_content)
    
    print("✅ Fichier TypeScript généré!")
    
    print("\n" + "=" * 80)
    print("🎉 TERMINÉ - Toutes les stats ont été récupérées depuis l'API!")
    print("=" * 80)

if __name__ == "__main__":
    main()