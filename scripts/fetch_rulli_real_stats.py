import requests
import json
import sys
import time

# Fix pour l'encodage UTF-8 sur Windows
sys.stdout.reconfigure(encoding='utf-8')

# NOUVELLE API KEY
API_KEY = "leBzDfKbRE5k9zEg3FuZE3Hh7XbukODNarOXLoVtPAiAtliDZ19wLu1Wnzi2"
BASE_URL = "https://api.sportmonks.com/v3/football"

headers = {
    "Accept": "application/json",
    "Authorization": API_KEY,
}

# IDs des saisons
SEASON_IDS = {
    "2025/2026": 25651,  # Ligue 1
    "2024/2025": 23643,  # Ligue 1
    "2023/2024": 21779,  # Ligue 1
}

def get_player_season_stats(player_id, season_id, season_name):
    """Récupère les vraies stats d'un joueur pour une saison"""
    url = f"{BASE_URL}/statistics/seasons/players/{player_id}"
    params = {
        "seasons": season_id
    }
    
    print(f"\n📊 Récupération saison {season_name} (ID: {season_id})...")
    
    try:
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 200:
            data = response.json()
            if data and "data" in data and len(data["data"]) > 0:
                # Trouver les stats de la bonne saison (peut y avoir plusieurs saisons)
                stats_data = None
                for item in data["data"]:
                    if item.get("season_id") == season_id and item.get("has_values"):
                        stats_data = item
                        break
                
                if not stats_data:
                    print(f"   ⚠️ Pas de données pour cette saison")
                    return None
                
                # Récupérer l'équipe
                team_name = "Olympique Marseille"
                
                # Les stats sont dans details
                if "details" in stats_data and len(stats_data["details"]) > 0:
                    detail = stats_data["details"][0]
                else:
                    print(f"   ⚠️ Pas de détails disponibles")
                    return None
                
                print(f"   ✅ Trouvé: {detail.get('games', {}).get('appearences', 0)} match(s) avec {team_name}")
                
                # Créer l'objet stats complet
                return {
                        "team": team_name,
                        "team_id": 44,
                        "league": "Ligue 1",
                        "rating": detail.get("rating"),
                        "minutes": detail.get("minutes", 0) or 0,
                        "appearences": detail.get("games", {}).get("appearences", 0) or 0,
                        "lineups": detail.get("games", {}).get("lineups", 0) or 0,
                        "captain": detail.get("games", {}).get("captain", 0) or 0,
                        
                        # Stats gardien
                        "saves": detail.get("goalkeeper", {}).get("saves", 0) or 0,
                        "goals_conceded": detail.get("goalkeeper", {}).get("goals_conceded", 0) or 0,
                        "clean_sheets": detail.get("goalkeeper", {}).get("cleansheets", 0) or 0,
                        "penalties_saved": detail.get("goalkeeper", {}).get("penalties_saved", 0) or 0,
                        "punches": detail.get("goalkeeper", {}).get("punches", 0) or 0,
                        "inside_box_saves": detail.get("goalkeeper", {}).get("inside_box_saves", 0) or 0,
                        
                        # Stats générales
                        "goals": detail.get("goals", {}).get("overall", 0) or 0,
                        "assists": detail.get("goals", {}).get("assists", 0) or 0,
                        "xg": detail.get("xg"),
                        "xa": detail.get("xa"),
                        
                        # Passes
                        "passes": detail.get("passes", {}).get("overall", 0) or 0,
                        "passes_completed": detail.get("passes", {}).get("completed", 0) or 0,
                        "passes_accuracy": detail.get("passes", {}).get("accuracy"),
                        "key_passes": detail.get("passes", {}).get("key_passes", 0) or 0,
                        
                        # Défense
                        "tackles": detail.get("defensive", {}).get("tackles", 0) or 0,
                        "blocks": detail.get("defensive", {}).get("blocks", 0) or 0,
                        "interceptions": detail.get("defensive", {}).get("interceptions", 0) or 0,
                        "clearances": detail.get("defensive", {}).get("clearances", 0) or 0,
                        
                        # Discipline
                        "fouls": detail.get("fouls", {}).get("overall", 0) or 0,
                        "fouls_drawn": detail.get("fouls", {}).get("drawn", 0) or 0,
                        "yellow_cards": detail.get("cards", {}).get("yellow_cards", 0) or 0,
                        "red_cards": detail.get("cards", {}).get("red_cards", 0) or 0,
                        "yellowred_cards": detail.get("cards", {}).get("yellowred_cards", 0) or 0,
                        
                        # Duels
                        "ground_duels": detail.get("duels", {}).get("ground", {}).get("overall", 0) or 0,
                        "ground_duels_won": detail.get("duels", {}).get("ground", {}).get("won", 0) or 0,
                        "aerial_duels": detail.get("duels", {}).get("aerial", {}).get("overall", 0) or 0,
                        "aerial_duels_won": detail.get("duels", {}).get("aerial", {}).get("won", 0) or 0,
                        
                        # Autres
                        "touches": detail.get("touches", 0) or 0,
                        "ball_losses": detail.get("ball_losses", 0) or 0,
                        "ball_recoveries": detail.get("ball_recoveries", 0) or 0,
                        "mistakes_leading_to_goals": detail.get("mistakes_leading_to_goals", 0) or 0,
                        "penalties_committed": detail.get("penalties", {}).get("committed", 0) or 0,
                        
                        # Non utilisés pour gardien mais on les met à 0
                        "shots": 0,
                        "shots_on_target": 0,
                        "crosses": 0,
                        "crosses_accurate": 0,
                        "dribbles": 0,
                        "dribbles_successful": 0,
                        "penalties_won": 0,
                        "penalties_scored": 0,
                        "penalties_missed": 0,
                        "penalties": 0,
                        "hit_woodwork": 0,
                        "offsides": 0,
                    }
            else:
                print(f"   ⚠️ Pas de données pour cette saison")
        
        elif response.status_code == 429:
            print("   ⏱️ Rate limit, pause de 65 secondes...")
            time.sleep(65)
            return get_player_season_stats(player_id, season_id, season_name)
        else:
            print(f"   ❌ Erreur {response.status_code}: {response.text[:100]}")
            
    except Exception as e:
        print(f"   ❌ Exception: {e}")
    
    return None

