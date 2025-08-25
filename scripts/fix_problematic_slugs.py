#!/usr/bin/env python3
"""
Script pour corriger les slugs problématiques avec accents et caractères spéciaux
"""

import os
import json
import shutil

def fix_slugs():
    print("=== CORRECTION DES SLUGS PROBLEMATIQUES ===\n")
    
    # Mapping des corrections nécessaires
    corrections = {
        # Liga
        'data/liga_2025_2026/atlético-madrid.json': 'atletico-madrid.json',
        'data/liga_2025_2026/deportivo-alavés.json': 'deportivo-alaves.json',
        
        # Premier League  
        'data/premier-league_2025_2026/brighton-&-hove-albion.json': 'brighton-hove-albion.json'
    }
    
    files_updated = []
    
    for old_path, new_filename in corrections.items():
        if os.path.exists(old_path):
            directory = os.path.dirname(old_path)
            new_path = os.path.join(directory, new_filename)
            
            print(f"Renaming: {os.path.basename(old_path)} -> {new_filename}")
            
            # Lire le contenu du fichier
            with open(old_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Corriger le slug dans le contenu
            new_slug = new_filename.replace('.json', '')
            data['slug'] = new_slug
            
            # Écrire le nouveau fichier
            with open(new_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            # Supprimer l'ancien fichier
            os.remove(old_path)
            
            files_updated.append({
                'old': os.path.basename(old_path),
                'new': new_filename,
                'slug': new_slug
            })
    
    return files_updated

def update_typescript_files(corrections):
    """Met à jour les fichiers TypeScript avec les nouveaux slugs"""
    
    print("\n=== MISE A JOUR DES FICHIERS TYPESCRIPT ===\n")
    
    # Mapping des fichiers TS et leurs corrections
    ts_updates = {
        'data/ligaTeams.ts': {
            'atlético-madrid': 'atletico-madrid',
            'deportivo-alavés': 'deportivo-alaves'
        },
        'data/premierLeagueTeams.ts': {
            'brighton-&-hove-albion': 'brighton-hove-albion'
        }
    }
    
    for ts_file, slug_corrections in ts_updates.items():
        if os.path.exists(ts_file):
            print(f"Updating {ts_file}...")
            
            with open(ts_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Appliquer les corrections
            updated = False
            for old_slug, new_slug in slug_corrections.items():
                if f'slug: "{old_slug}"' in content:
                    content = content.replace(f'slug: "{old_slug}"', f'slug: "{new_slug}"')
                    print(f"  Fixed: {old_slug} -> {new_slug}")
                    updated = True
            
            if updated:
                with open(ts_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"  Updated {ts_file} ✅")
        else:
            print(f"  Missing: {ts_file} ❌")

def main():
    # 1. Corriger les fichiers JSON
    corrections = fix_slugs()
    
    if corrections:
        print(f"\n{len(corrections)} fichiers corrigés:")
        for correction in corrections:
            print(f"  - {correction['old']} -> {correction['new']} (slug: {correction['slug']})")
        
        # 2. Mettre à jour les fichiers TypeScript
        update_typescript_files(corrections)
        
        print(f"\n=== PAGES A TESTER MAINTENANT ===")
        print("Liga:")
        print("  http://localhost:3000/liga/atletico-madrid (était atlético-madrid)")
        print("  http://localhost:3000/liga/deportivo-alaves (était deportivo-alavés)")
        print("Premier League:")
        print("  http://localhost:3000/premier-league/brighton-hove-albion (était brighton-&-hove-albion)")
        
    else:
        print("Aucun fichier à corriger trouvé")

if __name__ == "__main__":
    main()