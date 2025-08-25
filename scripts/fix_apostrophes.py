#!/usr/bin/env python3
"""
Script pour corriger les apostrophes qui cassent la syntaxe JavaScript/TypeScript
"""

import os
import re

def fix_apostrophes_in_file(filepath):
    """Corrige les apostrophes dans un fichier TypeScript"""
    if not os.path.exists(filepath):
        return False
    
    print(f"Fixing apostrophes in: {filepath}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Compter les apostrophes problématiques
    apostrophe_count = content.count("'")
    
    if apostrophe_count == 0:
        print(f"  No apostrophes found")
        return False
    
    print(f"  Found {apostrophe_count} apostrophes")
    
    # Remplacer toutes les apostrophes par des échappements ou des alternatives
    # Option 1: Échapper les apostrophes
    fixed_content = content.replace("'", "\\'")
    
    # Option 2: Alternative - remplacer par un caractère similaire
    # fixed_content = content.replace("'", "'")  # Apostrophe typographique
    
    # Sauvegarder
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(fixed_content)
    
    print(f"  Fixed all apostrophes")
    return True

def main():
    print("=== CORRECTION DES APOSTROPHES ===\n")
    
    ts_files = [
        'data/ligue1Teams.ts',
        'data/premierLeagueTeams.ts', 
        'data/ligaTeams.ts',
        'data/serieATeams.ts',
        'data/bundesligaTeams.ts'
    ]
    
    fixed_count = 0
    
    for filepath in ts_files:
        if fix_apostrophes_in_file(filepath):
            fixed_count += 1
    
    print(f"\n=== RESUME ===")
    print(f"Files with apostrophes fixed: {fixed_count}/{len(ts_files)}")
    
    if fixed_count > 0:
        print("\nLes apostrophes ont été échappées.")
        print("Redémarrer le serveur Next.js et tester:")
        print("  http://localhost:3002/ligue1")
        print("  http://localhost:3002/ligue1/lyon")

if __name__ == "__main__":
    main()