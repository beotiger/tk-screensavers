@ECHO OFF

:: @2024_04_09_1313 by Beotiger
:: Compile tkscrsavers.py into bundled frozen exe
:: with accompanied helping folder using tkscrsavers_onedir.spec
:: See README.md for details

:: Add --log-level DEBUG parameter if something goes wrong
pipenv run pyinstaller tkscrsavers_onedir.spec --noconfirm --clean

if %ERRORLEVEL% NEQ 0 (
    ECHO Error encountered. Details above...
    EXIT /B %ERRORLEVEL%
)

:: Rename exe to scr. Use right mouse click and Install on tkscrsavers.scr file
:: to install it as a screensaver for Windows(tm)

COPY .\dist\tkscrsavers\tkscrsavers.exe .\dist\tkscrsavers\tkscrsavers.scr

ECHO Success!
ECHO Now you can do right mouse click on .\dist\tkscrsavers\tkscrsavers.scr file
ECHO and choose Install option which does not require administrative privileges

ECHO.
ECHO See you late dude!
ECHO -- Beotiger 2024-04-09 09:09
