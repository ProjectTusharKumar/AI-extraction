@echo off
setlocal EnableDelayedExpansion

:: Animation frames for loading
set "frames=- \ | /"
set "delay=1"

:show_loader
for /L %%i in (0,1,3) do (
    cls
    echo !frames:~%%i,1!
    ping -n 2 127.0.0.1 > nul
)
goto :show_loader

:end
endlocal
