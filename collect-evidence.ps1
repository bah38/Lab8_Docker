$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot
$Host.UI.RawUI.WindowTitle = 'Lab 8 - Batoul Hachem - bah38'
Add-Type @'
using System;
using System.Runtime.InteropServices;
public class LabConsole {
    [DllImport("kernel32.dll")] public static extern IntPtr GetConsoleWindow();
    [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);
    [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr hWnd);
}
'@
$handle = [LabConsole]::GetConsoleWindow()
[LabConsole]::ShowWindow($handle, 3) | Out-Null
[LabConsole]::SetForegroundWindow($handle) | Out-Null
function Save-Command([string]$Name, [string]$Command) {
    Clear-Host
    Write-Host 'Lab 8 - Batoul Hachem (bah38)' -ForegroundColor Cyan
    Write-Host "PS> $Command" -ForegroundColor Yellow
    $result = & cmd.exe /c "$Command 2>&1" | Out-String -Width 160
    Write-Host $result
    "PS> $Command`r`n$result" | Set-Content "evidence/$Name.txt"
    Start-Sleep -Seconds 2
    & "$PSScriptRoot/capture-screen.ps1" -OutputPath "$PSScriptRoot/evidence/$Name.png"
}
Save-Command '01-docker-ps' 'docker ps -a'
Save-Command '02-docker-stop' 'docker stop lab8-bah38-hello'
Save-Command '03-docker-logs' 'docker logs lab8-bah38-hello'
Save-Command '04-stopped-container' 'docker ps -a --filter name=lab8-bah38-hello'
Save-Command '05-images' 'docker image ls --filter reference=bah38/lab8-batoul_hachem'
docker start lab8-bah38-hello | Out-Null
'complete' | Set-Content evidence/capture-complete.txt
