const axios = require('axios');

const API_TOKEN = 'KCKLQvVx687XrO9EBMLbZYEf8lQ7frEfZ9dvSqHt9PSIYMplUiVI3s3g34qZ';

async function testMarseillePlayers() {
    console.log('🔍 Testing Marseille squad with player verification...\n');

    try {
        // Get Marseille squad
        const squadResponse = await axios.get(
            `https://api.sportmonks.com/v3/football/squads/seasons/25651/teams/44`,
            {
                params: {
                    api_token: API_TOKEN,
                    include: 'player'
                }
            }
        );

        const squadPlayers = squadResponse.data.data;
        console.log(`📋 Found ${squadPlayers.length} players in Marseille squad endpoint\n`);

        // Check specific players
        const playersToCheck = ['Harit', 'Greenwood', 'Rowe', 'Rabiot'];

        for (const searchName of playersToCheck) {
            const player = squadPlayers.find(p =>
                p.player && p.player.name && p.player.name.includes(searchName)
            );

            if (player) {
                console.log(`\n👤 Checking ${player.player.display_name || player.player.name}...`);

                // Verify via individual endpoint
                try {
                    const playerCheckResponse = await axios.get(
                        `https://api.sportmonks.com/v3/football/players/${player.player.id}`,
                        {
                            params: {
                                api_token: API_TOKEN,
                                include: 'teams'
                            }
                        }
                    );

                    const playerData = playerCheckResponse.data.data;
                    const currentTeams = playerData.teams || [];

                    // Find active team
                    const activeTeam = currentTeams.find(t =>
                        !t.end || new Date(t.end) > new Date()
                    );

                    if (activeTeam) {
                        console.log(`   Current team ID: ${activeTeam.team_id}`);
                        console.log(`   Jersey number: ${activeTeam.jersey_number}`);

                        if (activeTeam.team_id === 44) {
                            console.log(`   ✅ KEEP: Still at Marseille`);
                        } else {
                            console.log(`   ❌ REMOVE: No longer at Marseille (now at team ${activeTeam.team_id})`);
                        }
                    } else {
                        console.log(`   ⚠️ No active team found`);
                    }

                    // Small delay
                    await new Promise(resolve => setTimeout(resolve, 500));

                } catch (error) {
                    console.log(`   Error checking player: ${error.message}`);
                }
            } else {
                console.log(`\n❓ ${searchName} not found in squad`);
            }
        }

    } catch (error) {
        console.error('Error:', error.message);
    }
}

testMarseillePlayers();