$ErrorActionPreference = 'Stop'
$base = $PSScriptRoot
$fecha = Get-Date -Format 'yyyyMMdd-HHmmss'
$salida = Join-Path $base "entrega-$fecha"
New-Item -ItemType Directory -Path $salida | Out-Null
$original = Join-Path (Split-Path $base -Parent) 'ProyeectoPadreJulianLorente.eapx'
$appEa = [Runtime.InteropServices.Marshal]::GetActiveObject('EA.App')
$repo = $appEa.Repository
$conexion = $repo.ConnectionString
if ([IO.Path]::GetFullPath($conexion) -ne [IO.Path]::GetFullPath($original)) { throw "La instancia abierta no corresponde al original esperado: $conexion" }
$tablas = @('t_package','t_object','t_diagram','t_connector','t_attribute','t_operation','t_objectscenarios','t_objectproperties','t_diagramobjects','t_diagramlinks')
foreach ($tabla in $tablas) {
    $xml = $repo.SQLQuery("SELECT * FROM $tabla")
    [IO.File]::WriteAllText((Join-Path $salida "antes-$tabla.xml"), $xml, [Text.UTF8Encoding]::new($false))
}
$backup = Join-Path $salida "respaldo-original-$fecha.eapx"
$copia = Join-Path $salida 'Modelo-negocio-Padre-Julian-Lorente.eapx'
Copy-Item -LiteralPath $original -Destination $backup
Copy-Item -LiteralPath $original -Destination $copia
$meta = [ordered]@{fecha=$fecha; original=$original; conexionActiva=$conexion; respaldo=$backup; copia=$copia; sha256Original=(Get-FileHash -LiteralPath $original -Algorithm SHA256).Hash; sha256Respaldo=(Get-FileHash -LiteralPath $backup -Algorithm SHA256).Hash; procesoEA=(Get-Process EA | Select-Object Id,StartTime,MainWindowTitle)}
$meta | ConvertTo-Json -Depth 5 | Set-Content -Encoding UTF8 (Join-Path $salida 'procedencia.json')
$salida | Set-Content -Encoding UTF8 (Join-Path $base 'entrega-actual.txt')
Write-Output ($meta | ConvertTo-Json -Depth 5)
