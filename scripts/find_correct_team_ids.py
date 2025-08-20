import requests
import json
import sys

# Forcer l'encodage UTF-8 pour Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'replace')

API_KEY = "j28l04KZC0LGFAdbxIzdyb8zz253K1YegT5vEUN5taw0dxuNr6U3jtRMmS6C"
BASE_URL = "https://api.sportmonks.com/v3/football"

def search_team(query):
    """Rechercher une équipe par nom"""
    url = f"{BASE_URL}/teams/search/{query}"
    params = {'api_token': API_KEY}
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        if 'data' in data and data['data']:
            print(f"\nRecherche pour '{query}':")
            for team in data['data'][:5]:  # Afficher les 5 premiers résultats
                print(f"  ID: {team['id']} | {team['name']} | Fondé: {team.get('founded', '?')}")
            return data['data']
    except:
        pass
    return []

def get_teams_by_country(country_id):
    """Récupérer toutes les équipes d'un pays"""
    url = f"{BASE_URL}/teams/countries/{country_id}"
    params = {'api_token': API_KEY}
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        if 'data' in data:
            return data['data']
    except:
        pass
    return []

def find_french_ligue1_teams():
    """Trouver les vraies équipes de Ligue 1"""
    print("=" * 60)
    print("RECHERCHE DES VRAIES EQUIPES DE LIGUE 1")
    print("=" * 60)
    
    # ID de la France = 17
    teams = get_teams_by_country(17)
    
    if teams:
        print(f"\nTrouvé {len(teams)} équipes françaises")
        
        # Filtrer les équipes principales (type = domestic)
        ligue1_candidates = []
        for team in teams:
            if team.get('type') == 'domestic':
                # Vérifier si le nom correspond à un club de Ligue 1
                ligue1_names = [
                    'Paris Saint Germain', 'Olympique Marseille', 'Olympique Lyonnais',
                    'Monaco', 'Lille', 'Nice', 'Rennes', 'Lens', 'Strasbourg',
                    'Reims', 'Nantes', 'Montpellier', 'Brest', 'Toulouse',
                    'Auxerre', 'Angers', 'Le Havre', 'Saint-Étienne'
                ]
                
                for l1_name in ligue1_names:
                    if l1_name.lower() in team['name'].lower():
                        ligue1_candidates.append(team)
                        break
        
        print(f"\nClubs Ligue 1 trouvés ({len(ligue1_candidates)}):")
        for team in sorted(ligue1_candidates, key=lambda x: x['name']):
            print(f"  {team['name'].ljust(25)} | ID: {team['id']} | Last played: {team.get('last_played_at', 'N/A')[:10]}")
    
    # Recherche directe pour quelques clubs spécifiques
    print("\n" + "=" * 60)
    print("RECHERCHE DIRECTE DE CLUBS SPECIFIQUES")
    print("=" * 60)
    
    clubs_to_search = [
        'paris saint', 'marseille', 'lyon', 'monaco', 'lille',
        'nice', 'rennes', 'lens', 'strasbourg', 'reims'
    ]
    
    for club in clubs_to_search:
        search_team(club)

if __name__ == "__main__":
    find_french_ligue1_teams()