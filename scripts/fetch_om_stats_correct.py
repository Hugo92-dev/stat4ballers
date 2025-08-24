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
    print("Clé API SportMonks manquante dans .env.local")
    exit(1)

BASE_URL = "https://api.sportmonks.com/v3/football"

# IDs CORRECTS des saisons Ligue 1
SEASON_IDS = [21779, 23643, 25651]  # 2023/24, 2024/25, 2025/26

# Mapping des IDs vers les années
SEASON_MAPPING = {
    21779: "2023/2024",
    23643: "2024/2025", 
    25651: "2025/2026"
}

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
    player_blocks = om_section.split('{')[2:]  # Diviser par joueur
    
    for block in player_blocks:
        player_id_match = re.search(r'id:\s*(\d+)', block)
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
    """Récupère les stats d'un joueur pour les saisons spécifiées"""
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
    """Mappe les stats SportMonks vers notre format, avec null pour les valeurs manquantes"""
    
    # Initialiser toutes les stats à null
    stats = {
        # Général
        'rating': None,
        'minutes': None,
        'appearences': None,
        'lineups': None,
        'captain': None,
        'substitutions': None,
        'touches': None,
        'saves': None,
        'punches': None,
        
        # Offensif
        'goals': None,
        'assists': None,
        'shots': None,
        'shots_on_target': None,
        'xg': None,
        'xa': None,
        'offsides': None,
        'penalties': None,
        'penalties_scored': None,
        'penalties_missed': None,
        'hit_woodwork': None,
        
        # Défensif
        'tackles': None,
        'blocks': None,
        'interceptions': None,
        'clearances': None,
        'aerial_duels': None,
        'aerial_duels_won': None,
        'ground_duels': None,
        'ground_duels_won': None,
        'fouls': None,
        'fouls_drawn': None,
        'yellow_cards': None,
        'red_cards': None,
        'clean_sheets': None,
        'goals_conceded': None,
        
        # Créatif
        'passes': None,
        'passes_completed': None,
        'passes_accuracy': None,
        'key_passes': None,
        'crosses': None,
        'crosses_accurate': None,
        'long_balls': None,
        'long_balls_accurate': None,
        'through_balls': None,
        'through_balls_accurate': None,
        'dribbles': None,
        'dribbles_successful': None,
        'progressive_carries': None,
        'big_chances_created': None
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
        'Aerial Duels': 'aerial_duels',
        'Aerial Duels Won': 'aerial_duels_won',
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
                total_value = value.get('total', value.get('average', None))
            else:
                total_value = value
            
            # Mapper vers notre format (null si pas de valeur ou 0)
            if stat_name in mapping and total_value is not None and total_value != 0:
                our_key = mapping[stat_name]
                stats[our_key] = float(total_value)
    
    # Calculer les pourcentages seulement si les données existent
    if stats['passes'] and stats['passes_completed']:
        stats['passes_accuracy'] = (stats['passes_completed'] / stats['passes']) * 100
    
    return stats

def process_om_stats():
    """Traite et sauvegarde les stats de l'OM avec les bons IDs de saison"""
    
    print("Récupération des joueurs de l'OM...")
    om_players = get_om_player_ids()
    print(f"  {len(om_players)} joueurs trouvés")
    
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
                    
                    # Utiliser le mapping correct
                    if season_id in SEASON_MAPPING:
                        season_name = SEASON_MAPPING[season_id]
                        
                        # Mapper les stats
                        mapped_stats = map_stats_to_our_format(stat_data)
                        all_stats[player_id]['stats'][season_name] = mapped_stats
                        
                        # Afficher un résumé
                        apps = mapped_stats.get('appearences')
                        goals = mapped_stats.get('goals')
                        assists = mapped_stats.get('assists')
                        
                        if apps:
                            print(f"  {season_name}: {int(apps) if apps else 0} matchs, {int(goals) if goals else 0} buts, {int(assists) if assists else 0} passes")
        
        # Pause entre les requêtes
        time.sleep(1)
    
    # Sauvegarder les résultats
    with open('om_stats_final.json', 'w', encoding='utf-8') as f:
        json.dump(all_stats, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Stats sauvegardées dans om_stats_final.json")
    print(f"Total: {len(all_stats)} joueurs avec stats")
    
    # Créer le fichier TypeScript
    create_typescript_file(all_stats)

def create_typescript_file(all_stats):
    """Crée un fichier TypeScript avec les stats"""
    
    ts_content = """// Stats réelles des joueurs de l'OM depuis SportMonks API
// Généré automatiquement avec les IDS DE SAISON CORRECTS
// 2023/2024 = ID 21779, 2024/2025 = ID 23643, 2025/2026 = ID 25651

export interface PlayerSeasonStats {
  // Général
  rating: number | null;
  minutes: number | null;
  appearences: number | null;
  lineups: number | null;
  captain: number | null;
  substitutions: number | null;
  touches: number | null;
  saves: number | null;
  punches: number | null;
  
  // Offensif
  goals: number | null;
  assists: number | null;
  shots: number | null;
  shots_on_target: number | null;
  xg: number | null;
  xa: number | null;
  offsides: number | null;
  penalties: number | null;
  penalties_scored: number | null;
  penalties_missed: number | null;
  hit_woodwork: number | null;
  
  // Défensif
  tackles: number | null;
  blocks: number | null;
  interceptions: number | null;
  clearances: number | null;
  aerial_duels: number | null;
  aerial_duels_won: number | null;
  ground_duels: number | null;
  ground_duels_won: number | null;
  fouls: number | null;
  fouls_drawn: number | null;
  yellow_cards: number | null;
  red_cards: number | null;
  clean_sheets: number | null;
  goals_conceded: number | null;
  
  // Créatif
  passes: number | null;
  passes_completed: number | null;
  passes_accuracy: number | null;
  key_passes: number | null;
  crosses: number | null;
  crosses_accurate: number | null;
  long_balls: number | null;
  long_balls_accurate: number | null;
  through_balls: number | null;
  through_balls_accurate: number | null;
  dribbles: number | null;
  dribbles_successful: number | null;
  progressive_carries: number | null;
  big_chances_created: number | null;
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
    with open('../data/omPlayersRealStatsFinal.ts', 'w', encoding='utf-8') as f:
        f.write(ts_content)
    
    print("✅ Fichier TypeScript créé: data/omPlayersRealStatsFinal.ts")

if __name__ == "__main__":
    print("🚀 Récupération des stats de l'OM avec les BONS IDs de saison...\n")
    print(f"IDs utilisés:")
    for season_id, season_name in SEASON_MAPPING.items():
        print(f"  - {season_name}: ID {season_id}")
    print()
    process_om_stats()
    
    # Vérifier Mason Greenwood
    print("\n=== Vérification de Mason Greenwood ===")
    with open('om_stats_final.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    greenwood = data.get('20333643')
    if greenwood:
        print(f"Nom: {greenwood['displayName']}")
        
        for season_name in ["2025/2026", "2024/2025", "2023/2024"]:
            if season_name in greenwood['stats']:
                stats = greenwood['stats'][season_name]
                print(f"\n{season_name}:")
                print(f"  Matchs: {stats.get('appearences')}")
                print(f"  Buts: {stats.get('goals')}")
                print(f"  Passes: {stats.get('assists')}")
    else:
        print("Mason Greenwood non trouvé!")