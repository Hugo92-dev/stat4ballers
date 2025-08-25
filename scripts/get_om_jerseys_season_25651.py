#!/usr/bin/env python3
"""
Script pour récupérer les VRAIS jersey_number de l'OM
pour la saison 25651 (saison actuelle 2025/2026)
"""

import requests
import json
import time

API_TOKEN = "leBzDfKbRE5k9zEg3FuZE3Hh7XbukODNarOXLoVtPAiAtliDZ19wLu1Wnzi2"
BASE_URL = "https://api.sportmonks.com/v3/football"
SEASON_ID = 25651
OM_TEAM_ID = 44

def make_api_call(endpoint, params=None):
    """Fait un appel API avec gestion des erreurs"""
    if params is None:
        params = {}
    
    params['api_token'] = API_TOKEN
    
    try:
        response = requests.get(f"{BASE_URL}/{endpoint}", params=params, timeout=30)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error {response.status_code} for {endpoint}")
            return None
        
    except Exception as e:
        print(f"Exception: {e}")
        return None

def get_season_jersey_numbers():
    """Récupère les jersey_number pour la saison 25651"""
    
    print(f"=== Récupération des numéros OM - Saison {SEASON_ID} ===\n")
    
    # Liste des joueurs OM connus
    om_players = [
        186418,    # Gerónimo Rulli
        29186,     # Jeffrey de Lange
        186456,    # Rubén Blanco
        37593233,  # Jelle Van Neck
        527759,    # Théo Vermot
        13171199,  # Leonardo Balerdi
        32390,     # Ulisses Garcia
        586846,    # Derek Cornelius
        37369302,  # Bamo Meïté
        130063,    # Pol Lirola
        335521,    # Facundo Medina
        28575687,  # CJ Egan-Riley
        512560,    # Amir Murillo
        1744,      # Pierre-Emile Højbjerg
        21803033,  # Azzedine Ounahi
        96691,     # Amine Harit
        95696,     # Geoffrey Kondogbia
        95694,     # Adrien Rabiot
        37541144,  # Bilal Nadir
        608285,    # Angel Gomes
        37737405,  # Darryl Bakola
        433458,    # Amine Gouiri
        31739,     # Pierre-Emerick Aubameyang
        20333643,  # Mason Greenwood
        95776,     # Neal Maupay
        20315925,  # Faris Moumbagna
        29328428,  # Igor Paixão
        537332,    # Timothy Weah
        37657133,  # François Mughe
        34455209,  # Jonathan Rowe
        37713942,  # Robinio Vaz
        37729567,  # Keyliane Abdallah
    ]
    
    jersey_numbers = {}
    
    # Méthode 1: Via l'endpoint squads/seasons
    print("1. Tentative via squads/seasons...")
    squads_response = make_api_call(
        f"squads/seasons/{SEASON_ID}/teams/{OM_TEAM_ID}"
    )
    
    if squads_response and 'data' in squads_response:
        for squad_entry in squads_response['data']:
            player_id = squad_entry.get('player_id')
            jersey = squad_entry.get('jersey_number')
            if player_id and jersey:
                jersey_numbers[player_id] = jersey
                print(f"  Found player {player_id}: #{jersey}")
    
    # Méthode 2: Pour chaque joueur, chercher ses détails pour cette saison
    print("\n2. Vérification individuelle par joueur...")
    for player_id in om_players:
        if player_id not in jersey_numbers:
            # Essayer de récupérer les infos du joueur pour cette saison
            print(f"  Checking player {player_id}...")
            
            # Endpoint 1: player squads
            squad_response = make_api_call(
                f"squads",
                {'filters': f'playerIds:{player_id};seasonIds:{SEASON_ID};teamIds:{OM_TEAM_ID}'}
            )
            
            if squad_response and 'data' in squad_response:
                for entry in squad_response['data']:
                    if entry.get('team_id') == OM_TEAM_ID and entry.get('season_id') == SEASON_ID:
                        jersey = entry.get('jersey_number')
                        if jersey:
                            jersey_numbers[player_id] = jersey
                            player_name = get_player_name(player_id)
                            print(f"    → {player_name}: #{jersey}")
                            break
            
            time.sleep(0.2)  # Éviter le rate limiting
    
    return jersey_numbers

def get_player_name(player_id):
    """Récupère le nom d'un joueur"""
    response = make_api_call(f"players/{player_id}")
    if response and 'data' in response:
        return response['data'].get('display_name', f'Player {player_id}')
    return f'Player {player_id}'

def update_typescript_file(jersey_numbers):
    """Met à jour le fichier TypeScript avec les bons numéros"""
    
    import re
    
    file_path = 'data/ligue1Teams_updated_om.ts'
    
    # Lire le fichier
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    updates_made = []
    current_player_id = None
    current_player_name = None
    
    # Parcourir ligne par ligne
    for i, line in enumerate(lines):
        # Détecter l'ID du joueur
        if 'id:' in line:
            match = re.search(r'id:\s*(\d+)', line)
            if match:
                current_player_id = int(match.group(1))
        
        # Détecter le nom du joueur
        if 'nom:' in line and current_player_id:
            match = re.search(r'nom:\s*"([^"]+)"', line)
            if match:
                current_player_name = match.group(1)
        
        # Mettre à jour le numéro si on a trouvé le bon
        if 'numero:' in line and current_player_id in jersey_numbers:
            new_number = jersey_numbers[current_player_id]
            old_line = lines[i]
            
            # Extraire l'ancien numéro
            old_match = re.search(r'numero:\s*(\d+|null)', old_line)
            if old_match:
                old_value = old_match.group(1)
                if old_value != str(new_number):
                    new_line = re.sub(r'numero:\s*(\d+|null)', f'numero: {new_number}', old_line)
                    lines[i] = new_line
                    updates_made.append(f"{current_player_name}: {old_value} → #{new_number}")
    
    # Écrire le fichier mis à jour
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    return updates_made

def main():
    # Récupérer les numéros de la saison 25651
    jersey_numbers = get_season_jersey_numbers()
    
    print(f"\n=== RÉSUMÉ ===")
    print(f"Numéros trouvés: {len(jersey_numbers)}")
    
    if jersey_numbers:
        # Afficher les numéros trouvés
        print("\nNuméros de maillot saison 25651:")
        for player_id, jersey in sorted(jersey_numbers.items(), key=lambda x: x[1]):
            player_name = get_player_name(player_id)
            print(f"  #{jersey:2d} - {player_name}")
        
        # Mettre à jour le fichier TypeScript
        print("\n=== Mise à jour du fichier TypeScript ===")
        updates = update_typescript_file(jersey_numbers)
        
        if updates:
            print("Mises à jour effectuées:")
            for update in updates:
                print(f"  ✓ {update}")
            print(f"\nTotal: {len(updates)} numéros corrigés")
        else:
            print("Aucune mise à jour nécessaire")
        
        # Points importants
        if 31739 in jersey_numbers:
            print(f"\n[OK] Aubameyang a bien le #{jersey_numbers[31739]}")
    else:
        print("\nAucun numéro trouvé - vérifier l'API")

if __name__ == "__main__":
    main()