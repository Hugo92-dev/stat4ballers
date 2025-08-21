#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import sys

# Forcer l'encodage UTF-8 pour Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'replace')

# Corrections manuelles pour les joueurs dont l'API SportMonks a des données incorrectes
# Ces joueurs jouent réellement pour ces équipes nationales
MANUAL_CORRECTIONS = {
    37369302: "Côte d'Ivoire",  # Bamo Meïté - joue pour la Côte d'Ivoire, pas la France
}

def fix_om_nationalities():
    """Corrige les nationalités sportives incorrectes pour l'OM"""
    
    # Lire le fichier
    file_path = "../data/ligue1Teams.ts"
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    corrections_made = []
    
    for player_id, correct_nationality in MANUAL_CORRECTIONS.items():
        # Chercher le joueur par son ID
        pattern = rf'(id:\s*{player_id},.*?nationality:\s*")[^"]+(")'
        
        def replace_nationality(match):
            corrections_made.append(f"Player ID {player_id}: {correct_nationality}")
            return match.group(1) + correct_nationality + match.group(2)
        
        # Remplacer la nationalité
        content = re.sub(pattern, replace_nationality, content, flags=re.DOTALL)
    
    # Écrire le fichier mis à jour
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("=" * 60)
    print("CORRECTIONS DES NATIONALITÉS POUR L'OM")
    print("=" * 60)
    
    if corrections_made:
        print(f"\n✅ {len(corrections_made)} correction(s) appliquée(s):")
        for correction in corrections_made:
            print(f"   - {correction}")
    else:
        print("\n✅ Aucune correction nécessaire")
    
    print("\n✅ Fichier ligue1Teams.ts mis à jour avec succès!")

if __name__ == "__main__":
    fix_om_nationalities()