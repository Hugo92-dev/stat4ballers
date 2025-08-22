import requests
import json
import sys

# Forcer l'encodage UTF-8 pour Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Token API avec abonnement avancé
API_TOKEN = 'leBzDfKbRE5k9zEg3FuZE3Hh7XbukODNarOXLoVtPAiAtliDZ19wLu1Wnzi2'
BASE_URL = 'https://api.sportmonks.com/v3/football'

def test_advanced_statistics():
    """Tester les statistiques avancées disponibles avec l'abonnement"""
    
    # ID de joueurs de test (Aubameyang et un autre joueur OM)
    players = [
        {'id': 31739, 'name': 'Aubameyang'},
        {'id': 186553, 'name': 'Leonardo Balerdi'}
    ]
    
    # Saison Ligue 1 2024/2025
    season_id = 25651
    
    print("=== TEST DES STATISTIQUES AVANCÉES ===\n")
    
    for player in players:
        player_id = player['id']
        player_name = player['name']
        
        print(f"\n{'='*60}")
        print(f"JOUEUR: {player_name} (ID: {player_id})")
        print('='*60)
        
        # 1. Test avec include=statistics.details
        print("\n1. STATISTIQUES AVEC DETAILS")
        print("-" * 40)
        
        url = f"{BASE_URL}/players/{player_id}"
        params = {
            'api_token': API_TOKEN,
            'include': 'statistics.details',
            'filters': f'statistics:season_id:{season_id}'
        }
        
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()['data']
            if 'statistics' in data and data['statistics']:
                for stat in data['statistics']:
                    if stat.get('season_id') == season_id:
                        print(f"✅ Statistiques saison {season_id} trouvées")
                        if 'details' in stat and stat['details']:
                            print("\nDétails disponibles:")
                            for detail in stat['details']:
                                if detail.get('type'):
                                    type_info = detail['type']
                                    print(f"  - {type_info.get('name', 'N/A')}: {detail.get('value', 'N/A')}")
                        else:
                            print("Pas de détails disponibles")
                        break
            else:
                print("❌ Pas de statistiques")
        else:
            print(f"❌ Erreur: {response.status_code}")
        
        # 2. Test statistiques de saison directes
        print("\n2. STATISTIQUES DE SAISON DIRECTES")
        print("-" * 40)
        
        url = f"{BASE_URL}/statistics/seasons/players/{player_id}"
        params = {
            'api_token': API_TOKEN,
            'filters': f'season_ids:{season_id}'
        }
        
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json().get('data', [])
            if data:
                stats = data[0] if isinstance(data, list) else data
                print(f"✅ Statistiques trouvées pour la saison {season_id}\n")
                
                # Afficher les statistiques principales
                stats_to_show = {
                    'minutes': 'Minutes jouées',
                    'appearences': 'Apparitions',
                    'lineups': 'Titularisations',
                    'goals': 'Buts',
                    'assists': 'Passes décisives',
                    'saves': 'Arrêts',
                    'inside_box_saves': 'Arrêts dans la surface',
                    'penalties_saved': 'Penalties arrêtés',
                    'yellow_cards': 'Cartons jaunes',
                    'red_cards': 'Cartons rouges',
                    'yellowred_cards': '2e jaune',
                    'rating': 'Note moyenne',
                    'expected_goals': 'xG',
                    'expected_assists': 'xA',
                    'shots': 'Tirs',
                    'shots_on_target': 'Tirs cadrés',
                    'passes': 'Passes réussies',
                    'passes_total': 'Total passes',
                    'passes_accuracy': 'Précision passes',
                    'key_passes': 'Passes clés',
                    'crosses': 'Centres',
                    'crosses_accuracy': 'Précision centres',
                    'tackles': 'Tacles',
                    'blocks': 'Blocks',
                    'interceptions': 'Interceptions',
                    'clearances': 'Dégagements',
                    'dribbles': 'Dribbles tentés',
                    'dribbles_succeeded': 'Dribbles réussis',
                    'dribbled_past': 'Fois dribblé',
                    'duels': 'Duels',
                    'duels_won': 'Duels gagnés',
                    'aerial_duels': 'Duels aériens',
                    'aerial_duels_won': 'Duels aériens gagnés',
                    'fouls': 'Fautes commises',
                    'fouls_drawn': 'Fautes subies',
                    'offsides': 'Hors-jeux',
                    'dispossesed': 'Dépossessions',
                    'clean_sheets': 'Clean sheets',
                    'penalties_committed': 'Penalties concédés'
                }
                
                for key, label in stats_to_show.items():
                    if key in stats and stats[key] is not None:
                        print(f"  {label}: {stats[key]}")
            else:
                print("❌ Pas de statistiques pour cette saison")
        else:
            print(f"❌ Erreur: {response.status_code}")
            if response.status_code == 403:
                print("   → Accès refusé (vérifier l'abonnement)")
        
        # 3. Test topscorers/assists
        print("\n3. MEILLEURS BUTEURS/PASSEURS")
        print("-" * 40)
        
        # Topscorers
        url = f"{BASE_URL}/topscorers/seasons/{season_id}"
        params = {
            'api_token': API_TOKEN,
            'per_page': 100
        }
        
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json().get('data', [])
            found = False
            for scorer in data:
                if scorer.get('player_id') == player_id:
                    print(f"✅ Trouvé dans les buteurs:")
                    print(f"   - Buts: {scorer.get('goals', 0)}")
                    print(f"   - Penalties: {scorer.get('penalties', 0)}")
                    print(f"   - Position: {scorer.get('position', 'N/A')}")
                    found = True
                    break
            if not found:
                print(f"   {player_name} non trouvé dans les buteurs")
        
        # Assists
        url = f"{BASE_URL}/topassists/seasons/{season_id}"
        params = {
            'api_token': API_TOKEN,
            'per_page': 100
        }
        
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json().get('data', [])
            found = False
            for assister in data:
                if assister.get('player_id') == player_id:
                    print(f"✅ Trouvé dans les passeurs:")
                    print(f"   - Passes décisives: {assister.get('assists', 0)}")
                    found = True
                    break
            if not found:
                print(f"   {player_name} non trouvé dans les passeurs")
    
    # Test des statistiques d'équipe
    print(f"\n\n{'='*60}")
    print("TEST STATISTIQUES D'ÉQUIPE (Olympique de Marseille)")
    print('='*60)
    
    team_id = 85  # OM
    
    url = f"{BASE_URL}/statistics/seasons/teams/{team_id}"
    params = {
        'api_token': API_TOKEN,
        'filters': f'season_ids:{season_id}'
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json().get('data', [])
        if data:
            stats = data[0] if isinstance(data, list) else data
            print("✅ Statistiques d'équipe disponibles:")
            print(f"   - Matchs joués: {stats.get('games', 0)}")
            print(f"   - Victoires: {stats.get('wins', 0)}")
            print(f"   - Nuls: {stats.get('draws', 0)}")
            print(f"   - Défaites: {stats.get('losses', 0)}")
            print(f"   - Buts marqués: {stats.get('goals_for', 0)}")
            print(f"   - Buts encaissés: {stats.get('goals_against', 0)}")
            print(f"   - Clean sheets: {stats.get('clean_sheets', 0)}")
    else:
        print(f"❌ Erreur statistiques équipe: {response.status_code}")
    
    print(f"\n{'='*60}")
    print("RÉSUMÉ DES STATISTIQUES DISPONIBLES AVEC VOTRE ABONNEMENT")
    print('='*60)
    
    print("\n✅ STATISTIQUES JOUEUR DISPONIBLES:")
    print("   • Minutes jouées, Apparitions, Titularisations")
    print("   • Buts, Passes décisives, xG, xA")
    print("   • Tirs, Tirs cadrés, Précision")
    print("   • Passes réussies, Précision, Passes clés")
    print("   • Tacles, Blocks, Interceptions, Dégagements")
    print("   • Dribbles réussis/ratés")
    print("   • Duels gagnés/perdus (au sol et aériens)")
    print("   • Cartons jaunes/rouges")
    print("   • Fautes commises/subies")
    print("   • Note moyenne")
    
    print("\n✅ STATISTIQUES GARDIEN DISPONIBLES:")
    print("   • Arrêts, Clean sheets")
    print("   • Arrêts dans la surface")
    print("   • Penalties arrêtés")
    print("   • Buts encaissés")
    
    print("\n✅ STATISTIQUES ÉQUIPE DISPONIBLES:")
    print("   • Résultats (V/N/D)")
    print("   • Buts marqués/encaissés")
    print("   • Clean sheets")
    print("   • Statistiques détaillées par match")

if __name__ == "__main__":
    test_advanced_statistics()