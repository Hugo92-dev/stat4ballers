const sportmonks = require('../api/sportmonks');
const League = require('../models/League');
const Team = require('../models/Team');
const Player = require('../models/Player');
const fs = require('fs').promises;
const path = require('path');

// League configurations
const LEAGUES = {
    ligue1: { 
        name: 'Ligue 1',
        currentSeason: 25651,
        teams: [44, 59, 79, 266, 271, 289, 450, 591, 598, 686, 690, 776, 1055, 3513, 3682, 4508, 6789, 9257]
    },
    premierleague: {
        name: 'Premier League',
        currentSeason: 25583,
        teams: [1, 3, 6, 8, 9, 11, 13, 14, 15, 18, 19, 20, 27, 29, 51, 52, 63, 71, 78, 236]
    },
    liga: {
        name: 'La Liga',
        currentSeason: 25659,
        teams: [36, 83, 93, 106, 214, 231, 377, 459, 485, 528, 594, 645, 676, 1099, 2975, 3457, 3468, 3477, 7980, 13258]
    },
    seriea: {
        name: 'Serie A',
        currentSeason: 25533,
        teams: [37, 43, 102, 109, 113, 268, 346, 398, 585, 597, 613, 625, 708, 1072, 1123, 2714, 2930, 7790, 8513, 10722]
    },
    bundesliga: {
        name: 'Bundesliga',
        currentSeason: 25646,
        teams: [68, 82, 90, 277, 353, 366, 503, 510, 683, 794, 1079, 2708, 2726, 2831, 3319, 3320, 3321, 3543]
    }
};

// Main refresh function
async function refreshLeague(leagueKey) {
    const league = LEAGUES[leagueKey];
    if (!league) {
        console.error(`League ${leagueKey} not found`);
        return;
    }

    console.log(`🔄 Starting refresh for ${league.name}...`);
    
    try {
        // Create backup before refresh
        await createBackup(leagueKey);
        
        // Refresh teams
        console.log(`📊 Fetching teams for ${league.name}...`);
        for (const teamId of league.teams) {
            await refreshTeam(teamId, league.currentSeason, leagueKey);
            await delay(500); // Respect rate limits
        }
        
        console.log(`✅ ${league.name} refresh completed successfully!`);
        
        // Log refresh
        await logRefresh(leagueKey, 'success');
    } catch (error) {
        console.error(`❌ Error refreshing ${league.name}:`, error.message);
        await logRefresh(leagueKey, 'error', error.message);
        throw error;
    }
}

// Refresh individual team
async function refreshTeam(teamId, seasonId, leagueKey) {
    try {
        console.log(`  → Fetching team ${teamId}...`);
        
        // Get team data
        const teamData = await sportmonks.getTeam(teamId);
        
        // Get team statistics
        const teamStats = await sportmonks.getTeamStatistics(teamId, seasonId);
        
        // Get team squad
        const squad = await sportmonks.getTeamSquad(teamId, seasonId);
        
        // Update or create team in database
        const team = await Team.findOneAndUpdate(
            { sportmonksId: teamId },
            {
                sportmonksId: teamId,
                name: teamData.data.name,
                slug: teamData.data.name.toLowerCase().replace(/\s+/g, '-'),
                shortName: teamData.data.short_code,
                logo: teamData.data.logo_path,
                venue: {
                    name: teamData.data.venue?.data?.name,
                    capacity: teamData.data.venue?.data?.capacity,
                    city: teamData.data.venue?.data?.city
                },
                founded: teamData.data.founded,
                statistics: mapTeamStatistics(teamStats.data),
                lastUpdated: new Date()
            },
            { upsert: true, new: true }
        );
        
        // Refresh players
        if (squad.data && squad.data.squad) {
            for (const playerData of squad.data.squad.data) {
                await refreshPlayer(playerData.player.data, teamId, seasonId);
                await delay(200);
            }
        }
        
        console.log(`    ✓ Team ${team.name} updated`);
    } catch (error) {
        console.error(`    ✗ Failed to refresh team ${teamId}:`, error.message);
    }
}

