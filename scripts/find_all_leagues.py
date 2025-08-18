import requests
import json

def find_all_leagues():
    """Trouve toutes les ligues avec pagination"""
    API_KEY = "j28l04KZC0LGFAdbxIzdyb8zz253K1YegT5vEUN5taw0dxuNr6U3jtRMmS6C"
    base_url = "https://api.sportmonks.com/v3/football"
    
    all_leagues = []
    page = 1
    has_more = True
    
    while has_more:
        params = {
            'api_token': API_KEY,
            'page': page,
            'per_page': 100
        }
        
        try:
            print(f"Fetching page {page}...")
            response = requests.get(f"{base_url}/leagues", params=params)
            response.raise_for_status()
            data = response.json()
            
            if 'data' in data and data['data']:
                all_leagues.extend(data['data'])
                
                # Vérifier s'il y a plus de pages
                pagination = data.get('pagination', {})
                if pagination.get('has_more', False):
                    page += 1
                else:
                    has_more = False
            else:
                has_more = False
                
        except Exception as e:
            print(f"Error on page {page}: {e}")
            has_more = False
    
    print(f"\nTotal leagues found: {len(all_leagues)}")
    
    # Chercher les 5 grands championnats
    major_leagues = []
    
    for league in all_leagues:
        name = league.get('name', '')
        name_lower = name.lower()
        
        # Chercher par nom exact ou partiel
        if any(term in name_lower for term in ['ligue 1', 'premier league', 'la liga', 'serie a', 'bundesliga']):
            major_leagues.append({
                'id': league['id'],
                'name': name,
                'country_id': league.get('country_id', ''),
                'active': league.get('active', False)
            })
    
    print("\nMajor European Leagues Found:")
    print("=" * 60)
    for league in major_leagues:
        print(f"ID: {league['id']:4} | Name: {league['name']:30} | Active: {league['active']}")
    
    # Sauvegarder tous les résultats
    with open('all_leagues.json', 'w', encoding='utf-8') as f:
        json.dump(all_leagues, f, ensure_ascii=False, indent=2)
    
    print(f"\nAll leagues saved to all_leagues.json")
    
    return major_leagues

if __name__ == "__main__":
    find_all_leagues()