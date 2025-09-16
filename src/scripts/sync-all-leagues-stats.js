const fs = require('fs');
const path = require('path');
const axios = require('axios');
require('dotenv').config();

// Configuration
const API_KEY = process.env.SPORTMONKS_API_KEY;
const BASE_URL = process.env.SPORTMONKS_BASE_URL;

// Configuration des ligues avec leurs IDs de saison 2025/2026
const LEAGUES = [
    {
        name: 'Ligue 1',
        slug: 'ligue1',
        seasonId: 25651,
        color: '🔵'
    },
    {
        name: 'Premier League',
        slug: 'premierleague',
        seasonId: 25583,
        color: '🔴'
    },
    {
        name: 'La Liga',
        slug: 'laliga',
        seasonId: 25659,
        color: '🟠'
    },
    {
        name: 'Serie A',
        slug: 'seriea',
        seasonId: 25533,
        color: '🟢'
    },
    {
        name: 'Bundesliga',
        slug: 'bundesliga',
        seasonId: 25646,
        color: '⚫'
    }
];

// Fonction pour récupérer les équipes d'une ligue
async function fetchLeagueTeams(seasonId) {
    try {
        const response = await axios.get(
            `${BASE_URL}/teams/seasons/${seasonId}`,
            {
                params: {
                    api_token: API_KEY
                }
            }
        );
        return response.data.data || [];
    } catch (error) {
        console.error(`❌ Erreur lors de la récupération des équipes:`, error.message);
        return [];
    }
}

// Fonction pour récupérer les statistiques d'une équipe
async function fetchTeamStats(teamId, seasonId) {
    try {
        const url = `${BASE_URL}/squads/seasons/${seasonId}/teams/${teamId}`;
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
        return [];
    }
}

