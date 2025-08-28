#!/usr/bin/env python3
"""Test de l'intégration front-end avec les nouvelles données"""

import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

def check_data_format():
    """Vérifie que les données sont au bon format"""
    
    print("🔍 Vérification du format des données")
    print("=" * 60)
    
    # Vérifier le fichier Ligue 1
    ligue1_file = Path('../data/ligue1PlayersCompleteStats.ts')
    
    if not ligue1_file.exists():
        print("❌ Fichier ligue1PlayersCompleteStats.ts non trouvé")
        return False
    
    with open(ligue1_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Vérifier les exports
    checks = {
        "Export correct": "export const ligue1PlayersRealStats" in content,
        "Interface PlayerRealStats": "export interface PlayerRealStats" in content,
        "Interface PlayerSeasonStats": "export interface PlayerSeasonStats" in content,
        "Données Donnarumma": '"129771":' in content,
        "Stats 2024/2025": '"2024/2025' in content,
        "Stats 2023/2024": '"2023/2024' in content,
        "Rating présent": '"rating":' in content,
        "Saves présent": '"saves":' in content,
        "Goals_conceded présent": '"goals_conceded":' in content
    }
    
    all_ok = True
    for check_name, result in checks.items():
        status = "✅" if result else "❌"
        print(f"  {status} {check_name}")
        if not result:
            all_ok = False
    
    # Vérifier spécifiquement Donnarumma
    print("\n📊 Analyse des stats de Donnarumma:")
    
    # Extraire la section Donnarumma
    start = content.find('"129771":')
    if start > 0:
        end = content.find('\n  },\n  "', start + 10)
        if end < 0:
            end = len(content) - 10
        
        donnarumma_section = content[start:end]
        
        # Compter les valeurs non-null dans la saison 2024/2025
        season_start = donnarumma_section.find('"2024/2025')
        if season_start > 0:
            season_end = donnarumma_section.find('},', season_start)
            season_data = donnarumma_section[season_start:season_end]
            
            # Compter les stats remplies
            stats_count = 0
            for line in season_data.split('\n'):
                if '": ' in line and 'null' not in line and '"team"' not in line and '"league"' not in line:
                    stats_count += 1
            
            print(f"  • Nombre de stats non-null en 2024/2025: {stats_count}")
            
            # Vérifier les stats clés pour un gardien
            key_stats = ['saves', 'goals_conceded', 'clean_sheets', 'minutes', 'appearences']
            for stat in key_stats:
                if f'"{stat}":' in season_data and f'"{stat}": null' not in season_data:
                    print(f"  ✅ {stat} présent")
                else:
                    print(f"  ⚠️ {stat} manquant ou null")
    
    return all_ok

def test_api_endpoint():
    """Teste l'endpoint API directement"""
    import requests
    
    print("\n🌐 Test de l'API")
    print("=" * 60)
    
    # Test pour Donnarumma
    player_id = 129771
    league = 'ligue1'
    
    url = f"http://localhost:3000/api/player-stats?playerId={player_id}&league={league}"
    
    try:
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print(f"  ✅ API répond correctement")
            
            if 'current' in data:
                current = data['current']
                if current:
                    print(f"  📊 Stats saison en cours:")
                    for key in ['appearences', 'minutes', 'saves', 'goals_conceded', 'clean_sheets']:
                        if key in current:
                            print(f"    • {key}: {current[key]}")
                else:
                    print(f"  ⚠️ Pas de stats pour la saison en cours")
            
            if 'previous' in data and data['previous']:
                print(f"  📊 {len(data['previous'])} saisons précédentes disponibles")
        else:
            print(f"  ❌ Erreur API: Status {response.status_code}")
            
    except Exception as e:
        print(f"  ⚠️ API non accessible: {e}")
        print("  ℹ️ Assurez-vous que le serveur Next.js est lancé (npm run dev)")

def main():
    print("🚀 Test d'intégration Front-End")
    print("=" * 60)
    
    # Vérifier le format des données
    data_ok = check_data_format()
    
    # Tester l'API
    test_api_endpoint()
    
    print("\n" + "=" * 60)
    if data_ok:
        print("✅ Les données sont prêtes pour le front-end")
        print("\n📌 Pour voir les stats sur le site:")
        print("   http://localhost:3000/ligue1/paris-saint-germain/gianluigi-donnarumma")
    else:
        print("⚠️ Les données doivent être mises à jour")
        print("   Lancez: python update_all_stats_correct_mapping.py")

if __name__ == "__main__":
    main()