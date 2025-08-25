#!/usr/bin/env python3
"""
Script pour mettre à jour les données de l'OM dans ligue1Teams.ts
avec les données complètes récupérées depuis l'API Sportmonks
"""

import json
import re
from typing import Dict, List, Any

def load_om_data() -> Dict:
    """Charge les données de l'OM depuis le fichier JSON"""
    with open('om_complete_squad_final.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def format_position(position: str) -> str:
    """Convertit la position API vers le format utilisé dans l'app"""
    position_mapping = {
        'Goalkeeper': 'GK',
        'Defender': 'DF', 
        'Midfielder': 'MF',
        'Attacker': 'FW'
    }
    return position_mapping.get(position, position)

def get_position_id(position: str) -> int:
    """Retourne l'ID de position selon le mapping existant"""
    position_id_mapping = {
        'GK': 24,
        'Goalkeeper': 24,
        'DF': 25,
        'Defender': 25,
        'MF': 26, 
        'Midfielder': 26,
        'FW': 27,
        'Attacker': 27
    }
    return position_id_mapping.get(position, 26)

def convert_to_typescript_format(om_data: Dict) -> str:
    """Convertit les données JSON en format TypeScript pour ligue1Teams.ts"""
    
    players = om_data['players']
    
    # Récupérer les numéros de maillot depuis les données existantes
    jersey_mapping = {
        537332: 22,    # Timothy Weah
        29328428: 14,  # Igor Paixão
        32390: 6,      # Ulisses Garcia
        335521: 32,    # Facundo Medina
        20333643: 10,  # Mason Greenwood
        37657133: 24,  # François Mughe
        433458: 9,     # Amine Gouiri
        95776: 7,      # Neal Maupay
        28575687: 4,   # CJ Egan-Riley
        37369302: 18,  # Bamo Meïté
        608285: 8,     # Angel Gomes
        37593233: 40,  # Jelle Van Neck
        13171199: 5,   # Leonardo Balerdi
        586846: 13,    # Derek Cornelius
        186456: 36,    # Rubén Blanco
        95694: 25,     # Adrien Rabiot
        37737405: 50,  # Darryl Bakola
        527759: 92,    # Théo Vermot
        130063: 29,    # Pol Lirola
        512560: 62,    # Amir Murillo
        37541144: 26,  # Bilal Nadir
        31739: 97,     # Pierre-Emerick Aubameyang
        186418: 1,     # Gerónimo Rulli
        29186: 12,     # Jeffrey de Lange
        96691: 11,     # Amine Harit
        95696: 19,     # Geoffrey Kondogbia
        1744: 23,      # Pierre-Emile Højbjerg
    }
    
    ts_players = []
    
    for player in players:
        # Données de base
        player_id = player['id']
        display_name = player['display_name']
        position = format_position(player['position'])
        position_id = get_position_id(player['position'])
        jersey = jersey_mapping.get(player_id)
        age = player['age']
        nationality = player['nationality'] or 'Unknown'
        height = player['height']
        weight = player['weight']
        image_path = player['image_path']
        slug = player['slug']
        
        # Format TypeScript
        ts_player = f"""      {{
        id: {player_id},
        nom: "{display_name}",
        displayName: "{display_name}",
        position: "{position}",
        position_id: {position_id},
        numero: {jersey if jersey else 'null'},
        age: "{age}",
        nationalite: "{nationality}",
        taille: {height if height else 'null'},
        poids: {weight if weight else 'null'},
        image: "{image_path}",
        playerSlug: "{slug}"
      }}"""
        
        ts_players.append(ts_player)
    
    # Construire l'objet OM complet
    om_object = f"""  {{
    id: 44,
    name: "Olympique Marseille",
    slug: "marseille",
    players: [
{',\\n'.join(ts_players)}
    ]
  }}"""
    
    return om_object

def update_ligue1_teams_file(new_om_data: str):
    """Met à jour le fichier ligue1Teams.ts avec les nouvelles données de l'OM"""
    
    # Lire le fichier existant
    with open('data/ligue1Teams.ts', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Trouver et remplacer la section OM
    # Pattern pour matcher l'objet OM complet
    pattern = r'(\s*{\s*id:\s*44,\s*name:\s*"Olympique Marseille",.*?players:\s*\[.*?\]\s*})'
    
    # Utiliser une approche plus robuste : trouver le début et la fin
    start_pattern = r'(\s*{\s*id:\s*44,\s*name:\s*"Olympique Marseille")'
    
    lines = content.split('\n')
    start_line = -1
    end_line = -1
    brace_count = 0
    found_start = False
    
    for i, line in enumerate(lines):
        if re.search(start_pattern, line) and not found_start:
            start_line = i
            found_start = True
            brace_count = 0
        
        if found_start:
            # Compter les accolades ouvertes et fermées
            brace_count += line.count('{') - line.count('}')
            if brace_count == 0 and i > start_line:
                end_line = i
                break
    
    if start_line != -1 and end_line != -1:
        # Remplacer les lignes
        new_lines = lines[:start_line] + new_om_data.split('\n') + lines[end_line + 1:]
        new_content = '\n'.join(new_lines)
        
        # Sauvegarder le fichier
        with open('data/ligue1Teams.ts', 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"✓ Fichier ligue1Teams.ts mis à jour !")
        print(f"  - OM remplacé des lignes {start_line} à {end_line}")
        print(f"  - {len(new_om_data.split('\\n'))} nouvelles lignes ajoutées")
        
        return True
    else:
        print("✗ Impossible de trouver la section OM dans ligue1Teams.ts")
        return False

def main():
    print("=== Mise à jour des données de l'OM ===\n")
    
    # 1. Charger les données de l'OM
    print("1. Chargement des données de l'OM...")
    om_data = load_om_data()
    print(f"✓ {om_data['successful_players']} joueurs chargés")
    
    # 2. Convertir au format TypeScript
    print("\\n2. Conversion au format TypeScript...")
    ts_data = convert_to_typescript_format(om_data)
    print(f"✓ Données converties ({len(ts_data.split('\\n'))} lignes)")
    
    # 3. Sauvegarder dans un fichier temporaire pour vérification
    print("\\n3. Sauvegarde temporaire...")
    with open('om_data_typescript.ts', 'w', encoding='utf-8') as f:
        f.write(ts_data)
    print("✓ Sauvegardé dans om_data_typescript.ts")
    
    # 4. Mettre à jour ligue1Teams.ts
    print("\\n4. Mise à jour de ligue1Teams.ts...")
    success = update_ligue1_teams_file(ts_data)
    
    if success:
        print("\\n=== SUCCÈS ===")
        print("L'effectif de l'OM a été mis à jour avec les données complètes !")
        print("\\nDonnées mises à jour :")
        print("- display_name (nom d'affichage)")
        print("- image_path (photos des joueurs)")
        print("- age (âges calculés)")
        print("- height/taille (tailles en cm)")
        print("- nationality (nationalités sportives)")
        print("- position (positions)")
        print("- jersey_number/numero (numéros de maillot)")
    else:
        print("\\n=== ÉCHEC ===")
        print("Impossible de mettre à jour le fichier ligue1Teams.ts")
        print("Vérifiez le fichier om_data_typescript.ts et copiez manuellement")

if __name__ == "__main__":
    main()