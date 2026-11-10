$ErrorActionPreference='Stop'
$out=(Get-Content (Join-Path $PSScriptRoot 'entrega-actual.txt')).Trim()
$meta=Get-Content -Raw -Encoding UTF8 (Join-Path $out 'procedencia.json') | ConvertFrom-Json
$r=([Runtime.InteropServices.Marshal]::GetActiveObject('EA.App')).Repository
if($r.ConnectionString -ne $meta.copia){throw 'Copia incorrecta'}
$r.CloseFile()
if(-not $r.OpenFile($meta.copia)){throw 'No se pudo volver a abrir la copia'}
[xml]$xml=$r.SQLQuery("SELECT Object_ID,ea_guid,Alias FROM t_object WHERE Object_Type='Class'")
$result=@()
foreach($row in ($xml.SelectNodes('//Row') | Where-Object {([string]$_.Alias).StartsWith('PJL.CL.')})){
    $e=$r.GetElementByGuid([string]$row.ea_guid)
    $updated=$e.Update()
    $result+=,[ordered]@{id=$e.ElementID;guid=$e.ElementGUID;nombre=$e.Name;tipo=$e.Type;editable=$updated;atributosNativos=$e.Attributes.Count;operacionesNativas=$e.Methods.Count;restricciones=$e.Constraints.Count}
    if(-not $updated){throw ('No editable '+$e.Name)}
}
$result | ConvertTo-Json -Depth 5 | Set-Content -Encoding UTF8 (Join-Path $out 'reapertura-y-editabilidad.json')
$principal=Get-Content -Raw -Encoding UTF8 (Join-Path $out 'diagramas-ea.json') | ConvertFrom-Json | Where-Object id -EQ 'V-00'
$r.OpenDiagram($principal.diagramId)
Write-Output ('Copia reabierta. '+$result.Count+' clases editables confirmadas por API; panorama abierto.')
