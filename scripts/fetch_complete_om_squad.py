#!/usr/bin/env python3
"""
Script pour récupérer TOUS les joueurs de l'OM avec leurs données complètes
Utilise les IDs trouvés dans ligue1Teams.ts
"""

import requests
import json
import time
from datetime import datetime, date
from typing import Dict, List, Any, Optional

API_TOKEN = "leBzDfKbRE5k9zEg3FuZE3Hh7XbukODNarOXLoVtPAiAtliDZ19wLu1Wnzi2"
BASE_URL = "https://api.sportmonks.com/v3/football"

OM_TEAM_ID = 44
SEASON_2025_26_ID = 25651
LIGUE1_ID = 301

# IDs de tous les joueurs de l'OM trouvés dans ligue1Teams.ts
OM_PLAYER_IDS = [
    537332,    # Timothy Weah
    29328428,  # Igor Paixão
    32390,     # Ulisses Garcia
    335521,    # Facundo Medina
    21803033,  # Azzedine Ounahi
    20315925,  # Faris Moumbagna
    20333643,  # Mason Greenwood
    37657133,  # François Mughe
    433458,    # Amine Gouiri
    95776,     # Neal Maupay
    28575687,  # CJ Egan-Riley
    37369302,  # Bamo Meïté
    608285,    # Angel Gomes
    34455209,  # Jonathan Rowe
    37593233,  # Jelle Van Neck
    13171199,  # Leonardo Balerdi
    586846,    # Derek Cornelius
    186456,    # Rubén Blanco
    95694,     # Adrien Rabiot
    37737405,  # Darryl Bakola
    527759,    # Théo Vermot
    130063,    # Pol Lirola
    512560,    # Amir Murillo
    37541144,  # Bilal Nadir
    31739,     # Pierre-Emerick Aubameyang
    186418,    # Gerónimo Rulli
    29186,     # Jeffrey de Lange
    96691,     # Amine Harit
    95696,     # Geoffrey Kondogbia
    1744,      # Pierre-Emile Højbjerg
]

def make_api_call(endpoint: str, params: dict = None) -> Optional[Dict]:
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
            print(f"Error {response.status_code}: {response.text[:100]}")
            return None
        
    except Exception as e:
        print(f"Exception: {e}")
        return None

def calculate_age(birth_date_str: str) -> Optional[int]:
    if not birth_date_str:
        return None
    
    try:
        birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d').date()
        today = date.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        return age
    except (ValueError, TypeError):
        return None

def get_player_complete_data(player_id: int) -> Optional[Dict]:
    """Récupère toutes les données d'un joueur avec includes complets"""
    print(f"Getting player {player_id}...")
    
    includes = [
        'country', 'nationality', 'city', 'position', 'detailedPosition', 'teams'
    ]
    
    params = {
        'include': ';'.join(includes)
    }
    
    data = make_api_call(f"players/{player_id}", params)
    
    if data and 'data' in data:
        return data['data']
    
    return None

def process_player_data(player_data: Dict, existing_data: Dict = None) -> Dict:
    """Traite les données d'un joueur selon les spécifications exactes demandées"""
    
    # Informations de base
    player_id = player_data.get('id')
    display_name = player_data.get('display_name') or player_data.get('name', 'Unknown')
    common_name = player_data.get('common_name', display_name)
    firstname = player_data.get('firstname', '')
    lastname = player_data.get('lastname', '')
    
    # Photo
    image_path = player_data.get('image_path')
    
    # Âge et mensurations  
    birth_date = player_data.get('date_of_birth')
    age = calculate_age(birth_date) if birth_date else None
    height = player_data.get('height')  # en cm
    weight = player_data.get('weight')  # en kg
    
    # NATIONALITÉ SPORTIVE (pas le pays de naissance)
    nationality_data = player_data.get('nationality', {})
    nationality_name = nationality_data.get('name') if nationality_data else None
    
    # Position générale
    position_data = player_data.get('position', {})
    position_name = position_data.get('name') if position_data else 'Unknown'
    
    # Position détaillée
    detailed_position_data = player_data.get('detailedPosition', {})
    detailed_position = detailed_position_data.get('name') if detailed_position_data else None
    
    # Numéro de maillot - d'abord essayer depuis les données existantes
    jersey_number = None
    if existing_data:
        jersey_number = existing_data.get('numero')
    
    # Si pas trouvé, essayer depuis les équipes
    if not jersey_number:
        teams = player_data.get('teams', [])
        for team in teams:
            if team.get('id') == OM_TEAM_ID and 'pivot' in team:
                jersey_number = team['pivot'].get('jersey_number')
                break
    
    processed_data = {
        'id': player_id,
        'display_name': display_name,  # NOM D'AFFICHAGE comme demandé
        'common_name': common_name,
        'name': display_name,  # Utiliser display_name comme nom principal
        'firstname': firstname,
        'lastname': lastname,
        'image_path': image_path,  # PHOTO comme demandée
        'age': age,  # ÂGE comme demandé
        'birth_date': birth_date,
        'height': height,  # TAILLE comme demandée
        'weight': weight,
        'nationality': nationality_name,  # NATIONALITÉ SPORTIVE comme demandée
        'position': position_name,  # POSITION comme demandée
        'detailed_position': detailed_position,  # POSITION DÉTAILLÉE comme demandée
        'jersey_number': jersey_number,  # NUMÉRO DE MAILLOT comme demandé
        'slug': display_name.lower().replace(' ', '-').replace('.', '').replace("'", '') if display_name else None
    }
    
    return processed_data

