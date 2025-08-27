#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de refresh pour la Ligue 1
Récupère les effectifs ET les statistiques réelles de tous les clubs
"""

import requests
import json
import sys
import os
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

# Fix pour l'encodage UTF-8 sur Windows
sys.stdout.reconfigure(encoding='utf-8')

API_KEY = "leBzDfKbRE5k9zEg3FuZE3Hh7XbukODNarOXLoVtPAiAtliDZ19wLu1Wnzi2"
BASE_URL = "https://api.sportmonks.com/v3/football"

headers = {
    "Accept": "application/json",
    "Authorization": API_KEY,
}

# Configuration Ligue 1
LEAGUE_ID = 301
LEAGUE_NAME = "Ligue 1"
SEASON_ID = 25651  # Saison 2025/2026
OUTPUT_DIR = "ligue1_2025_2026"

# Clubs de Ligue 1 avec leurs IDs et slugs corrects
LIGUE1_TEAMS = {
    85: "paris-saint-germain",
    591: "olympique-marseille", 
    79: "olympique-lyonnais",
    81: "as-monaco",
    76: "lille",
    83: "rennes",
    84: "nice",
    90: "reims",
    88: "montpellier",
    89: "nantes",
    82: "lens",
    266: "brest",
    95: "toulouse",
    93: "strasbourg",
    1020: "auxerre",
    295: "angers",
    75: "bordeaux",
    87: "metz",
    590: "le-havre",
}

# Charger le mapping des types SportMonks
try:
    with open('sportmonks_types_mapping.json', 'r', encoding='utf-8') as f:
        TYPES_MAPPING = json.load(f)
except FileNotFoundError:
    print("⚠️ Fichier sportmonks_types_mapping.json non trouvé, utilisation des positions par défaut")
    TYPES_MAPPING = {}

def get_position_name(type_id):
    """Obtient le nom de la position à partir de l'ID SportMonks"""
    if type_id:
        for category, positions in TYPES_MAPPING.items():
            if str(type_id) in positions:
                return positions[str(type_id)]
    return "Joueur"

def fetch_player_statistics(player_id, season_id=SEASON_ID):
    """Récupère les statistiques d'un joueur pour la saison"""
    try:
        stats_url = f"{BASE_URL}/statistics/seasons/players"
        params = {
            "api_token": API_KEY,
            "filters[player_ids]": player_id,
            "filters[season_ids]": season_id,
            "include": "details"
        }
        
        response = requests.get(stats_url, headers=headers, params=params, timeout=30)
        
        if response.status_code == 200:
            data = response.json().get('data', [])
            if data and len(data) > 0:
                stats = data[0]
                details = stats.get('details', {}).get('data', []) if stats.get('details') else []
                
                # Parser les détails pour obtenir les stats spécifiques
                result = {
                    "goals": 0,
                    "assists": 0, 
                    "yellow_cards": 0,
                    "red_cards": 0,
                    "minutes_played": 0
                }
                
                for detail in details:
                    type_id = detail.get('type', {}).get('id')
                    value = detail.get('value', {}).get('total')
                    
                    # Mapping des IDs SportMonks vers nos stats
                    if type_id == 52:  # Goals
                        result["goals"] = value or 0
                    elif type_id == 79:  # Assists
                        result["assists"] = value or 0
                    elif type_id == 84:  # Yellow cards
                        result["yellow_cards"] = value or 0
                    elif type_id == 83:  # Red cards
                        result["red_cards"] = value or 0
                    elif type_id == 90:  # Minutes played
                        result["minutes_played"] = value or 0
                
                # Fallback avec les valeurs directes si disponibles
                if stats.get('goals') is not None:
                    result["goals"] = stats['goals']
                if stats.get('assists') is not None:
                    result["assists"] = stats['assists']
                if stats.get('yellowcards') is not None:
                    result["yellow_cards"] = stats['yellowcards']
                if stats.get('redcards') is not None:
                    result["red_cards"] = stats['redcards']
                if stats.get('minutes_played') is not None:
                    result["minutes_played"] = stats['minutes_played']
                    
                return result
        
        # Retourner des stats vides si pas de données
        return {
            "goals": 0,
            "assists": 0,
            "yellow_cards": 0,
            "red_cards": 0,
            "minutes_played": 0
        }
        
    except Exception as e:
        return {
            "goals": 0,
            "assists": 0,
            "yellow_cards": 0,
            "red_cards": 0,
            "minutes_played": 0
        }

