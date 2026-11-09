Set-Location $PSScriptRoot
$Host.UI.RawUI.WindowTitle = 'Lab 8 - Live API verification - Batoul Hachem'
Add-Type @'
using System;
using System.Runtime.InteropServices;
public class LabApiConsole {
 [DllImport("kernel32.dll")] public static extern IntPtr GetConsoleWindow();
 [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);
 [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr hWnd);
}
'@
$handle = [LabApiConsole]::GetConsoleWindow()
[LabApiConsole]::ShowWindow($handle,3) | Out-Null
[LabApiConsole]::SetForegroundWindow($handle) | Out-Null
Clear-Host
Write-Host 'Lab 8 - Batoul Hachem (bah38)' -ForegroundColor Cyan
Write-Host 'PS> docker ps --filter name=lab8-bah38' -ForegroundColor Yellow
docker ps --filter name=lab8-bah38
Write-Host 'PS> curl.exe http://localhost:5000/api/users' -ForegroundColor Yellow
curl.exe --silent --show-error http://localhost:5000/api/users
Write-Host 'PS> curl.exe http://localhost:3000/get_users' -ForegroundColor Yellow
curl.exe --silent --show-error http://localhost:3000/get_users
Write-Host 'PS> .\.venv\Scripts\python.exe verify_containers.py' -ForegroundColor Yellow
& .\.venv\Scripts\python.exe verify_containers.py
Start-Sleep -Seconds 2
& "$PSScriptRoot/capture-screen.ps1" -OutputPath "$PSScriptRoot/evidence/07-api-results.png"
