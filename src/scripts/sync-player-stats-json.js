const fs = require('fs');
const path = require('path');
const axios = require('axios');
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

    // Si on a les détails du joueur (array of stats)
    if (playerData.details && Array.isArray(playerData.details)) {
        const details = playerData.details;

        // Extract stats from details array based on type_id
        details.forEach(stat => {
            const value = stat.value;

            switch(stat.type_id) {
                // General statistics
                case 118: // Rating
                    stats.rating = value?.average || value?.total || 0;
                    break;
                case 321: // Appearances
                    stats.appearances = value?.total || 0;
                    break;
                case 119: // Minutes Played
                    stats.minutesPlayed = value?.total || 0;
                    break;
                case 40: // Captain
                    stats.captain = value?.total || 0;
                    break;
                case 52: // Goals
                    stats.goals = value?.total || 0;
                    break;
                case 79: // Assists
                    stats.assists = value?.total || 0;
                    break;
                case 87: // Injuries
                    stats.injuries = value?.total || 0;
                    break;
                case 83: // Red Cards
                    stats.redCards = value?.total || 0;
                    break;

                // Offensive creativity
                case 42: // Shots Total
                    stats.shotsTotal = value?.total || 0;
                    break;
                case 86: // Shots on Target
                    stats.shotsOnTarget = value?.total || 0;
                    break;
                case 47: // Penalties
                    stats.penalties = value?.total || 0;
                    break;
                case 64: // Hit Woodwork
                    stats.hitWoodwork = value?.total || 0;
                    break;
                case 117: // Key Passes
                    stats.keyPasses = value?.total || 0;
                    break;
                case 580: // Big Chances Created
                    stats.bigChancesCreated = value?.total || 0;
                    break;
                case 5304: // Expected Goals
                    stats.expectedGoals = value?.total || value || 0;
                    break;
                case 125: // Accurate Through Balls
                    stats.accurateThroughBalls = value?.total || 0;
                    break;
                case 123: // Accurate Long Balls
                    stats.accurateLongBalls = value?.total || 0;
                    break;
                case 99: // Accurate Crosses
                    stats.accurateCrosses = value?.total || 0;
                    break;
                case 109: // Successful Dribbles
                    stats.successfulDribbles = value?.total || 0;
                    break;

                // Defensive commitment
                case 84: // Yellow Cards
                    stats.yellowCards = value?.total || 0;
                    break;
                case 78: // Tackles
                    stats.tackles = value?.total || 0;
                    break;
                case 324: // Own Goals
                    stats.ownGoals = value?.total || 0;
                    break;
                case 100: // Interceptions
                    stats.interceptions = value?.total || 0;
                    break;
                case 106: // Duels Won
                    stats.duelsWon = value?.total || 0;
                    break;
                case 107: // Aerials Won
                    stats.aerialsWon = value?.total || 0;
                    break;
                case 94: // Dispossessed
                    stats.dispossessed = value?.total || 0;
                    break;
                case 110: // Dribbled Past
                    stats.dribbledPast = value?.total || 0;
                    break;
                case 56: // Fouls
                    stats.fouls = value?.total || 0;
                    break;
                case 96: // Fouls Drawn
                    stats.foulsDrawn = value?.total || 0;
                    break;
                case 571: // Error Lead to Goal
                    stats.errorLeadToGoal = value?.total || 0;
                    break;

                // Goalkeeper specific
                case 57: // Saves
                    stats.saves = value?.total || 0;
                    break;
                case 104: // Saves Inside Box
                    stats.savesInsideBox = value?.total || 0;
                    break;
                case 88: // Goals Conceded
                    stats.goalsConceded = value?.total || 0;
                    break;
                case 194: // Clean Sheets
                    stats.cleanSheets = value?.total || 0;
                    break;
            }
        });
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

            stats.rating = details.rating ? parseFloat(details.rating) : stats.rating || 0;
        }
    }

    return stats;
}

