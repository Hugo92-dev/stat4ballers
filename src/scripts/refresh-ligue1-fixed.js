const sportmonks = require('../api/sportmonks');
const { database, League, Team, Player } = require('../utils/database');
const fs = require('fs').promises;
const path = require('path');

// Ligue 1 configuration for season 2025/26 from Stats_Ligue1.md
const LIGUE1_TEAMS = {
    44: 'Olympique Marseille',
    59: 'Nantes',
    79: 'Olympique Lyonnais',
    266: 'Brest',
    271: 'Lens',
    289: 'Toulouse',
    450: 'Nice',
    591: 'Paris Saint Germain',
    598: 'Rennes',
    686: 'Strasbourg',
    690: 'LOSC Lille',
    776: 'Angers SCO',
    1055: 'Le Havre',
    3513: 'Metz',
    3682: 'Auxerre',
    4508: 'Paris FC',
    6789: 'Monaco',
    9257: 'Lorient'
};

const LIGUE1_CONFIG = {
    name: 'Ligue 1',
    slug: 'ligue1',
    sportmonksId: 301,
    currentSeasonId: 25651,
    country: 'France'
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

// Create team slug
function createSlug(name) {
    return name.toLowerCase()
        .replace(/[àáäâ]/g, 'a')
        .replace(/[èéëê]/g, 'e')
        .replace(/[ìíïî]/g, 'i')
        .replace(/[òóöô]/g, 'o')
        .replace(/[ùúüû]/g, 'u')
        .replace(/[ç]/g, 'c')
        .replace(/\s+/g, '-')
        .replace(/[^a-z0-9-]/g, '');
}

// Refresh Ligue 1 data
async function refreshLigue1() {
    console.log('🔄 Starting Ligue 1 data refresh...');
    console.log(`📊 Season ID: ${LIGUE1_CONFIG.currentSeasonId}`);
    console.log(`👥 Teams to fetch: ${Object.keys(LIGUE1_TEAMS).length}`);
    
    try {
        // Create league entry
        await database.findOneAndUpdate(
            'leagues',
            { slug: LIGUE1_CONFIG.slug },
            {
                sportmonksId: LIGUE1_CONFIG.sportmonksId,
                name: LIGUE1_CONFIG.name,
                slug: LIGUE1_CONFIG.slug,
                country: LIGUE1_CONFIG.country,
                currentSeasonId: LIGUE1_CONFIG.currentSeasonId,
                lastUpdated: new Date().toISOString()
            },
            { upsert: true }
        );
        console.log('✅ League data updated');
        
        // Refresh each team
        let successCount = 0;
        let failCount = 0;
        
        for (const [teamId, teamName] of Object.entries(LIGUE1_TEAMS)) {
            console.log(`\n📍 Processing ${teamName} (ID: ${teamId})...`);
            const success = await refreshTeam(teamId, teamName);
            if (success) {
                successCount++;
            } else {
                failCount++;
            }
            await delay(1000); // Respect rate limits
        }
        
        console.log('\n✅ Ligue 1 teams refresh completed!');
        console.log(`📊 Success: ${successCount} teams, Failed: ${failCount} teams`);
        
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
async function refreshTeam(teamId, expectedName) {
    try {
        // Get team basic data (without includes that don't exist)
        console.log(`  → Fetching team details...`);
        const teamResponse = await sportmonks.makeRequest(`/football/teams/${teamId}`);
        
        if (!teamResponse.data) {
            throw new Error('No team data received');
        }
        
        const teamData = teamResponse.data;
        
        // Use the name from our documentation if available
        const teamName = expectedName || teamData.name;
        const teamSlug = createSlug(teamName);
        
        // Save team to database
        const team = {
            sportmonksId: parseInt(teamId),
            name: teamName,
            slug: teamSlug,
            shortName: teamData.short_code || teamName.substring(0, 3).toUpperCase(),
            logo: teamData.image_path || '',
            founded: teamData.founded,
            league: LIGUE1_CONFIG.slug,
            country: teamData.country?.name || LIGUE1_CONFIG.country,
            lastUpdated: new Date().toISOString()
        };
        
        await database.findOneAndUpdate(
            'teams',
            { sportmonksId: parseInt(teamId) },
            team,
            { upsert: true }
        );
        
        console.log(`    ✓ Team ${teamName} saved`);
        
        // Get team squad for current season
        console.log(`  → Fetching squad...`);
        await refreshTeamSquad(teamId, teamSlug, teamName);
        
        return true;
        
    } catch (error) {
        console.error(`    ✗ Failed to refresh team ${expectedName}:`, error.message);
        return false;
    }
}

// Refresh team squad
async function refreshTeamSquad(teamId, teamSlug, teamName) {
    try {
        // Try to get squad data - this endpoint should work
        const endpoint = `/football/squads/teams/${teamId}/seasons/${LIGUE1_CONFIG.currentSeasonId}`;
        const squadResponse = await sportmonks.makeRequest(endpoint);
        
        if (!squadResponse.data) {
            console.log(`    ⚠ No squad data available`);
            return;
        }
        
        // The response contains player IDs in the squad
        const squadData = squadResponse.data;
        let playerIds = [];
        
        // Extract player IDs from the squad data
        if (Array.isArray(squadData)) {
            playerIds = squadData.map(entry => entry.player_id).filter(id => id);
        } else if (squadData.player_id) {
            playerIds = [squadData.player_id];
        }
        
        console.log(`    → Found ${playerIds.length} players in squad`);
        
        // Fetch each player's details
        let savedCount = 0;
        for (const playerId of playerIds) {
            const success = await fetchAndSavePlayer(playerId, teamId, teamSlug, teamName);
            if (success) savedCount++;
            
            // Small delay between players
            if (savedCount % 5 === 0) {
                await delay(500);
            }
        }
        
        console.log(`    ✓ ${savedCount} players saved for ${teamName}`);
        
    } catch (error) {
        console.error(`    ✗ Failed to fetch squad:`, error.message);
    }
}

// Fetch and save individual player
async function fetchAndSavePlayer(playerId, teamId, teamSlug, teamName) {
    try {
        // Fetch player details
        const playerResponse = await sportmonks.makeRequest(`/football/players/${playerId}`);
        
        if (!playerResponse.data) {
            return false;
        }
        
        const playerData = playerResponse.data;
        
        // Create player slug
        const playerName = playerData.display_name || playerData.common_name || playerData.name || 'Unknown';
        const playerSlug = createSlug(playerName);
        
        // Determine position
        const position = playerData.position?.name || playerData.position || 'Unknown';
        const isGoalkeeper = position.toLowerCase().includes('goalkeeper') || 
                           position.toLowerCase().includes('keeper') || 
                           position === 'GK';
        
        const player = {
            sportmonksId: playerId,
            name: playerName,
            slug: playerSlug,
            firstName: playerData.firstname || '',
            lastName: playerData.lastname || '',
            displayName: playerData.display_name || playerName,
            image: playerData.image_path || '',
            dateOfBirth: playerData.date_of_birth,
            age: calculateAge(playerData.date_of_birth),
            height: playerData.height,
            weight: playerData.weight,
            nationality: playerData.country?.name || '',
            position: position,
            detailedPosition: playerData.detailed_position?.name || position,
            jerseyNumber: playerData.jersey_number || null,
            isGoalkeeper: isGoalkeeper,
            team: {
                sportmonksId: parseInt(teamId),
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
        
        return true;
        
    } catch (error) {
        console.error(`      ✗ Failed to save player ${playerId}:`, error.message);
        return false;
    }
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
            players: players
        };
        
        await fs.writeFile(backupFile, JSON.stringify(backupData, null, 2));
        console.log(`📁 Backup created: ${backupFile}`);
    } catch (error) {
        console.error('Failed to create backup:', error.message);
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
        
        console.log('\n🎉 Ligue 1 clubs and squads integration completed!');
        console.log('📌 Next step: Add player and team statistics');
        
    } catch (error) {
        console.error('\n❌ Data integration failed:', error);
        process.exit(1);
    }
}

// Run if called directly
if (require.main === module) {
    require('dotenv').config();
    main().catch(console.error);
}

module.exports = { refreshLigue1 };