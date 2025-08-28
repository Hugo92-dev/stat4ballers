#!/usr/bin/env python3
import sys
from pathlib import Path
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

def check_stats_files():
    """Vérifie l'état des fichiers de statistiques"""
    
    leagues = {
        'ligue1PlayersCompleteStats.ts': 'Ligue 1',
        'premier-leaguePlayersCompleteStats.ts': 'Premier League',
        'la-ligaPlayersCompleteStats.ts': 'Liga',
        'serie-aPlayersCompleteStats.ts': 'Serie A',
        'bundesligaPlayersCompleteStats.ts': 'Bundesliga'
    }
    
    print("🔍 État des fichiers de statistiques complètes")
    print("=" * 60)
    
    data_dir = Path('../data')
    
    for filename, league_name in leagues.items():
        file_path = data_dir / filename
        
        if file_path.exists():
            # Vérifier la date de modification
            mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
            file_size = file_path.stat().st_size / (1024 * 1024)  # En MB
            
            # Compter les joueurs
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                player_count = content.count('displayName')
                
            # Vérifier si généré récemment (dernières 2 heures)
            age_minutes = (datetime.now() - mtime).total_seconds() / 60
            
            if age_minutes < 120:
                status = "✅ À jour"
                color = "\033[92m"
            else:
                status = "⚠️ Ancien"
                color = "\033[93m"
                
            print(f"{color}{league_name:20s}: {status}\033[0m")
            print(f"  📊 {player_count} joueurs")
            print(f"  📦 {file_size:.2f} MB")
            print(f"  ⏰ Modifié: {mtime.strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Vérifier le contenu généré
            if "Généré automatiquement" in content[:500]:
                print(f"  ✓ Format correct")
            else:
                print(f"  ⚠️ Format à vérifier")
                
        else:
            print(f"\033[91m{league_name:20s}: ❌ Non trouvé\033[0m")
        
        print()
    
    # Résumé
    print("=" * 60)
    print("📈 RÉSUMÉ:")
    
    updated_count = 0
    for filename in leagues:
        file_path = data_dir / filename
        if file_path.exists():
            mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
            age_minutes = (datetime.now() - mtime).total_seconds() / 60
            if age_minutes < 120:
                updated_count += 1
    
    print(f"  • {updated_count}/{len(leagues)} ligues mises à jour récemment")
    
    if updated_count == len(leagues):
        print("\n✨ Toutes les ligues sont à jour!")
    else:
        print(f"\n⚠️ {len(leagues) - updated_count} ligues doivent être mises à jour")

if __name__ == "__main__":
    check_stats_files()