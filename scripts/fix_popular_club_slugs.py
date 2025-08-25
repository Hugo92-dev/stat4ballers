#!/usr/bin/env python3
"""
Script pour corriger les slugs des clubs populaires pour des URLs plus conviviales
"""

import os
import json

def fix_popular_slugs():
    print("=== CORRECTION DES SLUGS DES CLUBS POPULAIRES ===\n")
    
    # Corrections pour des URLs plus conviviales
    slug_corrections = {
        # Bundesliga
        'data/bundesliga_2025_2026/bayern-munchen.json': {
            'new_filename': 'bayern-munich.json',
            'new_slug': 'bayern-munich'
        },
        
        # Liga  
        'data/liga_2025_2026/fc-barcelona.json': {
            'new_filename': 'barcelona.json', 
            'new_slug': 'barcelona'
        }
    }
    
    corrections_made = []
    
    for old_path, correction in slug_corrections.items():
        if os.path.exists(old_path):
            directory = os.path.dirname(old_path)
            new_path = os.path.join(directory, correction['new_filename'])
            
            print(f"Fixing: {os.path.basename(old_path)} -> {correction['new_filename']}")
            
            # Lire et modifier le contenu
            with open(old_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            data['slug'] = correction['new_slug']
            
            # Écrire le nouveau fichier
            with open(new_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            # Supprimer l'ancien
            os.remove(old_path)
            
            corrections_made.append({
                'old_filename': os.path.basename(old_path),
                'new_filename': correction['new_filename'],
                'new_slug': correction['new_slug']
            })
    
    # Mettre à jour les fichiers TypeScript
    if corrections_made:
        print(f"\n=== MISE A JOUR DES FICHIERS TYPESCRIPT ===\n")
        
        ts_corrections = {
            'data/bundesligaTeams.ts': {
                'bayern-munchen': 'bayern-munich'
            },
            'data/ligaTeams.ts': {
                'fc-barcelona': 'barcelona'
            }
        }
        
        for ts_file, slug_map in ts_corrections.items():
            if os.path.exists(ts_file):
                print(f"Updating {ts_file}...")
                
                with open(ts_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                updated = False
                for old_slug, new_slug in slug_map.items():
                    if f'slug: "{old_slug}"' in content:
                        content = content.replace(f'slug: "{old_slug}"', f'slug: "{new_slug}"')
                        print(f"  Fixed slug: {old_slug} -> {new_slug}")
                        updated = True
                
                if updated:
                    with open(ts_file, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"  Updated successfully")
    
    return corrections_made

def create_url_alias_mappings(corrections_made):
    """Crée les mappings d'alias pour les URLs"""
    print(f"\n=== URL ALIASES A AJOUTER ===\n")
    
    # Suggestions d'alias à ajouter dans les pages
    aliases = {
        'bayern-munich': ['bayern-munchen', 'bayern', 'fcb'],
        'barcelona': ['fc-barcelona', 'barca', 'fcb-liga'],
        'atletico-madrid': ['atletico', 'atleti'],
        'deportivo-alaves': ['alaves'],
        'brighton-hove-albion': ['brighton']
    }
    
    print("Ajouter ces alias dans les pages [club]/page.tsx:")
    print("const slugAliases: Record<string, string> = {")
    for main_slug, alias_list in aliases.items():
        for alias in alias_list:
            print(f"  '{alias}': '{main_slug}',")
    print("};")

def main():
    corrections = fix_popular_slugs()
    
    if corrections:
        print(f"\n{len(corrections)} corrections effectuees:")
        for correction in corrections:
            print(f"  - {correction['old_filename']} -> {correction['new_filename']}")
        
        create_url_alias_mappings(corrections)
        
        print(f"\n=== NOUVELLES URLS A TESTER ===")
        print("Bundesliga:")
        print("  http://localhost:3000/bundesliga/bayern-munich")
        print("Liga:")  
        print("  http://localhost:3000/liga/barcelona")
        print("  http://localhost:3000/liga/atletico-madrid")
        print("  http://localhost:3000/liga/deportivo-alaves")
        print("Premier League:")
        print("  http://localhost:3000/premier-league/brighton-hove-albion")
        
    else:
        print("Aucune correction necessaire")

if __name__ == "__main__":
    main()