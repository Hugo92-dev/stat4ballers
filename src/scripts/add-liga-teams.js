const sportmonks = require('../api/sportmonks');
const { database, Team } = require('../utils/database');

// La Liga teams for season 2025/2026 from Stats_Liga.md
const LALIGA_TEAMS = {
    36: 'Celta de Vigo',
    83: 'FC Barcelona',
    93: 'Real Oviedo',
    106: 'Getafe',
    214: 'Valencia',
    231: 'Girona',
    377: 'Rayo Vallecano',
    459: 'Osasuna',
    485: 'Real Betis',
    528: 'Espanyol',
    594: 'Real Sociedad',
    645: 'Mallorca',
    676: 'Sevilla',
    1099: 'Elche',
    2975: 'Deportivo Alavés',
    3457: 'Levante',
    3468: 'Real Madrid',
    3477: 'Villarreal',
    7980: 'Atlético Madrid',
    13258: 'Athletic Club'
};

const SEASON_ID = 25659; // La Liga 2025/2026

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

// Delay utility
function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function addLaLigaTeams() {
    console.log('🚀 Adding La Liga teams to database');
    console.log(`📊 Season 2025/2026 (ID: ${SEASON_ID})`);
    console.log(`👥 ${Object.keys(LALIGA_TEAMS).length} teams to add\n`);
    
    // Initialize database
    await database.init();
    
    // Add league
    await database.findOneAndUpdate(
        'leagues',
        { slug: 'laliga' },
        {
            sportmonksId: 564,
            name: 'La Liga',
            slug: 'laliga',
            country: 'Spain',
            currentSeasonId: SEASON_ID,
            lastUpdated: new Date().toISOString()
        },
        { upsert: true }
    );
    console.log('✅ La Liga league entry created\n');
    
    let successCount = 0;
    let failCount = 0;
    
    // Process each team
    for (const [teamId, teamName] of Object.entries(LALIGA_TEAMS)) {
        console.log(`📍 Processing ${teamName} (ID: ${teamId})`);
        
        try {
            // Get team data from API
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
                        league: 'laliga',
                        country: 'Spain',
                        venue: {
                            name: team.venue?.name || '',
                            capacity: team.venue?.capacity || 0,
                            city: team.venue?.city || ''
                        },
                        lastUpdated: new Date().toISOString()
                    },
                    { upsert: true }
                );
                console.log(`  ✓ ${teamName} saved`);
                successCount++;
            } else {
                console.log(`  ✗ No data received for ${teamName}`);
                failCount++;
            }
        } catch (error) {
            console.log(`  ✗ Error: ${error.message}`);
            failCount++;
        }
        
        // Small delay between requests
        await delay(1000);
    }
    
    console.log('\n✅ La Liga teams import completed!');
    console.log(`📊 Success: ${successCount} teams, Failed: ${failCount} teams`);
    
    // Show all teams in database
    const allTeams = await database.find('teams', { league: 'laliga' });
    console.log(`\n📈 Total La Liga teams in database: ${allTeams.length}`);
    console.log('Teams:', allTeams.map(t => t.name).join(', '));
}

// Run
require('dotenv').config();
addLaLigaTeams().catch(console.error);