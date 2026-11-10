$ErrorActionPreference='Stop'
$out=(Get-Content (Join-Path $PSScriptRoot 'entrega-actual.txt')).Trim()
$meta=Get-Content -Raw -Encoding UTF8 (Join-Path $out 'procedencia.json') | ConvertFrom-Json
$m=Get-Content -Raw -Encoding UTF8 (Join-Path $out 'modelo-revisado.json') | ConvertFrom-Json
$manifest=Get-Content -Raw -Encoding UTF8 (Join-Path $out 'diagramas-ea.json') | ConvertFrom-Json
$r=([Runtime.InteropServices.Marshal]::GetActiveObject('EA.App')).Repository
if($r.ConnectionString -ne $meta.copia){throw 'Copia incorrecta'}
$project=$r.GetProjectInterface()
$historia=$m.vistas | Where-Object id -EQ 'V-22'
$historia.relaciones=@($historia.relaciones | Where-Object {$_ -notin @('REL-016','REL-062','REL-063')})
if('REL-015' -notin $historia.relaciones){$historia.relaciones+=,'REL-015'}
$m | ConvertTo-Json -Depth 35 | Set-Content -Encoding UTF8 (Join-Path $out 'modelo-revisado.json')
foreach($vid in @('V-22','V-30')){
    $entry=$manifest | Where-Object id -EQ $vid
    $v=$m.vistas | Where-Object id -EQ $vid
    $r.CloseDiagram($entry.diagramId)
    $d=$r.GetDiagramByID($entry.diagramId)
    for($i=0;$i -lt $d.DiagramLinks.Count;$i++){
        $dl=$d.DiagramLinks.GetAt($i);$co=$r.GetConnectorByID($dl.ConnectorID)
        if($vid -eq 'V-22' -and $co.Notes -match '^\[PJL:(REL-016|REL-062|REL-063)\]'){
            $dl.IsHidden=$true;$dl.Update() | Out-Null
        }
        if($vid -eq 'V-22' -and $co.Notes -match '^\[PJL:REL-015\]'){$dl.IsHidden=$false;$dl.Update() | Out-Null}
        if($vid -eq 'V-22' -and $co.Notes -match '^\[PJL:(REL-062|REL-063)\]'){
            $key=$matches[1];$a=$v.posiciones.Usuario;$b=$v.posiciones.Canje
            $lane=[int](($a.x+$a.w+$b.x)/2)+$(if($key -eq 'REL-062'){-50}else{50})
            $y1=[int]($a.y+$a.h/2);$y2=[int]($b.y+$b.h/2)
            $dl.LineStyle=3;$dl.Path="$($lane):$(-$y1);$($lane):$(-$y2);"
            if(-not $dl.Update()){throw $dl.GetLastError()}
        }
        if($vid -eq 'V-30' -and $co.Notes -match '^\[PJL:REL-026\]'){
            $dl.LineStyle=2;$dl.Path='';$dl.Geometry=''
            if(-not $dl.Update()){throw $dl.GetLastError()}
        }
    }
    $d.Update() | Out-Null;$r.ReloadDiagram($d.DiagramID)
    if(-not $project.PutDiagramImageToFile($project.GUIDtoXML($d.DiagramGUID),$entry.archivo,1)){throw 'No exportado'}
    Write-Output ('Recorrido final exportado '+$vid)
}
$principal=$manifest | Where-Object id -EQ 'V-00';$r.OpenDiagram($principal.diagramId)
foreach($tabla in @('t_diagram','t_diagramobjects','t_diagramlinks')){[IO.File]::WriteAllText((Join-Path $out "despues-$tabla.xml"),$r.SQLQuery("SELECT * FROM $tabla"),[Text.UTF8Encoding]::new($false))}
