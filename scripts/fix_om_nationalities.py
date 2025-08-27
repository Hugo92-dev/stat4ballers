#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import re
import sys
import os

# Forcer l'encodage UTF-8 pour Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'replace')

def fix_om_nationalities():
    """Corrige les nationalités Unknown pour l'OM en utilisant les données du fichier JSON source"""
    
    # Chemins des fichiers
    json_path = os.path.join(os.path.dirname(__file__), "../data/ligue1_2025_2026/marseille.json")
    ts_path = os.path.join(os.path.dirname(__file__), "../data/ligue1Teams.ts")
    
    # Lire les données JSON source de l'OM
    with open(json_path, 'r', encoding='utf-8') as f:
        om_data = json.load(f)
    
    # Créer un dictionnaire des nationalités par ID de joueur
    nationalities_map = {}
    for player in om_data['players']:
        player_id = player.get('id')
        nationality = player.get('nationality', 'Unknown')
        display_name = player.get('display_name', '')
        nationalities_map[player_id] = (display_name, nationality)
    
    # Lire le fichier ligue1Teams.ts
    with open(ts_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    corrections_made = []
    
    # Pour chaque joueur de l'OM, mettre à jour sa nationalité
    for player_id, (display_name, nationality) in nationalities_map.items():
        # Chercher le pattern pour ce joueur dans la section OM
        # Pattern: id: 186418, ... nationalite: "Unknown"
        pattern = rf'(id:\s*{player_id},.*?nationalite:\s*)"Unknown"'
        
        def replace_nationality(match):
            corrections_made.append(f"{display_name}: {nationality}")
            return match.group(1) + f'"{nationality}"'
        
        # Remplacer la nationalité
        new_content = re.sub(pattern, replace_nationality, content, count=1, flags=re.DOTALL)
        if new_content != content:
            content = new_content
    
    # Écrire le fichier modifié
    with open(ts_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("=" * 60)
    print("MISE À JOUR DES NATIONALITÉS POUR L'OM")
    print("=" * 60)
    
    if corrections_made:
        print(f"\n✅ {len(corrections_made)} nationalité(s) mise(s) à jour:")
        for correction in sorted(corrections_made):
            print(f"   - {correction}")
    else:
        print("\n✅ Aucune mise à jour nécessaire")
    
    print("\n✅ Fichier ligue1Teams.ts mis à jour avec succès!")

if __name__ == "__main__":
    fix_om_nationalities()