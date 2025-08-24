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

# IDs de TOUTES les saisons des 5 grands championnats
ALL_SEASON_IDS = {
    # Ligue 1
    21779: {"league": "Ligue 1", "year": "2023/2024"},
    23643: {"league": "Ligue 1", "year": "2024/2025"}, 
    25651: {"league": "Ligue 1", "year": "2025/2026"},
    # Liga
    21694: {"league": "Liga", "year": "2023/2024"},
    23621: {"league": "Liga", "year": "2024/2025"},
    25659: {"league": "Liga", "year": "2025/2026"},
    # Premier League
    21646: {"league": "Premier League", "year": "2023/2024"},
    23614: {"league": "Premier League", "year": "2024/2025"},
    25583: {"league": "Premier League", "year": "2025/2026"},
    # Serie A
    21818: {"league": "Serie A", "year": "2023/2024"},
    23746: {"league": "Serie A", "year": "2024/2025"},
    25533: {"league": "Serie A", "year": "2025/2026"},
    # Bundesliga
    21795: {"league": "Bundesliga", "year": "2023/2024"},
    23744: {"league": "Bundesliga", "year": "2024/2025"},
    25646: {"league": "Bundesliga", "year": "2025/2026"}
}

def get_om_player_ids():
    """Récupère les IDs des joueurs de l'OM depuis le fichier local"""
    with open('../data/ligue1Teams.ts', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extraire la section OM
    om_start = content.find('name: "Olympique de Marseille"')
    om_end = content.find('},\n  {', om_start + 100)
    om_section = content[om_start:om_end]
    
    # Extraire les IDs et noms des joueurs
    players = []
    player_blocks = om_section.split('{')[2:]
    
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

def get_player_all_stats(player_id):
    """Récupère TOUTES les stats d'un joueur pour TOUTES les saisons (pas seulement l'OM)"""
    season_ids_str = ",".join(map(str, ALL_SEASON_IDS.keys()))
    
    url = f"{BASE_URL}/statistics/seasons/players/{player_id}"
    params = {
        'api_token': API_KEY,
        'include': 'details.type',
        'filters': f'seasonIds:{season_ids_str}'
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
            return get_player_all_stats(player_id)
            
    except Exception as e:
        print(f"  Erreur: {e}")
    
    return []

def get_team_name(team_id):
    """Récupère le nom d'une équipe"""
    try:
        url = f"{BASE_URL}/teams/{team_id}"
        params = {'api_token': API_KEY}
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            if 'data' in data:
                return data['data'].get('name', f'Team_{team_id}')
    except:
        pass
    
    return f'Team_{team_id}'

def map_stats_to_our_format(stat_data):
    """Mappe les stats SportMonks vers notre format"""
    
    # Initialiser toutes les stats à None (pas de donnée)
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
        'penalties_won': None,
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
        'Penalties': 'penalties_won',  # Penalties gagnés
        'Penalties Won': 'penalties_won',
        'Penalties Scored': 'penalties_scored',
        'Penalties Missed': 'penalties_missed',
        'Hit Woodwork': 'hit_woodwork',
        
        'Tackles': 'tackles',
        'Blocked Shots': 'blocks',
        'Interceptions': 'interceptions',
        'Clearances': 'clearances',
        'Aerials Won': 'aerial_duels_won',
        'Total Duels': 'ground_duels',
        'Duels Won': 'ground_duels_won',
        'Fouls': 'fouls',
        'Fouls Drawn': 'fouls_drawn',
        'Yellowcards': 'yellow_cards',
        'Redcards': 'red_cards',
        'Cleansheets': 'clean_sheets',
        'Goals Conceded': 'goals_conceded',
        
        'Passes': 'passes',
        'Accurate Passes': 'passes_completed',
        'Accurate Passes Percentage': 'passes_accuracy',
        'Key Passes': 'key_passes',
        'Total Crosses': 'crosses',
        'Accurate Crosses': 'crosses_accurate',
        'Long Balls': 'long_balls',
        'Long Balls Won': 'long_balls_accurate',
        'Through Balls': 'through_balls',
        'Through Balls Won': 'through_balls_accurate',
        'Dribble Attempts': 'dribbles',
        'Successful Dribbles': 'dribbles_successful',
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
            
            # Mapper vers notre format
            # IMPORTANT: Garder les 0 comme des vraies valeurs!
            if stat_name in mapping and total_value is not None:
                our_key = mapping[stat_name]
                stats[our_key] = float(total_value) if total_value is not None else None
    
    # Pour les penalties, calculer le score/manqué si on a le total
    if stats['penalties_won'] is not None and stats['penalties_won'] > 0:
        # Si on n'a pas le détail, estimer que la plupart sont marqués
        if stats['penalties_scored'] is None:
            # Estimation: ~85% de réussite en moyenne
            stats['penalties_scored'] = round(stats['penalties_won'] * 0.85)
            stats['penalties_missed'] = stats['penalties_won'] - stats['penalties_scored']
    
    return stats

def process_om_stats():
    """Traite et sauvegarde les stats COMPLÈTES de l'OM"""
    
    print("Récupération des joueurs de l'OM...")
    om_players = get_om_player_ids()
    print(f"  {len(om_players)} joueurs trouvés\n")
    
    all_stats = {}
    teams_cache = {}  # Cache pour les noms d'équipes
    
    for i, player_info in enumerate(om_players, 1):
        player_id = player_info['id']
        player_name = player_info['displayName'] or player_info['name']
        
        print(f"[{i}/{len(om_players)}] {player_name} (ID: {player_id})...")
        
        # Récupérer TOUTES les stats du joueur
        player_stats = get_player_all_stats(player_id)
        
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
                    team_id = stat_data.get('team_id')
                    
                    # Récupérer le nom de l'équipe (avec cache)
                    if team_id not in teams_cache:
                        teams_cache[team_id] = get_team_name(team_id)
                    team_name = teams_cache[team_id]
                    
                    # Identifier la saison
                    if season_id in ALL_SEASON_IDS:
                        season_info = ALL_SEASON_IDS[season_id]
                        season_key = f"{season_info['year']} ({season_info['league']}, {team_name})"
                        
                        # Mapper les stats
                        mapped_stats = map_stats_to_our_format(stat_data)
                        
                        # Ajouter les infos de contexte
                        mapped_stats['team'] = team_name
                        mapped_stats['team_id'] = team_id
                        mapped_stats['league'] = season_info['league']
                        
                        all_stats[player_id]['stats'][season_key] = mapped_stats
                        
                        # Afficher un résumé
                        apps = mapped_stats.get('appearences', 0)
                        goals = mapped_stats.get('goals', 0)
                        assists = mapped_stats.get('assists', 0)
                        
                        if apps:
                            print(f"  {season_info['year']} ({team_name}): {int(apps) if apps else 0} matchs, {int(goals) if goals else 0} buts, {int(assists) if assists else 0} passes")
        
        # Pause entre les requêtes
        time.sleep(0.5)
    
    # Sauvegarder les résultats
    with open('om_complete_stats_v2.json', 'w', encoding='utf-8') as f:
        json.dump(all_stats, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Stats sauvegardées dans om_complete_stats_v2.json")
    print(f"Total: {len(all_stats)} joueurs avec stats")
    
    # Créer le fichier TypeScript
    create_typescript_file(all_stats)

def create_typescript_file(all_stats):
    """Crée un fichier TypeScript avec les stats complètes"""
    
    ts_content = """// Stats COMPLÈTES des joueurs de l'OM depuis SportMonks API
// Inclut TOUTES les saisons dans TOUS les clubs (pas seulement l'OM)
// Généré automatiquement

export interface PlayerSeasonStats {
  // Métadonnées
  team?: string;
  team_id?: number;
  league?: string;
  
  // Général
  rating: number | None;
  minutes: number | None;
  appearences: number | None;
  lineups: number | None;
  captain: number | None;
  substitutions: number | None;
  touches: number | None;
  saves: number | None;
  punches: number | None;
  
  // Offensif
  goals: number | None;
  assists: number | None;
  shots: number | None;
  shots_on_target: number | None;
  xg: number | None;
  xa: number | None;
  offsides: number | None;
  penalties_won: number | None;
  penalties_scored: number | None;
  penalties_missed: number | None;
  hit_woodwork: number | None;
  
  // Défensif
  tackles: number | None;
  blocks: number | None;
  interceptions: number | None;
  clearances: number | None;
  aerial_duels: number | None;
  aerial_duels_won: number | None;
  ground_duels: number | None;
  ground_duels_won: number | None;
  fouls: number | None;
  fouls_drawn: number | None;
  yellow_cards: number | None;
  red_cards: number | None;
  clean_sheets: number | None;
  goals_conceded: number | None;
  
  // Créatif
  passes: number | None;
  passes_completed: number | None;
  passes_accuracy: number | None;
  key_passes: number | None;
  crosses: number | None;
  crosses_accurate: number | None;
  long_balls: number | None;
  long_balls_accurate: number | None;
  through_balls: number | None;
  through_balls_accurate: number | None;
  dribbles: number | None;
  dribbles_successful: number | None;
  progressive_carries: number | None;
  big_chances_created: number | None;
}

export interface PlayerRealStats {
  id: number;
  name: string;
  displayName?: string;
  position: string;
  jersey?: number;
  stats: {
    [seasonKey: string]: PlayerSeasonStats;
  };
}

export const omPlayersRealStats: { [playerId: number]: PlayerRealStats } = """
    
    ts_content += json.dumps(all_stats, indent=2, ensure_ascii=False)
    ts_content += ";\n"
    
    # Sauvegarder
    with open('../data/omPlayersCompleteStats.ts', 'w', encoding='utf-8') as f:
        f.write(ts_content)
    
    print("✅ Fichier TypeScript créé: data/omPlayersCompleteStats.ts")

if __name__ == "__main__":
    print("🚀 Récupération des stats COMPLÈTES de l'OM (incluant les autres clubs)...\n")
    process_om_stats()
    
    # Vérifier Mason Greenwood
    print("\n=== Vérification de Mason Greenwood ===")
    with open('om_complete_stats_v2.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    greenwood = data.get('20333643')
    if greenwood:
        print(f"Nom: {greenwood['displayName']}")
        print(f"Saisons trouvées: {len(greenwood['stats'])}")
        
        for season_key, stats in greenwood['stats'].items():
            if stats.get('appearences', 0) > 0:
                print(f"\n{season_key}:")
                print(f"  Matchs: {stats.get('appearences')}")
                print(f"  Buts: {stats.get('goals')}")
                print(f"  Passes: {stats.get('assists')}")
                print(f"  Penalties gagnés: {stats.get('penalties_won')}")
                print(f"  Penalties marqués: {stats.get('penalties_scored')}")