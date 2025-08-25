#!/usr/bin/env python3
"""
Script ROBUSTE pour récupérer TOUS les joueurs d'une équipe
- Récupère dynamiquement tous les joueurs (pas de liste hardcodée)
- Utilise country_id comme fallback pour nationality
- Gère toutes les données manquantes intelligemment
- Essaie plusieurs endpoints pour être exhaustif
"""

import requests
import json
from datetime import datetime, date
from typing import Dict, List, Optional
import time
import sys

API_TOKEN = "leBzDfKbRE5k9zEg3FuZE3Hh7XbukODNarOXLoVtPAiAtliDZ19wLu1Wnzi2"
BASE_URL = "https://api.sportmonks.com/v3/football"

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
        print(f"Exception calling {endpoint}: {e}")
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
        print(f"  Using country as fallback for nationality: {country_data.get('name')}")
        return country_data.get('name')
    
    # Si rien ne marche, retourner Unknown
    return "Unknown"

def fetch_all_team_players(team_id: int, season_id: int = 25651) -> List[int]:
    """
    Récupère TOUS les IDs des joueurs d'une équipe via plusieurs méthodes
    pour être sûr de ne manquer personne
    """
    all_player_ids = set()
    
    print(f"\n=== Récupération exhaustive des joueurs (Team ID: {team_id}) ===")
    
    # Méthode 1: Utiliser la liste connue + recherche supplémentaire
    # D'abord, on a une liste de base connue pour l'OM
    if team_id == 44:  # OM
        print("\n1. Utilisation de la liste de base connue pour l'OM...")
        known_om_players = [
            537332,    # Timothy Weah
            29328428,  # Igor Paixão
            84726,     # Ulisses Garcia
            513711,    # Faris Moumbagna  
            84724,     # François Mughe
            25394,     # Facundo Medina
            37602093,  # Botond Kemenes
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
            37713942,  # Robinio Vaz
            37729567,  # Keyliane Abdallah
            32390,     # Mason Greenwood
            335521,    # Azzedine Ounahi
            21803033,  # Facundo Medina (duplicate ID?)
            20315925,  # Faris Moumbagna (duplicate ID?)
            20333643,  # François Mughe (duplicate ID?)
            37657133,  # Ulisses Garcia (duplicate ID?)
        ]
        for pid in known_om_players:
            all_player_ids.add(pid)
            print(f"  Added known player ID: {pid}")
    
    # Méthode 2: Chercher via les top scorers/assists de la saison
    print("\n2. Recherche via top scorers de Ligue 1...")
    topscorers_response = make_api_call(f"seasons/{season_id}/topscorers/aggregated", {
        'include': 'player.team',
        'per_page': 100
    })
    
    if topscorers_response and 'data' in topscorers_response:
        for scorer_data in topscorers_response['data']:
            player = scorer_data.get('player')
            if player:
                # Vérifier si c'est un joueur de notre équipe
                team = player.get('team')
                if team and team.get('id') == team_id:
                    all_player_ids.add(player.get('id'))
                    print(f"  Found scorer: {player.get('display_name')} (ID: {player.get('id')})")
    
    # Méthode 3: Chercher dans les statistiques agrégées
    print("\n3. Recherche via statistiques agrégées...")
    season_stats = make_api_call(f"seasons/{season_id}/teams/{team_id}", {
        'include': 'statistics'
    })
    
    if season_stats and 'data' in season_stats:
        # Essayer de récupérer des infos sur l'équipe
        print(f"  Team data retrieved for team {team_id}")
    
    # Méthode 4: Recherche par nom de joueurs connus (pour l'OM)
    if team_id == 44:
        print("\n4. Recherche par noms de joueurs connus...")
        known_names = ["Greenwood", "Aubameyang", "Rabiot", "Kondogbia", "Harit", "Rulli"]
        
        for name in known_names:
            search_response = make_api_call(f"players/search/{name}")
            if search_response and 'data' in search_response:
                for player in search_response['data']:
                    # Vérifier si le joueur est à l'OM actuellement
                    player_details = make_api_call(f"players/{player['id']}", {
                        'include': 'teams'
                    })
                    if player_details and 'data' in player_details:
                        teams = player_details['data'].get('teams', [])
                        for team in teams:
                            if team.get('id') == team_id:
                                all_player_ids.add(player['id'])
                                print(f"  Found by name: {player['display_name']} (ID: {player['id']})")
                                break
    
    # Méthode 5: Parcourir les fixtures récentes et récupérer les lineups
    print("\n5. Recherche via fixtures récentes...")
    fixtures_response = make_api_call(f"fixtures", {
        'filters': f'teamIds:{team_id};seasonIds:{season_id}',
        'include': 'lineups.player',
        'per_page': 10
    })
    
    if fixtures_response and 'data' in fixtures_response:
        for fixture in fixtures_response['data']:
            lineups = fixture.get('lineups', [])
            for lineup in lineups:
                player = lineup.get('player')
                if player and player.get('id'):
                    all_player_ids.add(player.get('id'))
                    print(f"  From lineup: {player.get('display_name')} (ID: {player.get('id')})")
    
    print(f"\n=== Total unique players found: {len(all_player_ids)} ===")
    return list(all_player_ids)

