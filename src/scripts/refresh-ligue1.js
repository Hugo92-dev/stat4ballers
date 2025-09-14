const sportmonks = require('../api/sportmonks');
const { database, League, Team, Player } = require('../utils/database');
const fs = require('fs').promises;
const path = require('path');

// Ligue 1 configuration for season 2025/26
const LIGUE1_CONFIG = {
    name: 'Ligue 1',
    slug: 'ligue1',
    sportmonksId: 301,
    currentSeasonId: 25651,
    previousSeasons: [21779, 23643],
    teamIds: [44, 59, 79, 266, 271, 289, 450, 591, 598, 686, 690, 776, 1055, 3513, 3682, 4508, 6789, 9257]
};

// Utility delay function
function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

// Initialize database
async function initDatabase() {
    await database.init();
    console.log('✅ Database initialized');
}

// Refresh Ligue 1 data
async function refreshLigue1() {
    console.log('🔄 Starting Ligue 1 data refresh...');
    console.log(`📊 Season ID: ${LIGUE1_CONFIG.currentSeasonId}`);
    console.log(`👥 Teams to fetch: ${LIGUE1_CONFIG.teamIds.length}`);
    
    try {
        // Create league entry
        await database.findOneAndUpdate(
            'leagues',
            { slug: LIGUE1_CONFIG.slug },
            {
                sportmonksId: LIGUE1_CONFIG.sportmonksId,
                name: LIGUE1_CONFIG.name,
                slug: LIGUE1_CONFIG.slug,
                country: 'France',
                currentSeasonId: LIGUE1_CONFIG.currentSeasonId,
                lastUpdated: new Date().toISOString()
            },
            { upsert: true }
        );
        console.log('✅ League data updated');
        
        // Refresh each team
        let teamCount = 0;
        for (const teamId of LIGUE1_CONFIG.teamIds) {
            teamCount++;
            console.log(`\n📍 Processing team ${teamCount}/${LIGUE1_CONFIG.teamIds.length} (ID: ${teamId})...`);
            await refreshTeam(teamId);
            await delay(1000); // Respect rate limits (3000 req/hour = ~1.2 req/sec)
        }
        
        console.log('\n✅ Ligue 1 refresh completed successfully!');
        console.log(`📊 Total teams processed: ${teamCount}`);
        
        // Show summary
        const teams = await database.find('teams');
        const players = await database.find('players');
        console.log(`📈 Database now contains: ${teams.length} teams, ${players.length} players`);
        
    } catch (error) {
        console.error('❌ Error refreshing Ligue 1:', error.message);
        throw error;
    }
}

// Refresh individual team
async function refreshTeam(teamId) {
    try {
        // Get team data with details
        console.log(`  → Fetching team details...`);
        const teamResponse = await sportmonks.makeRequest(`/teams/${teamId}`, {
            include: 'venue,coach'
        });
        
        if (!teamResponse.data) {
            throw new Error('No team data received');
        }
        
        const teamData = teamResponse.data;
        
        // Create slug from team name
        const teamSlug = teamData.name.toLowerCase()
            .replace(/[àáäâ]/g, 'a')
            .replace(/[èéëê]/g, 'e')
            .replace(/[ìíïî]/g, 'i')
            .replace(/[òóöô]/g, 'o')
            .replace(/[ùúüû]/g, 'u')
            .replace(/[ç]/g, 'c')
            .replace(/\s+/g, '-')
            .replace(/[^a-z0-9-]/g, '');
        
        // Save team to database
        const team = {
            sportmonksId: teamId,
            name: teamData.name,
            slug: teamSlug,
            shortName: teamData.short_code || teamData.name.substring(0, 3).toUpperCase(),
            logo: teamData.image_path || teamData.logo_path || '',
            venue: teamData.venue ? {
                name: teamData.venue.name,
                capacity: teamData.venue.capacity,
                city: teamData.venue.city
            } : null,
            founded: teamData.founded,
            league: LIGUE1_CONFIG.slug,
            lastUpdated: new Date().toISOString()
        };
        
        await database.findOneAndUpdate(
            'teams',
            { sportmonksId: teamId },
            team,
            { upsert: true }
        );
        
        console.log(`    ✓ Team ${teamData.name} saved`);
        
        // Get team squad for current season
        console.log(`  → Fetching squad for season ${LIGUE1_CONFIG.currentSeasonId}...`);
        await refreshTeamSquad(teamId, teamSlug, teamData.name);
        
        // Get team statistics
        console.log(`  → Fetching team statistics...`);
        await refreshTeamStatistics(teamId, LIGUE1_CONFIG.currentSeasonId);
        
    } catch (error) {
        console.error(`    ✗ Failed to refresh team ${teamId}:`, error.message);
    }
}

