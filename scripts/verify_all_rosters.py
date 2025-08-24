#!/usr/bin/env python3
"""
Vérifier que tous les clubs ont des effectifs complets
"""

import re
from pathlib import Path

data_dir = Path(__file__).parent.parent / 'data'

files = {
    'ligue1': 'ligue1Teams.ts',
    'premier-league': 'premierLeagueTeams.ts',
    'la-liga': 'ligaTeams.ts',
    'serie-a': 'serieATeams.ts',
    'bundesliga': 'bundesligaTeams.ts'
}

print("VÉRIFICATION DES EFFECTIFS")
print("="*50)

total_teams = 0
total_players = 0
teams_with_issues = []

for league, filename in files.items():
    filepath = data_dir / filename
    if filepath.exists():
        content = filepath.read_text(encoding='utf-8')
        
        # Parser les équipes
        teams_pattern = r'\{\s*id:\s*\d+,\s*name:\s*"([^"]+)",\s*slug:\s*"([^"]+)",\s*players:\s*\[(.*?)\]\s*\}'
        teams = re.findall(teams_pattern, content, re.DOTALL)
        
        print(f"\n{league.upper()}: {len(teams)} équipes")
        print("-"*50)
        
        for name, slug, players_str in teams:
            # Compter les joueurs
            player_count = players_str.count('id:')
            total_teams += 1
            total_players += player_count
            
            status = "OK" if player_count >= 20 else "!!"
            if player_count < 20:
                teams_with_issues.append(f"{league}/{slug}: {player_count} joueurs")
                
            print(f"{status} {name:30} ({slug:25}): {player_count} joueurs")

print("\n" + "="*50)
print("RÉSUMÉ")
print("="*50)
print(f"Total: {total_teams} équipes, {total_players} joueurs")
print(f"Moyenne: {total_players/total_teams:.1f} joueurs par équipe")

if teams_with_issues:
    print(f"\nATTENTION: {len(teams_with_issues)} équipes avec moins de 20 joueurs:")
    for issue in teams_with_issues:
        print(f"  - {issue}")
else:
    print("\nSUCCES: Toutes les équipes ont au moins 20 joueurs!")