#!/usr/bin/env python3
"""
Script pour mettre à jour les numéros de maillot de l'OM 
basé sur l'effectif officiel 2025/2026
"""

import json

# Numéros officiels OM saison 2025/2026
# Source: Site officiel OM et compositions récentes
OM_JERSEY_NUMBERS = {
    # GARDIENS
    186418: 1,     # Gerónimo Rulli
    29186: 36,     # Jeffrey de Lange  
    186456: 16,    # Rubén Blanco
    37593233: 40,  # Jelle Van Neck
    527759: 30,    # Théo Vermot
    
    # DÉFENSEURS
    13171199: 5,   # Leonardo Balerdi (Capitaine)
    32390: 6,      # Ulisses Garcia
    586846: 13,    # Derek Cornelius
    37369302: 18,  # Bamo Meïté
    130063: 29,    # Pol Lirola
    335521: 3,     # Facundo Medina
    28575687: 4,   # CJ Egan-Riley
    512560: 62,    # Amir Murillo
    
    # MILIEUX
    1744: 23,      # Pierre-Emile Højbjerg
    21803033: 8,   # Azzedine Ounahi
    96691: 11,     # Amine Harit
    95696: 19,     # Geoffrey Kondogbia
    95694: 25,     # Adrien Rabiot
    37541144: 77,  # Bilal Nadir
    608285: 47,    # Angel Gomes
    37737405: 50,  # Darryl Bakola
    
    # ATTAQUANTS  
    433458: 21,    # Amine Gouiri
    31739: 10,     # Pierre-Emerick Aubameyang
    20333643: 11,  # Mason Greenwood (partage le 11 avec Harit)
    95776: 7,      # Neal Maupay
    20315925: 14,  # Faris Moumbagna
    29328428: 9,   # Igor Paixão
    537332: 22,    # Timothy Weah
    37657133: 24,  # François Mughe
    34455209: 27,  # Jonathan Rowe
    37713942: 34,  # Robinio Vaz
    37729567: 48,  # Keyliane Abdallah
}

def main():
    print("=== Mise à jour des numéros de maillot OM 2025/2026 ===\n")
    
    # Charger le fichier TypeScript actuel
    with open('data/ligue1Teams_updated_om.ts', 'r', encoding='utf-8') as f:
        content = f.read()
    
    updates_made = []
    
    # Pour chaque joueur, mettre à jour son numéro
    for player_id, jersey_number in OM_JERSEY_NUMBERS.items():
        # Chercher le joueur dans le fichier
        search_str = f"id: {player_id},"
        
        if search_str in content:
            # Trouver la position du joueur
            start_idx = content.find(search_str)
            # Trouver le prochain "numero:" après cette position
            numero_idx = content.find("numero:", start_idx)
            
            if numero_idx != -1 and numero_idx < start_idx + 500:  # Dans les 500 caractères suivants
                # Trouver la fin de la ligne numero
                line_end = content.find(",", numero_idx)
                
                if line_end != -1:
                    old_line = content[numero_idx:line_end]
                    new_line = f"numero: {jersey_number}"
                    
                    # Remplacer seulement si différent
                    if old_line != new_line:
                        # Extraire le nom du joueur pour le log
                        nom_idx = content.rfind("nom:", start_idx - 200, start_idx)
                        if nom_idx != -1:
                            nom_end = content.find('",', nom_idx)
                            if nom_end != -1:
                                player_name = content[nom_idx + 6:nom_end]
                                updates_made.append(f"{player_name}: #{jersey_number}")
                        
                        content = content[:numero_idx] + new_line + content[line_end:]
    
    # Sauvegarder le fichier mis à jour
    with open('data/ligue1Teams_updated_om.ts', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("Mises à jour effectuées:")
    for update in sorted(updates_made):
        print(f"  ✓ {update}")
    
    print(f"\nTotal: {len(updates_made)} numéros mis à jour")
    print("Fichier data/ligue1Teams_updated_om.ts mis à jour avec succès!")

if __name__ == "__main__":
    main()