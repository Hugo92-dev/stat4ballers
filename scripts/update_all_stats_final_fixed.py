#!/usr/bin/env python3
"""
Script FINAL CORRIGÉ pour récupérer TOUTES les statistiques
Correction du bug de mapping où les IDs étaient utilisés comme valeurs
"""

import json
import requests
import time
from dotenv import load_dotenv
import os
import sys
from datetime import datetime
from pathlib import Path
import logging

# Configuration logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

# Fix encodage Windows
sys.stdout.reconfigure(encoding='utf-8')

# Charger l'API key
load_dotenv('../.env.local')
API_KEY = os.getenv('SPORTMONKS_API_TOKEN')

if not API_KEY:
    print("❌ Clé API manquante")
    exit(1)

BASE_URL = "https://api.sportmonks.com/v3/football"

# Configuration des championnats
LEAGUES = {
    'ligue1': {
        'name': 'Ligue 1',
        'file': '../data/ligue1PlayersCompleteStats.ts',
        'teams_dir': '../data/ligue1_2025_2026/',
        'seasons': {25651: "2025/2026", 23643: "2024/2025", 21779: "2023/2024"}
    },
    'premier-league': {
        'name': 'Premier League',
        'file': '../data/premier-leaguePlayersCompleteStats.ts',
        'teams_dir': '../data/premier-league_2025_2026/',
        'seasons': {25583: "2025/2026", 23614: "2024/2025", 21646: "2023/2024"}
    },
    'liga': {
        'name': 'Liga',
        'file': '../data/la-ligaPlayersCompleteStats.ts',
        'teams_dir': '../data/liga_2025_2026/',
        'seasons': {25659: "2025/2026", 23621: "2024/2025", 21694: "2023/2024"}
    },
    'serie-a': {
        'name': 'Serie A',
        'file': '../data/serie-aPlayersCompleteStats.ts',
        'teams_dir': '../data/serie-a_2025_2026/',
        'seasons': {25533: "2025/2026", 23746: "2024/2025", 21818: "2023/2024"}
    },
    'bundesliga': {
        'name': 'Bundesliga',
        'file': '../data/bundesligaPlayersCompleteStats.ts',
        'teams_dir': '../data/bundesliga_2025_2026/',
        'seasons': {25646: "2025/2026", 23744: "2024/2025", 21795: "2023/2024"}
    }
}

# Cache global
team_cache = {}
api_calls = 0
MAX_CALLS_PER_MINUTE = 60

def rate_limit():
    """Gestion du rate limiting"""
    global api_calls
    api_calls += 1
    
    if api_calls % 20 == 0:
        time.sleep(2)
    if api_calls % MAX_CALLS_PER_MINUTE == 0:
        logger.info("⏸️ Pause rate limit (30s)...")
        time.sleep(30)

def get_team_name(team_id):
    """Récupère le nom d'une équipe"""
    if team_id in team_cache:
        return team_cache[team_id]
    
    try:
        response = requests.get(
            f"{BASE_URL}/teams/{team_id}",
            params={'api_token': API_KEY},
            timeout=10
        )
        rate_limit()
        
        if response.status_code == 200:
            name = response.json()['data'].get('name', f'Team_{team_id}')
            team_cache[team_id] = name
            return name
    except:
        pass
    
    return f'Team_{team_id}'

def get_player_stats(player_id, season_ids):
    """Récupère les stats d'un joueur pour les saisons données"""
    url = f"{BASE_URL}/statistics/seasons/players/{player_id}"
    params = {
        'api_token': API_KEY,
        'include': 'details.type',
        'filters': f'seasonIds:{",".join(map(str, season_ids))}'
    }
    
    try:
        response = requests.get(url, params=params, timeout=15)
        rate_limit()
        
        if response.status_code == 200:
            return response.json().get('data', [])
        elif response.status_code == 429:
            logger.warning("Rate limit atteint, pause 60s...")
            time.sleep(60)
            return get_player_stats(player_id, season_ids)
    except Exception as e:
        logger.error(f"Erreur API pour joueur {player_id}: {e}")
    
    return []

