const fs = require('fs');
const path = require('path');
const axios = require('axios');
require('dotenv').config();

// Configuration
const API_KEY = 'KCKLQvVx687XrO9EBMLbZYEf8lQ7frEfZ9dvSqHt9PSIYMplUiVI3s3g34qZ';
const BASE_URL = 'https://api.sportmonks.com/v3/football';
const SEASON_ID = 25651; // Saison 2025/2026

// Configuration des championnats et leurs équipes
const LEAGUES = {
    'Ligue 1': [
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
        { name: 'Reims', id: 848 },
        { name: 'Montpellier', id: 552 },
        { name: 'Saint-Étienne', id: 669 },
        { name: 'Monaco', id: 631 },
        { name: 'Auxerre', id: 3682 }
    ],
    'Premier League': [
        { name: 'Manchester United', id: 14 },
        { name: 'Newcastle United', id: 19 },
        { name: 'Watford', id: 29 },
        { name: 'Wolverhampton Wanderers', id: 39 },
        { name: 'West Ham United', id: 49 },
        { name: 'Liverpool', id: 51 },
        { name: 'Leicester City', id: 54 },
        { name: 'Southampton', id: 68 },
        { name: 'Tottenham Hotspur', id: 73 },
        { name: 'Arsenal', id: 82 },
        { name: 'Manchester City', id: 85 },
        { name: 'Everton', id: 338 },
        { name: 'Bournemouth', id: 566 },
        { name: 'Chelsea', id: 610 },
        { name: 'Crystal Palace', id: 703 },
        { name: 'Fulham', id: 720 },
        { name: 'Brighton & Hove Albion', id: 788 },
        { name: 'West Bromwich Albion', id: 885 },
        { name: 'Aston Villa', id: 958 },
        { name: 'Brentford', id: 255 }
    ],
    'La Liga': [
        { name: 'Valencia', id: 84 },
        { name: 'Espanyol', id: 285 },
        { name: 'Getafe', id: 546 },
        { name: 'Cádiz', id: 595 },
        { name: 'Real Madrid', id: 3468 },
        { name: 'Barcelona', id: 83 },
        { name: 'Atlético Madrid', id: 612 },
        { name: 'Athletic Club', id: 86 },
        { name: 'Real Sociedad', id: 548 },
        { name: 'Real Betis', id: 713 },
        { name: 'Villarreal', id: 94 },
        { name: 'Celta Vigo', id: 715 },
        { name: 'Sevilla', id: 536 },
        { name: 'Mallorca', id: 714 },
        { name: 'Girona', id: 2443 },
        { name: 'Osasuna', id: 604 },
        { name: 'Leganés', id: 724 },
        { name: 'Alavés', id: 278 },
        { name: 'Las Palmas', id: 99 },
        { name: 'Real Valladolid', id: 2394 }
    ],
    'Serie A': [
        { name: 'Roma', id: 98 },
        { name: 'Juventus', id: 496 },
        { name: 'Milan', id: 497 },
        { name: 'Internazionale', id: 498 },
        { name: 'Napoli', id: 499 },
        { name: 'Lazio', id: 487 },
        { name: 'Atalanta', id: 499 },
        { name: 'Fiorentina', id: 502 },
        { name: 'Torino', id: 625 },
        { name: 'Bologna', id: 503 },
        { name: 'Hellas Verona', id: 504 },
        { name: 'Udinese', id: 623 },
        { name: 'Cagliari', id: 491 },
        { name: 'Genoa', id: 489 },
        { name: 'Lecce', id: 488 },
        { name: 'Monza', id: 4245 },
        { name: 'Parma', id: 526 },
        { name: 'Como', id: 519 },
        { name: 'Empoli', id: 520 },
        { name: 'Venezia', id: 518 }
    ],
    'Bundesliga': [
        { name: 'Bayern München', id: 2 },
        { name: 'Borussia Dortmund', id: 72 },
        { name: 'RB Leipzig', id: 383 },
        { name: 'Bayer Leverkusen', id: 89 },
        { name: 'Union Berlin', id: 411 },
        { name: 'VfB Stuttgart', id: 88 },
        { name: 'Borussia Mönchengladbach', id: 172 },
        { name: 'Eintracht Frankfurt', id: 87 },
        { name: 'Werder Bremen', id: 91 },
        { name: 'SC Freiburg', id: 97 },
        { name: 'TSG Hoffenheim', id: 2446 },
        { name: 'FC Augsburg', id: 191 },
        { name: 'VfL Wolfsburg', id: 85 },
        { name: 'Mainz 05', id: 96 },
        { name: 'FC Köln', id: 90 },
        { name: 'Holstein Kiel', id: 1616 },
        { name: 'VfL Bochum', id: 93 },
        { name: 'St. Pauli', id: 1620 }
    ]
};

