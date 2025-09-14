const express = require('express');
const router = express.Router();
const sportmonks = require('../api/sportmonks');
const { Team, Player } = require('../utils/database');

// Get team by ID or slug
router.get('/:teamIdentifier', async (req, res) => {
    try {
        const { teamIdentifier } = req.params;
        
        // Check if it's a number (ID) or string (slug)
        let team;
        if (!isNaN(teamIdentifier)) {
            // It's an ID
            team = await Team.findOne({ sportmonksId: parseInt(teamIdentifier) });
        } else {
            // It's a slug
            team = await Team.findOne({ slug: teamIdentifier });
        }
        
        if (!team && !isNaN(teamIdentifier)) {
            // Fetch from API
            const apiTeam = await sportmonks.getTeam(teamIdentifier);
            
            team = new Team({
                sportmonksId: teamIdentifier,
                name: apiTeam.data.name,
                slug: apiTeam.data.name.toLowerCase().replace(/\s+/g, '-'),
                shortName: apiTeam.data.short_code,
                logo: apiTeam.data.logo_path,
                venue: {
                    name: apiTeam.data.venue?.data?.name,
                    capacity: apiTeam.data.venue?.data?.capacity,
                    city: apiTeam.data.venue?.data?.city
                },
                founded: apiTeam.data.founded,
                coach: {
                    name: apiTeam.data.coach?.data?.fullname,
                    nationality: apiTeam.data.coach?.data?.nationality,
                    image: apiTeam.data.coach?.data?.image_path
                }
            });
            
            await team.save();
        }
        
        res.json({
            success: true,
            data: team
        });
    } catch (error) {
        res.status(500).json({
            success: false,
            error: error.message
        });
    }
});

// Get team statistics
router.get('/:teamIdentifier/statistics', async (req, res) => {
    try {
        const { teamIdentifier } = req.params;
        
        // Find team by slug or ID
        let team;
        if (!isNaN(teamIdentifier)) {
            team = await Team.findOne({ sportmonksId: teamIdentifier });
        } else {
            team = await Team.findOne({ slug: teamIdentifier });
        }
        
        const teamId = team ? team.sportmonksId : teamIdentifier;
        const { season = '25651' } = req.query; // Default to Ligue 1 2025/2026
        
        const statistics = await sportmonks.getTeamStatistics(teamId, season);
        
        // Map statistics to our format
        const mappedStats = {
            rating: statistics.data.details?.find(s => s.type_id === 118)?.value || 0,
            gamesPlayed: statistics.data.details?.find(s => s.type_id === 27263)?.value || 0,
            averagePointsPerGame: statistics.data.details?.find(s => s.type_id === 9676)?.value || 0,
            averagePlayerAge: statistics.data.details?.find(s => s.type_id === 9673)?.value || 0,
            teamWins: statistics.data.details?.find(s => s.type_id === 214)?.value || 0,
            teamDraws: statistics.data.details?.find(s => s.type_id === 215)?.value || 0,
            teamLost: statistics.data.details?.find(s => s.type_id === 216)?.value || 0,
            goalsScored: statistics.data.details?.find(s => s.type_id === 191)?.value || 0,
            goalsConceded: statistics.data.details?.find(s => s.type_id === 88)?.value || 0,
            cleanSheets: statistics.data.details?.find(s => s.type_id === 194)?.value || 0,
            redCards: statistics.data.details?.find(s => s.type_id === 83)?.value || 0,
            highestRatedPlayer: statistics.data.details?.find(s => s.type_id === 211)?.value || null
        };
        
        // Update team in database
        await Team.findOneAndUpdate(
            { sportmonksId: teamId },
            { 
                statistics: mappedStats,
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

// Get team squad
router.get('/:teamIdentifier/squad', async (req, res) => {
    try {
        const { teamIdentifier } = req.params;
        
        // Find team by slug or ID
        let team;
        if (!isNaN(teamIdentifier)) {
            team = await Team.findOne({ sportmonksId: teamIdentifier });
        } else {
            team = await Team.findOne({ slug: teamIdentifier });
        }
        
        const teamId = team ? team.sportmonksId : teamIdentifier;
        const { season = '25651' } = req.query;
        
        // First try to get from database
        let players = await Player.find({ 
            'team.sportmonksId': parseInt(teamId)
        });
        
        if (players.length === 0) {
            // Try with team slug
            players = await Player.find({
                'team.slug': teamIdentifier
            });
        }
        
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