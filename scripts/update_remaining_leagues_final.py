#!/usr/bin/env python3
"""
Script pour mettre à jour les ligues restantes (Premier League, Liga, Serie A, Bundesliga)
"""

import json
import requests
import time
from dotenv import load_dotenv
import os
import sys
from datetime import datetime
from pathlib import Path

# Fix encodage Windows
sys.stdout.reconfigure(encoding='utf-8')

# Charger l'API key
load_dotenv('../.env.local')
API_KEY = os.getenv('SPORTMONKS_API_TOKEN')

if not API_KEY:
    print("❌ Clé API manquante")
    exit(1)

BASE_URL = "https://api.sportmonks.com/v3/football"

# Ligues à mettre à jour
LEAGUES = {
    'premier-league': {
        'name': 'Premier League', 
        'file': '../data/premier-leaguePlayersCompleteStats.ts',
        'teams': '../data/premier-league_2025_2026/',
        'seasons': {
            25583: "2025/2026",
            23614: "2024/2025",
            21646: "2023/2024"
        }
    },
    'liga': {
        'name': 'Liga',
        'file': '../data/la-ligaPlayersCompleteStats.ts',
        'teams': '../data/liga_2025_2026/',
        'seasons': {
            25659: "2025/2026",
            23621: "2024/2025",
            21694: "2023/2024"
        }
    },
    'serie-a': {
        'name': 'Serie A',
        'file': '../data/serie-aPlayersCompleteStats.ts',
        'teams': '../data/serie-a_2025_2026/',
        'seasons': {
            25533: "2025/2026",
            23746: "2024/2025",
            21818: "2023/2024"
        }
    },
    'bundesliga': {
        'name': 'Bundesliga',
        'file': '../data/bundesligaPlayersCompleteStats.ts',
        'teams': '../data/bundesliga_2025_2026/',
        'seasons': {
            25646: "2025/2026",
            23744: "2024/2025",
            21795: "2023/2024"
        }
    }
}

# Cache et compteurs
team_name_cache = {}
api_calls = 0
errors = []

def safe_request(url, params, max_retries=3):
    """Effectue une requête avec gestion des erreurs"""
    global api_calls
    
    for attempt in range(max_retries):
        try:
            api_calls += 1
            
            # Rate limiting
            if api_calls % 15 == 0:
                time.sleep(2)
            if api_calls % 75 == 0:
                print(f"      ⏸️ Pause anti rate-limit (30s)...")
                time.sleep(30)
            
            response = requests.get(url, params=params, timeout=15)
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 429:
                wait = min(60 * (attempt + 1), 180)
                print(f"      ⏳ Rate limit, attente {wait}s...")
                time.sleep(wait)
            elif response.status_code == 404:
                return None
            else:
                if attempt == max_retries - 1:
                    errors.append(f"HTTP {response.status_code}: {url}")
                
        except requests.exceptions.Timeout:
            if attempt < max_retries - 1:
                time.sleep(5)
        except Exception as e:
            if attempt == max_retries - 1:
                errors.append(f"Exception: {str(e)[:100]}")
    
    return None

def get_team_name(team_id):
    """Récupère le nom d'une équipe"""
    if team_id in team_name_cache:
        return team_name_cache[team_id]
    
    data = safe_request(
        f"{BASE_URL}/teams/{team_id}",
        {'api_token': API_KEY}
    )
    
    if data and 'data' in data:
        name = data['data'].get('name', f'Team_{team_id}')
    else:
        name = f'Team_{team_id}'
    
    team_name_cache[team_id] = name
    return name

def get_player_stats(player_id, season_ids):
    """Récupère les stats d'un joueur"""
    data = safe_request(
        f"{BASE_URL}/statistics/seasons/players/{player_id}",
        {
            'api_token': API_KEY,
            'include': 'details.type',
            'filters': f'seasonIds:{",".join(map(str, season_ids))}'
        }
    )
    
    return data.get('data', []) if data else []

