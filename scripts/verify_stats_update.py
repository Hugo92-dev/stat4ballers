import json
import os
import sys
from pathlib import Path
from datetime import datetime

# Fix pour l'encodage UTF-8 sur Windows
sys.stdout.reconfigure(encoding='utf-8')

def check_league_stats(league_key, config):
    """Vérifie les stats générées pour un championnat"""
    print(f"\n🏆 {config['name']}")
    print("-" * 40)
    
    stats_files = list(Path('../data').glob(f'{league_key}PlayersStats_*.ts'))
    
    if not stats_files:
        print(f"  ⚠️ Aucun fichier de stats trouvé")
        return False
    
    print(f"  📊 {len(stats_files)} équipes avec stats générées:")
    
    for stats_file in stats_files:
        team_slug = stats_file.stem.replace(f'{league_key}PlayersStats_', '')
        
        # Vérifier la date de modification
        mtime = datetime.fromtimestamp(stats_file.stat().st_mtime)
        age_minutes = (datetime.now() - mtime).total_seconds() / 60
        
        if age_minutes < 60:  # Fichier modifié dans la dernière heure
            status = "✅ À jour"
        else:
            status = "⚠️ Ancien"
            
        # Lire le contenu pour compter les joueurs
        with open(stats_file, 'r', encoding='utf-8') as f:
            content = f.read()
            player_count = content.count('displayName')
            
        print(f"    - {team_slug}: {player_count} joueurs {status} ({mtime.strftime('%H:%M:%S')})")
    
    return True

def main():
    """Vérifie l'état de la mise à jour des stats"""
    print("🔍 Vérification de la mise à jour des statistiques")
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    leagues_config = {
        'ligue1': {
            'name': 'Ligue 1',
            'expected_teams': 18
        },
        'premier-league': {
            'name': 'Premier League',
            'expected_teams': 20
        },
        'liga': {
            'name': 'Liga',
            'expected_teams': 20
        },
        'serie-a': {
            'name': 'Serie A',
            'expected_teams': 20
        },
        'bundesliga': {
            'name': 'Bundesliga',
            'expected_teams': 18
        }
    }
    
    summary = []
    
    for league_key, config in leagues_config.items():
        has_stats = check_league_stats(league_key, config)
        if has_stats:
            stats_files = list(Path('../data').glob(f'{league_key}PlayersStats_*.ts'))
            completion = (len(stats_files) / config['expected_teams']) * 100
            summary.append(f"{config['name']}: {len(stats_files)}/{config['expected_teams']} ({completion:.0f}%)")
    
    print("\n" + "=" * 50)
    print("📈 RÉSUMÉ:")
    for item in summary:
        print(f"  • {item}")
    
    # Vérifier si le script principal est toujours en cours
    if os.path.exists('fetch_all_leagues_complete_stats.py'):
        print("\n⚙️ Le script de mise à jour principale semble toujours actif")

if __name__ == "__main__":
    main()