#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import json
import sys
from datetime import datetime

# Forcer l'encodage UTF-8 pour Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'replace')

API_KEY = "j28l04KZC0LGFAdbxIzdyb8zz253K1YegT5vEUN5taw0dxuNr6U3jtRMmS6C"
BASE_URL = "https://api.sportmonks.com/v3/football"

def get_player_statistics(player_id, season_id):
    """Récupère les statistiques d'un joueur pour une saison"""
    url = f"{BASE_URL}/players/{player_id}"
    params = {
        'api_token': API_KEY,
        'include': 'statistics.details,statistics.type,position,nationality'
    }
    
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Erreur API: {response.status_code}")
            print(response.text)
            return None
    except Exception as e:
        print(f"Erreur: {e}")
        return None

def get_player_detailed_stats(player_id, season_id):
    """Récupère les statistiques détaillées via l'endpoint spécifique"""
    url = f"{BASE_URL}/players/{player_id}/statistics/seasons/{season_id}"
    params = {
        'api_token': API_KEY,
        'include': 'details,type'
    }
    
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Erreur API: {response.status_code}")
            print(response.text)
            return None
    except Exception as e:
        print(f"Erreur: {e}")
        return None

def explore_statistics_types():
    """Explore les types de statistiques disponibles"""
    # Prenons Mbappé (ID: 184798) comme exemple
    # Season ID pour Ligue 1 2024/25: 23435
    
    print("=" * 80)
    print("EXPLORATION DES STATISTIQUES DISPONIBLES DANS SPORTMONKS")
    print("=" * 80)
    
    # Test avec Kylian Mbappé au Real Madrid
    player_id = 184798  # Mbappé
    season_id = 23696   # La Liga 2024/25
    
    print(f"\n🔍 Test avec Kylian Mbappé (ID: {player_id})")
    print(f"   Saison La Liga 2024/25 (ID: {season_id})")
    print("-" * 40)
    
    # Méthode 1: Via le player endpoint avec include
    print("\n📊 Méthode 1: Via player endpoint avec statistics")
    data = get_player_statistics(player_id, season_id)
    
    if data and 'data' in data:
        player = data['data']
        print(f"Joueur: {player.get('name', 'N/A')}")
        
        if 'statistics' in player and player['statistics']:
            stats = player['statistics'][0] if isinstance(player['statistics'], list) else player['statistics']
            
            # Lister toutes les clés disponibles
            print("\n🔑 Clés disponibles dans les statistiques:")
            for key in stats.keys():
                value = stats[key]
                if value is not None and value != 0:
                    print(f"  - {key}: {value}")
    
    # Méthode 2: Via l'endpoint spécifique des statistiques
    print("\n📊 Méthode 2: Via endpoint statistics/seasons")
    data2 = get_player_detailed_stats(player_id, season_id)
    
    if data2 and 'data' in data2:
        stats_data = data2['data']
        
        if isinstance(stats_data, dict):
            print("\n🔑 Statistiques détaillées disponibles:")
            
            # Organiser par catégorie
            categories = {
                'Général': ['games', 'minutes', 'starts', 'substitute_in', 'substitute_out', 
                           'substitutes_on_bench', 'captain', 'injured', 'on_bench'],
                'Attaque': ['goals', 'assists', 'shots_total', 'shots_on_target', 'shots_off_target',
                           'shots_blocked', 'penalties_scored', 'penalties_missed', 'penalties_saved',
                           'hit_woodwork', 'rating'],
                'Passes': ['passes_total', 'passes_accuracy', 'passes_key', 'passes_accurate',
                          'passes_inaccurate', 'crosses_total', 'crosses_accurate'],
                'Défense': ['tackles_total', 'tackles_blocks', 'tackles_interceptions',
                           'duels_total', 'duels_won', 'dribbled_past', 'clearances',
                           'blocked_shots', 'interceptions', 'saves', 'goals_conceded'],
                'Discipline': ['yellow_cards', 'yellowred_cards', 'red_cards', 'fouls_committed',
                              'fouls_drawn', 'offsides'],
                'Autres': ['dribbles_attempts', 'dribbles_success', 'dribbles_dribbled_past',
                          'ground_duels_won', 'aerial_duels_won', 'dispossessed', 'mistakes',
                          'ball_losses', 'ball_recoveries']
            }
            
            for category, stat_keys in categories.items():
                print(f"\n📌 {category}:")
                found_stats = []
                for key in stat_keys:
                    if key in stats_data:
                        value = stats_data[key]
                        if value is not None:
                            found_stats.append(f"{key}: {value}")
                
                if found_stats:
                    for stat in found_stats:
                        print(f"    • {stat}")
                else:
                    print(f"    (Aucune statistique trouvée)")
            
            # Afficher toutes les autres clés non catégorisées
            all_categorized = []
            for cat_keys in categories.values():
                all_categorized.extend(cat_keys)
            
            other_keys = [k for k in stats_data.keys() if k not in all_categorized and not k.startswith('_')]
            if other_keys:
                print(f"\n📌 Autres statistiques trouvées:")
                for key in other_keys:
                    value = stats_data[key]
                    if value is not None and value != 0:
                        print(f"    • {key}: {value}")