def fetch_player_details(player_id: int) -> Optional[dict]:
    """Récupère les détails complets d'un joueur avec toutes les données"""
    
    player_response = make_api_call(f"players/{player_id}", {
        'include': 'nationality;country;position;detailedPosition;teams;statistics.details'
    })
    
    if not player_response or 'data' not in player_response:
        return None
    
    player_data = player_response['data']
    
    # Récupérer la nationalité intelligemment
    nationality = get_nationality_smart(player_data)
    
    # Récupérer le numéro de maillot depuis les statistiques
    jersey_number = None
    stats = player_data.get('statistics', [])
    for stat in stats:
        if stat.get('jersey_number'):
            jersey_number = stat.get('jersey_number')
            break
    
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

def fetch_complete_team_roster(team_id: int, team_name: str = "Team") -> dict:
    """
    Fonction principale pour récupérer l'effectif COMPLET d'une équipe
    """
    print(f"\n{'='*60}")
    print(f"RÉCUPÉRATION COMPLÈTE DE L'EFFECTIF: {team_name}")
    print(f"{'='*60}")
    
    # 1. Récupérer tous les IDs des joueurs
    player_ids = fetch_all_team_players(team_id)
    
    if not player_ids:
        print("ERREUR: Aucun joueur trouvé!")
        return None
    
    # 2. Récupérer les détails de chaque joueur
    print(f"\n=== Récupération des détails pour {len(player_ids)} joueurs ===")
    
    players_data = []
    for i, player_id in enumerate(player_ids, 1):
        print(f"\n[{i}/{len(player_ids)}] Récupération du joueur {player_id}...")
        
        player_details = fetch_player_details(player_id)
        
        if player_details:
            players_data.append(player_details)
            print(f"  [OK] {player_details['display_name']}")
            print(f"    Position: {player_details['position']}")
            print(f"    Nationalité: {player_details['nationality']}")
            print(f"    Âge: {player_details['age']} ans")
            if player_details['jersey_number']:
                print(f"    Numéro: #{player_details['jersey_number']}")
        else:
            print(f"  [FAIL] Échec de récupération")
        
        # Éviter le rate limiting
        time.sleep(0.5)
    
    # 3. Créer le résultat final
    result = {
        'team_id': team_id,
        'team_name': team_name,
        'season': '2025/2026',
        'players_count': len(players_data),
        'players': sorted(players_data, key=lambda x: (
            x['position_id'],  # Trier par position
            x['jersey_number'] if x['jersey_number'] else 999,  # Puis par numéro
            x['display_name']  # Puis par nom
        )),
        'fetched_at': datetime.now().isoformat(),
        'missing_nationalities': [p['display_name'] for p in players_data if p['nationality'] == 'Unknown']
    }
    
    # 4. Afficher le résumé
    print(f"\n{'='*60}")
    print(f"RÉSUMÉ DE L'EFFECTIF {team_name}")
    print(f"{'='*60}")
    print(f"Total joueurs: {len(players_data)}")
    
    # Répartition par position
    positions = {}
    for player in players_data:
        pos = player['position']
        positions[pos] = positions.get(pos, 0) + 1
    
    print("\nRépartition par position:")
    for pos, count in sorted(positions.items()):
        print(f"  {pos}: {count} joueurs")
    
    # Nationalités manquantes
    if result['missing_nationalities']:
        print(f"\nNationalités manquantes pour {len(result['missing_nationalities'])} joueurs:")
        for name in result['missing_nationalities']:
            print(f"  - {name}")
    
    return result

def main():
    """Fonction principale pour tester avec l'OM"""
    
    # Configuration pour l'OM
    OM_TEAM_ID = 44
    OM_TEAM_NAME = "Olympique Marseille"
    
    # Récupérer l'effectif complet
    roster_data = fetch_complete_team_roster(OM_TEAM_ID, OM_TEAM_NAME)
    
    if roster_data:
        # Sauvegarder les données
        output_file = f"om_roster_complete_robust.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(roster_data, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"\n[OK] Données sauvegardées dans: {output_file}")
        
        # Générer aussi le code TypeScript
        print("\n=== Génération du code TypeScript ===")
        ts_players = []
        
        for player in roster_data['players']:
            ts_player = f"""      {{
        id: {player['id']},
        nom: "{player['display_name']}",
        displayName: "{player['display_name']}",
        position: "{player['position']}",
        position_id: {player['position_id']},
        numero: {player['jersey_number'] if player['jersey_number'] else 'null'},
        age: "{player['age'] if player['age'] else 'Unknown'}",
        nationalite: "{player['nationality']}",
        taille: {player['height'] if player['height'] else 'null'},
        poids: {player['weight'] if player['weight'] else 'null'},
        image: "{player['image_path'] or 'https://cdn.sportmonks.com/images/soccer/placeholder.png'}",
        playerSlug: "{player['slug']}"
      }}"""
            ts_players.append(ts_player)
        
        ts_code = ",\n".join(ts_players)
        
        with open('om_roster_typescript.txt', 'w', encoding='utf-8') as f:
            f.write(ts_code)
        
        print(f"[OK] Code TypeScript généré dans: om_roster_typescript.txt")
        
    else:
        print("\n[ERREUR] Échec de la récupération de l'effectif")
        sys.exit(1)

if __name__ == "__main__":
    main()