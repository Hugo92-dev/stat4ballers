import requests
import json
import sys

# Forcer l'encodage UTF-8 pour Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'replace')

API_KEY = "j28l04KZC0LGFAdbxIzdyb8zz253K1YegT5vEUN5taw0dxuNr6U3jtRMmS6C"
BASE_URL = "https://api.sportmonks.com/v3/football"

print("=" * 60)
print("VERIFICATION DES VRAIS JOUEURS SAISON 2025/2026")
print("=" * 60)

# Joueurs à vérifier selon l'utilisateur
players_to_verify = {
    'Lille': ['Giroud'],
    'Nantes': ['Lahdo', 'Mayckel'],
    'Brest': ['Majecki', 'Radosław']
}

clubs = [
    {'id': 690, 'name': 'Lille'},
    {'id': 59, 'name': 'Nantes'},
    {'id': 266, 'name': 'Brest'}
]

def check_squad(team_id, team_name, search_players):
    """Vérifier l'effectif d'une équipe et chercher des joueurs spécifiques"""
    print(f"\n{'='*40}")
    print(f"{team_name} (ID: {team_id})")
    print(f"{'='*40}")
    print(f"Recherche de: {', '.join(search_players)}")
    
    # Essayer l'endpoint simple d'abord
    print("\n1. Endpoint simple /squads/teams/{id}:")
    url = f"{BASE_URL}/squads/teams/{team_id}"
    params = {
        'api_token': API_KEY,
        'include': 'player'
    }
    
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            if 'data' in data:
                squad = data['data']
                print(f"   Total: {len(squad)} joueurs")
                
                found_players = []
                all_names = []
                
                for player_data in squad:
                    if 'player' in player_data and player_data['player']:
                        player = player_data['player']
                        full_name = f"{player.get('firstname', '')} {player.get('lastname', '')}".strip()
                        common_name = player.get('common_name', '')
                        jersey = player_data.get('jersey_number', '?')
                        
                        all_names.append(f"#{jersey} {common_name or full_name}")
                        
                        # Vérifier si c'est un des joueurs recherchés
                        for search_name in search_players:
                            if search_name.lower() in full_name.lower() or search_name.lower() in common_name.lower():
                                found_players.append(f"   ✓ TROUVÉ: #{jersey} {common_name or full_name}")
                
                if found_players:
                    print("\n   🎯 Joueurs confirmés:")
                    for p in found_players:
                        print(p)
                else:
                    print(f"\n   ❌ Aucun des joueurs recherchés trouvé")
                
                print("\n   Tous les joueurs:")
                for name in all_names[:10]:  # Afficher les 10 premiers
                    print(f"   {name}")
                if len(all_names) > 10:
                    print(f"   ... et {len(all_names)-10} autres")
    except Exception as e:
        print(f"   Erreur: {e}")
    
    # Essayer aussi avec la saison 25651
    print("\n2. Avec season 25651 /squads/seasons/25651/teams/{id}:")
    url = f"{BASE_URL}/squads/seasons/25651/teams/{team_id}"
    
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            if 'data' in data and isinstance(data['data'], list):
                squad = data['data']
                print(f"   Total: {len(squad)} joueurs")
                
                found_players = []
                
                for player_data in squad[:5]:  # Vérifier les 5 premiers
                    if 'player' in player_data and player_data['player']:
                        player = player_data['player']
                        full_name = f"{player.get('firstname', '')} {player.get('lastname', '')}".strip()
                        common_name = player.get('common_name', '')
                        
                        for search_name in search_players:
                            if search_name.lower() in full_name.lower() or search_name.lower() in common_name.lower():
                                found_players.append(f"   ✓ TROUVÉ: {common_name or full_name}")
                
                if found_players:
                    print("\n   🎯 Joueurs confirmés:")
                    for p in found_players:
                        print(p)
    except Exception as e:
        print(f"   Erreur: {e}")

# Vérifier chaque club
for club in clubs:
    check_squad(club['id'], club['name'], players_to_verify[club['name']])

print("\n" + "=" * 60)
print("CONCLUSION")
print("=" * 60)
print("\nSi Giroud apparaît à Lille, alors l'endpoint simple /squads/teams/{id}")
print("donne bien les effectifs 2025/2026 actuels.")
print("\nIl faut donc utiliser cet endpoint pour tous les clubs !")