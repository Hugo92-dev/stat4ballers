#!/usr/bin/env python3
"""
Script pour récupérer TOUS les effectifs de Ligue 1
Basé sur le script robuste validé avec l'OM
Saison 2025/2026 (ID: 25651)
"""

import requests
import json
from datetime import datetime, date
from typing import Dict, List, Optional
import time
import os

API_TOKEN = "leBzDfKbRE5k9zEg3FuZE3Hh7XbukODNarOXLoVtPAiAtliDZ19wLu1Wnzi2"
BASE_URL = "https://api.sportmonks.com/v3/football"
LIGUE1_SEASON_ID = 25651

def make_api_call(endpoint: str, params: dict = None) -> Optional[Dict]:
    """Fait un appel API avec gestion des erreurs et rate limiting"""
    if params is None:
        params = {}
    
    params['api_token'] = API_TOKEN
    
    try:
        response = requests.get(f"{BASE_URL}/{endpoint}", params=params, timeout=30)
        
        if response.status_code == 429:
            print("Rate limit hit, waiting 60 seconds...")
            time.sleep(60)
            return make_api_call(endpoint, params)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error {response.status_code} for {endpoint}")
            return None
        
    except Exception as e:
        print(f"Exception: {e}")
        return None

def calculate_age(birth_date_str: str) -> Optional[int]:
    """Calcule l'âge à partir de la date de naissance"""
    if not birth_date_str:
        return None
    
    try:
        birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d').date()
        today = date.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        return age
    except:
        return None

def get_nationality_smart(player_data: dict) -> Optional[str]:
    """
    Récupère la nationalité intelligemment:
    1. D'abord essaie nationality
    2. Si null, utilise country comme fallback
    """
    # Essai 1: nationality
    nationality_data = player_data.get('nationality')
    if nationality_data and nationality_data.get('name'):
        return nationality_data.get('name')
    
    # Essai 2: country comme fallback
    country_data = player_data.get('country')
    if country_data and country_data.get('name'):
        return country_data.get('name')
    
    return "Unknown"

def get_ligue1_teams() -> Dict:
    """Récupère tous les clubs de Ligue 1 depuis l'API"""
    print(f"\n=== Récupération des équipes de Ligue 1 ===")
    
    teams = {}
    
    # Récupérer les standings pour avoir tous les clubs
    standings_response = make_api_call(
        f"standings/seasons/{LIGUE1_SEASON_ID}",
        {'include': 'participant'}
    )
    
    if standings_response and 'data' in standings_response:
        for standing in standings_response['data']:
            participant = standing.get('participant')
            if participant:
                team_id = participant.get('id')
                team_name = participant.get('name')
                if team_id and team_name:
                    # Créer un slug pour le nom
                    slug = team_name.lower().replace(' ', '-').replace('.', '').replace("'", '')
                    # Corrections spécifiques
                    if "marseille" in slug:
                        slug = "marseille"
                    elif "paris" in slug or "psg" in slug:
                        slug = "paris-saint-germain"
                    elif "lyon" in slug:
                        slug = "lyon"
                    elif "lille" in slug or "losc" in slug:
                        slug = "lille"
                    elif "monaco" in slug:
                        slug = "monaco"
                    elif "lens" in slug:
                        slug = "lens"
                    elif "rennes" in slug:
                        slug = "rennes"
                    elif "nice" in slug:
                        slug = "nice"
                    elif "strasbourg" in slug:
                        slug = "strasbourg"
                    elif "brest" in slug:
                        slug = "brest"
                    elif "reims" in slug:
                        slug = "reims"
                    elif "nantes" in slug:
                        slug = "nantes"
                    elif "montpellier" in slug:
                        slug = "montpellier"
                    elif "toulouse" in slug:
                        slug = "toulouse"
                    elif "auxerre" in slug:
                        slug = "auxerre"
                    elif "angers" in slug:
                        slug = "angers"
                    elif "saint-etienne" in slug or "saint etienne" in slug:
                        slug = "saint-etienne"
                    elif "havre" in slug:
                        slug = "le-havre"
                    
                    teams[team_id] = {
                        'name': team_name,
                        'slug': slug
                    }
                    print(f"  Found: {team_name} (ID: {team_id}, slug: {slug})")
    
    return teams

def fetch_team_squad(team_id: int, team_name: str) -> List[Dict]:
    """Récupère l'effectif complet d'une équipe avec les numéros de maillot de la saison"""
    print(f"\n  Récupération effectif {team_name}...")
    
    players_data = []
    player_ids = set()
    jersey_numbers = {}
    
    # Méthode 1: Via squads/seasons pour avoir les numéros de maillot
    squads_response = make_api_call(
        f"squads/seasons/{LIGUE1_SEASON_ID}/teams/{team_id}"
    )
    
    if squads_response and 'data' in squads_response:
        for squad_entry in squads_response['data']:
            player_id = squad_entry.get('player_id')
            jersey = squad_entry.get('jersey_number')
            if player_id:
                player_ids.add(player_id)
                if jersey:
                    jersey_numbers[player_id] = jersey
    
    # Méthode 2: Via les fixtures récentes pour compléter
    fixtures_response = make_api_call(
        "fixtures",
        {
            'filters': f'teamIds:{team_id};seasonIds:{LIGUE1_SEASON_ID}',
            'include': 'lineups.player',
            'per_page': 5
        }
    )
    
    if fixtures_response and 'data' in fixtures_response:
        for fixture in fixtures_response['data']:
            lineups = fixture.get('lineups', [])
            for lineup in lineups:
                if lineup.get('team_id') == team_id:
                    player = lineup.get('player')
                    if player and player.get('id'):
                        player_ids.add(player.get('id'))
    
    # Récupérer les détails de chaque joueur
    for player_id in player_ids:
        player_data = fetch_player_details(player_id, jersey_numbers.get(player_id))
        if player_data:
            players_data.append(player_data)
            time.sleep(0.1)  # Éviter le rate limiting
    
    return players_data

