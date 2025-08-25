#!/usr/bin/env python3
"""
Script pour corriger les espaces en fin de nom des joueurs
"""

import json
import os
import re

def fix_trailing_spaces_in_json(filepath):
    """Corrige les espaces en fin dans un fichier JSON"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Corriger les espaces dans display_name
        content = re.sub(r'"display_name":\s*"([^"]+)\s+"', r'"display_name": "\1"', content)
        
        # Corriger les espaces dans nom
        content = re.sub(r'"nom":\s*"([^"]+)\s+"', r'"nom": "\1"', content)
        
        # Corriger les espaces dans displayName
        content = re.sub(r'"displayName":\s*"([^"]+)\s+"', r'"displayName": "\1"', content)
        
        # Corriger les espaces dans name
        content = re.sub(r'"name":\s*"([^"]+)\s+"', r'"name": "\1"', content)
        
        # Corriger les espaces dans fullName
        content = re.sub(r'"fullName":\s*"([^"]+)\s+"', r'"fullName": "\1"', content)
        
        # Corriger les espaces dans playerSlug
        content = re.sub(r'"playerSlug":\s*"([^"]+)\s+"', r'"playerSlug": "\1"', content)
        content = re.sub(r'"slug":\s*"([^"]+)\s+"', r'"slug": "\1"', content)
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
    except Exception as e:
        print(f"Erreur avec {filepath}: {e}")
        return False

def fix_trailing_spaces_in_ts(filepath):
    """Corrige les espaces en fin dans un fichier TypeScript"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Corriger les espaces dans nom
        content = re.sub(r'nom:\s*"([^"]+)\s+"', r'nom: "\1"', content)
        
        # Corriger les espaces dans displayName
        content = re.sub(r'displayName:\s*"([^"]+)\s+"', r'displayName: "\1"', content)
        
        # Corriger les espaces dans playerSlug
        content = re.sub(r'playerSlug:\s*"([^"]+)\s+"', r'playerSlug: "\1"', content)
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
    except Exception as e:
        print(f"Erreur avec {filepath}: {e}")
        return False

def main():
    print("=== CORRECTION DES ESPACES EN FIN DE NOM ===\n")
    
    data_folder = "C:\\Users\\hugo\\stat4ballers\\data"
    
    # Corriger les fichiers JSON
    leagues = ['ligue1', 'premier-league', 'liga', 'serie-a', 'bundesliga']
    
    total_fixed = 0
    
    for league in leagues:
        league_folder = os.path.join(data_folder, f"{league}_2025_2026")
        if os.path.exists(league_folder):
            print(f"Traitement de {league}...")
            for filename in os.listdir(league_folder):
                if filename.endswith('.json'):
                    filepath = os.path.join(league_folder, filename)
                    if fix_trailing_spaces_in_json(filepath):
                        print(f"  [OK] {filename}")
                        total_fixed += 1
    
    # Corriger les fichiers TypeScript
    ts_files = [
        'ligue1Teams.ts',
        'premierLeagueTeams.ts',
        'ligaTeams.ts',
        'serieATeams.ts',
        'bundesligaTeams.ts',
        'playerSearchData.ts',
        'la-ligaPlayersCompleteStats.ts',
        'bundesligaPlayersCompleteStats.ts',
        'serie-aPlayersCompleteStats.ts',
        'premier-leaguePlayersCompleteStats.ts',
        'ligue1PlayersCompleteStats.ts'
    ]
    
    print("\nTraitement des fichiers TypeScript...")
    for filename in ts_files:
        filepath = os.path.join(data_folder, filename)
        if os.path.exists(filepath):
            if fix_trailing_spaces_in_ts(filepath):
                print(f"  [OK] {filename}")
                total_fixed += 1
    
    print(f"\n=== RÉSUMÉ ===")
    print(f"Total de fichiers corrigés: {total_fixed}")
    print("\nLes espaces en fin de nom ont été supprimés.")
    print("Redémarrer le serveur Next.js si nécessaire.")

if __name__ == "__main__":
    main()