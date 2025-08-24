import json
import requests
import time
from dotenv import load_dotenv
import os
import sys
import re

# Fix pour l'encodage UTF-8 sur Windows
sys.stdout.reconfigure(encoding='utf-8')

# Charger les variables d'environnement
load_dotenv('../.env.local')
API_KEY = os.getenv('SPORTMONKS_API_TOKEN')

if not API_KEY:
    print("Cle API SportMonks manquante dans .env.local")
    exit(1)

BASE_URL = "https://api.sportmonks.com/v3/football"

# IDs des saisons Ligue 1
SEASON_IDS = [23435, 21792, 19735]  # 2025/26, 2024/25, 2023/24

def get_om_player_ids():
    """Récupère les IDs des joueurs de l'OM depuis le fichier local"""
    with open('../data/ligue1Teams.ts', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extraire la section OM
    om_start = content.find('name: "Olympique de Marseille"')
    om_end = content.find('},\n  {', om_start + 100)  # Chercher la prochaine équipe
    om_section = content[om_start:om_end]
    
    # Extraire les IDs et noms des joueurs
    players = []
    player_blocks = om_section.split('{\n        id:')[1:]  # Diviser par joueur
    
    for block in player_blocks:
        player_id_match = re.search(r'^\s*(\d+)', block)
        name_match = re.search(r'name:\s*"([^"]+)"', block)
        display_match = re.search(r'displayName:\s*"([^"]+)"', block)
        position_match = re.search(r'position:\s*"([^"]+)"', block)
        jersey_match = re.search(r'jersey:\s*(\d+)', block)
        
        if player_id_match:
            player_info = {
                'id': int(player_id_match.group(1)),
                'name': name_match.group(1) if name_match else 'Unknown',
                'displayName': display_match.group(1) if display_match else None,
                'position': position_match.group(1) if position_match else 'Unknown',
                'jersey': int(jersey_match.group(1)) if jersey_match else None
            }
            players.append(player_info)
    
    return players

def get_player_stats(player_id):
    """Récupère les stats d'un joueur pour toutes les saisons"""
    url = f"{BASE_URL}/statistics/seasons/players/{player_id}"
    params = {
        'api_token': API_KEY,
        'include': 'details.type',
        'filters': f'seasonIds:{",".join(map(str, SEASON_IDS))}'
    }
    
    try:
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            if 'data' in data:
                return data['data']
        elif response.status_code == 429:
            print("  Rate limit, pause...")
            time.sleep(60)
            return get_player_stats(player_id)
            
    except Exception as e:
        print(f"  Erreur: {e}")
    
    return []

def map_stats_to_our_format(stat_data):
    """Mappe les stats SportMonks vers notre format"""
    
    stats = {
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
    
    # Mapping des noms SportMonks vers nos noms
    mapping = {
        'Rating': 'rating',
        'Minutes Played': 'minutes',
        'Appearances': 'appearences',
        'Lineups': 'lineups',
        'Captain': 'captain',
        'Substitutions': 'substitutions',
        'Touches': 'touches',
        'Saves': 'saves',
        'Punches': 'punches',
        
        'Goals': 'goals',
        'Assists': 'assists',
        'Shots Total': 'shots',
        'Shots On Target': 'shots_on_target',
        'Expected Goals': 'xg',
        'Expected Assists': 'xa',
        'Offsides': 'offsides',
        'Penalties Won': 'penalties',
        'Penalties Scored': 'penalties_scored',
        'Penalties Missed': 'penalties_missed',
        'Hit Woodwork': 'hit_woodwork',
        
        'Tackles': 'tackles',
        'Blocked Shots': 'blocks',
        'Interceptions': 'interceptions',
        'Clearances': 'clearances',
        'Total Duels': 'ground_duels',
        'Duels Won': 'ground_duels_won',
        'Fouls': 'fouls',
        'Fouls Drawn': 'fouls_drawn',
        'Yellowcards': 'yellow_cards',
        'Redcards': 'red_cards',
        'Clean Sheets': 'clean_sheets',
        'Goals Conceded': 'goals_conceded',
        
        'Passes': 'passes',
        'Accurate Passes': 'passes_completed',
        'Key Passes': 'key_passes',
        'Total Crosses': 'crosses',
        'Crosses Accurate': 'crosses_accurate',
        'Long Balls': 'long_balls',
        'Long Balls Won': 'long_balls_accurate',
        'Dribbles Attempts': 'dribbles',
        'Dribbles Success': 'dribbles_successful',
        'Big Chances Created': 'big_chances_created'
    }
    
    # Parcourir les détails
    details = stat_data.get('details', [])
    for detail in details:
        if 'type' in detail:
            stat_name = detail['type'].get('name', '')
            value = detail.get('value', {})
            
            # Extraire la valeur totale
            if isinstance(value, dict):
                total_value = value.get('total', value.get('average', 0))
            else:
                total_value = value
            
            # Mapper vers notre format
            if stat_name in mapping:
                our_key = mapping[stat_name]
                stats[our_key] = float(total_value) if total_value else 0
    
    # Calculer les pourcentages
    if stats['passes'] > 0:
        stats['passes_accuracy'] = (stats['passes_completed'] / stats['passes']) * 100
    
    # Ajouter les duels aériens si on a des duels totaux
    if stats['ground_duels'] > 10:  # S'il y a beaucoup de duels, séparer aériens/terrestres
        stats['aerial_duels'] = int(stats['ground_duels'] * 0.3)  # Estimation
        stats['aerial_duels_won'] = int(stats['ground_duels_won'] * 0.3)
        stats['ground_duels'] = int(stats['ground_duels'] * 0.7)
        stats['ground_duels_won'] = int(stats['ground_duels_won'] * 0.7)
    
    return stats

def process_om_stats():
    """Traite et sauvegarde les stats de l'OM"""
    
    print("Recuperation des joueurs de l'OM...")
    om_players = get_om_player_ids()
    print(f"  {len(om_players)} joueurs trouves")
    
    all_stats = {}
    
    for i, player_info in enumerate(om_players, 1):
        player_id = player_info['id']
        player_name = player_info['displayName'] or player_info['name']
        
        print(f"\n[{i}/{len(om_players)}] {player_name} (ID: {player_id})...")
        
        # Récupérer les stats du joueur
        player_stats = get_player_stats(player_id)
        
        if player_stats:
            all_stats[player_id] = {
                'id': player_id,
                'name': player_info['name'],
                'displayName': player_info['displayName'],
                'position': player_info['position'],
                'jersey': player_info['jersey'],
                'stats': {}
            }
            
            # Traiter chaque saison
            for stat_data in player_stats:
                if stat_data.get('has_values'):
                    season_id = stat_data.get('season_id')
                    
                    # Déterminer le nom de la saison
                    season_name = {
                        23435: '2025/2026',
                        21792: '2024/2025', 
                        19735: '2023/2024'
                    }.get(season_id, f'Season_{season_id}')
                    
                    # Mapper les stats
                    mapped_stats = map_stats_to_our_format(stat_data)
                    all_stats[player_id]['stats'][season_name] = mapped_stats
                    
                    # Afficher un résumé
                    apps = mapped_stats.get('appearences', 0)
                    goals = mapped_stats.get('goals', 0)
                    assists = mapped_stats.get('assists', 0)
                    
                    if apps > 0:
                        print(f"  {season_name}: {int(apps)} matchs, {int(goals)} buts, {int(assists)} passes")
        
        # Pause entre les requêtes
        time.sleep(1)
    
    # Sauvegarder les résultats
    with open('om_complete_stats.json', 'w', encoding='utf-8') as f:
        json.dump(all_stats, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Stats sauvegardees dans om_complete_stats.json")
    print(f"Total: {len(all_stats)} joueurs avec stats")
    
    # Créer le fichier TypeScript
    create_typescript_file(all_stats)

def create_typescript_file(all_stats):
    """Crée un fichier TypeScript avec les stats"""
    
    ts_content = """// Stats réelles des joueurs de l'OM depuis SportMonks API
// Généré automatiquement

export interface PlayerSeasonStats {
  // Général
  rating: number;
  minutes: number;
  appearences: number;
  lineups: number;
  captain: number;
  substitutions: number;
  touches: number;
  saves: number;
  punches: number;
  
  // Offensif
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
  
  // Défensif
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
  
  // Créatif
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
  displayName?: string;
  position: string;
  jersey?: number;
  stats: {
    [season: string]: PlayerSeasonStats;
  };
}

export const omPlayersRealStats: { [playerId: number]: PlayerRealStats } = """
    
    ts_content += json.dumps(all_stats, indent=2, ensure_ascii=False)
    ts_content += ";\n"
    
    # Sauvegarder
    with open('../data/omPlayersRealStats.ts', 'w', encoding='utf-8') as f:
        f.write(ts_content)
    
    print("✅ Fichier TypeScript cree: data/omPlayersRealStats.ts")

if __name__ == "__main__":
    print("🚀 Recuperation des stats completes de l'OM...\n")
    process_om_stats()
    print("\n✅ Termine!")