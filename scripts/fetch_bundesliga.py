#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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

# IDs des équipes de Bundesliga 2025/2026
BUNDESLIGA_TEAMS = [
    {'id': 503, 'name': 'Bayern Munich', 'slug': 'bayern'},
    {'id': 68, 'name': 'Borussia Dortmund', 'slug': 'borussia-dortmund'},
    {'id': 277, 'name': 'RB Leipzig', 'slug': 'leipzig'},
    {'id': 3321, 'name': 'Bayer Leverkusen', 'slug': 'bayer-leverkusen'},
    {'id': 1079, 'name': 'Union Berlin', 'slug': 'union-berlin'},
    {'id': 3543, 'name': 'SC Freiburg', 'slug': 'freiburg'},
    {'id': 366, 'name': 'Eintracht Frankfurt', 'slug': 'eintracht-frankfurt'},
    {'id': 510, 'name': 'VfL Wolfsburg', 'slug': 'wolfsburg'},
    {'id': 794, 'name': 'Mainz 05', 'slug': 'mainz'},
    {'id': 683, 'name': 'Borussia Mönchengladbach', 'slug': 'borussia-monchengladbach'},
    {'id': 3320, 'name': 'FC Köln', 'slug': 'koln'},
    {'id': 2726, 'name': 'TSG Hoffenheim', 'slug': 'hoffenheim'},
    {'id': 3319, 'name': 'VfB Stuttgart', 'slug': 'stuttgart'},
    {'id': 90, 'name': 'FC Augsburg', 'slug': 'augsburg'},
    {'id': 82, 'name': 'Werder Bremen', 'slug': 'werder'},
    {'id': 2831, 'name': 'Heidenheim', 'slug': 'heidenheim'},
    {'id': 353, 'name': 'St. Pauli', 'slug': 'sankt-pauli'},
    {'id': 2708, 'name': 'Hamburger SV', 'slug': 'hambourg'}
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
    'Jamaica': 'Jamaïque',
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
    'Malaysia': 'Malaisie',
    'Philippines': 'Philippines',
    'Zimbabwe': 'Zimbabwe',
    'Zambia': 'Zambie'
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
    
    return 'Unknown'

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
        
        for player_data in squad:
            if 'player' in player_data and player_data['player']:
                player = player_data['player']
                
                # Récupérer le nom correct
                common_name = player.get('common_name')
                display_name = player.get('display_name')
                firstname = player.get('firstname', '')
                lastname = player.get('lastname', '')
                full_name = f"{firstname} {lastname}".strip()
                
                # Cas spéciaux pour des joueurs connus Bundesliga
                if player.get('id') == 19222:  # Harry Kane
                    name = "H. Kane"
                elif player.get('id') == 1614:  # Neuer
                    name = "M. Neuer"
                elif player.get('id') == 187791:  # Musiala
                    name = "J. Musiala"
                elif player.get('id') == 186863:  # Wirtz
                    name = "F. Wirtz"
                elif player.get('id') == 2827:  # Reus (s'il est encore là)
                    name = "M. Reus"
                elif player.get('id') == 861:  # Müller
                    name = "T. Müller"
                elif player.get('id') == 1622:  # Kimmich
                    name = "J. Kimmich"
                elif common_name:
                    name = common_name
                elif display_name:
                    name = display_name
                else:
                    name = full_name if full_name else 'Unknown'
                
                # Récupérer la nationalité
                nationality = 'Unknown'
                if 'country' in player and player['country']:
                    nationality = player['country'].get('name', 'Unknown')
                    # Traduire en français
                    nationality = translate_nationality(nationality)
                elif player.get('nationality_id'):
                    nationality = get_nationality_from_api(player['nationality_id'])
                
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
    
    ts_content = """// Données des équipes de Bundesliga - Saison 2025/2026
// Généré automatiquement depuis l'API SportMonks
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
  colors: string[];
  players: Player[];
}

export const bundesligaTeams: Team[] = [
"""
    
    # Couleurs des équipes Bundesliga
    team_colors = {
        'bayern': ['#DC052D', '#FFFFFF'],
        'borussia-dortmund': ['#FDE100', '#000000'],
        'leipzig': ['#DD0741', '#FFFFFF'],
        'bayer-leverkusen': ['#E32221', '#000000'],
        'union-berlin': ['#EB1923', '#FFFFFF'],
        'freiburg': ['#EE1C25', '#FFFFFF'],
        'eintracht-frankfurt': ['#E00034', '#000000', '#FFFFFF'],
        'wolfsburg': ['#65B32E', '#FFFFFF'],
        'mainz': ['#C3141E', '#FFFFFF'],
        'borussia-monchengladbach': ['#000000', '#FFFFFF', '#007A33'],
        'koln': ['#ED1C24', '#FFFFFF'],
        'hoffenheim': ['#1961AC', '#FFFFFF'],
        'stuttgart': ['#E32219', '#FFFFFF'],
        'augsburg': ['#BA3733', '#46714D'],
        'werder': ['#1D9053', '#FFFFFF'],
        'heidenheim': ['#003278', '#ED1B23'],
        'sankt-pauli': ['#8B4513', '#FFFFFF'],
        'hambourg': ['#003278', '#FFFFFF', '#ED1B23']
    }
    
    for i, (team_info, players) in enumerate(teams_data):
        colors = team_colors.get(team_info['slug'], ['#000000', '#FFFFFF'])
        colors_str = "[" + ", ".join([f"'{color}'" for color in colors]) + "]"
        
        ts_content += f"""  {{
    id: {team_info['id']},
    name: "{team_info['name']}",
    slug: "{team_info['slug']}",
    colors: {colors_str},
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
    print("RÉCUPÉRATION DES EFFECTIFS BUNDESLIGA - 2025/2026")
    print("=" * 60)
    print(f"\nRécupération de {len(BUNDESLIGA_TEAMS)} équipes...\n")
    
    # Trier les équipes par ordre alphabétique
    BUNDESLIGA_TEAMS.sort(key=lambda x: x['name'])
    
    all_teams_data = []
    
    for team in BUNDESLIGA_TEAMS:
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
        output_file = "data/bundesligaTeams.ts"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(ts_content)
        
        print(f"\n{'='*60}")
        print(f"RÉSUMÉ")
        print(f"{'='*60}")
        print(f"✅ {len(all_teams_data)}/{len(BUNDESLIGA_TEAMS)} équipes récupérées avec succès")
        print(f"📁 Fichier généré: {output_file}")
        
        # Statistiques
        total_players = sum(len(players) for _, players in all_teams_data)
        print(f"👥 Total de joueurs: {total_players}")
        print(f"📊 Moyenne par équipe: {total_players/len(all_teams_data):.1f} joueurs")
        
        # Vérifier quelques stars connues
        print(f"\n🌟 Vérification des stars:")
        
        # Vérifier Bayern
        for team, players in all_teams_data:
            if team['slug'] == 'bayern':
                for player in players:
                    if 'Kane' in player['name']:
                        print(f"  Bayern Munich - {player['name']} ({player['nationality']})")
                        break
        
        # Vérifier Dortmund
        for team, players in all_teams_data:
            if team['slug'] == 'borussia-dortmund':
                for player in players[:5]:
                    if player['position'] == 'FW':
                        print(f"  Borussia Dortmund - {player['name']} ({player['nationality']})")
                        break
                        
        # Vérifier Leverkusen
        for team, players in all_teams_data:
            if team['slug'] == 'bayer-leverkusen':
                for player in players:
                    if 'Wirtz' in player['name']:
                        print(f"  Bayer Leverkusen - {player['name']} ({player['nationality']})")
                        break
    else:
        print("\n❌ Aucune donnée récupérée")

if __name__ == "__main__":
    main()