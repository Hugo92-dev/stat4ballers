#!/usr/bin/env node
/**
 * Scheduler automatique pour le refresh des données
 * Exécute le script de refresh tous les lundis et vendredis à 21h (heure française)
 */

const cron = require('node-cron');
const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

// Configuration
const SCHEDULE = '0 21 * * 1,5'; // Lundi (1) et Vendredi (5) à 21h00
const PYTHON_SCRIPT = path.join(__dirname, 'refresh_all_data.py');
const LOG_DIR = path.join(__dirname, '..', 'logs');
const LOG_FILE = path.join(LOG_DIR, 'scheduler.log');

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

// Fonction pour exécuter le script Python
function runRefresh() {
    log('🚀 Démarrage du refresh automatique des données');
    
    const pythonProcess = spawn('python', [PYTHON_SCRIPT], {
        cwd: path.join(__dirname, '..'),
        env: { ...process.env, PYTHONIOENCODING: 'utf-8' }
    });
    
    pythonProcess.stdout.on('data', (data) => {
        const output = data.toString('utf8').trim();
        if (output) {
            console.log(output);
        }
    });
    
    pythonProcess.stderr.on('data', (data) => {
        const error = data.toString('utf8').trim();
        if (error) {
            log(`Erreur Python: ${error}`, 'ERROR');
        }
    });
    
    pythonProcess.on('close', (code) => {
        if (code === 0) {
            log('✅ Refresh terminé avec succès', 'SUCCESS');
        } else {
            log(`❌ Refresh terminé avec le code: ${code}`, 'ERROR');
        }
    });
    
    pythonProcess.on('error', (error) => {
        log(`❌ Erreur lors de l'exécution: ${error.message}`, 'ERROR');
    });
}

// Fonction pour afficher le prochain refresh
function getNextRunTime() {
    const now = new Date();
    const dayOfWeek = now.getDay();
    const currentHour = now.getHours();
    
    let daysUntilNext;
    
    // Si lundi et avant 21h, c'est aujourd'hui
    if (dayOfWeek === 1 && currentHour < 21) {
        daysUntilNext = 0;
    }
    // Si entre lundi 21h et vendredi avant 21h
    else if ((dayOfWeek === 1 && currentHour >= 21) || (dayOfWeek > 1 && dayOfWeek < 5) || (dayOfWeek === 5 && currentHour < 21)) {
        daysUntilNext = 5 - dayOfWeek;
    }
    // Si vendredi après 21h ou weekend
    else {
        daysUntilNext = dayOfWeek === 0 ? 1 : (8 - dayOfWeek);
    }
    
    const nextRun = new Date(now);
    nextRun.setDate(now.getDate() + daysUntilNext);
    nextRun.setHours(21, 0, 0, 0);
    
    // Si c'est aujourd'hui mais l'heure est passée, passer au prochain
    if (daysUntilNext === 0 && currentHour >= 21) {
        nextRun.setDate(nextRun.getDate() + (dayOfWeek === 1 ? 4 : 3));
    }
    
    return nextRun;
}

// Démarrer le scheduler
log('=' .repeat(60));
log('🕐 DÉMARRAGE DU SCHEDULER AUTOMATIQUE');
log('=' .repeat(60));
log(`📅 Programmé pour: Tous les lundis et vendredis à 21h00 (heure française)`);

const nextRun = getNextRunTime();
log(`⏭️ Prochain refresh: ${nextRun.toLocaleString('fr-FR')}`);

// Planifier la tâche
const task = cron.schedule(SCHEDULE, () => {
    runRefresh();
}, {
    scheduled: true,
    timezone: "Europe/Paris"
});

// Gestion de l'arrêt propre
process.on('SIGINT', () => {
    log('\n⚠️ Arrêt du scheduler demandé...', 'WARNING');
    task.stop();
    log('✅ Scheduler arrêté proprement');
    process.exit(0);
});

process.on('SIGTERM', () => {
    log('\n⚠️ Signal SIGTERM reçu, arrêt du scheduler...', 'WARNING');
    task.stop();
    process.exit(0);
});

// Garder le processus actif
log('✅ Scheduler actif et en attente...');
log('ℹ️ Appuyez sur Ctrl+C pour arrêter le scheduler\n');