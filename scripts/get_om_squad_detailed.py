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
LIGUE1_SEASON_ID = 25651  # Saison 2025/2026

def get_om_squad_detailed():
    """Récupérer l'effectif détaillé de l'OM pour la saison actuelle"""
    
    print("=== RÉCUPÉRATION DÉTAILLÉE DES JOUEURS DE L'OM ===\n")
    
    # Essayer avec l'endpoint des squads
    url = f"{BASE_URL}/squads/teams/{OM_TEAM_ID}/current"
    params = {
        'api_token': API_TOKEN,
        'include': 'player'
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json().get('data', [])
        print(f"✅ {len(data)} joueurs trouvés via squads endpoint\n")
        
        player_mapping = {}
        
        for entry in data:
            if 'player' in entry:
                player = entry['player']
                player_id = player.get('id')
                display_name = player.get('display_name', '')
                name = player.get('name', '')
                common_name = player.get('common_name', '')
                jersey = entry.get('jersey_number', '?')
                
                # Utiliser le meilleur nom disponible
                best_name = display_name or name or common_name
                
                if best_name:
                    # Nettoyer le nom pour créer une clé
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
                    
                    position = player.get('position', {}).get('name', 'N/A') if isinstance(player.get('position'), dict) else 'N/A'
                    print(f"  • {best_name} (#{jersey}) - {position}")
                    print(f"    ID: {player_id} | Clé: {clean_name}")
        
        if player_mapping:
            print("\n=== MAPPING TYPESCRIPT ===\n")
            print("export function getOMPlayerIds(): Record<string, number> {")
            print("  return {")
            
            for key, value in sorted(player_mapping.items()):
                print(f"    '{key}': {value},")
            
            print("  };")
            print("}")
        
        return player_mapping
    else:
        print(f"❌ Erreur avec squads endpoint: {response.status_code}")
    
    # Essayer un autre endpoint
    print("\nEssai avec l'endpoint des joueurs par équipe...\n")
    
    url = f"{BASE_URL}/players"
    params = {
        'api_token': API_TOKEN,
        'filters': f'team_ids:{OM_TEAM_ID}',
        'per_page': 100
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json().get('data', [])
        print(f"✅ {len(data)} joueurs trouvés\n")
        
        player_mapping = {}
        
        for player in data:
            player_id = player.get('id')
            display_name = player.get('display_name', '')
            name = player.get('name', '')
            common_name = player.get('common_name', '')
            
            # Utiliser le meilleur nom disponible
            best_name = display_name or name or common_name
            
            if best_name:
                # Nettoyer le nom
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
                
                print(f"  • {best_name}")
                print(f"    ID: {player_id} | Clé: {clean_name}")
        
        if player_mapping:
            print("\n=== MAPPING TYPESCRIPT ===\n")
            print("export function getOMPlayerIds(): Record<string, number> {")
            print("  return {")
            
            for key, value in sorted(player_mapping.items()):
                print(f"    '{key}': {value},")
            
            print("  };")
            print("}")
        
        return player_mapping
    else:
        print(f"❌ Erreur: {response.status_code}")
        return {}

if __name__ == "__main__":
    get_om_squad_detailed()