#!/usr/bin/env python3

import json

def main():
    # Charger les données
    with open('om_complete_squad_final.json', 'r', encoding='utf-8') as f:
        om_data = json.load(f)
    
    players = om_data['players']
    
    # Numéros de maillot connus
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
    
    # Conversion des positions
    def format_position(pos):
        mapping = {
            'Goalkeeper': 'GK',
            'Defender': 'DF', 
            'Midfielder': 'MF',
            'Attacker': 'FW'
        }
        return mapping.get(pos, pos)
    
    def get_position_id(pos):
        mapping = {
            'Goalkeeper': 24,
            'Defender': 25,
            'Midfielder': 26,
            'Attacker': 27
        }
        return mapping.get(pos, 26)
    
    # Générer le TypeScript
    ts_content = """  {
    id: 44,
    name: "Olympique Marseille",
    slug: "marseille",
    players: [
"""
    
    for i, player in enumerate(players):
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
        
        comma = "," if i < len(players) - 1 else ""
        
        ts_content += f"""      {{
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
      }}{comma}
"""
    
    ts_content += """    ]
  }"""
    
    # Sauvegarder
    with open('om_updated_data.txt', 'w', encoding='utf-8') as f:
        f.write(ts_content)
    
    print("TypeScript data generated in om_updated_data.txt")
    print(f"Players processed: {len(players)}")

if __name__ == "__main__":
    main()