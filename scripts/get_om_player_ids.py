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

def get_om_squad():
    """Récupérer l'effectif actuel de l'OM depuis l'API"""
    
    print("=== RÉCUPÉRATION DES IDS SPORTMONKS DES JOUEURS DE L'OM ===\n")
    
    # Récupérer l'équipe avec les joueurs
    url = f"{BASE_URL}/teams/{OM_TEAM_ID}"
    params = {
        'api_token': API_TOKEN,
        'include': 'players'
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        print(f"❌ Erreur API: {response.status_code}")
        return {}
    
    data = response.json()['data']
    
    if 'players' not in data:
        print("❌ Pas de joueurs trouvés")
        return {}
    
    players = data['players']
    print(f"✅ {len(players)} joueurs trouvés dans l'effectif de l'OM\n")
    
    # Créer le mapping nom -> ID
    player_mapping = {}
    
    for player in players:
        player_id = player.get('id')
        display_name = player.get('display_name', '')
        name = player.get('name', '')
        
        # Nettoyer le nom pour créer une clé
        # Supprimer les espaces, accents, caractères spéciaux
        clean_name = display_name or name
        clean_name = clean_name.replace(' ', '')
        clean_name = clean_name.replace('-', '')
        clean_name = clean_name.replace("'", '')
        clean_name = clean_name.replace(".", '')
        clean_name = clean_name.replace("ø", 'o')
        clean_name = clean_name.replace("Ø", 'O')
        clean_name = clean_name.replace("é", 'e')
        clean_name = clean_name.replace("è", 'e')
        clean_name = clean_name.replace("ë", 'e')
        clean_name = clean_name.replace("á", 'a')
        clean_name = clean_name.replace("à", 'a')
        clean_name = clean_name.replace("ï", 'i')
        clean_name = clean_name.replace("í", 'i')
        clean_name = clean_name.replace("ñ", 'n')
        clean_name = clean_name.replace("ç", 'c')
        clean_name = clean_name.replace("ü", 'u')
        clean_name = clean_name.replace("ú", 'u')
        clean_name = clean_name.replace("ó", 'o')
        clean_name = clean_name.replace("ö", 'o')
        
        player_mapping[clean_name] = player_id
        
        # Afficher l'info
        position = player.get('position', {}).get('name', 'N/A') if player.get('position') else 'N/A'
        print(f"  • {display_name or name} (#{player.get('jersey_number', '?')}) - {position}")
        print(f"    ID: {player_id} | Clé: {clean_name}")
    
    print("\n=== MAPPING TYPESCRIPT ===\n")
    print("export function getOMPlayerIds(): Record<string, number> {")
    print("  return {")
    
    for key, value in sorted(player_mapping.items()):
        print(f"    '{key}': {value},")
    
    print("  };")
    print("}")
    
    return player_mapping

if __name__ == "__main__":
    get_om_squad()