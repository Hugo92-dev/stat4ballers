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

API_TOKEN = os.getenv('SPORTMONKS_API_TOKEN')
BASE_URL = 'https://api.sportmonks.com/v3/football'

def explore_player_statistics():
    """Explorer toutes les statistiques disponibles pour un joueur"""
    
    # Utilisons Aubameyang comme exemple (ID: 31739)
    player_id = 31739
    
    print("=== EXPLORATION DES STATISTIQUES DISPONIBLES POUR UN JOUEUR ===\n")
    print(f"Joueur test: Pierre-Emerick Aubameyang (ID: {player_id})\n")
    
    # 1. Endpoint basique du joueur
    print("1. ENDPOINT BASIQUE DU JOUEUR")
    print("-" * 50)
    url = f"{BASE_URL}/players/{player_id}"
    params = {'api_token': API_TOKEN}
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()['data']
        print(f"✅ Données de base disponibles:")
        for key in data.keys():
            print(f"   - {key}: {data[key]}")
    else:
        print(f"❌ Erreur: {response.status_code}")
    
    print("\n")
    
    # 2. Avec include=statistics
    print("2. AVEC INCLUDE=STATISTICS")
    print("-" * 50)
    params = {
        'api_token': API_TOKEN,
        'include': 'statistics'
    }
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()['data']
        if 'statistics' in data:
            stats = data['statistics']
            print(f"✅ {len(stats)} entrées de statistiques trouvées")
            if stats:
                # Afficher la première entrée pour voir la structure
                print("\nStructure d'une entrée de statistiques:")
                first_stat = stats[0]
                for key, value in first_stat.items():
                    print(f"   - {key}: {value}")
                
                # Afficher toutes les saisons disponibles
                print("\nSaisons disponibles:")
                seasons = set()
                for stat in stats:
                    if 'season_id' in stat:
                        seasons.add(stat['season_id'])
                for season in sorted(seasons):
                    print(f"   - Season ID: {season}")
        else:
            print("❌ Pas de statistiques disponibles")
    else:
        print(f"❌ Erreur: {response.status_code}")
    
    print("\n")
    
    # 3. Avec include=statistics.details
    print("3. AVEC INCLUDE=STATISTICS.DETAILS")
    print("-" * 50)
    params = {
        'api_token': API_TOKEN,
        'include': 'statistics.details'
    }
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()['data']
        if 'statistics' in data and data['statistics']:
            stat = data['statistics'][0]
            if 'details' in stat:
                print(f"✅ Détails disponibles:")
                details = stat['details']
                for detail in details[:10]:  # Afficher les 10 premiers
                    print(f"   - {detail}")
            else:
                print("❌ Pas de détails dans les statistiques")
        else:
            print("❌ Pas de statistiques disponibles")
    else:
        print(f"❌ Erreur: {response.status_code}")
    
    print("\n")
    
    # 4. Avec include=statistics.seasons
    print("4. AVEC INCLUDE=STATISTICS.SEASONS")
    print("-" * 50)
    params = {
        'api_token': API_TOKEN,
        'include': 'statistics.seasons'
    }
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        print(f"✅ Réponse reçue")
    else:
        print(f"❌ Erreur: {response.status_code}")
    
    print("\n")
    
    # 5. Autres includes possibles
    print("5. AUTRES INCLUDES POSSIBLES")
    print("-" * 50)
    
    includes_to_test = [
        'team',
        'nationality',
        'country',
        'position',
        'detailedposition',
        'metadata',
        'sidelined',
        'trophies',
        'transfers',
        'latest',
        'career'
    ]
    
    for include in includes_to_test:
        params = {
            'api_token': API_TOKEN,
            'include': include
        }
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()['data']
            if include in data:
                print(f"✅ {include}: Disponible")
                # Afficher un échantillon des données
                if isinstance(data[include], dict):
                    keys = list(data[include].keys())[:5]
                    print(f"     Clés: {keys}")
                elif isinstance(data[include], list) and data[include]:
                    print(f"     {len(data[include])} entrées")
            else:
                print(f"❌ {include}: Pas dans la réponse")
        else:
            print(f"❌ {include}: Erreur {response.status_code}")
    
    print("\n")
    
    # 6. Endpoint des statistiques de saison
    print("6. ENDPOINT STATISTIQUES PAR SAISON")
    print("-" * 50)
    
    # Essayer avec la saison Ligue 1 2024/2025
    season_id = 23435
    url = f"{BASE_URL}/players/{player_id}/statistics/seasons/{season_id}"
    params = {'api_token': API_TOKEN}
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Statistiques saison {season_id} disponibles")
        if 'data' in data:
            print(json.dumps(data['data'], indent=2))
    else:
        print(f"❌ Erreur: {response.status_code}")
        if response.status_code == 403:
            print("   → Probablement limité au plan payant")
    
    print("\n")
    
    # 7. Endpoint topscorers (meilleurs buteurs)
    print("7. ENDPOINT TOPSCORERS (MEILLEURS BUTEURS)")
    print("-" * 50)
    
    url = f"{BASE_URL}/topscorers/seasons/{season_id}"
    params = {'api_token': API_TOKEN}
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        try:
            data = response.json().get('data', [])
            print(f"✅ Top buteurs disponibles: {len(data)} joueurs")
            # Chercher Aubameyang dans la liste
            for scorer in data:
                if scorer.get('player_id') == player_id:
                    print(f"\nAubameyang trouvé dans les buteurs:")
                    print(json.dumps(scorer, indent=2))
                    break
        except:
            print("❌ Erreur lors du parsing des données")
    else:
        print(f"❌ Erreur: {response.status_code}")
    
    print("\n")
    
    # 8. Résumé final
    print("=" * 60)
    print("RÉSUMÉ DES STATISTIQUES DISPONIBLES")
    print("=" * 60)
    print("\n✅ DISPONIBLES (Plan gratuit):")
    print("  - Informations de base (nom, âge, position, nationalité, taille, poids)")
    print("  - Équipe actuelle")
    print("  - Nationalité sportive")
    print("  - Position détaillée")
    print("  - Buts (via endpoint topscorers)")
    print("\n❌ NON DISPONIBLES (Plan payant requis):")
    print("  - Statistiques détaillées (passes, xG, tacles, etc.)")
    print("  - Historique complet")
    print("  - Données par match")
    print("  - Trophées")
    print("  - Transferts")

if __name__ == "__main__":
    explore_player_statistics()