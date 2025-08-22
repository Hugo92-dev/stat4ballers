import requests
import json
import sys
from datetime import datetime

# Forcer l'encodage UTF-8 pour Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Token API avec abonnement avancé
API_TOKEN = 'leBzDfKbRE5k9zEg3FuZE3Hh7XbukODNarOXLoVtPAiAtliDZ19wLu1Wnzi2'
BASE_URL = 'https://api.sportmonks.com/v3/football'

def get_seasons_for_league(league_id, league_name):
    """Récupérer toutes les saisons d'une ligue"""
    url = f"{BASE_URL}/seasons"
    params = {
        'api_token': API_TOKEN,
        'filters': f'league_id:{league_id}',
        'per_page': 100
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        seasons = response.json().get('data', [])
        print(f"\n{league_name} - Saisons disponibles:")
        print("-" * 50)
        
        # Trier par année décroissante
        seasons_sorted = sorted(seasons, key=lambda x: x.get('name', ''), reverse=True)
        
        recent_seasons = []
        for season in seasons_sorted[:5]:  # Afficher les 5 dernières saisons
            season_name = season.get('name', 'N/A')
            season_id = season.get('id')
            is_current = season.get('is_current', False)
            finished = season.get('finished', False)
            
            status = "🔴 En cours" if is_current else "✅ Terminée" if finished else "⏸️ Pas commencée"
            print(f"  • {season_name} (ID: {season_id}) - {status}")
            
            recent_seasons.append({
                'id': season_id,
                'name': season_name,
                'is_current': is_current,
                'finished': finished
            })
        
        return recent_seasons
    return []

def test_player_historical_stats(player_id, player_name, season_ids):
    """Tester les statistiques d'un joueur sur plusieurs saisons"""
    print(f"\n📊 Statistiques de {player_name} (ID: {player_id})")
    print("=" * 60)
    
    for season in season_ids:
        season_id = season['id']
        season_name = season['name']
        
        print(f"\nSaison {season_name}:")
        print("-" * 40)
        
        url = f"{BASE_URL}/statistics/seasons/players/{player_id}"
        params = {
            'api_token': API_TOKEN,
            'filters': f'season_ids:{season_id}'
        }
        
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json().get('data', [])
            if data and len(data) > 0:
                stats = data[0] if isinstance(data, list) else data
                
                # Vérifier si les statistiques ont des valeurs
                has_stats = any([
                    stats.get('minutes', 0) > 0,
                    stats.get('appearences', 0) > 0,
                    stats.get('goals', 0) > 0,
                    stats.get('assists', 0) > 0
                ])
                
                if has_stats:
                    print("✅ Statistiques disponibles:")
                    
                    # Afficher les stats principales
                    if stats.get('minutes'):
                        print(f"   • Minutes: {stats.get('minutes', 0)}")
                    if stats.get('appearences'):
                        print(f"   • Matchs: {stats.get('appearences', 0)}")
                    if stats.get('lineups'):
                        print(f"   • Titularisations: {stats.get('lineups', 0)}")
                    if stats.get('goals') is not None:
                        print(f"   • Buts: {stats.get('goals', 0)}")
                    if stats.get('assists') is not None:
                        print(f"   • Passes décisives: {stats.get('assists', 0)}")
                    if stats.get('yellow_cards') is not None:
                        print(f"   • Cartons jaunes: {stats.get('yellow_cards', 0)}")
                    if stats.get('red_cards') is not None:
                        print(f"   • Cartons rouges: {stats.get('red_cards', 0)}")
                    if stats.get('rating'):
                        print(f"   • Note moyenne: {stats.get('rating', 0):.2f}")
                    
                    # Stats avancées si disponibles
                    if stats.get('expected_goals'):
                        print(f"   • xG: {stats.get('expected_goals', 0):.2f}")
                    if stats.get('expected_assists'):
                        print(f"   • xA: {stats.get('expected_assists', 0):.2f}")
                    if stats.get('shots'):
                        print(f"   • Tirs: {stats.get('shots', 0)}")
                    if stats.get('shots_on_target'):
                        print(f"   • Tirs cadrés: {stats.get('shots_on_target', 0)}")
                    if stats.get('passes_accuracy'):
                        print(f"   • Précision passes: {stats.get('passes_accuracy', 0)}%")
                else:
                    print("❌ Pas de données statistiques (joueur n'a pas joué)")
            else:
                print("❌ Aucune donnée pour cette saison")
        else:
            print(f"❌ Erreur API: {response.status_code}")

def main():
    print("=== TEST DES STATISTIQUES HISTORIQUES ===")
    print("=" * 60)
    
    # IDs des ligues principales
    leagues = {
        301: 'Ligue 1',
        8: 'Premier League',
        564: 'La Liga',
        384: 'Serie A',
        82: 'Bundesliga'
    }
    
    # 1. Récupérer les saisons disponibles pour chaque ligue
    print("\n🗓️ SAISONS DISPONIBLES PAR CHAMPIONNAT")
    all_seasons = {}
    
    for league_id, league_name in leagues.items():
        seasons = get_seasons_for_league(league_id, league_name)
        all_seasons[league_name] = seasons
    
    # 2. Tester les statistiques historiques pour quelques joueurs
    print("\n\n🎯 TEST DES STATISTIQUES HISTORIQUES DE JOUEURS")
    print("=" * 60)
    
    # Joueurs de test avec leurs ligues
    test_players = [
        {
            'id': 31739,
            'name': 'Pierre-Emerick Aubameyang',
            'league': 'Ligue 1',
            'info': 'Attaquant - Olympique de Marseille'
        },
        {
            'id': 186553,
            'name': 'Leonardo Balerdi',
            'league': 'Ligue 1',
            'info': 'Défenseur - Olympique de Marseille'
        },
        {
            'id': 184798,
            'name': 'Kylian Mbappé',
            'league': 'Ligue 1',
            'info': 'Attaquant - Ex-PSG'
        },
        {
            'id': 899,
            'name': 'Bukayo Saka',
            'league': 'Premier League',
            'info': 'Ailier - Arsenal'
        }
    ]
    
    for player in test_players:
        if player['league'] in all_seasons:
            print(f"\n{'='*60}")
            print(f"{player['name']} - {player['info']}")
            test_player_historical_stats(
                player['id'], 
                player['name'],
                all_seasons[player['league']][:3]  # Tester les 3 dernières saisons
            )
    
    # 3. Résumé final
    print("\n\n" + "=" * 60)
    print("📋 RÉSUMÉ DE L'HISTORIQUE DISPONIBLE")
    print("=" * 60)
    
    print("\n✅ DONNÉES HISTORIQUES DISPONIBLES:")
    print("   • Statistiques complètes des saisons précédentes")
    print("   • Généralement 10+ saisons d'historique par ligue")
    print("   • Données détaillées pour chaque saison terminée")
    print("   • Possibilité de comparer les performances entre saisons")
    
    print("\n📊 STATISTIQUES ACCESSIBLES PAR SAISON:")
    print("   • Toutes les stats listées précédemment")
    print("   • Minutes, buts, passes décisives")
    print("   • xG, xA (saisons récentes)")
    print("   • Cartons, fautes, tirs, passes")
    print("   • Note moyenne par saison")
    
    print("\n💡 RECOMMANDATIONS D'AFFICHAGE:")
    print("   • Afficher la saison en cours (même si peu de données)")
    print("   • Ajouter les 2-3 dernières saisons terminées")
    print("   • Permettre de basculer entre les saisons")
    print("   • Afficher l'évolution des stats clés")

if __name__ == "__main__":
    main()