// Fonction principale
async function syncPlayerStats() {
    try {
        // Lire le fichier JSON des joueurs
        const playersPath = path.join(__dirname, '../../data/db/players.json');
        let players = [];

        try {
            const data = fs.readFileSync(playersPath, 'utf8');
            players = JSON.parse(data);
            console.log(`✅ ${players.length} joueurs trouvés dans la base de données`);
        } catch (error) {
            console.error('❌ Erreur lors de la lecture du fichier players.json:', error.message);
            return;
        }

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

            console.log(`📋 ${squadData.length} joueurs trouvés dans l'API`);

            // Traiter chaque joueur de l'équipe
            for (const playerData of squadData) {
                if (!playerData.player) {
                    totalSkipped++;
                    continue;
                }

                const apiPlayer = playerData.player;

                try {
                    // Trouver le joueur dans notre base JSON par son ID SportMonks
                    let playerIndex = players.findIndex(p => p.sportmonksId === apiPlayer.id);

                    if (playerIndex === -1) {
                        console.log(`⚠️ Joueur non trouvé: ${apiPlayer.display_name || apiPlayer.name} (ID: ${apiPlayer.id})`);
                        totalSkipped++;
                        continue;
                    }

                    // Récupérer les stats détaillées si possible
                    const detailedStats = await fetchPlayerDetailedStats(apiPlayer.id);

                    // Mapper les stats
                    const mappedStats = mapStatsToModel(playerData, detailedStats);

                    // Mettre à jour seulement si on a des stats
                    if (Object.keys(mappedStats).length > 0) {
                        // Mettre à jour les statistiques du joueur
                        players[playerIndex].statistics = {
                            ...players[playerIndex].statistics,
                            ...mappedStats
                        };

                        players[playerIndex].lastUpdated = new Date().toISOString();

                        const statsCount = mappedStats.appearances || 0;
                        const statsDetails = [];
                        if (mappedStats.goals > 0) statsDetails.push(`${mappedStats.goals} buts`);
                        if (mappedStats.assists > 0) statsDetails.push(`${mappedStats.assists} passes`);
                        if (mappedStats.cleanSheets > 0) statsDetails.push(`${mappedStats.cleanSheets} CS`);
                        if (mappedStats.saves > 0) statsDetails.push(`${mappedStats.saves} arrêts`);

                        const detailsStr = statsDetails.length > 0 ? `, ${statsDetails.join(', ')}` : '';
                        console.log(`✅ ${players[playerIndex].displayName || players[playerIndex].name}: ${statsCount} matchs${detailsStr}, note: ${(mappedStats.rating || 0).toFixed(2)}`);
                        totalUpdated++;
                    } else {
                        console.log(`⏭️ ${players[playerIndex].displayName || players[playerIndex].name}: Pas de stats disponibles`);
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

        // Sauvegarder les joueurs mis à jour dans le fichier JSON
        fs.writeFileSync(playersPath, JSON.stringify(players, null, 2));

        console.log('\n' + '='.repeat(50));
        console.log('📊 RÉSUMÉ DE LA SYNCHRONISATION');
        console.log('='.repeat(50));
        console.log(`✅ Joueurs mis à jour: ${totalUpdated}`);
        console.log(`⏭️ Joueurs ignorés: ${totalSkipped}`);
        console.log(`❌ Erreurs: ${totalFailed}`);

        // Afficher quelques exemples de joueurs avec des stats
        console.log('\n🌟 Top 5 buteurs de Ligue 1:');
        const ligue1Players = players.filter(p => p.league === 'ligue1' && p.statistics?.goals > 0);
        ligue1Players.sort((a, b) => (b.statistics?.goals || 0) - (a.statistics?.goals || 0));

        ligue1Players.slice(0, 5).forEach((player, index) => {
            console.log(`${index + 1}. ${player.displayName || player.name} (${player.team?.name}): ${player.statistics.goals} buts en ${player.statistics.appearances} matchs`);
        });

    } catch (error) {
        console.error('❌ Erreur fatale:', error);
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