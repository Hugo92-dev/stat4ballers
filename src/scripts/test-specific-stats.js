const axios = require('axios');
require('dotenv').config();

const API_KEY = process.env.SPORTMONKS_API_KEY;
const BASE_URL = process.env.SPORTMONKS_BASE_URL;
const SEASON_ID = 25651; // Ligue 1
const MARSEILLE_ID = 44;

async function testSpecificStats() {
    try {
        console.log('🔍 Test des stats spécifiques: Expected Goals, Through Balls, Long Balls\n');

        // Première étape : récupérer les joueurs
        const url = `${BASE_URL}/squads/seasons/${SEASON_ID}/teams/${MARSEILLE_ID}`;
        const response = await axios.get(url, {
            params: {
                api_token: API_KEY,
                include: 'player'
            }
        });

        if (response.data && response.data.data) {
            const squad = response.data.data;
            console.log(`✅ ${squad.length} joueurs trouvés\n`);

            // Prendre le premier joueur pour tester
            const testPlayer = squad.find(p => p.player && p.player.id);

            if (testPlayer) {
                const playerId = testPlayer.player.id;
                const playerName = testPlayer.player.display_name || testPlayer.player.name;

                console.log(`🎯 Test avec ${playerName} (ID: ${playerId})\n`);

                // Récupérer les stats détaillées du joueur
                console.log('📡 Récupération des stats détaillées...');
                const detailedUrl = `${BASE_URL}/players/${playerId}`;
                const detailedResponse = await axios.get(detailedUrl, {
                    params: {
                        api_token: API_KEY,
                        include: 'statistics.details',
                        seasons: SEASON_ID
                    }
                });

                if (detailedResponse.data?.data?.statistics?.data) {
                    const seasonStats = detailedResponse.data.data.statistics.data.find(s => s.season_id === SEASON_ID);

                    if (seasonStats?.details?.data) {
                        const details = seasonStats.details.data[0];
                        console.log(`✅ Stats détaillées trouvées\n`);

                        // Chercher les stats spécifiques
                        const targetStats = [
                            { id: 5304, name: 'Expected Goals', code: 'EXPECTED_GOALS' },
                            { id: 125, name: 'Accurate Through Balls', code: 'THROUGH_BALLS_WON' },
                            { id: 123, name: 'Accurate Long Balls', code: 'LONG_BALLS_WON' }
                        ];

                        console.log('🔍 Recherche des stats spécifiques:');
                        targetStats.forEach(targetStat => {
                            if (details[targetStat.code.toLowerCase().replace('_', '_')]) {
                                console.log(`✅ ${targetStat.name}: ${JSON.stringify(details[targetStat.code.toLowerCase()])}`);
                            } else {
                                console.log(`❌ ${targetStat.name}: Non trouvé dans les stats détaillées`);
                            }
                        });

                        console.log('\n📋 Structure complète des stats détaillées:');
                        console.log(JSON.stringify(details, null, 2));
                    } else {
                        console.log('❌ Pas de détails de stats pour cette saison');
                    }
                } else {
                    console.log('❌ Pas de stats détaillées disponibles');
                }
            }
        }

    } catch (error) {
        console.error('❌ Erreur:', error.response?.data || error.message);
    }
}

// Lancer le test
testSpecificStats();