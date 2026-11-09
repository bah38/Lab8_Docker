param([Parameter(Mandatory=$true)][string]$OutputPath)
if (-not ('LabScreenDpi' -as [type])) {
    Add-Type @'
using System.Runtime.InteropServices;
public class LabScreenDpi {
    [DllImport("user32.dll")] public static extern bool SetProcessDPIAware();
}
'@
}
[LabScreenDpi]::SetProcessDPIAware() | Out-Null
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing
$bounds = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
$bitmap = New-Object System.Drawing.Bitmap($bounds.Width, $bounds.Height)
$graphics = [System.Drawing.Graphics]::FromImage($bitmap)
try {
    $graphics.CopyFromScreen($bounds.Location, [System.Drawing.Point]::Empty, $bounds.Size)
    $bitmap.Save($OutputPath, [System.Drawing.Imaging.ImageFormat]::Png)
} finally {
    $graphics.Dispose()
    $bitmap.Dispose()
}
