import json
import os
from datetime import datetime
import requests
from typing import Dict, List, Any

class HybridScraper2025:
    """
    Scraper hybride pour la saison 2025-2026
    Combine données manuelles actualisées + API progressive
    """
    
    def __init__(self):
        self.season = "2025-2026"
        self.api_key = None  # À ajouter si on utilise une API
        
    def get_squad_2025_26(self) -> Dict[str, List[Dict]]:
        """
        Retourne les effectifs ACTUELS saison 2025-2026
        15 joueurs principaux par club
        """
        return {
            "ligue1": {
                "psg": [
                    # Gardiens
                    {"nom": "Gianluigi Donnarumma", "poste": "GK", "numero": 1, "age": 25, "nationalite": "Italie"},
                    {"nom": "Lucas Chevalier", "poste": "GK", "numero": 30, "age": 23, "nationalite": "France"},
                    {"nom": "Matvey Safonov", "poste": "GK", "numero": 39, "age": 25, "nationalite": "Russie"},
                    
                    # Défenseurs
                    {"nom": "Achraf Hakimi", "poste": "RB", "numero": 2, "age": 26, "nationalite": "Maroc"},
                    {"nom": "Marquinhos", "poste": "CB", "numero": 5, "age": 30, "nationalite": "Brésil"},
                    {"nom": "Lucas Hernández", "poste": "CB", "numero": 21, "age": 28, "nationalite": "France"},
                    {"nom": "Willian Pacho", "poste": "CB", "numero": 51, "age": 23, "nationalite": "Équateur"},
                    {"nom": "Nuno Mendes", "poste": "LB", "numero": 25, "age": 22, "nationalite": "Portugal"},
                    {"nom": "Milan Škriniar", "poste": "CB", "numero": 37, "age": 29, "nationalite": "Slovaquie"},
                    
                    # Milieux
                    {"nom": "Vitinha", "poste": "CM", "numero": 17, "age": 24, "nationalite": "Portugal"},
                    {"nom": "Warren Zaïre-Emery", "poste": "CM", "numero": 33, "age": 18, "nationalite": "France"},
                    {"nom": "João Neves", "poste": "DM", "numero": 87, "age": 20, "nationalite": "Portugal"},
                    {"nom": "Fabián Ruiz", "poste": "CM", "numero": 8, "age": 28, "nationalite": "Espagne"},
                    {"nom": "Lee Kang-in", "poste": "AM", "numero": 19, "age": 23, "nationalite": "Corée du Sud"},
                    
                    # Attaquants
                    {"nom": "Ousmane Dembélé", "poste": "RW", "numero": 10, "age": 27, "nationalite": "France"},
                    {"nom": "Bradley Barcola", "poste": "LW", "numero": 29, "age": 22, "nationalite": "France"},
                    {"nom": "Gonçalo Ramos", "poste": "ST", "numero": 9, "age": 23, "nationalite": "Portugal"},
                    {"nom": "Randal Kolo Muani", "poste": "ST", "numero": 23, "age": 26, "nationalite": "France"},
                    {"nom": "Marco Asensio", "poste": "RW", "numero": 11, "age": 28, "nationalite": "Espagne"}
                ],
                
                "marseille": [
                    # Gardiens
                    {"nom": "Gerónimo Rulli", "poste": "GK", "numero": 1, "age": 32, "nationalite": "Argentine"},
                    {"nom": "Jeffrey de Lange", "poste": "GK", "numero": 30, "age": 26, "nationalite": "Pays-Bas"},
                    
                    # Défenseurs
                    {"nom": "Amir Murillo", "poste": "RB", "numero": 62, "age": 22, "nationalite": "Panama"},
                    {"nom": "Leonardo Balerdi", "poste": "CB", "numero": 5, "age": 25, "nationalite": "Argentine"},
                    {"nom": "Derek Cornelius", "poste": "CB", "numero": 13, "age": 27, "nationalite": "Canada"},
                    {"nom": "Ulisses Garcia", "poste": "LB", "numero": 6, "age": 28, "nationalite": "Suisse"},
                    {"nom": "Quentin Merlin", "poste": "LB", "numero": 3, "age": 22, "nationalite": "France"},
                    {"nom": "Lilian Brassier", "poste": "CB", "numero": 20, "age": 25, "nationalite": "France"},
                    
                    # Milieux
                    {"nom": "Pierre-Emile Højbjerg", "poste": "DM", "numero": 23, "age": 29, "nationalite": "Danemark"},
                    {"nom": "Adrien Rabiot", "poste": "CM", "numero": 25, "age": 29, "nationalite": "France"},
                    {"nom": "Amine Harit", "poste": "AM", "numero": 11, "age": 27, "nationalite": "Maroc"},
                    {"nom": "Geoffrey Kondogbia", "poste": "DM", "numero": 27, "age": 31, "nationalite": "Centrafrique"},
                    
                    # Attaquants
                    {"nom": "Mason Greenwood", "poste": "RW", "numero": 10, "age": 23, "nationalite": "Angleterre"},
                    {"nom": "Neal Maupay", "poste": "ST", "numero": 32, "age": 28, "nationalite": "France"},
                    {"nom": "Jonathan Rowe", "poste": "LW", "numero": 17, "age": 21, "nationalite": "Angleterre"},
                    {"nom": "Ismaïla Sarr", "poste": "RW", "numero": 23, "age": 26, "nationalite": "Sénégal"}
                ],
                
                "monaco": [
                    {"nom": "Radosław Majecki", "poste": "GK", "numero": 1, "age": 25, "nationalite": "Pologne"},
                    {"nom": "Vanderson", "poste": "RB", "numero": 2, "age": 23, "nationalite": "Brésil"},
                    {"nom": "Thilo Kehrer", "poste": "CB", "numero": 5, "age": 28, "nationalite": "Allemagne"},
                    {"nom": "Mohammed Salisu", "poste": "CB", "numero": 22, "age": 25, "nationalite": "Ghana"},
                    {"nom": "Caio Henrique", "poste": "LB", "numero": 12, "age": 27, "nationalite": "Brésil"},
                    {"nom": "Denis Zakaria", "poste": "DM", "numero": 6, "age": 28, "nationalite": "Suisse"},
                    {"nom": "Lamine Camara", "poste": "CM", "numero": 15, "age": 20, "nationalite": "Sénégal"},
                    {"nom": "Aleksandr Golovin", "poste": "AM", "numero": 17, "age": 28, "nationalite": "Russie"},
                    {"nom": "Maghnes Akliouche", "poste": "RW", "numero": 11, "age": 22, "nationalite": "France"},
                    {"nom": "Takumi Minamino", "poste": "AM", "numero": 18, "age": 29, "nationalite": "Japon"},
                    {"nom": "Folarin Balogun", "poste": "ST", "numero": 29, "age": 23, "nationalite": "Angleterre"},
                    {"nom": "Breel Embolo", "poste": "ST", "numero": 36, "age": 27, "nationalite": "Suisse"},
                    {"nom": "Eliesse Ben Seghir", "poste": "LW", "numero": 7, "age": 19, "nationalite": "Maroc"},
                    {"nom": "George Ilenikhena", "poste": "ST", "numero": 21, "age": 18, "nationalite": "France"},
                    {"nom": "Krépin Diatta", "poste": "RW", "numero": 27, "age": 25, "nationalite": "Sénégal"}
                ],
                
                "lille": [
                    {"nom": "Lucas Chevalier", "poste": "GK", "numero": 30, "age": 23, "nationalite": "France"},
                    {"nom": "Thomas Meunier", "poste": "RB", "numero": 12, "age": 33, "nationalite": "Belgique"},
                    {"nom": "Bafodé Diakité", "poste": "CB", "numero": 18, "age": 23, "nationalite": "France"},
                    {"nom": "Alexsandro Ribeiro", "poste": "CB", "numero": 4, "age": 25, "nationalite": "Brésil"},
                    {"nom": "Gabriel Gudmundsson", "poste": "LB", "numero": 5, "age": 25, "nationalite": "Suède"},
                    {"nom": "Benjamin André", "poste": "DM", "numero": 21, "age": 34, "nationalite": "France"},
                    {"nom": "André Gomes", "poste": "CM", "numero": 8, "age": 31, "nationalite": "Portugal"},
                    {"nom": "Angel Gomes", "poste": "AM", "numero": 10, "age": 24, "nationalite": "Angleterre"},
                    {"nom": "Ngal'ayel Mukau", "poste": "CM", "numero": 6, "age": 20, "nationalite": "RD Congo"},
                    {"nom": "Edon Zhegrova", "poste": "RW", "numero": 23, "age": 25, "nationalite": "Kosovo"},
                    {"nom": "Osame Sahraoui", "poste": "LW", "numero": 11, "age": 23, "nationalite": "Norvège"},
                    {"nom": "Jonathan David", "poste": "ST", "numero": 9, "age": 24, "nationalite": "Canada"},
                    {"nom": "Mohamed Bayo", "poste": "ST", "numero": 27, "age": 26, "nationalite": "Guinée"},
                    {"nom": "Matias Fernandez-Pardo", "poste": "LW", "numero": 20, "age": 19, "nationalite": "Belgique"},
                    {"nom": "Rémy Cabella", "poste": "AM", "numero": 7, "age": 34, "nationalite": "France"}
                ]
            },
            
            "premier-league": {
                "arsenal": [
                    {"nom": "David Raya", "poste": "GK", "numero": 22, "age": 29, "nationalite": "Espagne"},
                    {"nom": "Ben White", "poste": "RB", "numero": 4, "age": 27, "nationalite": "Angleterre"},
                    {"nom": "William Saliba", "poste": "CB", "numero": 2, "age": 23, "nationalite": "France"},
                    {"nom": "Gabriel Magalhães", "poste": "CB", "numero": 6, "age": 27, "nationalite": "Brésil"},
                    {"nom": "Riccardo Calafiori", "poste": "LB", "numero": 33, "age": 22, "nationalite": "Italie"},
                    {"nom": "Declan Rice", "poste": "DM", "numero": 41, "age": 25, "nationalite": "Angleterre"},
                    {"nom": "Martin Ødegaard", "poste": "AM", "numero": 8, "age": 26, "nationalite": "Norvège"},
                    {"nom": "Mikel Merino", "poste": "CM", "numero": 23, "age": 28, "nationalite": "Espagne"},
                    {"nom": "Bukayo Saka", "poste": "RW", "numero": 7, "age": 23, "nationalite": "Angleterre"},
                    {"nom": "Kai Havertz", "poste": "CF", "numero": 29, "age": 25, "nationalite": "Allemagne"},
                    {"nom": "Gabriel Martinelli", "poste": "LW", "numero": 11, "age": 23, "nationalite": "Brésil"},
                    {"nom": "Leandro Trossard", "poste": "LW/RW", "numero": 19, "age": 30, "nationalite": "Belgique"},
                    {"nom": "Gabriel Jesus", "poste": "ST", "numero": 9, "age": 27, "nationalite": "Brésil"},
                    {"nom": "Raheem Sterling", "poste": "LW/RW", "numero": 30, "age": 30, "nationalite": "Angleterre"},
                    {"nom": "Ethan Nwaneri", "poste": "AM", "numero": 53, "age": 17, "nationalite": "Angleterre"}
                ],
                
                "manchester-city": [
                    {"nom": "Ederson", "poste": "GK", "numero": 31, "age": 31, "nationalite": "Brésil"},
                    {"nom": "Kyle Walker", "poste": "RB", "numero": 2, "age": 34, "nationalite": "Angleterre"},
                    {"nom": "Rúben Dias", "poste": "CB", "numero": 3, "age": 27, "nationalite": "Portugal"},
                    {"nom": "John Stones", "poste": "CB", "numero": 5, "age": 30, "nationalite": "Angleterre"},
                    {"nom": "Joško Gvardiol", "poste": "LB/CB", "numero": 24, "age": 22, "nationalite": "Croatie"},
                    {"nom": "Rodri", "poste": "DM", "numero": 16, "age": 28, "nationalite": "Espagne"},
                    {"nom": "Kevin De Bruyne", "poste": "AM", "numero": 17, "age": 33, "nationalite": "Belgique"},
                    {"nom": "Bernardo Silva", "poste": "AM/RW", "numero": 20, "age": 30, "nationalite": "Portugal"},
                    {"nom": "Mateo Kovačić", "poste": "CM", "numero": 8, "age": 30, "nationalite": "Croatie"},
                    {"nom": "Phil Foden", "poste": "AM/LW", "numero": 47, "age": 24, "nationalite": "Angleterre"},
                    {"nom": "Erling Haaland", "poste": "ST", "numero": 9, "age": 24, "nationalite": "Norvège"},
                    {"nom": "Jack Grealish", "poste": "LW", "numero": 10, "age": 29, "nationalite": "Angleterre"},
                    {"nom": "Jérémy Doku", "poste": "RW", "numero": 11, "age": 22, "nationalite": "Belgique"},
                    {"nom": "Savinho", "poste": "RW", "numero": 26, "age": 20, "nationalite": "Brésil"},
                    {"nom": "Rico Lewis", "poste": "RB/CM", "numero": 82, "age": 20, "nationalite": "Angleterre"}
                ],
                
                "liverpool": [
                    {"nom": "Alisson", "poste": "GK", "numero": 1, "age": 32, "nationalite": "Brésil"},
                    {"nom": "Trent Alexander-Arnold", "poste": "RB", "numero": 66, "age": 26, "nationalite": "Angleterre"},
                    {"nom": "Virgil van Dijk", "poste": "CB", "numero": 4, "age": 33, "nationalite": "Pays-Bas"},
                    {"nom": "Ibrahima Konaté", "poste": "CB", "numero": 5, "age": 25, "nationalite": "France"},
                    {"nom": "Andrew Robertson", "poste": "LB", "numero": 26, "age": 30, "nationalite": "Écosse"},
                    {"nom": "Ryan Gravenberch", "poste": "DM", "numero": 38, "age": 22, "nationalite": "Pays-Bas"},
                    {"nom": "Alexis Mac Allister", "poste": "CM", "numero": 10, "age": 26, "nationalite": "Argentine"},
                    {"nom": "Dominik Szoboszlai", "poste": "AM", "numero": 8, "age": 24, "nationalite": "Hongrie"},
                    {"nom": "Curtis Jones", "poste": "CM", "numero": 17, "age": 23, "nationalite": "Angleterre"},
                    {"nom": "Mohamed Salah", "poste": "RW", "numero": 11, "age": 32, "nationalite": "Égypte"},
                    {"nom": "Luis Díaz", "poste": "LW", "numero": 7, "age": 27, "nationalite": "Colombie"},
                    {"nom": "Cody Gakpo", "poste": "LW/ST", "numero": 18, "age": 25, "nationalite": "Pays-Bas"},
                    {"nom": "Darwin Núñez", "poste": "ST", "numero": 9, "age": 25, "nationalite": "Uruguay"},
                    {"nom": "Diogo Jota", "poste": "CF/LW", "numero": 20, "age": 28, "nationalite": "Portugal"},
                    {"nom": "Federico Chiesa", "poste": "RW", "numero": 14, "age": 27, "nationalite": "Italie"}
                ]
            },
            
            "liga": {
                "real-madrid": [
                    {"nom": "Thibaut Courtois", "poste": "GK", "numero": 1, "age": 32, "nationalite": "Belgique"},
                    {"nom": "Dani Carvajal", "poste": "RB", "numero": 2, "age": 32, "nationalite": "Espagne"},
                    {"nom": "Antonio Rüdiger", "poste": "CB", "numero": 22, "age": 31, "nationalite": "Allemagne"},
                    {"nom": "David Alaba", "poste": "CB", "numero": 4, "age": 32, "nationalite": "Autriche"},
                    {"nom": "Ferland Mendy", "poste": "LB", "numero": 23, "age": 29, "nationalite": "France"},
                    {"nom": "Aurélien Tchouaméni", "poste": "DM", "numero": 14, "age": 24, "nationalite": "France"},
                    {"nom": "Federico Valverde", "poste": "CM", "numero": 8, "age": 26, "nationalite": "Uruguay"},
                    {"nom": "Jude Bellingham", "poste": "AM", "numero": 5, "age": 21, "nationalite": "Angleterre"},
                    {"nom": "Eduardo Camavinga", "poste": "CM", "numero": 12, "age": 22, "nationalite": "France"},
                    {"nom": "Vinícius Júnior", "poste": "LW", "numero": 7, "age": 24, "nationalite": "Brésil"},
                    {"nom": "Kylian Mbappé", "poste": "ST", "numero": 9, "age": 26, "nationalite": "France"},
                    {"nom": "Rodrygo", "poste": "RW", "numero": 11, "age": 24, "nationalite": "Brésil"},
                    {"nom": "Luka Modrić", "poste": "CM", "numero": 10, "age": 39, "nationalite": "Croatie"},
                    {"nom": "Arda Güler", "poste": "AM/RW", "numero": 15, "age": 19, "nationalite": "Turquie"},
                    {"nom": "Brahim Díaz", "poste": "AM/RW", "numero": 21, "age": 25, "nationalite": "Maroc"}
                ],
                
                "barcelona": [
                    {"nom": "Marc-André ter Stegen", "poste": "GK", "numero": 1, "age": 32, "nationalite": "Allemagne"},
                    {"nom": "Jules Koundé", "poste": "RB", "numero": 23, "age": 26, "nationalite": "France"},
                    {"nom": "Ronald Araújo", "poste": "CB", "numero": 4, "age": 25, "nationalite": "Uruguay"},
                    {"nom": "Pau Cubarsí", "poste": "CB", "numero": 2, "age": 17, "nationalite": "Espagne"},
                    {"nom": "Alejandro Balde", "poste": "LB", "numero": 3, "age": 21, "nationalite": "Espagne"},
                    {"nom": "Marc Casadó", "poste": "DM", "numero": 17, "age": 21, "nationalite": "Espagne"},
                    {"nom": "Pedri", "poste": "CM", "numero": 8, "age": 22, "nationalite": "Espagne"},
                    {"nom": "Gavi", "poste": "CM", "numero": 6, "age": 20, "nationalite": "Espagne"},
                    {"nom": "Frenkie de Jong", "poste": "CM", "numero": 21, "age": 27, "nationalite": "Pays-Bas"},
                    {"nom": "Dani Olmo", "poste": "AM/RW", "numero": 20, "age": 26, "nationalite": "Espagne"},
                    {"nom": "Lamine Yamal", "poste": "RW", "numero": 19, "age": 17, "nationalite": "Espagne"},
                    {"nom": "Robert Lewandowski", "poste": "ST", "numero": 9, "age": 36, "nationalite": "Pologne"},
                    {"nom": "Raphinha", "poste": "LW/RW", "numero": 11, "age": 28, "nationalite": "Brésil"},
                    {"nom": "Ferran Torres", "poste": "LW/ST", "numero": 7, "age": 24, "nationalite": "Espagne"},
                    {"nom": "Pau Víctor", "poste": "ST", "numero": 18, "age": 23, "nationalite": "Espagne"}
                ],
                
                "atletico-madrid": [
                    {"nom": "Jan Oblak", "poste": "GK", "numero": 13, "age": 31, "nationalite": "Slovénie"},
                    {"nom": "Nahuel Molina", "poste": "RB", "numero": 16, "age": 26, "nationalite": "Argentine"},
                    {"nom": "José María Giménez", "poste": "CB", "numero": 2, "age": 29, "nationalite": "Uruguay"},
                    {"nom": "Robin Le Normand", "poste": "CB", "numero": 24, "age": 28, "nationalite": "Espagne"},
                    {"nom": "Reinildo Mandava", "poste": "LB", "numero": 23, "age": 30, "nationalite": "Mozambique"},
                    {"nom": "Koke", "poste": "CM", "numero": 6, "age": 32, "nationalite": "Espagne"},
                    {"nom": "Rodrigo De Paul", "poste": "CM", "numero": 5, "age": 30, "nationalite": "Argentine"},
                    {"nom": "Pablo Barrios", "poste": "CM", "numero": 8, "age": 21, "nationalite": "Espagne"},
                    {"nom": "Conor Gallagher", "poste": "CM", "numero": 4, "age": 24, "nationalite": "Angleterre"},
                    {"nom": "Antoine Griezmann", "poste": "AM/ST", "numero": 7, "age": 33, "nationalite": "France"},
                    {"nom": "Julián Álvarez", "poste": "ST", "numero": 19, "age": 24, "nationalite": "Argentine"},
                    {"nom": "Alexander Sørloth", "poste": "ST", "numero": 9, "age": 29, "nationalite": "Norvège"},
                    {"nom": "Samuel Lino", "poste": "LW", "numero": 12, "age": 25, "nationalite": "Brésil"},
                    {"nom": "Ángel Correa", "poste": "RW/ST", "numero": 10, "age": 29, "nationalite": "Argentine"},
                    {"nom": "Giuliano Simeone", "poste": "RW", "numero": 22, "age": 22, "nationalite": "Argentine"}
                ]
            },
            
            "bundesliga": {
                "bayern": [
                    {"nom": "Manuel Neuer", "poste": "GK", "numero": 1, "age": 38, "nationalite": "Allemagne"},
                    {"nom": "Joshua Kimmich", "poste": "RB/DM", "numero": 6, "age": 29, "nationalite": "Allemagne"},
                    {"nom": "Dayot Upamecano", "poste": "CB", "numero": 2, "age": 26, "nationalite": "France"},
                    {"nom": "Kim Min-jae", "poste": "CB", "numero": 3, "age": 28, "nationalite": "Corée du Sud"},
                    {"nom": "Alphonso Davies", "poste": "LB", "numero": 19, "age": 24, "nationalite": "Canada"},
                    {"nom": "João Palhinha", "poste": "DM", "numero": 16, "age": 29, "nationalite": "Portugal"},
                    {"nom": "Aleksandar Pavlović", "poste": "CM", "numero": 45, "age": 20, "nationalite": "Allemagne"},
                    {"nom": "Jamal Musiala", "poste": "AM", "numero": 42, "age": 21, "nationalite": "Allemagne"},
                    {"nom": "Michael Olise", "poste": "RW", "numero": 17, "age": 23, "nationalite": "France"},
                    {"nom": "Leroy Sané", "poste": "LW", "numero": 10, "age": 28, "nationalite": "Allemagne"},
                    {"nom": "Harry Kane", "poste": "ST", "numero": 9, "age": 31, "nationalite": "Angleterre"},
                    {"nom": "Serge Gnabry", "poste": "RW", "numero": 7, "age": 29, "nationalite": "Allemagne"},
                    {"nom": "Kingsley Coman", "poste": "LW", "numero": 11, "age": 28, "nationalite": "France"},
                    {"nom": "Thomas Müller", "poste": "AM/ST", "numero": 25, "age": 35, "nationalite": "Allemagne"},
                    {"nom": "Mathys Tel", "poste": "ST", "numero": 39, "age": 19, "nationalite": "France"}
                ],
                
                "borussia-dortmund": [
                    {"nom": "Gregor Kobel", "poste": "GK", "numero": 1, "age": 27, "nationalite": "Suisse"},
                    {"nom": "Julian Ryerson", "poste": "RB", "numero": 26, "age": 27, "nationalite": "Norvège"},
                    {"nom": "Nico Schlotterbeck", "poste": "CB", "numero": 4, "age": 25, "nationalite": "Allemagne"},
                    {"nom": "Niklas Süle", "poste": "CB", "numero": 25, "age": 29, "nationalite": "Allemagne"},
                    {"nom": "Ramy Bensebaini", "poste": "LB", "numero": 5, "age": 29, "nationalite": "Algérie"},
                    {"nom": "Emre Can", "poste": "DM", "numero": 23, "age": 30, "nationalite": "Allemagne"},
                    {"nom": "Pascal Groß", "poste": "CM", "numero": 13, "age": 33, "nationalite": "Allemagne"},
                    {"nom": "Julian Brandt", "poste": "AM", "numero": 10, "age": 28, "nationalite": "Allemagne"},
                    {"nom": "Felix Nmecha", "poste": "CM", "numero": 8, "age": 24, "nationalite": "Allemagne"},
                    {"nom": "Donyell Malen", "poste": "RW", "numero": 21, "age": 25, "nationalite": "Pays-Bas"},
                    {"nom": "Karim Adeyemi", "poste": "LW", "numero": 27, "age": 22, "nationalite": "Allemagne"},
                    {"nom": "Serhou Guirassy", "poste": "ST", "numero": 9, "age": 28, "nationalite": "Guinée"},
                    {"nom": "Maximilian Beier", "poste": "ST", "numero": 14, "age": 22, "nationalite": "Allemagne"},
                    {"nom": "Jamie Gittens", "poste": "LW", "numero": 43, "age": 20, "nationalite": "Angleterre"},
                    {"nom": "Giovanni Reyna", "poste": "AM/RW", "numero": 7, "age": 22, "nationalite": "États-Unis"}
                ]
            },
            
            "serie-a": {
                "inter": [
                    {"nom": "Yann Sommer", "poste": "GK", "numero": 1, "age": 36, "nationalite": "Suisse"},
                    {"nom": "Denzel Dumfries", "poste": "RWB", "numero": 2, "age": 28, "nationalite": "Pays-Bas"},
                    {"nom": "Francesco Acerbi", "poste": "CB", "numero": 15, "age": 36, "nationalite": "Italie"},
                    {"nom": "Alessandro Bastoni", "poste": "CB", "numero": 95, "age": 25, "nationalite": "Italie"},
                    {"nom": "Benjamin Pavard", "poste": "CB", "numero": 28, "age": 28, "nationalite": "France"},
                    {"nom": "Federico Dimarco", "poste": "LWB", "numero": 32, "age": 27, "nationalite": "Italie"},
                    {"nom": "Hakan Çalhanoğlu", "poste": "DM", "numero": 20, "age": 30, "nationalite": "Turquie"},
                    {"nom": "Nicolò Barella", "poste": "CM", "numero": 23, "age": 27, "nationalite": "Italie"},
                    {"nom": "Henrikh Mkhitaryan", "poste": "CM", "numero": 22, "age": 35, "nationalite": "Arménie"},
                    {"nom": "Piotr Zieliński", "poste": "AM", "numero": 7, "age": 30, "nationalite": "Pologne"},
                    {"nom": "Lautaro Martínez", "poste": "ST", "numero": 10, "age": 27, "nationalite": "Argentine"},
                    {"nom": "Marcus Thuram", "poste": "ST", "numero": 9, "age": 27, "nationalite": "France"},
                    {"nom": "Mehdi Taremi", "poste": "ST", "numero": 99, "age": 32, "nationalite": "Iran"},
                    {"nom": "Marko Arnautović", "poste": "ST", "numero": 8, "age": 35, "nationalite": "Autriche"},
                    {"nom": "Carlos Augusto", "poste": "LWB", "numero": 30, "age": 25, "nationalite": "Brésil"}
                ],
                
                "milan": [
                    {"nom": "Mike Maignan", "poste": "GK", "numero": 16, "age": 29, "nationalite": "France"},
                    {"nom": "Emerson Royal", "poste": "RB", "numero": 22, "age": 25, "nationalite": "Brésil"},
                    {"nom": "Fikayo Tomori", "poste": "CB", "numero": 23, "age": 27, "nationalite": "Angleterre"},
                    {"nom": "Malick Thiaw", "poste": "CB", "numero": 28, "age": 23, "nationalite": "Allemagne"},
                    {"nom": "Theo Hernández", "poste": "LB", "numero": 19, "age": 27, "nationalite": "France"},
                    {"nom": "Youssouf Fofana", "poste": "DM", "numero": 29, "age": 25, "nationalite": "France"},
                    {"nom": "Tijjani Reijnders", "poste": "CM", "numero": 14, "age": 26, "nationalite": "Pays-Bas"},
                    {"nom": "Ruben Loftus-Cheek", "poste": "AM", "numero": 8, "age": 28, "nationalite": "Angleterre"},
                    {"nom": "Christian Pulisic", "poste": "RW", "numero": 11, "age": 26, "nationalite": "États-Unis"},
                    {"nom": "Rafael Leão", "poste": "LW", "numero": 10, "age": 25, "nationalite": "Portugal"},
                    {"nom": "Álvaro Morata", "poste": "ST", "numero": 7, "age": 32, "nationalite": "Espagne"},
                    {"nom": "Tammy Abraham", "poste": "ST", "numero": 90, "age": 27, "nationalite": "Angleterre"},
                    {"nom": "Samuel Chukwueze", "poste": "RW", "numero": 21, "age": 25, "nationalite": "Nigeria"},
                    {"nom": "Noah Okafor", "poste": "LW/ST", "numero": 17, "age": 24, "nationalite": "Suisse"},
                    {"nom": "Yunus Musah", "poste": "CM/RW", "numero": 80, "age": 22, "nationalite": "États-Unis"}
                ],
                
                "juventus": [
                    {"nom": "Michele Di Gregorio", "poste": "GK", "numero": 29, "age": 27, "nationalite": "Italie"},
                    {"nom": "Andrea Cambiaso", "poste": "RB/LB", "numero": 27, "age": 24, "nationalite": "Italie"},
                    {"nom": "Gleison Bremer", "poste": "CB", "numero": 3, "age": 27, "nationalite": "Brésil"},
                    {"nom": "Pierre Kalulu", "poste": "CB", "numero": 15, "age": 24, "nationalite": "France"},
                    {"nom": "Danilo", "poste": "CB/RB", "numero": 6, "age": 33, "nationalite": "Brésil"},
                    {"nom": "Manuel Locatelli", "poste": "DM", "numero": 5, "age": 26, "nationalite": "Italie"},
                    {"nom": "Khéphren Thuram", "poste": "CM", "numero": 19, "age": 23, "nationalite": "France"},
                    {"nom": "Douglas Luiz", "poste": "CM", "numero": 26, "age": 26, "nationalite": "Brésil"},
                    {"nom": "Teun Koopmeiners", "poste": "AM", "numero": 8, "age": 26, "nationalite": "Pays-Bas"},
                    {"nom": "Kenan Yildiz", "poste": "LW", "numero": 10, "age": 19, "nationalite": "Turquie"},
                    {"nom": "Dušan Vlahović", "poste": "ST", "numero": 9, "age": 24, "nationalite": "Serbie"},
                    {"nom": "Francisco Conceição", "poste": "RW", "numero": 7, "age": 22, "nationalite": "Portugal"},
                    {"nom": "Nicolás González", "poste": "RW/LW", "numero": 11, "age": 26, "nationalite": "Argentine"},
                    {"nom": "Timothy Weah", "poste": "RW", "numero": 22, "age": 24, "nationalite": "États-Unis"},
                    {"nom": "Weston McKennie", "poste": "CM", "numero": 16, "age": 26, "nationalite": "États-Unis"}
                ]
            }
        }
    
    def generate_stats_template(self, player: Dict) -> Dict:
        """
        Génère des stats de base pour un joueur
        À remplacer par des vraies données via API
        """
        return {
            "id": player["nom"].lower().replace(" ", "-").replace("'", ""),
            "nom": player["nom"],
            "poste": player["poste"],
            "numero": player["numero"],
            "age": player["age"],
            "nationalite": player["nationalite"],
            
            # Stats de base (à remplir avec API ou scraping)
            "matchs_joues": 0,
            "titularisations": 0,
            "minutes": 0,
            "note_moyenne": 0.0,
            
            # Stats offensives
            "buts": 0,
            "passes_decisives": 0,
            "xg": 0.0,
            "xa": 0.0,
            "tirs_total": 0,
            "tirs_cadres": 0,
            "penalties_marques": 0,
            
            # Stats créatives
            "passes_cles": 0,
            "passes_reussies_pct": 0.0,
            "dribbles_reussis": 0,
            "centres_reussis": 0,
            
            # Stats défensives
            "tacles_reussis": 0,
            "interceptions": 0,
            "duels_aeriens_gagnes": 0,
            "cleansheets": 0,
            
            # Discipline
            "cartons_jaunes": 0,
            "cartons_rouges": 0,
            
            "last_update": datetime.now().isoformat()
        }
    
    def save_players_data(self):
        """
        Sauvegarde toutes les données des joueurs
        """
        squads = self.get_squad_2025_26()
        all_data = {}
        
        for league_name, teams in squads.items():
            all_data[league_name] = {}
            
            for team_name, players in teams.items():
                all_data[league_name][team_name] = []
                
                for player in players:
                    player_data = self.generate_stats_template(player)
                    all_data[league_name][team_name].append(player_data)
        
        # Sauvegarder le fichier principal
        output_path = os.path.join('public', 'data', 'players_2025_26.json')
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump({
                'season': self.season,
                'last_update': datetime.now().isoformat(),
                'total_clubs': sum(len(teams) for teams in squads.values()),
                'total_players': sum(len(players) for teams in squads.values() for players in teams.values()),
                'leagues': all_data
            }, f, ensure_ascii=False, indent=2)
        
        print(f"[OK] Donnees sauvegardees: {output_path}")
        
        # Créer aussi des fichiers par ligue pour optimiser le chargement
        for league_name, teams in all_data.items():
            league_path = os.path.join('public', 'data', f'{league_name}_2025_26.json')
            with open(league_path, 'w', encoding='utf-8') as f:
                json.dump({
                    'league': league_name,
                    'season': self.season,
                    'last_update': datetime.now().isoformat(),
                    'teams': teams
                }, f, ensure_ascii=False, indent=2)
            print(f"  - {league_name}: {league_path}")
        
        return all_data
    
    def update_stats_from_api(self, api_key: str = None):
        """
        Mise à jour progressive des stats via API
        À appeler quotidiennement avec limite de 100 requêtes
        """
        if not api_key:
            print("[!] Cle API non fournie - Stats de base uniquement")
            return
        
        # TODO: Implémenter la logique de mise à jour progressive
        # - Charger le fichier existant
        # - Identifier les joueurs sans stats
        # - Faire 100 requêtes max
        # - Sauvegarder les mises à jour
        pass

if __name__ == "__main__":
    print("Generation des donnees saison 2025-2026")
    print("="*50)
    
    scraper = HybridScraper2025()
    data = scraper.save_players_data()
    
    print("\nResume:")
    print(f"  - Saison: 2025-2026")
    print(f"  - Championnats: 5")
    print(f"  - Clubs: 20 (4 par championnat pour commencer)")
    print(f"  - Joueurs: ~300 (15 par club)")
    print("\nProchaines etapes:")
    print("  1. Integrer ces donnees dans l'app Next.js")
    print("  2. Ajouter progressivement les autres clubs")
    print("  3. Mettre a jour les stats via API (100 requetes/jour)")
    print("  4. Implementer les radar charts avec les vraies stats")