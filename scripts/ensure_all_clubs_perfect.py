#!/usr/bin/env python3
"""
S'assurer que TOUS les clubs ont les mêmes infos complètes que Marseille
"""

import os
import re
import shutil
from pathlib import Path

data_dir = Path(__file__).parent.parent / 'data'
public_dir = Path(__file__).parent.parent / 'public'

# Mapping des slugs problématiques
slug_mappings = {
    'west-ham-united': 'West Ham United.png',
    'afc-bournemouth': 'AFC Bournemouth.png',
    'brighton-hove-albion': 'Brighton & Hove Albion.png',
}

def ensure_logo_files():
    """S'assurer que tous les logos sont accessibles avec les bons noms"""
    leagues = ['ligue1', 'premier-league', 'liga', 'serie-a', 'bundesliga']
    
    for league in leagues:
        logo_dir = public_dir / 'logos' / 'clubs' / league
        
        if not logo_dir.exists():
            continue
            
        # Pour chaque fichier de logo existant
        for logo_file in logo_dir.glob('*.png'):
            # Si c'est un fichier avec espace
            if ' ' in logo_file.name:
                # Créer une copie avec le nom slugifié
                slug_name = logo_file.name.lower().replace(' ', '-').replace('&', 'and')
                slug_path = logo_dir / slug_name
                
                if not slug_path.exists():
                    print(f"Créer copie: {logo_file.name} -> {slug_name}")
                    shutil.copy2(logo_file, slug_path)

def check_all_clubs():
    """Vérifier que tous les clubs ont les infos complètes"""
    
    # Lire teamDetails.ts
    team_details_path = data_dir / 'teamDetails.ts'
    team_details_content = team_details_path.read_text(encoding='utf-8')
    
    # Extraire tous les clubs avec leurs détails
    details_pattern = r"'([^']+)':\s*\{([^}]+)\}"
    matches = re.findall(details_pattern, team_details_content, re.DOTALL)
    
    print(f"Total: {len(matches)} clubs dans teamDetails")
    
    missing_info = []
    
    for slug, details in matches:
        has_stadium = 'stadium:' in details
        has_capacity = 'capacity:' in details
        has_founded = 'founded:' in details
        
        if not (has_stadium and has_capacity and has_founded):
            missing = []
            if not has_stadium:
                missing.append('stadium')
            if not has_capacity:
                missing.append('capacity')
            if not has_founded:
                missing.append('founded')
            missing_info.append(f"{slug}: manque {', '.join(missing)}")
    
    if missing_info:
        print(f"\nPROBLEMES: {len(missing_info)} clubs avec infos manquantes:")
        for info in missing_info:
            print(f"  - {info}")
    else:
        print("\nPARFAIT! Tous les clubs ont stade, capacité et année de fondation!")
    
    return len(missing_info) == 0

if __name__ == "__main__":
    print("="*50)
    print("VERIFICATION ET CORRECTION DES CLUBS")
    print("="*50)
    
    print("\n1. Créer les copies de logos pour les slugs...")
    ensure_logo_files()
    
    print("\n2. Vérifier que tous les clubs ont les infos complètes...")
    all_good = check_all_clubs()
    
    if all_good:
        print("\n✅ TOUS LES CLUBS SONT PARFAITS!")
    else:
        print("\n⚠️ Des corrections sont nécessaires")