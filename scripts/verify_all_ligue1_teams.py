import requests
import json
import time
import sys

# Forcer l'encodage UTF-8 pour Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'replace')

API_KEY = "j28l04KZC0LGFAdbxIzdyb8zz253K1YegT5vEUN5taw0dxuNr6U3jtRMmS6C"
BASE_URL = "https://api.sportmonks.com/v3/football"

# Liste complète des clubs Ligue 1 avec leurs IDs SportMonks
LIGUE1_TEAMS = [
    {'id': 591, 'name': 'Paris Saint-Germain', 'slug': 'psg'},
    {'id': 44, 'name': 'Olympique de Marseille', 'slug': 'marseille'},
    {'id': 79, 'name': 'Olympique Lyonnais', 'slug': 'lyon'},
    {'id': 6789, 'name': 'AS Monaco', 'slug': 'monaco'},
    {'id': 65, 'name': 'Lille OSC', 'slug': 'lille'},
    {'id': 85, 'name': 'OGC Nice', 'slug': 'nice'},
    {'id': 1163, 'name': 'Stade Rennais', 'slug': 'rennes'},
    {'id': 66, 'name': 'RC Lens', 'slug': 'lens'},
    {'id': 2348, 'name': 'RC Strasbourg', 'slug': 'strasbourg'},
    {'id': 538, 'name': 'Stade de Reims', 'slug': 'reims'},
    {'id': 82, 'name': 'FC Nantes', 'slug': 'nantes'},
    {'id': 71, 'name': 'Montpellier HSC', 'slug': 'montpellier'},
    {'id': 584, 'name': 'Stade Brestois', 'slug': 'brest'},
    {'id': 583, 'name': 'Toulouse FC', 'slug': 'toulouse'},
    {'id': 1272, 'name': 'AJ Auxerre', 'slug': 'auxerre'},
    {'id': 580, 'name': 'Angers SCO', 'slug': 'angers'},
    {'id': 1246, 'name': 'Le Havre AC', 'slug': 'le-havre'},
    {'id': 1714, 'name': 'AS Saint-Etienne', 'slug': 'saint-etienne'}
]

def get_team_squad(team_id, team_name):
    """Récupérer l'effectif d'une équipe"""
    url = f"{BASE_URL}/squads/teams/{team_id}"
    params = {
        'api_token': API_KEY,
        'include': 'player'
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        if 'data' in data:
            squad = data['data']
            print(f"[OK] {team_name}: {len(squad)} joueurs trouvés")
            
            # Afficher quelques joueurs pour vérification
            if squad:
                print(f"     Exemples de joueurs:")
                for i, player_data in enumerate(squad[:3]):
                    if 'player' in player_data and player_data['player']:
                        player = player_data['player']
                        name = player.get('common_name', player.get('display_name', 'Unknown'))
                        jersey = player_data.get('jersey_number', '?')
                        print(f"       #{jersey} {name}")
            return squad
        else:
            print(f"[ERREUR] {team_name}: Pas de données dans la réponse")
            return []
            
    except requests.exceptions.RequestException as e:
        print(f"[ERREUR] {team_name}: {e}")
        return []

def verify_all_teams():
    """Vérifier tous les clubs de Ligue 1"""
    print("=" * 60)
    print("VERIFICATION DES EFFECTIFS LIGUE 1 2024/2025")
    print("=" * 60)
    
    results = {
        'success': [],
        'failed': [],
        'incomplete': []
    }
    
    for team in LIGUE1_TEAMS:
        print(f"\n{team['name']}...")
        squad = get_team_squad(team['id'], team['name'])
        
        time.sleep(0.5)  # Éviter le rate limiting
        
        if not squad:
            results['failed'].append(team['name'])
        elif len(squad) < 20:
            results['incomplete'].append({
                'name': team['name'],
                'count': len(squad)
            })
        else:
            results['success'].append({
                'name': team['name'],
                'count': len(squad)
            })
    
    # Afficher le résumé
    print("\n" + "=" * 60)
    print("RESUME")
    print("=" * 60)
    
    print(f"\n[OK] CLUBS AVEC EFFECTIFS COMPLETS ({len(results['success'])}):")
    for team in results['success']:
        print(f"  - {team['name']}: {team['count']} joueurs")
    
    if results['incomplete']:
        print(f"\n[WARN] CLUBS AVEC EFFECTIFS INCOMPLETS ({len(results['incomplete'])}):")
        for team in results['incomplete']:
            print(f"  - {team['name']}: {team['count']} joueurs seulement")
    
    if results['failed']:
        print(f"\n[ERREUR] CLUBS SANS DONNEES ({len(results['failed'])}):")
        for team_name in results['failed']:
            print(f"  - {team_name}")
    
    print(f"\nTOTAL: {len(results['success'])}/{len(LIGUE1_TEAMS)} clubs avec données complètes")

if __name__ == "__main__":
    verify_all_teams()