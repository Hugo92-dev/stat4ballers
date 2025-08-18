import requests

API_KEY = "j28l04KZC0LGFAdbxIzdyb8zz253K1YegT5vEUN5taw0dxuNr6U3jtRMmS6C"
base_url = "https://api.sportmonks.com/v3/football"

def search_teams(search_terms):
    """Recherche des équipes par différents termes"""
    for term in search_terms:
        print(f"\nSearching for: {term}")
        print("-" * 40)
        
        try:
            response = requests.get(
                f"{base_url}/teams/search/{term}",
                params={'api_token': API_KEY, 'per_page': 10}
            )
            response.raise_for_status()
            data = response.json()
            
            if 'data' in data:
                for team in data['data']:
                    print(f"ID: {team['id']:4} | Name: {team['name']:30} | Country ID: {team.get('country_id')}")
            else:
                print("No teams found")
                
        except Exception as e:
            print(f"Error: {e}")

# Rechercher les équipes françaises
search_terms = ['marseille', 'monaco', 'lyon', 'paris', 'lille', 'nice', 'lens', 'rennes']
search_teams(search_terms)