import requests
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
            for team in data['data'][:10]:  # Afficher les 10 premiers résultats
                country = team.get('country_id', '?')
                if country == 17:  # France
                    print(f"  [FRANCE] ID: {team['id']} | {team['name']} | Type: {team.get('type', '?')} | Last: {team.get('last_played_at', 'N/A')[:10]}")
            return data['data']
    except Exception as e:
        print(f"Erreur: {e}")
    return []

print("=" * 60)
print("RECHERCHE DES CLUBS MANQUANTS")
print("=" * 60)

# Rechercher Le Havre
print("\n1. LE HAVRE:")
search_team("havre")
search_team("le havre")
search_team("HAC")

# Rechercher Auxerre
print("\n2. AUXERRE:")
search_team("auxerre")
search_team("AJ auxerre")
search_team("AJA")