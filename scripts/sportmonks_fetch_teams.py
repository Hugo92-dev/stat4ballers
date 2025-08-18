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
        # 24 = Goalkeeper
        # 25 = Defender
        # 26 = Midfielder
        # 27 = Attacker/Forward
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
    
    def search_team(self, team_name: str) -> Optional[int]:
        """Recherche une équipe par nom"""
        search_term = team_name.split()[0].lower()  # Premier mot du nom
        data = self.make_request(f"/teams/search/{search_term}")
        
        if data and 'data' in data:
            for team in data['data']:
                if team_name.lower() in team['name'].lower():
                    print(f"Found {team_name}: ID={team['id']}")
                    return team['id']
        
        return None
    
    def get_team_squad(self, team_id: int, team_name: str) -> List[Dict]:
        """Récupère l'effectif d'une équipe"""
        print(f"\nFetching squad for {team_name} (ID: {team_id})")
        
        # Obtenir les IDs des joueurs
        squad_data = self.make_request(f"/squads/teams/{team_id}")
        
        if not squad_data or 'data' not in squad_data:
            print(f"  No squad data found")
            return []
        
        players = []
        squad_info = squad_data['data']
        print(f"  Found {len(squad_info)} squad entries")
        
        # Pour chaque entrée de l'effectif, récupérer les infos du joueur
        for i, squad_entry in enumerate(squad_info[:30]):  # Limiter à 30 joueurs
            player_id = squad_entry.get('player_id')
            if not player_id:
                continue
            
            # Récupérer les infos détaillées du joueur
            player_data = self.make_request(f"/players/{player_id}")
            
            if player_data and 'data' in player_data:
                player = player_data['data']
                
                # Créer l'objet joueur avec les infos
                player_info = {
                    'nom': player.get('display_name') or player.get('name', 'Unknown'),
                    'position': self.map_position(squad_entry.get('position_id')),
                    'numero': squad_entry.get('jersey_number'),
                    'age': self.calculate_age(player.get('date_of_birth')),
                    'nationalite': self.get_nationality(player.get('nationality_id')),
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
                print(f"    [{i+1}/{len(squad_info)}] {player_info['nom']} - {player_info['position']}")
            
            # Pause pour respecter les limites de l'API
            if (i + 1) % 5 == 0:
                time.sleep(1)
        
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
    
    def get_nationality(self, nationality_id: Optional[int]) -> str:
        """Récupère la nationalité"""
        if not nationality_id:
            return "France"
        
        # Cache des nationalités pour éviter trop d'appels API
        if not hasattr(self, 'nationality_cache'):
            self.nationality_cache = {
                17: "France",
                462: "Angleterre",
                161: "Espagne", 
                82: "Allemagne",
                113: "Italie",
                32: "Brésil",
                11: "Argentine",
                139: "Portugal",
                320: "Pays-Bas",
                1161: "Belgique",
                552: "Uruguay",
                91: "Croatie",
                14: "Algérie",
                119: "Maroc",
                15: "Cameroun",
                153: "Sénégal",
                573: "Côte d'Ivoire"
            }
        
        # Si on a déjà la nationalité en cache
        if nationality_id in self.nationality_cache:
            return self.nationality_cache[nationality_id]
        
        # Sinon, faire un appel API pour récupérer la nationalité
        try:
            data = self.make_request(f"/countries/{nationality_id}")
            if data and 'data' in data:
                country_name = data['data'].get('name', 'Unknown')
                # Traduire en français les pays communs
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
                    'Ivory Coast': 'Côte d\'Ivoire',
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
                    'Albania': 'Albanie',
                    'Macedonia': 'Macédoine',
                    'Montenegro': 'Monténégro',
                    'Slovenia': 'Slovénie',
                    'Scotland': 'Écosse',
                    'Wales': 'Pays de Galles',
                    'Ireland': 'Irlande',
                    'Northern Ireland': 'Irlande du Nord',
                    'United States': 'États-Unis',
                    'Canada': 'Canada',
                    'Mexico': 'Mexique',
                    'Colombia': 'Colombie',
                    'Chile': 'Chili',
                    'Peru': 'Pérou',
                    'Ecuador': 'Équateur',
                    'Venezuela': 'Venezuela',
                    'Paraguay': 'Paraguay',
                    'Bolivia': 'Bolivie'
                }
                country_name = translations.get(country_name, country_name)
                self.nationality_cache[nationality_id] = country_name
                return country_name
        except:
            pass
        
        return "France"
    
    def fetch_ligue1_teams(self):
        """Récupère les données des 4 clubs de Ligue 1"""
        # Les IDs sont déjà connus, pas besoin de les chercher
        
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
    print("FETCHING LIGUE 1 TEAMS DATA FROM SPORTMONKS")
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
    
    print("=" * 60)

if __name__ == "__main__":
    main()