def test_multiple_players():
    """Test avec plusieurs joueurs pour voir la consistance"""
    print("\n" + "=" * 80)
    print("TEST AVEC PLUSIEURS JOUEURS")
    print("=" * 80)
    
    # Quelques IDs de joueurs connus
    test_players = [
        {'id': 184798, 'name': 'Kylian Mbappé', 'season': 23696},  # La Liga
        {'id': 184786, 'name': 'Jude Bellingham', 'season': 23696}, # La Liga
        {'id': 184675, 'name': 'Erling Haaland', 'season': 23686},  # Premier League
    ]
    
    for player_info in test_players[:1]:  # Test juste avec le premier pour l'instant
        print(f"\n🎯 {player_info['name']}")
        data = get_player_detailed_stats(player_info['id'], player_info['season'])
        
        if data and 'data' in data:
            stats = data['data']
            if isinstance(stats, dict):
                # Compter les stats non-nulles
                non_null_stats = {k: v for k, v in stats.items() 
                                 if v is not None and v != 0 and not k.startswith('_')}
                print(f"   Nombre de statistiques disponibles: {len(non_null_stats)}")
                
                # Afficher quelques stats clés
                key_stats = ['goals', 'assists', 'minutes', 'rating', 'passes_accuracy']
                for stat in key_stats:
                    if stat in stats and stats[stat] is not None:
                        print(f"   - {stat}: {stats[stat]}")

if __name__ == "__main__":
    print("🚀 Démarrage de l'exploration des statistiques SportMonks...")
    print(f"   Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    explore_statistics_types()
    test_multiple_players()
    
    print("\n✅ Exploration terminée!")
    print("\n📝 RÉSUMÉ DES STATISTIQUES DISPONIBLES:")
    print("""
Les principales statistiques récupérables via SportMonks API sont:

🎯 STATISTIQUES GÉNÉRALES:
- Matchs joués, minutes, titularisations
- Remplacements (entrées/sorties)
- Capitanat, blessures

⚽ STATISTIQUES OFFENSIVES:
- Buts, passes décisives
- Tirs (total, cadrés, non-cadrés, bloqués)
- Penalties (marqués, ratés)
- Dribbles (tentés, réussis)
- Note moyenne (rating)

🎯 STATISTIQUES DE PASSES:
- Passes totales, précision des passes
- Passes clés, passes réussies/ratées
- Centres (total, réussis)

🛡️ STATISTIQUES DÉFENSIVES:
- Tacles (total, réussis, interceptions)
- Duels (total, gagnés, aériens, au sol)
- Dégagements, tirs bloqués
- Interceptions

⚠️ DISCIPLINE:
- Cartons jaunes, jaunes-rouges, rouges
- Fautes commises/subies
- Hors-jeu

Ces statistiques peuvent être récupérées pour chaque joueur et chaque saison!
""")