// Fonction pour récupérer les stats détaillées d'un joueur
async function fetchPlayerDetailedStats(playerId, seasonId) {
    try {
        const url = `${BASE_URL}/players/${playerId}`;
        const response = await axios.get(url, {
            params: {
                api_token: API_KEY,
                include: 'statistics.details',
                seasons: seasonId
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
function mapStatsToModel(playerData, detailedStats = null, seasonId) {
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
        const seasonStats = detailedStats.statistics.data.find(s => s.season_id === seasonId);

        if (seasonStats && seasonStats.details && seasonStats.details.data && seasonStats.details.data[0]) {
            const details = seasonStats.details.data[0];

            // Compléter avec les stats détaillées si manquantes
            stats.appearances = stats.appearances || details.appearances || 0;
            stats.minutesPlayed = stats.minutesPlayed || details.minutes || 0;
            stats.captain = stats.captain || details.captain || 0;
            stats.goals = stats.goals || details.goals?.scored || details.goals || 0;
            stats.assists = stats.assists || details.assists || 0;
        }
    }

    return stats;
}

// Fonction pour synchroniser les stats d'une ligue
async function syncLeagueStats(league) {
    const results = {
        updated: 0,
        skipped: 0,
        failed: 0,
        topScorers: []
    };

    console.log(`\n${league.color} Traitement de ${league.name} (Season ID: ${league.seasonId})`);
    console.log('='.repeat(60));

    // Récupérer les équipes de la ligue
    const teams = await fetchLeagueTeams(league.seasonId);
    if (teams.length === 0) {
        console.log(`⚠️ Aucune équipe trouvée pour ${league.name}`);
        return results;
    }

    console.log(`📋 ${teams.length} équipes trouvées`);

    // Lire le fichier JSON des joueurs
    const playersPath = path.join(__dirname, '../../data/db/players.json');
    let players = [];

    try {
        const data = fs.readFileSync(playersPath, 'utf8');
        players = JSON.parse(data);
    } catch (error) {
        console.error('❌ Erreur lors de la lecture du fichier players.json');
        return results;
    }

    // Traiter chaque équipe
    for (const team of teams) {
        process.stdout.write(`  📍 ${team.name}...`);

        const squadData = await fetchTeamStats(team.id, league.seasonId);

        if (!squadData || squadData.length === 0) {
            process.stdout.write(' ⚠️ Aucune donnée\n');
            results.failed++;
            continue;
        }

        let teamUpdated = 0;
        let teamSkipped = 0;

        // Traiter chaque joueur de l'équipe
        for (const playerData of squadData) {
            if (!playerData.player) {
                teamSkipped++;
                continue;
            }

            const apiPlayer = playerData.player;

            // Trouver le joueur dans notre base JSON par son ID SportMonks
            let playerIndex = players.findIndex(p => p.sportmonksId === apiPlayer.id);

            if (playerIndex === -1) {
                teamSkipped++;
                continue;
            }

            // Récupérer les stats détaillées si nécessaire
            const detailedStats = await fetchPlayerDetailedStats(apiPlayer.id, league.seasonId);

            // Mapper les stats
            const mappedStats = mapStatsToModel(playerData, detailedStats, league.seasonId);

            // Mettre à jour seulement si on a des stats
            if (Object.keys(mappedStats).length > 0) {
                // Mettre à jour les statistiques du joueur
                players[playerIndex].statistics = {
                    ...players[playerIndex].statistics,
                    ...mappedStats
                };

                players[playerIndex].lastUpdated = new Date().toISOString();

                teamUpdated++;
                results.updated++;

                // Collecter les meilleurs buteurs
                if (mappedStats.goals > 0) {
                    results.topScorers.push({
                        name: players[playerIndex].displayName || players[playerIndex].name,
                        team: team.name,
                        goals: mappedStats.goals,
                        appearances: mappedStats.appearances
                    });
                }
            } else {
                teamSkipped++;
                results.skipped++;
            }
        }

        process.stdout.write(` ✅ ${teamUpdated} mis à jour, ${teamSkipped} ignorés\n`);

        // Pause entre les équipes pour éviter de surcharger l'API
        await new Promise(resolve => setTimeout(resolve, 500));
    }

    // Sauvegarder les joueurs mis à jour
    fs.writeFileSync(playersPath, JSON.stringify(players, null, 2));

    return results;
}

// Fonction principale
async function syncAllLeaguesStats() {
    try {
        console.log('🚀 Démarrage de la synchronisation des statistiques pour tous les championnats');
        console.log('📅 Saison 2025/2026');
        console.log('⏳ Cette opération peut prendre 15-20 minutes...\n');

        const globalResults = {
            total: { updated: 0, skipped: 0, failed: 0 },
            byLeague: {},
            allTopScorers: []
        };

        // Traiter chaque ligue
        for (const league of LEAGUES) {
            const results = await syncLeagueStats(league);

            globalResults.total.updated += results.updated;
            globalResults.total.skipped += results.skipped;
            globalResults.total.failed += results.failed;
            globalResults.byLeague[league.name] = results;
            globalResults.allTopScorers = globalResults.allTopScorers.concat(results.topScorers);

            // Pause entre les ligues
            if (LEAGUES.indexOf(league) < LEAGUES.length - 1) {
                console.log('\n⏳ Pause de 5 secondes avant la prochaine ligue...');
                await new Promise(resolve => setTimeout(resolve, 5000));
            }
        }

        // Afficher le résumé global
        console.log('\n' + '='.repeat(60));
        console.log('📊 RÉSUMÉ GLOBAL DE LA SYNCHRONISATION');
        console.log('='.repeat(60));
        console.log(`✅ Total joueurs mis à jour: ${globalResults.total.updated}`);
        console.log(`⏭️ Total joueurs ignorés: ${globalResults.total.skipped}`);
        console.log(`❌ Total erreurs: ${globalResults.total.failed}`);

        // Résumé par ligue
        console.log('\n📈 Détails par championnat:');
        for (const league of LEAGUES) {
            const results = globalResults.byLeague[league.name];
            if (results) {
                console.log(`${league.color} ${league.name}: ${results.updated} mis à jour, ${results.skipped} ignorés`);
            }
        }

        // Top 10 buteurs tous championnats confondus
        console.log('\n🏆 Top 10 buteurs (tous championnats):');
        globalResults.allTopScorers
            .sort((a, b) => b.goals - a.goals)
            .slice(0, 10)
            .forEach((player, index) => {
                console.log(`${index + 1}. ${player.name} (${player.team}): ${player.goals} buts en ${player.appearances} matchs`);
            });

        console.log('\n✨ Synchronisation terminée avec succès!');

    } catch (error) {
        console.error('❌ Erreur fatale:', error);
        process.exit(1);
    }
}

// Lancer le script
if (require.main === module) {
    syncAllLeaguesStats()
        .then(() => {
            process.exit(0);
        })
        .catch(error => {
            console.error('\n❌ Erreur lors de la synchronisation:', error);
            process.exit(1);
        });
}

module.exports = { syncAllLeaguesStats };