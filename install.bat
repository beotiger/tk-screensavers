@ECHO off

:: @2024_04_09_1223 by Beotiger

:: Installing compiled tkscrsavers.scr to Windows\System32 folder

:: Restart as Administrator if not already running as Administrator
(NET session >nul 2>&1)||(MSHTA "javascript: var shell = new ActiveXObject('shell.application'); shell.ShellExecute('%~nx0', '', '', 'runas', 1);close();" & Exit /B)

:: Restoring current working directory
PUSHD "%~dp0"
SET CWD=%cd%\dist
SET CWD2=%cd%

SET TARGET_DIR=%SystemRoot%\System32
SET BASE_FILENAME=tkscrsavers.scr
:: @2025_02_14_1618 Config settings
SET BASE_CONFIG=settings.json
SET TARGET_CONFIG_PATH=%userprofile%\tkscrsavers.json

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

ECHO Copying %CWD2%\%BASE_CONFIG% to %TARGET_CONFIG_PATH% ...
COPY %CWD2%\%BASE_CONFIG% %TARGET_CONFIG_PATH%

ECHO.
ECHO SUCCESS! %BASE_FILENAME% should now be available in
ECHO Window's Screen Saver Settings dialog:
ECHO.
ECHO "System Settings -> Personalization -> Lock screen -> Screen saver settings"
ECHO.

ECHO
ECHO See you later dude!
ECHO -- Beotiger 2024-04-09 24:04:09
PAUSE
