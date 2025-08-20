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

# IDs CORRECTS des 18 équipes de Ligue 1 2025/2026
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
    {'id': 59, 'name': 'FC Nantes', 'slug': 'nantes'},
    {'id': 289, 'name': 'Toulouse FC', 'slug': 'toulouse'},
    {'id': 266, 'name': 'Stade Brestois', 'slug': 'brest'},
    {'id': 3682, 'name': 'AJ Auxerre', 'slug': 'auxerre'},
    {'id': 776, 'name': 'Angers SCO', 'slug': 'angers'},
    {'id': 1055, 'name': 'Le Havre AC', 'slug': 'le-havre'},
    {'id': 4508, 'name': 'Paris FC', 'slug': 'paris-fc'},
    {'id': 3513, 'name': 'FC Metz', 'slug': 'metz'},
    {'id': 9257, 'name': 'FC Lorient', 'slug': 'lorient'}
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

# Cache pour les nationalités
nationality_cache = {}

# Traduction des nationalités anglais -> français
NATIONALITY_TRANSLATIONS = {
    'England': 'Angleterre',
    'France': 'France',
    'Germany': 'Allemagne', 
    'Spain': 'Espagne',
    'Italy': 'Italie',
    'Netherlands': 'Pays-Bas',
    'Belgium': 'Belgique',
    'Portugal': 'Portugal',
    'Brazil': 'Brésil',
    'Argentina': 'Argentine',
    'United States': 'États-Unis',
    'Denmark': 'Danemark',
    'Sweden': 'Suède',
    'Norway': 'Norvège',
    'Finland': 'Finlande',
    'Poland': 'Pologne',
    'Switzerland': 'Suisse',
    'Austria': 'Autriche',
    'Czech Republic': 'République tchèque',
    'Slovakia': 'Slovaquie',
    'Hungary': 'Hongrie',
    'Romania': 'Roumanie',
    'Bulgaria': 'Bulgarie',
    'Serbia': 'Serbie',
    'Croatia': 'Croatie',
    'Slovenia': 'Slovénie',
    'Scotland': 'Écosse',
    'Ireland': 'Irlande',
    'Northern Ireland': 'Irlande du Nord',
    'Wales': 'Pays de Galles',
    'Turkey': 'Turquie',
    'Ukraine': 'Ukraine',
    'Russia': 'Russie',
    'Greece': 'Grèce',
    'Albania': 'Albanie',
    'Georgia': 'Géorgie',
    'Bosnia and Herzegovina': 'Bosnie-Herzégovine',
    'North Macedonia': 'Macédoine du Nord',
    'Montenegro': 'Monténégro',
    'Kosovo': 'Kosovo',
    'Iceland': 'Islande',
    'Morocco': 'Maroc',
    'Algeria': 'Algérie',
    'Tunisia': 'Tunisie',
    'Egypt': 'Égypte',
    'Senegal': 'Sénégal',
    'Ivory Coast': "Côte d'Ivoire",
    'Ghana': 'Ghana',
    'Nigeria': 'Nigéria',
    'Cameroon': 'Cameroun',
    'Mali': 'Mali',
    'Burkina Faso': 'Burkina Faso',
    'Guinea': 'Guinée',
    'Gabon': 'Gabon',
    'Congo': 'Congo',
    'DR Congo': 'RD Congo',
    'Congo DR': 'RD Congo',
    'South Africa': 'Afrique du Sud',
    'Japan': 'Japon',
    'South Korea': 'Corée du Sud',
    'Australia': 'Australie',
    'New Zealand': 'Nouvelle-Zélande',
    'Canada': 'Canada',
    'Mexico': 'Mexique',
    'Colombia': 'Colombie',
    'Uruguay': 'Uruguay',
    'Chile': 'Chili',
    'Peru': 'Pérou',
    'Ecuador': 'Équateur',
    'Venezuela': 'Venezuela',
    'Paraguay': 'Paraguay',
    'Bolivia': 'Bolivie',
    'French Guiana': 'Guyane française',
    'Armenia': 'Arménie',
    'Azerbaijan': 'Azerbaïdjan',
    'Israel': 'Israël',
    'Cyprus': 'Chypre',
    'Lebanon': 'Liban',
    'Iran': 'Iran',
    'China': 'Chine',
    'India': 'Inde',
    'Thailand': 'Thaïlande',
    'Indonesia': 'Indonésie',
    'Malaysia': 'Malaisie'
}

