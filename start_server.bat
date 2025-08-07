@echo off
echo ========================================
echo    System Rezerwacji Salek - DACPOL
echo ========================================
echo.

cd /d "%~dp0"

echo Instalowanie wymaganych pakietow...
venv\Scripts\pip.exe install -r requirements.txt

echo.
echo Uruchamianie serwera...
echo.
echo ========================================
echo   GOTOWE! Otwórz przeglądarkę i wejdź na:
echo.
echo   http://localhost:5000
echo.
echo   W sieci lokalnej (dla innych):
echo   http://%COMPUTERNAME%:5000
echo   lub
echo   http://IP-KOMPUTERA:5000
echo ========================================
echo.
echo Aby zatrzymać serwer, naciśnij Ctrl+C
echo.

venv\Scripts\python.exe app.py

pause
