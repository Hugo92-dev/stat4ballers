@echo off
echo ================================
echo MISE A JOUR SECURISEE DES STATS
echo ================================
echo.
echo Cette mise a jour:
echo - Fait un backup automatique avant
echo - Verifie que tout fonctionne
echo - Restaure le backup si erreur
echo.

cd scripts
python update_now.py

if %ERRORLEVEL% EQU 0 (
    echo.
    echo =============================
    echo MISE A JOUR REUSSIE !
    echo =============================
) else (
    echo.
    echo =============================
    echo ERREUR - Site non modifie
    echo Verifiez logs dans scripts/logs
    echo =============================
)

echo.
pause