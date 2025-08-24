import requests
import json
from dotenv import load_dotenv
import os
import sys

# Fix pour l'encodage UTF-8 sur Windows
sys.stdout.reconfigure(encoding='utf-8')

# Charger les variables d'environnement
load_dotenv('../.env.local')
API_KEY = os.getenv('SPORTMONKS_API_TOKEN')

if not API_KEY:
    print("Clé API manquante")
    exit(1)

BASE_URL = "https://api.sportmonks.com/v3/football"

print("=== Récupération des saisons de Ligue 1 ===\n")

# Essayer avec l'endpoint général des saisons
url = f"{BASE_URL}/seasons"
params = {
    'api_token': API_KEY,
    'filters': 'leagueIds:61',  # Ligue 1
    'per_page': 100
}

response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()
    
    if 'data' in data:
        seasons = data['data']
        
        # Trier par ending_at décroissant pour avoir les plus récentes en premier
        seasons_sorted = sorted(seasons, key=lambda x: x.get('ending_at', ''), reverse=True)
        
        print(f"Nombre total de saisons Ligue 1 trouvées: {len(seasons)}\n")
        print("Saisons récentes de Ligue 1:")
        print("-" * 60)
        
        # Identifier les saisons qui nous intéressent
        target_seasons = {}
        
        for season in seasons_sorted[:10]:  # Afficher les 10 dernières
            season_id = season.get('id')
            name = season.get('name', 'Unknown')
            is_current = season.get('is_current', False)
            finished = season.get('finished', False)
            starting_at = season.get('starting_at', 'Unknown')
            ending_at = season.get('ending_at', 'Unknown')
            
            # Identifier les saisons spécifiques par les dates
            if '2025' in starting_at or '2025' in name:
                if is_current or not finished:
                    target_seasons['2025/2026'] = season_id
            elif '2024' in starting_at:
                target_seasons['2024/2025'] = season_id
            elif '2023' in starting_at:
                target_seasons['2023/2024'] = season_id
            
            status = "🟢 EN COURS" if is_current else ("✅ Terminée" if finished else "⏳ En attente")
            
            print(f"\nID: {season_id}")
            print(f"  Nom: {name}")
            print(f"  Statut: {status}")
            print(f"  Début: {starting_at}")
            print(f"  Fin: {ending_at}")
        
        print("\n" + "=" * 60)
        print("SAISONS IDENTIFIÉES POUR RÉCUPÉRER LES STATS:")
        print("=" * 60)
        
        for season_name, season_id in sorted(target_seasons.items()):
            print(f"  {season_name}: ID = {season_id}")
        
        # Sauvegarder les IDs des saisons
        with open('ligue1_seasons.json', 'w', encoding='utf-8') as f:
            json.dump({
                'all_seasons': seasons,
                'target_seasons': target_seasons
            }, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Saisons sauvegardées dans ligue1_seasons.json")
        
        # Afficher le code à utiliser
        print("\n📝 Code à utiliser dans fetch_om_complete_stats.py:")
        print("-" * 60)
        
        if target_seasons:
            # Obtenir les IDs dans l'ordre chronologique
            season_ids = [
                target_seasons.get('2023/2024'),
                target_seasons.get('2024/2025'),
                target_seasons.get('2025/2026')
            ]
            season_ids = [s for s in season_ids if s]  # Retirer les None
            
            print(f"SEASON_IDS = {season_ids}  # IDs corrects pour Ligue 1")
            print(f"# Mapping:")
            for season_name, season_id in sorted(target_seasons.items()):
                print(f"#   {season_id} = {season_name}")
        else:
            print("⚠️ Aucune saison cible trouvée - vérifier manuellement")
            
else:
    print(f"Erreur: {response.status_code}")
    if response.text:
        print(response.text)