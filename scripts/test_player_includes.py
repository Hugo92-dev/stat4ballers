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

def test_player_with_includes(player_id, player_name):
    """Test différents includes pour voir si on peut récupérer le nom du pays"""
    print(f"\n{'='*60}")
    print(f"🔍 TEST INCLUDES POUR {player_name} (ID: {player_id})")
    print("="*60)
    
    # Différents includes à tester
    includes_to_test = [
        "nationality",
        "country", 
        "nationality.country",
        "country.nationality",
        "team,nationality",
        "team,country",
        "position,nationality",
        "position,country"
    ]
    
    for include in includes_to_test:
        print(f"\n📋 Test avec include='{include}':")
        
        url = f"{BASE_URL}/players/{player_id}"
        params = {
            'api_token': API_KEY,
            'include': include
        }
        
        try:
            response = requests.get(url, params=params)
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                if 'data' in data:
                    player_data = data['data']
                    
                    # Chercher des informations sur la nationalité
                    nationality_info = None
                    country_info = None
                    
                    if 'nationality' in player_data:
                        nationality_info = player_data['nationality']
                        print(f"   ✅ nationality trouvé: {nationality_info}")
                    
                    if 'country' in player_data:
                        country_info = player_data['country']
                        print(f"   ✅ country trouvé: {country_info}")
                    
                    if not nationality_info and not country_info:
                        print(f"   ❌ Pas d'info nationalité/pays avec cet include")
                else:
                    print(f"   ❌ Pas de données")
            elif response.status_code == 404:
                print(f"   ❌ Include '{include}' n'existe pas")
            elif response.status_code == 403:
                print(f"   ❌ Accès refusé pour include '{include}'")
            else:
                print(f"   ❌ Erreur {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Exception: {e}")

def main():
    print("="*60)
    print("🔬 TEST DES INCLUDES POUR RÉCUPÉRER LES NATIONALITÉS")
    print("="*60)
    
    # Test sur quelques joueurs problématiques
    test_players = [
        (32390, "U. Garcia (Suisse)"),    # nationality_id: 62
        (586846, "D. Cornelius (Canada)"), # nationality_id: 1004  
        (1744, "P. Højbjerg (Danemark)"),  # nationality_id: 320
        (433458, "A. Gouiri (Algérie)")    # nationality_id: 614 - on sait que c'est bon
    ]
    
    for player_id, player_name in test_players:
        test_player_with_includes(player_id, player_name)
    
    print(f"\n{'='*60}")
    print("✅ TESTS TERMINÉS")
    print("="*60)

if __name__ == "__main__":
    main()