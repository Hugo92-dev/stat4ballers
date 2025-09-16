const axios = require('axios');
require('dotenv').config();

const API_KEY = process.env.SPORTMONKS_API_KEY;
const BASE_URL = process.env.SPORTMONKS_BASE_URL;
const SEASON_ID = 25651;
const MARSEILLE_ID = 44;

async function testApiStructure() {
    try {
        console.log('🔍 Testing API response structure\n');

        const url = `${BASE_URL}/squads/seasons/${SEASON_ID}/teams/${MARSEILLE_ID}`;
        const response = await axios.get(url, {
            params: {
                api_token: API_KEY,
                include: 'player;details.type'
            }
        });

        if (response.data && response.data.data) {
            const squad = response.data.data;
            console.log(`✅ Got ${squad.length} players\n`);

            // Check first player structure
            if (squad[0]) {
                console.log('First player structure:');
                console.log('- player_id:', squad[0].player_id);
                console.log('- jersey_number:', squad[0].jersey_number);
                console.log('- position_id:', squad[0].position_id);

                if (squad[0].player) {
                    console.log('\nPlayer object exists:');
                    console.log('- id:', squad[0].player.id);
                    console.log('- name:', squad[0].player.name);
                    console.log('- display_name:', squad[0].player.display_name);
                    console.log('- image_path:', squad[0].player.image_path);
                }

                console.log('\nDetails exists?:', !!squad[0].details);

                // Find a player with actual stats (more matches played)
                const playerWithStats = squad.find(p => p.position_id !== 24) || squad[0]; // Not goalkeeper
                if (playerWithStats) {
                    console.log('\nPlayer with possible stats:', playerWithStats.player?.display_name);
                    console.log('Details structure:', JSON.stringify(playerWithStats.details, null, 2));
                }
            }
        }
    } catch (error) {
        console.error('❌ Error:', error.response?.data || error.message);
    }
}

// Run test
testApiStructure();