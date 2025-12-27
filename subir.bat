@echo off
echo Buscando Git...
where git >nul 2>&1
if errorlevel 1 (
    echo Git no encontrado en PATH.
    echo Abriendo Git Bash...
    start "" "%ProgramFiles%\Git\git-bash.exe"
    echo Ejecuta estos comandos en Git Bash:
    echo cd "/c/Users/Rafael/Desktop/VECTA 12D Automatico"
    echo git init
    echo git add .
    echo git commit -m "Primera subida"
    echo git remote add origin https://github.com/porleyrafael/VECTA-12D-Automatico.git
    echo git push -u origin main
) else (
    echo Git encontrado. Configurando...
    git init
    git add .
    git commit -m "Primera subida"
    git remote add origin https://github.com/porleyrafael/VECTA-12D-Automatico.git
    git push -u origin main
)
pause