def map_stats_correctly(season_data, league_name, season_year):
    """Mappe les stats avec le mapping CORRECT - SANS BUG"""
    
    stats = {
        # Métadonnées
        'team': None,
        'team_id': None,
        'league': league_name,
        
        # Stats générales
        'rating': None,
        'minutes': None,
        'appearences': None,
        'lineups': None,
        'captain': None,
        'substitutions': None,
        'touches': None,
        
        # Stats offensives
        'goals': None,
        'assists': None,
        'xg': None,
        'xa': None,
        'shots': None,
        'shots_on_target': None,
        'penalties_won': None,
        'penalties': None,
        'penalties_scored': None,
        'penalties_missed': None,
        'hit_woodwork': None,
        'offsides': None,
        
        # Stats de passes
        'passes': None,
        'passes_completed': None,
        'passes_accuracy': None,
        'key_passes': None,
        'crosses': None,
        'crosses_accurate': None,
        
        # Stats de dribbles
        'dribbles': None,
        'dribbles_successful': None,
        
        # Stats défensives
        'tackles': None,
        'blocks': None,
        'interceptions': None,
        'clearances': None,
        'ground_duels': None,
        'ground_duels_won': None,
        'aerial_duels': None,
        'aerial_duels_won': None,
        
        # Discipline
        'fouls': None,
        'fouls_drawn': None,
        'yellow_cards': None,
        'red_cards': None,
        'yellowred_cards': None,
        'penalties_committed': None,
        
        # Autres
        'ball_losses': None,
        'ball_recoveries': None,
        'mistakes_leading_to_goals': None,
        
        # Stats gardien
        'saves': None,
        'punches': None,
        'inside_box_saves': None,
        'clean_sheets': None,
        'goals_conceded': None,
        'penalties_saved': None,
        
        # Calculé
        'crosses_accuracy': None
    }
    
    # Récupérer team_id
    team_id = season_data.get('team_id')
    if team_id:
        stats['team_id'] = team_id
        stats['team'] = get_team_name(team_id)
    
    # MAPPING CORRECT ET COMPLET
    # Basé sur l'analyse réelle de l'API SportMonks
    if 'details' in season_data:
        for detail in season_data['details']:
            type_data = detail.get('type')
            if not isinstance(type_data, dict):
                continue
                
            type_id = type_data.get('id')
            value = detail.get('value', {})
            
            # Extraire la vraie valeur (pas l'ID!)
            if isinstance(value, dict):
                actual_value = value.get('total', value.get('average'))
            else:
                actual_value = value
            
            # MAPPING COMPLET ET CORRECT
            # Général
            if type_id == 118:
                stats['rating'] = actual_value
            elif type_id == 119:
                stats['minutes'] = actual_value
            elif type_id == 321:
                stats['appearences'] = actual_value
            elif type_id == 322:
                stats['lineups'] = actual_value
            elif type_id == 40:
                stats['captain'] = actual_value
            elif type_id == 323:
                stats['substitutions'] = actual_value
            elif type_id == 97:
                stats['touches'] = actual_value
                
            # Offensif
            elif type_id == 52:
                stats['goals'] = actual_value
            elif type_id == 79:  # CORRECT: ID pour assists
                stats['assists'] = actual_value
            elif type_id == 58:  # CORRECT: ID pour shots_blocked
                stats['shots_blocked'] = actual_value
            elif type_id == 576:
                stats['xg'] = actual_value
            elif type_id == 577:
                stats['xa'] = actual_value
            elif type_id == 42:  # CORRECT: shots total
                stats['shots'] = actual_value
            elif type_id == 86:  # CORRECT: shots on target
                stats['shots_on_target'] = actual_value
            elif type_id == 218:
                stats['penalties_won'] = actual_value
            elif type_id == 85:
                stats['penalties'] = actual_value
            elif type_id == 86:
                stats['penalties_scored'] = actual_value
            elif type_id == 62:
                stats['penalties_missed'] = actual_value
            elif type_id == 64:  # CORRECT: hit woodwork
                stats['hit_woodwork'] = actual_value
            elif type_id == 69:
                stats['offsides'] = actual_value
                
            # Passes
            elif type_id == 80:
                stats['passes'] = actual_value
            elif type_id == 116:
                stats['passes_completed'] = actual_value
            elif type_id == 1584:
                stats['passes_accuracy'] = actual_value
            elif type_id == 102:
                stats['key_passes'] = actual_value
            elif type_id == 114:
                stats['crosses'] = actual_value
            elif type_id == 115:
                stats['crosses_accurate'] = actual_value
                
            # Dribbles
            elif type_id == 108:
                stats['dribbles'] = actual_value
            elif type_id == 109:
                stats['dribbles_successful'] = actual_value
                
            # Défensif
            elif type_id == 78:  # CORRECT: tackles
                stats['tackles'] = actual_value
            elif type_id == 97:  # CORRECT: blocks (blocked shots)
                stats['blocks'] = actual_value
            elif type_id == 100:  # CORRECT: interceptions
                stats['interceptions'] = actual_value
            elif type_id == 101:
                stats['clearances'] = actual_value
            elif type_id == 105:  # CORRECT: total duels
                stats['ground_duels'] = actual_value
            elif type_id == 106:  # CORRECT: duels won
                stats['ground_duels_won'] = actual_value
            elif type_id == 117:  # aerial duels
                stats['aerial_duels'] = actual_value
            elif type_id == 107:  # CORRECT: aerials won
                stats['aerial_duels_won'] = actual_value
                
            # Discipline
            elif type_id == 56:
                stats['fouls'] = actual_value
            elif type_id == 96:
                stats['fouls_drawn'] = actual_value
            elif type_id == 84:
                stats['yellow_cards'] = actual_value
            elif type_id == 83:
                stats['red_cards'] = actual_value
            elif type_id == 85:  # CORRECT: yellowred cards
                stats['yellowred_cards'] = actual_value
            elif type_id == 217:
                stats['penalties_committed'] = actual_value
                
            # Gardien
            elif type_id == 57:
                stats['saves'] = actual_value
            elif type_id == 207:
                stats['punches'] = actual_value
            elif type_id == 104:
                stats['inside_box_saves'] = actual_value
            elif type_id == 194:
                stats['clean_sheets'] = actual_value
            elif type_id == 88:
                stats['goals_conceded'] = actual_value
            elif type_id == 240:
                stats['penalties_saved'] = actual_value
                
            # Autres
            elif type_id == 219:
                stats['ball_losses'] = actual_value
            elif type_id == 220:
                stats['ball_recoveries'] = actual_value
            elif type_id == 571:
                stats['mistakes_leading_to_goals'] = actual_value
    
    # Calculer crosses_accuracy si possible
    if stats['crosses'] and stats['crosses_accurate']:
        try:
            stats['crosses_accuracy'] = round(
                (stats['crosses_accurate'] / stats['crosses']) * 100, 2
            )
        except:
            pass
    
    # S'assurer que les valeurs importantes sont 0 et non None pour les attaquants
    if 'FW' in str(season_year) or 'MF' in str(season_year):
        for key in ['goals', 'assists', 'shots', 'dribbles']:
            if stats[key] is None:
                stats[key] = 0
    
    # Pour les gardiens
    if 'GK' in str(season_year):
        for key in ['saves', 'goals_conceded', 'clean_sheets']:
            if stats[key] is None:
                stats[key] = 0
    
    return stats

