#!/usr/bin/env node
/**
 * Script de refresh manuel des données
 * Permet de lancer le refresh à la demande
 */

const { spawn } = require('child_process');
const path = require('path');
const readline = require('readline');

const PYTHON_SCRIPT = path.join(__dirname, 'refresh_all_data.py');

// Créer l'interface readline pour l'interaction
const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

// Couleurs pour la console
const colors = {
    reset: '\x1b[0m',
    bright: '\x1b[1m',
    green: '\x1b[32m',
    yellow: '\x1b[33m',
    red: '\x1b[31m',
    cyan: '\x1b[36m'
};

function printHeader() {
    console.clear();
    console.log(colors.cyan + '╔════════════════════════════════════════════════╗' + colors.reset);
    console.log(colors.cyan + '║' + colors.bright + '     REFRESH MANUEL DES DONNÉES STAT4BALLERS     ' + colors.reset + colors.cyan + '║' + colors.reset);
    console.log(colors.cyan + '╚════════════════════════════════════════════════╝' + colors.reset);
    console.log('');
    console.log('📊 Ce script va mettre à jour:');
    console.log('  • Les effectifs de tous les clubs');
    console.log('  • Les statistiques de tous les joueurs');
    console.log('  • Les 5 grands championnats européens');
    console.log('');
    console.log(colors.yellow + '⚠️  Note: Le refresh peut prendre plusieurs minutes' + colors.reset);
    console.log('');
}

function runRefresh() {
    console.log(colors.green + '🚀 Démarrage du refresh...' + colors.reset);
    console.log('═'.repeat(50));
    console.log('');
    
    const startTime = Date.now();
    
    const pythonProcess = spawn('python', [PYTHON_SCRIPT], {
        cwd: path.join(__dirname, '..'),
        env: { ...process.env, PYTHONIOENCODING: 'utf-8' }
    });
    
    pythonProcess.stdout.on('data', (data) => {
        process.stdout.write(data.toString('utf8'));
    });
    
    pythonProcess.stderr.on('data', (data) => {
        process.stderr.write(colors.red + data.toString('utf8') + colors.reset);
    });
    
    pythonProcess.on('close', (code) => {
        const duration = ((Date.now() - startTime) / 1000 / 60).toFixed(2);
        
        console.log('');
        console.log('═'.repeat(50));
        
        if (code === 0) {
            console.log(colors.green + colors.bright + '✅ Refresh terminé avec succès!' + colors.reset);
            console.log(`⏱️  Durée totale: ${duration} minutes`);
        } else {
            console.log(colors.red + `❌ Refresh terminé avec des erreurs (code: ${code})` + colors.reset);
            console.log(`⏱️  Durée: ${duration} minutes`);
        }
        
        console.log('');
        askForAnotherRefresh();
    });
    
    pythonProcess.on('error', (error) => {
        console.error(colors.red + `❌ Erreur lors de l'exécution: ${error.message}` + colors.reset);
        askForAnotherRefresh();
    });
}

function askForAnotherRefresh() {
    rl.question('\n' + colors.cyan + '🔄 Voulez-vous lancer un autre refresh? (o/N): ' + colors.reset, (answer) => {
        if (answer.toLowerCase() === 'o' || answer.toLowerCase() === 'oui') {
            console.log('');
            runRefresh();
        } else {
            console.log(colors.green + '\n👋 À bientôt!' + colors.reset);
            rl.close();
            process.exit(0);
        }
    });
}

function main() {
    printHeader();
    
    rl.question(colors.cyan + '❓ Voulez-vous lancer le refresh maintenant? (O/n): ' + colors.reset, (answer) => {
        if (answer.toLowerCase() === 'n' || answer.toLowerCase() === 'non') {
            console.log(colors.yellow + '\n❌ Refresh annulé' + colors.reset);
            rl.close();
            process.exit(0);
        } else {
            console.log('');
            runRefresh();
        }
    });
}

// Gestion de l'interruption
process.on('SIGINT', () => {
    console.log(colors.yellow + '\n\n⚠️ Refresh interrompu par l\'utilisateur' + colors.reset);
    rl.close();
    process.exit(1);
});

// Lancer le script
main();