// Fonction pour récupérer les statistiques d'une équipe pour une saison
async function fetchTeamSeasonStats(teamId, teamName) {
    try {
        console.log(`📊 Récupération des stats pour ${teamName} (ID: ${teamId})...`);

        // Utiliser l'endpoint exact fourni avec include statistics.details
        const url = `${BASE_URL}/teams/seasons/${SEASON_ID}`;
        const response = await axios.get(url, {
            params: {
                api_token: API_KEY,
                include: 'statistics.details',
                filter: `teamIds:${teamId}`
            },
            timeout: 15000
        });

        if (response.data && response.data.data && response.data.data.length > 0) {
            const teamData = response.data.data[0];
            if (teamData.statistics && teamData.statistics.length > 0) {
                // Trouver les stats de la bonne saison
                const seasonStats = teamData.statistics.find(s => s.season_id === SEASON_ID);

                if (seasonStats && seasonStats.details && seasonStats.details.length > 0) {
                    const details = seasonStats.details;

                    // Helper function pour trouver une stat par type_id
                    const findStat = (typeId) => {
                        const stat = details.find(d => d.type_id === typeId);
                        return stat ? stat.value : null;
                    };

                    console.log(`✅ Stats trouvées pour ${teamName}`);
                    return {
                        teamId: teamId,
                        teamName: teamName,
                        seasonId: SEASON_ID,
                        statistics: {
                            // Stats générales
                            rating: findStat(118) || null,
                            gamesPlayed: findStat(188) || 0,
                            wins: findStat(214) || 0,
                            draws: findStat(215) || 0,
                            losses: findStat(216) || 0,

                            // Buts
                            goalsScored: findStat(191) || 0,
                            goalsConceded: findStat(88) || 0,
                            goalDifference: (findStat(191) || 0) - (findStat(88) || 0),

                            // Clean sheets
                            cleanSheets: findStat(194) || 0,
                            cleanSheetsPercentage: findStat(9674) || 0,

                            // Possession et passes
                            averagePossession: findStat(182) || null,

                            // Cartons
                            yellowCards: findStat(84) || 0,
                            redCards: findStat(83) || 0,

                            // Moyennes
                            averageGoalsScored: findStat(9680) || 0,
                            averageGoalsConceded: findStat(9679) || 0,

                            // Points et classement
                            points: findStat(212) || 0,
                            position: null, // Position pas disponible dans les détails

                            // Age moyen de l'équipe
                            averagePlayerAge: findStat(9673) || null,

                            // Dernière mise à jour
                            lastUpdated: new Date().toISOString()
                        }
                    };
                }
            }
        }

        console.log(`⚠️ Aucune statistique trouvée pour ${teamName}`);
        return {
            teamId: teamId,
            teamName: teamName,
            seasonId: SEASON_ID,
            statistics: null
        };

    } catch (error) {
        console.error(`❌ Erreur pour ${teamName}:`, error.response?.data?.message || error.message);
        return {
            teamId: teamId,
            teamName: teamName,
            seasonId: SEASON_ID,
            statistics: null,
            error: error.message
        };
    }
}

// Fonction pour traiter une ligue
async function processLeague(leagueName, teams) {
    console.log(`\n🏆 Traitement de ${leagueName}...`);
    const leagueStats = [];

    for (const team of teams) {
        const stats = await fetchTeamSeasonStats(team.id, team.name);
        leagueStats.push(stats);

        // Pause entre les requêtes pour respecter les limites de l'API
        await new Promise(resolve => setTimeout(resolve, 500));
    }

    return leagueStats;
}

// Fonction principale
async function syncAllTeamsStats() {
    console.log('🚀 Début de la synchronisation des statistiques des équipes...\n');

    const allStats = {};
    let totalTeams = 0;
    let successfulTeams = 0;

    for (const [leagueName, teams] of Object.entries(LEAGUES)) {
        const leagueStats = await processLeague(leagueName, teams);
        allStats[leagueName] = leagueStats;

        totalTeams += teams.length;
        successfulTeams += leagueStats.filter(s => s.statistics !== null).length;

        console.log(`✅ ${leagueName}: ${leagueStats.filter(s => s.statistics !== null).length}/${teams.length} équipes avec des stats\n`);
    }

    // Sauvegarder les données
    const dataDir = path.join(__dirname, '../../data/db');
    if (!fs.existsSync(dataDir)) {
        fs.mkdirSync(dataDir, { recursive: true });
    }

    const filePath = path.join(dataDir, 'teams-stats.json');

    // Si le fichier existe, on le charge et on met à jour
    let existingData = {};
    if (fs.existsSync(filePath)) {
        try {
            existingData = JSON.parse(fs.readFileSync(filePath, 'utf8'));
        } catch (error) {
            console.error('⚠️ Impossible de lire le fichier existant, création d\'un nouveau fichier');
        }
    }

    // Fusionner les nouvelles données avec les existantes
    const finalData = {
        ...existingData,
        ...allStats,
        metadata: {
            lastUpdate: new Date().toISOString(),
            season: SEASON_ID,
            totalTeams: totalTeams,
            teamsWithStats: successfulTeams
        }
    };

    fs.writeFileSync(filePath, JSON.stringify(finalData, null, 2));

    console.log(`\n✨ Synchronisation terminée!`);
    console.log(`📊 ${successfulTeams}/${totalTeams} équipes avec des statistiques`);
    console.log(`💾 Données sauvegardées dans: ${filePath}`);
}

// Lancer le script
syncAllTeamsStats().catch(error => {
    console.error('❌ Erreur fatale:', error);
    process.exit(1);
});