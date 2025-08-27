#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Utilitaires pour récupérer les statistiques complètes des joueurs
Version 2 - Plus robuste avec fallback sur saisons précédentes
"""

import requests
import time

def fetch_complete_player_statistics(player_id, season_id, api_key, base_url):
    """
    Récupère TOUTES les statistiques d'un joueur pour la saison
    Essaye d'abord la saison demandée, puis les saisons précédentes en fallback
    """
    
    # Saisons de fallback (2024/2025) si 2025/2026 n'a pas de données
    fallback_seasons = {
        25651: 23871,  # Ligue 1: 2025/2026 -> 2024/2025
        25583: 23924,  # Premier League: 2025/2026 -> 2024/2025
        25659: 23887,  # La Liga: 2025/2026 -> 2024/2025
        25533: 23918,  # Serie A: 2025/2026 -> 2024/2025
        25646: 23988   # Bundesliga: 2025/2026 -> 2024/2025
    }
    
    # Essayer d'abord avec la saison demandée
    stats = try_fetch_stats_for_season(player_id, season_id, api_key, base_url)
    
    # Si pas de stats et qu'on a une saison de fallback, essayer avec
    if not has_valid_stats(stats) and season_id in fallback_seasons:
        print(f"        ⏳ Pas de stats 2025/2026, recherche 2024/2025...")
        fallback_stats = try_fetch_stats_for_season(player_id, fallback_seasons[season_id], api_key, base_url)
        if has_valid_stats(fallback_stats):
            print(f"        ✅ Stats 2024/2025 trouvées (temporaire)")
            return fallback_stats
    
    return stats

def try_fetch_stats_for_season(player_id, season_id, api_key, base_url):
    """
    Essaye de récupérer les stats pour une saison spécifique
    """
    try:
        # Endpoint qui fonctionne le mieux : topscorers/topassists par saison
        # D'abord essayer l'endpoint direct du joueur
        url = f"{base_url}/players/{player_id}"
        params = {
            "api_token": api_key,
            "include": "statistics.details.type,statistics.season"
        }
        
        response = requests.get(url, params=params, timeout=15)
        
        if response.status_code == 200:
            data = response.json().get('data', {})
            
            # Chercher les stats de la saison demandée
            if data.get('statistics'):
                stats_data = data['statistics'].get('data', [])
                for stat_entry in stats_data:
                    if stat_entry.get('season_id') == season_id:
                        return parse_stats_from_entry(stat_entry)
        
        # Si pas trouvé, essayer via team statistics
        return fetch_via_team_stats(player_id, season_id, api_key, base_url)
        
    except Exception as e:
        return get_empty_stats()

def fetch_via_team_stats(player_id, season_id, api_key, base_url):
    """
    Alternative: récupérer via les stats d'équipe
    """
    try:
        # D'abord récupérer l'équipe du joueur
        url = f"{base_url}/players/{player_id}"
        params = {"api_token": api_key, "include": "team"}
        
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json().get('data', {})
            team = data.get('team')
            
            if team and team.get('data'):
                team_id = team['data'].get('id')
                
                # Récupérer les stats de l'équipe pour la saison
                url = f"{base_url}/teams/{team_id}/seasons/{season_id}/players"
                params = {"api_token": api_key, "include": "statistics"}
                
                response = requests.get(url, params=params, timeout=10)
                if response.status_code == 200:
                    players = response.json().get('data', [])
                    for player_data in players:
                        if player_data.get('player_id') == player_id:
                            if player_data.get('statistics'):
                                return parse_stats_from_entry(player_data['statistics'])
    except:
        pass
    
    return get_empty_stats()

def parse_stats_from_entry(stat_entry):
    """
    Parse un objet de stats en dictionnaire complet
    """
    result = get_empty_stats()
    
    # Stats directes si disponibles
    direct_fields = {
        'appearances': 'appearances',
        'lineups': 'lineups',
        'minutes_played': 'minutes_played',
        'goals': 'goals',
        'assists': 'assists',
        'yellowcards': 'yellow_cards',
        'redcards': 'red_cards',
        'saves': 'saves',
        'cleansheets': 'clean_sheets',
        'rating': 'rating',
        'captain': 'captain'
    }
    
    for api_field, our_field in direct_fields.items():
        if stat_entry.get(api_field) is not None:
            result[our_field] = stat_entry[api_field]
    
    # Parser les détails si disponibles
    if stat_entry.get('details'):
        details = stat_entry['details'].get('data', []) if 'data' in stat_entry['details'] else stat_entry['details']
        
        for detail in details:
            type_id = detail.get('type', {}).get('id') if detail.get('type') else detail.get('type_id')
            value = detail.get('value', {})
            stat_value = value.get('total') if isinstance(value, dict) else value
            
            # Mapping des type_ids
            type_mapping = {
                52: 'goals',
                79: 'assists', 
                86: 'shots_total',
                87: 'shots_on_target',
                88: 'hit_woodwork',
                59: 'offsides',
                80: 'passes',
                81: 'accurate_passes_percentage',
                130: 'key_passes',
                82: 'total_crosses',
                105: 'total_duels',
                106: 'duels_won',
                123: 'aerials_won',
                91: 'tackles',
                56: 'fouls',
                58: 'fouls_drawn',
                84: 'yellow_cards',
                83: 'red_cards',
                267: 'goals_conceded',
                206: 'saves',
                209: 'saves_inside_box',
                76: 'clean_sheets',
                240: 'penalties_saved'
            }
            
            if type_id in type_mapping:
                result[type_mapping[type_id]] = stat_value or 0
    
    return result

def has_valid_stats(stats):
    """
    Vérifie si on a des stats valides (non nulles)
    """
    return any([
        stats.get('appearances', 0) > 0,
        stats.get('minutes_played', 0) > 0,
        stats.get('goals', 0) > 0,
        stats.get('assists', 0) > 0,
        stats.get('passes', 0) > 0
    ])

def get_empty_stats():
    """
    Retourne un dictionnaire de stats vides
    """
    return {
        # Carte Générale
        "appearances": 0,
        "lineups": 0,
        "minutes_played": 0,
        "captain": 0,
        "rating": 0.0,
        
        # Carte Offensive
        "goals": 0,
        "assists": 0,
        "shots_total": 0,
        "shots_on_target": 0,
        "hit_woodwork": 0,
        "offsides": 0,
        
        # Carte Créative
        "passes": 0,
        "accurate_passes_percentage": 0.0,
        "key_passes": 0,
        "total_crosses": 0,
        
        # Carte Défensive & Discipline
        "total_duels": 0,
        "duels_won": 0,
        "aerials_won": 0,
        "tackles": 0,
        "fouls": 0,
        "fouls_drawn": 0,
        "yellow_cards": 0,
        "red_cards": 0,
        
        # Carte Gardien
        "goals_conceded": 0,
        "saves": 0,
        "saves_inside_box": 0,
        "clean_sheets": 0,
        "penalties_saved": 0
    }