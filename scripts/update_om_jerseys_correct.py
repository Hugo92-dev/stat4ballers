#!/usr/bin/env python3
"""
Script avec les VRAIS numéros de maillot OM depuis l'API
Basé sur jersey_number de la saison actuelle
"""

import json
import re

# VRAIS numéros depuis l'API (jersey_number)
REAL_JERSEY_NUMBERS = {
    # GARDIENS
    186418: 1,      # Gerónimo Rulli
    29186: 12,      # Jeffrey de Lange
    186456: 13,     # Rubén Blanco
    37593233: 40,   # Jelle Van Neck
    527759: 92,     # Théo Vermot (PAS 30 mais 92!)
    
    # DÉFENSEURS  
    13171199: 5,    # Leonardo Balerdi
    32390: 6,       # Ulisses Garcia
    586846: 13,     # Derek Cornelius
    37369302: 18,   # Bamo Meïté
    130063: 29,     # Pol Lirola
    335521: 32,     # Facundo Medina (PAS 3 mais 32!)
    28575687: 56,   # CJ Egan-Riley (PAS 4 mais 56!)
    512560: 62,     # Amir Murillo
    
    # MILIEUX
    1744: 5,        # Pierre-Emile Højbjerg (partage le 5 avec Balerdi)
    21803033: 8,    # Azzedine Ounahi
    96691: 11,      # Amine Harit
    95696: 19,      # Geoffrey Kondogbia
    95694: 25,      # Adrien Rabiot
    37541144: 34,   # Bilal Nadir (PAS 77 mais 34!)
    608285: 47,     # Angel Gomes
    37737405: 50,   # Darryl Bakola
    
    # ATTAQUANTS
    433458: 9,      # Amine Gouiri
    31739: 9,       # Pierre-Emerick Aubameyang (partage le 9 avec Gouiri)
    20333643: 11,   # Mason Greenwood (partage le 11 avec Harit)
    95776: 13,      # Neal Maupay (partage le 13 avec Cornelius et Blanco)
    20315925: 14,   # Faris Moumbagna
    29328428: 14,   # Igor Paixão (partage le 14 avec Moumbagna)
    537332: 22,     # Timothy Weah
    37657133: 24,   # François Mughe
    34455209: 27,   # Jonathan Rowe
    37713942: 33,   # Robinio Vaz (PAS 34 mais 33!)
    37729567: 48,   # Keyliane Abdallah
}

def update_typescript_file():
    """Met à jour le fichier TypeScript avec les VRAIS numéros"""
    
    file_path = 'data/ligue1Teams_updated_om.ts'
    
    # Lire le fichier
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    updates_made = []
    current_player_id = None
    current_player_name = None
    
    # Parcourir ligne par ligne
    for i, line in enumerate(lines):
        # Détecter l'ID du joueur
        if 'id:' in line:
            match = re.search(r'id:\s*(\d+)', line)
            if match:
                current_player_id = int(match.group(1))
        
        # Détecter le nom du joueur
        if 'nom:' in line and current_player_id:
            match = re.search(r'nom:\s*"([^"]+)"', line)
            if match:
                current_player_name = match.group(1)
        
        # Mettre à jour le numéro si nécessaire
        if 'numero:' in line and current_player_id in REAL_JERSEY_NUMBERS:
            new_number = REAL_JERSEY_NUMBERS[current_player_id]
            old_line = lines[i]
            
            # Extraire l'ancien numéro pour voir si on doit mettre à jour
            old_match = re.search(r'numero:\s*(\d+)', old_line)
            if old_match:
                old_number = int(old_match.group(1))
                if old_number != new_number:
                    new_line = re.sub(r'numero:\s*\d+', f'numero: {new_number}', old_line)
                    lines[i] = new_line
                    updates_made.append(f"{current_player_name}: {old_number} → #{new_number}")
    
    # Écrire le fichier mis à jour
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    return updates_made

def main():
    print("=== Correction des VRAIS numéros de maillot OM ===")
    print("Basé sur jersey_number de l'API\n")
    
    # Effectuer les mises à jour
    updates = update_typescript_file()
    
    if updates:
        print("Corrections effectuées:")
        for update in sorted(updates):
            print(f"  ✓ {update}")
        print(f"\nTotal: {len(updates)} numéros corrigés")
    else:
        print("Tous les numéros sont déjà corrects!")
    
    # Afficher les points importants
    print("\n=== Points importants ===")
    print("• Vermot: #92 (PAS #30)")
    print("• Egan-Riley: #56 (PAS #4)")
    print("• Medina: #32 (PAS #3)")
    print("• Nadir: #34 (PAS #77)")
    print("• Robinio Vaz: #33 (PAS #34)")
    print("\nNote: Certains joueurs partagent le même numéro (ex: #9, #11, #13, #14)")
    print("\nFichier mis à jour avec les VRAIS numéros!")

if __name__ == "__main__":
    main()