// Refresh individual player
async function refreshPlayer(playerData, teamId, seasonId) {
    try {
        const playerId = playerData.id;
        
        // Get player statistics
        const playerStats = await sportmonks.getPlayerStatistics(playerId, seasonId);
        const mappedStats = sportmonks.mapPlayerStatistics(playerStats.data?.details || []);
        
        // Update or create player in database
        await Player.findOneAndUpdate(
            { sportmonksId: playerId },
            {
                sportmonksId: playerId,
                name: playerData.display_name || playerData.fullname,
                slug: (playerData.display_name || playerData.fullname).toLowerCase().replace(/\s+/g, '-'),
                firstName: playerData.firstname,
                lastName: playerData.lastname,
                displayName: playerData.display_name,
                image: playerData.image_path,
                dateOfBirth: playerData.birthdate,
                age: playerData.age,
                height: playerData.height,
                weight: playerData.weight,
                nationality: playerData.nationality,
                position: playerData.position?.data?.name || 'Unknown',
                detailedPosition: playerData.detailed_position?.data?.name,
                jerseyNumber: playerData.jersey_number,
                currentSeason: seasonId,
                statistics: mappedStats,
                lastUpdated: new Date()
            },
            { upsert: true }
        );
    } catch (error) {
        console.error(`      ✗ Failed to refresh player ${playerData.id}:`, error.message);
    }
}

// Map team statistics
function mapTeamStatistics(data) {
    const details = data.details || [];
    return {
        rating: details.find(s => s.type_id === 118)?.value || 0,
        gamesPlayed: details.find(s => s.type_id === 27263)?.value || 0,
        averagePointsPerGame: details.find(s => s.type_id === 9676)?.value || 0,
        averagePlayerAge: details.find(s => s.type_id === 9673)?.value || 0,
        teamWins: details.find(s => s.type_id === 214)?.value || 0,
        teamDraws: details.find(s => s.type_id === 215)?.value || 0,
        teamLost: details.find(s => s.type_id === 216)?.value || 0,
        goalsScored: details.find(s => s.type_id === 191)?.value || 0,
        goalsConceded: details.find(s => s.type_id === 88)?.value || 0,
        cleanSheets: details.find(s => s.type_id === 194)?.value || 0,
        redCards: details.find(s => s.type_id === 83)?.value || 0,
        highestRatedPlayer: details.find(s => s.type_id === 211)?.value || null
    };
}

// Create backup before refresh
async function createBackup(leagueKey) {
    try {
        const backupDir = path.join(__dirname, '../../data/backup');
        await fs.mkdir(backupDir, { recursive: true });
        
        const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
        const backupFile = path.join(backupDir, `${leagueKey}_${timestamp}.json`);
        
        // Get current data
        const teams = await Team.find({ 'league.slug': leagueKey }).lean();
        const teamIds = teams.map(t => t._id);
        const players = await Player.find({ team: { $in: teamIds } }).lean();
        
        const backupData = {
            timestamp,
            league: leagueKey,
            teams,
            players
        };
        
        await fs.writeFile(backupFile, JSON.stringify(backupData, null, 2));
        console.log(`📁 Backup created: ${backupFile}`);
    } catch (error) {
        console.error('Failed to create backup:', error.message);
    }
}

// Log refresh operation
async function logRefresh(leagueKey, status, error = null) {
    try {
        const logDir = path.join(__dirname, '../../data/logs');
        await fs.mkdir(logDir, { recursive: true });
        
        const logFile = path.join(logDir, 'refresh.log');
        const logEntry = {
            timestamp: new Date().toISOString(),
            league: leagueKey,
            status,
            error
        };
        
        await fs.appendFile(logFile, JSON.stringify(logEntry) + '\n');
    } catch (err) {
        console.error('Failed to write log:', err.message);
    }
}

// Utility delay function
function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

// Run from command line
if (require.main === module) {
    const leagueArg = process.argv[2];
    
    if (!leagueArg) {
        console.log('Usage: node refresh.js <league>');
        console.log('Leagues: ligue1, premierleague, liga, seriea, bundesliga, all');
        process.exit(1);
    }
    
    require('dotenv').config();
    const mongoose = require('mongoose');
    
    mongoose.connect(process.env.MONGODB_URI, {
        useNewUrlParser: true,
        useUnifiedTopology: true
    }).then(async () => {
        console.log('✅ Connected to MongoDB');
        
        if (leagueArg === 'all') {
            for (const league of Object.keys(LEAGUES)) {
                await refreshLeague(league);
                await delay(5000); // Wait between leagues
            }
        } else {
            await refreshLeague(leagueArg);
        }
        
        await mongoose.disconnect();
        console.log('🔌 Disconnected from MongoDB');
        process.exit(0);
    }).catch(err => {
        console.error('❌ MongoDB connection error:', err);
        process.exit(1);
    });
}

module.exports = { refreshLeague, refreshTeam, refreshPlayer };