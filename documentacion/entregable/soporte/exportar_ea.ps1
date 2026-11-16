param([switch]$ReutilizarExportaciones)
$ErrorActionPreference = 'Stop'
$entrega = Split-Path $PSScriptRoot -Parent
$raiz = Split-Path (Split-Path $entrega -Parent) -Parent
$eaApp = [Runtime.InteropServices.Marshal]::GetActiveObject('EA.App')
$repo = $eaApp.Repository
$esperado = Join-Path $raiz 'documentacion/modelo-clases/entrega-20261110-021751/Modelo-negocio-Padre-Julian-Lorente.eapx'
if ([IO.Path]::GetFullPath($repo.ConnectionString) -ne [IO.Path]::GetFullPath($esperado)) {
    throw 'La instancia abierta no corresponde a la entrega revisada. No se cambia de repositorio automáticamente.'
}
$pngDir = Join-Path $PSScriptRoot 'exportaciones-ea'
$fuenteDir = Join-Path $entrega 'fuente-enterprise'
New-Item -ItemType Directory -Path $pngDir,$fuenteDir -Force | Out-Null
$proyecto = $repo.GetProjectInterface()
function Get-Rows([string]$sql) {
    [xml]$xml = $repo.SQLQuery($sql)
    @($xml.SelectNodes('//Row'))
}
$tablas = @('t_package','t_object','t_diagram','t_diagramobjects','t_connector','t_attribute','t_operation','t_objectconstraint','t_objectproperties')
foreach ($tabla in $tablas) {
    [IO.File]::WriteAllText((Join-Path $PSScriptRoot "ea-$tabla.xml"), $repo.SQLQuery("SELECT * FROM $tabla"), [Text.UTF8Encoding]::new($false))
}
$diagramas = Get-Rows 'SELECT Diagram_ID, Name, Diagram_Type, Package_ID, ea_guid FROM t_diagram'
$clasesPrevias = Get-Content (Join-Path (Split-Path $esperado -Parent) 'diagramas-ea.json') -Raw -Encoding UTF8 | ConvertFrom-Json
$clasesIds = @($clasesPrevias | ForEach-Object { [int]$_.diagramId })
$salida = @()
foreach ($d in $diagramas) {
    $id = [int]$d.Diagram_ID
    $tipo = if ($id -eq 1) { 'contexto' } elseif ($d.Name -match '^CU-(00|G\d{2}) -') { 'casos-uso' } elseif ($id -in $clasesIds) { 'clases' } else { $null }
    if (-not $tipo) { continue }
    $nombre = '{0}-{1:D3}.png' -f $tipo,$id
    $archivo = Join-Path $pngDir $nombre
    $ok = if ($ReutilizarExportaciones -and (Test-Path -LiteralPath $archivo)) { $true } else { $proyecto.PutDiagramImageToFile($proyecto.GUIDtoXML([string]$d.ea_guid), $archivo, 1) }
    if (-not $ok -or -not (Test-Path -LiteralPath $archivo)) { throw "No se pudo exportar el diagrama $id" }
    $salida += [ordered]@{id=$id;nombre=[string]$d.Name;tipo=$tipo;guid=[string]$d.ea_guid;packageId=[int]$d.Package_ID;archivo="soporte/exportaciones-ea/$nombre"}
}
# Copia de lectura compartida: no se cierra EA ni se modifica la fuente.
# Se exige estabilidad de la fuente al terminar y que la copia abra en ACE.
function Get-SharedHash([string]$path) {
    $s = [IO.File]::Open($path,[IO.FileMode]::Open,[IO.FileAccess]::Read,[IO.FileShare]::ReadWrite)
    try { $h=[Security.Cryptography.SHA256]::Create(); try { [BitConverter]::ToString($h.ComputeHash($s)).Replace('-','') } finally { $h.Dispose() } } finally { $s.Dispose() }
}
$antes = Get-SharedHash $esperado
$destino = Join-Path $fuenteDir 'Modelo-negocio-Padre-Julian-Lorente.eapx'
$src = [IO.File]::Open($esperado,[IO.FileMode]::Open,[IO.FileAccess]::Read,[IO.FileShare]::ReadWrite)
try { $dst=[IO.File]::Create($destino); try { $src.CopyTo($dst) } finally { $dst.Dispose() } } finally { $src.Dispose() }
$despues=Get-SharedHash $esperado
$copiaHash=Get-SharedHash $destino
if ($antes -ne $despues -or $antes -ne $copiaHash) { throw 'La fuente cambió durante la copia. Repetir cuando no haya ediciones.' }
$cn=New-Object -ComObject ADODB.Connection
$cn.Open("Provider=Microsoft.ACE.OLEDB.12.0;Data Source=$destino;Mode=Read;")
$cuentas=@()
try {
    foreach($t in $tablas) {
        $rs=$cn.Execute("SELECT COUNT(*) AS total FROM $t")
        $copiado=[int]$rs.Fields.Item(0).Value
        $actual=[int]((Get-Rows "SELECT COUNT(*) AS total FROM $t").total)
        if($copiado -ne $actual){throw "Recuento distinto en $t"}
        $cuentas+=[ordered]@{tabla=$t;filas=$copiado;coincide=$true}
    }
} finally { $cn.Close() }
[ordered]@{fecha='2026-11-10';fuente=$esperado;copia='fuente-enterprise/Modelo-negocio-Padre-Julian-Lorente.eapx';sha256=$copiaHash;fuenteEstableDuranteCopia=$true;copiaLeidaConACE=$true;cuentas=$cuentas;diagramas=$salida;nota='Exportaciones mediante Automation Interface. Fuente abierta, sin cambios durante la captura; se compararon huellas y recuentos. No se sustituyó el original ni se eliminaron LDB.'} | ConvertTo-Json -Depth 8 | Set-Content (Join-Path $PSScriptRoot 'inventario-entrega-ea.json') -Encoding UTF8
Write-Output "Exportados $($salida.Count) diagramas y copiado fuente EA con SHA-256 verificado."
