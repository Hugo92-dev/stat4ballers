#!/usr/bin/env python3
"""
Script optimisé pour récupérer tous les effectifs de Ligue 1
Saison 2025/2026 (ID: 25651)
"""

import requests
import json
from datetime import datetime, date
from typing import Dict, List, Optional
import time
import os

API_TOKEN = "leBzDfKbRE5k9zEg3FuZE3Hh7XbukODNarOXLoVtPAiAtliDZ19wLu1Wnzi2"
BASE_URL = "https://api.sportmonks.com/v3/football"
LIGUE1_SEASON_ID = 25651

# On a déjà OM, on va chercher les autres
LIGUE1_TEAMS = {
    44: {"name": "Olympique Marseille", "slug": "marseille", "done": True},
    591: {"name": "Paris Saint-Germain", "slug": "paris-saint-germain", "done": False},
    79: {"name": "Olympique Lyonnais", "slug": "lyon", "done": False},
    690: {"name": "LOSC Lille", "slug": "lille", "done": False},
    6789: {"name": "Monaco", "slug": "monaco", "done": False},
    271: {"name": "Lens", "slug": "lens", "done": False},
    598: {"name": "Rennes", "slug": "rennes", "done": False},
    450: {"name": "Nice", "slug": "nice", "done": False},
}

print("Test Ligue 1 teams")

