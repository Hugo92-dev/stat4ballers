#!/usr/bin/env python3
"""
Script FINAL pour récupérer TOUTES les statistiques avec le MAPPING CORRECT
Basé sur l'analyse réelle des IDs SportMonks
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

# MAPPING CORRECT basé sur l'analyse réelle des données
CORRECT_TYPE_MAPPING = {
    # Général
    118: 'rating',           # Note moyenne
    119: 'minutes',          # Minutes jouées
    321: 'appearences',      # Matchs joués
    322: 'lineups',          # Titularisations
    40: 'captain',           # Capitaine
    323: 'substitutions',    # Entrées en jeu (bench)
    
    # Offensif
    52: 'goals',             # Buts marqués
    58: 'assists',           # Passes décisives
    64: 'shots',             # Tirs
    65: 'shots_on_target',   # Tirs cadrés
    218: 'penalties_won',    # Penaltys obtenus
    85: 'penalties',         # Penaltys tirés
    86: 'penalties_scored',  # Penaltys marqués
    62: 'penalties_missed',  # Penaltys ratés
    70: 'hit_woodwork',      # Poteaux/barres
    69: 'offsides',          # Hors-jeu
    
    # Passes
    80: 'passes',            # Passes tentées
    116: 'passes_completed', # Passes réussies
    1584: 'passes_accuracy', # % précision passes
    102: 'key_passes',       # Passes clés
    114: 'crosses',          # Centres
    115: 'crosses_accurate', # Centres réussis
    122: 'long_balls',       # Balles longues
    123: 'long_balls_accurate', # Balles longues réussies
    
    # Dribbles
    108: 'dribbles',         # Dribbles tentés
    109: 'dribbles_successful', # Dribbles réussis
    
    # Défensif
    78: 'tackles',           # Tacles
    82: 'blocks',            # Contres
    100: 'interceptions',    # Interceptions
    101: 'clearances',       # Dégagements
    105: 'duels',            # Duels totaux
    106: 'duels_won',        # Duels gagnés
    107: 'aerial_duels_won', # Duels aériens gagnés
    110: 'dribbled_past',    # Dribblé par adversaire
    
    # Discipline
    56: 'fouls',             # Fautes commises
    96: 'fouls_drawn',       # Fautes subies
    84: 'yellow_cards',      # Cartons jaunes
    83: 'red_cards',         # Cartons rouges
    217: 'penalties_committed', # Penaltys concédés
    
    # Gardien
    57: 'saves',             # Arrêts
    88: 'goals_conceded',    # Buts encaissés
    194: 'clean_sheets',     # Clean sheets
    240: 'penalties_saved',  # Penaltys arrêtés
    207: 'punches',          # Dégagements aux poings
    104: 'inside_box_saves', # Arrêts dans la surface
    
    # Autres
    571: 'mistakes_leading_to_goals', # Erreurs menant à but
    574: 'dispossessed',     # Dépossédé
    97: 'touches',           # Touches de balle
    
    # Équipe
    214: 'team_wins',        # Victoires équipe
    215: 'team_draws',       # Nuls équipe
    216: 'team_losses'       # Défaites équipe
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
    """Mappe les stats avec le mapping CORRECT"""
    
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
    
    # Appliquer le mapping CORRECT
    if 'details' in season_data:
        for detail in season_data['details']:
            type_data = detail.get('type')
            if isinstance(type_data, dict):
                type_id = type_data.get('id')
                
                # Utiliser le NOUVEAU mapping
                if type_id in CORRECT_TYPE_MAPPING:
                    field_name = CORRECT_TYPE_MAPPING[type_id]
                    
                    # Certains champs ne sont pas dans notre structure finale
                    if field_name in stats:
                        value = detail.get('value', {})
                        if isinstance(value, dict):
                            stats[field_name] = value.get('total', value.get('average'))
                        else:
                            stats[field_name] = value
    
    # Calculer crosses_accuracy si possible
    if stats['crosses'] and stats['crosses_accurate']:
        try:
            stats['crosses_accuracy'] = round(
                (stats['crosses_accurate'] / stats['crosses']) * 100, 2
            )
        except:
            pass
    
    # Nettoyer les valeurs None qui devraient être 0
    for key in ['captain', 'goals', 'assists', 'yellow_cards', 'red_cards']:
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
                
                # Progress
                if p_idx % 5 == 0:
                    print(f"  Progress: {p_idx}/{len(players)}...", end='\r')
                
                # Récupérer les stats
                stats_data = get_player_stats(player_id, season_ids)
                
                if stats_data:
                    player_stats = {
                        'displayName': display_name,
                        'position': player.get('position', ''),
                        'jersey': player.get('jersey_number'),
                        'stats': {}
                    }
                    
                    # Traiter chaque saison
                    for season_stat in stats_data:
                        season_id = season_stat.get('season_id')
                        if season_id not in league_config['seasons']:
                            continue
                        
                        # Mapper avec le BON mapping
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
// Mapping CORRIGÉ basé sur l'analyse réelle des IDs
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
  penalties_saved?: null;
  
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
    print("🚀 Mise à jour COMPLÈTE avec MAPPING CORRECT")
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