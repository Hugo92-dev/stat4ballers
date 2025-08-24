#!/usr/bin/env python3
"""
Extraire les IDs corrects depuis nos fichiers de données
"""

import re
from pathlib import Path

data_dir = Path(__file__).parent.parent / 'data'

# Fichiers à analyser
files = {
    'ligue1': 'ligue1Teams.ts',
    'premier-league': 'premierLeagueTeams.ts',
    'la-liga': 'ligaTeams.ts',
    'serie-a': 'serieATeams.ts',
    'bundesliga': 'bundesligaTeams.ts'
}

all_teams = {}

for league, filename in files.items():
    filepath = data_dir / filename
    if filepath.exists():
        content = filepath.read_text(encoding='utf-8')
        
        # Extraire les IDs et slugs
        team_pattern = r'id:\s*(\d+),\s*name:\s*"([^"]+)",\s*slug:\s*"([^"]+)"'
        matches = re.findall(team_pattern, content)
        
        teams = {}
        for team_id, name, slug in matches:
            teams[slug] = int(team_id)
            print(f"{league}: {slug} -> {team_id} ({name})")
        
        all_teams[league] = teams

print(f"\n\nConfiguration Python:")
print("LEAGUES_CONFIG = {")
for league, teams in all_teams.items():
    print(f"    '{league}': {{")
    print(f"        'teams': {{")
    for slug, team_id in teams.items():
        print(f"            '{slug}': {team_id},")
    print(f"        }}")
    print(f"    }},")
print("}")