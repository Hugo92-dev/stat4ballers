#!/usr/bin/env python3
"""
Vérifier que tous les slugs correspondent entre les fichiers teams et teamDetails
"""

import re
from pathlib import Path

data_dir = Path(__file__).parent.parent / 'data'

# Extraire les slugs depuis les fichiers teams
def get_slugs_from_teams():
    all_slugs = {}
    
    files = {
        'ligue1': 'ligue1Teams.ts',
        'premier-league': 'premierLeagueTeams.ts',
        'la-liga': 'ligaTeams.ts',
        'serie-a': 'serieATeams.ts',
        'bundesliga': 'bundesligaTeams.ts'
    }
    
    for league, filename in files.items():
        filepath = data_dir / filename
        if filepath.exists():
            content = filepath.read_text(encoding='utf-8')
            
            # Extraire les slugs
            slug_pattern = r'slug:\s*"([^"]+)"'
            slugs = re.findall(slug_pattern, content)
            
            all_slugs[league] = slugs
            print(f"\n{league}: {len(slugs)} équipes")
            for slug in slugs:
                print(f"  - {slug}")
    
    return all_slugs

# Extraire les slugs depuis teamDetails.ts
def get_slugs_from_details():
    filepath = data_dir / 'teamDetails.ts'
    if filepath.exists():
        content = filepath.read_text(encoding='utf-8')
        
        # Extraire les slugs (clés de l'objet)
        slug_pattern = r"'([^']+)':\s*\{"
        slugs = re.findall(slug_pattern, content)
        
        return set(slugs)
    return set()

# Comparer
teams_slugs = get_slugs_from_teams()
details_slugs = get_slugs_from_details()

print("\n" + "="*50)
print("SLUGS MANQUANTS DANS teamDetails.ts:")
print("="*50)

for league, slugs in teams_slugs.items():
    missing = [s for s in slugs if s not in details_slugs]
    if missing:
        print(f"\n{league}:")
        for slug in missing:
            print(f"  ❌ {slug}")

print("\n" + "="*50)
print("SLUGS EN TROP DANS teamDetails.ts:")
print("="*50)

all_teams_slugs = set()
for slugs in teams_slugs.values():
    all_teams_slugs.update(slugs)

extra = details_slugs - all_teams_slugs
if extra:
    for slug in sorted(extra):
        print(f"  ⚠️ {slug}")