const fs = require('fs');
const path = require('path');
const axios = require('axios');
require('dotenv').config();

// Configuration
const API_KEY = 'KCKLQvVx687XrO9EBMLbZYEf8lQ7frEfZ9dvSqHt9PSIYMplUiVI3s3g34qZ';
const BASE_URL = 'https://api.sportmonks.com/v3/football';

// League configurations with season IDs and club IDs for 2025/2026
const LEAGUES = [
    {
        name: 'Ligue 1',
        slug: 'ligue1',
        seasonId: 25651,
        teams: [
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
        ]
    },
    {
        name: 'Premier League',
        slug: 'premierleague',
        seasonId: 25583,
        teams: [
            { name: 'West Ham United', id: 1 },
            { name: 'Sunderland', id: 3 },
            { name: 'Tottenham Hotspur', id: 6 },
            { name: 'Liverpool', id: 8 },
            { name: 'Manchester City', id: 9 },
            { name: 'Fulham', id: 11 },
            { name: 'Everton', id: 13 },
            { name: 'Manchester United', id: 14 },
            { name: 'Aston Villa', id: 15 },
            { name: 'Chelsea', id: 18 },
            { name: 'Arsenal', id: 19 },
            { name: 'Newcastle United', id: 20 },
            { name: 'Burnley', id: 27 },
            { name: 'Wolverhampton Wanderers', id: 29 },
            { name: 'Crystal Palace', id: 51 },
            { name: 'AFC Bournemouth', id: 52 },
            { name: 'Nottingham Forest', id: 63 },
            { name: 'Leeds United', id: 71 },
            { name: 'Brighton & Hove Albion', id: 78 },
            { name: 'Brentford', id: 236 }
        ]
    },
    {
        name: 'La Liga',
        slug: 'laliga',
        seasonId: 25659,
        teams: [
            { name: 'Celta Vigo', id: 36 },
            { name: 'FC Barcelona', id: 83 },
            { name: 'Real Oviedo', id: 93 },
            { name: 'Getafe', id: 106 },
            { name: 'Valencia', id: 214 },
            { name: 'Girona', id: 231 },
            { name: 'Rayo Vallecano', id: 377 },
            { name: 'Osasuna', id: 459 },
            { name: 'Real Betis', id: 485 },
            { name: 'Espanyol', id: 528 },
            { name: 'Real Sociedad', id: 594 },
            { name: 'Mallorca', id: 645 },
            { name: 'Sevilla', id: 676 },
            { name: 'Elche', id: 1099 },
            { name: 'Deportivo Alavés', id: 2975 },
            { name: 'Levante', id: 3457 },
            { name: 'Real Madrid', id: 3468 },
            { name: 'Villarreal', id: 3477 },
            { name: 'Atlético Madrid', id: 7980 },
            { name: 'Athletic Club', id: 13258 }
        ]
    },
    {
        name: 'Serie A',
        slug: 'seriea',
        seasonId: 25533,
        teams: [
            { name: 'Roma', id: 37 },
            { name: 'Lazio', id: 43 },
            { name: 'Genoa', id: 102 },
            { name: 'Fiorentina', id: 109 },
            { name: 'Milan', id: 113 },
            { name: 'Como', id: 268 },
            { name: 'Udinese', id: 346 },
            { name: 'Parma', id: 398 },
            { name: 'Cagliari', id: 585 },
            { name: 'Napoli', id: 597 },
            { name: 'Torino', id: 613 },
            { name: 'Juventus', id: 625 },
            { name: 'Atalanta', id: 708 },
            { name: 'Pisa', id: 1072 },
            { name: 'Hellas Verona', id: 1123 },
            { name: 'Sassuolo', id: 2714 },
            { name: 'Inter', id: 2930 },
            { name: 'Lecce', id: 7790 },
            { name: 'Bologna', id: 8513 },
            { name: 'Cremonese', id: 10722 }
        ]
    },
    {
        name: 'Bundesliga',
        slug: 'bundesliga',
        seasonId: 25646,
        teams: [
            { name: 'Borussia Dortmund', id: 68 },
            { name: 'Werder Bremen', id: 82 },
            { name: 'FC Augsburg', id: 90 },
            { name: 'RB Leipzig', id: 277 },
            { name: 'St. Pauli', id: 353 },
            { name: 'Eintracht Frankfurt', id: 366 },
            { name: 'FC Bayern München', id: 503 },
            { name: 'VfL Wolfsburg', id: 510 },
            { name: 'Borussia Mönchengladbach', id: 683 },
            { name: 'FSV Mainz 05', id: 794 },
            { name: 'FC Union Berlin', id: 1079 },
            { name: 'Hamburger SV', id: 2708 },
            { name: 'TSG Hoffenheim', id: 2726 },
            { name: 'Heidenheim', id: 2831 },
            { name: 'VfB Stuttgart', id: 3319 },
            { name: 'FC Köln', id: 3320 },
            { name: 'Bayer 04 Leverkusen', id: 3321 },
            { name: 'SC Freiburg', id: 3543 }
        ]
    }
];

