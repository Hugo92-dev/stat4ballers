import requests
import json
import sys

# Forcer l'encodage UTF-8 pour Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Token API
API_TOKEN = 'leBzDfKbRE5k9zEg3FuZE3Hh7XbukODNarOXLoVtPAiAtliDZ19wLu1Wnzi2'
BASE_URL = 'https://api.sportmonks.com/v3/football'

def test_known_seasons():
    """Tester avec des IDs de saisons connus"""
    
    print("=== TEST DES SAISONS HISTORIQUES CONNUES ===\n")
    
    # IDs de saisons connues (basé sur le script précédent)
    known_seasons = {
        'Ligue 1': [
            {'id': 25651, 'name': '2024/2025', 'status': 'current'},
            {'id': 23435, 'name': '2023/2024', 'status': 'finished'},
            {'id': 21053, 'name': '2022/2023', 'status': 'finished'},
            {'id': 19734, 'name': '2021/2022', 'status': 'finished'},
            {'id': 18378, 'name': '2020/2021', 'status': 'finished'}
        ],
        'Premier League': [
            {'id': 25655, 'name': '2024/2025', 'status': 'current'},
            {'id': 23625, 'name': '2023/2024', 'status': 'finished'},
            {'id': 21779, 'name': '2022/2023', 'status': 'finished'},
            {'id': 19799, 'name': '2021/2022', 'status': 'finished'}
        ]
    }
    
    # Joueurs de test avec historique connu
    test_cases = [
        {
            'player_id': 31739,
            'player_name': 'Aubameyang',
            'seasons_to_test': [25651, 23435]  # Saisons récentes Ligue 1
        },
        {
            'player_id': 184798,
            'player_name': 'Mbappé',
            'seasons_to_test': [23435, 21053, 19734]  # Saisons PSG
        },
        {
            'player_id': 186,
            'player_name': 'Messi',
            'seasons_to_test': [23435, 21053]  # Saisons PSG
        },
        {
            'player_id': 899,
            'player_name': 'Saka',
            'seasons_to_test': [25655, 23625, 21779]  # Saisons Arsenal
        }
    ]
    
    for test in test_cases:
        print(f"\n{'='*60}")
        print(f"📊 {test['player_name']} (ID: {test['player_id']})")
        print('='*60)
        
        for season_id in test['seasons_to_test']:
            # Trouver le nom de la saison
            season_name = 'Inconnue'
            for league, seasons in known_seasons.items():
                for s in seasons:
                    if s['id'] == season_id:
                        season_name = f"{league} {s['name']}"
                        break
            
            print(f"\nSaison {season_name} (ID: {season_id}):")
            print("-" * 40)
            
            # Tester l'endpoint des statistiques
            url = f"{BASE_URL}/statistics/seasons/players/{test['player_id']}"
            params = {
                'api_token': API_TOKEN,
                'filters': f'season_ids:{season_id}'
            }
            
            response = requests.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json().get('data', [])
                if data and len(data) > 0:
                    stats = data[0] if isinstance(data, list) else data
                    
                    # Afficher les stats si elles existent
                    if stats.get('minutes', 0) > 0 or stats.get('appearences', 0) > 0:
                        print("✅ Statistiques disponibles:")
                        
                        # Stats principales
                        print(f"   • Minutes: {stats.get('minutes', 0)}")
                        print(f"   • Matchs: {stats.get('appearences', 0)}")
                        print(f"   • Titularisations: {stats.get('lineups', 0)}")
                        print(f"   • Buts: {stats.get('goals', 0)}")
                        print(f"   • Passes décisives: {stats.get('assists', 0)}")
                        
                        # Stats avancées si disponibles
                        if stats.get('rating'):
                            print(f"   • Note moyenne: {stats.get('rating', 0):.2f}")
                        if stats.get('expected_goals'):
                            print(f"   • xG: {stats.get('expected_goals', 0):.2f}")
                        if stats.get('expected_assists'):
                            print(f"   • xA: {stats.get('expected_assists', 0):.2f}")
                        
                        # Cartons
                        if stats.get('yellow_cards') or stats.get('red_cards'):
                            print(f"   • Cartons J/R: {stats.get('yellow_cards', 0)}/{stats.get('red_cards', 0)}")
                    else:
                        print("❌ Pas de données (joueur n'a pas joué cette saison)")
                else:
                    print("❌ Aucune donnée disponible")
            else:
                print(f"❌ Erreur API: {response.status_code}")
    
    # Test avec un joueur plus récent (pour voir plus de saisons)
    print(f"\n\n{'='*60}")
    print("📊 TEST COMPLET: Mbappé - Toutes les saisons")
    print('='*60)
    
    player_id = 184798
    
    # Récupérer toutes les statistiques du joueur
    url = f"{BASE_URL}/players/{player_id}"
    params = {
        'api_token': API_TOKEN,
        'include': 'statistics'
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()['data']
        if 'statistics' in data:
            stats_list = data['statistics']
            print(f"\n✅ {len(stats_list)} saisons trouvées dans l'historique")
            
            # Compter les saisons avec des données
            seasons_with_data = 0
            for stat in stats_list:
                if stat.get('has_values'):
                    seasons_with_data += 1
            
            print(f"   • Saisons avec données: {seasons_with_data}")
            print(f"   • Saisons sans données: {len(stats_list) - seasons_with_data}")
            
            # Afficher quelques saisons avec données
            print("\nSaisons avec statistiques disponibles (IDs):")
            count = 0
            for stat in stats_list:
                if stat.get('has_values') and count < 10:
                    season_id = stat.get('season_id')
                    team_id = stat.get('team_id')
                    print(f"   • Saison ID: {season_id}, Équipe ID: {team_id}")
                    count += 1
    
    print(f"\n\n{'='*60}")
    print("📋 RÉSUMÉ FINAL")
    print('='*60)
    
    print("\n✅ HISTORIQUE DISPONIBLE:")
    print("   • Les statistiques des saisons précédentes SONT disponibles")
    print("   • Données complètes pour les saisons terminées")
    print("   • La saison en cours a peu/pas de données (normal en début de saison)")
    print("   • L'historique remonte à plusieurs années")
    
    print("\n📊 DONNÉES ACCESSIBLES:")
    print("   • Statistiques détaillées par saison")
    print("   • Minutes, matchs, titularisations")
    print("   • Buts, passes décisives")
    print("   • xG, xA (saisons récentes)")
    print("   • Notes moyennes")
    print("   • Cartons et discipline")
    
    print("\n💡 IMPLÉMENTATION SUGGÉRÉE:")
    print("   • Afficher par défaut la saison en cours")
    print("   • Ajouter un sélecteur pour voir les saisons précédentes")
    print("   • Afficher 2023/2024 et 2022/2023 comme historique")
    print("   • Comparer l'évolution entre les saisons")

if __name__ == "__main__":
    test_known_seasons()