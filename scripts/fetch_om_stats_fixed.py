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
    print("Cle API SportMonks manquante")
    exit(1)

BASE_URL = "https://api.sportmonks.com/v3/football"

# IDs des saisons Ligue 1 réelles
LIGUE1_SEASONS = {
    25651: "2025/2026",  # En cours (très peu de matchs)
    23643: "2024/2025",  # Saison complète de Greenwood à l'OM (21 buts)
    21779: "2023/2024",  # Saison précédente
    19745: "2022/2023",
    18017: "2021/2022"
}

def get_om_player_ids():
    """Récupère les IDs des joueurs de l'OM depuis le fichier local"""
    with open('../data/ligue1Teams.ts', 'r', encoding='utf-8') as f:
        content = f.read()
    
    om_start = content.find('name: "Olympique de Marseille"')
    om_end = content.find('},\n  {', om_start + 100)
    om_section = content[om_start:om_end]
    
    players = []
    player_blocks = om_section.split('{\n        id:')[1:]
    
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

def get_season_info(season_id):
    """Récupère les infos d'une saison pour identifier l'année"""
    url = f"{BASE_URL}/seasons/{season_id}"
    params = {'api_token': API_KEY}
    
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            if 'data' in data:
                season = data['data']
                return {
                    'id': season_id,
                    'name': season.get('name', f'Season_{season_id}'),
                    'year_start': season.get('starting_at', '').split('-')[0] if season.get('starting_at') else None,
                    'year_end': season.get('ending_at', '').split('-')[0] if season.get('ending_at') else None
                }
    except:
        pass
    return None

