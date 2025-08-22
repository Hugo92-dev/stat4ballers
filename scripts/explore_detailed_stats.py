import requests
import os
import json
import sys
from dotenv import load_dotenv

# Forcer l'encodage UTF-8 pour Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Charger les variables d'environnement
load_dotenv('.env.local')

# Utiliser le token fourni directement
API_TOKEN = 'leBzDfKbRE5k9zEg3FuZE3Hh7XbukODNarOXLoVtPAiAtliDZ19wLu1Wnzi2'
BASE_URL = 'https://api.sportmonks.com/v3/football'

def explore_detailed_statistics():
    """Explorer toutes les statistiques détaillées disponibles pour un joueur"""
    
    # Utilisons Aubameyang comme exemple
    player_id = 31739
    # Saison actuelle Ligue 1 2024/2025
    current_season_id = 25651
    
    print("=== EXPLORATION DES STATISTIQUES DÉTAILLÉES ===\n")
    print(f"Joueur test: Pierre-Emerick Aubameyang (ID: {player_id})")
    print(f"Saison: Ligue 1 2024/2025 (ID: {current_season_id})\n")
    
    # 1. Récupérer les statistiques détaillées pour une saison spécifique
    print("1. STATISTIQUES DÉTAILLÉES PAR SAISON")
    print("-" * 60)
    
    url = f"{BASE_URL}/statistics/seasons/players/{player_id}"
    params = {
        'api_token': API_TOKEN,
        'filters': f'season_ids:{current_season_id}'
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json().get('data', [])
        if data:
            print("✅ Statistiques trouvées pour la saison actuelle:\n")
            stats = data[0] if isinstance(data, list) else data
            
            # Afficher toutes les clés disponibles
            for key, value in stats.items():
                if key not in ['id', 'player_id', 'team_id', 'season_id', 'position_id', 'jersey_number']:
                    print(f"  - {key}: {value}")
        else:
            print("❌ Pas de statistiques pour cette saison")
    else:
        print(f"❌ Erreur: {response.status_code}")
        print(response.text[:500])
    
    print("\n")
    
    # 2. Essayer l'endpoint des statistiques agrégées
    print("2. STATISTIQUES AGRÉGÉES")
    print("-" * 60)
    
    url = f"{BASE_URL}/statistics/aggregated"
    params = {
        'api_token': API_TOKEN,
        'filters': f'player_ids:{player_id};season_ids:{current_season_id}'
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json().get('data', [])
        if data:
            print("✅ Statistiques agrégées trouvées:\n")
            stats = data[0] if isinstance(data, list) else data
            
            # Organiser les stats par catégorie
            categories = {
                'Général': ['minutes', 'games', 'games_started', 'captain'],
                'Buts': ['goals', 'penalties', 'penalties_scored', 'penalties_missed'],
                'Passes': ['assists', 'passes', 'passes_accuracy', 'passes_key', 'passes_total'],
                'Tirs': ['shots', 'shots_on_target', 'shots_total', 'shots_blocked'],
                'Défense': ['tackles', 'blocks', 'interceptions', 'clearances', 'saves'],
                'Discipline': ['yellow_cards', 'yellowred_cards', 'red_cards', 'fouls', 'fouls_drawn'],
                'Dribbles': ['dribbles', 'dribbles_succeeded', 'dribbles_failed', 'dribbles_past'],
                'Duels': ['duels', 'duels_won', 'duels_lost', 'aerial_duels_won', 'aerial_duels_lost'],
                'Avancé': ['expected_goals', 'expected_assists', 'rating', 'offsides']
            }
            
            for category, keys in categories.items():
                print(f"\n  {category}:")
                for key in keys:
                    if key in stats:
                        print(f"    - {key}: {stats[key]}")
        else:
            print("❌ Pas de statistiques agrégées")
    else:
        print(f"❌ Erreur: {response.status_code}")
    
    print("\n")
    
    # 3. Essayer les statistiques détaillées par match
    print("3. STATISTIQUES PAR MATCH (dernier match)")
    print("-" * 60)
    
    # Récupérer les derniers matchs du joueur
    url = f"{BASE_URL}/fixtures"
    params = {
        'api_token': API_TOKEN,
        'filters': f'player_ids:{player_id}',
        'per_page': 1,
        'include': 'statistics'
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json().get('data', [])
        if data and 'statistics' in data[0]:
            print("✅ Statistiques du dernier match trouvées:\n")
            match_stats = data[0]['statistics']
            for stat in match_stats:
                if stat.get('player_id') == player_id:
                    for key, value in stat.items():
                        if key not in ['id', 'player_id', 'team_id', 'fixture_id']:
                            print(f"  - {key}: {value}")
                    break
        else:
            print("❌ Pas de statistiques de match")
    else:
        print(f"❌ Erreur: {response.status_code}")
    
    print("\n")
    
    # 4. Liste complète de toutes les statistiques possibles
    print("=" * 60)
    print("LISTE COMPLÈTE DES STATISTIQUES DISPONIBLES")
    print("=" * 60)
    
    all_stats = {
        "Statistiques de base": [
            "minutes - Minutes jouées",
            "games - Matchs joués", 
            "games_started - Matchs commencés comme titulaire",
            "captain - Fois capitaine",
            "position - Position jouée",
            "rating - Note moyenne"
        ],
        "Statistiques offensives": [
            "goals - Buts marqués",
            "assists - Passes décisives",
            "shots - Tirs",
            "shots_on_target - Tirs cadrés",
            "shots_total - Total de tirs",
            "shots_blocked - Tirs bloqués",
            "penalties - Penalties tirés",
            "penalties_scored - Penalties marqués",
            "penalties_missed - Penalties ratés",
            "expected_goals (xG) - Buts attendus",
            "expected_assists (xA) - Passes décisives attendues"
        ],
        "Statistiques de passes": [
            "passes - Passes réussies",
            "passes_total - Total de passes",
            "passes_accuracy - Précision des passes (%)",
            "passes_key - Passes clés",
            "crosses - Centres",
            "crosses_accurate - Centres réussis",
            "crosses_total - Total de centres"
        ],
        "Statistiques défensives": [
            "tackles - Tacles",
            "tackles_blocks - Tacles et blocks",
            "interceptions - Interceptions",
            "clearances - Dégagements",
            "blocks - Blocks",
            "saves - Arrêts (gardiens)",
            "goals_conceded - Buts encaissés (gardiens)",
            "clean_sheets - Clean sheets (gardiens)"
        ],
        "Statistiques de dribbles": [
            "dribbles - Dribbles tentés",
            "dribbles_succeeded - Dribbles réussis",
            "dribbles_failed - Dribbles ratés",
            "dribbles_past - Fois dribblé par un adversaire"
        ],
        "Statistiques de duels": [
            "duels - Duels totaux",
            "duels_won - Duels gagnés",
            "duels_lost - Duels perdus",
            "aerial_duels - Duels aériens",
            "aerial_duels_won - Duels aériens gagnés",
            "aerial_duels_lost - Duels aériens perdus",
            "ground_duels_won - Duels au sol gagnés"
        ],
        "Statistiques disciplinaires": [
            "yellow_cards - Cartons jaunes",
            "yellowred_cards - Deuxièmes cartons jaunes",
            "red_cards - Cartons rouges",
            "fouls - Fautes commises",
            "fouls_drawn - Fautes subies",
            "offsides - Hors-jeux"
        ],
        "Autres statistiques": [
            "hit_woodwork - Poteaux/barres",
            "dispossessed - Fois dépossédé",
            "touches - Touches de balle",
            "mistakes_leading_to_goals - Erreurs menant à un but",
            "mistakes_leading_to_shots - Erreurs menant à un tir",
            "ball_recoveries - Récupérations de balle",
            "ball_losses - Pertes de balle"
        ]
    }
    
    print("\n✅ STATISTIQUES DISPONIBLES AVEC VOTRE ABONNEMENT:\n")
    for category, stats in all_stats.items():
        print(f"\n{category}:")
        for stat in stats:
            print(f"  • {stat}")
    
    print("\n" + "=" * 60)
    print("RECOMMANDATIONS POUR L'AFFICHAGE")
    print("=" * 60)
    print("\n1. Pour un joueur de champ (attaquant/milieu/défenseur):")
    print("   - Buts, Passes décisives, Minutes jouées")
    print("   - Tirs, Tirs cadrés, xG")
    print("   - Passes réussies, Précision des passes")
    print("   - Dribbles réussis, Duels gagnés")
    print("   - Cartons jaunes/rouges")
    print("\n2. Pour un gardien:")
    print("   - Arrêts, Clean sheets")
    print("   - Buts encaissés, Minutes jouées")
    print("   - Passes réussies, Précision des passes")
    print("   - Cartons jaunes/rouges")

if __name__ == "__main__":
    explore_detailed_statistics()