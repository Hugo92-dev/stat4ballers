const mongoose = require('mongoose');
const axios = require('axios');
const Player = require('../models/Player');
const Team = require('../models/Team');
require('dotenv').config();

// Configuration
const API_KEY = process.env.SPORTMONKS_API_KEY;
const BASE_URL = process.env.SPORTMONKS_BASE_URL;
const SEASON_ID = 25651; // Saison 2025/2026

// IDs des équipes de Ligue 1
const LIGUE1_TEAMS = [
    { name: 'Olympique Marseille', id: 44 },
    { name: 'Nantes', id: 59 },
    { name: 'Olympique Lyonnais', id: 79 },
    { name: 'Brest', id: 266 },
    { name: 'Lens', id: 271 },
    { name: 'Toulouse', id: 289 },
    { name: 'Nice', id: 450 },
    { name: 'Paris Saint Germain', id: 591 },
    { name: 'Rennes', id: 598 },
    { name: 'Strasbourg', id: 686 },
    { name: 'LOSC Lille', id: 690 },
    { name: 'Angers SCO', id: 776 },
    { name: 'Le Havre', id: 1055 },
    { name: 'Metz', id: 3513 },
    { name: 'Auxerre', id: 3682 },
    { name: 'Paris', id: 4508 },
    { name: 'Monaco', id: 6789 },
    { name: 'Lorient', id: 9257 }
];

// Fonction pour récupérer les statistiques d'une équipe
async function fetchTeamStats(teamId, teamName) {
    try {
        console.log(`📊 Récupération des stats pour ${teamName}...`);

        // Utiliser l'endpoint exact fourni
        const url = `${BASE_URL}/squads/seasons/${SEASON_ID}/teams/${teamId}`;
        const response = await axios.get(url, {
            params: {
                api_token: API_KEY,
                include: 'player;details.type'
            }
        });

        if (response.data && response.data.data) {
            return response.data.data;
        }
        return [];
    } catch (error) {
        console.error(`❌ Erreur pour ${teamName}:`, error.response?.data?.message || error.message);
        return [];
    }
}

// Fonction pour récupérer les stats détaillées d'un joueur
async function fetchPlayerDetailedStats(playerId) {
    try {
        const url = `${BASE_URL}/players/${playerId}`;
        const response = await axios.get(url, {
            params: {
                api_token: API_KEY,
                include: 'statistics.details',
                seasons: SEASON_ID
            }
        });

        if (response.data && response.data.data) {
            return response.data.data;
        }
        return null;
    } catch (error) {
        return null;
    }
}

// Mapper les stats de l'API vers notre modèle
function mapStatsToModel(playerData, detailedStats = null) {
    const stats = {};

    // Si on a les détails du joueur
    if (playerData.details && playerData.details.data) {
        const details = playerData.details.data;

        // Chercher les stats de la saison actuelle
        const currentSeasonStats = details.find(d =>
            d.type_id === 34 && // Type pour les stats de saison
            d.season_id === SEASON_ID
        );

        if (currentSeasonStats) {
            // Stats générales
            stats.appearances = currentSeasonStats.appearances || 0;
            stats.minutesPlayed = currentSeasonStats.minutes || 0;
            stats.goals = currentSeasonStats.goals || 0;
            stats.assists = currentSeasonStats.assists || 0;
            stats.yellowCards = currentSeasonStats.yellow_cards || 0;
            stats.redCards = currentSeasonStats.red_cards || 0;
            stats.rating = currentSeasonStats.rating ? parseFloat(currentSeasonStats.rating) : null;
        }
    }

    // Si on a des stats détaillées supplémentaires
    if (detailedStats && detailedStats.statistics && detailedStats.statistics.data) {
        const seasonStats = detailedStats.statistics.data.find(s => s.season_id === SEASON_ID);

        if (seasonStats && seasonStats.details && seasonStats.details.data && seasonStats.details.data[0]) {
            const details = seasonStats.details.data[0];

            // Compléter avec les stats détaillées
            stats.appearances = details.appearances || stats.appearances || 0;
            stats.minutesPlayed = details.minutes || stats.minutesPlayed || 0;
            stats.captain = details.captain || 0;
            stats.goals = details.goals?.scored || details.goals || stats.goals || 0;
            stats.assists = details.assists || stats.assists || 0;
            stats.injuries = details.injuries || 0;

            // Stats offensives
            stats.shotsTotal = details.shots?.total || 0;
            stats.shotsOnTarget = details.shots?.on_target || 0;
            stats.penalties = details.penalties?.scored || 0;
            stats.hitWoodwork = details.hit_woodwork || 0;
            stats.keyPasses = details.key_passes || 0;
            stats.bigChancesCreated = details.big_chances_created || 0;
            stats.expectedGoals = details.xg?.expected_goals ? parseFloat(details.xg.expected_goals) : null;
            stats.accurateThroughBalls = details.passes?.accurate_through_balls || 0;
            stats.accurateLongBalls = details.passes?.accurate_long_balls || 0;
            stats.accurateCrosses = details.crosses?.accurate || 0;
            stats.successfulDribbles = details.dribbles?.succeeded || 0;

            // Stats défensives
            stats.yellowCards = details.cards?.yellow || stats.yellowCards || 0;
            stats.redCards = details.cards?.red || stats.redCards || 0;
            stats.tackles = details.tackles?.total || 0;
            stats.ownGoals = details.goals?.own || 0;
            stats.interceptions = details.interceptions || 0;
            stats.duelsWon = details.duels?.won || 0;
            stats.aerialsWon = details.aerials?.won || 0;
            stats.dispossessed = details.dispossessed || 0;
            stats.dribbledPast = details.dribbled_past || 0;
            stats.fouls = details.fouls?.committed || 0;
            stats.foulsDrawn = details.fouls?.drawn || 0;
            stats.errorLeadToGoal = details.errors_led_to_goal || 0;

            // Stats gardien
            stats.saves = details.saves?.total || 0;
            stats.savesInsideBox = details.saves?.inside_box || 0;
            stats.goalsConceded = details.goals?.conceded || 0;
            stats.cleanSheets = details.clean_sheets || 0;

            stats.rating = details.rating ? parseFloat(details.rating) : stats.rating;
        }
    }

    return stats;
}