// Refresh team squad
async function refreshTeamSquad(teamId, teamSlug, teamName) {
    try {
        const squadResponse = await sportmonks.makeRequest(`/squads/seasons/${LIGUE1_CONFIG.currentSeasonId}/teams/${teamId}`, {
            include: 'player.position,player.detailedposition'
        });
        
        if (!squadResponse.data || squadResponse.data.length === 0) {
            console.log(`    ⚠ No squad data available for ${teamName}`);
            return;
        }
        
        const players = squadResponse.data;
        console.log(`    → Found ${players.length} players`);
        
        let playerCount = 0;
        for (const squadEntry of players) {
            if (squadEntry.player) {
                playerCount++;
                await refreshPlayer(squadEntry.player, teamId, teamSlug, teamName);
                
                // Small delay between players to avoid rate limits
                if (playerCount % 5 === 0) {
                    await delay(500);
                }
            }
        }
        
        console.log(`    ✓ ${playerCount} players saved for ${teamName}`);
        
    } catch (error) {
        console.error(`    ✗ Failed to fetch squad:`, error.message);
    }
}

// Refresh individual player
async function refreshPlayer(playerData, teamId, teamSlug, teamName) {
    try {
        const playerId = playerData.id;
        
        // Create player slug
        const playerSlug = (playerData.display_name || playerData.common_name || playerData.name || '').toLowerCase()
            .replace(/[àáäâ]/g, 'a')
            .replace(/[èéëê]/g, 'e')
            .replace(/[ìíïî]/g, 'i')
            .replace(/[òóöô]/g, 'o')
            .replace(/[ùúüû]/g, 'u')
            .replace(/[ç]/g, 'c')
            .replace(/\s+/g, '-')
            .replace(/[^a-z0-9-]/g, '');
        
        // Determine if player is a goalkeeper
        const position = playerData.position?.name || 'Unknown';
        const isGoalkeeper = position.toLowerCase().includes('goalkeeper') || position === 'GK';
        
        const player = {
            sportmonksId: playerId,
            name: playerData.display_name || playerData.common_name || playerData.name,
            slug: playerSlug,
            firstName: playerData.firstname,
            lastName: playerData.lastname,
            displayName: playerData.display_name,
            image: playerData.image_path || '',
            dateOfBirth: playerData.date_of_birth,
            age: calculateAge(playerData.date_of_birth),
            height: playerData.height,
            weight: playerData.weight,
            nationality: playerData.nationality?.name || playerData.nationality || '',
            position: position,
            detailedPosition: playerData.detailedposition?.name || position,
            jerseyNumber: null, // Will be updated from squad data if available
            isGoalkeeper: isGoalkeeper,
            team: {
                sportmonksId: teamId,
                slug: teamSlug,
                name: teamName
            },
            currentSeason: LIGUE1_CONFIG.currentSeasonId,
            lastUpdated: new Date().toISOString()
        };
        
        await database.findOneAndUpdate(
            'players',
            { sportmonksId: playerId },
            player,
            { upsert: true }
        );
        
    } catch (error) {
        console.error(`      ✗ Failed to save player ${playerData.id}:`, error.message);
    }
}

// Refresh team statistics
async function refreshTeamStatistics(teamId, seasonId) {
    try {
        const statsResponse = await sportmonks.makeRequest(`/teams/${teamId}/seasons/${seasonId}/statistics`);
        
        if (!statsResponse.data || !statsResponse.data.details) {
            console.log(`    ⚠ No statistics available`);
            return;
        }
        
        const details = statsResponse.data.details;
        
        // Map statistics according to our documentation
        const statistics = {
            season: seasonId,
            rating: findStatValue(details, 118),
            gamesPlayed: findStatValue(details, 27263),
            averagePointsPerGame: findStatValue(details, 9676),
            averagePlayerAge: findStatValue(details, 9673),
            teamWins: findStatValue(details, 214),
            teamDraws: findStatValue(details, 215),
            teamLost: findStatValue(details, 216),
            goalsScored: findStatValue(details, 191),
            goalsConceded: findStatValue(details, 88),
            cleanSheets: findStatValue(details, 194),
            redCards: findStatValue(details, 83)
        };
        
        // Update team with statistics
        const team = await database.findOne('teams', { sportmonksId: teamId });
        if (team) {
            team.statistics = statistics;
            await database.updateOne('teams', { sportmonksId: teamId }, team);
            console.log(`    ✓ Statistics updated`);
        }
        
    } catch (error) {
        console.error(`    ✗ Failed to fetch statistics:`, error.message);
    }
}

