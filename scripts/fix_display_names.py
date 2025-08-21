#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import re

# Forcer l'encodage UTF-8 pour Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'replace')

def smart_display_name(full_name):
    """
    Crée un display_name intelligent à partir du fullName
    Règles:
    - Si le nom a 2 parties: on les garde (ex: "Kylian Mbappé")
    - Si le nom a 3 parties: premier prénom + dernier nom  
    - Si le nom a 4+ parties: on essaie de deviner intelligemment
    """
    if not full_name:
        return full_name
    
    parts = full_name.split()
    
    if len(parts) <= 2:
        # Nom simple: prénom + nom
        return full_name
    elif len(parts) == 3:
        # Format typique: Prénom (Deuxième_prénom) Nom
        # On garde: Prénom Nom
        return f"{parts[0]} {parts[-1]}"
    elif len(parts) == 4:
        # Cas fréquents:
        # 1. Prénom Deuxième_prénom Nom Nom2 -> Prénom Nom
        # 2. Prénom Nom de Famille -> Prénom Nom
        
        # Si le 3e mot est un connecteur, on prend prénom + les 2 derniers
        connectors = ['de', 'da', 'do', 'dos', 'das', 'del', 'della', 'van', 'von', 'di', 'le', 'la']
        
        if parts[2].lower() in connectors:
            # Ex: "João Pedro de Jesus" -> "João de Jesus"
            return f"{parts[0]} {parts[2]} {parts[3]}"
        else:
            # Cas comme "Leonardo Julián Balerdi Rossa"
            # On suppose que les 2 premiers sont les prénoms, les 2 derniers les noms
            # On prend: premier prénom + premier nom de famille
            return f"{parts[0]} {parts[2]}"
    else:
        # 5+ parties: cas complexe
        # Stratégie: Premier prénom + recherche intelligente du nom principal
        
        connectors = ['de', 'da', 'do', 'dos', 'das', 'del', 'della', 'van', 'von', 'di', 'le', 'la']
        
        # Chercher un connecteur dans les parties du milieu/fin
        for i in range(2, len(parts) - 1):
            if parts[i].lower() in connectors:
                # On a trouvé un connecteur, on prend ce qui suit
                return f"{parts[0]} {' '.join(parts[i:])}"
        
        # Pas de connecteur trouvé
        # Pour un nom comme "João Pedro Junqueira de Jesus"
        # On suppose que les premiers mots sont des prénoms
        # On prend le premier prénom + le mot du milieu comme nom de famille
        if len(parts) == 5:
            return f"{parts[0]} {parts[2]}"
        else:
            # Fallback: premier + dernier
            return f"{parts[0]} {parts[-1]}"

def fix_display_names_in_file(file_path):
    """Corrige les displayName dans un fichier de données"""
    
    print(f"\n📁 Traitement de {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    new_lines = []
    i = 0
    players_fixed = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Chercher une ligne avec fullName
        if 'fullName:' in line:
            # Extraire le fullName
            match = re.search(r'fullName:\s*"([^"]+)"', line)
            if match:
                full_name = match.group(1)
                
                # Générer le bon displayName
                display_name = smart_display_name(full_name)
                
                # Ajouter la ligne fullName
                new_lines.append(line)
                
                # Vérifier si la ligne suivante est displayName
                if i + 1 < len(lines) and 'displayName:' in lines[i + 1]:
                    # Remplacer le displayName existant
                    indent = len(lines[i + 1]) - len(lines[i + 1].lstrip())
                    new_lines.append(' ' * indent + f'displayName: "{display_name}",\n')
                    i += 2  # Skip la ligne displayName originale
                    players_fixed += 1
                else:
                    # Pas de displayName, on l'ajoute
                    indent = len(line) - len(line.lstrip())
                    new_lines.append(' ' * indent + f'displayName: "{display_name}",\n')
                    i += 1
                    players_fixed += 1
            else:
                new_lines.append(line)
                i += 1
        else:
            new_lines.append(line)
            i += 1
    
    # Écrire le fichier corrigé
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    print(f"   ✅ {players_fixed} joueurs corrigés")

def main():
    """Corrige tous les fichiers de données"""
    
    print("=" * 80)
    print("CORRECTION DES DISPLAY_NAME")
    print("=" * 80)
    
    data_files = [
        'data/ligue1Teams.ts',
        'data/premierLeagueTeams.ts',
        'data/ligaTeams.ts',
        'data/serieATeams.ts',
        'data/bundesligaTeams.ts'
    ]
    
    # Tester avec quelques exemples
    test_names = [
        "Kylian Mbappé",
        "Leonardo Julián Balerdi Rossa",
        "Gianluigi Donnarumma",
        "Achraf Hakimi Mouh",
        "Marcos Aoás Corrêa",
        "João Pedro Junqueira de Jesus",
        "Luis Henrique Tomaz de Lima"
    ]
    
    print("\n🧪 Tests de conversion:")
    for name in test_names:
        display = smart_display_name(name)
        print(f"   {name:40} → {display}")
    
    print("\n" + "-" * 80)
    
    # Corriger tous les fichiers
    for file_path in data_files:
        fix_display_names_in_file(file_path)
    
    print("\n✅ Tous les fichiers ont été corrigés!")

if __name__ == "__main__":
    main()