def translate_nationality(nationality):
    """Traduire la nationalité en français"""
    return NATIONALITY_TRANSLATIONS.get(nationality, nationality)

def get_nationality_from_api(nat_id):
    """Récupérer la nationalité directement depuis l'API"""
    if nat_id in nationality_cache:
        return nationality_cache[nat_id]
    
    url = f"{BASE_URL}/countries/{nat_id}"
    params = {'api_token': API_KEY}
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        if 'data' in data and data['data']:
            country_name = data['data'].get('name', 'Unknown')
            # Traduire en français
            country_name = translate_nationality(country_name)
            nationality_cache[nat_id] = country_name
            return country_name
    except:
        pass
    
    # Fallback sur le mapping manuel amélioré
    nationality_map = {
        17: 'France', 32: 'Espagne', 6: 'Brésil', 2: 'Argentine',
        27: 'Portugal', 20: 'Italie', 11: 'Allemagne', 24: 'Pays-Bas',
        5: 'Belgique', 14: 'Angleterre', 9: 'Croatie', 22: 'Maroc',
        320: 'Algérie', 148: 'Sénégal', 38: 'Cameroun', 91: "Côte d'Ivoire",
        462: 'Mali', 65: 'Ghana', 127: 'Nigéria', 26: 'Pologne',
        10: 'Danemark', 31: 'Suède', 25: 'Norvège', 16: 'Finlande',
        3: 'Autriche', 33: 'Suisse', 1093: 'République tchèque', 30: 'Slovaquie',
        18: 'Hongrie', 28: 'Roumanie', 7: 'Bulgarie', 29: 'Serbie',
        13: 'Écosse', 19: 'Irlande', 35: 'Turquie', 36: 'Ukraine',
        41: 'Albanie', 37: 'Grèce', 12: 'Géorgie', 8: 'Colombie',
        4: 'Australie', 23: 'Mexique', 34: 'États-Unis', 15: 'Islande',
        21: 'Japon', 45: 'Bosnie-Herzégovine', 117: 'Burkina Faso',
        138: 'Guinée', 133: 'Gabon', 74: 'Congo'
    }
    
    result = nationality_map.get(nat_id, 'Unknown')
    nationality_cache[nat_id] = result
    return result

