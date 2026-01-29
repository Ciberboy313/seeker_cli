@echo off
echo Avvio di Seeker CLI in modalita' di logging...
echo Tutto l'output verra' salvato in session.log
echo.
python main.py > session.log 2>&1