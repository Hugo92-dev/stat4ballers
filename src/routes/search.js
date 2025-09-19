const express = require('express');
const router = express.Router();
const { find } = require('../utils/database');

// Fonction utilitaire pour normaliser les textes avec caractères spéciaux
function normalizeText(text) {
    if (!text) return '';
    return text
        .normalize('NFD')
        .replace(/[\u0300-\u036f]/g, '')
        // Caractères scandinaves spécifiques
        .replace(/[øØ]/g, 'o')
        .replace(/[æÆ]/g, 'ae')
        .replace(/[åÅ]/g, 'a')
        // Caractères allemands
        .replace(/[ßẞ]/g, 'ss')
        .replace(/[üÜ]/g, 'u')
        .replace(/[öÖ]/g, 'o')
        .replace(/[äÄ]/g, 'a')
        // Caractères slaves
        .replace(/[čČ]/g, 'c')
        .replace(/[šŠ]/g, 's')
        .replace(/[žŽ]/g, 'z')
        .replace(/[đĐ]/g, 'd')
        .replace(/[ćĆ]/g, 'c')
        .replace(/[ñÑ]/g, 'n')
        .toLowerCase();
}

// Global search with autocomplete
router.get('/', async (req, res) => {
    try {
        const { q, type = 'all', limit = 10 } = req.query;
        
        if (!q || q.length < 2) {
            return res.status(400).json({
                success: false,
                error: 'Search query must be at least 2 characters'
            });
        }
        
        const searchRegex = new RegExp(q, 'i');
        const results = {
            leagues: [],
            teams: [],
            players: []
        };
        
        // Search leagues
        if (type === 'all' || type === 'league') {
            const allLeagues = await find('leagues');
            results.leagues = allLeagues
                .filter(l => searchRegex.test(l.name) || searchRegex.test(l.country))
                .slice(0, limit);
        }

        // Search teams
        if (type === 'all' || type === 'team') {
            const allTeams = await find('teams');
            results.teams = allTeams
                .filter(t => searchRegex.test(t.name) || (t.shortName && searchRegex.test(t.shortName)))
                .slice(0, limit);
        }

        // Search players
        if (type === 'all' || type === 'player') {
            const allPlayers = await find('players');
            results.players = allPlayers
                .filter(p => searchRegex.test(p.name) ||
                            (p.firstName && searchRegex.test(p.firstName)) ||
                            (p.lastName && searchRegex.test(p.lastName)))
                .slice(0, limit);
        }
        
        res.json({
            success: true,
            data: results
        });
    } catch (error) {
        res.status(500).json({
            success: false,
            error: error.message
        });
    }
});