def get_team_squad_with_details(team_id, team_name):
    """Récupérer l'effectif avec plus de détails"""
    url = f"{BASE_URL}/squads/teams/{team_id}"
    params = {
        'api_token': API_KEY,
        'include': 'player.country'  # Inclure les données du pays
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        if 'data' not in data:
            print(f"  ❌ {team_name}: Pas de données")
            return []
        
        squad = data['data']
        print(f"  ✅ {team_name}: {len(squad)} joueurs trouvés")
        
        players = []
        corrections_made = []
        
        for player_data in squad:
            if 'player' in player_data and player_data['player']:
                player = player_data['player']
                
                # Récupérer le nom correct
                name = player.get('common_name') or player.get('display_name') or 'Unknown'
                full_name = f"{player.get('firstname', '')} {player.get('lastname', '')}".strip()
                
                # Corrections manuelles pour les noms connus incorrects
                if "Bieveth" in name or "Bieveth" in full_name:
                    name = name.replace("Bieveth", "Biereth")
                    full_name = full_name.replace("Bieveth", "Biereth")
                    corrections_made.append(f"Bieveth → Biereth")
                
                # Récupérer la nationalité
                nationality = 'Unknown'
                if 'country' in player and player['country']:
                    nationality = player['country'].get('name', 'Unknown')
                    # Traduire en français
                    nationality = translate_nationality(nationality)
                elif player.get('nationality_id'):
                    nationality = get_nationality_from_api(player['nationality_id'])
                
                # Corrections manuelles pour les nationalités connues incorrectes
                if "Biereth" in name and nationality in ['Algérie', 'Algeria']:
                    nationality = 'Angleterre'
                    corrections_made.append(f"Biereth: nationalité → Angleterre")
                
                # Extraire les infos du joueur
                player_info = {
                    'id': player.get('id'),
                    'name': name,
                    'fullName': full_name,
                    'jersey': player_data.get('jersey_number'),
                    'position': POSITION_MAPPING.get(
                        player_data.get('position_id') or player.get('position_id'), 
                        'Unknown'
                    ),
                    'dateOfBirth': player.get('date_of_birth'),
                    'height': player.get('height'),
                    'weight': player.get('weight'),
                    'nationality': nationality,
                    'image': player.get('image_path')
                }
                
                players.append(player_info)
        
        if corrections_made:
            print(f"     Corrections: {', '.join(corrections_made)}")
        
        # Afficher quelques joueurs clés pour vérification
        key_players = []
        for player in players[:3]:
            jersey = player['jersey'] if player['jersey'] else '?'
            key_players.append(f"#{jersey} {player['name']} ({player['nationality']})")
        
        if key_players:
            print(f"     Exemples: {', '.join(key_players)}")
        
        return players
        
    except requests.exceptions.RequestException as e:
        print(f"  ❌ {team_name}: Erreur API - {e}")
        return []

def generate_typescript_data(teams_data):
    """Générer le fichier TypeScript avec les données"""
    
    ts_content = """// Données des équipes de Ligue 1 - Saison 2025/2026
// Généré automatiquement depuis l'API SportMonks (avec corrections)
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
            
            # Échapper les guillemets dans les noms
            name = player['name'].replace('"', '\\"').replace("'", "\\'")
            fullName = player['fullName'].replace('"', '\\"').replace("'", "\\'")
            nationality = player['nationality'].replace('"', '\\"').replace("'", "\\'")
            
            ts_content += f"""      {{
        id: {player['id']},
        name: "{name}",
        fullName: "{fullName}",
        jersey: {jersey},
        position: "{player['position']}",
        dateOfBirth: "{player['dateOfBirth'] or ''}",
        nationality: "{nationality}",
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
    print("RÉCUPÉRATION COMPLÈTE DES EFFECTIFS LIGUE 1 - 2025/2026")
    print("Avec données détaillées et corrections")
    print("=" * 60)
    print(f"\nRécupération de {len(LIGUE1_TEAMS)} équipes...\n")
    
    all_teams_data = []
    
    for team in LIGUE1_TEAMS:
        players = get_team_squad_with_details(team['id'], team['name'])
        
        if players:
            # Trier par numéro de maillot
            players.sort(key=lambda x: x['jersey'] if x['jersey'] else 999)
            all_teams_data.append((team, players))
        
        time.sleep(0.5)  # Éviter le rate limiting
    
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
        
        # Vérifier quelques joueurs clés
        print(f"\n🔍 Vérifications spécifiques:")
        
        # Vérifier Monaco pour Biereth
        for team, players in all_teams_data:
            if team['slug'] == 'monaco':
                print(f"\nMonaco - Vérification Biereth:")
                for player in players:
                    if 'Biereth' in player['name']:
                        print(f"  ✅ #{player['jersey']} {player['name']} - {player['nationality']}")
                        break
        
        # Vérifier d'autres joueurs connus
        for team, players in all_teams_data:
            if team['slug'] == 'lille':
                for player in players:
                    if 'Giroud' in player['name']:
                        print(f"\nLille - Giroud:")
                        print(f"  ✅ #{player['jersey']} {player['name']} - {player['nationality']}")
                        break
    else:
        print("\n❌ Aucune donnée récupérée")

if __name__ == "__main__":
    main()