def fetch_player_details(player_id: int, jersey_number: Optional[int] = None) -> Optional[dict]:
    """Récupère les détails complets d'un joueur avec toutes les données"""
    
    player_response = make_api_call(f"players/{player_id}", {
        'include': 'nationality;country;position;detailedPosition'
    })
    
    if not player_response or 'data' not in player_response:
        return None
    
    player_data = player_response['data']
    
    # Récupérer la nationalité intelligemment
    nationality = get_nationality_smart(player_data)
    
    # Position
    position_data = player_data.get('position', {})
    position_name = position_data.get('name') if position_data else 'Unknown'
    
    # Mapping des positions
    position_mapping = {
        'Goalkeeper': 'GK',
        'Defender': 'DF',
        'Midfielder': 'MF',
        'Attacker': 'FW'
    }
    
    position_id_mapping = {
        'Goalkeeper': 24,
        'Defender': 25,
        'Midfielder': 26,
        'Attacker': 27
    }
    
    processed_data = {
        'id': player_id,
        'display_name': player_data.get('display_name') or player_data.get('name', 'Unknown'),
        'common_name': player_data.get('common_name'),
        'name': player_data.get('display_name') or player_data.get('name', 'Unknown'),
        'firstname': player_data.get('firstname', ''),
        'lastname': player_data.get('lastname', ''),
        'image_path': player_data.get('image_path'),
        'age': calculate_age(player_data.get('date_of_birth')),
        'birth_date': player_data.get('date_of_birth'),
        'height': player_data.get('height'),
        'weight': player_data.get('weight'),
        'nationality': nationality,
        'position': position_mapping.get(position_name, position_name),
        'position_id': position_id_mapping.get(position_name, 26),
        'detailed_position': player_data.get('detailedPosition', {}).get('name') if player_data.get('detailedPosition') else None,
        'jersey_number': jersey_number,
        'slug': (player_data.get('display_name') or '').lower().replace(' ', '-').replace('.', '').replace("'", '')
    }
    
    return processed_data

def generate_typescript_file(teams_data: Dict) -> str:
    """Génère le fichier TypeScript pour la Ligue 1"""
    
    ts_content = "export const ligue1Teams = [\n"
    
    for team_id, team_info in teams_data.items():
        ts_content += f"""  {{
    id: {team_id},
    nom: "{team_info['name']}",
    slug: "{team_info['slug']}",
    players: [\n"""
        
        for player in team_info.get('players', []):
            jersey = player.get('jersey_number', 'null')
            if jersey is None:
                jersey = 'null'
                
            ts_content += f"""      {{
        id: {player['id']},
        nom: "{player['display_name']}",
        displayName: "{player['display_name']}",
        position: "{player['position']}",
        position_id: {player['position_id']},
        numero: {jersey},
        age: "{player['age'] if player['age'] else 'Unknown'}",
        nationalite: "{player['nationality']}",
        taille: {player['height'] if player['height'] else 'null'},
        poids: {player['weight'] if player['weight'] else 'null'},
        image: "{player['image_path'] or 'https://cdn.sportmonks.com/images/soccer/placeholder.png'}",
        playerSlug: "{player['slug']}"
      }},\n"""
        
        ts_content = ts_content.rstrip(',\n') + "\n    ]\n  },\n"
    
    ts_content = ts_content.rstrip(',\n') + "\n];\n"
    
    return ts_content

def main():
    print("=== RÉCUPÉRATION DE TOUS LES EFFECTIFS LIGUE 1 2025/2026 ===")
    
    # Créer le dossier de sortie
    os.makedirs('data/ligue1_2025_2026', exist_ok=True)
    
    # Récupérer tous les clubs de Ligue 1
    teams = get_ligue1_teams()
    
    if not teams:
        print("ERREUR: Aucune équipe trouvée pour la Ligue 1")
        return
    
    teams_data = {}
    
    # Pour chaque équipe, récupérer l'effectif
    for team_id, team_info in teams.items():
        print(f"\n{'='*60}")
        print(f"Traitement: {team_info['name']}")
        print(f"{'='*60}")
        
        players = fetch_team_squad(team_id, team_info['name'])
        
        teams_data[team_id] = {
            'name': team_info['name'],
            'slug': team_info['slug'],
            'players': sorted(players, key=lambda x: (
                x['position_id'],
                x['jersey_number'] if x['jersey_number'] else 999,
                x['display_name']
            ))
        }
        
        print(f"    -> {len(players)} joueurs récupérés")
        
        # Pause pour éviter le rate limiting
        time.sleep(1)
    
    # Sauvegarder les données JSON
    json_file = "data/ligue1_2025_2026/ligue1_teams_complete.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(teams_data, f, indent=2, ensure_ascii=False, default=str)
    
    print(f"\n[OK] Données JSON sauvegardées: {json_file}")
    
    # Générer le fichier TypeScript
    ts_content = generate_typescript_file(teams_data)
    ts_file = "data/ligue1Teams.ts"
    
    with open(ts_file, 'w', encoding='utf-8') as f:
        f.write(ts_content)
    
    print(f"[OK] Fichier TypeScript généré: {ts_file}")
    
    print("\n=== TERMINÉ ===")
    print(f"Tous les effectifs de Ligue 1 ont été récupérés avec succès!")
    print(f"Total: {len(teams_data)} équipes")
    
    # Afficher le résumé
    for team_id, team_info in teams_data.items():
        print(f"  - {team_info['name']}: {len(team_info['players'])} joueurs")

if __name__ == "__main__":
    main()