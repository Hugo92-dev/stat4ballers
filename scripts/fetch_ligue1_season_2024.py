import requests
import json
import time
import sys
from datetime import datetime

# Forcer l'encodage UTF-8 pour Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'replace')

API_KEY = "j28l04KZC0LGFAdbxIzdyb8zz253K1YegT5vEUN5taw0dxuNr6U3jtRMmS6C"
BASE_URL = "https://api.sportmonks.com/v3/football"
SEASON_ID = 25651  # Saison 2024/2025 confirmée

# IDs CORRECTS des équipes de Ligue 1
LIGUE1_TEAMS = [
    {'id': 591, 'name': 'Paris Saint-Germain', 'slug': 'psg'},
    {'id': 44, 'name': 'Olympique de Marseille', 'slug': 'marseille'},
    {'id': 79, 'name': 'Olympique Lyonnais', 'slug': 'lyon'},
    {'id': 6789, 'name': 'AS Monaco', 'slug': 'monaco'},
    {'id': 690, 'name': 'Lille OSC', 'slug': 'lille'},
    {'id': 450, 'name': 'OGC Nice', 'slug': 'nice'},
    {'id': 598, 'name': 'Stade Rennais', 'slug': 'rennes'},
    {'id': 271, 'name': 'RC Lens', 'slug': 'lens'},
    {'id': 686, 'name': 'RC Strasbourg', 'slug': 'strasbourg'},
    {'id': 1028, 'name': 'Stade de Reims', 'slug': 'reims'},
    {'id': 59, 'name': 'FC Nantes', 'slug': 'nantes'},
    {'id': 581, 'name': 'Montpellier HSC', 'slug': 'montpellier'},
    {'id': 266, 'name': 'Stade Brestois', 'slug': 'brest'},
    {'id': 289, 'name': 'Toulouse FC', 'slug': 'toulouse'},
    {'id': 3682, 'name': 'AJ Auxerre', 'slug': 'auxerre'},
    {'id': 776, 'name': 'Angers SCO', 'slug': 'angers'},
    {'id': 1055, 'name': 'Le Havre AC', 'slug': 'le-havre'},
    {'id': 108, 'name': 'AS Saint-Etienne', 'slug': 'saint-etienne'}
]

# Mapper les positions
POSITION_MAPPING = {
    24: 'GK', 150: 'GK', 151: 'GK',  # Gardiens
    25: 'DF', 148: 'CB', 152: 'CB', 153: 'CB', 154: 'CB',  # Défenseurs centraux
    155: 'LB', 156: 'RB',  # Latéraux
    26: 'MF', 149: 'DM', 157: 'DM', 158: 'CM', 159: 'CM',  # Milieux
    160: 'AM', 161: 'LM', 162: 'RM',  # Milieux offensifs
    27: 'FW', 163: 'LW', 164: 'RW', 165: 'ST', 166: 'CF'  # Attaquants
}

