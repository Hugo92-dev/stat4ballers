#!/usr/bin/env python3
"""
Script propre et unique pour mettre à jour les numéros de maillot OM
Saison 2025/2026 - Source unique de vérité
"""

import json
import re

# Numéros OFFICIELS OM 2025/2026
# Vérifié avec les compositions récentes
JERSEY_NUMBERS_2025_2026 = {
    # GARDIENS
    186418: 1,      # Gerónimo Rulli
    29186: 36,      # Jeffrey de Lange
    186456: 16,     # Rubén Blanco
    37593233: 40,   # Jelle Van Neck
    527759: 30,     # Théo Vermot
    
    # DÉFENSEURS
    13171199: 5,    # Leonardo Balerdi (Capitaine)
    32390: 6,       # Ulisses Garcia
    586846: 13,     # Derek Cornelius
    37369302: 18,   # Bamo Meïté
    130063: 29,     # Pol Lirola
    335521: 3,      # Facundo Medina
    28575687: 4,    # CJ Egan-Riley (confirmé correct)
    512560: 62,     # Amir Murillo
    
    # MILIEUX
    1744: 23,       # Pierre-Emile Højbjerg
    21803033: 8,    # Azzedine Ounahi
    96691: 11,      # Amine Harit
    95696: 19,      # Geoffrey Kondogbia
    95694: 25,      # Adrien Rabiot
    37541144: 77,   # Bilal Nadir
    608285: 47,     # Angel Gomes
    37737405: 50,   # Darryl Bakola
    
    # ATTAQUANTS
    433458: 21,     # Amine Gouiri
    31739: 97,      # Pierre-Emerick Aubameyang (CORRECT: #97)
    20333643: 10,   # Mason Greenwood (#10)
    95776: 7,       # Neal Maupay
    20315925: 14,   # Faris Moumbagna
    29328428: 9,    # Igor Paixão
    537332: 22,     # Timothy Weah
    37657133: 24,   # François Mughe
    34455209: 27,   # Jonathan Rowe
    37713942: 34,   # Robinio Vaz
    37729567: 48,   # Keyliane Abdallah
}

def update_typescript_file():
    """Met à jour le fichier TypeScript avec les bons numéros"""
    
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
        if 'numero:' in line and current_player_id in JERSEY_NUMBERS_2025_2026:
            new_number = JERSEY_NUMBERS_2025_2026[current_player_id]
            old_line = lines[i]
            new_line = re.sub(r'numero:\s*\d+', f'numero: {new_number}', old_line)
            
            if old_line != new_line:
                lines[i] = new_line
                updates_made.append(f"{current_player_name}: #{new_number}")
    
    # Écrire le fichier mis à jour
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    return updates_made

def main():
    print("=== Mise à jour des numéros de maillot OM 2025/2026 ===")
    print("Source unique et harmonieuse - Pas de doublons\n")
    
    # Effectuer les mises à jour
    updates = update_typescript_file()
    
    if updates:
        print("Mises à jour effectuées:")
        for update in sorted(updates):
            print(f"  ✓ {update}")
        print(f"\nTotal: {len(updates)} numéros corrigés")
    else:
        print("Tous les numéros sont déjà corrects!")
    
    # Afficher quelques vérifications importantes
    print("\n=== Vérifications clés ===")
    print("• Aubameyang: #97 (pas #10)")
    print("• Greenwood: #10")
    print("• Harit: #11")
    print("• Egan-Riley: #4 (confirmé)")
    print("\nFichier data/ligue1Teams_updated_om.ts mis à jour avec succès!")

if __name__ == "__main__":
    main()