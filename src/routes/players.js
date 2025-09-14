const express = require('express');
const router = express.Router();
const sportmonks = require('../api/sportmonks');
const { Player } = require('../utils/database');

// Get player by ID
router.get('/:playerId', async (req, res) => {
    try {
        const { playerId } = req.params;
        
        let player = await Player.findOne({ sportmonksId: playerId })
            .populate('team', 'name slug logo');
        
        if (!player) {
            // Fetch from API
            const apiPlayer = await sportmonks.getPlayer(playerId);
            
            player = new Player({
                sportmonksId: playerId,
                name: apiPlayer.data.display_name || apiPlayer.data.fullname,
                slug: (apiPlayer.data.display_name || apiPlayer.data.fullname).toLowerCase().replace(/\s+/g, '-'),
                firstName: apiPlayer.data.firstname,
                lastName: apiPlayer.data.lastname,
                displayName: apiPlayer.data.display_name,
                image: apiPlayer.data.image_path,
                dateOfBirth: apiPlayer.data.birthdate,
                age: apiPlayer.data.age,
                height: apiPlayer.data.height,
                weight: apiPlayer.data.weight,
                nationality: apiPlayer.data.nationality,
                position: apiPlayer.data.position?.data?.name || 'Unknown',
                detailedPosition: apiPlayer.data.detailed_position?.data?.name,
                jerseyNumber: apiPlayer.data.jersey_number
            });
            
            await player.save();
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
router.get('/:playerId/statistics', async (req, res) => {
    try {
        const { playerId } = req.params;
        const { season = '25651' } = req.query;
        
        const statistics = await sportmonks.getPlayerStatistics(playerId, season);
        const mappedStats = sportmonks.mapPlayerStatistics(statistics.data.details || []);
        
        // Update player in database
        await Player.findOneAndUpdate(
            { sportmonksId: playerId },
            { 
                statistics: mappedStats,
                currentSeason: season,
                lastUpdated: new Date()
            }
        );
        
        res.json({
            success: true,
            data: mappedStats
        });
    } catch (error) {
        res.status(500).json({
            success: false,
            error: error.message
        });
    }
});

// Get player radar chart data
router.get('/:playerId/radar', async (req, res) => {
    try {
        const { playerId } = req.params;
        
        const player = await Player.findOne({ sportmonksId: playerId });
        
        if (!player) {
            return res.status(404).json({
                success: false,
                error: 'Player not found'
            });
        }
        
        const radarData = player.getRadarChartData();
        
        res.json({
            success: true,
            data: {
                playerId: player.sportmonksId,
                name: player.name,
                position: player.position,
                isGoalkeeper: player.isGoalkeeper(),
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
        
        const players = await Player.find({ 
            sportmonksId: { $in: playerIds } 
        });
        
        const comparisonData = players.map(player => ({
            playerId: player.sportmonksId,
            name: player.name,
            team: player.team?.name,
            position: player.position,
            image: player.image,
            isGoalkeeper: player.isGoalkeeper(),
            charts: player.getRadarChartData()
        }));
        
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