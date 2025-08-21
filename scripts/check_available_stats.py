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

def check_topscorers():
    """Vérifie les stats disponibles via topscorers"""
    print("\n" + "=" * 80)
    print("📊 TOPSCORERS - Meilleurs buteurs de Ligue 1")
    print("=" * 80)
    
    url = f"{BASE_URL}/topscorers/seasons/23435"  # Ligue 1 2024/25
    params = {
        'api_token': API_KEY,
        'include': 'player'
    }
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data.get('data'):
            scorers = data['data'][:5]  # Top 5
            
            print(f"\n✅ Top 5 buteurs trouvés!\n")
            
            for i, scorer in enumerate(scorers, 1):
                player = scorer.get('player', {})
                print(f"{i}. {player.get('name', 'N/A')}")
                
                # Afficher TOUTES les stats disponibles
                for key, value in scorer.items():
                    if key not in ['player', 'id'] and value is not None:
                        print(f"   • {key}: {value}")
                print()
    else:
        print(f"❌ Erreur: {response.status_code}")
        print(response.text[:500])

def check_assists():
    """Vérifie les stats de passes décisives"""
    print("\n" + "=" * 80)
    print("🎯 ASSISTS - Meilleurs passeurs de Ligue 1")
    print("=" * 80)
    
    url = f"{BASE_URL}/topassists/seasons/23435"  # Ligue 1 2024/25
    params = {
        'api_token': API_KEY,
        'include': 'player'
    }
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data.get('data'):
            assisters = data['data'][:5]  # Top 5
            
            print(f"\n✅ Top 5 passeurs trouvés!\n")
            
            for i, assister in enumerate(assisters, 1):
                player = assister.get('player', {})
                print(f"{i}. {player.get('name', 'N/A')}")
                
                # Afficher TOUTES les stats disponibles
                for key, value in assister.items():
                    if key not in ['player', 'id'] and value is not None:
                        print(f"   • {key}: {value}")
                print()
    else:
        print(f"❌ Erreur: {response.status_code}")
        # Cet endpoint pourrait ne pas exister

def check_fixtures_stats():
    """Vérifie les stats disponibles dans les matchs"""
    print("\n" + "=" * 80)
    print("⚽ FIXTURES - Stats des matchs récents")
    print("=" * 80)
    
    # D'abord récupérer des matchs récents
    url = f"{BASE_URL}/fixtures"
    params = {
        'api_token': API_KEY,
        'filters': 'fixtureLeagues:301',  # Ligue 1
        'per_page': 5
    }
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data.get('data'):
            fixtures = data['data']
            
            if fixtures:
                print(f"\n✅ {len(fixtures)} matchs trouvés")
                
                # Prendre le premier match et récupérer ses stats
                fixture_id = fixtures[0]['id']
                print(f"\nAnalyse du match ID: {fixture_id}")
                
                # Récupérer les stats du match
                url2 = f"{BASE_URL}/fixtures/{fixture_id}"
                params2 = {
                    'api_token': API_KEY,
                    'include': 'statistics'
                }
                
                response2 = requests.get(url2, params2)
                if response2.status_code == 200:
                    match_data = response2.json()
                    if match_data.get('data'):
                        match = match_data['data']
                        
                        if 'statistics' in match:
                            stats = match['statistics']
                            if stats:
                                print("   ✅ Stats du match disponibles:")
                                
                                # Afficher un échantillon des stats
                                for stat in stats[:5]:
                                    print(f"   - Type: {stat.get('type', {}).get('name', 'N/A')}")
                                    print(f"     Données: {stat.get('data', {})}")
                        else:
                            print("   ❌ Pas de stats pour ce match")
    else:
        print(f"❌ Erreur: {response.status_code}")

