import json
import sys
import os
from pathlib import Path

# Fix pour l'encodage UTF-8 sur Windows
sys.stdout.reconfigure(encoding='utf-8')

def check_club_stats(file_path, league_name):
    """Vérifie les statistiques d'un fichier de ligue"""
    print(f"\n📊 VÉRIFICATION {league_name.upper()}")
    print("=" * 50)
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Extraction basique des équipes sans évaluation du code
        teams_with_issues = []
        teams_ok = []
        
        # Chercher les équipes dans le contenu
        import re
        team_blocks = re.findall(r'{\s*id:\s*\d+,\s*name:\s*["\']([^"\']+)["\'],\s*slug:\s*["\']([^"\']+)["\'],\s*players:\s*\[(.*?)\]', content, re.DOTALL)
        
        for team_name, team_slug, players_content in team_blocks:
            # Compter les joueurs avec des stats
            players_with_stats = players_content.count('"2025_2026"')
            players_with_2024 = players_content.count('"2024_2025"')
            players_with_2023 = players_content.count('"2023_2024"')
            
            total_players = players_content.count('nom:')
            
            if players_with_stats > 0:
                teams_ok.append({
                    'name': team_name,
                    'slug': team_slug,
                    'total_players': total_players,
                    'with_2025': players_with_stats,
                    'with_2024': players_with_2024,
                    'with_2023': players_with_2023
                })
            else:
                teams_with_issues.append({
                    'name': team_name,
                    'slug': team_slug,
                    'total_players': total_players
                })
        
        # Rapport
        print(f"✅ Équipes OK: {len(teams_ok)}")
        print(f"⚠️  Équipes avec problèmes: {len(teams_with_issues)}")
        
        if teams_with_issues:
            print("\n🔍 ÉQUIPES À PROBLÈMES:")
            for team in teams_with_issues:
                print(f"  - {team['name']} ({team['slug']}) - {team['total_players']} joueurs")
        
        if teams_ok:
            print(f"\n📈 STATISTIQUES DES ÉQUIPES OK:")
            total_players = sum(team['total_players'] for team in teams_ok)
            total_2025 = sum(team['with_2025'] for team in teams_ok)
            total_2024 = sum(team['with_2024'] for team in teams_ok)
            total_2023 = sum(team['with_2023'] for team in teams_ok)
            
            print(f"  - Total joueurs: {total_players}")
            print(f"  - Avec stats 2025/2026: {total_2025}")
            print(f"  - Avec stats 2024/2025: {total_2024}")
            print(f"  - Avec stats 2023/2024: {total_2023}")
        
        return teams_with_issues, teams_ok
        
    except Exception as e:
        print(f"❌ Erreur lors de la lecture de {file_path}: {e}")
        return [], []

def main():
    print("🔍 VÉRIFICATION COMPLÈTE DES STATISTIQUES")
    print("=" * 60)
    
    # Fichiers à vérifier
    files_to_check = [
        ('data/ligue1Teams.ts', 'Ligue 1'),
        ('data/premierLeagueTeams.ts', 'Premier League'),
        ('data/ligaTeams.ts', 'Liga'),
        ('data/serieATeams.ts', 'Serie A'),
        ('data/bundesligaTeams.ts', 'Bundesliga')
    ]
    
    all_issues = []
    all_ok = []
    
    for file_path, league_name in files_to_check:
        if os.path.exists(file_path):
            issues, ok = check_club_stats(file_path, league_name)
            all_issues.extend([(league_name, team) for team in issues])
            all_ok.extend([(league_name, team) for team in ok])
        else:
            print(f"⚠️  Fichier non trouvé: {file_path}")
    
    # Résumé global
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ GLOBAL")
    print("=" * 60)
    
    print(f"✅ Total équipes avec stats: {len(all_ok)}")
    print(f"⚠️  Total équipes problématiques: {len(all_issues)}")
    
    if all_issues:
        print("\n🎯 CLUBS À METTRE À JOUR EN PRIORITÉ:")
        for league, team in all_issues:
            print(f"  - {league}: {team['name']} ({team['slug']})")
    
    # Clubs spécifiquement mentionnés
    problem_clubs = [
        'olympique-lyonnais', 'fc-bayern-munchen', 'fsv-mainz-05', 
        'fc-union-berlin', 'tsg-hoffenheim', 'fc-koln'
    ]
    
    print(f"\n🔍 VÉRIFICATION CLUBS SPÉCIFIQUES:")
    for league, team in all_ok + [(l, {'slug': t['slug'], 'name': t['name']}) for l, t in all_issues]:
        if team['slug'] in problem_clubs:
            status = "✅" if any(team['slug'] == ok_team['slug'] for _, ok_team in all_ok) else "⚠️"
            print(f"  {status} {team['name']} ({team['slug']})")

if __name__ == "__main__":
    main()