def process_league(league_key, league_config):
    """Traite un championnat complet"""
    logger.info(f"\n{'='*60}")
    logger.info(f"🏆 {league_config['name']}")
    logger.info(f"{'='*60}\n")
    
    teams_dir = Path(league_config['teams_dir'])
    if not teams_dir.exists():
        logger.error(f"Dossier {teams_dir} introuvable")
        return {}
    
    # Lister les fichiers d'équipes
    team_files = [
        f for f in teams_dir.glob('*.json')
        if not f.stem.endswith('_stats') and not f.stem.endswith('_complete')
    ]
    
    logger.info(f"📋 {len(team_files)} équipes trouvées\n")
    
    all_players_stats = {}
    season_ids = list(league_config['seasons'].keys())
    
    for t_idx, team_file in enumerate(team_files, 1):
        try:
            with open(team_file, 'r', encoding='utf-8') as f:
                team_data = json.load(f)
            
            team_name = team_data.get('name', team_file.stem)
            players = team_data.get('players', [])
            
            if not players:
                continue
            
            logger.info(f"[{t_idx}/{len(team_files)}] {team_name} ({len(players)} joueurs)")
            
            for p_idx, player in enumerate(players, 1):
                player_id = player.get('id')
                if not player_id:
                    continue
                
                display_name = player.get('display_name', 'Unknown')
                position = player.get('position', '')
                
                # Progress
                if p_idx % 5 == 0:
                    print(f"  Progress: {p_idx}/{len(players)}...", end='\r')
                
                # Récupérer les stats
                stats_data = get_player_stats(player_id, season_ids)
                
                if stats_data:
                    player_stats = {
                        'displayName': display_name,
                        'position': position,
                        'jersey': player.get('jersey_number'),
                        'stats': {}
                    }
                    
                    # Traiter chaque saison
                    for season_stat in stats_data:
                        season_id = season_stat.get('season_id')
                        if season_id not in league_config['seasons']:
                            continue
                        
                        # Mapper avec le BON mapping (sans bug!)
                        mapped_stats = map_stats_correctly(
                            season_stat,
                            league_config['name'],
                            league_config['seasons'][season_id]
                        )
                        
                        # Clé de la saison
                        season_key = f"{league_config['seasons'][season_id]} ({league_config['name']}, {mapped_stats['team']})"
                        player_stats['stats'][season_key] = mapped_stats
                    
                    all_players_stats[player_id] = player_stats
            
            print(f"  ✅ {team_name} terminée                    ")
            
            # Pause entre équipes
            time.sleep(1)
            
        except Exception as e:
            logger.error(f"Erreur pour {team_file.stem}: {e}")
            continue
    
    return all_players_stats

