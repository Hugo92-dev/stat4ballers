#!/usr/bin/env python3
"""
Applique les VRAIS numéros de maillot de la saison 25651
"""

import re

# Numéros récupérés depuis l'API pour la saison 25651
JERSEY_NUMBERS_SEASON_25651 = {
    186418: 1,      # Gerónimo Rulli
    28575687: 4,    # CJ Egan-Riley  
    13171199: 5,    # Leonardo Balerdi
    32390: 6,       # Ulisses Garcia
    95776: 7,       # Neal Maupay
    608285: 8,      # Angel Gomes (PAS 47!)
    433458: 9,      # Amine Gouiri
    20333643: 10,   # Mason Greenwood
    96691: 11,      # Amine Harit
    29186: 12,      # Jeffrey de Lange
    586846: 13,     # Derek Cornelius
    29328428: 14,   # Igor Paixão
    34455209: 17,   # Jonathan Rowe (PAS 27!)
    37369302: 18,   # Bamo Meïté
    95696: 19,      # Geoffrey Kondogbia
    537332: 22,     # Timothy Weah
    1744: 23,       # Pierre-Emile Højbjerg
    37657133: 24,   # François Mughe
    95694: 25,      # Adrien Rabiot
    37541144: 26,   # Bilal Nadir (PAS 34!)
    130063: 29,     # Pol Lirola
    335521: 32,     # Facundo Medina
    37713942: 34,   # Robinio Vaz
    186456: 36,     # Rubén Blanco (PAS 16!)
    37593233: 40,   # Jelle Van Neck
    37729567: 48,   # Keyliane Abdallah
    37737405: 50,   # Darryl Bakola
    512560: 62,     # Amir Murillo
    527759: 92,     # Théo Vermot
    31739: 97,      # Pierre-Emerick Aubameyang (PAS 9!)
    # Note: Ounahi (21803033) et Moumbagna (20315925) non trouvés dans l'API
}

def update_file():
    """Met à jour le fichier avec les numéros corrects"""
    
    file_path = 'data/ligue1Teams_updated_om.ts'
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    updates_made = []
    
    for player_id, correct_jersey in JERSEY_NUMBERS_SEASON_25651.items():
        # Chercher le pattern pour ce joueur
        pattern = f'id: {player_id},[^}}]*?numero: (\\d+|null)'
        
        match = re.search(pattern, content, re.DOTALL)
        if match:
            current_jersey = match.group(1)
            
            if current_jersey != str(correct_jersey):
                # Remplacer uniquement pour ce joueur spécifique
                old_pattern = f'id: {player_id},[^}}]*?numero: {current_jersey}'
                new_pattern = match.group(0).replace(f'numero: {current_jersey}', f'numero: {correct_jersey}')
                
                content_before = content
                content = content.replace(match.group(0), new_pattern, 1)
                
                if content != content_before:
                    # Trouver le nom du joueur pour le log
                    name_match = re.search(f'id: {player_id},[^}}]*?nom: "([^"]+)"', content, re.DOTALL)
                    player_name = name_match.group(1) if name_match else f"ID {player_id}"
                    
                    updates_made.append(f"{player_name}: #{current_jersey} → #{correct_jersey}")
    
    # Sauvegarder
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return updates_made

def main():
    print("=== Application des numéros de la saison 25651 ===\n")
    
    updates = update_file()
    
    if updates:
        print("Corrections effectuées:")
        for update in sorted(updates):
            print(f"  ✓ {update}")
        print(f"\nTotal: {len(updates)} numéros corrigés")
    else:
        print("Tous les numéros sont déjà corrects!")
    
    print("\n=== Points clés ===")
    print("• Aubameyang: #97 (confirmé)")
    print("• Egan-Riley: #4")
    print("• Angel Gomes: #8")
    print("• Bilal Nadir: #26")
    print("• Jonathan Rowe: #17")
    print("• Rubén Blanco: #36")

if __name__ == "__main__":
    main()