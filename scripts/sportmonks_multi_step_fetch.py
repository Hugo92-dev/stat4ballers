import requests
import json
import os
import time

API_KEY = "j28l04KZC0LGFAdbxIzdyb8zz253K1YegT5vEUN5taw0dxuNr6U3jtRMmS6C"
BASE_URL = "https://api.sportmonks.com/v3/football"

# Configuration des ligues avec IDs d'équipes
LEAGUES = {
    "ligue1": {
        "name": "Ligue 1",
        "teams": [
            {'id': 591, 'name': 'Paris Saint-Germain', 'slug': 'psg'},
            {'id': 44, 'name': 'Olympique de Marseille', 'slug': 'marseille'},
            {'id': 79, 'name': 'Olympique Lyonnais', 'slug': 'lyon'},
            {'id': 6789, 'name': 'AS Monaco', 'slug': 'monaco'},
            {'id': 65, 'name': 'Lille OSC', 'slug': 'lille'},
            {'id': 85, 'name': 'OGC Nice', 'slug': 'nice'},
            {'id': 1163, 'name': 'Stade Rennais', 'slug': 'rennes'},
            {'id': 66, 'name': 'RC Lens', 'slug': 'lens'},
            {'id': 2348, 'name': 'RC Strasbourg', 'slug': 'strasbourg'},
            {'id': 538, 'name': 'Stade de Reims', 'slug': 'reims'},
            {'id': 82, 'name': 'FC Nantes', 'slug': 'nantes'},
            {'id': 71, 'name': 'Montpellier HSC', 'slug': 'montpellier'},
            {'id': 584, 'name': 'Stade Brestois', 'slug': 'brest'},
            {'id': 583, 'name': 'Toulouse FC', 'slug': 'toulouse'},
            {'id': 1272, 'name': 'AJ Auxerre', 'slug': 'auxerre'},
            {'id': 580, 'name': 'Angers SCO', 'slug': 'angers'},
            {'id': 1246, 'name': 'Le Havre AC', 'slug': 'le-havre'},
            {'id': 1714, 'name': 'AS Saint-Etienne', 'slug': 'saint-etienne'}
        ]
    }
}

# Traduction des nationalités vers le français
NATIONALITY_TRANSLATIONS = {
    'France': 'France', 'Spain': 'Espagne', 'Brazil': 'Brésil', 'Argentina': 'Argentine',
    'Portugal': 'Portugal', 'Italy': 'Italie', 'Germany': 'Allemagne', 'Netherlands': 'Pays-Bas',
    'Belgium': 'Belgique', 'England': 'Angleterre', 'Croatia': 'Croatie', 'Morocco': 'Maroc',
    'Algeria': 'Algérie', 'Senegal': 'Sénégal', 'Cameroon': 'Cameroun', 'Ivory Coast': 'Côte d\'Ivoire',
    'Mali': 'Mali', 'Ghana': 'Ghana', 'Nigeria': 'Nigéria', 'Poland': 'Pologne', 'Denmark': 'Danemark',
    'Sweden': 'Suède', 'Norway': 'Norvège', 'Finland': 'Finlande', 'Austria': 'Autriche',
    'Switzerland': 'Suisse', 'Czech Republic': 'République tchèque', 'Slovakia': 'Slovaquie',
    'Hungary': 'Hongrie', 'Romania': 'Roumanie', 'Bulgaria': 'Bulgarie', 'Serbia': 'Serbie',
    'Montenegro': 'Monténégro', 'Bosnia and Herzegovina': 'Bosnie-Herzégovine', 'Slovenia': 'Slovénie',
    'Macedonia': 'Macédoine', 'Albania': 'Albanie', 'Greece': 'Grèce', 'Turkey': 'Turquie',
    'Russia': 'Russie', 'Ukraine': 'Ukraine', 'Belarus': 'Biélorussie', 'Lithuania': 'Lituanie',
    'Latvia': 'Lettonie', 'Estonia': 'Estonie', 'Japan': 'Japon', 'South Korea': 'Corée du Sud',
    'Australia': 'Australie', 'New Zealand': 'Nouvelle-Zélande', 'United States': 'États-Unis',
    'Canada': 'Canada', 'Mexico': 'Mexique', 'Colombia': 'Colombie', 'Chile': 'Chili',
    'Peru': 'Pérou', 'Uruguay': 'Uruguay', 'Ecuador': 'Équateur', 'Venezuela': 'Venezuela',
    'Paraguay': 'Paraguay', 'Bolivia': 'Bolivie', 'Costa Rica': 'Costa Rica', 'Panama': 'Panama',
    'Honduras': 'Honduras', 'Guatemala': 'Guatemala', 'El Salvador': 'Salvador', 'Nicaragua': 'Nicaragua',
    'Jamaica': 'Jamaïque', 'Trinidad and Tobago': 'Trinité-et-Tobago', 'Egypt': 'Égypte',
    'Tunisia': 'Tunisie', 'South Africa': 'Afrique du Sud', 'Kenya': 'Kenya', 'Ethiopia': 'Éthiopie',
    'Angola': 'Angola', 'Mozambique': 'Mozambique', 'Cape Verde': 'Cap-Vert', 'Guinea': 'Guinée',
    'Burkina Faso': 'Burkina Faso', 'Benin': 'Bénin', 'Togo': 'Togo', 'Gabon': 'Gabon',
    'Congo': 'Congo', 'Democratic Republic of the Congo': 'République démocratique du Congo',
    'Central African Republic': 'République centrafricaine', 'Chad': 'Tchad', 'Niger': 'Niger',
    'Madagascar': 'Madagascar', 'Mauritania': 'Mauritanie', 'Mauritius': 'Maurice',
    'Comoros': 'Comores', 'Seychelles': 'Seychelles', 'Réunion': 'Réunion', 'Martinique': 'Martinique',
    'Guadeloupe': 'Guadeloupe', 'French Guiana': 'Guyane française', 'New Caledonia': 'Nouvelle-Calédonie',
    'Tahiti': 'Tahiti', 'Scotland': 'Écosse', 'Wales': 'Pays de Galles', 'Northern Ireland': 'Irlande du Nord',
    'Republic of Ireland': 'République d\'Irlande', 'Iceland': 'Islande'
}

