import json
import os
import requests
from datetime import datetime

API_KEY = 'a2c0e8de-f953-46ba-9d77-ff7e0ecc8db3'
BASE_URL = 'https://api.sportmonks.com/v3/football'

HEADERS = {
    'Accept': 'application/json',
    'Authorization': f'{API_KEY}'
}

RONALDO_ID = 580
MESSI_ID = 184798

def fetch_player_career_stats(player_id, player_name):
    """Récupère toutes les statistiques de carrière d'un joueur"""
    
    print(f"\nRécupération des statistiques complètes de {player_name}...")
    
    all_seasons_data = []
    
    # Récupérer toutes les saisons disponibles
    url = f"{BASE_URL}/players/{player_id}"
    params = {
        'include': 'statistics.season,statistics.details,transfers.team',
        'filters': 'statisticSeasons'
    }
    
    response = requests.get(url, headers=HEADERS, params=params)
    
    if response.status_code == 200:
        data = response.json().get('data', {})
        statistics = data.get('statistics', [])
        
        print(f"{len(statistics)} saisons trouvées pour {player_name}")
        
        for stat in statistics:
            season_info = stat.get('season', {})
            details = stat.get('details', [])
            
            # Extraire les statistiques détaillées
            stats_dict = {
                'season_id': season_info.get('id'),
                'season_name': season_info.get('name', 'Unknown'),
                'team_id': stat.get('team_id'),
                'games_played': 0,
                'goals': 0,
                'assists': 0,
                'yellow_cards': 0,
                'red_cards': 0,
                'minutes_played': 0
            }
            
            # Parcourir les détails pour extraire les stats
            for detail in details:
                type_id = detail.get('type_id')
                value = detail.get('value', {})
                
                # Mapper les types aux statistiques
                if type_id == 52:  # Games played
                    stats_dict['games_played'] = value.get('total', 0)
                elif type_id == 208:  # Goals
                    stats_dict['goals'] = value.get('total', 0)
                elif type_id == 209:  # Assists
                    stats_dict['assists'] = value.get('total', 0)
                elif type_id == 84:  # Yellow cards
                    stats_dict['yellow_cards'] = value.get('total', 0)
                elif type_id == 83:  # Red cards
                    stats_dict['red_cards'] = value.get('total', 0)
                elif type_id == 79:  # Minutes played
                    stats_dict['minutes_played'] = value.get('total', 0)
            
            all_seasons_data.append(stats_dict)
    
    # Trier par saison
    all_seasons_data.sort(key=lambda x: x['season_name'], reverse=True)
    
    return all_seasons_data

def fetch_detailed_season_stats(player_id, player_name):
    """Récupère les statistiques détaillées par saison"""
    
    print(f"\nRécupération des statistiques détaillées de {player_name}...")
    
    url = f"{BASE_URL}/players/{player_id}"
    params = {
        'include': 'statistics.season,statistics.details.type,statistics.team'
    }
    
    all_stats = []
    
    response = requests.get(url, headers=HEADERS, params=params)
    
    if response.status_code == 200:
        data = response.json()
        player_data = data.get('data', {})
        stats = player_data.get('statistics', [])
        
        if stats:
            for stat in stats:
                season = stat.get('season', {})
                team = stat.get('team', {})
                details = stat.get('details', [])
                
                season_stats = {
                    'player_id': player_id,
                    'player_name': player_name,
                    'season_id': season.get('id'),
                    'season_name': season.get('name', 'Unknown'),
                    'team_id': team.get('id'),
                    'team_name': team.get('name', 'Unknown'),
                    'statistics': {}
                }
                
                # Mapper tous les détails
                stat_mapping = {
                    52: 'matches_jouées',
                    79: 'minutes_jouées',
                    208: 'buts',
                    209: 'passes_décisives',
                    210: 'penalties_marqués',
                    211: 'penalties_ratés',
                    56: 'tirs',
                    58: 'tirs_cadrés',
                    80: 'passes',
                    81: 'passes_réussies',
                    82: 'précision_passes_%',
                    84: 'cartons_jaunes',
                    83: 'cartons_rouges',
                    85: 'fautes_commises',
                    86: 'fautes_subies',
                    64: 'dribbles_tentés',
                    65: 'dribbles_réussis',
                    45: 'duels_aériens_gagnés',
                    88: 'interceptions',
                    89: 'tacles',
                    214: 'clean_sheets',
                    78: 'hors_jeu'
                }
                
                for detail in details:
                    type_data = detail.get('type', {})
                    type_id = type_data.get('id')
                    value = detail.get('value', {})
                    
                    if type_id in stat_mapping:
                        stat_name = stat_mapping[type_id]
                        season_stats['statistics'][stat_name] = value.get('total', 0) if isinstance(value, dict) else value
                
                all_stats.append(season_stats)
    else:
        print(f"Erreur lors de la récupération: {response.status_code}")
    
    # Trier par saison (du plus récent au plus ancien)
    all_stats.sort(key=lambda x: x['season_name'], reverse=True)
    
    return all_stats

