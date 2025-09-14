const sportmonks = require('../api/sportmonks');
const { database, League, Team, Player } = require('../utils/database');
const fs = require('fs').promises;
const path = require('path');

// Ligue 1 teams from Stats_Ligue1.md
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

const SEASON_ID = 25651; // Season 2025/2026

// Utility delay
function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

// Create slug
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

async function main() {
    console.log('🚀 Starting Ligue 1 data integration');
    console.log(`📊 Season 2025/2026 (ID: ${SEASON_ID})`);
    console.log(`👥 ${Object.keys(LIGUE1_TEAMS).length} teams to process\n`);
    
    // Initialize database
    await database.init();
    
    // Create league
    await database.findOneAndUpdate(
        'leagues',
        { slug: 'ligue1' },
        {
            sportmonksId: 301,
            name: 'Ligue 1',
            slug: 'ligue1',
            country: 'France',
            currentSeasonId: SEASON_ID,
            lastUpdated: new Date().toISOString()
        },
        { upsert: true }
    );
    console.log('✅ League created\n');
    
    // Process each team
    for (const [teamId, teamName] of Object.entries(LIGUE1_TEAMS)) {
        console.log(`📍 Processing ${teamName} (ID: ${teamId})`);
        
        try {
            // Get team data - using the correct endpoint without /football
            console.log('  → Fetching team data...');
            const teamData = await sportmonks.getTeam(teamId);
            
            if (teamData && teamData.data) {
                const team = teamData.data;
                const slug = createSlug(teamName);
                
                // Save team
                await database.findOneAndUpdate(
                    'teams',
                    { sportmonksId: parseInt(teamId) },
                    {
                        sportmonksId: parseInt(teamId),
                        name: teamName,
                        slug: slug,
                        shortName: team.short_code || teamName.substring(0, 3).toUpperCase(),
                        logo: team.logo_path || team.image_path || '',
                        founded: team.founded || null,
                        league: 'ligue1',
                        country: 'France',
                        venue: {
                            name: team.venue?.data?.name || '',
                            capacity: team.venue?.data?.capacity || 0,
                            city: team.venue?.data?.city || ''
                        },
                        lastUpdated: new Date().toISOString()
                    },
                    { upsert: true }
                );
                console.log(`  ✓ Team saved`);
                
                // Get squad
                console.log('  → Fetching squad...');
                const squadData = await sportmonks.getTeamSquad(teamId, SEASON_ID);
                
                if (squadData && squadData.data && squadData.data.squad?.data) {
                    const players = squadData.data.squad.data;
                    console.log(`  → Found ${players.length} players`);
                    
                    let savedCount = 0;
                    for (const squadEntry of players) {
                        if (squadEntry.player?.data) {
                            const player = squadEntry.player.data;
                            const playerName = player.display_name || player.common_name || player.fullname || 'Unknown';
                            const playerSlug = createSlug(playerName);
                            
                            // Determine position
                            const position = squadEntry.position?.data?.name || player.position?.data?.name || 'Unknown';
                            const isGoalkeeper = position.toLowerCase().includes('keeper') || position === 'Goalkeeper';
                            
                            await database.findOneAndUpdate(
                                'players',
                                { sportmonksId: player.player_id || player.id },
                                {
                                    sportmonksId: player.player_id || player.id,
                                    name: playerName,
                                    slug: playerSlug,
                                    firstName: player.firstname || '',
                                    lastName: player.lastname || '',
                                    displayName: player.display_name || playerName,
                                    image: player.image_path || '',
                                    dateOfBirth: player.birthdate,
                                    nationality: player.nationality || '',
                                    position: position,
                                    jerseyNumber: squadEntry.jersey_number || null,
                                    isGoalkeeper: isGoalkeeper,
                                    team: {
                                        sportmonksId: parseInt(teamId),
                                        slug: slug,
                                        name: teamName
                                    },
                                    currentSeason: SEASON_ID,
                                    lastUpdated: new Date().toISOString()
                                },
                                { upsert: true }
                            );
                            savedCount++;
                        }
                    }
                    console.log(`  ✓ ${savedCount} players saved`);
                } else {
                    console.log(`  ⚠ No squad data available`);
                }
                
            } else {
                console.log(`  ✗ No team data received`);
            }
            
        } catch (error) {
            console.log(`  ✗ Error: ${error.message}`);
        }
        
        // Delay between teams
        await delay(1000);
        console.log('');
    }
    
    // Summary
    const teams = await database.find('teams');
    const players = await database.find('players');
    
    console.log('✅ Import completed!');
    console.log(`📊 Total: ${teams.length} teams, ${players.length} players in database`);
}

// Run
require('dotenv').config();
main().catch(console.error);