def check_player_matches():
    """Vérifie les stats d'un joueur via ses matchs"""
    print("\n" + "=" * 80)
    print("👤 PLAYER MATCHES - Stats par match d'un joueur")
    print("=" * 80)
    
    # Utilisons un ID de joueur du PSG
    player_id = 184675  # Un joueur connu
    
    # D'abord récupérer les infos du joueur
    url = f"{BASE_URL}/players/{player_id}"
    params = {
        'api_token': API_KEY
    }
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data.get('data'):
            player = data['data']
            print(f"\nJoueur: {player.get('name', 'N/A')}")
            print(f"Position: {player.get('position', {}).get('name', 'N/A') if isinstance(player.get('position'), dict) else 'N/A'}")
            
            # Maintenant essayer de récupérer ses matchs
            # Note: Cet endpoint pourrait ne pas être disponible dans le plan gratuit
            print("\nRecherche des matchs du joueur...")
    else:
        print(f"❌ Erreur: {response.status_code}")

def check_standings_detailed():
    """Vérifie le classement avec toutes les stats"""
    print("\n" + "=" * 80)
    print("📋 STANDINGS - Classement avec statistiques détaillées")
    print("=" * 80)
    
    url = f"{BASE_URL}/standings/seasons/23435"  # Ligue 1 2024/25
    params = {
        'api_token': API_KEY
    }
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data.get('data'):
            standings = data['data']
            
            if standings and len(standings) > 0:
                # Prendre le premier groupe (généralement il n'y en a qu'un en Ligue 1)
                group = standings[0] if isinstance(standings, list) else standings
                
                print(f"\n✅ Classement trouvé!\n")
                
                # Afficher les 3 premières équipes
                for team in group.get('standings', [])[:3]:
                    print(f"Position {team.get('position')}: {team.get('participant', {}).get('name', 'N/A')}")
                    
                    # Afficher TOUTES les stats disponibles
                    stats_to_show = ['points', 'games_played', 'won', 'draw', 'lost',
                                     'goals_for', 'goals_against', 'goal_difference']
                    
                    for stat in stats_to_show:
                        if stat in team:
                            print(f"   • {stat}: {team[stat]}")
                    
                    # Chercher d'autres stats
                    other_stats = [k for k in team.keys() 
                                  if k not in stats_to_show + ['id', 'participant', 'position', 'participant_id']]
                    
                    if other_stats:
                        print("   Autres stats disponibles:")
                        for stat in other_stats:
                            if team[stat] is not None:
                                print(f"   • {stat}: {team[stat]}")
                    print()
    else:
        print(f"❌ Erreur: {response.status_code}")
        print(response.text[:500])

def main():
    print("🚀 Analyse des statistiques disponibles dans SportMonks API")
    print(f"   Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("   Plan API: Gratuit (limitations possibles)")
    
    # Tester chaque endpoint
    check_topscorers()
    check_assists()
    check_standings_detailed()
    check_fixtures_stats()
    check_player_matches()
    
    print("\n" + "=" * 80)
    print("📝 RÉSUMÉ DES STATISTIQUES DISPONIBLES")
    print("=" * 80)
    print("""
Avec le plan API actuel, voici les statistiques récupérables:

✅ **DISPONIBLES VIA TOPSCORERS** (/topscorers/seasons/{season_id}):
   - Buts marqués (goals)
   - Nombre de matchs (appearances)
   - Minutes jouées (minutes)
   - Penalties marqués/ratés
   - Équipe et position du joueur

✅ **DISPONIBLES VIA STANDINGS** (/standings/seasons/{season_id}):
   - Stats d'équipe: Points, matchs joués, V/N/D
   - Buts pour/contre, différence de buts
   - Forme récente
   - Statistiques par lieu (domicile/extérieur)

⚠️ **POTENTIELLEMENT DISPONIBLES** (à vérifier):
   - Passes décisives (via topassists endpoint)
   - Stats par match (via fixtures)
   - Cartons jaunes/rouges
   - Temps de jeu détaillé

❌ **NON DISPONIBLES** (plan payant requis):
   - xG, xA (expected goals/assists)
   - Passes réussies, précision
   - Tacles, interceptions
   - Dribbles, duels
   - Tirs cadrés/non-cadrés
   - Stats défensives détaillées

Pour avoir toutes les statistiques détaillées, il faudrait:
1. Soit upgrader vers un plan payant SportMonks
2. Soit combiner avec une autre source de données
3. Soit se limiter aux stats de base (buts, passes, cartons)
""")

if __name__ == "__main__":
    main()