def get_team_squad_by_season(team_id, team_name, season_id):
    """Récupérer l'effectif d'une équipe pour une saison spécifique"""
    url = f"{BASE_URL}/squads/seasons/{season_id}/teams/{team_id}"
    params = {
        'api_token': API_KEY,
        'include': 'player'
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        if 'data' not in data:
            # Essayer l'endpoint alternatif sans saison
            return get_team_squad_fallback(team_id, team_name)
        
        squad = data['data']
        
        if not isinstance(squad, list):
            return get_team_squad_fallback(team_id, team_name)
            
        print(f"  ✅ {team_name}: {len(squad)} joueurs trouvés (saison actuelle)")
        
        players = []
        for player_data in squad:
            if 'player' in player_data and player_data['player']:
                player = player_data['player']
                
                # Extraire les infos du joueur
                player_info = {
                    'id': player.get('id'),
                    'name': player.get('common_name') or player.get('display_name') or 'Unknown',
                    'fullName': f"{player.get('firstname', '')} {player.get('lastname', '')}".strip(),
                    'jersey': player_data.get('jersey_number'),
                    'position': POSITION_MAPPING.get(
                        player_data.get('position_id') or player.get('position_id'), 
                        'Unknown'
                    ),
                    'dateOfBirth': player.get('date_of_birth'),
                    'height': player.get('height'),
                    'weight': player.get('weight'),
                    'nationality': get_nationality(player.get('nationality_id')),
                    'image': player.get('image_path')
                }
                
                players.append(player_info)
        
        return players
        
    except requests.exceptions.RequestException as e:
        print(f"  ⚠️ {team_name}: Erreur API, essai fallback")
        return get_team_squad_fallback(team_id, team_name)

def get_team_squad_fallback(team_id, team_name):
    """Fallback: récupérer l'effectif sans spécifier la saison"""
    url = f"{BASE_URL}/squads/teams/{team_id}"
    params = {
        'api_token': API_KEY,
        'include': 'player'
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        if 'data' not in data:
            print(f"  ❌ {team_name}: Aucune donnée")
            return []
        
        squad = data['data']
        print(f"  ✅ {team_name}: {len(squad)} joueurs trouvés (fallback)")
        
        players = []
        for player_data in squad:
            if 'player' in player_data and player_data['player']:
                player = player_data['player']
                
                player_info = {
                    'id': player.get('id'),
                    'name': player.get('common_name') or player.get('display_name') or 'Unknown',
                    'fullName': f"{player.get('firstname', '')} {player.get('lastname', '')}".strip(),
                    'jersey': player_data.get('jersey_number'),
                    'position': POSITION_MAPPING.get(
                        player_data.get('position_id') or player.get('position_id'), 
                        'Unknown'
                    ),
                    'dateOfBirth': player.get('date_of_birth'),
                    'height': player.get('height'),
                    'weight': player.get('weight'),
                    'nationality': get_nationality(player.get('nationality_id')),
                    'image': player.get('image_path')
                }
                
                players.append(player_info)
        
        return players
        
    except:
        print(f"  ❌ {team_name}: Échec total")
        return []

def get_nationality(nat_id):
    """Mapper les IDs de nationalité"""
    nationality_map = {
        17: 'France', 32: 'Espagne', 6: 'Brésil', 2: 'Argentine',
        27: 'Portugal', 20: 'Italie', 11: 'Allemagne', 24: 'Pays-Bas',
        5: 'Belgique', 14: 'Angleterre', 9: 'Croatie', 22: 'Maroc',
        320: 'Algérie', 148: 'Sénégal', 38: 'Cameroun', 91: "Côte d'Ivoire",
        462: 'Mali', 65: 'Ghana', 127: 'Nigéria', 26: 'Pologne'
    }
    return nationality_map.get(nat_id, 'Unknown')

def generate_typescript_data(teams_data):
    """Générer le fichier TypeScript avec les données"""
    
    ts_content = """// Données des équipes de Ligue 1 - Saison 2024/2025
// Généré automatiquement depuis l'API SportMonks (Season ID: 25651)
// Date: """ + datetime.now().strftime("%Y-%m-%d %H:%M") + """

export interface Player {
  id: number;
  name: string;
  fullName?: string;
  jersey?: number;
  position: string;
  dateOfBirth?: string;
  nationality?: string;
  height?: number;
  weight?: number;
  image?: string;
}

export interface Team {
  id: number;
  name: string;
  slug: string;
  players: Player[];
}

export const ligue1Teams: Team[] = [
"""
    
    for i, (team_info, players) in enumerate(teams_data):
        ts_content += f"""  {{
    id: {team_info['id']},
    name: "{team_info['name']}",
    slug: "{team_info['slug']}",
    players: [
"""
        
        for j, player in enumerate(players):
            jersey = f"{player['jersey']}" if player['jersey'] else "null"
            height = f"{player['height']}" if player['height'] else "null"
            weight = f"{player['weight']}" if player['weight'] else "null"
            
            ts_content += f"""      {{
        id: {player['id']},
        name: "{player['name'].replace('"', '\\"')}",
        fullName: "{player['fullName'].replace('"', '\\"')}",
        jersey: {jersey},
        position: "{player['position']}",
        dateOfBirth: "{player['dateOfBirth'] or ''}",
        nationality: "{player['nationality']}",
        height: {height},
        weight: {weight},
        image: "{player['image'] or ''}"
      }}"""
            if j < len(players) - 1:
                ts_content += ","
            ts_content += "\n"
        
        ts_content += "    ]\n  }"
        if i < len(teams_data) - 1:
            ts_content += ","
        ts_content += "\n"
    
    ts_content += "];\n"
    
    return ts_content

def main():
    print("=" * 60)
    print("RÉCUPÉRATION DES EFFECTIFS LIGUE 1 - SAISON 2024/2025")
    print(f"Utilisation de la Season ID: {SEASON_ID}")
    print("=" * 60)
    print(f"\nRécupération de {len(LIGUE1_TEAMS)} équipes...\n")
    
    all_teams_data = []
    
    for team in LIGUE1_TEAMS:
        players = get_team_squad_by_season(team['id'], team['name'], SEASON_ID)
        
        if players:
            # Trier par numéro de maillot
            players.sort(key=lambda x: x['jersey'] if x['jersey'] else 999)
            all_teams_data.append((team, players))
        
        time.sleep(0.3)  # Éviter le rate limiting
    
    # Générer le fichier TypeScript
    if all_teams_data:
        ts_content = generate_typescript_data(all_teams_data)
        
        # Sauvegarder le fichier
        output_file = "data/ligue1Teams.ts"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(ts_content)
        
        print(f"\n{'='*60}")
        print(f"RÉSUMÉ")
        print(f"{'='*60}")
        print(f"✅ {len(all_teams_data)}/{len(LIGUE1_TEAMS)} équipes récupérées avec succès")
        print(f"📁 Fichier généré: {output_file}")
        
        # Statistiques
        total_players = sum(len(players) for _, players in all_teams_data)
        print(f"👥 Total de joueurs: {total_players}")
        print(f"📊 Moyenne par équipe: {total_players/len(all_teams_data):.1f} joueurs")
        
        # Afficher quelques joueurs clés pour vérification
        print(f"\n🔍 Vérification rapide:")
        for team, players in all_teams_data[:3]:
            print(f"\n{team['name']}:")
            for player in players[:3]:
                if player['jersey']:
                    print(f"  #{player['jersey']} {player['name']}")
    else:
        print("\n❌ Aucune donnée récupérée")

if __name__ == "__main__":
    main()