import json
import requests
import time
from dotenv import load_dotenv
import os
import sys

# Fix pour l'encodage UTF-8 sur Windows
sys.stdout.reconfigure(encoding='utf-8')

# Charger les variables d'environnement
load_dotenv('../.env.local')
API_KEY = os.getenv('SPORTMONKS_API_TOKEN')

if not API_KEY:
    print("Cle API SportMonks manquante dans .env.local")
    exit(1)

BASE_URL = "https://api.sportmonks.com/v3/football"

# IDs des saisons
SEASONS = {
    "2025/2026": 23435,  # Ligue 1 2025/2026
    "2024/2025": 21792,  # Ligue 1 2024/2025
    "2023/2024": 19735,  # Ligue 1 2023/2024
}

# ID de l'OM
OM_TEAM_ID = 44

def get_team_stats_for_season(season_id, season_name):
    """Récupère les stats de tous les joueurs de l'OM pour une saison"""
    
    url = f"{BASE_URL}/squads/seasons/{season_id}/teams/{OM_TEAM_ID}"
    params = {
        'api_token': API_KEY,
        'include': 'player;details.type'
    }
    
    print(f"\nRecuperation des stats pour la saison {season_name} (ID: {season_id})...")
    
    try:
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            if 'data' in data:
                return data['data']
        elif response.status_code == 429:
            print("Rate limit atteint, pause de 60 secondes...")
            time.sleep(60)
            return get_team_stats_for_season(season_id, season_name)
        else:
            print(f"Erreur API: {response.status_code}")
            print(response.text)
            return None
    except Exception as e:
        print(f"Erreur: {e}")
        return None

def map_stats_to_categories(player_data):
    """Mappe les stats SportMonks vers nos catégories"""
    
    stats = {}
    details = player_data.get('details', []) if player_data else []
    
    # Initialiser toutes les stats à 0
    all_stats = {
        # Général
        'rating': 0,
        'minutes': 0,
        'appearences': 0,
        'lineups': 0,
        'captain': 0,
        'substitutions': 0,
        'touches': 0,
        'saves': 0,
        'punches': 0,
        
        # Offensif
        'goals': 0,
        'assists': 0,
        'shots': 0,
        'shots_on_target': 0,
        'xg': 0,
        'xa': 0,
        'offsides': 0,
        'penalties': 0,
        'penalties_scored': 0,
        'penalties_missed': 0,
        'hit_woodwork': 0,
        
        # Défensif
        'tackles': 0,
        'blocks': 0,
        'interceptions': 0,
        'clearances': 0,
        'aerial_duels': 0,
        'aerial_duels_won': 0,
        'ground_duels': 0,
        'ground_duels_won': 0,
        'fouls': 0,
        'fouls_drawn': 0,
        'yellow_cards': 0,
        'red_cards': 0,
        'clean_sheets': 0,
        'goals_conceded': 0,
        
        # Créatif
        'passes': 0,
        'passes_completed': 0,
        'passes_accuracy': 0,
        'key_passes': 0,
        'crosses': 0,
        'crosses_accurate': 0,
        'long_balls': 0,
        'long_balls_accurate': 0,
        'through_balls': 0,
        'through_balls_accurate': 0,
        'dribbles': 0,
        'dribbles_successful': 0,
        'progressive_carries': 0,
        'big_chances_created': 0
    }
    
    # Mapper les stats depuis les détails
    stat_mapping = {
        # Général
        'rating': 'rating',
        'minutes_played': 'minutes',
        'appearances': 'appearences',
        'lineups': 'lineups',
        'captain': 'captain',
        'substitutions': 'substitutions',
        'touches': 'touches',
        'saves': 'saves',
        'punches': 'punches',
        
        # Offensif
        'goals': 'goals',
        'assists': 'assists',
        'shots_total': 'shots',
        'shots_on_target': 'shots_on_target',
        'expected_goals': 'xg',
        'expected_assists': 'xa',
        'offsides': 'offsides',
        'penalties': 'penalties',
        'penalties_scored': 'penalties_scored',
        'penalties_missed': 'penalties_missed',
        'hit_woodwork': 'hit_woodwork',
        
        # Défensif
        'tackles': 'tackles',
        'blocks': 'blocks',
        'interceptions': 'interceptions',
        'clearances': 'clearances',
        'aerial_duels': 'aerial_duels',
        'aerial_duels_won': 'aerial_duels_won',
        'ground_duels': 'ground_duels',
        'ground_duels_won': 'ground_duels_won',
        'fouls': 'fouls',
        'fouls_drawn': 'fouls_drawn',
        'yellowcards': 'yellow_cards',
        'redcards': 'red_cards',
        'clean_sheets': 'clean_sheets',
        'goals_conceded': 'goals_conceded',
        
        # Créatif
        'passes_total': 'passes',
        'passes_accurate': 'passes_completed',
        'passes_accuracy': 'passes_accuracy',
        'key_passes': 'key_passes',
        'crosses_total': 'crosses',
        'crosses_accurate': 'crosses_accurate',
        'long_balls': 'long_balls',
        'long_balls_accurate': 'long_balls_accurate',
        'through_balls': 'through_balls',
        'through_balls_accurate': 'through_balls_accurate',
        'dribbles_attempts': 'dribbles',
        'dribbles_success': 'dribbles_successful',
        'progressive_carries': 'progressive_carries',
        'big_chances_created': 'big_chances_created'
    }
    
    # Parcourir les détails et mapper les stats
    for detail in details:
        if 'type' in detail:
            type_data = detail['type']
            type_name = type_data.get('code', '').lower()
            
            # Utiliser le mapping pour assigner la valeur
            if type_name in stat_mapping:
                stat_key = stat_mapping[type_name]
                value = detail.get('value', 0)
                
                # Gérer les valeurs None ou string
                if value is None:
                    value = 0
                elif isinstance(value, str):
                    try:
                        value = float(value)
                    except:
                        value = 0
                        
                all_stats[stat_key] = value
    
    # Calculer les pourcentages si nécessaire
    if all_stats['passes'] > 0 and all_stats['passes_accuracy'] == 0:
        all_stats['passes_accuracy'] = (all_stats['passes_completed'] / all_stats['passes']) * 100
    
    return all_stats

