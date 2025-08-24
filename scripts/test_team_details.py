#!/usr/bin/env python3
"""
Test API pour récupérer les détails d'une équipe (stade, coach, stats, trophées)
"""

import requests
import json

API_KEY = "leBzDfKbRE5k9zEg3FuZE3Hh7XbukODNarOXLoVtPAiAtliDZ19wLu1Wnzi2"
BASE_URL = "https://api.sportmonks.com/v3/football"

headers = {
    "Accept": "application/json",
    "Authorization": API_KEY,
}

# Test avec l'OM (ID 44 selon les données du user)
team_id = 44
print("=== TEST RECUPERATION DETAILS EQUIPE (OM) ===\n")

# Test avec différents includes
url = f"{BASE_URL}/teams/{team_id}"
params = {
    'include': 'coaches;venue;statistics;trophies'
}

response = requests.get(url, headers=headers, params=params)

if response.status_code == 200:
    data = response.json()
    team = data.get('data', {})
    
    print(f"Équipe: {team.get('name')}")
    print(f"Nom court: {team.get('short_code')}")
    print(f"Fondé en: {team.get('founded')}")
    
    # Venue (stade)
    venue = team.get('venue')
    if venue:
        print(f"\n=== STADE ===")
        print(f"Nom: {venue.get('name')}")
        print(f"Ville: {venue.get('city', {}).get('name') if venue.get('city') else 'N/A'}")
        print(f"Capacité: {venue.get('capacity')}")
        print(f"Adresse: {venue.get('address')}")
        print(f"Surface: {venue.get('surface')}")
    
    # Coaches
    coaches = team.get('coaches', [])
    if coaches:
        print(f"\n=== ENTRAINEURS ===")
        for coach in coaches[:1]:  # Prendre seulement l'entraîneur actuel
            print(f"Nom: {coach.get('name')}")
            print(f"Nationalité: {coach.get('nationality', {}).get('name') if coach.get('nationality') else 'N/A'}")
            print(f"Image: {coach.get('image_path')}")
    
    # Statistics
    stats = team.get('statistics', [])
    if stats:
        print(f"\n=== STATISTIQUES (dernières disponibles) ===")
        # Prendre les stats les plus récentes
        latest_stats = stats[0] if stats else {}
        details = latest_stats.get('details', [])
        for stat in details[:10]:  # Limiter l'affichage
            stat_type = stat.get('type', {})
            print(f"{stat_type.get('name')}: {stat.get('value', {}).get('all')}")
    
    # Trophies
    trophies = team.get('trophies', [])
    if trophies:
        print(f"\n=== TROPHEES ({len(trophies)} au total) ===")
        for trophy in trophies[:5]:  # Afficher les 5 premiers
            print(f"- {trophy.get('name')} ({trophy.get('times')} fois)")
    
    # Sauvegarder pour analyse
    with open('team_details_test.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"\n✅ Données complètes sauvegardées dans team_details_test.json")
    
else:
    print(f"❌ Erreur API: {response.status_code}")
    print(response.text)