def main():
    print("=== Récupération COMPLÈTE de l'effectif OM ===\n")
    print(f"Team ID: {OM_TEAM_ID}")
    print(f"Season: {SEASON_2025_26_ID}")
    print(f"Joueurs à traiter: {len(OM_PLAYER_IDS)}")
    
    # Charger les données existantes pour les numéros de maillot
    existing_players_data = {}
    try:
        # Pas besoin de lire le fichier TypeScript, on a déjà les IDs
        pass
    except:
        pass
    
    complete_players_data = []
    failed_players = []
    
    for i, player_id in enumerate(OM_PLAYER_IDS):
        print(f"\n--- Joueur {i+1}/{len(OM_PLAYER_IDS)} (ID: {player_id}) ---")
        
        # Récupérer les données complètes depuis l'API
        player_data = get_player_complete_data(player_id)
        
        if player_data:
            # Traiter les données
            processed = process_player_data(player_data, existing_players_data.get(player_id))
            complete_players_data.append(processed)
            
            print(f"SUCCESS: {processed['display_name']}")
            print(f"  Position: {processed['position']} ({processed['detailed_position']})")
            print(f"  Nationalité: {processed['nationality']}")
            print(f"  Âge: {processed['age']} ans")
            print(f"  Taille: {processed['height']} cm")
            print(f"  Jersey: #{processed['jersey_number'] or 'N/A'}")
        else:
            failed_players.append(player_id)
            print(f"FAILED: Could not get data for player {player_id}")
        
        # Pause pour éviter le rate limiting
        time.sleep(1)
    
    # Sauvegarder les données
    output_data = {
        'team_id': OM_TEAM_ID,
        'team_name': 'Olympique Marseille',
        'season_id': SEASON_2025_26_ID,
        'season_name': '2025/2026',
        'league_id': LIGUE1_ID,
        'league_name': 'Ligue 1',
        'fetched_at': datetime.now().isoformat(),
        'total_players_attempted': len(OM_PLAYER_IDS),
        'successful_players': len(complete_players_data),
        'failed_players': len(failed_players),
        'failed_player_ids': failed_players,
        'players': complete_players_data
    }
    
    # Sauvegarder dans le répertoire racine
    output_file = 'om_complete_squad_final.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False, default=str)
    
    print(f"\n=== RÉSUMÉ FINAL ===")
    print(f"Équipe: {output_data['team_name']}")
    print(f"Saison: {output_data['season_name']}")
    print(f"Joueurs tentés: {output_data['total_players_attempted']}")
    print(f"Joueurs réussis: {output_data['successful_players']}")
    print(f"Joueurs échoués: {output_data['failed_players']}")
    if failed_players:
        print(f"IDs échoués: {failed_players}")
    print(f"Données sauvées dans: {output_file}")
    
    # Vérification des données requises
    print(f"\n=== VÉRIFICATION DES DONNÉES REQUISES ===")
    complete_count = 0
    for player in complete_players_data:
        has_all_required = all([
            player.get('display_name'),
            player.get('image_path'),
            player.get('age') is not None,
            player.get('height') is not None,
            player.get('nationality'),
            player.get('position')
        ])
        if has_all_required:
            complete_count += 1
        else:
            print(f"INCOMPLETE: {player['display_name']} - missing data")
    
    print(f"Joueurs avec TOUTES les données requises: {complete_count}/{len(complete_players_data)}")
    
    # Échantillon des premiers joueurs
    if complete_players_data:
        print(f"\n=== ÉCHANTILLON (Premiers 5 joueurs) ===")
        for player in complete_players_data[:5]:
            print(f"\n{player['display_name']}")
            print(f"  Photo: {player['image_path']}")
            print(f"  Âge: {player['age']} ans")
            print(f"  Taille: {player['height']} cm")
            print(f"  Nationalité: {player['nationality']}")
            print(f"  Position: {player['position']} ({player['detailed_position']})")
            print(f"  Numéro: #{player['jersey_number'] or 'N/A'}")

if __name__ == "__main__":
    main()