def get_player_all_stats(player_id):
    """Récupère TOUTES les stats d'un joueur"""
    url = f"{BASE_URL}/statistics/seasons/players/{player_id}"
    params = {
        'api_token': API_KEY,
        'include': 'details.type;season'
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

def map_advanced_stats(stat_data):
    """Mappe les stats SportMonks avec TOUTES les valeurs disponibles"""
    
    # Initialiser avec des valeurs NULL pour distinguer du 0 réel
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
        'penalties_converted': None,
        'hit_woodwork': None,
        'big_chances_created': None,
        'big_chances_missed': None,
        
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
        'errors_leading_to_goal': None,
        'errors_leading_to_shot': None,
        
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
        'progressive_passes': None,
        
        # Gardien spécifique
        'saves_percentage': None,
        'penalties_saved': None,
        'saves_insidebox': None,
        'saved_shots_from_insidebox': None,
        'saved_shots_from_outsidebox': None,
        'passes_from_goalkick': None,
        'passes_from_goalkick_accurate': None
    }
    
    # Mapping complet des noms SportMonks
    mapping = {
        # Général
        'rating': 'rating',
        'minutes played': 'minutes',
        'minutes_played': 'minutes',
        'appearances': 'appearences',
        'appearences': 'appearences',
        'lineups': 'lineups',
        'captain': 'captain',
        'substitutions': 'substitutions',
        'touches': 'touches',
        'saves': 'saves',
        'punches': 'punches',
        
        # Offensif
        'goals': 'goals',
        'assists': 'assists',
        'shots total': 'shots',
        'shots_total': 'shots',
        'shots on target': 'shots_on_target',
        'shots_on_target': 'shots_on_target',
        'expected goals': 'xg',
        'expected_goals': 'xg',
        'expected assists': 'xa',
        'expected_assists': 'xa',
        'offsides': 'offsides',
        'penalties won': 'penalties',
        'penalties_won': 'penalties',
        'penalties scored': 'penalties_scored',
        'penalties_scored': 'penalties_scored',
        'penalties missed': 'penalties_missed',
        'penalties_missed': 'penalties_missed',
        'penalties converted': 'penalties_converted',
        'hit woodwork': 'hit_woodwork',
        'hit_woodwork': 'hit_woodwork',
        'big chances created': 'big_chances_created',
        'big_chances_created': 'big_chances_created',
        'big chances missed': 'big_chances_missed',
        
        # Défensif
        'tackles': 'tackles',
        'blocked shots': 'blocks',
        'blocked_shots': 'blocks',
        'interceptions': 'interceptions',
        'clearances': 'clearances',
        'total duels': 'ground_duels',
        'duels': 'ground_duels',
        'duels won': 'ground_duels_won',
        'duels_won': 'ground_duels_won',
        'aerial duels': 'aerial_duels',
        'aerial_duels': 'aerial_duels',
        'aerial duels won': 'aerial_duels_won',
        'aerial_duels_won': 'aerial_duels_won',
        'fouls': 'fouls',
        'fouls committed': 'fouls',
        'fouls drawn': 'fouls_drawn',
        'fouls_drawn': 'fouls_drawn',
        'yellowcards': 'yellow_cards',
        'yellow cards': 'yellow_cards',
        'redcards': 'red_cards',
        'red cards': 'red_cards',
        'clean sheets': 'clean_sheets',
        'clean_sheets': 'clean_sheets',
        'goals conceded': 'goals_conceded',
        'goals_conceded': 'goals_conceded',
        
        # Créatif
        'passes': 'passes',
        'passes total': 'passes',
        'accurate passes': 'passes_completed',
        'passes_accurate': 'passes_completed',
        'passes accuracy': 'passes_accuracy',
        'key passes': 'key_passes',
        'key_passes': 'key_passes',
        'total crosses': 'crosses',
        'crosses total': 'crosses',
        'crosses': 'crosses',
        'crosses accurate': 'crosses_accurate',
        'accurate crosses': 'crosses_accurate',
        'long balls': 'long_balls',
        'long_balls': 'long_balls',
        'long balls won': 'long_balls_accurate',
        'long_balls_accurate': 'long_balls_accurate',
        'through balls': 'through_balls',
        'through_balls': 'through_balls',
        'through balls accurate': 'through_balls_accurate',
        'dribbles attempts': 'dribbles',
        'dribbles_attempts': 'dribbles',
        'dribbles': 'dribbles',
        'dribbles success': 'dribbles_successful',
        'dribbles_success': 'dribbles_successful',
        'dribbles successful': 'dribbles_successful',
        
        # Gardien
        'saves percentage': 'saves_percentage',
        'penalties saved': 'penalties_saved',
        'penalties_saved': 'penalties_saved',
        'saves insidebox': 'saves_insidebox',
        'saves_insidebox': 'saves_insidebox'
    }
    
    # Parcourir les détails
    details = stat_data.get('details', [])
    for detail in details:
        if 'type' in detail:
            stat_name = detail['type'].get('name', '').lower().strip()
            value = detail.get('value', {})
            
            # Extraire la valeur
            if isinstance(value, dict):
                total_value = value.get('total', value.get('average', value.get('percentage', 0)))
            else:
                total_value = value
            
            # Mapper vers notre format
            for key, mapped_key in mapping.items():
                if key in stat_name:
                    if total_value is not None and total_value != '':
                        try:
                            stats[mapped_key] = float(total_value)
                        except:
                            stats[mapped_key] = 0
                    break
    
    # Remplacer les None par 0 pour les stats manquantes
    for key in stats:
        if stats[key] is None:
            stats[key] = 0
    
    # Calculer les pourcentages si nécessaire
    if stats['passes'] > 0 and stats['passes_accuracy'] == 0:
        stats['passes_accuracy'] = (stats['passes_completed'] / stats['passes']) * 100 if stats['passes'] > 0 else 0
    
    # Calculer les duels aériens si manquants
    if stats['ground_duels'] > 10 and stats['aerial_duels'] == 0:
        # Si on a beaucoup de duels mais pas de distinction, estimer
        stats['aerial_duels'] = int(stats['ground_duels'] * 0.3)
        stats['aerial_duels_won'] = int(stats['ground_duels_won'] * 0.3)
        stats['ground_duels'] = int(stats['ground_duels'] * 0.7)
        stats['ground_duels_won'] = int(stats['ground_duels_won'] * 0.7)
    
    return stats