def fetch_team_data(team_id, team_slug):
    """Récupère les données d'une équipe spécifique avec les stats des joueurs"""
    
    try:
        print(f"  🔄 {team_slug}...")
        
        # 1. Infos du club
        club_url = f"{BASE_URL}/teams/{team_id}"
        params = {"api_token": API_KEY, "include": "venue"}
        response = requests.get(club_url, headers=headers, params=params, timeout=30)
        
        if response.status_code != 200:
            print(f"    ❌ Erreur infos club: {response.status_code}")
            return None
            
        club_data = response.json()['data']
        
        # 2. Effectif
        squad_url = f"{BASE_URL}/squads/teams/{team_id}"
        params = {"api_token": API_KEY, "include": "player"}
        response = requests.get(squad_url, headers=headers, params=params, timeout=30)
        
        if response.status_code != 200:
            print(f"    ❌ Erreur effectif: {response.status_code}")
            return None
            
        squad_data = response.json()['data']
        
        # 3. Traiter les joueurs avec leurs stats
        players = []
        stats_fetched = 0
        
        for item in squad_data:
            if not item.get('player'):
                continue
                
            player = item['player']
            position = get_position_name(player.get('position_id'))
            
            # Récupérer les statistiques du joueur
            player_stats = fetch_player_statistics(player['id'])
            if player_stats['goals'] > 0 or player_stats['assists'] > 0 or player_stats['minutes_played'] > 0:
                stats_fetched += 1
            
            player_data = {
                "id": player['id'],
                "name": player['name'],
                "display_name": player.get('display_name', player['name']),
                "position": position,
                "jersey_number": item.get('jersey_number'),
                "age": datetime.now().year - int(player['date_of_birth'][:4]) if player.get('date_of_birth') else None,
                "date_of_birth": player.get('date_of_birth'),
                "nationality": player.get('nationality', {}).get('name') if player.get('nationality') else None,
                "height": player.get('height'),
                "weight": player.get('weight'),
                "image_path": player.get('image_path'),
                "statistics": player_stats,
                "market_value": None
            }
            players.append(player_data)
            
            # Petite pause entre les requêtes de stats pour éviter le rate limiting
            time.sleep(0.5)
        
        # Structure finale
        team_data = {
            "id": team_id,
            "name": club_data['name'],
            "short_name": club_data.get('short_code'),
            "slug": team_slug,
            "founded": club_data.get('founded'),
            "logo_path": club_data.get('image_path'),
            "venue": {
                "name": club_data.get('venue', {}).get('name') if club_data.get('venue') else None,
                "capacity": club_data.get('venue', {}).get('capacity') if club_data.get('venue') else None,
                "city": club_data.get('venue', {}).get('city', {}).get('name') if club_data.get('venue') and club_data['venue'].get('city') else None,
            } if club_data.get('venue') else None,
            "players": players,
            "last_updated": datetime.now().isoformat()
        }
        
        print(f"    ✅ {len(players)} joueurs - {stats_fetched} avec stats")
        return team_data
        
    except Exception as e:
        print(f"    ❌ Erreur: {str(e)}")
        return None

def refresh_ligue1():
    """Rafraîchit toutes les données de la Ligue 1 avec les stats"""
    
    print("=" * 60)
    print(f"🇫🇷 REFRESH LIGUE 1 AVEC STATS - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    start_time = time.time()
    
    # Créer le répertoire de sortie
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_path = os.path.join(project_root, "data", OUTPUT_DIR)
    os.makedirs(output_path, exist_ok=True)
    
    success_count = 0
    error_count = 0
    
    print(f"\n📊 Récupération de {len(LIGUE1_TEAMS)} équipes de Ligue 1...")
    print("📈 Récupération des effectifs ET des statistiques des joueurs...")
    
    # Traiter chaque équipe
    for team_id, team_slug in LIGUE1_TEAMS.items():
        team_data = fetch_team_data(team_id, team_slug)
        
        if team_data:
            # Sauvegarder les données
            filename = f"{team_slug}.json"
            filepath = os.path.join(output_path, filename)
            
            try:
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(team_data, f, ensure_ascii=False, indent=2)
                success_count += 1
            except Exception as e:
                print(f"    ❌ Erreur sauvegarde {team_slug}: {str(e)}")
                error_count += 1
        else:
            error_count += 1
        
        # Pause entre les équipes
        if team_id != list(LIGUE1_TEAMS.keys())[-1]:
            time.sleep(3)
    
    # Statistiques finales
    elapsed_time = time.time() - start_time
    
    print("\n" + "=" * 60)
    print("📈 RÉSUMÉ DU REFRESH LIGUE 1")
    print("=" * 60)
    print(f"✅ Équipes mises à jour: {success_count}/{len(LIGUE1_TEAMS)}")
    print(f"❌ Erreurs: {error_count}/{len(LIGUE1_TEAMS)}")
    print(f"⏱️ Durée: {elapsed_time:.1f} secondes")
    
    # Compter le nombre total de joueurs et ceux avec des stats
    total_players = 0
    players_with_stats = 0
    for filename in os.listdir(output_path):
        if filename.endswith('.json'):
            try:
                with open(os.path.join(output_path, filename), 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    players = data.get('players', [])
                    total_players += len(players)
                    for p in players:
                        stats = p.get('statistics', {})
                        if stats.get('goals', 0) > 0 or stats.get('assists', 0) > 0 or stats.get('minutes_played', 0) > 0:
                            players_with_stats += 1
            except:
                pass
    
    print(f"👥 Total joueurs: {total_players}")
    print(f"📊 Joueurs avec stats: {players_with_stats}")
    print(f"\n✨ Refresh Ligue 1 avec stats terminé!")
    
    return success_count == len(LIGUE1_TEAMS)

if __name__ == "__main__":
    try:
        success = refresh_ligue1()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⚠️ Refresh interrompu")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Erreur fatale: {str(e)}")
        sys.exit(1)