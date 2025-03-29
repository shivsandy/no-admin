@echo off
setlocal

:: Get the current user from the environment variable
set "user=%USERNAME%"

:: Define the source path (the folder where the script is running)
set "source=%~dp0"

:: Define the destination path
set "destination=C:\Users\%user%\resolution"

:: Create the folder if it doesn't exist
if not exist "%destination%" (
    mkdir "%destination%"
)

:: Copy the resolution.exe to the new folder
copy "%source%resolution.exe" "%destination%\"

:: Copy the uninstaller.bat to the new folder
copy "%source%uninstaller.bat" "%destination%\"

:: Set permissions for the copied resolution.exe file
icacls "%destination%\resolution.exe" /grant "%user%:F" /T

:: Remove write permission for the resolution.exe file
icacls "%destination%\resolution.exe" /deny "%user%:W" /T

:: Create a shortcut in the startup folder (shell:startup)
set "startup=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
copy "%destination%\resolution.exe" "%startup%\resolution.exe"

:: Run the application after copying
start "" "%destination%\resolution.exe"

:: Notify the user
echo Setup complete. The application has been copied to "%destination%" and will run at startup.
echo Uninstaller.bat has been copied to "%destination%" as well.
pause

endlocal
