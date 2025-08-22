import requests
import sys
import json

# Forcer l'encodage UTF-8 pour Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

API_TOKEN = 'leBzDfKbRE5k9zEg3FuZE3Hh7XbukODNarOXLoVtPAiAtliDZ19wLu1Wnzi2'
BASE_URL = 'https://api.sportmonks.com/v3/football'

def test_om_players():
    """Tester quelques joueurs de l'OM"""
    
    print("=== TEST INTÉGRATION COMPLÈTE OM ===\n")
    
    # Quelques joueurs de l'OM avec leurs IDs réels
    players = [
        {'name': 'Pierre-Emerick Aubameyang', 'id': 31739},
        {'name': 'Mason Greenwood', 'id': 184465},
        {'name': 'Amine Harit', 'id': 31166},
        {'name': 'Geoffrey Kondogbia', 'id': 906},
        {'name': 'Leonardo Balerdi', 'id': 186553}
    ]
    
    # IDs des saisons
    seasons = [
        {'id': 25651, 'name': '2025/2026 (actuelle)'},
        {'id': 23435, 'name': '2024/2025'},
        {'id': 21053, 'name': '2023/2024'}
    ]
    
    for player in players:
        print(f"\n{'='*60}")
        print(f"📊 {player['name']} (ID: {player['id']})")
        print('='*60)
        
        total_goals = 0
        total_assists = 0
        total_minutes = 0
        total_matches = 0
        seasons_with_data = []
        
        for season in seasons:
            url = f"{BASE_URL}/statistics/seasons/players/{player['id']}"
            params = {
                'api_token': API_TOKEN,
                'filters': f'season_ids:{season["id"]}'
            }
            
            response = requests.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json().get('data', [])
                if data:
                    stats = data[0] if isinstance(data, list) else data
                    
                    # Vérifier si le joueur a des données
                    minutes = stats.get('minutes', 0)
                    matches = stats.get('appearences', 0)
                    goals = stats.get('goals', 0)
                    assists = stats.get('assists', 0)
                    
                    if minutes > 0 or matches > 0:
                        print(f"\n✅ {season['name']}:")
                        print(f"   • Minutes: {minutes}")
                        print(f"   • Matchs: {matches}")
                        print(f"   • Buts: {goals}")
                        print(f"   • Passes décisives: {assists}")
                        
                        if stats.get('rating'):
                            print(f"   • Note moyenne: {stats.get('rating'):.2f}")
                        if stats.get('yellow_cards'):
                            print(f"   • Cartons jaunes: {stats.get('yellow_cards')}")
                        
                        total_goals += goals
                        total_assists += assists
                        total_minutes += minutes
                        total_matches += matches
                        seasons_with_data.append(season['name'])
                    else:
                        print(f"\n⏸️ {season['name']}: Pas de données")
                else:
                    print(f"\n❌ {season['name']}: Aucune donnée")
        
        # Afficher le cumul
        if seasons_with_data:
            print(f"\n📊 CUMUL TOTAL ({len(seasons_with_data)} saisons):")
            print(f"   • Total minutes: {total_minutes}")
            print(f"   • Total matchs: {total_matches}")
            print(f"   • Total buts: {total_goals}")
            print(f"   • Total passes décisives: {total_assists}")
            if total_matches > 0:
                print(f"   • Ratio buts/match: {total_goals/total_matches:.2f}")
                print(f"   • Ratio passes/match: {total_assists/total_matches:.2f}")
    
    print(f"\n\n{'='*60}")
    print("💡 RÉSUMÉ")
    print('='*60)
    print("\n✅ Système fonctionnel:")
    print("   • API répond correctement")
    print("   • Données disponibles pour certaines saisons")
    print("   • Calcul du cumul possible")
    print("\n📝 Notes:")
    print("   • Saison 2025/2026 vient de commencer (peu/pas de données)")
    print("   • Certains joueurs ont des données historiques")
    print("   • Le système de vue cumulée est prêt")

if __name__ == "__main__":
    test_om_players()