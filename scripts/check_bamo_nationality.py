#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import json
import sys

# Forcer l'encodage UTF-8 pour Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'replace')

API_KEY = "j28l04KZC0LGFAdbxIzdyb8zz253K1YegT5vEUN5taw0dxuNr6U3jtRMmS6C"
BASE_URL = "https://api.sportmonks.com/v3/football"

def check_player_nationality(player_id, player_name):
    """Vérifie la nationalité sportive d'un joueur"""
    url = f"{BASE_URL}/players/{player_id}"
    params = {
        'api_token': API_KEY,
        'include': 'nationality'
    }
    
    try:
        print(f"Vérification de {player_name} (ID: {player_id})...")
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            print(f"Réponse complète: {json.dumps(data, indent=2, ensure_ascii=False)}")
            
            if 'data' in data:
                player_data = data['data']
                
                # Afficher les infos du joueur
                print(f"\n✅ Joueur trouvé: {player_data.get('common_name', player_data.get('display_name'))}")
                print(f"   Date de naissance: {player_data.get('date_of_birth')}")
                print(f"   Country ID: {player_data.get('country_id')}")
                print(f"   Nationality ID: {player_data.get('nationality_id')}")
                
                # Vérifier la nationalité incluse
                if 'nationality' in player_data and player_data['nationality']:
                    nationality = player_data['nationality']
                    print(f"\n🏳️ Nationalité sportive détectée:")
                    print(f"   Nom: {nationality.get('name')}")
                    print(f"   ID: {nationality.get('id')}")
                else:
                    print("\n❌ Pas de nationalité incluse dans la réponse")
        else:
            print(f"❌ Erreur {response.status_code}: {response.text}")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")

# Vérifier Bamo Meïté
print("=" * 60)
check_player_nationality(37369302, "Bamo Meïté")

# Vérifier aussi quelques autres joueurs de l'OM pour comparaison
print("\n" + "=" * 60)
check_player_nationality(433458, "Amine Gouiri")  # Devrait être Algérie

print("\n" + "=" * 60)
check_player_nationality(32390, "Ulisses Garcia")  # Devrait être Suisse