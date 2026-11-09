param([string]$Action = 'inspect', [int]$X = 0, [int]$Y = 0)
Add-Type @'
using System;
using System.Runtime.InteropServices;
public class LabDesktop {
 [DllImport("user32.dll")] public static extern bool SetProcessDPIAware();
 [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr hWnd);
 [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);
 [DllImport("user32.dll")] public static extern bool SetCursorPos(int x, int y);
 [DllImport("user32.dll")] public static extern void mouse_event(uint flags, uint dx, uint dy, uint data, UIntPtr extra);
}
'@
[LabDesktop]::SetProcessDPIAware() | Out-Null
$process = Get-Process 'Docker Desktop' | Where-Object {$_.MainWindowHandle -ne 0} | Select-Object -First 1
if ($Action -eq 'activate') {
 $keys = New-Object -ComObject WScript.Shell
 $keys.SendKeys('%')
 $keys.AppActivate($process.Id) | Out-Null
 [LabDesktop]::ShowWindow($process.MainWindowHandle,3) | Out-Null
 [LabDesktop]::SetForegroundWindow($process.MainWindowHandle) | Out-Null
} elseif ($Action -eq 'click') {
 [LabDesktop]::SetCursorPos($X,$Y) | Out-Null
 [LabDesktop]::mouse_event(2,0,0,0,[UIntPtr]::Zero)
 [LabDesktop]::mouse_event(4,0,0,0,[UIntPtr]::Zero)
} else {
 Add-Type -AssemblyName UIAutomationClient
 $element = [System.Windows.Automation.AutomationElement]::FromHandle($process.MainWindowHandle)
 $elements = $element.FindAll([System.Windows.Automation.TreeScope]::Descendants,[System.Windows.Automation.Condition]::TrueCondition)
 foreach ($item in $elements) {
  if ($item.Current.Name -ne '') { '{0} | {1} | {2}' -f $item.Current.ControlType.ProgrammaticName,$item.Current.Name,$item.Current.BoundingRectangle }
 }
}
