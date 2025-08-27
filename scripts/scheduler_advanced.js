#!/usr/bin/env node
/**
 * Scheduler automatique avancé avec horaires décalés par championnat
 * Exécute les refresh selon un planning précis pour chaque ligue
 */

const cron = require('node-cron');
const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

// Configuration des horaires par championnat
// Format: [heures, minutes, script]
const LEAGUE_SCHEDULES = {
    // Lundis et vendredis à différentes heures
    'bundesliga': {
        schedule: '0 17 * * 1,5',  // 17h00 lundi et vendredi
        script: 'refresh_bundesliga.py',
        name: '🇩🇪 Bundesliga'
    },
    'serie_a': {
        schedule: '0 18 * * 1,5',  // 18h00 lundi et vendredi
        script: 'refresh_serie_a.py',
        name: '🇮🇹 Serie A'
    },
    'liga': {
        schedule: '0 19 * * 1,5',  // 19h00 lundi et vendredi
        script: 'refresh_liga.py',
        name: '🇪🇸 La Liga'
    },
    'premier_league': {
        schedule: '0 20 * * 1,5',  // 20h00 lundi et vendredi
        script: 'refresh_premier_league.py',
        name: '🏴󠁧󠁢󠁥󠁮󠁧󠁿 Premier League'
    },
    'ligue1': {
        schedule: '0 21 * * 1,5',  // 21h00 lundi et vendredi
        script: 'refresh_ligue1.py',
        name: '🇫🇷 Ligue 1'
    }
};

// Dossier des logs
const LOG_DIR = path.join(__dirname, '..', 'logs');
const LOG_FILE = path.join(LOG_DIR, 'scheduler_advanced.log');

// Créer le dossier logs s'il n'existe pas
if (!fs.existsSync(LOG_DIR)) {
    fs.mkdirSync(LOG_DIR, { recursive: true });
}

// Fonction de log
function log(message, level = 'INFO') {
    const timestamp = new Date().toISOString();
    const logMessage = `[${timestamp}] [${level}] ${message}\n`;
    
    console.log(logMessage.trim());
    
    try {
        fs.appendFileSync(LOG_FILE, logMessage, 'utf8');
    } catch (error) {
        console.error('Erreur lors de l\'écriture du log:', error);
    }
}

// Fonction pour exécuter un script Python
function runRefresh(leagueName, scriptName) {
    log(`🚀 Démarrage du refresh ${leagueName}`);
    
    const pythonScript = path.join(__dirname, scriptName);
    const pythonProcess = spawn('python', [pythonScript], {
        cwd: path.join(__dirname),
        env: { ...process.env, PYTHONIOENCODING: 'utf-8' }
    });
    
    let outputBuffer = '';
    
    pythonProcess.stdout.on('data', (data) => {
        const output = data.toString('utf8').trim();
        if (output) {
            outputBuffer += output + '\n';
            // Afficher seulement les lignes importantes
            if (output.includes('✅') || output.includes('❌') || output.includes('📊')) {
                console.log(`[${leagueName}] ${output}`);
            }
        }
    });
    
    pythonProcess.stderr.on('data', (data) => {
        const error = data.toString('utf8').trim();
        if (error) {
            log(`Erreur ${leagueName}: ${error}`, 'ERROR');
        }
    });
    
    pythonProcess.on('close', (code) => {
        if (code === 0) {
            log(`✅ ${leagueName} terminé avec succès`, 'SUCCESS');
        } else {
            log(`❌ ${leagueName} terminé avec le code: ${code}`, 'ERROR');
        }
        
        // Sauvegarder le résumé dans un fichier
        const summaryFile = path.join(LOG_DIR, `last_${scriptName.replace('.py', '')}.log`);
        try {
            fs.writeFileSync(summaryFile, outputBuffer, 'utf8');
        } catch (error) {
            log(`Impossible de sauvegarder le résumé pour ${leagueName}`, 'WARNING');
        }
    });
    
    pythonProcess.on('error', (error) => {
        log(`❌ Erreur lors de l'exécution ${leagueName}: ${error.message}`, 'ERROR');
    });
}

