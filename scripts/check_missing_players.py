import json
import sys

# Fix pour l'encodage UTF-8 sur Windows
sys.stdout.reconfigure(encoding='utf-8')

# Charger les données complètes
with open('om_complete_stats_v2.json', 'r', encoding='utf-8') as f:
    fetched_data = json.load(f)

# IDs des joueurs de l'OM dans ligue1Teams.ts (equipe marseille)
om_player_ids = [
    186418,  # Gerónimo Rulli
    29186,   # Jeffrey de Lange
    186456,  # Rubén Blanco
    37593233, # Jelle Van Neck
    28575687, # CJ Egan-Riley
    13171199, # Leonardo Balerdi
    32390,   # Ulisses Garcia
    586846,  # Derek Cornelius
    37369302, # Bamo Meïté
    95694,   # Adrien Rabiot
    1744,    # Pierre-Emile Hojbjerg
    95696,   # Geoffrey Kondogbia
    130063,  # Pol Lirola
    37657133, # François Mughe
    37541144, # Bilal Nadir
    335521,  # Facundo Medina
    37737405, # Darryl Bakola
    512560,  # Amir Murillo
    608285,  # Angel Gomes
    96691,   # Amine Harit
    21803033, # Azzedine Ounahi
    31739,   # Pierre-Emerick Aubameyang
    95776,   # Neal Maupay
    20333643, # Mason Greenwood
    433458,  # Amine Gouiri
    20315925, # Faris Moumbagna
    537332,  # Timothy Weah
    29328428, # Igor Paixão
    34455209, # Jonathan Rowe
]

# IDs dans les données récupérées
fetched_ids = set(fetched_data.keys())

# Convertir en strings pour comparaison
om_player_ids_str = set(str(id) for id in om_player_ids)

# Trouver les manquants
missing_ids = om_player_ids_str - fetched_ids

print("=" * 80)
print("ANALYSE DES JOUEURS MANQUANTS")
print("=" * 80)

print(f"\nTotal joueurs OM dans ligue1Teams.ts: {len(om_player_ids)}")
print(f"Total joueurs récupérés: {len(fetched_ids)}")
print(f"Joueurs manquants: {len(missing_ids)}")

if missing_ids:
    print("\n🚨 JOUEURS MANQUANTS (IDs):")
    for player_id in sorted(missing_ids):
        print(f"  - {player_id}")
        
    # Identifier les noms des manquants
    print("\n📝 DÉTAILS DES JOUEURS MANQUANTS:")
    player_names = {
        '186418': "Gerónimo Rulli (GK)",
        '29186': "Jeffrey de Lange (GK)",
        '186456': "Rubén Blanco (GK)",
        '37593233': "Jelle Van Neck (GK)",
        '28575687': "CJ Egan-Riley",
        '13171199': "Leonardo Balerdi",
        '32390': "Ulisses Garcia", 
        '586846': "Derek Cornelius",
        '37369302': "Bamo Meïté",
        '95694': "Adrien Rabiot",
        '1744': "Pierre-Emile Hojbjerg",
        '95696': "Geoffrey Kondogbia",
        '130063': "Pol Lirola",
        '37657133': "François Mughe",
        '37541144': "Bilal Nadir",
        '335521': "Facundo Medina",
        '37737405': "Darryl Bakola",
        '512560': "Amir Murillo",
        '608285': "Angel Gomes",
        '96691': "Amine Harit",
        '21803033': "Azzedine Ounahi",
        '31739': "Pierre-Emerick Aubameyang",
        '95776': "Neal Maupay",
        '20333643': "Mason Greenwood",
        '433458': "Amine Gouiri",
        '20315925': "Faris Moumbagna",
        '537332': "Timothy Weah",
        '29328428': "Igor Paixão",
        '34455209': "Jonathan Rowe",
    }
    
    for player_id in sorted(missing_ids):
        if player_id in player_names:
            print(f"  - {player_id}: {player_names[player_id]}")
        else:
            print(f"  - {player_id}: (nom inconnu)")

print("\n✅ PROCHAINE ÉTAPE:")
print("Il faut relancer le script de récupération avec TOUS les IDs des joueurs de l'OM")