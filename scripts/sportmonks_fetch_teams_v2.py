import requests
import json
import time
from typing import Dict, List, Optional

class SportMonksTeamFetcher:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.sportmonks.com/v3/football"
        
        # IDs des équipes françaises principales (confirmés via API)
        self.ligue1_teams = {
            "Paris Saint-Germain": 591,
            "Olympique de Marseille": 44,
            "Olympique Lyonnais": 79,
            "AS Monaco": 6789
        }
        
        # Mapping des positions basé sur l'API SportMonks (vérifié)
        # 24 = Goalkeeper, 25 = Defender, 26 = Midfielder, 27 = Attacker/Forward
        self.position_map = {
            24: "Gardien",
            25: "Défenseur",
            26: "Milieu",
            27: "Attaquant",
            # Anciens IDs au cas où
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
    
    def make_request(self, endpoint: str, params: Optional[Dict] = None) -> Optional[Dict]:
        """Effectue une requête à l'API"""
        if params is None:
            params = {}
        params['api_token'] = self.api_key
        
        try:
            url = f"{self.base_url}{endpoint}"
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error calling {endpoint}: {e}")
            return None
    
    def get_team_squad(self, team_id: int, team_name: str) -> List[Dict]:
        """Récupère l'effectif d'une équipe avec nationalités"""
        print(f"\nFetching squad for {team_name} (ID: {team_id})")
        
        # Obtenir les IDs des joueurs
        squad_data = self.make_request(f"/squads/teams/{team_id}")
        
        if not squad_data or 'data' not in squad_data:
            print(f"  No squad data found")
            return []
        
        players = []
        squad_info = squad_data['data']
        print(f"  Found {len(squad_info)} squad entries")
        
        # Pour chaque entrée de l'effectif, récupérer les infos du joueur avec nationalité
        for i, squad_entry in enumerate(squad_info[:30]):  # Limiter à 30 joueurs
            player_id = squad_entry.get('player_id')
            if not player_id:
                continue
            
            # Récupérer les infos détaillées du joueur avec l'include nationality
            player_data = self.make_request(
                f"/players/{player_id}",
                params={"include": "nationality,country"}
            )
            
            if player_data and 'data' in player_data:
                player = player_data['data']
                
                # Récupérer la nationalité
                nationality_name = "France"  # Défaut
                
                # Essayer d'abord nationality
                if 'nationality' in player and player['nationality']:
                    nationality_name = player['nationality'].get('name', 'France')
                # Sinon essayer country
                elif 'country' in player and player['country']:
                    nationality_name = player['country'].get('name', 'France')
                
                # Traduire les nationalités en français
                nationality_name = self.translate_nationality(nationality_name)
                
                # Créer l'objet joueur avec les infos
                player_info = {
                    'nom': player.get('display_name') or player.get('name', 'Unknown'),
                    'position': self.map_position(squad_entry.get('position_id')),
                    'numero': squad_entry.get('jersey_number'),
                    'age': self.calculate_age(player.get('date_of_birth')),
                    'nationalite': nationality_name,
                    'valeur_marchande': None,  # Non disponible dans l'API de base
                    'minutes': 0,
                    'buts': 0,
                    'passes_decisives': 0,
                    'tirs_par_match': 0,
                    'passes_par_match': 0,
                    'tacles_par_match': 0,
                    'interceptions_par_match': 0
                }
                
                players.append(player_info)
                print(f"    [{i+1}/{len(squad_info)}] {player_info['nom']} - {player_info['position']} - {player_info['nationalite']}")
            
            # Pause pour respecter les limites de l'API
            if (i + 1) % 5 == 0:
                time.sleep(1)
        
        # Trier les joueurs par position
        players.sort(key=lambda x: self.position_order.get(x['position'], 5))
        
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
            from datetime import datetime
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
            'Uruguay': 'Uruguay',
            'Croatia': 'Croatie',
            'Algeria': 'Algérie',
            'Morocco': 'Maroc',
            'Cameroon': 'Cameroun',
            'Senegal': 'Sénégal',
            'Ivory Coast': "Côte d'Ivoire",
            'Ghana': 'Ghana',
            'Japan': 'Japon',
            'South Korea': 'Corée du Sud',
            'Switzerland': 'Suisse',
            'Austria': 'Autriche',
            'Denmark': 'Danemark',
            'Sweden': 'Suède',
            'Norway': 'Norvège',
            'Finland': 'Finlande',
            'Poland': 'Pologne',
            'Czech Republic': 'République Tchèque',
            'Slovakia': 'Slovaquie',
            'Hungary': 'Hongrie',
            'Romania': 'Roumanie',
            'Bulgaria': 'Bulgarie',
            'Greece': 'Grèce',
            'Turkey': 'Turquie',
            'Russia': 'Russie',
            'Ukraine': 'Ukraine',
            'Serbia': 'Serbie',
            'Bosnia and Herzegovina': 'Bosnie',
            'Bosnia & Herzegovina': 'Bosnie',
            'Albania': 'Albanie',
            'North Macedonia': 'Macédoine du Nord',
            'Macedonia': 'Macédoine',
            'Montenegro': 'Monténégro',
            'Slovenia': 'Slovénie',
            'Scotland': 'Écosse',
            'Wales': 'Pays de Galles',
            'Ireland': 'Irlande',
            'Republic of Ireland': 'Irlande',
            'Northern Ireland': 'Irlande du Nord',
            'United States': 'États-Unis',
            'USA': 'États-Unis',
            'Canada': 'Canada',
            'Mexico': 'Mexique',
            'Colombia': 'Colombie',
            'Chile': 'Chili',
            'Peru': 'Pérou',
            'Ecuador': 'Équateur',
            'Venezuela': 'Venezuela',
            'Paraguay': 'Paraguay',
            'Bolivia': 'Bolivie',
            'Georgia': 'Géorgie',
            'Mali': 'Mali',
            'Guinea': 'Guinée',
            'Gabon': 'Gabon',
            'DR Congo': 'RD Congo',
            'Congo DR': 'RD Congo',
            'Burkina Faso': 'Burkina Faso',
            'Tunisia': 'Tunisie',
            'Egypt': 'Égypte',
            'Nigeria': 'Nigeria',
            'South Africa': 'Afrique du Sud',
            'Zambia': 'Zambie',
            'Zimbabwe': 'Zimbabwe',
            'Angola': 'Angola',
            'Mozambique': 'Mozambique',
            'Cape Verde': 'Cap-Vert',
            'Guinea-Bissau': 'Guinée-Bissau',
            'Equatorial Guinea': 'Guinée Équatoriale',
            'Central African Republic': 'République Centrafricaine',
            'Chad': 'Tchad',
            'Niger': 'Niger',
            'Benin': 'Bénin',
            'Togo': 'Togo',
            'Liberia': 'Libéria',
            'Sierra Leone': 'Sierra Leone',
            'Mauritania': 'Mauritanie',
            'Gambia': 'Gambie',
            'Comoros': 'Comores',
            'Madagascar': 'Madagascar',
            'Australia': 'Australie',
            'New Zealand': 'Nouvelle-Zélande',
            'Panama': 'Panama',
            'Costa Rica': 'Costa Rica',
            'Honduras': 'Honduras',
            'El Salvador': 'Salvador',
            'Guatemala': 'Guatemala',
            'Jamaica': 'Jamaïque',
            'Haiti': 'Haïti',
            'Dominican Republic': 'République Dominicaine',
            'Cuba': 'Cuba',
            'Trinidad and Tobago': 'Trinité-et-Tobago',
            'Trinidad & Tobago': 'Trinité-et-Tobago'
        }
        return translations.get(nationality, nationality)
    
    def fetch_ligue1_teams(self):
        """Récupère les données des 4 clubs de Ligue 1"""
        # Créer la structure de données
        ligue1_data = {
            "championnat": "Ligue 1",
            "saison": "2025-2026",
            "clubs": []
        }
        
        # Récupérer les effectifs
        for team_name, team_id in self.ligue1_teams.items():
            if team_id:
                players = self.get_team_squad(team_id, team_name)
                
                club_data = {
                    "nom": team_name,
                    "logo": f"/logos/{team_name.lower().replace(' ', '_')}.png",
                    "stade": self.get_stadium_name(team_name),
                    "joueurs": players
                }
                
                ligue1_data["clubs"].append(club_data)
                time.sleep(2)
        
        return ligue1_data
    
    def get_stadium_name(self, team_name: str) -> str:
        """Retourne le nom du stade"""
        stadiums = {
            "Paris Saint-Germain": "Parc des Princes",
            "Olympique de Marseille": "Orange Vélodrome",
            "Olympique Lyonnais": "Groupama Stadium",
            "AS Monaco": "Stade Louis II"
        }
        return stadiums.get(team_name, "Stade Municipal")

