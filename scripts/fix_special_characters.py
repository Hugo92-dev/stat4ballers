#!/usr/bin/env python3
"""
Script pour corriger tous les caractères spéciaux dans les fichiers TypeScript
"""

import os
import re
from unidecode import unidecode

def clean_string_for_ts(text):
    """Nettoie une chaîne pour TypeScript"""
    # Remplacer les accents par des équivalents ASCII
    clean_text = unidecode(text)
    # Garder seulement les caractères alphanumériques, espaces, traits d'union
    clean_text = re.sub(r'[^\w\s-]', '', clean_text)
    return clean_text

def fix_typescript_file(filepath):
    """Corrige les caractères spéciaux dans un fichier TypeScript"""
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return False
    
    print(f"Fixing: {filepath}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Sauvegarder l'original
    backup_path = filepath + '.backup'
    with open(backup_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  Backup created: {backup_path}")
    
    lines = content.split('\n')
    fixed_lines = []
    changes_made = 0
    
    for line in lines:
        original_line = line
        
        # Corriger les playerSlug avec accents
        if 'playerSlug:' in line:
            # Extraire le slug entre guillemets
            match = re.search(r'playerSlug: "([^"]*)"', line)
            if match:
                old_slug = match.group(1)
                new_slug = clean_string_for_ts(old_slug.lower().replace(' ', '-'))
                if old_slug != new_slug:
                    line = line.replace(f'playerSlug: "{old_slug}"', f'playerSlug: "{new_slug}"')
                    changes_made += 1
        
        # Note: On garde les noms avec accents pour l'affichage, mais on nettoie les slugs
        fixed_lines.append(line)
    
    if changes_made > 0:
        # Réécrire le fichier
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(fixed_lines))
        print(f"  Fixed {changes_made} player slugs")
        return True
    else:
        # Supprimer le backup si aucun changement
        os.remove(backup_path)
        print(f"  No changes needed")
        return False

def main():
    print("=== CORRECTION DES CARACTERES SPECIAUX ===\n")
    
    # Fichiers TypeScript à corriger
    ts_files = [
        'data/ligue1Teams.ts',
        'data/premierLeagueTeams.ts',
        'data/ligaTeams.ts',
        'data/serieATeams.ts',
        'data/bundesligaTeams.ts'
    ]
    
    total_fixed = 0
    
    for filepath in ts_files:
        if fix_typescript_file(filepath):
            total_fixed += 1
    
    print(f"\n=== RESUME ===")
    print(f"Files fixed: {total_fixed}/{len(ts_files)}")
    
    if total_fixed > 0:
        print("\nLes fichiers ont été corrigés. Testez maintenant:")
        print("  http://localhost:3000/ligue1")
        print("  http://localhost:3000/ligue1/lyon")
        print("  http://localhost:3000/ligue1/paris-saint-germain")

if __name__ == "__main__":
    # Installer unidecode si nécessaire
    try:
        from unidecode import unidecode
    except ImportError:
        print("Installing unidecode...")
        os.system("pip install unidecode")
        from unidecode import unidecode
    
    main()