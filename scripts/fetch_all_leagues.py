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
        
        # Teams IDs pour tous les championnats (à compléter)
        self.all_teams = {
            'ligue1': {
                'league_name': 'Ligue 1',
                'teams': [
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
            },
            'premier-league': {
                'league_name': 'Premier League',
                'teams': [
                    {'id': 9, 'name': 'Arsenal'},
                    {'id': 10, 'name': 'Aston Villa'},
                    {'id': 1, 'name': 'Chelsea'},
                    {'id': 7, 'name': 'Everton'},
                    {'id': 8, 'name': 'Liverpool'},
                    {'id': 14, 'name': 'Manchester City'},
                    {'id': 19, 'name': 'Manchester United'},
                    {'id': 13, 'name': 'Newcastle United'},
                    {'id': 18, 'name': 'Tottenham Hotspur'},
                    {'id': 746, 'name': 'West Ham United'},
                    {'id': 36, 'name': 'Wolverhampton Wanderers'},
                    {'id': 35, 'name': 'Brentford'},
                    {'id': 43, 'name': 'Brighton & Hove Albion'},
                    {'id': 45, 'name': 'Crystal Palace'},
                    {'id': 40, 'name': 'Fulham'},
                    {'id': 130, 'name': 'Leicester City'},
                    {'id': 52, 'name': 'Nottingham Forest'},
                    {'id': 34, 'name': 'AFC Bournemouth'},
                    {'id': 83, 'name': 'Southampton'},
                    {'id': 134, 'name': 'Ipswich Town'}
                ]
            },
            'laliga': {
                'league_name': 'La Liga',
                'teams': [
                    {'id': 3468, 'name': 'Real Madrid'},
                    {'id': 529, 'name': 'FC Barcelona'},
                    {'id': 554, 'name': 'Atlético Madrid'},
                    {'id': 548, 'name': 'Sevilla FC'},
                    {'id': 714, 'name': 'Real Betis'},
                    {'id': 715, 'name': 'Real Sociedad'},
                    {'id': 546, 'name': 'Valencia CF'},
                    {'id': 555, 'name': 'Villarreal CF'},
                    {'id': 751, 'name': 'Athletic Bilbao'},
                    {'id': 724, 'name': 'CA Osasuna'},
                    {'id': 542, 'name': 'RC Celta de Vigo'},
                    {'id': 720, 'name': 'Rayo Vallecano'},
                    {'id': 712, 'name': 'RCD Mallorca'},
                    {'id': 725, 'name': 'Getafe CF'},
                    {'id': 2930, 'name': 'Girona FC'},
                    {'id': 721, 'name': 'Deportivo Alavés'},
                    {'id': 576, 'name': 'UD Las Palmas'},
                    {'id': 728, 'name': 'CD Leganés'},
                    {'id': 541, 'name': 'Real Valladolid'},
                    {'id': 2905, 'name': 'RCD Espanyol'}
                ]
            },
            'serie-a': {
                'league_name': 'Serie A',
                'teams': [
                    {'id': 496, 'name': 'Juventus'},
                    {'id': 489, 'name': 'AC Milan'},
                    {'id': 505, 'name': 'Inter Milan'},
                    {'id': 503, 'name': 'AS Roma'},
                    {'id': 511, 'name': 'SSC Napoli'},
                    {'id': 502, 'name': 'Lazio'},
                    {'id': 499, 'name': 'Atalanta'},
                    {'id': 500, 'name': 'ACF Fiorentina'},
                    {'id': 492, 'name': 'Torino FC'},
                    {'id': 487, 'name': 'Bologna FC'},
                    {'id': 5890, 'name': 'Hellas Verona'},
                    {'id': 506, 'name': 'Udinese Calcio'},
                    {'id': 867, 'name': 'Genoa CFC'},
                    {'id': 522, 'name': 'US Lecce'},
                    {'id': 497, 'name': 'Cagliari Calcio'},
                    {'id': 648, 'name': 'Parma Calcio 1913'},
                    {'id': 1390, 'name': 'AS Venezia'},
                    {'id': 6361, 'name': 'Como 1907'},
                    {'id': 508, 'name': 'Empoli FC'},
                    {'id': 6577, 'name': 'AC Monza'}
                ]
            },
            'bundesliga': {
                'league_name': 'Bundesliga',
                'teams': [
                    {'id': 157, 'name': 'Bayern Munich'},
                    {'id': 160, 'name': 'Borussia Dortmund'},
                    {'id': 174, 'name': 'RB Leipzig'},
                    {'id': 172, 'name': 'Bayer 04 Leverkusen'},
                    {'id': 164, 'name': 'Eintracht Frankfurt'},
                    {'id': 169, 'name': 'VfL Wolfsburg'},
                    {'id': 163, 'name': 'Borussia Mönchengladbach'},
                    {'id': 180, 'name': 'SC Freiburg'},
                    {'id': 2394, 'name': 'VfB Stuttgart'},
                    {'id': 173, 'name': '1. FC Union Berlin'},
                    {'id': 165, 'name': 'TSG 1899 Hoffenheim'},
                    {'id': 165, 'name': 'FC Augsburg'},
                    {'id': 162, 'name': 'Werder Bremen'},
                    {'id': 191, 'name': '1. FSV Mainz 05'},
                    {'id': 167, 'name': 'VfL Bochum'},
                    {'id': 184, 'name': 'FC Heidenheim'},
                    {'id': 668, 'name': 'FC St. Pauli'},
                    {'id': 2446, 'name': 'Holstein Kiel'}
                ]
            }
        }
    
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
        """Traduit les nationalités en français (version simplifiée)"""
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
    
    def fetch_league_data(self, league_key: str, league_info: Dict) -> Dict:
        """Récupère les données d'un championnat"""
        print(f"\n{'='*60}")
        print(f"FETCHING {league_info['league_name'].upper()}")
        print(f"{'='*60}")
        
        league_data = {
            "championnat": league_info['league_name'],
            "saison": "2025-2026",
            "clubs": []
        }
        
        for i, team_info in enumerate(league_info['teams'], 1):
            print(f"\n[{i}/{len(league_info['teams'])}]", end=" ")
            players = self.get_team_squad(team_info['id'], team_info['name'])
            
            if players:
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
    
    def fetch_all_leagues(self):
        """Récupère les données de tous les championnats"""
        
        for league_key, league_info in self.all_teams.items():
            league_data = self.fetch_league_data(league_key, league_info)
            
            # Sauvegarder les données
            filename = f"../public/data/{league_key}_sportmonks_2025_26.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(league_data, f, ensure_ascii=False, indent=2)
            
            print(f"\n[OK] Data saved to {filename}")
            print(f"  Total clubs: {len(league_data['clubs'])}")
            
            # Résumé
            total_players = sum(len(club['joueurs']) for club in league_data['clubs'])
            print(f"  Total players: {total_players}")

def main():
    API_KEY = "j28l04KZC0LGFAdbxIzdyb8zz253K1YegT5vEUN5taw0dxuNr6U3jtRMmS6C"
    
    fetcher = SportMonksFullFetcher(API_KEY)
    
    print("=" * 60)
    print("FETCHING ALL LEAGUES DATA FROM SPORTMONKS")
    print("WITH CORRECT NATIONALITIES AND SORTED BY POSITION")
    print("=" * 60)
    
    # Récupérer toutes les données
    fetcher.fetch_all_leagues()
    
    print("\n" + "=" * 60)
    print("ALL DATA FETCHED SUCCESSFULLY!")
    print("=" * 60)

if __name__ == "__main__":
    main()