def process_om_stats():
    """Process et sauvegarde les stats de l'OM"""
    
    all_players_stats = {}
    
    for season_name, season_id in SEASONS.items():
        squad_data = get_team_stats_for_season(season_id, season_name)
        
        if squad_data:
            print(f"  {len(squad_data)} joueurs trouves pour {season_name}")
            
            for player_squad in squad_data:
                player = player_squad.get('player', {})
                player_id = player.get('id')
                player_name = player.get('display_name', player.get('name', 'Unknown'))
                
                if player_id:
                    if player_id not in all_players_stats:
                        all_players_stats[player_id] = {
                            'id': player_id,
                            'name': player_name,
                            'display_name': player.get('display_name'),
                            'position': player.get('position', {}).get('name') if player.get('position') else 'Unknown',
                            'jersey': player_squad.get('jersey_number'),
                            'stats': {}
                        }
                    
                    # Mapper les stats
                    stats = map_stats_to_categories(player_squad)
                    all_players_stats[player_id]['stats'][season_name] = stats
                    
                    print(f"    - {player_name}: {stats.get('appearences', 0)} matchs, {stats.get('goals', 0)} buts")
        
        # Pause entre les requêtes
        time.sleep(2)
    
    # Sauvegarder les résultats
    output_file = 'om_real_stats.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_players_stats, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Stats sauvegardees dans {output_file}")
    print(f"Total: {len(all_players_stats)} joueurs avec stats")
    
    # Créer aussi un fichier TypeScript
    create_typescript_file(all_players_stats)

def create_typescript_file(players_stats):
    """Créé un fichier TypeScript avec les stats"""
    
    ts_content = """// Stats réelles des joueurs de l'OM depuis SportMonks API
// Généré automatiquement

export interface PlayerSeasonStats {
  rating: number;
  minutes: number;
  appearences: number;
  lineups: number;
  captain: number;
  substitutions: number;
  touches: number;
  saves: number;
  punches: number;
  goals: number;
  assists: number;
  shots: number;
  shots_on_target: number;
  xg: number;
  xa: number;
  offsides: number;
  penalties: number;
  penalties_scored: number;
  penalties_missed: number;
  hit_woodwork: number;
  tackles: number;
  blocks: number;
  interceptions: number;
  clearances: number;
  aerial_duels: number;
  aerial_duels_won: number;
  ground_duels: number;
  ground_duels_won: number;
  fouls: number;
  fouls_drawn: number;
  yellow_cards: number;
  red_cards: number;
  clean_sheets: number;
  goals_conceded: number;
  passes: number;
  passes_completed: number;
  passes_accuracy: number;
  key_passes: number;
  crosses: number;
  crosses_accurate: number;
  long_balls: number;
  long_balls_accurate: number;
  through_balls: number;
  through_balls_accurate: number;
  dribbles: number;
  dribbles_successful: number;
  progressive_carries: number;
  big_chances_created: number;
}

export interface PlayerRealStats {
  id: number;
  name: string;
  display_name?: string;
  position: string;
  jersey?: number;
  stats: {
    [season: string]: PlayerSeasonStats;
  };
}

export const omRealStats: { [playerId: number]: PlayerRealStats } = """
    
    # Ajouter les données
    ts_content += json.dumps(players_stats, indent=2, ensure_ascii=False)
    ts_content += ";\n"
    
    # Sauvegarder
    with open('../data/omRealStats.ts', 'w', encoding='utf-8') as f:
        f.write(ts_content)
    
    print("✅ Fichier TypeScript cree: data/omRealStats.ts")

if __name__ == "__main__":
    print("🚀 Demarrage de la recuperation des stats reelles de l'OM...")
    process_om_stats()
    print("\n✅ Termine!")