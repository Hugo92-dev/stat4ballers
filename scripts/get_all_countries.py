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

def get_all_countries():
    """Récupère tous les pays disponibles via l'API"""
    print("="*60)
    print("🌍 RÉCUPÉRATION DE TOUS LES PAYS")
    print("="*60)
    
    url = f"{BASE_URL}/countries"
    params = {'api_token': API_KEY}
    
    try:
        response = requests.get(url, params=params)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            # Afficher quelques pays pour comprendre la structure
            if 'data' in data and len(data['data']) > 0:
                print(f"✅ {len(data['data'])} pays trouvés")
                
                print("\n📋 Premiers pays (structure):")
                for i, country in enumerate(data['data'][:5]):
                    print(f"  {i+1}. {country}")
                
                # Créer un mapping des IDs qu'on recherche
                target_ids = [17, 44, 462, 614, 1424, 38, 1004, 5, 1247, 3483, 320, 593, 32, 556, 65437, 3662]
                
                print(f"\n🎯 MAPPING DES IDs RECHERCHÉS:")
                mapping = {}
                
                for country in data['data']:
                    country_id = country.get('id')
                    country_name = country.get('name', 'Unknown')
                    
                    if country_id in target_ids:
                        mapping[country_id] = country_name
                        print(f"  {country_id}: {country_name}")
                
                print(f"\n📊 {len(mapping)}/{len(target_ids)} IDs trouvés")
                
                # Afficher tous les mappings trouvés
                print(f"\n{'='*60}")
                print("📝 MAPPING COMPLET POUR LE CODE")
                print("="*60)
                
                for country_id, name in mapping.items():
                    print(f"{country_id}: \"{name}\",")
                
                return mapping
                
            else:
                print("❌ Pas de données trouvées")
        else:
            print(f"❌ Erreur API: {response.status_code}")
            try:
                error_data = response.json()
                print(f"Détails: {json.dumps(error_data, indent=2)}")
            except:
                print(f"Contenu: {response.text}")
                
    except Exception as e:
        print(f"❌ Exception: {e}")
    
    return {}

def main():
    get_all_countries()

if __name__ == "__main__":
    main()