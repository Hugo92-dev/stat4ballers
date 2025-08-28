#!/usr/bin/env python3
"""Script de monitoring de la mise à jour des stats"""

import sys
import json
from pathlib import Path
from datetime import datetime
import time

sys.stdout.reconfigure(encoding='utf-8')

def check_file_status(file_path, league_name):
    """Vérifie le statut d'un fichier de stats"""
    if not file_path.exists():
        return f"❌ {league_name}: Non trouvé"
    
    # Vérifier la date de modification
    mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
    age_minutes = (datetime.now() - mtime).total_seconds() / 60
    
    # Lire le fichier pour avoir des infos
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Compter les joueurs
    player_count = content.count('"displayName":')
    
    # Vérifier si c'est la version corrigée
    is_fixed = "Version CORRIGÉE" in content or "Bug de mapping résolu" in content
    
    if age_minutes < 5:
        status = "🔄 En cours de mise à jour"
    elif age_minutes < 60:
        status = "✅ Récemment mis à jour"
    else:
        status = "⚠️ Ancien"
    
    version = "📦 Version corrigée" if is_fixed else "⚠️ Version avec bug"
    
    return f"{status} {league_name}: {player_count} joueurs - {version} - Modifié il y a {int(age_minutes)} min"

def test_player_stats(league_file, player_name, expected_stats):
    """Teste les stats d'un joueur spécifique"""
    if not league_file.exists():
        return None
    
    with open(league_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Chercher le joueur
    if player_name not in content:
        return f"❌ {player_name} non trouvé"
    
    # Extraire ses stats
    start = content.find(f'"{player_name}"')
    if start < 0:
        return f"❌ {player_name} non trouvé"
    
    # Chercher la section de stats récentes
    stats_start = content.find('"2024/2025', start)
    if stats_start < 0:
        stats_start = content.find('"2025/2026', start)
    
    if stats_start < 0:
        return f"⚠️ Pas de stats récentes pour {player_name}"
    
    stats_end = content.find('},', stats_start)
    stats_section = content[stats_start:stats_end]
    
    # Vérifier les valeurs attendues
    results = []
    for stat, expected_value in expected_stats.items():
        if f'"{stat}":' in stats_section:
            # Extraire la valeur
            value_start = stats_section.find(f'"{stat}":') + len(f'"{stat}":')
            value_end = stats_section.find(',', value_start)
            if value_end < 0:
                value_end = stats_section.find('}', value_start)
            
            value_str = stats_section[value_start:value_end].strip()
            
            # Parser la valeur
            try:
                if value_str == 'null':
                    value = None
                elif '.' in value_str:
                    value = float(value_str)
                else:
                    value = int(value_str)
                
                if value == expected_value:
                    results.append(f"✅ {stat}: {value}")
                else:
                    results.append(f"❌ {stat}: {value} (attendu: {expected_value})")
            except:
                results.append(f"⚠️ {stat}: erreur de parsing")
        else:
            results.append(f"❌ {stat}: non trouvé")
    
    return "\n".join(results)

def main():
    print("📊 MONITORING DE LA MISE À JOUR DES STATISTIQUES")
    print("=" * 60)
    
    # Configuration des fichiers
    files_to_check = {
        'ligue1': Path('../data/ligue1PlayersCompleteStats.ts'),
        'premier-league': Path('../data/premier-leaguePlayersCompleteStats.ts'),
        'liga': Path('../data/la-ligaPlayersCompleteStats.ts'),
        'serie-a': Path('../data/serie-aPlayersCompleteStats.ts'),
        'bundesliga': Path('../data/bundesligaPlayersCompleteStats.ts')
    }
    
    # Monitoring continu
    while True:
        print(f"\n⏰ {datetime.now().strftime('%H:%M:%S')}")
        print("-" * 60)
        
        # Vérifier chaque fichier
        for league, file_path in files_to_check.items():
            status = check_file_status(file_path, league.upper())
            print(status)
        
        # Tests de validation sur quelques joueurs clés
        print("\n🔍 Tests de validation:")
        
        # Test Mbappé
        print("\n📌 Mbappé (Real Madrid):")
        mbappe_test = test_player_stats(
            files_to_check['liga'],
            "Kylian Mbappé",
            {"goals": 31, "assists": 39, "minutes": 2919}  # Stats 2024/2025
        )
        if mbappe_test:
            print(mbappe_test)
        
        # Test Donnarumma
        print("\n📌 Donnarumma (PSG):")
        donna_test = test_player_stats(
            files_to_check['ligue1'],
            "Gianluigi Donnarumma",
            {"saves": 49, "goals_conceded": 25, "clean_sheets": 4}  # Stats 2024/2025
        )
        if donna_test:
            print(donna_test)
        
        print("\n" + "=" * 60)
        print("Mise à jour dans 30 secondes... (Ctrl+C pour arrêter)")
        
        try:
            time.sleep(30)
        except KeyboardInterrupt:
            print("\n👋 Arrêt du monitoring")
            break

if __name__ == "__main__":
    main()