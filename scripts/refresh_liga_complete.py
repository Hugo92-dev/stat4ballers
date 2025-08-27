#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de refresh complet pour La Liga
Récupère les effectifs ET génère les statistiques TypeScript
"""

import requests
import json
import sys
import os
import time
from datetime import datetime
from typing import Dict, Any, List

# Fix pour l'encodage UTF-8 sur Windows
sys.stdout.reconfigure(encoding='utf-8')

API_KEY = "leBzDfKbRE5k9zEg3FuZE3Hh7XbukODNarOXLoVtPAiAtliDZ19wLu1Wnzi2"
BASE_URL = "https://api.sportmonks.com/v3/football"

headers = {
    "Accept": "application/json",
    "Authorization": API_KEY,
}

# Configuration La Liga
LEAGUE_ID = 564
LEAGUE_NAME = "La Liga"
SEASON_ID = 25659  # Saison 2025/2026
OUTPUT_DIR = "liga_2025_2026"

# Clubs de La Liga avec leurs IDs et slugs corrects
LIGA_TEAMS = {
    3468: "real-madrid",
    83: "barcelona",
    7980: "atletico-madrid",
    13258: "athletic-club",
    594: "real-sociedad",
    485: "real-betis",
    676: "sevilla",
    3477: "villarreal",
    214: "valencia",
    231: "girona",
    459: "osasuna",
    106: "getafe",
    36: "celta-de-vigo",
    645: "mallorca",
    2975: "deportivo-alaves",
    377: "rayo-vallecano",
    528: "espanyol",
    93: "real-oviedo",
    3457: "levante",
    1099: "elche"
}

# Charger le mapping des types SportMonks
try:
    with open('sportmonks_types_mapping.json', 'r', encoding='utf-8') as f:
        TYPES_MAPPING = json.load(f)
except FileNotFoundError:
    print("⚠️ Fichier sportmonks_types_mapping.json non trouvé")
    TYPES_MAPPING = {}

def get_position_name(type_id):
    """Obtient le nom de la position à partir de l'ID SportMonks"""
    if type_id:
        for category, positions in TYPES_MAPPING.items():
            if str(type_id) in positions:
                return positions[str(type_id)]
    return "Joueur"

def fetch_player_statistics(player_id):
    """Récupère les statistiques complètes d'un joueur"""
    try:
        url = f"{BASE_URL}/players/{player_id}"
        params = {"include": "statistics.details"}
        response = requests.get(url, headers=headers, params=params, timeout=30)
        
        if response.status_code == 200:
            data = response.json().get('data', {})
            if data.get('statistics'):
                stats_data = data['statistics'].get('data', [])
                
                # Chercher les stats de la saison actuelle
                for stat in stats_data:
                    if stat.get('season_id') == SEASON_ID:
                        return parse_statistics(stat)
                
                # Si pas de stats 2025/2026, chercher 2024/2025
                for stat in stats_data:
                    if stat.get('season_id') == 23887:  # Liga 2024/2025
                        print(f"        ⏳ Utilisation stats 2024/2025")
                        return parse_statistics(stat)
        
        return get_empty_stats()
    except Exception as e:
        return get_empty_stats()

def parse_statistics(stat_data):
    """Parse les statistiques depuis la réponse API"""
    stats = {
        # Général
        "appearances": stat_data.get('appearances', 0),
        "lineups": stat_data.get('lineups', 0),
        "minutes_played": stat_data.get('minutes_played', 0),
        "captain": stat_data.get('captain', 0),
        "rating": stat_data.get('rating', 0.0),
        
        # Offensif
        "goals": stat_data.get('goals', 0),
        "assists": stat_data.get('assists', 0),
        "shots_total": 0,
        "shots_on_target": 0,
        "hit_woodwork": 0,
        "offsides": 0,
        
        # Créatif
        "passes": 0,
        "accurate_passes_percentage": 0.0,
        "key_passes": 0,
        "total_crosses": 0,
        
        # Défensif
        "total_duels": 0,
        "duels_won": 0,
        "aerials_won": 0,
        "tackles": 0,
        "fouls": 0,
        "fouls_drawn": 0,
        "yellow_cards": stat_data.get('yellowcards', 0),
        "red_cards": stat_data.get('redcards', 0),
        
        # Gardien
        "goals_conceded": stat_data.get('goals_conceded', 0),
        "saves": stat_data.get('saves', 0),
        "saves_inside_box": 0,
        "clean_sheets": stat_data.get('cleansheets', 0),
        "penalties_saved": 0
    }
    
    # Parser les détails si disponibles
    if stat_data.get('details'):
        details = stat_data['details'].get('data', []) if 'data' in stat_data['details'] else stat_data['details']
        for detail in details:
            parse_detail(detail, stats)
    
    return stats