def map_stats(details):
    """Mappe les stats au format requis"""
    stats = {
        'rating': None, 'minutes': None, 'appearences': None, 'lineups': None,
        'captain': None, 'touches': None, 'goals': None, 'assists': None,
        'xg': None, 'xa': None, 'shots': None, 'shots_on_target': None,
        'hit_woodwork': None, 'saves': None, 'goals_conceded': None,
        'clean_sheets': None, 'penalties_saved': None, 'punches': None,
        'inside_box_saves': None, 'passes': None, 'passes_completed': None,
        'passes_accuracy': None, 'key_passes': None, 'crosses': None,
        'crosses_accurate': None, 'tackles': None, 'blocks': None,
        'interceptions': None, 'clearances': None, 'fouls': None,
        'fouls_drawn': None, 'yellow_cards': None, 'red_cards': None,
        'yellowred_cards': None, 'ground_duels': None, 'ground_duels_won': None,
        'aerial_duels': None, 'aerial_duels_won': None, 'duels': None,
        'duels_won': None, 'dribbles': None, 'dribbles_successful': None,
        'penalties': None, 'penalties_won': None, 'penalties_scored': None,
        'penalties_missed': None, 'penalties_committed': None, 'offsides': None,
        'ball_losses': None, 'ball_recoveries': None,
        'mistakes_leading_to_goals': None, 'crosses_accuracy': None,
        'substitutions': None
    }
    
    # Mapping SportMonks
    type_map = {
        52: 'rating', 79: 'minutes', 113: 'appearences', 114: 'lineups',
        118: 'captain', 192: 'touches', 208: 'goals', 209: 'assists',
        576: 'xg', 577: 'xa', 42: 'shots', 86: 'shots_on_target',
        81: 'hit_woodwork', 206: 'saves', 131: 'goals_conceded',
        130: 'clean_sheets', 240: 'penalties_saved', 207: 'punches',
        129: 'inside_box_saves', 124: 'passes', 125: 'passes_completed',
        126: 'passes_accuracy', 147: 'key_passes', 45: 'crosses',
        46: 'crosses_accurate', 88: 'tackles', 74: 'blocks',
        75: 'interceptions', 78: 'clearances', 105: 'fouls',
        106: 'fouls_drawn', 56: 'yellow_cards', 57: 'red_cards',
        58: 'yellowred_cards', 127: 'dribbles', 128: 'dribbles_successful',
        85: 'penalties', 218: 'penalties_won', 84: 'penalties_scored',
        83: 'penalties_missed', 217: 'penalties_committed', 41: 'offsides',
        219: 'ball_losses', 220: 'ball_recoveries',
        215: 'mistakes_leading_to_goals', 68: 'aerial_duels',
        69: 'aerial_duels_won', 155: 'ground_duels', 156: 'ground_duels_won',
        212: 'duels', 213: 'duels_won', 96: 'substitutions'
    }
    
    for detail in details:
        type_id = detail.get('type', {}).get('id') if isinstance(detail.get('type'), dict) else None
        if type_id in type_map:
            value = detail.get('value', {})
            if isinstance(value, dict):
                stats[type_map[type_id]] = value.get('total', value.get('average'))
            else:
                stats[type_map[type_id]] = value
    
    # Calculer crosses_accuracy
    if stats['crosses'] and stats['crosses_accurate']:
        try:
            stats['crosses_accuracy'] = round((stats['crosses_accurate'] / stats['crosses']) * 100, 2)
        except:
            pass
    
    return stats

