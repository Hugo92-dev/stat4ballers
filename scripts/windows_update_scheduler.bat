@echo off
REM Script de mise à jour automatique pour Windows Task Scheduler
REM À exécuter les lundis et vendredis à 21h

echo ========================================
echo Mise à jour des données Stat4Ballers
echo %date% %time%
echo ========================================

REM Aller dans le répertoire du projet
cd /d C:\Users\hugo\stat4ballers

REM Activer l'environnement Python si nécessaire
REM call venv\Scripts\activate

REM Aller dans le dossier des scripts
cd scripts

REM Exécuter le script de mise à jour
python update_all_data.py

REM Vérifier si la mise à jour a réussi
if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✓ Mise à jour réussie
    
    REM Retourner au dossier racine
    cd ..
    
    REM Ajouter et commiter les changements
    git add -A
    git commit -m "Auto-update: %date% %time%"
    git push
    
    echo ✓ Changements poussés sur GitHub
) else (
    echo.
    echo ⚠ Erreur lors de la mise à jour
    echo Code d'erreur: %ERRORLEVEL%
)

echo.
echo ========================================
echo Fin de la mise à jour
echo ========================================

REM Garder la fenêtre ouverte pendant 10 secondes pour voir les résultats
timeout /t 10