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

def test_endpoints():
    """Test différents endpoints pour trouver comment accéder aux stats"""
    
    print("=" * 80)
    print("TEST DES ENDPOINTS SPORTMONKS POUR LES STATISTIQUES")
    print("=" * 80)
    
    # Test 1: Récupérer un match avec les statistiques
    print("\n📊 Test 1: Statistiques via les matchs (fixtures)")
    # On va chercher un match récent du PSG
    team_id = 85  # PSG
    url = f"{BASE_URL}/fixtures"
    params = {
        'api_token': API_KEY,
        'filters[team_ids]': team_id,
        'filters[season_ids]': 23435,  # Ligue 1 2024/25
        'include': 'statistics,lineups.player,events',
        'per_page': 1
    }
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data.get('data'):
            print("✅ Accès aux fixtures réussi!")
            fixture = data['data'][0] if isinstance(data['data'], list) else data['data']
            
            # Vérifier si on a des stats
            if 'statistics' in fixture:
                print("   Stats disponibles dans le match!")
                stats = fixture['statistics']
                if stats and len(stats) > 0:
                    print(f"   Nombre de stats: {len(stats)}")
                    # Afficher un échantillon
                    for stat in stats[:3]:
                        print(f"   - {stat}")
            
            # Vérifier les lineups
            if 'lineups' in fixture:
                print("   Lineups disponibles!")
                lineups = fixture['lineups']
                if lineups and len(lineups) > 0:
                    for lineup in lineups[:1]:
                        if 'player' in lineup:
                            player = lineup['player']
                            print(f"   Joueur trouvé: {player.get('name', 'N/A')}")
    else:
        print(f"❌ Erreur: {response.status_code}")
        print(response.text[:200])
    
    # Test 2: Statistiques d'équipe pour la saison
    print("\n📊 Test 2: Statistiques d'équipe pour la saison")
    url = f"{BASE_URL}/teams/{team_id}"
    params = {
        'api_token': API_KEY,
        'include': 'statistics.season,squad.player',
        'filters[season_ids]': 23435
    }
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data.get('data'):
            print("✅ Accès aux données d'équipe réussi!")
            team = data['data']
            
            if 'statistics' in team:
                print("   Stats d'équipe disponibles!")
                stats = team['statistics']
                if stats:
                    print(f"   Nombre de stats: {len(stats)}")
            
            if 'squad' in team:
                print("   Squad disponible!")
                squad = team['squad']
                if squad and len(squad) > 0:
                    print(f"   Nombre de joueurs: {len(squad)}")
                    # Vérifier si on a des stats par joueur
                    for player_data in squad[:1]:
                        if 'player' in player_data:
                            player = player_data['player']
                            print(f"   Exemple joueur: {player.get('name', 'N/A')}")
    else:
        print(f"❌ Erreur: {response.status_code}")
        print(response.text[:200])
    
    # Test 3: Topscorers endpoint
    print("\n📊 Test 3: Topscorers de la saison (stats de buts)")
    url = f"{BASE_URL}/topscorers/seasons/{23435}"
    params = {
        'api_token': API_KEY,
        'include': 'player,statistics'
    }
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data.get('data'):
            print("✅ Accès aux topscorers réussi!")
            scorers = data['data']
            if isinstance(scorers, list) and len(scorers) > 0:
                print(f"   Nombre de buteurs: {len(scorers)}")
                for scorer in scorers[:3]:
                    player = scorer.get('player', {})
                    print(f"   - {player.get('name', 'N/A')}")
                    
                    # Afficher les stats disponibles
                    for key, value in scorer.items():
                        if key not in ['player', 'id', 'season_id', 'player_id']:
                            print(f"     • {key}: {value}")
    else:
        print(f"❌ Erreur: {response.status_code}")
        print(response.text[:200])
    
    # Test 4: Standings avec stats
    print("\n📊 Test 4: Classement avec statistiques")
    url = f"{BASE_URL}/standings/seasons/{23435}"
    params = {
        'api_token': API_KEY,
        'include': 'details,group'
    }
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data.get('data'):
            print("✅ Accès au classement réussi!")
            standings = data['data']
            if isinstance(standings, list) and len(standings) > 0:
                standing = standings[0]
                
                # Chercher le PSG dans le classement
                for team_standing in standing.get('standings', [])[:3]:
                    print(f"   Équipe: {team_standing.get('team_name', 'N/A')}")
                    print(f"   - Points: {team_standing.get('points')}")
                    print(f"   - Buts marqués: {team_standing.get('goals_for')}")
                    print(f"   - Buts encaissés: {team_standing.get('goals_against')}")
                    
                    # Afficher toutes les stats disponibles
                    stats_keys = ['won', 'draw', 'lost', 'goals_for', 'goals_against', 
                                 'clean_sheets', 'failed_to_score', 'avg_goals_per_game',
                                 'avg_goals_against_per_game', 'avg_first_goal_scored',
                                 'avg_first_goal_conceded']
                    
                    for key in stats_keys:
                        if key in team_standing:
                            print(f"   - {key}: {team_standing[key]}")
    else:
        print(f"❌ Erreur: {response.status_code}")
        print(response.text[:200])
    
    # Test 5: Player par ID avec différents includes
    print("\n📊 Test 5: Joueur individuel avec différents includes")
    player_id = 184798  # Mbappé
    url = f"{BASE_URL}/players/{player_id}"
    
    includes_to_test = [
        'currentTeam',
        'position',
        'detailedPosition',
        'metadata',
        'transfers',
        'sidelinedHistory'
    ]
    
    for include in includes_to_test:
        params = {
            'api_token': API_KEY,
            'include': include
        }
        
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            if data.get('data'):
                player = data['data']
                if include in player:
                    print(f"   ✅ Include '{include}' disponible")
                    # Afficher un échantillon des données
                    include_data = player[include]
                    if include_data:
                        print(f"      Type: {type(include_data)}")
                        if isinstance(include_data, dict):
                            for key in list(include_data.keys())[:3]:
                                print(f"      - {key}: {include_data[key]}")
        else:
            print(f"   ❌ Include '{include}' non disponible")

if __name__ == "__main__":
    print("🚀 Test des endpoints SportMonks pour les statistiques...")
    print(f"   Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    test_endpoints()
    
    print("\n" + "=" * 80)
    print("RÉSUMÉ DES POSSIBILITÉS")
    print("=" * 80)
    print("""
D'après les tests, voici comment récupérer les statistiques:

1. **Via les TOPSCORERS** (/topscorers/seasons/{season_id})
   - Buts marqués
   - Peut-être passes décisives et autres stats

2. **Via les FIXTURES** (/fixtures avec include=statistics,lineups)
   - Stats match par match
   - Performance individuelle par match

3. **Via les STANDINGS** (/standings/seasons/{season_id})
   - Stats d'équipe globales
   - Buts pour/contre, victoires, défaites, etc.

4. **Via les PLAYERS** (/players/{id})
   - Informations de base du joueur
   - Position, équipe actuelle, etc.
   
Note: L'accès direct aux statistiques détaillées semble limité dans notre plan API.
Il faudra probablement agréger les données depuis plusieurs endpoints.
""")