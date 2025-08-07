@echo off
echo ========================================
echo    GENERATOR LINKU DLA FIRMY
echo ========================================
echo.

echo Szukanie adresu IP...
for /f "tokens=2 delims=:" %%i in ('ipconfig ^| findstr /i "IPv4"') do (
    set IP=%%i
    goto :found
)

:found
set IP=%IP: =%
echo.
echo ========================================
echo   GOTOWY LINK DLA CAŁEJ FIRMY:
echo.
echo   http://%IP%:5000
echo.
echo ========================================
echo.
echo Skopiuj ten link i wyślij wszystkim w firmie!
echo.
echo Instrukcje:
echo 1. Wyślij link emailem do wszystkich
echo 2. Każdy wchodzi w przeglądarce na ten adres
echo 3. Aplikacja działa na komputerach i telefonach
echo.
echo UWAGA: Ten komputer musi być włączony!
echo.
pause