// Helper function pour mapper les positions
function mapPosition(positionName) {
    if (!positionName) return 'Unknown';

    const position = positionName.toLowerCase();
    if (position.includes('goalkeeper') || position.includes('keeper')) return 'Goalkeeper';
    if (position.includes('defender') || position.includes('back')) return 'Defender';
    if (position.includes('midfielder') || position.includes('midfield')) return 'Midfielder';
    if (position.includes('forward') || position.includes('attacker') || position.includes('striker')) return 'Forward';
    return 'Unknown';
}

// Fonction principale
async function syncPlayerStats() {
    try {
        await mongoose.connect(process.env.MONGODB_URI);
        console.log('✅ Connecté à MongoDB');

        let totalUpdated = 0;
        let totalSkipped = 0;
        let totalFailed = 0;

        // Traiter chaque équipe
        for (const team of LIGUE1_TEAMS) {
            console.log(`\n🏟️  Traitement de ${team.name} (ID: ${team.id})`);

            const squadData = await fetchTeamStats(team.id, team.name);

            if (!squadData || squadData.length === 0) {
                console.log(`⚠️ Aucune donnée trouvée pour ${team.name}`);
                totalFailed++;
                continue;
            }

            console.log(`📋 ${squadData.length} joueurs trouvés`);

            // Traiter chaque joueur
            for (const playerData of squadData) {
                if (!playerData.player || !playerData.player.data) {
                    totalSkipped++;
                    continue;
                }

                const apiPlayer = playerData.player.data;

                try {
                    // Trouver le joueur dans notre base par son ID SportMonks
                    let dbPlayer = await Player.findOne({ sportmonksId: apiPlayer.id });

                    // Si pas trouvé par ID, essayer par nom avec l'équipe
                    if (!dbPlayer) {
                        const playerName = apiPlayer.display_name || apiPlayer.name;

                        // Trouver l'équipe dans la base
                        const dbTeam = await Team.findOne({ name: { $regex: team.name, $options: 'i' } });

                        if (dbTeam) {
                            // Chercher le joueur par nom et équipe
                            dbPlayer = await Player.findOne({
                                team: dbTeam._id,
                                $or: [
                                    { name: playerName },
                                    { displayName: playerName },
                                    { name: { $regex: new RegExp(playerName.split(' ')[0], 'i') } },
                                    { lastName: { $regex: new RegExp(playerName.split(' ').pop(), 'i') } }
                                ]
                            });
                        }
                    }

                    if (!dbPlayer) {
                        console.log(`⚠️ Joueur non trouvé en base: ${apiPlayer.display_name || apiPlayer.name} (ID: ${apiPlayer.id})`);

                        // Créer le joueur s'il n'existe pas avec les infos de base
                        const dbTeam = await Team.findOne({ name: { $regex: team.name, $options: 'i' } });
                        if (dbTeam) {
                            dbPlayer = new Player({
                                sportmonksId: apiPlayer.id,
                                name: apiPlayer.name,
                                displayName: apiPlayer.display_name,
                                firstName: apiPlayer.firstname,
                                lastName: apiPlayer.lastname,
                                slug: (apiPlayer.display_name || apiPlayer.name).toLowerCase().replace(/\s+/g, '-').replace(/[^\w-]/g, ''),
                                image: apiPlayer.image_path,
                                dateOfBirth: apiPlayer.date_of_birth,
                                nationality: apiPlayer.nationality?.data?.name || '',
                                position: mapPosition(apiPlayer.position?.data?.name),
                                detailedPosition: apiPlayer.position?.data?.name,
                                jerseyNumber: playerData.jersey_number,
                                team: dbTeam._id,
                                currentSeason: '2025/2026'
                            });
                            await dbPlayer.save();
                            console.log(`✨ Nouveau joueur créé: ${dbPlayer.displayName}`);
                        } else {
                            totalSkipped++;
                            continue;
                        }
                    }

                    // Récupérer les stats détaillées si possible
                    const detailedStats = await fetchPlayerDetailedStats(apiPlayer.id);

                    // Mapper les stats
                    const mappedStats = mapStatsToModel(playerData, detailedStats);

                    // Mettre à jour seulement si on a des stats
                    if (Object.keys(mappedStats).length > 0) {
                        // Conserver les stats existantes et ajouter/mettre à jour avec les nouvelles
                        dbPlayer.statistics = {
                            ...dbPlayer.statistics,
                            ...mappedStats
                        };

                        dbPlayer.currentSeason = '2025/2026';
                        dbPlayer.lastUpdated = new Date();

                        await dbPlayer.save();

                        const statsCount = mappedStats.appearances || 0;
                        console.log(`✅ ${dbPlayer.displayName || dbPlayer.name}: ${statsCount} matchs, ${mappedStats.goals || 0} buts`);
                        totalUpdated++;
                    } else {
                        console.log(`⏭️ ${dbPlayer.displayName || dbPlayer.name}: Pas de stats disponibles`);
                        totalSkipped++;
                    }

                } catch (error) {
                    console.error(`❌ Erreur pour ${apiPlayer.display_name}:`, error.message);
                    totalFailed++;
                }
            }

            // Pause entre les équipes pour éviter de surcharger l'API
            await new Promise(resolve => setTimeout(resolve, 1000));
        }

        console.log('\n' + '='.repeat(50));
        console.log('📊 RÉSUMÉ DE LA SYNCHRONISATION');
        console.log('='.repeat(50));
        console.log(`✅ Joueurs mis à jour: ${totalUpdated}`);
        console.log(`⏭️ Joueurs ignorés: ${totalSkipped}`);
        console.log(`❌ Erreurs: ${totalFailed}`);

        // Afficher quelques exemples de joueurs avec des stats
        console.log('\n🌟 Exemples de joueurs avec stats:');
        const playersWithStats = await Player.find({
            'statistics.appearances': { $gt: 0 }
        })
        .sort({ 'statistics.goals': -1 })
        .limit(5)
        .populate('team', 'name');

        playersWithStats.forEach(player => {
            console.log(`- ${player.displayName || player.name} (${player.team?.name}): ${player.statistics.appearances} matchs, ${player.statistics.goals} buts`);
        });

    } catch (error) {
        console.error('❌ Erreur fatale:', error);
    } finally {
        await mongoose.disconnect();
        console.log('\n🔌 Déconnecté de MongoDB');
    }
}

// Lancer le script
if (require.main === module) {
    console.log('🚀 Démarrage de la synchronisation des statistiques des joueurs de Ligue 1');
    console.log(`📅 Saison 2025/2026 (ID: ${SEASON_ID})`);
    console.log('⏳ Cette opération peut prendre quelques minutes...\n');

    syncPlayerStats()
        .then(() => {
            console.log('\n✨ Synchronisation terminée avec succès!');
            process.exit(0);
        })
        .catch(error => {
            console.error('\n❌ Erreur lors de la synchronisation:', error);
            process.exit(1);
        });
}

module.exports = { syncPlayerStats };