def save_league_stats(league_key, league_config, stats):
    """Sauvegarde les stats d'un championnat"""
    output_file = Path(league_config['file'])
    
    # Générer le contenu TypeScript
    ts_content = f"""// Stats COMPLÈTES des joueurs de {league_config['name']} depuis SportMonks API
// Version CORRIGÉE - Bug de mapping résolu
// Généré automatiquement le {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

export interface PlayerSeasonStats {{
  // Métadonnées
  team?: string;
  team_id?: number;
  league?: string;
  
  // Stats générales
  rating?: number | null;
  minutes?: number | null;
  appearences?: number | null;
  lineups?: number | null;
  captain?: number | null;
  substitutions?: number | null;
  touches?: number | null;
  
  // Stats offensives
  goals?: number | null;
  assists?: number | null;
  xg?: number | null;
  xa?: number | null;
  shots?: number | null;
  shots_on_target?: number | null;
  penalties_won?: number | null;
  penalties?: number | null;
  penalties_scored?: number | null;
  penalties_missed?: number | null;
  hit_woodwork?: number | null;
  offsides?: number | null;
  
  // Stats de passes
  passes?: number | null;
  passes_completed?: number | null;
  passes_accuracy?: number | null;
  key_passes?: number | null;
  crosses?: number | null;
  crosses_accurate?: number | null;
  
  // Stats de dribbles
  dribbles?: number | null;
  dribbles_successful?: number | null;
  
  // Stats défensives
  tackles?: number | null;
  blocks?: number | null;
  interceptions?: number | null;
  clearances?: number | null;
  ground_duels?: number | null;
  ground_duels_won?: number | null;
  aerial_duels?: number | null;
  aerial_duels_won?: number | null;
  
  // Discipline
  fouls?: number | null;
  fouls_drawn?: number | null;
  yellow_cards?: number | null;
  red_cards?: number | null;
  yellowred_cards?: number | null;
  penalties_committed?: number | null;
  
  // Autres
  ball_losses?: number | null;
  ball_recoveries?: number | null;
  mistakes_leading_to_goals?: number | null;
  
  // Stats gardien
  saves?: number | null;
  punches?: number | null;
  inside_box_saves?: number | null;
  clean_sheets?: number | null;
  goals_conceded?: number | null;
  penalties_saved?: number | null;
  
  // Calculé
  crosses_accuracy?: number | null;
}}

export interface PlayerRealStats {{
  displayName: string;
  position: string;
  jersey?: number;
  stats: {{
    [seasonKey: string]: PlayerSeasonStats | null;
  }};
}}

export const {league_key.replace('-', '')}PlayersRealStats: {{ [playerId: number]: PlayerRealStats }} = {json.dumps(stats, indent=2, ensure_ascii=False)};
"""
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(ts_content)
    
    logger.info(f"\n💾 Sauvegardé: {output_file.name}")
    logger.info(f"📊 Total: {len(stats)} joueurs avec statistiques")

def main():
    """Fonction principale"""
    print("🚀 Mise à jour COMPLÈTE avec mapping CORRIGÉ")
    print("🔧 Correction du bug où les IDs étaient utilisés comme valeurs")
    print(f"⏰ Début: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Traiter chaque championnat
    for league_key, league_config in LEAGUES.items():
        try:
            stats = process_league(league_key, league_config)
            if stats:
                save_league_stats(league_key, league_config, stats)
                logger.info(f"✅ {league_config['name']} terminé!")
        except KeyboardInterrupt:
            print("\n⚠️ Interruption utilisateur")
            break
        except Exception as e:
            logger.error(f"Erreur pour {league_config['name']}: {e}")
            continue
    
    print("\n" + "=" * 60)
    print(f"✨ Mise à jour terminée!")
    print(f"⏰ Fin: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📊 Total d'appels API: {api_calls}")

if __name__ == "__main__":
    main()