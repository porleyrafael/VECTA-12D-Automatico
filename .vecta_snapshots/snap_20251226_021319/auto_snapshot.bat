@echo off
echo VECTA 12D - Sistema de Auto-Snapshots
echo ===================================
cd /d "C:\Users\Rafael\Desktop\VECTA 12D Automatico"
python vecta_snapshot_system.py snapshot "Auto-snapshot despues de cambios"
echo.
echo Snapshot creado automaticamente.
echo Para generar reporte: python vecta_snapshot_system.py report
pause