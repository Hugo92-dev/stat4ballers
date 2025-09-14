const express = require('express');
const router = express.Router();
const sportmonks = require('../api/sportmonks');
const { League, Team } = require('../utils/database');

// League IDs mapping
const LEAGUE_IDS = {
    'ligue1': { current: 25651, previous: [23643, 21779] },
    'premierleague': { current: 25583, previous: [23614, 21646] },
    'laliga': { current: 25659, previous: [23621, 21694] },
    'liga': { current: 25659, previous: [23621, 21694] },
    'seriea': { current: 25533, previous: [23746, 21818] },
    'bundesliga': { current: 25646, previous: [23744, 21795] }
};

// Get all leagues
router.get('/', async (req, res) => {
    try {
        const leagues = await League.find().select('-__v');
        res.json({
            success: true,
            data: leagues
        });
    } catch (error) {
        res.status(500).json({
            success: false,
            error: error.message
        });
    }
});

// Get specific league
router.get('/:leagueSlug', async (req, res) => {
    try {
        const { leagueSlug } = req.params;
        const { season } = req.query;
        
        let league = await League.findOne({ slug: leagueSlug }).populate('teams');
        
        if (!league) {
            // Fetch from API if not in database
            const leagueConfig = LEAGUE_IDS[leagueSlug];
            if (!leagueConfig) {
                return res.status(404).json({
                    success: false,
                    error: 'League not found'
                });
            }
            
            const seasonId = season === 'current' ? leagueConfig.current : leagueConfig.current;
            const apiData = await sportmonks.getSeasonData(leagueConfig.current, seasonId);
            
            // Store in database
            league = new League({
                sportmonksId: leagueConfig.current,
                name: apiData.league.data.name,
                slug: leagueSlug,
                country: apiData.league.data.country.data.name,
                logo: apiData.league.data.logo_path,
                seasons: [{
                    id: seasonId,
                    name: '2025/2026',
                    year: '2025',
                    isCurrent: true
                }]
            });
            
            await league.save();
        }
        
        res.json({
            success: true,
            data: league
        });
    } catch (error) {
        res.status(500).json({
            success: false,
            error: error.message
        });
    }
});

// Get league standings
router.get('/:leagueSlug/standings', async (req, res) => {
    try {
        const { leagueSlug } = req.params;
        const { season = 'current' } = req.query;
        
        const leagueConfig = LEAGUE_IDS[leagueSlug];
        if (!leagueConfig) {
            return res.status(404).json({
                success: false,
                error: 'League not found'
            });
        }
        
        const seasonId = season === 'current' ? leagueConfig.current : leagueConfig.current;
        const standings = await sportmonks.getSeasonStandings(seasonId);
        
        res.json({
            success: true,
            data: standings
        });
    } catch (error) {
        res.status(500).json({
            success: false,
            error: error.message
        });
    }
});

// Get league teams
router.get('/:leagueSlug/teams', async (req, res) => {
    try {
        const { leagueSlug } = req.params;
        const { season = 'current' } = req.query;
        
        console.log('Fetching teams for league:', leagueSlug);
        const teams = await Team.find({ 
            league: leagueSlug 
        });
        console.log('Found teams:', teams.length);
        
        if (teams.length === 0) {
            // Fetch from API
            const leagueConfig = LEAGUE_IDS[leagueSlug];
            if (!leagueConfig) {
                return res.status(404).json({
                    success: false,
                    error: 'League not found'
                });
            }
            
            const seasonId = season === 'current' ? leagueConfig.current : leagueConfig.current;
            const apiTeams = await sportmonks.getSeasonTeams(seasonId);
            
            res.json({
                success: true,
                data: apiTeams
            });
        } else {
            res.json({
                success: true,
                data: teams
            });
        }
    } catch (error) {
        res.status(500).json({
            success: false,
            error: error.message
        });
    }
});

module.exports = router;