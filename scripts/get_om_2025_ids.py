import requests
import sys

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

def get_om_squad_2025():
    """Récupérer l'effectif de l'OM pour la saison 2025/2026"""
    
    print("=== EFFECTIF OM SAISON 2025/2026 ===\n")
    
    # Récupérer l'effectif par l'endpoint squads/seasons
    url = f"{BASE_URL}/squads/seasons/{LIGUE1_SEASON_ID}/teams/{OM_TEAM_ID}"
    params = {
        'api_token': API_TOKEN,
        'include': 'player'
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json().get('data', [])
        print(f"✅ {len(data)} joueurs trouvés\n")
        
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
                    print(f"  • #{jersey:>2} {best_name:<30} ID: {player_id}")
                    
                    # Créer la clé pour le mapping
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
        
        print("\n=== MAPPING TYPESCRIPT ===\n")
        print("export function getOMPlayerIds(): Record<string, number> {")
        print("  return {")
        
        for key, value in sorted(player_mapping.items()):
            print(f"    '{key}': {value},")
        
        print("  };")
        print("}")
        
        return player_mapping
    else:
        print(f"❌ Erreur {response.status_code}")
        
        # Essayer une autre approche
        print("\nEssai avec l'endpoint transfers...\n")
        
        # Récupérer les transferts récents vers l'OM
        url = f"{BASE_URL}/transfers"
        params = {
            'api_token': API_TOKEN,
            'filters': f'team_in_id:{OM_TEAM_ID}',
            'include': 'player',
            'per_page': 50
        }
        
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json().get('data', [])
            print(f"Transferts récents vers l'OM: {len(data)} trouvés\n")
            
            for transfer in data[:10]:  # Afficher les 10 derniers
                if 'player' in transfer:
                    player = transfer['player']
                    print(f"  • {player.get('display_name', player.get('name', 'N/A'))} - ID: {player.get('id')}")

if __name__ == "__main__":
    get_om_squad_2025()