const mongoose = require('mongoose');
const axios = require('axios');
const Player = require('../models/Player');
const Team = require('../models/Team');
require('dotenv').config();

const API_KEY = process.env.SPORTMONKS_API_KEY;
const BASE_URL = process.env.SPORTMONKS_BASE_URL;
const SEASON_ID = 25651;
const MARSEILLE_ID = 44;

async function testMarseilleStats() {
    try {
        console.log('🔍 Test avec l\'Olympique de Marseille\n');

        // 1. Tester l'API directement
        console.log('📡 Appel API...');
        const url = `${BASE_URL}/squads/seasons/${SEASON_ID}/teams/${MARSEILLE_ID}`;
        const response = await axios.get(url, {
            params: {
                api_token: API_KEY,
                include: 'player;details.type'
            }
        });

        if (response.data && response.data.data) {
            const squad = response.data.data;
            console.log(`✅ API: ${squad.length} joueurs trouvés\n`);

            // Afficher les 3 premiers joueurs avec leurs stats
            for (let i = 0; i < Math.min(3, squad.length); i++) {
                const player = squad[i].player?.data;
                if (player) {
                    console.log(`Joueur ${i+1}: ${player.display_name || player.name}`);
                    console.log(`  ID: ${player.id}`);

                    // Vérifier les détails
                    if (squad[i].details?.data) {
                        const seasonDetails = squad[i].details.data.find(d =>
                            d.type_id === 34 && d.season_id === SEASON_ID
                        );
                        if (seasonDetails) {
                            console.log(`  Stats trouvées:`);
                            console.log(`    - Matchs: ${seasonDetails.appearances || 0}`);
                            console.log(`    - Buts: ${seasonDetails.goals || 0}`);
                            console.log(`    - Passes: ${seasonDetails.assists || 0}`);
                        } else {
                            console.log(`  Pas de stats pour la saison actuelle`);
                        }
                    }
                    console.log();
                }
            }
        }

        // 2. Vérifier la base de données
        await mongoose.connect(process.env.MONGODB_URI);
        console.log('📊 Vérification de la base de données...');

        const marseilleTeam = await Team.findOne({ name: /Marseille/i });
        if (marseilleTeam) {
            const players = await Player.find({ team: marseilleTeam._id })
                .limit(5)
                .sort({ 'statistics.appearances': -1 });

            console.log(`\n✅ Base de données: ${players.length} joueurs Marseille trouvés`);
            players.forEach(p => {
                console.log(`- ${p.displayName || p.name}: ${p.statistics?.appearances || 0} matchs, ${p.statistics?.goals || 0} buts`);
            });
        } else {
            console.log('⚠️ Équipe Marseille non trouvée en base');
        }

        await mongoose.disconnect();

    } catch (error) {
        console.error('❌ Erreur:', error.response?.data || error.message);
        if (mongoose.connection.readyState === 1) {
            await mongoose.disconnect();
        }
    }
}

// Lancer le test
console.log('🚀 Test de récupération des stats pour l\'Olympique de Marseille');
console.log('='.repeat(60) + '\n');

testMarseilleStats()
    .then(() => console.log('\n✅ Test terminé'))
    .catch(err => console.error('\n❌ Erreur fatale:', err));