#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import json
import sys
import time

# Forcer l'encodage UTF-8 pour Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'replace')

API_KEY = "j28l04KZC0LGFAdbxIzdyb8zz253K1YegT5vEUN5taw0dxuNr6U3jtRMmS6C"
BASE_URL = "https://api.sportmonks.com/v3/football"

def get_detailed_player_info(player_id, player_name):
    """Récupère toutes les infos détaillées d'un joueur"""
    print(f"\n{'='*50}")
    print(f"🔍 ANALYSE DÉTAILLÉE - {player_name} (ID: {player_id})")
    print("="*50)
    
    url = f"{BASE_URL}/players/{player_id}"
    params = {'api_token': API_KEY}
    
    try:
        response = requests.get(url, params=params)
        print(f"Status code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if 'data' in data:
                player_data = data['data']
                
                # Afficher toutes les infos importantes
                print(f"Name: {player_data.get('name', 'N/A')}")
                print(f"Display name: {player_data.get('display_name', 'N/A')}")
                print(f"Common name: {player_data.get('common_name', 'N/A')}")
                print(f"Country ID: {player_data.get('country_id', 'N/A')}")
                print(f"Nationality ID: {player_data.get('nationality_id', 'N/A')}")
                
                # Récupérer les noms des pays
                country_id = player_data.get('country_id')
                nationality_id = player_data.get('nationality_id')
                
                if country_id:
                    country_name = get_country_name(country_id)
                    print(f"Pays de naissance: {country_name} (ID: {country_id})")
                
                if nationality_id:
                    nationality_name = get_country_name(nationality_id)
                    print(f"Nationalité sportive: {nationality_name} (ID: {nationality_id})")
                
                print(f"Position ID: {player_data.get('position_id', 'N/A')}")
                print(f"Date de naissance: {player_data.get('date_of_birth', 'N/A')}")
                print(f"Taille: {player_data.get('height', 'N/A')} cm")
                print(f"Poids: {player_data.get('weight', 'N/A')} kg")
                
                return player_data
            else:
                print("❌ Pas de données trouvées")
        else:
            print(f"❌ Erreur API: {response.status_code}")
            if response.status_code == 429:
                print("⏳ Rate limit atteint")
                
    except Exception as e:
        print(f"❌ Exception: {e}")
    
    return None

def get_country_name(country_id):
    """Récupère le nom d'un pays par son ID"""
    url = f"{BASE_URL}/countries/{country_id}"
    params = {'api_token': API_KEY}
    
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            if 'data' in data:
                return data['data'].get('name', 'Unknown')
    except Exception as e:
        print(f"Erreur récupération pays {country_id}: {e}")
    
    return f"Unknown (ID: {country_id})"

def main():
    print("="*60)
    print("🔍 DEBUG DES NATIONALITÉS SPORTIVES - JOUEURS OM")
    print("="*60)
    
    # Joueurs problématiques mentionnés
    players_to_check = [
        (31739, "Pierre-Emerick Aubameyang"),  # Gabon selon vous
        (34455209, "Jonathan Rowe"),           # Angleterre selon vous  
        (20333643, "Mason Greenwood"),        # Angleterre selon vous
        (433458, "Amine Gouiri"),             # Algérie - celui qui marche
    ]
    
    print("Vérification des joueurs problématiques...")
    
    for player_id, player_name in players_to_check:
        player_data = get_detailed_player_info(player_id, player_name)
        time.sleep(1)  # Pause pour éviter le rate limiting
    
    print(f"\n{'='*60}")
    print("✅ ANALYSE TERMINÉE")
    print("="*60)

if __name__ == "__main__":
    main()