#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import sys

# Forcer l'encodage UTF-8 pour Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'replace')

def fix_om_nationalities():
    """Corrige manuellement les nationalités des joueurs de l'OM selon vos indications"""
    
    print("="*60)
    print("🔧 CORRECTION MANUELLE DES NATIONALITÉS OM")
    print("="*60)
    
    # Corrections à apporter selon vos informations
    corrections = [
        # Corrections des erreurs précédentes
        {
            'id': 31739,  # Pierre-Emerick Aubameyang
            'name': 'P. Aubameyang',
            'current': 'France',
            'correct': 'Gabon'
        },
        {
            'id': 34455209,  # Jonathan Rowe
            'name': 'J. Rowe', 
            'current': 'Côte d\'Ivoire',  # Erreur du script précédent
            'correct': 'Angleterre'
        },
        {
            'id': 20333643,  # Mason Greenwood
            'name': 'M. Greenwood',
            'current': 'Côte d\'Ivoire',  # Erreur du script précédent
            'correct': 'Angleterre'
        },
        # Garder la correction qui était bonne
        {
            'id': 433458,  # Amine Gouiri
            'name': 'A. Gouiri',
            'current': 'France',
            'correct': 'Algérie'  # Cette correction était bonne
        }
    ]
    
    # Lire le fichier
    try:
        with open('data/ligue1Teams.ts', 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ Erreur lecture fichier: {e}")
        return
    
    original_content = content
    corrections_applied = 0
    
    for correction in corrections:
        print(f"\n🔧 {correction['name']} (ID: {correction['id']})")
        print(f"   {correction['current']} → {correction['correct']}")
        
        # Pattern pour trouver le joueur spécifique
        pattern = rf'(\{{[^}}]*id:\s*{correction["id"]}[^}}]*nationality:\s*["\']){re.escape(correction["current"])}(["\'][^}}]*\}})'
        replacement = rf'\g<1>{correction["correct"]}\g<2>'
        
        new_content = re.sub(pattern, replacement, content)
        
        if new_content != content:
            print(f"   ✅ Correction appliquée")
            content = new_content
            corrections_applied += 1
        else:
            print(f"   ❌ Impossible de trouver le pattern")
            # Essayer de trouver le joueur pour debug
            debug_pattern = rf'id:\s*{correction["id"]}'
            if re.search(debug_pattern, content):
                print(f"   🔍 Joueur trouvé mais pattern nationalité non matché")
            else:
                print(f"   🔍 Joueur avec ID {correction['id']} non trouvé")
    
    # Sauvegarder si des corrections ont été appliquées
    if corrections_applied > 0:
        try:
            with open('data/ligue1Teams.ts', 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"\n💾 {corrections_applied}/{len(corrections)} corrections sauvegardées")
        except Exception as e:
            print(f"❌ Erreur sauvegarde: {e}")
    else:
        print(f"\n❌ Aucune correction appliquée")
    
    print(f"\n{'='*60}")
    print("✅ CORRECTION MANUELLE TERMINÉE")
    print("="*60)

def main():
    fix_om_nationalities()

if __name__ == "__main__":
    main()