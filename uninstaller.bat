@echo off
setlocal

:: Get the current user from the environment variable
set "user=%USERNAME%"

:: Define the destination path
set "destination=C:\Users\%user%\resolution"

:: Define the Startup folder path
set "startup=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"

:: Remove the shortcut from the Startup folder
if exist "%startup%\resolution.exe" (
    del "%startup%\resolution.exe"
    echo Startup shortcut removed successfully.
) else (
    echo No startup shortcut found.
)

:: Remove the resolution.exe from the destination folder
if exist "%destination%\resolution.exe" (
    del "%destination%\resolution.exe"
    echo resolution.exe removed successfully from "%destination%" folder.
) else (
    echo resolution.exe not found in "%destination%" folder.
)

:: Remove the folder if it's empty
if exist "%destination%" (
    rmdir "%destination%"
    echo Folder "%destination%" removed successfully.
) else (
    echo Folder "%destination%" not found.
)

:: Notify the user about the uninstallation completion
echo Uninstallation completed successfully. All changes have been reversed.

:: Wait for 5 seconds before auto-closing the script
timeout /t 5 /nobreak >nul

endlocal
