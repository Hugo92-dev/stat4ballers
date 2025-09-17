const axios = require('axios');
require('dotenv').config();

const API_KEY = process.env.SPORTMONKS_API_KEY;
const BASE_URL = process.env.SPORTMONKS_BASE_URL;

// Tester avec la Premier League et une équipe connue (Manchester City)
const SEASON_ID = 25583; // Premier League 2025/2026
const MANCHESTER_CITY_ID = 23; // Manchester City

async function testXGEndpoint() {
    try {
        console.log('🔍 Test spécifique des Expected Goals avec Manchester City\n');

        // Récupérer l'équipe de Manchester City
        const squadUrl = `${BASE_URL}/squads/seasons/${SEASON_ID}/teams/${MANCHESTER_CITY_ID}`;
        const response = await axios.get(squadUrl, {
            params: {
                api_token: API_KEY,
                include: 'player'
            }
        });

        if (response.data?.data) {
            const squad = response.data.data;
            console.log(`✅ ${squad.length} joueurs trouvés à Manchester City\n`);

            // Chercher Haaland (il devrait avoir des xG)
            const haaland = squad.find(p =>
                p.player &&
                (p.player.display_name || p.player.name).toLowerCase().includes('haaland')
            );

            if (haaland) {
                const playerId = haaland.player.id;
                const playerName = haaland.player.display_name || haaland.player.name;

                console.log(`🎯 Test avec ${playerName} (ID: ${playerId})\n`);

                // Récupérer les stats détaillées
                const detailedUrl = `${BASE_URL}/players/${playerId}`;
                console.log(`📡 URL: ${detailedUrl}`);

                const detailedResponse = await axios.get(detailedUrl, {
                    params: {
                        api_token: API_KEY,
                        include: 'statistics.details'
                    }
                });

                console.log('📊 Structure de la réponse:');
                if (detailedResponse.data?.data?.statistics?.data) {
                    const stats = detailedResponse.data.data.statistics.data;
                    console.log(`✅ ${stats.length} saisons trouvées`);

                    // Chercher la saison actuelle
                    const currentSeason = stats.find(s => s.season_id === SEASON_ID);
                    if (currentSeason) {
                        console.log('✅ Saison actuelle trouvée');
                        if (currentSeason.details?.data?.[0]) {
                            const details = currentSeason.details.data[0];
                            console.log('\n📋 Propriétés disponibles contenant "xg" ou "expected":');
                            Object.keys(details).forEach(key => {
                                if (key.toLowerCase().includes('xg') || key.toLowerCase().includes('expected')) {
                                    console.log(`  - ${key}: ${JSON.stringify(details[key])}`);
                                }
                            });

                            // Chercher toutes les propriétés avec des valeurs numériques pour détecter xG
                            console.log('\n🔍 Toutes les propriétés numériques (possibles xG):');
                            Object.keys(details).forEach(key => {
                                const value = details[key];
                                if (typeof value === 'number' && value > 0 && value < 50) {
                                    console.log(`  - ${key}: ${value}`);
                                }
                            });
                        }
                    } else {
                        console.log('❌ Saison actuelle non trouvée');
                        console.log('Saisons disponibles:', stats.map(s => s.season_id));
                    }
                } else {
                    console.log('❌ Pas de statistiques dans la réponse');
                    console.log('Structure:', Object.keys(detailedResponse.data?.data || {}));
                }

            } else {
                console.log('❌ Haaland non trouvé dans l\'équipe');
                console.log('Joueurs disponibles:', squad.slice(0, 5).map(p => p.player?.display_name || p.player?.name));
            }
        }

    } catch (error) {
        console.error('❌ Erreur:', error.response?.data || error.message);
    }
}

testXGEndpoint();