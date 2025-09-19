const axios = require('axios');

const API_TOKEN = 'KCKLQvVx687XrO9EBMLbZYEf8lQ7frEfZ9dvSqHt9PSIYMplUiVI3s3g34qZ';

async function testMarseilleSync() {
    console.log('🔍 Testing Marseille squad sync with verification...\n');

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

        let kept = [];
        let removed = [];

        // Check each player
        for (const squadEntry of squadPlayers) {
            const player = squadEntry.player;

            if (player && player.name && player.name.includes('Harit')) {
                console.log(`\n🔍 Checking ${player.display_name || player.name}...`);

                try {
                    const playerResponse = await axios.get(
                        `https://api.sportmonks.com/v3/football/players/${player.id}`,
                        {
                            params: {
                                api_token: API_TOKEN,
                                include: 'teams'
                            }
                        }
                    );

                    const playerData = playerResponse.data.data;
                    const teams = playerData.teams || [];

                    console.log(`   Teams found: ${teams.map(t => `${t.team_id} (end: ${t.end || 'active'})`).join(', ')}`);

                    // Find current team
                    const currentTeam = teams.find(t =>
                        (!t.end || new Date(t.end) > new Date())
                    );

                    if (currentTeam) {
                        console.log(`   Current team ID: ${currentTeam.team_id}`);

                        if (currentTeam.team_id === 44) {
                            console.log(`   ✅ KEEP: Still at Marseille`);
                            kept.push(player.display_name || player.name);
                        } else {
                            console.log(`   ❌ REMOVE: Now at team ${currentTeam.team_id} (not Marseille)`);
                            removed.push(player.display_name || player.name);
                        }
                    } else {
                        console.log(`   ❌ REMOVE: No current team found`);
                        removed.push(player.display_name || player.name);
                    }

                } catch (error) {
                    console.log(`   ⚠️ Error checking: ${error.message}`);
                }

                await new Promise(resolve => setTimeout(resolve, 1000));
            }
        }

        console.log(`\n📊 Summary:`);
        console.log(`   Kept: ${kept.length} players`);
        console.log(`   Removed: ${removed.length} players`);
        if (removed.length > 0) {
            console.log(`   Removed players: ${removed.join(', ')}`);
        }

    } catch (error) {
        console.error('Error:', error.message);
    }
}

testMarseilleSync();