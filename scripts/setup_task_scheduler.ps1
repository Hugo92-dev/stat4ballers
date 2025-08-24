# Script PowerShell pour créer les tâches planifiées Windows
# Exécuter ce script en tant qu'administrateur

$taskPath = "\Stat4Ballers\"
$scriptPath = "C:\Users\hugo\stat4ballers\scripts\windows_update_scheduler.bat"

# Créer le dossier de tâches s'il n'existe pas
$folder = Get-ScheduledTask | Where-Object {$_.TaskPath -eq $taskPath}
if (-not $folder) {
    $null = New-Item -Path "HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Schedule\TaskCache\Tree" -Name "Stat4Ballers" -Force
}

# Tâche du lundi soir
$actionMonday = New-ScheduledTaskAction -Execute $scriptPath
$triggerMonday = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Monday -At 9:00PM
$principalMonday = New-ScheduledTaskPrincipal -UserId "$env:USERNAME" -LogonType Interactive -RunLevel Highest
$settingsMonday = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

Register-ScheduledTask -TaskName "Stat4Ballers Update Monday" `
    -TaskPath $taskPath `
    -Action $actionMonday `
    -Trigger $triggerMonday `
    -Principal $principalMonday `
    -Settings $settingsMonday `
    -Description "Mise à jour automatique des données Stat4Ballers - Lundi 21h" `
    -Force

Write-Host "✓ Tâche du lundi créée" -ForegroundColor Green

# Tâche du vendredi soir
$actionFriday = New-ScheduledTaskAction -Execute $scriptPath
$triggerFriday = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Friday -At 9:00PM
$principalFriday = New-ScheduledTaskPrincipal -UserId "$env:USERNAME" -LogonType Interactive -RunLevel Highest
$settingsFriday = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

Register-ScheduledTask -TaskName "Stat4Ballers Update Friday" `
    -TaskPath $taskPath `
    -Action $actionFriday `
    -Trigger $triggerFriday `
    -Principal $principalFriday `
    -Settings $settingsFriday `
    -Description "Mise à jour automatique des données Stat4Ballers - Vendredi 21h" `
    -Force

Write-Host "✓ Tâche du vendredi créée" -ForegroundColor Green

# Afficher les tâches créées
Write-Host "`nTâches planifiées créées:" -ForegroundColor Yellow
Get-ScheduledTask -TaskPath $taskPath | Format-Table TaskName, State, Triggers

Write-Host "`nPour voir les tâches: Ouvrir 'Planificateur de tâches' et naviguer vers Stat4Ballers" -ForegroundColor Cyan
Write-Host "Pour tester manuellement: Clic droit sur une tâche > Exécuter" -ForegroundColor Cyan