// Fonction pour récupérer les statistiques d'une équipe
async function fetchTeamStats(teamId, teamName, seasonId) {
    try {
        console.log(`   📊 Récupération des stats pour ${teamName}...`);

        // Utiliser l'endpoint exact fourni
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
        console.error(`   ❌ Erreur pour ${teamName}:`, error.response?.data?.message || error.message);
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
        const seasonStats = detailedStats.statistics.data[0]; // Prendre les stats de la première saison disponible

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

        // Traiter chaque championnat
        for (const league of LEAGUES) {
            console.log(`\n🏆 Traitement de ${league.name} (${league.teams.length} équipes)`);
            console.log('='.repeat(50));

            let leagueUpdated = 0;
            let leagueSkipped = 0;

            // Traiter chaque équipe du championnat
            for (const team of league.teams) {
                const squadData = await fetchTeamStats(team.id, team.name, league.seasonId);

                if (!squadData || squadData.length === 0) {
                    console.log(`   ⚠️ Aucune donnée trouvée pour ${team.name}`);
                    totalFailed++;
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

                    try {
                        // Trouver le joueur dans notre base JSON par son ID SportMonks
                        let playerIndex = players.findIndex(p => p.sportmonksId === apiPlayer.id);

                        if (playerIndex === -1) {
                            teamSkipped++;
                            continue;
                        }

                        // Récupérer les stats détaillées si possible
                        const detailedStats = await fetchPlayerDetailedStats(apiPlayer.id, league.seasonId);

                        // Mapper les stats
                        const mappedStats = mapStatsToModel(playerData, detailedStats);

                        // TOUJOURS mettre à jour les stats, même si elles sont vides ou à 0
                        // Initialiser avec des valeurs par défaut si pas de stats
                        const defaultStats = {
                            rating: 0,
                            appearances: 0,
                            minutesPlayed: 0,
                            goals: 0,
                            assists: 0,
                            yellowCards: 0,
                            redCards: 0,
                            shotsTotal: 0,
                            shotsOnTarget: 0,
                            tackles: 0,
                            interceptions: 0,
                            saves: 0,
                            cleanSheets: 0,
                            goalsConceded: 0,
                            penalties: 0,
                            keyPasses: 0,
                            duelsWon: 0,
                            aerialsWon: 0,
                            successfulDribbles: 0,
                            dispossessed: 0,
                            fouls: 0,
                            foulsDrawn: 0
                        };

                        // Fusionner les stats par défaut avec les stats récupérées
                        const finalStats = {
                            ...defaultStats,
                            ...mappedStats
                        };

                        // Mettre à jour les statistiques du joueur
                        players[playerIndex].statistics = {
                            ...players[playerIndex].statistics,
                            ...finalStats
                        };

                        players[playerIndex].lastUpdated = new Date().toISOString();
                        teamUpdated++;
                        totalUpdated++;

                    } catch (error) {
                        console.error(`      ❌ Erreur pour ${apiPlayer.display_name}:`, error.message);
                        totalFailed++;
                    }
                }

                if (teamUpdated > 0) {
                    console.log(`      ✅ ${team.name}: ${teamUpdated} joueurs mis à jour`);
                } else if (teamSkipped > 0) {
                    console.log(`      ⚠️ ${team.name}: ${teamSkipped} joueurs non trouvés dans la base`);
                } else {
                    console.log(`      ⏭️ ${team.name}: Aucune mise à jour`);
                }

                leagueUpdated += teamUpdated;
                leagueSkipped += teamSkipped;

                // Pause entre les équipes pour éviter de surcharger l'API
                await new Promise(resolve => setTimeout(resolve, 300));
            }

            console.log(`   📊 ${league.name} - Total: ${leagueUpdated} mis à jour, ${leagueSkipped} ignorés`);

            // Pause entre les championnats
            if (LEAGUES.indexOf(league) < LEAGUES.length - 1) {
                console.log('   ⏳ Pause de 2 secondes avant le prochain championnat...');
                await new Promise(resolve => setTimeout(resolve, 2000));
            }
        }

        // Sauvegarder les joueurs mis à jour dans le fichier JSON
        fs.writeFileSync(playersPath, JSON.stringify(players, null, 2));

        console.log('\n' + '='.repeat(60));
        console.log('📊 RÉSUMÉ DE LA SYNCHRONISATION DES STATISTIQUES');
        console.log('='.repeat(60));
        console.log(`✅ Total joueurs mis à jour: ${totalUpdated}`);
        console.log(`⏭️ Total joueurs ignorés: ${totalSkipped}`);
        console.log(`❌ Total erreurs: ${totalFailed}`);

        // Stats par championnat
        console.log('\n📈 Détails par championnat:');
        for (const league of LEAGUES) {
            const leaguePlayers = players.filter(p => p.league === league.slug);
            const withStats = leaguePlayers.filter(p => p.statistics?.appearances > 0);
            console.log(`   ${league.name}: ${withStats.length}/${leaguePlayers.length} joueurs avec des statistiques`);
        }

        // Top buteurs tous championnats confondus
        console.log('\n🌟 Top 10 buteurs tous championnats confondus:');
        const scorers = players.filter(p => p.statistics?.goals > 0);
        scorers.sort((a, b) => (b.statistics?.goals || 0) - (a.statistics?.goals || 0));

        scorers.slice(0, 10).forEach((player, index) => {
            const leagueName = LEAGUES.find(l => l.slug === player.league)?.name || player.league;
            console.log(`${(index + 1).toString().padStart(2)}. ${player.displayName || player.name} (${player.team?.name}, ${leagueName}): ${player.statistics.goals} buts en ${player.statistics.appearances} matchs`);
        });

    } catch (error) {
        console.error('❌ Erreur fatale:', error);
    }
}

// Lancer le script
if (require.main === module) {
    console.log('========================================');
    console.log('  SYNCHRONISATION DES STATISTIQUES  ');
    console.log('========================================');
    console.log('🚀 Démarrage de la synchronisation des statistiques');
    console.log('📅 Saison 2025/2026 pour les 5 grands championnats');
    console.log('⏳ Cette opération peut prendre 15-20 minutes...\n');

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