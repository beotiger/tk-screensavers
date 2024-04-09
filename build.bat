@ECHO OFF

REM @2024_04_04_1330 by Beotiger
REM Compile tkscrsavers.py into bundled frozen exe using tkscrsavers.spec
REM See README.md for details

REM Add --log-level DEBUG parameter if something goes wrong
pipenv run pyinstaller tkscrsavers.spec --noconfirm --clean

if %ERRORLEVEL% NEQ 0 (
    ECHO Error encountered. Details above...
    EXIT /B %ERRORLEVEL%
)

REM Rename exe to scr. Use right mouse click and Install on tkscrsavers.scr file
REM to install it as a screensaver for Windows(tm)

REM Or copy tkscrsavers.scr file to WINDOWS/System32 folder
REM Or run install.bat file here

ECHO.
COPY .\dist\tkscrsavers.exe .\dist\tkscrsavers.scr

ECHO.
ECHO Success! Now run install.bat file to install it to system screensavers directory.
ECHO.
ECHO Or you can do right mouse click on .\dist\tkscrsavers.scr file
ECHO and choose Install option in context menu which does not require administrative privileges

ECHO.
ECHO See you late dude!
ECHO -- Beotiger 2024-04-09 09:09
