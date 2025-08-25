#!/usr/bin/env python3
"""
Script pour ajouter les joueurs manquants à notre effectif OM
"""

import requests
import json
from datetime import datetime, date

API_TOKEN = "leBzDfKbRE5k9zEg3FuZE3Hh7XbukODNarOXLoVtPAiAtliDZ19wLu1Wnzi2"
BASE_URL = "https://api.sportmonks.com/v3/football"

def make_api_call(endpoint, params=None):
    if params is None:
        params = {}
    
    params['api_token'] = API_TOKEN
    
    try:
        response = requests.get(f"{BASE_URL}/{endpoint}", params=params, timeout=30)
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

def calculate_age(birth_date_str):
    if not birth_date_str:
        return None
    
    try:
        birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d').date()
        today = date.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        return age
    except:
        return None

def process_player_data(player_data, jersey_number=None):
    """Traite les données d'un joueur selon nos spécifications"""
    
    player_id = player_data.get('id')
    display_name = player_data.get('display_name') or player_data.get('name', 'Unknown')
    common_name = player_data.get('common_name', display_name)
    firstname = player_data.get('firstname', '')
    lastname = player_data.get('lastname', '')
    
    image_path = player_data.get('image_path')
    
    birth_date = player_data.get('date_of_birth')
    age = calculate_age(birth_date) if birth_date else None
    height = player_data.get('height')
    weight = player_data.get('weight')
    
    nationality_data = player_data.get('nationality', {})
    nationality_name = nationality_data.get('name') if nationality_data else None
    
    position_data = player_data.get('position', {})
    position_name = position_data.get('name') if position_data else 'Unknown'
    
    detailed_position_data = player_data.get('detailedPosition', {})
    detailed_position = detailed_position_data.get('name') if detailed_position_data else None
    
    def format_position(pos):
        mapping = {
            'Goalkeeper': 'GK',
            'Defender': 'DF', 
            'Midfielder': 'MF',
            'Attacker': 'FW'
        }
        return mapping.get(pos, pos)
    
    def get_position_id(pos):
        mapping = {
            'Goalkeeper': 24,
            'Defender': 25,
            'Midfielder': 26,
            'Attacker': 27
        }
        return mapping.get(pos, 26)
    
    processed_data = {
        'id': player_id,
        'display_name': display_name,
        'common_name': common_name,
        'name': display_name,
        'firstname': firstname,
        'lastname': lastname,
        'image_path': image_path,
        'age': age,
        'birth_date': birth_date,
        'height': height,
        'weight': weight,
        'nationality': nationality_name,
        'position': format_position(position_name),
        'position_id': get_position_id(position_name),
        'detailed_position': detailed_position,
        'jersey_number': jersey_number,
        'slug': display_name.lower().replace(' ', '-').replace('.', '').replace("'", '') if display_name else None
    }
    
    return processed_data

def main():
    print("=== Ajout des joueurs manquants ===\\n")
    
    # IDs et numéros des joueurs manquants
    missing_players_info = {
        37713942: 34,  # Robinio Vaz
        37729567: 48,  # Keyliane Abdallah
    }
    
    # 1. Charger nos données actuelles
    with open('om_complete_squad_final.json', 'r', encoding='utf-8') as f:
        current_data = json.load(f)
    
    print(f"Effectif actuel: {len(current_data['players'])} joueurs")
    
    # 2. Récupérer les données des joueurs manquants
    new_players = []
    
    for player_id, jersey_number in missing_players_info.items():
        print(f"\\nRécupération du joueur {player_id}...")
        
        player_data = make_api_call(f"players/{player_id}", {
            'include': 'nationality;position;detailedPosition;country;city'
        })
        
        if player_data and 'data' in player_data:
            processed = process_player_data(player_data['data'], jersey_number)
            new_players.append(processed)
            
            print(f"SUCCESS: {processed['display_name']}")
            print(f"  Position: {processed['position']} (ID: {processed['position_id']})")
            print(f"  Nationalité: {processed['nationality']}")
            print(f"  Âge: {processed['age']} ans")
            print(f"  Taille: {processed['height']} cm")
            print(f"  Jersey: #{processed['jersey_number']}")
        else:
            print(f"FAILED: Impossible de récupérer les données du joueur {player_id}")
    
    # 3. Ajouter les nouveaux joueurs à l'effectif
    if new_players:
        current_data['players'].extend(new_players)
        current_data['players_count'] = len(current_data['players'])
        current_data['updated_at'] = datetime.now().isoformat()
        current_data['added_players'] = len(new_players)
        
        # Sauvegarder l'effectif mis à jour
        with open('om_complete_squad_updated.json', 'w', encoding='utf-8') as f:
            json.dump(current_data, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"\\n=== RÉSUMÉ ===")
        print(f"Effectif précédent: {len(current_data['players']) - len(new_players)} joueurs")
        print(f"Joueurs ajoutés: {len(new_players)}")
        print(f"Nouvel effectif: {len(current_data['players'])} joueurs")
        print(f"Données sauvées dans: om_complete_squad_updated.json")
        
        # 4. Mettre à jour aussi le fichier TypeScript
        print(f"\\n=== Mise à jour TypeScript ===")
        
        # Convertir les nouveaux joueurs au format TypeScript
        ts_additions = []
        for player in new_players:
            ts_player = f"""      {{
        id: {player['id']},
        nom: "{player['display_name']}",
        displayName: "{player['display_name']}",
        position: "{player['position']}",
        position_id: {player['position_id']},
        numero: {player['jersey_number'] if player['jersey_number'] else 'null'},
        age: "{player['age']}",
        nationalite: "{player['nationality'] or 'Unknown'}",
        taille: {player['height'] if player['height'] else 'null'},
        poids: {player['weight'] if player['weight'] else 'null'},
        image: "{player['image_path'] or 'https://cdn.sportmonks.com/images/soccer/placeholder.png'}",
        playerSlug: "{player['slug']}"
      }}"""
            
            ts_additions.append(ts_player)
        
        print(f"\\nNouveaux joueurs à ajouter au fichier TypeScript:")
        for addition in ts_additions:
            print(addition)
        
        # Sauvegarder les ajouts TypeScript dans un fichier séparé
        with open('new_players_typescript.txt', 'w', encoding='utf-8') as f:
            f.write(',\\n'.join(ts_additions))
        
        print(f"\\nCode TypeScript sauvé dans: new_players_typescript.txt")
        
    else:
        print("\\nAucun nouveau joueur récupéré")

if __name__ == "__main__":
    main()