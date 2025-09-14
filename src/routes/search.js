const express = require('express');
const router = express.Router();
const { League, Team, Player } = require('../utils/database');

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
            const allLeagues = await League.find();
            results.leagues = allLeagues
                .filter(l => searchRegex.test(l.name) || searchRegex.test(l.country))
                .slice(0, limit);
        }
        
        // Search teams
        if (type === 'all' || type === 'team') {
            const allTeams = await Team.find();
            results.teams = allTeams
                .filter(t => searchRegex.test(t.name) || (t.shortName && searchRegex.test(t.shortName)))
                .slice(0, limit);
        }
        
        // Search players
        if (type === 'all' || type === 'player') {
            const allPlayers = await Player.find();
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

// Autocomplete suggestions
router.get('/suggestions', async (req, res) => {
    try {
        const { q } = req.query;
        
        if (!q || q.length < 2) {
            return res.json({
                success: true,
                data: []
            });
        }
        
        const searchRegex = new RegExp(`^${q}`, 'i');
        const suggestions = [];
        
        // Get top 3 from each category
        const allLeagues = await League.find();
        const allTeams = await Team.find();
        const allPlayers = await Player.find();
        
        const leagues = allLeagues
            .filter(l => searchRegex.test(l.name))
            .slice(0, 3);
        const teams = allTeams
            .filter(t => searchRegex.test(t.name))
            .slice(0, 3);
        const players = allPlayers
            .filter(p => searchRegex.test(p.name))
            .slice(0, 4);
        
        leagues.forEach(l => suggestions.push({
            type: 'league',
            id: l.slug,
            name: l.name,
            url: `/league/${l.slug}`
        }));
        
        teams.forEach(t => suggestions.push({
            type: 'team',
            id: t.sportmonksId,
            name: t.name,
            url: `/team/${t.slug}`
        }));
        
        players.forEach(p => suggestions.push({
            type: 'player',
            id: p.sportmonksId,
            name: p.name,
            url: `/player/${p.sportmonksId}`
        }));
        
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

module.exports = router;