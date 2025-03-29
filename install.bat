@echo off
chcp 65001 >nul
echo Vérification et installation des modules requis...

:: Vérifie si Python est installé
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python n'est pas installé. Installez Python et réessayez.
    pause
    exit
)

:: Installe les modules nécessaires
pip install --upgrade discord aiohttp psutil mss requests pycryptodome

:: Exécute main.py
echo Lancement de main.py...
start main.py