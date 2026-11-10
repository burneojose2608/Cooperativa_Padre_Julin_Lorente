$ErrorActionPreference='Stop'
$out=(Get-Content (Join-Path $PSScriptRoot 'entrega-actual.txt')).Trim()
$meta=Get-Content -Raw (Join-Path $out 'procedencia.json') | ConvertFrom-Json
$ea=[Runtime.InteropServices.Marshal]::GetActiveObject('EA.App')
$r=$ea.Repository
if ($r.ConnectionString -eq $meta.original) {
    $r.CloseFile()
    $meta.sha256Original=(Get-FileHash -LiteralPath $meta.original -Algorithm SHA256).Hash
    $backup=Join-Path $out ('respaldo-cerrado-'+$meta.fecha+'.eapx')
    Copy-Item -LiteralPath $meta.original -Destination $backup
    Copy-Item -LiteralPath $meta.original -Destination $meta.copia -Force
    $meta | Add-Member -NotePropertyName respaldoConsistente -NotePropertyValue $backup -Force
    $meta | Add-Member -NotePropertyName sha256RespaldoConsistente -NotePropertyValue (Get-FileHash $backup -Algorithm SHA256).Hash -Force
    $meta | ConvertTo-Json -Depth 6 | Set-Content -Encoding UTF8 (Join-Path $out 'procedencia.json')
    if (-not $r.OpenFile($meta.copia)) { throw 'EA no pudo abrir copia' }
}
Write-Output ('CONEXION: '+$r.ConnectionString)
[xml]$p=$r.SQLQuery("SELECT Package_ID,Name,Parent_ID,ea_guid FROM t_package WHERE Name='Vista_Logica'")
$p.EADATA.Dataset_0.Data.Row | ConvertTo-Json
