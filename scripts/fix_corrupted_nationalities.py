#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import sys

# Forcer l'encodage UTF-8 pour Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'replace')

def fix_corrupted_nationalities():
    """Corrige les nationalités corrompues (Angleterre'Ivoire)"""
    
    print("="*60)
    print("🔧 CORRECTION DES NATIONALITÉS CORROMPUES")
    print("="*60)
    
    try:
        with open('data/ligue1Teams.ts', 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ Erreur lecture: {e}")
        return
    
    original_content = content
    
    # Corriger "Angleterre'Ivoire" en "Angleterre"
    content = content.replace("Angleterre'Ivoire", "Angleterre")
    
    # Vérifier les changements
    changes_made = original_content != content
    
    if changes_made:
        # Compter les corrections
        corrections = original_content.count("Angleterre'Ivoire")
        
        print(f"✅ {corrections} corrections appliquées:")
        print("   • Angleterre'Ivoire → Angleterre")
        
        # Sauvegarder
        try:
            with open('data/ligue1Teams.ts', 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"💾 Fichier sauvegardé")
        except Exception as e:
            print(f"❌ Erreur sauvegarde: {e}")
    else:
        print("✅ Aucune corruption trouvée")

def main():
    fix_corrupted_nationalities()

if __name__ == "__main__":
    main()