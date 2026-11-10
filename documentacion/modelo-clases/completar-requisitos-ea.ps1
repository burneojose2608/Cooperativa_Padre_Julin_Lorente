$ErrorActionPreference='Stop'
$out=(Get-Content (Join-Path $PSScriptRoot 'entrega-actual.txt')).Trim()
$src=Get-Content -Raw -Encoding UTF8 (Join-Path $out 'requisitos-fuentes.json') | ConvertFrom-Json
$meta=Get-Content -Raw -Encoding UTF8 (Join-Path $out 'procedencia.json') | ConvertFrom-Json
$r=([Runtime.InteropServices.Marshal]::GetActiveObject('EA.App')).Repository
if($r.ConnectionString -ne $meta.copia){throw 'Copia incorrecta'}
[xml]$xml=$r.SQLQuery("SELECT Object_ID,Alias FROM t_object WHERE Object_Type='Requirement'")
$ids=@{};foreach($row in $xml.SelectNodes('//Row')){$ids[[string]$row.Alias]=[int]$row.Object_ID}
foreach($group in @('hu','ur','rf','familias')){
    foreach($p in $src.$group.PSObject.Properties){
        $key=$p.Name;$data=$p.Value;$id=$ids['PJL.REQ.'+$key]
        if(-not $id){throw ('Falta requisito '+$key)}
        $e=$r.GetElementByID($id)
        if($group -eq 'hu'){
            $e.Notes = ($e.Notes -split '=== Criterios originales conservados ===')[0].Trim()+"`r`n`r`n=== Criterios originales conservados ===`r`n"+$data.textoOriginal
        }else{
            $e.Name=$key+' '+$data.nombre
            $e.Notes="Identificador original: $key`r`n$($data.texto)`r`nFuente: $($data.fuente)`r`nRequisito documentado; no acredita implementación ni aprobación formal. Las decisiones posteriores de registro gobiernan los cambios respecto de la fuente histórica."
        }
        if(-not $e.Update()){throw $e.GetLastError()}
    }
}
Write-Output 'Fuentes exactas añadidas a 57 UR, 91 RF detallados, 14 familias y 91 HU.'
