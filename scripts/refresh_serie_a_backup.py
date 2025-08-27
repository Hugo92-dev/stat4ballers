#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de refresh pour la Serie A
Récupère les effectifs et statistiques de tous les clubs
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

# Configuration Serie A
LEAGUE_ID = 384
LEAGUE_NAME = "Serie A"
SEASON_ID = 25533  # Saison 2025/2026
OUTPUT_DIR = "serie-a_2025_2026"

# Clubs de Serie A avec leurs IDs et slugs corrects
SERIE_A_TEAMS = {
    625: "juventus",
    2930: "inter",
    113: "milan",
    597: "napoli",
    37: "roma",
    43: "lazio",
    708: "atalanta",
    109: "fiorentina",
    8513: "bologna",
    613: "torino",
    346: "udinese",
    102: "genoa",
    2714: "sassuolo",
    7790: "lecce",
    585: "cagliari",
    1123: "hellas-verona",
    398: "parma",
    268: "como",
    10722: "cremonese",
    1072: "pisa"
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

def fetch_team_data(team_id, team_slug):
    """Récupère les données d'une équipe spécifique"""
    
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
        
        # 3. Traiter les joueurs
        players = []
        for item in squad_data:
            if not item.get('player'):
                continue
                
            player = item['player']
            position = get_position_name(player.get('position_id'))
            
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
                "statistics": {
                    "goals": 0,
                    "assists": 0,
                    "yellow_cards": 0,
                    "red_cards": 0,
                    "minutes_played": 0
                },
                "market_value": None
            }
            players.append(player_data)
        
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
        
        print(f"    ✅ {len(players)} joueurs")
        return team_data
        
    except Exception as e:
        print(f"    ❌ Erreur: {str(e)}")
        return None

def refresh_serie_a():
    """Rafraîchit toutes les données de la Serie A"""
    
    print("=" * 60)
    print(f"🇮🇹 REFRESH SERIE A - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    start_time = time.time()
    
    # Créer le répertoire de sortie
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_path = os.path.join(project_root, "data", OUTPUT_DIR)
    os.makedirs(output_path, exist_ok=True)
    
    success_count = 0
    error_count = 0
    
    print(f"\n📊 Récupération de {len(SERIE_A_TEAMS)} équipes de Serie A...")
    
    # Traiter chaque équipe
    for team_id, team_slug in SERIE_A_TEAMS.items():
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
        
        # Pause entre les requêtes
        if team_id != list(SERIE_A_TEAMS.keys())[-1]:
            time.sleep(2)
    
    # Statistiques finales
    elapsed_time = time.time() - start_time
    
    print("\n" + "=" * 60)
    print("📈 RÉSUMÉ DU REFRESH SERIE A")
    print("=" * 60)
    print(f"✅ Équipes mises à jour: {success_count}/{len(SERIE_A_TEAMS)}")
    print(f"❌ Erreurs: {error_count}/{len(SERIE_A_TEAMS)}")
    print(f"⏱️ Durée: {elapsed_time:.1f} secondes")
    
    # Compter le nombre total de joueurs
    total_players = 0
    for filename in os.listdir(output_path):
        if filename.endswith('.json'):
            try:
                with open(os.path.join(output_path, filename), 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    total_players += len(data.get('players', []))
            except:
                pass
    
    print(f"👥 Total joueurs: {total_players}")
    print(f"\n✨ Refresh Serie A terminé!")
    
    return success_count == len(SERIE_A_TEAMS)

if __name__ == "__main__":
    try:
        success = refresh_serie_a()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⚠️ Refresh interrompu")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Erreur fatale: {str(e)}")
        sys.exit(1)