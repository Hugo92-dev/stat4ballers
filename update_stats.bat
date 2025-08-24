@echo off
echo ================================
echo 🔄 Mise à jour des statistiques
echo ================================
echo.

cd scripts
python update_all_data.py

echo.
echo ✅ Mise à jour terminée !
pause