// Fetch player statistics for radar charts
async function refreshPlayerStatistics(playerId, seasonId) {
    try {
        const statsResponse = await sportmonks.makeRequest(`/players/${playerId}/seasons/${seasonId}/statistics`);
        
        if (!statsResponse.data || statsResponse.data.length === 0) {
            return null;
        }
        
        // Get the most recent statistics
        const stats = statsResponse.data[0];
        if (!stats.details) {
            return null;
        }
        
        // Map all 59 player statistics according to our documentation
        const mappedStats = sportmonks.mapPlayerStatistics(stats.details);
        
        // Update player with statistics
        const player = await database.findOne('players', { sportmonksId: playerId });
        if (player) {
            player.statistics = mappedStats;
            
            // Calculate radar chart data
            player.radarCharts = sportmonks.calculateRadarCharts(mappedStats, player.isGoalkeeper);
            
            await database.updateOne('players', { sportmonksId: playerId }, player);
        }
        
        return mappedStats;
        
    } catch (error) {
        console.error(`Failed to fetch player ${playerId} statistics:`, error.message);
        return null;
    }
}

// Helper function to find statistic value
function findStatValue(details, typeId) {
    const stat = details.find(s => s.type_id === typeId);
    return stat ? stat.value.value || stat.value : 0;
}

// Calculate age from date of birth
function calculateAge(dateOfBirth) {
    if (!dateOfBirth) return null;
    const today = new Date();
    const birthDate = new Date(dateOfBirth);
    let age = today.getFullYear() - birthDate.getFullYear();
    const monthDiff = today.getMonth() - birthDate.getMonth();
    if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDate.getDate())) {
        age--;
    }
    return age;
}

// Create backup before refresh
async function createBackup() {
    try {
        const backupDir = path.join(__dirname, '../../data/backup');
        await fs.mkdir(backupDir, { recursive: true });
        
        const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
        const backupFile = path.join(backupDir, `ligue1_${timestamp}.json`);
        
        // Get current data
        const teams = await database.find('teams');
        const players = await database.find('players');
        
        const backupData = {
            timestamp,
            league: 'ligue1',
            teams: teams.filter(t => t.league === 'ligue1'),
            players: players.filter(p => p.team && LIGUE1_CONFIG.teamIds.includes(p.team.sportmonksId))
        };
        
        await fs.writeFile(backupFile, JSON.stringify(backupData, null, 2));
        console.log(`📁 Backup created: ${backupFile}`);
    } catch (error) {
        console.error('Failed to create backup:', error.message);
    }
}

// Log refresh operation
async function logRefresh(status, error = null) {
    try {
        const logDir = path.join(__dirname, '../../data/logs');
        await fs.mkdir(logDir, { recursive: true });
        
        const logFile = path.join(logDir, 'refresh.log');
        const logEntry = {
            timestamp: new Date().toISOString(),
            league: 'ligue1',
            status,
            error
        };
        
        await fs.appendFile(logFile, JSON.stringify(logEntry) + '\n');
    } catch (err) {
        console.error('Failed to write log:', err.message);
    }
}

// Main execution
async function main() {
    console.log('🚀 Starting Ligue 1 data integration from SportMonks API');
    console.log(`🔑 API Key: ${process.env.SPORTMONKS_API_KEY ? 'Configured ✓' : 'Missing ✗'}`);
    
    try {
        await initDatabase();
        await createBackup();
        await refreshLigue1();
        
        // Now fetch detailed statistics for all players (separate pass to manage rate limits)
        console.log('\n📊 Fetching detailed player statistics for radar charts...');
        const players = await database.find('players');
        const ligue1Players = players.filter(p => p.team && LIGUE1_CONFIG.teamIds.includes(p.team.sportmonksId));
        
        console.log(`📈 Processing statistics for ${ligue1Players.length} players...`);
        let statsCount = 0;
        
        for (const player of ligue1Players) {
            statsCount++;
            if (statsCount % 10 === 0) {
                console.log(`  → Progress: ${statsCount}/${ligue1Players.length} players`);
            }
            
            await refreshPlayerStatistics(player.sportmonksId, LIGUE1_CONFIG.currentSeasonId);
            
            // Respect rate limits
            await delay(1500);
        }
        
        console.log(`\n✅ Player statistics updated: ${statsCount} players processed`);
        
        await logRefresh('success');
        console.log('\n🎉 Ligue 1 data integration completed successfully!');
        
    } catch (error) {
        console.error('\n❌ Data integration failed:', error);
        await logRefresh('error', error.message);
        process.exit(1);
    }
}

// Run if called directly
if (require.main === module) {
    require('dotenv').config();
    main().catch(console.error);
}

module.exports = { refreshLigue1 };