def main():
    API_KEY = "j28l04KZC0LGFAdbxIzdyb8zz253K1YegT5vEUN5taw0dxuNr6U3jtRMmS6C"
    
    fetcher = SportMonksTeamFetcher(API_KEY)
    
    print("=" * 60)
    print("FETCHING LIGUE 1 TEAMS DATA FROM SPORTMONKS V3")
    print("WITH CORRECT NATIONALITIES AND SORTED BY POSITION")
    print("=" * 60)
    
    # Récupérer les données
    ligue1_data = fetcher.fetch_ligue1_teams()
    
    # Sauvegarder les données
    output_file = "../public/data/ligue1_sportmonks_2025_26.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(ligue1_data, f, ensure_ascii=False, indent=2)
    
    print("\n" + "=" * 60)
    print(f"Data saved to {output_file}")
    print(f"Total clubs: {len(ligue1_data['clubs'])}")
    
    for club in ligue1_data['clubs']:
        print(f"  - {club['nom']}: {len(club['joueurs'])} players")
        # Compter par position
        positions_count = {}
        for player in club['joueurs']:
            pos = player['position']
            positions_count[pos] = positions_count.get(pos, 0) + 1
        print(f"    (G:{positions_count.get('Gardien', 0)} D:{positions_count.get('Défenseur', 0)} M:{positions_count.get('Milieu', 0)} A:{positions_count.get('Attaquant', 0)})")
    
    print("=" * 60)

if __name__ == "__main__":
    main()