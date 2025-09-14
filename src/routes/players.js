const express = require('express');
const router = express.Router();
const sportmonks = require('../api/sportmonks');
const { find, findOne } = require('../utils/database');

// Get player by slug
router.get('/:playerSlug', async (req, res) => {
    try {
        const { playerSlug } = req.params;

        // Search in local JSON database by slug
        let player = await findOne('players', { slug: playerSlug });

        if (!player) {
            return res.status(404).json({
                success: false,
                error: 'Player not found'
            });
        }

        res.json({
            success: true,
            data: player
        });
    } catch (error) {
        res.status(500).json({
            success: false,
            error: error.message
        });
    }
});

// Get player statistics
router.get('/:playerSlug/statistics', async (req, res) => {
    try {
        const { playerSlug } = req.params;
        const { season = '2025' } = req.query;

        const player = await findOne('players', { slug: playerSlug });

        if (!player) {
            return res.status(404).json({
                success: false,
                error: 'Player not found'
            });
        }

        // Return existing statistics from player data
        const stats = player.statistics || {
            rating: 0,
            appearances: 0,
            goals: 0,
            assists: 0,
            minutesPlayed: 0,
            yellowCards: 0,
            redCards: 0
        };

        res.json({
            success: true,
            data: stats
        });
    } catch (error) {
        res.status(500).json({
            success: false,
            error: error.message
        });
    }
});

// Get player radar chart data
router.get('/:playerSlug/radar', async (req, res) => {
    try {
        const { playerSlug } = req.params;

        const player = await findOne('players', { slug: playerSlug });

        if (!player) {
            return res.status(404).json({
                success: false,
                error: 'Player not found'
            });
        }

        // Simple radar data based on player statistics
        const stats = player.statistics || {};
        const isGoalkeeper = player.isGoalkeeper || false;

        const radarData = isGoalkeeper ? {
            general: {
                saves: stats.saves || 0,
                cleanSheets: stats.cleanSheets || 0,
                appearances: stats.appearances || 0,
                rating: stats.rating || 0
            }
        } : {
            general: {
                goals: stats.goals || 0,
                assists: stats.assists || 0,
                appearances: stats.appearances || 0,
                rating: stats.rating || 0
            },
            offensive: {
                goals: stats.goals || 0,
                assists: stats.assists || 0,
                shots: stats.shots || 0
            },
            defensive: {
                tackles: stats.tackles || 0,
                blocks: stats.blocks || 0,
                interceptions: stats.interceptions || 0
            }
        };

        res.json({
            success: true,
            data: {
                playerId: player.sportmonksId,
                name: player.name,
                position: player.position,
                isGoalkeeper: isGoalkeeper,
                charts: radarData
            }
        });
    } catch (error) {
        res.status(500).json({
            success: false,
            error: error.message
        });
    }
});

// Compare multiple players
router.post('/compare', async (req, res) => {
    try {
        const { playerIds } = req.body;

        if (!playerIds || playerIds.length < 2 || playerIds.length > 4) {
            return res.status(400).json({
                success: false,
                error: 'Please provide between 2 and 4 player IDs'
            });
        }

        const players = [];
        for (const id of playerIds) {
            const player = await findOne('players', { sportmonksId: parseInt(id) });
            if (player) players.push(player);
        }

        const comparisonData = players.map(player => {
            const stats = player.statistics || {};
            const isGoalkeeper = player.isGoalkeeper || false;

            return {
                playerId: player.sportmonksId,
                name: player.name,
                team: player.team?.name,
                position: player.position,
                image: player.image,
                isGoalkeeper: isGoalkeeper,
                charts: isGoalkeeper ? {
                    general: {
                        saves: stats.saves || 0,
                        cleanSheets: stats.cleanSheets || 0,
                        appearances: stats.appearances || 0,
                        rating: stats.rating || 0
                    }
                } : {
                    general: {
                        goals: stats.goals || 0,
                        assists: stats.assists || 0,
                        appearances: stats.appearances || 0,
                        rating: stats.rating || 0
                    }
                }
            };
        });

        res.json({
            success: true,
            data: comparisonData
        });
    } catch (error) {
        res.status(500).json({
            success: false,
            error: error.message
        });
    }
});

module.exports = router;