def parse_detail(detail, stats):
    """Parse un détail de statistique"""
    type_id = detail.get('type_id') or (detail.get('type', {}).get('id') if detail.get('type') else None)
    value = detail.get('value', {})
    stat_value = value.get('total', 0) if isinstance(value, dict) else value
    
    # Mapping des type_ids vers nos stats
    mapping = {
        86: 'shots_total',
        87: 'shots_on_target',
        88: 'hit_woodwork',
        59: 'offsides',
        80: 'passes',
        81: 'accurate_passes_percentage',
        130: 'key_passes',
        82: 'total_crosses',
        105: 'total_duels',
        106: 'duels_won',
        123: 'aerials_won',
        91: 'tackles',
        56: 'fouls',
        58: 'fouls_drawn',
        209: 'saves_inside_box',
        240: 'penalties_saved'
    }
    
    if type_id in mapping:
        stats[mapping[type_id]] = stat_value or 0

def get_empty_stats():
    """Retourne des stats vides"""
    return {
        "appearances": 0, "lineups": 0, "minutes_played": 0, "captain": 0, "rating": 0.0,
        "goals": 0, "assists": 0, "shots_total": 0, "shots_on_target": 0, "hit_woodwork": 0, "offsides": 0,
        "passes": 0, "accurate_passes_percentage": 0.0, "key_passes": 0, "total_crosses": 0,
        "total_duels": 0, "duels_won": 0, "aerials_won": 0, "tackles": 0, "fouls": 0, "fouls_drawn": 0,
        "yellow_cards": 0, "red_cards": 0, "goals_conceded": 0, "saves": 0, "saves_inside_box": 0,
        "clean_sheets": 0, "penalties_saved": 0
    }

def fetch_team_data(team_id, team_slug):
    """Récupère les données d'une équipe spécifique avec stats"""
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
            if player_stats['appearances'] > 0 or player_stats['goals'] > 0 or player_stats['minutes_played'] > 0:
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
            
            # Pause pour éviter le rate limiting
            time.sleep(0.2)
        
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

def generate_typescript_stats(all_teams_data):
    """Génère le fichier TypeScript avec les stats des joueurs"""
    ts_content = """// Généré automatiquement depuis l'API SportMonks
// Stats La Liga 2025/2026

export interface PlayerStats {
  team: string;
  team_id: number;
  league: string;
  rating?: number;
  minutes: number;
  appearences: number;
  lineups: number;
  captain: number;
  goals: number;
  assists: number;
  shots: number;
  shots_on_target: number;
  hit_woodwork: number;
  saves: number;
  goals_conceded: number;
  clean_sheets: number;
  penalties_saved: number;
  passes: number;
  passes_accuracy?: number;
  key_passes: number;
  crosses: number;
  tackles: number;
  fouls: number;
  fouls_drawn: number;
  yellow_cards: number;
  red_cards: number;
  duels: number;
  duels_won: number;
  aerial_duels_won: number;
  offsides: number;
}

export interface PlayerData {
  displayName: string;
  position: string;
  jersey: number | null;
  nationality: string;
  currentTeam: string;
  stats: { [season: string]: PlayerStats };
}

export const ligaPlayersCompleteStats: { [playerId: string]: PlayerData } = {
"""
    
    for team_data in all_teams_data.values():
        team_name = team_data['name']
        team_id = team_data['id']
        
        for player in team_data['players']:
            stats = player['statistics']
            
            # Ne garder que les joueurs avec des stats
            if stats['appearances'] == 0 and stats['minutes_played'] == 0:
                continue
            
            player_entry = f"""  "{player['id']}": {{
    "displayName": "{player['display_name']}",
    "position": "{player['position']}",
    "jersey": {player['jersey_number'] if player['jersey_number'] else 'null'},
    "nationality": "{player['nationality'] or ''}",
    "currentTeam": "{team_name}",
    "stats": {{
      "2025/2026 (La Liga, {team_name})": {{
        "team": "{team_name}",
        "team_id": {team_id},
        "league": "La Liga",
        "rating": {stats['rating']},
        "minutes": {stats['minutes_played']},
        "appearences": {stats['appearances']},
        "lineups": {stats['lineups']},
        "captain": {stats['captain']},
        "goals": {stats['goals']},
        "assists": {stats['assists']},
        "shots": {stats['shots_total']},
        "shots_on_target": {stats['shots_on_target']},
        "hit_woodwork": {stats['hit_woodwork']},
        "saves": {stats['saves']},
        "goals_conceded": {stats['goals_conceded']},
        "clean_sheets": {stats['clean_sheets']},
        "penalties_saved": {stats['penalties_saved']},
        "passes": {stats['passes']},
        "passes_accuracy": {stats['accurate_passes_percentage']},
        "key_passes": {stats['key_passes']},
        "crosses": {stats['total_crosses']},
        "tackles": {stats['tackles']},
        "fouls": {stats['fouls']},
        "fouls_drawn": {stats['fouls_drawn']},
        "yellow_cards": {stats['yellow_cards']},
        "red_cards": {stats['red_cards']},
        "duels": {stats['total_duels']},
        "duels_won": {stats['duels_won']},
        "aerial_duels_won": {stats['aerials_won']},
        "offsides": {stats['offsides']}
      }}
    }}
  }},
"""
            ts_content += player_entry
    
    ts_content = ts_content.rstrip(',\n') + "\n};"
    return ts_content