def save_goat_stats():
    """Sauvegarde les statistiques de Ronaldo et Messi"""
    
    print("Début de la récupération des statistiques CR7 vs Messi...")
    
    # Récupérer les statistiques des deux joueurs
    ronaldo_stats = fetch_detailed_season_stats(RONALDO_ID, "Cristiano Ronaldo")
    messi_stats = fetch_detailed_season_stats(MESSI_ID, "Lionel Messi")
    
    # Créer le dossier si nécessaire
    goat_dir = 'data/goat'
    os.makedirs(goat_dir, exist_ok=True)
    
    # Sauvegarder les données
    goat_data = {
        'last_updated': datetime.now().isoformat(),
        'ronaldo': {
            'player_id': RONALDO_ID,
            'name': 'Cristiano Ronaldo',
            'seasons': ronaldo_stats
        },
        'messi': {
            'player_id': MESSI_ID,
            'name': 'Lionel Messi',
            'seasons': messi_stats
        }
    }
    
    # Calculer les totaux carrière
    for player_key in ['ronaldo', 'messi']:
        player_data = goat_data[player_key]
        career_totals = {
            'total_buts': 0,
            'total_passes_décisives': 0,
            'total_matches': 0,
            'total_minutes': 0,
            'total_cartons_jaunes': 0,
            'total_cartons_rouges': 0,
            'total_tirs': 0,
            'total_tirs_cadrés': 0,
            'total_penalties_marqués': 0,
            'total_penalties_ratés': 0,
            'nombre_saisons': len(player_data['seasons'])
        }
        
        for season in player_data['seasons']:
            stats = season.get('statistics', {})
            career_totals['total_buts'] += stats.get('buts', 0)
            career_totals['total_passes_décisives'] += stats.get('passes_décisives', 0)
            career_totals['total_matches'] += stats.get('matches_jouées', 0)
            career_totals['total_minutes'] += stats.get('minutes_jouées', 0)
            career_totals['total_cartons_jaunes'] += stats.get('cartons_jaunes', 0)
            career_totals['total_cartons_rouges'] += stats.get('cartons_rouges', 0)
            career_totals['total_tirs'] += stats.get('tirs', 0)
            career_totals['total_tirs_cadrés'] += stats.get('tirs_cadrés', 0)
            career_totals['total_penalties_marqués'] += stats.get('penalties_marqués', 0)
            career_totals['total_penalties_ratés'] += stats.get('penalties_ratés', 0)
        
        # Calculer les moyennes
        if career_totals['total_matches'] > 0:
            career_totals['buts_par_match'] = round(career_totals['total_buts'] / career_totals['total_matches'], 2)
            career_totals['passes_par_match'] = round(career_totals['total_passes_décisives'] / career_totals['total_matches'], 2)
        else:
            career_totals['buts_par_match'] = 0
            career_totals['passes_par_match'] = 0
        
        player_data['career_totals'] = career_totals
    
    # Sauvegarder le fichier
    output_file = os.path.join(goat_dir, 'goat_stats.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(goat_data, f, ensure_ascii=False, indent=2)
    
    print(f"\nStatistiques sauvegardées dans {output_file}")
    print(f"Ronaldo: {len(ronaldo_stats)} saisons récupérées")
    print(f"   - Total buts: {goat_data['ronaldo']['career_totals']['total_buts']}")
    print(f"   - Total passes décisives: {goat_data['ronaldo']['career_totals']['total_passes_décisives']}")
    print(f"Messi: {len(messi_stats)} saisons récupérées")
    print(f"   - Total buts: {goat_data['messi']['career_totals']['total_buts']}")
    print(f"   - Total passes décisives: {goat_data['messi']['career_totals']['total_passes_décisives']}")
    
    return goat_data

if __name__ == "__main__":
    save_goat_stats()