print("=" * 80)
print("RÉCUPÉRATION DES VRAIES STATS DE RULLI DEPUIS L'API")
print("=" * 80)

# Charger les données existantes
with open('om_complete_stats_v2.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# ID de Rulli
player_id = 186418

# Créer la structure pour Rulli
rulli_data = {
    "displayName": "Gerónimo Rulli",
    "position": "GK",
    "jersey": 1,
    "stats": {}
}

# Récupérer les vraies stats pour chaque saison
for season_name, season_id in SEASON_IDS.items():
    stats = get_player_season_stats(player_id, season_id, season_name)
    
    if stats and stats.get("appearences", 0) > 0:
        season_key = f"{season_name} (Ligue 1, Olympique Marseille)"
        rulli_data["stats"][season_key] = stats
        
        # Afficher les stats importantes
        print(f"\n   📈 Stats clés {season_name}:")
        print(f"      - Matchs: {stats['appearences']}")
        print(f"      - Minutes: {stats['minutes']}")
        print(f"      - Buts encaissés: {stats['goals_conceded']}")
        print(f"      - Clean sheets: {stats['clean_sheets']}")
        print(f"      - Arrêts: {stats['saves']}")
        print(f"      - Penalties arrêtés: {stats['penalties_saved']}")

# Mettre à jour les données
data['186418'] = rulli_data

# Sauvegarder
with open('om_complete_stats_v2.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("\n✅ Données de Rulli mises à jour avec les VRAIES stats de l'API!")

# Régénérer le fichier TypeScript
print("\n📝 Régénération du fichier TypeScript...")
exec(open('generate_om_typescript.py').read())

print("\n✅ Tout est mis à jour avec les vraies données!")