def refresh_liga():
    """Rafraîchit toutes les données de La Liga avec stats"""
    
    print("=" * 60)
    print(f"🇪🇸 REFRESH LA LIGA COMPLET - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    start_time = time.time()
    
    # Créer le répertoire de sortie
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_path = os.path.join(project_root, "data", OUTPUT_DIR)
    os.makedirs(output_path, exist_ok=True)
    
    all_teams_data = {}
    success_count = 0
    error_count = 0
    
    print(f"\n📊 Récupération de {len(LIGA_TEAMS)} équipes de La Liga...")
    print("📈 Récupération des effectifs ET des statistiques...\n")
    
    # Traiter chaque équipe
    for team_id, team_slug in LIGA_TEAMS.items():
        team_data = fetch_team_data(team_id, team_slug)
        
        if team_data:
            all_teams_data[team_slug] = team_data
            
            # Sauvegarder les données JSON
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
        if team_id != list(LIGA_TEAMS.keys())[-1]:
            time.sleep(2)
    
    # Générer le fichier TypeScript avec les stats
    print("\n📝 Génération du fichier TypeScript des stats...")
    ts_content = generate_typescript_stats(all_teams_data)
    ts_path = os.path.join(project_root, "data", "la-ligaPlayersCompleteStats.ts")
    
    try:
        with open(ts_path, 'w', encoding='utf-8') as f:
            f.write(ts_content)
        print("   ✅ Fichier la-ligaPlayersCompleteStats.ts généré")
    except Exception as e:
        print(f"   ❌ Erreur génération TypeScript: {str(e)}")
    
    # Statistiques finales
    elapsed_time = time.time() - start_time
    
    print("\n" + "=" * 60)
    print("📈 RÉSUMÉ DU REFRESH LA LIGA")
    print("=" * 60)
    print(f"✅ Équipes mises à jour: {success_count}/{len(LIGA_TEAMS)}")
    print(f"❌ Erreurs: {error_count}/{len(LIGA_TEAMS)}")
    print(f"⏱️ Durée: {elapsed_time:.1f} secondes")
    
    # Compter les joueurs et stats
    total_players = 0
    players_with_stats = 0
    
    for team_data in all_teams_data.values():
        players = team_data['players']
        total_players += len(players)
        for p in players:
            stats = p['statistics']
            if stats['appearances'] > 0 or stats['goals'] > 0 or stats['minutes_played'] > 0:
                players_with_stats += 1
    
    print(f"👥 Total joueurs: {total_players}")
    print(f"📊 Joueurs avec stats: {players_with_stats}")
    print(f"\n✨ Refresh La Liga terminé!")
    
    return success_count == len(LIGA_TEAMS)

if __name__ == "__main__":
    try:
        success = refresh_liga()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⚠️ Refresh interrompu")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Erreur fatale: {str(e)}")
        sys.exit(1)