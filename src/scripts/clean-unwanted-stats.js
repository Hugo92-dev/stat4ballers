const fs = require('fs');
const path = require('path');

async function cleanUnwantedStats() {
    try {
        console.log('🧹 Nettoyage des statistiques non désirées\n');

        // Lire le fichier JSON des joueurs
        const playersPath = path.join(__dirname, '../../data/db/players.json');
        let players = [];

        try {
            const data = fs.readFileSync(playersPath, 'utf8');
            players = JSON.parse(data);
            console.log(`✅ ${players.length} joueurs trouvés dans la base de données\n`);
        } catch (error) {
            console.error('❌ Erreur lors de la lecture du fichier players.json:', error.message);
            return;
        }

        let playersUpdated = 0;
        const statsToRemove = ['expectedGoals', 'injuries', 'accurateThroughBalls', 'accurateLongBalls'];

        // Nettoyer chaque joueur
        players.forEach((player, index) => {
            if (player.statistics) {
                let hasChanges = false;

                statsToRemove.forEach(stat => {
                    if (player.statistics[stat] !== undefined) {
                        delete player.statistics[stat];
                        hasChanges = true;
                    }
                });

                if (hasChanges) {
                    player.lastUpdated = new Date().toISOString();
                    playersUpdated++;
                }
            }
        });

        // Sauvegarder les joueurs nettoyés
        fs.writeFileSync(playersPath, JSON.stringify(players, null, 2));

        console.log('🎉 Nettoyage terminé avec succès!');
        console.log(`✅ ${playersUpdated} joueurs mis à jour`);
        console.log('\n📋 Statistiques supprimées:');
        console.log('  - Expected Goals (expectedGoals)');
        console.log('  - Injuries (injuries)');
        console.log('  - Accurate Through Balls (accurateThroughBalls)');
        console.log('  - Accurate Long Balls (accurateLongBalls)');

    } catch (error) {
        console.error('❌ Erreur fatale:', error);
    }
}

// Lancer le nettoyage
cleanUnwantedStats();