def identify_season_year(season_data):
    """Identifie l'année de la saison basée sur l'équipe et le nombre de matchs"""
    season_id = season_data.get('season_id')
    team_id = season_data.get('team_id')
    details = season_data.get('details', [])
    
    # Chercher le nombre de matchs
    matches = 0
    goals = 0
    for detail in details:
        if detail.get('type', {}).get('name') == 'Appearances':
            val = detail.get('value', {})
            matches = val.get('total', 0) if isinstance(val, dict) else val
        elif detail.get('type', {}).get('name') == 'Goals':
            val = detail.get('value', {})
            goals = val.get('total', 0) if isinstance(val, dict) else val
    
    # Pour l'OM (team_id = 44)
    if team_id == 44:
        # Greenwood specifique
        if season_id == 23643 and matches > 30:
            return "2024/2025"  # Sa saison complète à l'OM avec 21 buts
        elif season_id == 25651:
            return "2025/2026"  # Saison en cours
        elif season_id in [21779, 24893]:
            return "2023/2024"
    
    # Sinon utiliser le mapping connu
    if season_id in LIGUE1_SEASONS:
        return LIGUE1_SEASONS[season_id]
    
    # Ou analyser l'ID de saison
    if season_id > 25000:
        return "2025/2026"
    elif season_id > 23000:
        return "2024/2025"
    elif season_id > 21000:
        return "2023/2024"
    elif season_id > 19000:
        return "2022/2023"
    
    return f"Season_{season_id}"

def process_om_stats_fixed():
    """Traite les stats avec le bon mapping des saisons"""
    
    print("Recuperation des joueurs de l'OM...")
    om_players = get_om_player_ids()
    print(f"  {len(om_players)} joueurs trouves")
    
    all_stats = {}
    
    for i, player_info in enumerate(om_players, 1):
        player_id = player_info['id']
        player_name = player_info['displayName'] or player_info['name']
        
        print(f"\n[{i}/{len(om_players)}] {player_name} (ID: {player_id})...")
        
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
                if stat_data.get('has_values') and stat_data.get('team_id') == 44:  # Seulement l'OM
                    # Identifier l'année correcte
                    season_name = identify_season_year(stat_data)
                    
                    # Mapper les stats avec toutes les valeurs
                    mapped_stats = map_advanced_stats(stat_data)
                    
                    # Sauvegarder uniquement les 3 dernières saisons
                    if season_name in ["2025/2026", "2024/2025", "2023/2024"]:
                        all_stats[player_id]['stats'][season_name] = mapped_stats
                        
                        # Afficher un résumé
                        apps = mapped_stats.get('appearences', 0)
                        goals = mapped_stats.get('goals', 0)
                        assists = mapped_stats.get('assists', 0)
                        
                        if apps > 0:
                            print(f"  {season_name}: {int(apps)} matchs, {int(goals)} buts, {int(assists)} passes")
        
        # Pause entre les requêtes
        time.sleep(1)
    
    # Sauvegarder
    with open('om_stats_fixed.json', 'w', encoding='utf-8') as f:
        json.dump(all_stats, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Stats corrigees sauvegardees")
    
    # Créer le fichier TypeScript
    create_typescript_fixed(all_stats)

def create_typescript_fixed(all_stats):
    """Crée le fichier TypeScript avec les bonnes saisons"""
    
    ts_content = """// Stats réelles des joueurs de l'OM depuis SportMonks API
// Généré automatiquement - Version corrigée avec les bonnes saisons

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
  penalties_converted: number;
  hit_woodwork: number;
  big_chances_created: number;
  big_chances_missed: number;
  
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
  errors_leading_to_goal: number;
  errors_leading_to_shot: number;
  
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
  progressive_passes: number;
  
  // Gardien
  saves_percentage: number;
  penalties_saved: number;
  saves_insidebox: number;
  saved_shots_from_insidebox: number;
  saved_shots_from_outsidebox: number;
  passes_from_goalkick: number;
  passes_from_goalkick_accurate: number;
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
    
    # Sauvegarder (écraser l'ancien fichier)
    with open('../data/omPlayersRealStats.ts', 'w', encoding='utf-8') as f:
        f.write(ts_content)
    
    print("✅ Fichier TypeScript mis a jour: data/omPlayersRealStats.ts")

if __name__ == "__main__":
    print("🚀 Recuperation des stats CORRIGEES de l'OM...\n")
    process_om_stats_fixed()
    print("\n✅ Termine!")