import requests
import json

def find_leagues():
    """Trouve les IDs des ligues principales"""
    API_KEY = "j28l04KZC0LGFAdbxIzdyb8zz253K1YegT5vEUN5taw0dxuNr6U3jtRMmS6C"
    base_url = "https://api.sportmonks.com/v3/football"
    
    # Récupérer toutes les ligues
    params = {
        'api_token': API_KEY,
        'per_page': 1000  # Pour avoir toutes les ligues
    }
    
    try:
        response = requests.get(f"{base_url}/leagues", params=params)
        response.raise_for_status()
        data = response.json()
        
        # Chercher les 5 grands championnats
        target_leagues = {
            'ligue 1': None,
            'premier league': None,
            'la liga': None,
            'serie a': None,
            'bundesliga': None
        }
        
        if 'data' in data:
            print(f"Total leagues found: {len(data['data'])}")
            print("\nShowing first 20 leagues:")
            print("-" * 50)
            
            for i, league in enumerate(data['data'][:20]):
                print(f"ID: {league.get('id')}, Name: {league.get('name')}")
            
            print("\n" + "=" * 50)
            print("Searching for major leagues...")
            print("-" * 50)
            
            # Afficher toutes les ligues qui pourraient correspondre
            for league in data['data']:
                name = league.get('name', '')
                name_lower = name.lower()
                country_id = league.get('country_id', '')
                
                # Chercher les ligues principales par nom ou pays
                if any(term in name_lower for term in ['ligue 1', 'premier', 'la liga', 'serie a', 'bundesliga', 
                                                        'france', 'england', 'spain', 'italy', 'germany',
                                                        'primera', 'championship']):
                    print(f"ID: {league['id']}, Name: {name}, Country ID: {country_id}")
        
        print("Found leagues:")
        print("=" * 50)
        for key, value in target_leagues.items():
            if value:
                print(f"{key.upper()}: ID={value['id']}, Name={value['name']}, Country={value['country']}")
            else:
                print(f"{key.upper()}: NOT FOUND")
        
        # Sauvegarder les IDs trouvés
        with open('league_ids.json', 'w') as f:
            json.dump(target_leagues, f, indent=2)
        
        return target_leagues
        
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    find_leagues()