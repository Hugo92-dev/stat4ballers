import requests
import json
import time
from typing import Dict, List, Optional
from datetime import datetime

class SportMonksFullFetcher:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.sportmonks.com/v3/football"
        
        # Mapping des positions
        self.position_map = {
            24: "Gardien",
            25: "Défenseur", 
            26: "Milieu",
            27: "Attaquant",
            1: "Gardien",
            2: "Défenseur",
            3: "Défenseur",
            4: "Défenseur",
            5: "Défenseur",
            6: "Milieu",
            7: "Milieu",
            8: "Milieu",
            9: "Milieu",
            10: "Milieu",
            11: "Attaquant",
            12: "Attaquant",
            13: "Attaquant",
            14: "Attaquant",
            28: "Milieu"
        }
        
        # Ordre des positions pour le tri
        self.position_order = {
            "Gardien": 1,
            "Défenseur": 2,
            "Milieu": 3,
            "Attaquant": 4
        }
        
        # IDs de toutes les équipes de Ligue 1
        self.ligue1_teams = [
            {'id': 591, 'name': 'Paris Saint-Germain'},
            {'id': 44, 'name': 'Olympique de Marseille'},
            {'id': 79, 'name': 'Olympique Lyonnais'},
            {'id': 6789, 'name': 'AS Monaco'},
            {'id': 65, 'name': 'Lille OSC'},
            {'id': 85, 'name': 'OGC Nice'},
            {'id': 77, 'name': 'RC Lens'},
            {'id': 69, 'name': 'Stade Rennais'},
            {'id': 1020, 'name': 'Stade de Reims'},
            {'id': 74, 'name': 'Toulouse FC'},
            {'id': 88, 'name': 'FC Nantes'},
            {'id': 57, 'name': 'Montpellier HSC'},
            {'id': 106, 'name': 'RC Strasbourg'},
            {'id': 66, 'name': 'Stade Brestois'},
            {'id': 334, 'name': 'AJ Auxerre'},
            {'id': 75, 'name': 'Le Havre AC'},
            {'id': 674, 'name': 'Angers SCO'},
            {'id': 58, 'name': 'AS Saint-Étienne'}
        ]
    
    def make_request(self, endpoint: str, params: Optional[Dict] = None) -> Optional[Dict]:
        """Effectue une requête à l'API"""
        if params is None:
            params = {}
        params['api_token'] = self.api_key
        
        try:
            url = f"{self.base_url}{endpoint}"
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"  Error calling {endpoint}: {e}")
            return None
    
    def get_team_squad(self, team_id: int, team_name: str) -> List[Dict]:
        """Récupère l'effectif d'une équipe avec nationalités via includes"""
        print(f"  Fetching squad for {team_name} (ID: {team_id})")
        
        # Obtenir l'effectif avec les données des joueurs et nationalités
        squad_data = self.make_request(
            f"/squads/teams/{team_id}",
            params={"include": "player.nationality"}
        )
        
        if not squad_data or 'data' not in squad_data:
            print(f"    No squad data found")
            return []
        
        players = []
        squad_info = squad_data['data']
        
        # Pour chaque entrée de l'effectif
        for squad_entry in squad_info[:30]:  # Limiter à 30 joueurs
            if 'player' not in squad_entry:
                continue
            
            player = squad_entry['player']
            
            # Récupérer la nationalité
            nationality_name = "Unknown"
            
            if 'nationality' in player and player['nationality']:
                nationality_name = player['nationality'].get('name', 'Unknown')
            
            # Traduire les nationalités en français
            nationality_name = self.translate_nationality(nationality_name)
            
            # Créer l'objet joueur avec les infos
            player_info = {
                'nom': player.get('display_name') or player.get('name', 'Unknown'),
                'position': self.map_position(squad_entry.get('position_id')),
                'numero': squad_entry.get('jersey_number'),
                'age': self.calculate_age(player.get('date_of_birth')),
                'nationalite': nationality_name,
                'valeur_marchande': None,
                'minutes': 0,
                'buts': 0,
                'passes_decisives': 0,
                'tirs_par_match': 0,
                'passes_par_match': 0,
                'tacles_par_match': 0,
                'interceptions_par_match': 0
            }
            
            players.append(player_info)
        
        # Trier les joueurs par position
        players.sort(key=lambda x: self.position_order.get(x['position'], 5))
        
        print(f"    Found {len(players)} players")
        return players
    
    def map_position(self, position_id: Optional[int]) -> str:
        """Convertit l'ID de position en nom"""
        if not position_id:
            return "Milieu"
        return self.position_map.get(position_id, "Milieu")
    
    def calculate_age(self, date_of_birth: Optional[str]) -> int:
        """Calcule l'âge"""
        if not date_of_birth:
            return 25
        
        try:
            birth_date = datetime.strptime(date_of_birth, "%Y-%m-%d")
            today = datetime.now()
            age = today.year - birth_date.year
            if today.month < birth_date.month or (today.month == birth_date.month and today.day < birth_date.day):
                age -= 1
            return age
        except:
            return 25
    
    def translate_nationality(self, nationality: str) -> str:
        """Traduit les nationalités en français"""
        translations = {
            'France': 'France',
            'England': 'Angleterre',
            'Spain': 'Espagne',
            'Germany': 'Allemagne',
            'Italy': 'Italie',
            'Brazil': 'Brésil',
            'Argentina': 'Argentine',
            'Portugal': 'Portugal',
            'Netherlands': 'Pays-Bas',
            'Belgium': 'Belgique',
            'Croatia': 'Croatie',
            'Uruguay': 'Uruguay',
            'Switzerland': 'Suisse',
            'Poland': 'Pologne',
            'Denmark': 'Danemark',
            'Sweden': 'Suède',
            'Norway': 'Norvège',
            'Serbia': 'Serbie',
            'Austria': 'Autriche',
            'Czech Republic': 'République Tchèque',
            'Scotland': 'Écosse',
            'Wales': 'Pays de Galles',
            'Ireland': 'Irlande',
            'United States': 'États-Unis',
            'Canada': 'Canada',
            'Mexico': 'Mexique',
            'Colombia': 'Colombie',
            'Chile': 'Chili',
            'Ecuador': 'Équateur',
            'Peru': 'Pérou',
            'Japan': 'Japon',
            'South Korea': 'Corée du Sud',
            'Australia': 'Australie',
            'Algeria': 'Algérie',
            'Morocco': 'Maroc',
            'Tunisia': 'Tunisie',
            'Egypt': 'Égypte',
            'Senegal': 'Sénégal',
            'Nigeria': 'Nigeria',
            'Ghana': 'Ghana',
            'Cameroon': 'Cameroun',
            'Ivory Coast': "Côte d'Ivoire",
            'Mali': 'Mali',
            'Georgia': 'Géorgie',
            'Ukraine': 'Ukraine',
            'Russia': 'Russie',
            'Turkey': 'Turquie',
            'Greece': 'Grèce',
            'Finland': 'Finlande',
            'Romania': 'Roumanie',
            'Hungary': 'Hongrie',
            'Slovakia': 'Slovaquie',
            'Slovenia': 'Slovénie',
            'Bulgaria': 'Bulgarie',
            'Albania': 'Albanie',
            'North Macedonia': 'Macédoine du Nord',
            'Bosnia and Herzegovina': 'Bosnie',
            'Montenegro': 'Monténégro',
            'Kosovo': 'Kosovo',
            'Iceland': 'Islande',
            'Luxembourg': 'Luxembourg',
            'Armenia': 'Arménie',
            'Georgia': 'Géorgie',
            'Azerbaijan': 'Azerbaïdjan',
            'Kazakhstan': 'Kazakhstan',
            'Israel': 'Israël',
            'South Africa': 'Afrique du Sud',
            'Zimbabwe': 'Zimbabwe',
            'Zambia': 'Zambie',
            'Angola': 'Angola',
            'Mozambique': 'Mozambique',
            'DR Congo': 'RD Congo',
            'Congo': 'Congo',
            'Gabon': 'Gabon',
            'Guinea': 'Guinée',
            'Burkina Faso': 'Burkina Faso',
            'Central African Republic': 'République Centrafricaine',
            'Togo': 'Togo',
            'Benin': 'Bénin',
            'Niger': 'Niger',
            'Chad': 'Tchad',
            'Cape Verde': 'Cap-Vert',
            'Guinea-Bissau': 'Guinée-Bissau',
            'Equatorial Guinea': 'Guinée Équatoriale',
            'Liberia': 'Libéria',
            'Sierra Leone': 'Sierra Leone',
            'Mauritania': 'Mauritanie',
            'Gambia': 'Gambie',
            'Comoros': 'Comores',
            'Madagascar': 'Madagascar',
            'Jamaica': 'Jamaïque',
            'Haiti': 'Haïti',
            'Dominican Republic': 'République Dominicaine',
            'Cuba': 'Cuba',
            'Trinidad and Tobago': 'Trinité-et-Tobago',
            'Costa Rica': 'Costa Rica',
            'Honduras': 'Honduras',
            'El Salvador': 'Salvador',
            'Guatemala': 'Guatemala',
            'Panama': 'Panama',
            'Venezuela': 'Venezuela',
            'Paraguay': 'Paraguay',
            'Bolivia': 'Bolivie',
            'New Zealand': 'Nouvelle-Zélande'
        }
        return translations.get(nationality, nationality)
    
    def fetch_ligue1_data(self):
        """Récupère les données de tous les clubs de Ligue 1"""
        print(f"\n{'='*60}")
        print(f"FETCHING LIGUE 1 COMPLETE DATA")
        print(f"{'='*60}")
        
        league_data = {
            "championnat": "Ligue 1",
            "saison": "2025-2026",
            "clubs": []
        }
        
        for i, team_info in enumerate(self.ligue1_teams, 1):
            print(f"\n[{i}/{len(self.ligue1_teams)}]", end=" ")
            players = self.get_team_squad(team_info['id'], team_info['name'])
            
            club_data = {
                "nom": team_info['name'],
                "logo": f"/logos/{team_info['name'].lower().replace(' ', '_')}.png",
                "stade": "",
                "joueurs": players
            }
            
            league_data["clubs"].append(club_data)
            
            # Pause pour respecter les limites API
            time.sleep(2)
        
        return league_data

def main():
    API_KEY = "j28l04KZC0LGFAdbxIzdyb8zz253K1YegT5vEUN5taw0dxuNr6U3jtRMmS6C"
    
    fetcher = SportMonksFullFetcher(API_KEY)
    
    print("=" * 60)
    print("RE-FETCHING ALL LIGUE 1 DATA")
    print("=" * 60)
    
    # Récupérer toutes les données
    ligue1_data = fetcher.fetch_ligue1_data()
    
    # Sauvegarder les données
    output_file = "../public/data/ligue1_sportmonks_2025_26.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(ligue1_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n[OK] Data saved to {output_file}")
    print(f"Total clubs: {len(ligue1_data['clubs'])}")
    
    # Résumé
    total_players = sum(len(club['joueurs']) for club in ligue1_data['clubs'])
    print(f"Total players: {total_players}")
    
    for club in ligue1_data['clubs']:
        print(f"  - {club['nom']}: {len(club['joueurs'])} players")

if __name__ == "__main__":
    main()