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

def get_raw_player_data(player_id, player_name):
    """Récupère les données brutes complètes d'un joueur"""
    print(f"\n{'='*60}")
    print(f"🔍 DONNÉES BRUTES - {player_name} (ID: {player_id})")
    print("="*60)
    
    url = f"{BASE_URL}/players/{player_id}"
    params = {'api_token': API_KEY}
    
    try:
        response = requests.get(url, params=params)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            # Afficher la réponse JSON complète pour debug
            print("📄 RÉPONSE JSON COMPLÈTE:")
            print(json.dumps(data, indent=2, ensure_ascii=False))
            
            return data
        else:
            print(f"❌ Erreur API: {response.status_code}")
            try:
                error_data = response.json()
                print(f"Détails: {json.dumps(error_data, indent=2)}")
            except:
                print(f"Contenu: {response.text}")
                
    except Exception as e:
        print(f"❌ Exception: {e}")
    
    return None

def main():
    print("="*60)
    print("🔍 ANALYSE DES DONNÉES BRUTES - JOUEURS OM PROBLÉMATIQUES")
    print("="*60)
    
    # Joueurs problématiques selon vous
    players_to_check = [
        (28575687, "C. Egan Riley"),     # Actuellement: Côte d'Ivoire
        (32390, "U. Garcia Lopes"),      # Actuellement: Portugal
        (586846, "D. Cornelius"),        # Actuellement: Sénégal
    ]
    
    for player_id, player_name in players_to_check:
        get_raw_player_data(player_id, player_name)
        time.sleep(1)  # Pause pour éviter le rate limiting
    
    print(f"\n{'='*60}")
    print("✅ ANALYSE TERMINÉE")
    print("="*60)

if __name__ == "__main__":
    main()