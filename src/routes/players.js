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

        // Complete statistics based on player statistics
        const stats = player.statistics || {};
        const isGoalkeeper = player.position === 'Goalkeeper' || player.isGoalkeeper || false;

        let radarData;

        if (isGoalkeeper) {
            // Goalkeeper: General (without goals, assists, injuries) + Specific goalkeeper stats
            radarData = {
                general: {
                    rating: stats.rating || 0,
                    appearances: stats.appearances || 0,
                    minutesPlayed: stats.minutesPlayed || 0,
                    captain: stats.captain || 0,
                    redCards: stats.redCards || 0
                },
                goalkeeper: {
                    saves: stats.saves || 0,
                    savesInsideBox: stats.savesInsideBox || 0,
                    goalsConceded: stats.goalsConceded || 0,
                    cleanSheets: stats.cleanSheets || 0
                }
            };
        } else {
            // Field players: All 3 categories (General, Offensive, Defensive)
            radarData = {
                general: {
                    rating: stats.rating || 0,
                    appearances: stats.appearances || 0,
                    minutesPlayed: stats.minutesPlayed || 0,
                    captain: stats.captain || 0,
                    goals: stats.goals || 0,
                    assists: stats.assists || 0,
                    injuries: stats.injuries || 0,
                    redCards: stats.redCards || 0
                },
                offensive: {
                    shotsTotal: stats.shotsTotal || 0,
                    shotsOnTarget: stats.shotsOnTarget || 0,
                    penalties: stats.penalties || 0,
                    hitWoodwork: stats.hitWoodwork || 0,
                    keyPasses: stats.keyPasses || 0,
                    bigChancesCreated: stats.bigChancesCreated || 0,
                    expectedGoals: stats.expectedGoals || 0,
                    throughBallsWon: stats.throughBallsWon || 0,
                    longBallsWon: stats.longBallsWon || 0,
                    accurateCrosses: stats.accurateCrosses || 0,
                    successfulDribbles: stats.successfulDribbles || 0
                },
                defensive: {
                    yellowCards: stats.yellowCards || 0,
                    tackles: stats.tackles || 0,
                    ownGoals: stats.ownGoals || 0,
                    interceptions: stats.interceptions || 0,
                    duelsWon: stats.duelsWon || 0,
                    aerialsWon: stats.aerialsWon || 0,
                    dispossessed: stats.dispossessed || 0,
                    dribbledPast: stats.dribbledPast || 0,
                    fouls: stats.fouls || 0,
                    foulsDrawn: stats.foulsDrawn || 0,
                    errorLeadToGoal: stats.errorLeadToGoal || 0
                }
            };
        }

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