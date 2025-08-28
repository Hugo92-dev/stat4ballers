#!/usr/bin/env python3
"""Test rapide des joueurs clés après mise à jour"""

import sys
import json

sys.stdout.reconfigure(encoding='utf-8')

def test_player_via_api(player_id, league, player_name):
    """Teste un joueur via l'API locale"""
    import requests
    
    url = f"http://localhost:3000/api/player-stats?playerId={player_id}&league={league}"
    
    try:
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            
            print(f"\n🎯 {player_name}")
            print("-" * 40)
            
            # Stats saison précédente (2024/2025)
            if 'previous' in data and data['previous']:
                prev = data['previous'][0] if isinstance(data['previous'], list) else data['previous']
                
                print(f"📅 Saison 2024/2025:")
                
                # Stats principales selon la position
                if 'saves' in prev and prev.get('saves'):  # Gardien
                    print(f"  • Matchs: {prev.get('appearences', 0)}")
                    print(f"  • Arrêts: {prev.get('saves', 0)}")
                    print(f"  • Buts encaissés: {prev.get('goals_conceded', 0)}")
                    print(f"  • Clean sheets: {prev.get('clean_sheets', 0)}")
                else:  # Joueur de champ
                    print(f"  • Matchs: {prev.get('appearences', 0)}")
                    print(f"  • Buts: {prev.get('goals', 0)}")
                    print(f"  • Passes décisives: {prev.get('assists', 0)}")
                    print(f"  • Minutes: {prev.get('minutes', 0)}")
                
                print(f"  • Note moyenne: {prev.get('rating', 'N/A')}")
                return True
            else:
                print(f"  ⚠️ Pas de données pour la saison précédente")
                return False
        else:
            print(f"  ❌ Erreur API: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"  ❌ Erreur: {e}")
        return False

def main():
    print("🔍 TEST DES JOUEURS CLÉS")
    print("=" * 60)
    
    # Liste des joueurs à tester
    players = [
        # Ligue 1
        (129771, 'ligue1', 'Gianluigi Donnarumma (PSG)'),
        (184432, 'ligue1', 'Kylian Mbappé (PSG)'),  # S'il est encore dans les données
        (184327, 'ligue1', 'Mason Greenwood (OM)'),
        (84465, 'ligue1', 'Alexandre Lacazette (Lyon)'),
        
        # Premier League
        (182915, 'premierLeague', 'Erling Haaland (Man City)'),
        (38804, 'premierLeague', 'Mohamed Salah (Liverpool)'),
        (97718, 'premierLeague', 'Bukayo Saka (Arsenal)'),
        
        # Liga
        (96611, 'liga', 'Kylian Mbappé (Real Madrid)'),
        (93105, 'liga', 'Vinícius Júnior (Real Madrid)'),
        (184675, 'liga', 'Jude Bellingham (Real Madrid)'),
        
        # Serie A
        (338923, 'serieA', 'Victor Osimhen (Napoli)'),
        (133295, 'serieA', 'Dušan Vlahović (Juventus)'),
        
        # Bundesliga
        (204023, 'bundesliga', 'Harry Kane (Bayern)'),
        (43658, 'bundesliga', 'Florian Wirtz (Leverkusen)'),
    ]
    
    success_count = 0
    total_count = len(players)
    
    for player_id, league, name in players:
        if test_player_via_api(player_id, league, name):
            success_count += 1
    
    print("\n" + "=" * 60)
    print(f"📊 RÉSULTAT: {success_count}/{total_count} joueurs avec données correctes")
    
    if success_count == total_count:
        print("✅ Tous les joueurs clés ont des statistiques correctes!")
    elif success_count > total_count * 0.8:
        print("🔶 La plupart des joueurs ont des données correctes")
    else:
        print("⚠️ Des mises à jour sont encore nécessaires")

if __name__ == "__main__":
    main()