// Fonction pour obtenir les prochaines exécutions
function getNextRuns() {
    const now = new Date();
    const nextRuns = [];
    
    for (const [key, config] of Object.entries(LEAGUE_SCHEDULES)) {
        const parts = config.schedule.split(' ');
        const hour = parseInt(parts[1]);
        const dayOfWeek = now.getDay();
        const currentHour = now.getHours();
        
        let nextRun = new Date(now);
        
        // Trouver le prochain lundi ou vendredi
        if (dayOfWeek === 1 && currentHour < hour) {
            // C'est lundi et avant l'heure
            nextRun.setHours(hour, 0, 0, 0);
        } else if (dayOfWeek === 5 && currentHour < hour) {
            // C'est vendredi et avant l'heure
            nextRun.setHours(hour, 0, 0, 0);
        } else if (dayOfWeek === 1 && currentHour >= hour) {
            // Lundi après l'heure -> vendredi
            nextRun.setDate(now.getDate() + 4);
            nextRun.setHours(hour, 0, 0, 0);
        } else if (dayOfWeek === 5 && currentHour >= hour) {
            // Vendredi après l'heure -> lundi prochain
            nextRun.setDate(now.getDate() + 3);
            nextRun.setHours(hour, 0, 0, 0);
        } else if (dayOfWeek < 1 || dayOfWeek === 0) {
            // Dimanche -> lundi
            nextRun.setDate(now.getDate() + (1 - dayOfWeek + 7) % 7);
            nextRun.setHours(hour, 0, 0, 0);
        } else if (dayOfWeek < 5) {
            // Entre mardi et jeudi -> vendredi
            nextRun.setDate(now.getDate() + (5 - dayOfWeek));
            nextRun.setHours(hour, 0, 0, 0);
        } else {
            // Samedi -> lundi
            nextRun.setDate(now.getDate() + 2);
            nextRun.setHours(hour, 0, 0, 0);
        }
        
        nextRuns.push({
            name: config.name,
            time: nextRun,
            hour: `${hour}h00`
        });
    }
    
    return nextRuns.sort((a, b) => a.time - b.time);
}

// Fonction principale
function main() {
    log('=' .repeat(60));
    log('🕐 DÉMARRAGE DU SCHEDULER AVANCÉ');
    log('=' .repeat(60));
    
    // Afficher la configuration
    log('\n📅 Planning des refresh automatiques:');
    log('  Lundi et Vendredi:');
    log('    • 17h00 - 🇩🇪 Bundesliga');
    log('    • 18h00 - 🇮🇹 Serie A');
    log('    • 19h00 - 🇪🇸 La Liga');
    log('    • 20h00 - 🏴󠁧󠁢󠁥󠁮󠁧󠁿 Premier League');
    log('    • 21h00 - 🇫🇷 Ligue 1');
    
    // Afficher les prochaines exécutions
    const nextRuns = getNextRuns();
    log('\n⏭️ Prochaines exécutions:');
    nextRuns.slice(0, 5).forEach(run => {
        log(`  ${run.name} - ${run.time.toLocaleString('fr-FR')} (${run.hour})`);
    });
    
    // Créer les tâches cron
    const tasks = [];
    
    for (const [key, config] of Object.entries(LEAGUE_SCHEDULES)) {
        const task = cron.schedule(config.schedule, () => {
            runRefresh(config.name, config.script);
        }, {
            scheduled: true,
            timezone: "Europe/Paris"
        });
        
        tasks.push(task);
        log(`✅ Tâche planifiée: ${config.name}`);
    }
    
    // Gestion de l'arrêt propre
    process.on('SIGINT', () => {
        log('\n⚠️ Arrêt du scheduler demandé...', 'WARNING');
        tasks.forEach(task => task.stop());
        log('✅ Toutes les tâches arrêtées');
        process.exit(0);
    });
    
    process.on('SIGTERM', () => {
        log('\n⚠️ Signal SIGTERM reçu...', 'WARNING');
        tasks.forEach(task => task.stop());
        process.exit(0);
    });
    
    log('\n✅ Scheduler actif et en attente...');
    log('ℹ️ Appuyez sur Ctrl+C pour arrêter\n');
}

// Option pour tester un refresh immédiat
if (process.argv[2] === '--test') {
    const league = process.argv[3];
    if (league && LEAGUE_SCHEDULES[league]) {
        log(`🧪 Mode test: Exécution immédiate de ${LEAGUE_SCHEDULES[league].name}`);
        runRefresh(LEAGUE_SCHEDULES[league].name, LEAGUE_SCHEDULES[league].script);
    } else {
        log('❌ Usage: node scheduler_advanced.js --test [ligue1|premier_league|liga|serie_a|bundesliga]', 'ERROR');
        process.exit(1);
    }
} else {
    // Démarrer le scheduler normal
    main();
}