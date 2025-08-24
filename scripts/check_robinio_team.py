#!/usr/bin/env python3
"""
Vérifier dans quelle équipe est Robinio Vaz
"""

import requests
import json

API_KEY = "leBzDfKbRE5k9zEg3FuZE3Hh7XbukODNarOXLoVtPAiAtliDZ19wLu1Wnzi2"
BASE_URL = "https://api.sportmonks.com/v3/football"

headers = {
    "Accept": "application/json",
    "Authorization": API_KEY,
}

print("=== VERIFICATION DES EQUIPES DE ROBINIO VAZ ===\n")

# Vérifier l'équipe 3825
print("1. Équipe ID 3825:")
url = f"{BASE_URL}/teams/3825"
response = requests.get(url, headers=headers)
if response.status_code == 200:
    data = response.json()
    team = data.get('data', {})
    print(f"   Nom: {team.get('name')}")
    print(f"   Pays: {team.get('country', {}).get('name') if team.get('country') else 'N/A'}")
    print(f"   Type: {team.get('type')}")
else:
    print(f"   Erreur: {response.status_code}")

# Vérifier l'équipe 151389
print("\n2. Équipe ID 151389:")
url = f"{BASE_URL}/teams/151389"
response = requests.get(url, headers=headers)
if response.status_code == 200:
    data = response.json()
    team = data.get('data', {})
    print(f"   Nom: {team.get('name')}")
    print(f"   Pays: {team.get('country', {}).get('name') if team.get('country') else 'N/A'}")
    print(f"   Type: {team.get('type')}")
else:
    print(f"   Erreur: {response.status_code}")

print("\n3. Pour info, l'OM principal:")
print(f"   ID: 85")
print(f"   Nom: Olympique Marseille")

print("\n=== SOLUTION ===")
print("Robinio Vaz n'est PAS dans l'équipe première de l'OM (ID 85)")
print("Il est dans l'équipe réserve ou les jeunes")
print("\nPour l'ajouter automatiquement, il faudrait:")
print("1. Identifier toutes les équipes affiliées à l'OM (réserve, U19, etc.)")
print("2. Récupérer les joueurs de ces équipes")
print("3. Les intégrer dans l'effectif principal pour l'affichage")