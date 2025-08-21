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

def get_country_name(country_id):
    """Récupère le nom d'un pays par son ID"""
    url = f"{BASE_URL}/countries/{country_id}"
    params = {'api_token': API_KEY}
    
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            if 'data' in data:
                name = data['data'].get('name', 'Unknown')
                return name
        elif response.status_code == 429:
            print(f"⏳ Rate limit pour country_id {country_id}")
            time.sleep(2)
            return get_country_name(country_id)
    except Exception as e:
        print(f"Erreur pour country_id {country_id}: {e}")
    
    return f"Unknown (ID: {country_id})"

def main():
    print("="*60)
    print("🌍 RÉSOLUTION DES IDS DE PAYS")
    print("="*60)
    
    # IDs trouvés dans l'analyse précédente
    country_ids_to_check = [
        17,    # Aubameyang et Gouiri (pays de naissance)
        3662,  # Aubameyang (nationalité sportive) - Gabon
        462,   # Rowe et Greenwood (pays + nationalité) - Angleterre
        614,   # Gouiri (nationalité sportive) - Algérie
    ]
    
    print("Résolution des IDs de pays...")
    
    country_mapping = {}
    
    for country_id in country_ids_to_check:
        print(f"\n🔍 Country ID {country_id}:")
        country_name = get_country_name(country_id)
        print(f"   → {country_name}")
        country_mapping[country_id] = country_name
        time.sleep(0.5)
    
    print(f"\n{'='*60}")
    print("📋 MAPPING FINAL")
    print("="*60)
    
    for country_id, name in country_mapping.items():
        print(f"{country_id}: \"{name}\"")
    
    print(f"\n{'='*60}")
    print("🎯 RÉSUMÉ POUR LES JOUEURS OM")
    print("="*60)
    
    print("Pierre-Emerick Aubameyang:")
    print(f"  - Pays de naissance: {country_mapping.get(17, 'Unknown')} (ID: 17)")
    print(f"  - Nationalité sportive: {country_mapping.get(3662, 'Unknown')} (ID: 3662)")
    
    print("\nJonathan Rowe:")
    print(f"  - Pays de naissance: {country_mapping.get(462, 'Unknown')} (ID: 462)")
    print(f"  - Nationalité sportive: {country_mapping.get(462, 'Unknown')} (ID: 462)")
    
    print("\nMason Greenwood:")
    print(f"  - Pays de naissance: {country_mapping.get(462, 'Unknown')} (ID: 462)")
    print(f"  - Nationalité sportive: {country_mapping.get(462, 'Unknown')} (ID: 462)")
    
    print("\nAmine Gouiri:")
    print(f"  - Pays de naissance: {country_mapping.get(17, 'Unknown')} (ID: 17)")
    print(f"  - Nationalité sportive: {country_mapping.get(614, 'Unknown')} (ID: 614)")

if __name__ == "__main__":
    main()