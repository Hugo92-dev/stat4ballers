import json
import requests
import time
from dotenv import load_dotenv
import os
import sys

# Fix pour l'encodage UTF-8 sur Windows
sys.stdout.reconfigure(encoding='utf-8')

# Charger les variables d'environnement depuis le fichier à la racine
load_dotenv('../.env.local')
API_KEY = os.getenv('SPORTMONKS_API_TOKEN')

if not API_KEY:
    print("Cle API SportMonks manquante dans .env.local")
    exit(1)

BASE_URL = "https://api.sportmonks.com/v3/football"
HEADERS = {
    'Authorization': f'Bearer {API_KEY}'
}

def get_player_with_photo(player_id):
    """Récupère les informations du joueur avec son URL de photo"""
    try:
        url = f"{BASE_URL}/players/{player_id}"
        params = {
            'include': 'nationality'  # On garde la nationalité au cas où
        }
        
        response = requests.get(url, headers=HEADERS, params=params)
        
        if response.status_code == 200:
            data = response.json()
            if 'data' in data:
                player_data = data['data']
                # L'URL de la photo est dans image_path
                return player_data.get('image_path', None)
        elif response.status_code == 429:
            print("Rate limit atteint, pause de 60 secondes...")
            time.sleep(60)
            return get_player_with_photo(player_id)
        else:
            print(f"Erreur API pour joueur {player_id}: {response.status_code}")
            return None
    except Exception as e:
        print(f"Erreur pour joueur {player_id}: {e}")
        return None

def update_om_photos():
    """Met à jour les URLs des photos pour tous les joueurs de l'OM"""
    
    # Charger les données actuelles
    with open('../data/ligue1Teams.ts', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Importer le module pour accéder aux données
    import sys
    sys.path.append('..')
    
    # On va plutôt lire directement le fichier et extraire l'OM
    print("Recuperation des photos des joueurs de l'OM...")
    
    # Trouver la section OM dans le fichier
    om_start = content.find('name: "Olympique de Marseille"')
    if om_start == -1:
        print("OM non trouve dans le fichier")
        return
    
    # Trouver les joueurs de l'OM
    players_start = content.find('players: [', om_start)
    players_end = content.find(']', players_start)
    
    if players_start == -1 or players_end == -1:
        print("Joueurs de l'OM non trouves")
        return
    
    # Extraire et parser les joueurs
    players_section = content[players_start:players_end+1]
    
    # Compter les joueurs pour avoir une idée  
    # Chercher soit 'id:' soit 'playerId:'
    player_count = players_section.count('id:')
    print(f"{player_count} joueurs trouves pour l'OM")
    
    # On va créer un mapping playerId -> imageUrl
    photo_updates = {}
    updated_count = 0
    
    # Extraire tous les playerIds
    import re
    # Chercher les patterns 'id: <number>' (en évitant l'id de l'équipe)
    # On cherche après players: [ pour éviter l'id de l'équipe
    player_ids = re.findall(r'id:\s*(\d+)', players_section)
    
    for i, player_id in enumerate(player_ids, 1):
        print(f"  [{i}/{len(player_ids)}] Récupération photo joueur {player_id}...", end='')
        
        image_url = get_player_with_photo(player_id)
        
        if image_url:
            photo_updates[player_id] = image_url
            updated_count += 1
            print(f" OK - Photo trouvee")
        else:
            print(f" Pas de photo")
        
        # Pause pour respecter le rate limit
        time.sleep(0.5)
    
    print(f"\n{updated_count}/{len(player_ids)} photos recuperees")
    
    # Maintenant, mettre à jour le fichier avec les URLs des photos
    new_content = content
    
    for player_id, image_url in photo_updates.items():
        # Trouver le joueur dans le contenu
        player_pattern = f'id: {player_id},'
        player_pos = new_content.find(player_pattern)
        
        if player_pos != -1:
            # S'assurer qu'on est bien dans la section des joueurs
            if new_content.rfind('players: [', 0, player_pos) > new_content.rfind(']', 0, player_pos):
                # Trouver la fin de cet objet joueur
                next_brace = new_content.find('}', player_pos)
                
                # Vérifier si image existe déjà
                image_check = new_content[player_pos:next_brace]
                
                if 'image:' in image_check:
                    # Remplacer l'image existante
                    old_image_start = image_check.find('image:')
                    old_image_line_start = player_pos + old_image_start
                    old_image_end = new_content.find('\n', old_image_line_start)
                    old_image_full = new_content[old_image_line_start:old_image_end]
                    
                    new_content = new_content.replace(
                        old_image_full,
                        f'image: "{image_url}"'
                    )
                    print(f"  Photo mise a jour pour joueur {player_id}")
                else:
                    # Ajouter image avant la fermeture de l'objet
                    insertion_point = next_brace
                    new_content = (
                        new_content[:insertion_point] + 
                        f',\n        image: "{image_url}"' + 
                        new_content[insertion_point:]
                    )
                    print(f"  Photo ajoutee pour joueur {player_id}")
    
    # Sauvegarder le fichier mis à jour
    with open('../data/ligue1Teams.ts', 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"\nFichier ligue1Teams.ts mis a jour avec {updated_count} photos")
    
    # Créer un fichier de rapport
    with open('om_photos_report.json', 'w', encoding='utf-8') as f:
        json.dump({
            'total_players': len(player_ids),
            'photos_found': updated_count,
            'missing_photos': len(player_ids) - updated_count,
            'photo_urls': photo_updates
        }, f, indent=2, ensure_ascii=False)
    
    print("Rapport sauvegarde dans om_photos_report.json")

if __name__ == "__main__":
    print("Demarrage de la recuperation des photos de l'OM...")
    update_om_photos()
    print("Termine !")