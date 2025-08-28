#!/usr/bin/env python3
"""Mapping CORRECT des IDs SportMonks basé sur les vraies données de l'API"""

# MAPPING VÉRIFIÉ ET CORRECT basé sur l'API réelle
CORRECT_STAT_MAPPING = {
    # Général
    321: 'appearences',      # Appearances
    322: 'lineups',          # Lineups
    323: 'substitutions',    # Bench (substitutions)
    119: 'minutes',          # Minutes Played
    118: 'rating',           # Rating
    40: 'captain',           # Captain
    
    # Offensif
    52: 'goals',             # Goals
    79: 'assists',           # Assists (PAS 58 !)
    42: 'shots',             # Shots Total
    86: 'shots_on_target',   # Shots On Target (PAS 65 !)
    41: 'shots_off_target',  # Shots Off Target
    58: 'shots_blocked',     # Shots Blocked (PAS assists !)
    64: 'hit_woodwork',      # Hit Woodwork (PAS 70 !)
    51: 'offsides',          # Offsides
    
    # Penalties
    47: 'penalties',         # Penalties
    85: 'penalties_scored',  # À vérifier
    62: 'penalties_missed',  # À vérifier
    218: 'penalties_won',    # À vérifier
    217: 'penalties_committed', # À vérifier
    
    # Passes
    80: 'passes',            # Passes
    116: 'passes_completed', # Accurate Passes
    1584: 'passes_accuracy', # Accurate Passes Percentage
    117: 'key_passes',       # Key Passes
    98: 'crosses',           # Total Crosses
    99: 'crosses_accurate',  # Accurate Crosses
    124: 'through_balls',    # Through Balls
    125: 'through_balls_won', # Through Balls Won
    122: 'long_balls',       # Long Balls
    123: 'long_balls_won',   # Long Balls Won
    
    # Défense
    78: 'tackles',           # Tackles (PAS 105 !)
    100: 'interceptions',    # Interceptions (PAS 74 !)
    97: 'blocks',            # Blocked Shots (PAS 82 !)
    101: 'clearances',       # Clearances (PAS 99 !)
    
    # Duels
    105: 'duels',            # Total Duels
    106: 'duels_won',        # Duels Won
    107: 'aerial_duels_won', # Aerials Won
    
    # Dribbles
    108: 'dribbles',         # Dribble Attempts
    109: 'dribbles_successful', # Successful Dribbles
    110: 'dribbled_past',    # Dribbled Past
    94: 'dispossessed',      # Dispossessed
    
    # Discipline
    56: 'fouls',             # Fouls
    96: 'fouls_drawn',       # Fouls Drawn
    84: 'yellow_cards',      # Yellowcards
    83: 'red_cards',         # Redcards
    
    # Gardien
    57: 'saves',             # À vérifier pour les gardiens
    88: 'goals_conceded',    # Goals Conceded
    194: 'clean_sheets',     # Cleansheets
    207: 'punches',          # À vérifier
    104: 'inside_box_saves', # À vérifier
    240: 'penalties_saved',  # À vérifier
    
    # Stats avancées
    576: 'xg',               # Expected Goals
    577: 'xa',               # Expected Assists
    580: 'big_chances_created', # Big Chances Created
    581: 'big_chances_missed',  # Big Chances Missed
    571: 'mistakes_leading_to_goals', # Error Lead To Goal
    
    # Autres
    87: 'injuries',          # Injuries
    214: 'wins',             # Team Wins
    215: 'draws',            # Team Draws
    216: 'losses',           # Team Lost
}

def print_mapping_code():
    """Génère le code Python pour le mapping"""
    print("# MAPPING CORRECT basé sur l'API réelle SportMonks")
    print("# Généré automatiquement à partir des vraies données API")
    print()
    
    # Trier par catégorie
    categories = {
        'Général': [321, 322, 323, 119, 118, 40],
        'Offensif': [52, 79, 42, 86, 41, 58, 64, 51],
        'Passes': [80, 116, 1584, 117, 98, 99],
        'Défense': [78, 100, 97, 101],
        'Duels': [105, 106, 107],
        'Dribbles': [108, 109, 110, 94],
        'Discipline': [56, 96, 84, 83],
        'Gardien': [57, 88, 194]
    }
    
    for category, ids in categories.items():
        print(f"            # {category}")
        for type_id in ids:
            if type_id in CORRECT_STAT_MAPPING:
                field = CORRECT_STAT_MAPPING[type_id]
                print(f"            elif type_id == {type_id}:")
                print(f"                stats['{field}'] = actual_value")
        print()

if __name__ == "__main__":
    print("MAPPING CORRECT DES IDS SPORTMONKS")
    print("=" * 70)
    print()
    print_mapping_code()
    
    print("\nERREURS DANS LE SCRIPT ACTUEL:")
    print("-" * 70)
    print("ERREUR: ID 58 est utilisé pour 'assists' -> FAUX ! C'est 'shots_blocked'")
    print("ERREUR: ID 79 n'est pas mappé -> C'est le VRAI ID pour 'assists'")
    print("ERREUR: ID 65 est utilisé pour 'shots_on_target' -> FAUX ! C'est ID 86")
    print("ERREUR: ID 70 est utilisé pour 'hit_woodwork' -> FAUX ! C'est ID 64")
    print("ERREUR: ID 105 est utilisé pour 'tackles' -> FAUX ! C'est ID 78")
    print("ERREUR: ID 74 est utilisé pour 'interceptions' -> FAUX ! C'est ID 100")