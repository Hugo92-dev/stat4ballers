import requests
import sys
import json

# Forcer l'encodage UTF-8 pour Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

API_TOKEN = 'leBzDfKbRE5k9zEg3FuZE3Hh7XbukODNarOXLoVtPAiAtliDZ19wLu1Wnzi2'
BASE_URL = 'https://api.sportmonks.com/v3/football'

# ID de l'Olympique de Marseille
OM_TEAM_ID = 85

def search_players_by_name():
    """Chercher les joueurs de l'OM par leur nom"""
    
    print("=== RECHERCHE DES JOUEURS ACTUELS DE L'OM ===\n")
    
    # Liste des joueurs actuels de l'OM (depuis nos données)
    om_players = [
        "Geronimo Rulli",
        "Jeffrey de Lange",
        "Simon Ngapandouetnbu",
        "Leonardo Balerdi",
        "Derek Cornelius",
        "Lilian Brassier",
        "Murillo",
        "Pol Lirola",
        "Quentin Merlin",
        "Amir Murillo",
        "Ulisses Garcia",
        "Michael Murillo",
        "Luis Henrique",
        "Geoffrey Kondogbia",
        "Pierre-Emile Hojbjerg",
        "Adrien Rabiot",
        "Valentin Rongier",
        "Bilal Nadir",
        "Ismael Bennacer",
        "Azzedine Ounahi",
        "Jonathan Rowe",
        "Valentin Carboni",
        "Luis Henrique",
        "Mason Greenwood",
        "Amine Harit",
        "Elye Wahi",
        "Pierre-Emerick Aubameyang",
        "Neal Maupay",
        "Bamo Meite"
    ]
    
    player_mapping = {}
    
    for player_name in om_players:
        print(f"\nRecherche de: {player_name}")
        
        # Rechercher le joueur
        url = f"{BASE_URL}/players"
        params = {
            'api_token': API_TOKEN,
            'filters': f'search:{player_name}',
            'per_page': 5
        }
        
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json().get('data', [])
            
            if data:
                # Prendre le premier résultat
                player = data[0]
                player_id = player.get('id')
                display_name = player.get('display_name', '')
                name = player.get('name', '')
                
                best_name = display_name or name
                
                # Créer la clé
                clean_name = best_name.replace(' ', '')
                clean_name = clean_name.replace('-', '')
                clean_name = clean_name.replace("'", '')
                clean_name = clean_name.replace(".", '')
                clean_name = clean_name.replace("ø", 'o')
                clean_name = clean_name.replace("Ø", 'O')
                
                # Normaliser les accents
                import unicodedata
                clean_name = unicodedata.normalize('NFD', clean_name)
                clean_name = ''.join(c for c in clean_name if unicodedata.category(c) != 'Mn')
                
                player_mapping[clean_name] = player_id
                
                print(f"  ✅ Trouvé: {best_name} (ID: {player_id})")
                print(f"     Clé: {clean_name}")
            else:
                print(f"  ❌ Non trouvé")
    
    print("\n=== MAPPING TYPESCRIPT ===\n")
    print("export function getOMPlayerIds(): Record<string, number> {")
    print("  return {")
    
    for key, value in sorted(player_mapping.items()):
        print(f"    '{key}': {value},")
    
    print("  };")
    print("}")
    
    return player_mapping

if __name__ == "__main__":
    search_players_by_name()