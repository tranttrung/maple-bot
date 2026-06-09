@echo off
echo ========================================
echo MapleStory Bot - Build Windows Executable
echo ========================================
echo.

echo [1/3] Installing dependencies...
pip install -r requirements.txt

echo [2/3] Installing PyInstaller...
pip install pyinstaller

echo [3/3] Building Executable...
pyinstaller --onefile --name MapleBot src/main.py

echo.
echo ========================================
echo Build complete! 
echo You can find the executable "MapleBot.exe" inside the "dist" folder.
echo.
echo IMPORTANT: Please copy the "src/config.json" file and place it next to "MapleBot.exe" in the "dist" folder before running it!
echo ========================================
pause