def process_league(league_key, league_config):
    """Traite une ligue complète"""
    print(f"\n{'='*60}")
    print(f"🏆 {league_config['name']}")
    print(f"{'='*60}\n")
    
    teams_dir = Path(league_config['teams'])
    if not teams_dir.exists():
        print(f"  ❌ Dossier {teams_dir} introuvable")
        return {}
    
    # Filtrer seulement les vrais fichiers d'équipes
    team_files = [
        f for f in teams_dir.glob('*.json') 
        if not f.stem.endswith('_stats') and not f.stem.endswith('_complete')
    ]
    
    print(f"  📋 {len(team_files)} équipes à traiter\n")
    
    all_stats = {}
    season_ids = list(league_config['seasons'].keys())
    successful_teams = 0
    
    for t_idx, team_file in enumerate(team_files, 1):
        try:
            with open(team_file, 'r', encoding='utf-8') as f:
                team_data = json.load(f)
            
            team_name = team_data.get('name', team_file.stem)
            players = team_data.get('players', [])
            
            if not players:
                continue
            
            print(f"  [{t_idx}/{len(team_files)}] {team_name} ({len(players)} joueurs)")
            successful_players = 0
            
            for p_idx, player in enumerate(players, 1):
                player_id = player.get('id')
                if not player_id:
                    continue
                
                display_name = player.get('display_name', 'Unknown')
                
                # Progress simple
                if p_idx % 5 == 0:
                    print(f"    Progress: {p_idx}/{len(players)}...")
                
                # Récupérer les stats
                stats_data = get_player_stats(player_id, season_ids)
                
                if stats_data:
                    successful_players += 1
                    
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
                        
                        team_id = season_stat.get('team_id')
                        team_name_stat = get_team_name(team_id) if team_id else None
                        
                        # Mapper les stats
                        mapped_stats = map_stats(season_stat.get('details', []))
                        mapped_stats['team'] = team_name_stat
                        mapped_stats['team_id'] = team_id
                        mapped_stats['league'] = league_config['name']
                        
                        # Clé de la saison
                        season_key = f"{league_config['seasons'][season_id]} ({league_config['name']}, {team_name_stat})"
                        player_stats['stats'][season_key] = mapped_stats
                    
                    all_stats[player_id] = player_stats
            
            print(f"    ✅ {successful_players}/{len(players)} joueurs récupérés")
            successful_teams += 1
            
            # Pause entre équipes
            time.sleep(1)
            
        except Exception as e:
            print(f"    ❌ Erreur: {e}")
            errors.append(f"{team_name}: {str(e)[:100]}")
            continue
    
    print(f"\n  📊 Bilan: {successful_teams}/{len(team_files)} équipes traitées avec succès")
    return all_stats

def save_stats(league_key, league_config, stats):
    """Sauvegarde les stats"""
    output_file = Path(league_config['file'])
    
    ts_content = f"""// Stats COMPLÈTES des joueurs de {league_config['name']} depuis SportMonks API
// Inclut TOUTES les saisons dans TOUS les clubs
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
    
    print(f"\n  💾 Sauvegardé: {output_file.name}")
    print(f"  📊 Total: {len(stats)} joueurs")

def main():
    """Fonction principale"""
    print("🚀 Mise à jour des ligues restantes")
    print(f"⏰ Début: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    completed = []
    failed = []
    
    for league_key, league_config in LEAGUES.items():
        try:
            print(f"\n📍 Traitement de {league_config['name']}...")
            stats = process_league(league_key, league_config)
            
            if stats:
                save_stats(league_key, league_config, stats)
                completed.append(league_config['name'])
                print(f"  ✅ {league_config['name']} terminé!")
            else:
                failed.append(league_config['name'])
                print(f"  ⚠️ {league_config['name']}: Aucune donnée")
                
        except KeyboardInterrupt:
            print("\n⚠️ Interruption utilisateur")
            break
        except Exception as e:
            print(f"  ❌ Erreur pour {league_config['name']}: {e}")
            failed.append(league_config['name'])
            continue
    
    # Rapport final
    print("\n" + "=" * 60)
    print("📊 RAPPORT FINAL")
    print("=" * 60)
    
    if completed:
        print(f"\n✅ Ligues mises à jour ({len(completed)}):")
        for league in completed:
            print(f"  • {league}")
    
    if failed:
        print(f"\n⚠️ Ligues échouées ({len(failed)}):")
        for league in failed:
            print(f"  • {league}")
    
    if errors:
        print(f"\n❌ Erreurs détaillées ({len(errors)} premières):")
        for error in errors[:10]:
            print(f"  • {error}")
    
    print(f"\n⏰ Fin: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📡 Total appels API: {api_calls}")

if __name__ == "__main__":
    main()