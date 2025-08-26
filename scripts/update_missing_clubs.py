import json
import requests
from time import sleep
import sys
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv('.env.local')

# Fix pour l'encodage UTF-8 sur Windows  
sys.stdout.reconfigure(encoding='utf-8')

# Configuration API
API_TOKEN = os.getenv('SPORTMONKS_API_TOKEN')
BASE_URL = "https://api.sportmonks.com/v3/football"

if not API_TOKEN:
    print("❌ Token API non trouvé!")
    exit(1)

# Clubs spécifiques à mettre à jour
CLUBS_TO_UPDATE = {
    'ligue1': {
        'olympique-lyonnais': {
            'name': 'Olympique Lyonnais',
            'sportmonks_id': 79  # Lyon
        }
    },
    'bundesliga': {
        'fc-bayern-munchen': {
            'name': 'Bayern Munich', 
            'sportmonks_id': 503  # Bayern
        },
        'fsv-mainz-05': {
            'name': 'Mainz 05',
            'sportmonks_id': 794  # Mainz
        },
        'fc-union-berlin': {
            'name': 'Union Berlin',
            'sportmonks_id': 1079  # Union Berlin
        },
        'tsg-hoffenheim': {
            'name': 'Hoffenheim', 
            'sportmonks_id': 2726  # Hoffenheim
        },
        'fc-koln': {
            'name': '1. FC Köln',
            'sportmonks_id': 3320  # Köln
        }
    }
}

SEASONS = {
    '2025/2026': 23932,
    '2024/2025': 23194, 
    '2023/2024': 22322
}

def get_team_players(team_id, season_id):
    """Récupère tous les joueurs d'une équipe pour une saison"""
    url = f"{BASE_URL}/squads/seasons/{season_id}/teams/{team_id}"
    headers = {
        'Authorization': f'Bearer {API_TOKEN}',
    }
    params = {
        'include': 'player;player.position;player.detailedPosition'
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            return data.get('data', [])
        else:
            print(f"❌ Erreur API pour équipe {team_id}: {response.status_code}")
            return []
    except Exception as e:
        print(f"❌ Erreur requête pour équipe {team_id}: {e}")
        return []

def get_player_stats(player_id, season_id):
    """Récupère les statistiques d'un joueur pour une saison"""
    url = f"{BASE_URL}/players/{player_id}"
    headers = {
        'Authorization': f'Bearer {API_TOKEN}',
    }
    params = {
        'include': f'statistics.details;statistics.type'
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            player_data = data.get('data', {})
            
            # Filtrer les stats pour la saison demandée
            statistics = player_data.get('statistics', [])
            season_stats = None
            
            for stat in statistics:
                if stat.get('season_id') == season_id:
                    season_stats = stat
                    break
            
            return season_stats
        else:
            print(f"⚠️ Stats non trouvées pour joueur {player_id}")
            return None
    except Exception as e:
        print(f"❌ Erreur stats joueur {player_id}: {e}")
        return None

def update_club_data(league_id, club_slug, club_info):
    """Met à jour les données d'un club spécifique"""
    print(f"\n🔄 Mise à jour de {club_info['name']} ({league_id})...")
    
    team_id = club_info['sportmonks_id']
    updated_players = []
    
    # Récupérer les joueurs pour la saison la plus récente d'abord
    main_season_id = SEASONS['2025/2026']
    players_data = get_team_players(team_id, main_season_id)
    
    if not players_data:
        print(f"❌ Aucun joueur trouvé pour {club_info['name']}")
        return
    
    print(f"📊 {len(players_data)} joueurs trouvés")
    
    for player_squad in players_data:
        player_info = player_squad.get('player', {})
        player_id = player_info.get('id')
        
        if not player_id:
            continue
            
        print(f"  - {player_info.get('display_name', 'N/A')}")
        
        # Structure du joueur
        player_data = {
            'id': player_id,
            'nom': player_info.get('name', ''),
            'displayName': player_info.get('display_name', ''),
            'position': player_info.get('position', {}).get('name', 'Unknown'),
            'position_id': player_info.get('position', {}).get('id', 0),
            'numero': player_squad.get('jersey_number'),
            'age': str(player_info.get('age', '')),
            'nationalite': player_info.get('nationality', ''),
            'taille': player_info.get('height'),
            'poids': player_info.get('weight'),
            'image': player_info.get('image_path', ''),
            'playerSlug': player_info.get('display_name', '').lower().replace(' ', '-').replace("'", ""),
            'stats': {}
        }
        
        # Récupérer les stats pour chaque saison
        for season_name, season_id in SEASONS.items():
            stats = get_player_stats(player_id, season_id)
            
            if stats and stats.get('details'):
                # Formater les stats
                details = stats['details']
                season_key = season_name.replace('/', '_')
                
                player_data['stats'][season_key] = {
                    'team': club_info['name'],
                    'team_id': team_id,
                    'league': league_id,
                    'appearences': details.get('appearences'),
                    'lineups': details.get('lineups'),
                    'minutes': details.get('minutes'),
                    'goals': details.get('goals'),
                    'assists': details.get('assists'),
                    'yellow_cards': details.get('yellow_cards'),
                    'red_cards': details.get('red_cards'),
                    'rating': details.get('rating'),
                    'captain': details.get('captain'),
                    'shots': details.get('shots_total'),
                    'shots_on_target': details.get('shots_on_target'),
                    'passes': details.get('passes_total'),
                    'passes_accuracy': details.get('passes_accuracy'),
                    'key_passes': details.get('key_passes'),
                    'dribbles': details.get('dribbles_attempts'),
                    'dribbles_success': details.get('dribbles_success'),
                    'duels': details.get('duels_total'),
                    'duels_won': details.get('duels_won'),
                    'tackles': details.get('tackles'),
                    'interceptions': details.get('interceptions'),
                    'fouls': details.get('fouls_committed'),
                    'fouls_drawn': details.get('fouls_drawn'),
                    'saves': details.get('saves') if player_data['position'] == 'Goalkeeper' else None,
                    'goals_conceded': details.get('goals_conceded') if player_data['position'] == 'Goalkeeper' else None,
                    'clean_sheets': details.get('clean_sheets') if player_data['position'] == 'Goalkeeper' else None
                }
                
            sleep(0.1)  # Rate limiting
        
        updated_players.append(player_data)
    
    # Sauvegarder dans un fichier temporaire
    output_file = f'{club_slug}_updated_stats.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            'club': club_info['name'],
            'slug': club_slug,
            'league': league_id,
            'players': updated_players
        }, f, indent=2, ensure_ascii=False)
    
    print(f"✅ {club_info['name']} mis à jour - {len(updated_players)} joueurs")
    print(f"📁 Sauvegardé dans {output_file}")

def main():
    print("🚀 MISE À JOUR DES CLUBS MANQUANTS")
    print("=" * 50)
    
    total_clubs = sum(len(clubs) for clubs in CLUBS_TO_UPDATE.values())
    current = 0
    
    for league_id, clubs in CLUBS_TO_UPDATE.items():
        print(f"\n📊 {league_id.upper()} - {len(clubs)} clubs à traiter")
        
        for club_slug, club_info in clubs.items():
            current += 1
            print(f"\n[{current}/{total_clubs}] {club_info['name']}")
            update_club_data(league_id, club_slug, club_info)
            sleep(1)  # Pause entre les clubs
    
    print(f"\n✅ TERMINÉ - {total_clubs} clubs mis à jour!")

if __name__ == "__main__":
    main()