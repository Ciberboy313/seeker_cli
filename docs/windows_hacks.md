# Windows Hacks Cookbook / Cookbook comandi Windows

## English

This file contains pre-approved commands used by the application when a request matches the cookbook.
WARNING: Theme commands restart Windows Explorer, so the desktop/taskbar may disappear briefly.

### Windows Theme Management

Set Light Theme:
```powershell
Set-ItemProperty -Path HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize -Name AppsUseLightTheme -Value 1 -Type Dword -Force; Set-ItemProperty -Path HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize -Name SystemUsesLightTheme -Value 1 -Type Dword -Force; Stop-Process -Name explorer -Force; Start-Process explorer.exe
```

Set Dark Theme:
```powershell
Set-ItemProperty -Path HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize -Name AppsUseLightTheme -Value 0 -Type Dword -Force; Set-ItemProperty -Path HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize -Name SystemUsesLightTheme -Value 0 -Type Dword -Force; Stop-Process -Name explorer -Force; Start-Process explorer.exe
```

Verify Current Theme:
```powershell
Get-ItemProperty -Path HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize | Select-Object AppsUseLightTheme, SystemUsesLightTheme
```
Notes: 1 means light, 0 means dark. `AppsUseLightTheme` is for apps, `SystemUsesLightTheme` is for system UI.

## Italiano

Questo file contiene comandi pre-approvati usati dall applicazione quando una richiesta corrisponde al cookbook.
ATTENZIONE: i comandi tema riavviano Windows Explorer, quindi desktop e taskbar potrebbero sparire per pochi secondi.

### Gestione tema Windows

Imposta tema chiaro:
```powershell
Set-ItemProperty -Path HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize -Name AppsUseLightTheme -Value 1 -Type Dword -Force; Set-ItemProperty -Path HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize -Name SystemUsesLightTheme -Value 1 -Type Dword -Force; Stop-Process -Name explorer -Force; Start-Process explorer.exe
```

Imposta tema scuro:
```powershell
Set-ItemProperty -Path HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize -Name AppsUseLightTheme -Value 0 -Type Dword -Force; Set-ItemProperty -Path HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize -Name SystemUsesLightTheme -Value 0 -Type Dword -Force; Stop-Process -Name explorer -Force; Start-Process explorer.exe
```

Verifica tema corrente:
```powershell
Get-ItemProperty -Path HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize | Select-Object AppsUseLightTheme, SystemUsesLightTheme
```
Note: 1 significa chiaro, 0 significa scuro. `AppsUseLightTheme` e per le app, `SystemUsesLightTheme` per la UI di sistema.