// Autocomplete suggestions pour la recherche globale
router.get('/suggestions', async (req, res) => {
    try {
        const { q } = req.query;

        if (!q || q.length < 2) {
            return res.json({
                success: true,
                data: []
            });
        }

        // Normaliser la recherche pour gérer les caractères spéciaux et scandinaves
        const normalizedQuery = normalizeText(q);

        // Créer une regex pour la recherche
        const searchRegex = new RegExp(normalizedQuery, 'i');
        const suggestions = [];

        // Championnats statiques
        const leagues = [
            { id: 'ligue1', name: 'Ligue 1', slug: 'ligue1' },
            { id: 'premierleague', name: 'Premier League', slug: 'premierleague' },
            { id: 'laliga', name: 'La Liga', slug: 'laliga' },
            { id: 'seriea', name: 'Serie A', slug: 'seriea' },
            { id: 'bundesliga', name: 'Bundesliga', slug: 'bundesliga' }
        ];

        // Filtrer les championnats
        leagues
            .filter(l => searchRegex.test(l.name))
            .slice(0, 3)
            .forEach(l => suggestions.push({
                type: 'League',
                id: l.id,
                name: l.name,
                url: `/league/${l.slug}`
            }));

        // Récupérer les équipes et joueurs depuis la base
        const allTeams = await find('teams');
        const allPlayers = await find('players');

        // Filtrer les équipes principales des 5 championnats et supprimer les doublons
        const teamSlugs = new Set();
        const mainLeagues = ['ligue1', 'premierleague', 'laliga', 'seriea', 'bundesliga'];

        // Priorité aux équipes des championnats principaux avec slug défini
        const mainTeams = allTeams
            .filter(t => {
                // Prioriser les équipes avec un league défini (équipes principales)
                if (!t.league || !mainLeagues.includes(t.league)) return false;
                // Vérifier si le nom correspond et qu'il y a un slug
                return t.slug && searchRegex.test(normalizeText(t.name));
            })
            .sort((a, b) => {
                // Trier par ordre de priorité des championnats
                const leagueOrder = { 'ligue1': 1, 'premierleague': 2, 'laliga': 3, 'seriea': 4, 'bundesliga': 5 };
                return (leagueOrder[a.league] || 999) - (leagueOrder[b.league] || 999);
            });

        // Ajouter les équipes principales (une seule par nom similaire)
        const teamNormalizedNames = new Set();
        const teamBaseNames = new Set(); // Pour détecter les variations comme "Olympique Marseille" vs "Olympique de Marseille"

        mainTeams.forEach(t => {
            const normalizedName = normalizeText(t.name);
            // Créer un nom de base en supprimant les mots courants comme "de", "du", "des", "da", "del", etc.
            const baseName = normalizedName
                .replace(/\b(de|du|des|da|del|della|di|das|den|der|die)\b/g, '')
                .replace(/\s+/g, ' ')
                .trim();

            if (!teamNormalizedNames.has(normalizedName) && !teamBaseNames.has(baseName) && !teamSlugs.has(t.slug)) {
                teamNormalizedNames.add(normalizedName);
                teamBaseNames.add(baseName);
                teamSlugs.add(t.slug);
                suggestions.push({
                    type: 'Team',
                    id: t.sportmonksId,
                    name: t.name,
                    url: `/team/${t.slug}`
                });
            }
        });

        // Si on a moins de 5 équipes principales, compléter avec d'autres équipes des ligues principales uniquement
        if (suggestions.filter(s => s.type === 'Team').length < 5) {
            allTeams
                .filter(t => {
                    if (!t.slug) return false;
                    if (teamSlugs.has(t.slug)) return false;
                    // Éviter les équipes sans league défini ou avec des noms déjà trouvés
                    const normalizedName = normalizeText(t.name);
                    const baseName = normalizedName
                        .replace(/\b(de|du|des|da|del|della|di|das|den|der|die)\b/g, '')
                        .replace(/\s+/g, ' ')
                        .trim();
                    if (teamNormalizedNames.has(normalizedName) || teamBaseNames.has(baseName)) return false;
                    // Chercher uniquement dans les équipes avec un ID connu des 5 ligues principales
                    const mainLeagueTeamIds = [
                        // Quelques IDs supplémentaires des équipes principales si nécessaire
                        // Mais en priorité, ne montrer que les équipes avec league défini
                    ];
                    return searchRegex.test(normalizeText(t.name));
                })
                .slice(0, 5 - suggestions.filter(s => s.type === 'Team').length)
                .forEach(t => {
                    const normalizedName = normalizeText(t.name);
                    const baseName = normalizedName
                        .replace(/\b(de|du|des|da|del|della|di|das|den|der|die)\b/g, '')
                        .replace(/\s+/g, ' ')
                        .trim();

                    if (!teamSlugs.has(t.slug) && !teamNormalizedNames.has(normalizedName) && !teamBaseNames.has(baseName)) {
                        teamSlugs.add(t.slug);
                        teamNormalizedNames.add(normalizedName);
                        teamBaseNames.add(baseName);
                        suggestions.push({
                            type: 'Team',
                            id: t.sportmonksId,
                            name: t.name,
                            url: `/team/${t.slug}`
                        });
                    }
                });
        }

        // Filtrer les joueurs
        allPlayers
            .filter(p => {
                const playerName = normalizeText(p.name);
                const playerDisplayName = p.displayName ? normalizeText(p.displayName) : '';
                return playerName.includes(normalizedQuery) || playerDisplayName.includes(normalizedQuery);
            })
            .slice(0, 7)
            .forEach(p => {
                const slug = p.name.toLowerCase()
                    .normalize('NFD')
                    .replace(/[\u0300-\u036f]/g, '')
                    .replace(/\s+/g, '-')
                    .replace(/[^a-z0-9\-]/g, '');
                suggestions.push({
                    type: 'Player',
                    id: p.sportmonksId,
                    name: p.displayName || p.name,
                    url: `/player/${slug}` // Changé de /joueur/ à /player/
                });
            });

        res.json({
            success: true,
            data: suggestions
        });
    } catch (error) {
        res.status(500).json({
            success: false,
            error: error.message
        });
    }
});

// Endpoint pour l'autocomplétion des joueurs (pour la comparaison)
router.get('/players', async (req, res) => {
    try {
        const { q } = req.query;

        if (!q || q.length < 2) {
            return res.json({
                success: true,
                data: []
            });
        }

        // Normaliser la recherche
        const normalizedQuery = normalizeText(q);

        const allPlayers = await find('players');

        const players = allPlayers
            .filter(p => {
                const playerName = normalizeText(p.name);
                const playerDisplayName = p.displayName ? normalizeText(p.displayName) : '';
                return playerName.includes(normalizedQuery) || playerDisplayName.includes(normalizedQuery);
            })
            .slice(0, 10)
            .map(p => ({
                id: p.sportmonksId,
                name: p.displayName || p.name,
                team: p.team ? p.team.name : '',
                position: p.position
            }));

        res.json({
            success: true,
            data: players
        });
    } catch (error) {
        res.status(500).json({
            success: false,
            error: error.message
        });
    }
});

module.exports = router;