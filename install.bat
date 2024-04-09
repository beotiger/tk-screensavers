@ECHO off

:: @2024_04_09_1223 by Beotiger

:: Installing compiled tkscrsavers.scr to Windows\System32 folder

:: Restart as Administrator if not already running as Administrator
(NET session >nul 2>&1)||(MSHTA "javascript: var shell = new ActiveXObject('shell.application'); shell.ShellExecute('%~nx0', '', '', 'runas', 1);close();" & Exit /B)

:: Restoring current working directory
PUSHD "%~dp0"
SET CWD=%cd%\dist

SET TARGET_DIR=%SystemRoot%\System32
SET BASE_FILENAME=tkscrsavers.scr

ECHO Copying %CWD%\%BASE_FILENAME% to %TARGET_DIR% ...
COPY %CWD%\%BASE_FILENAME% %TARGET_DIR%
if %ERRORLEVEL% NEQ 0 (
    ECHO Error encountered. Details above.
    ECHO.
    ECHO Did you run this batch as administrator?
    ECHO.
    PAUSE
    EXIT /B %ERRORLEVEL%
)

ECHO.
ECHO SUCCESS! %BASE_FILENAME% should now be available in
ECHO Window's Screen Saver Settings dialog:
ECHO.
ECHO "System Settings -> Personalization -> Lock screen -> Screen saver settings"
ECHO.
ECHO See you later dude!
ECHO -- Beotiger 2024-04-09 24:04:09
PAUSE