def make_request(endpoint, params=None):
    """Effectue une requête à l'API SportMonks avec gestion d'erreur"""
    if params is None:
        params = {}
    
    params['api_token'] = API_KEY
    
    try:
        response = requests.get(f"{BASE_URL}/{endpoint}", params=params)
        response.raise_for_status()
        
        data = response.json()
        if 'data' not in data:
            print(f"Warning: No data in response for {endpoint}")
            return []
        
        return data['data']
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {endpoint}: {e}")
        return []

def get_team_squad(team_id):
    """Récupérer l'effectif d'une équipe avec les informations des joueurs"""
    endpoint = f"squads/teams/{team_id}"
    params = {'include': 'player.nationality'}
    
    squad_data = make_request(endpoint, params)
    return squad_data

def get_player_statistics(player_id, season_id):
    """Étape 3: Récupérer les statistiques détaillées d'un joueur"""
    endpoint = f"players/{player_id}"
    params = {
        'include': 'statistics.details,position,nationality',
        'filters': f'playerStatisticSeasons:{season_id}'
    }
    
    player_data = make_request(endpoint, params)
    return player_data

def process_league_data(league_key, league_config):
    """Traite toutes les données d'une ligue selon l'approche multi-étapes"""
    print(f"\n=== Processing {league_config['name']} ===")
    
    teams = league_config['teams']
    league_data = {}
    
    for team in teams:
        team_id = team['id']
        team_name = team['name']
        team_slug = team['slug']
        print(f"\nProcessing {team_name}...")
        
        # Récupérer l'effectif de l'équipe
        squad = get_team_squad(team_id)
        
        if not squad:
            print(f"  No squad data for {team_name}")
            continue
        
        players_data = []
        
        # Traiter chaque joueur de l'effectif
        for squad_member in squad:
            if 'player' not in squad_member:
                continue
                
            player = squad_member['player']
            player_id = player['id']
            
            # Mapper la position
            position_mapping = {24: 'Gardien', 25: 'Défenseur', 26: 'Milieu', 27: 'Attaquant'}
            position = position_mapping.get(player.get('position_id'), 'Inconnu')
            
            # Récupérer et traduire la nationalité
            nationality = 'Inconnue'
            if 'nationality' in player and player['nationality']:
                nationality_name = player['nationality'].get('name', 'Inconnue')
                nationality = NATIONALITY_TRANSLATIONS.get(nationality_name, nationality_name)
            
            # Construire les données du joueur
            player_data = {
                'id': player_id,
                'nom': player.get('display_name', player.get('common_name', '')),
                'position': position,
                'position_id': player.get('position_id'),
                'age': player.get('date_of_birth'),
                'nationalite': nationality,
                'numero': squad_member.get('jersey_number'),
                'taille': player.get('height'),
                'poids': player.get('weight')
            }
            
            players_data.append(player_data)
            
        # Trier les joueurs par position (Gardiens -> Défenseurs -> Milieux -> Attaquants)
        position_order = {'Gardien': 1, 'Défenseur': 2, 'Milieu': 3, 'Attaquant': 4, 'Inconnu': 5}
        players_data.sort(key=lambda x: (position_order.get(x['position'], 5), x['nom']))
        
        league_data[team_slug] = {
            'club_id': team_id,
            'club_name': team_name,
            'players': players_data
        }
        
        print(f"  OK {len(players_data)} players processed for {team_name}")
        
        # Pause pour éviter de surcharger l'API
        time.sleep(0.5)
    
    # Sauvegarder les données de la ligue
    output_file = f"../data/{league_key}Data.ts"
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    ts_content = f"""// Données {league_config['name']} générées automatiquement
export const {league_key.replace('-', '')}Data = {json.dumps(league_data, ensure_ascii=False, indent=2)};
"""
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(ts_content)
    
    print(f"\nOK {league_config['name']} data saved to {output_file}")
    print(f"OK Total clubs processed: {len(league_data)}")

def main():
    """Point d'entrée principal - traite toutes les ligues"""
    print("=== SportMonks Multi-Step Data Fetcher ===")
    print("This script will fetch data using the proper SportMonks API structure:")
    print("1. Leagues -> Teams")
    print("2. Teams -> Squads") 
    print("3. Players -> Statistics (future enhancement)")
    print()
    
    # Traiter chaque ligue
    for league_key, league_config in LEAGUES.items():
        try:
            process_league_data(league_key, league_config)
            print(f"\n{'='*50}")
        except Exception as e:
            print(f"Error processing {league_config['name']}: {e}")
            continue
    
    print("\nAll leagues processed successfully!")
    print("\nNext steps:")
    print("1. Update your components to use the new data files")
    print("2. Test each league's club pages")
    print("3. Verify player data accuracy")

if __name__ == "__main__":
    main()