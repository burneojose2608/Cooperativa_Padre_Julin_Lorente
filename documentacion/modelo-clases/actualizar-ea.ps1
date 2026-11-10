param([ValidateSet('Modelo','Diagramas','Inventario')][string]$Fase='Modelo')
$ErrorActionPreference='Stop'
$out=(Get-Content (Join-Path $PSScriptRoot 'entrega-actual.txt')).Trim()
$m=Get-Content -Raw -Encoding UTF8 (Join-Path $out 'modelo-revisado.json') | ConvertFrom-Json
$meta=Get-Content -Raw -Encoding UTF8 (Join-Path $out 'procedencia.json') | ConvertFrom-Json
$ea=[Runtime.InteropServices.Marshal]::GetActiveObject('EA.App')
$r=$ea.Repository
if ($r.ConnectionString -ne $meta.copia) { throw 'Solo se permite modificar la copia de trabajo identificada en procedencia.json' }
$project=$r.GetProjectInterface()
function Rows([string]$sql) {
    [xml]$xml=$r.SQLQuery($sql)
    @($xml.SelectNodes('//Row'))
}
$candidates=@(Rows "SELECT Package_ID,Name,Parent_ID,ea_guid FROM t_package WHERE Name='Vista_Logica'")
$logic=@($candidates | Where-Object { ( $r.GetPackageByID([int]$_.Parent_ID)).Name -eq 'Model' })
if ($logic.Count -ne 1) { throw 'Vista_Logica no se identifica unívocamente por nombre y jerarquía' }
$lp=$r.GetPackageByGuid([string]$logic[0].ea_guid)
$logfile=Join-Path $out 'registro-ea.jsonl'
function Log($tipo,$id,$guid,$nombre,$accion) {
    [ordered]@{fecha=(Get-Date -Format o);tipo=$tipo;id=$id;guid=$guid;nombre=$nombre;accion=$accion} | ConvertTo-Json -Compress | Add-Content -Encoding UTF8 $logfile
}
function Save($obj) { if (-not $obj.Update()) { throw ('Error Update: '+$obj.GetLastError()) } }
function FindItem($collection,$name) {
    $collection.Refresh()
    $found=@()
    for($i=0;$i -lt $collection.Count;$i++){ $it=$collection.GetAt($i); if($it.Name -ceq $name){$found+=,$it} }
    if($found.Count -gt 1){throw "Duplicados de $name"}
    if($found.Count -eq 1){return $found[0]}
    return $null
}
function Pkg($parent,$name) {
    $p=FindItem $parent.Packages $name
    $act='reutilizado'
    if($null -eq $p){$p=$parent.Packages.AddNew($name,'');Save $p;$parent.Packages.Refresh();$act='creado'}
    Log 'Package' $p.PackageID $p.PackageGUID $name $act
    return $p
}
$elements=@{}
foreach($row in (Rows 'SELECT Object_ID,Alias FROM t_object')){
    if([string]$row.Alias -like 'PJL.*'){$key=[string]$row.Alias;if($elements.ContainsKey($key)){throw "Alias duplicado $key"};$elements[$key]=$r.GetElementByID([int]$row.Object_ID)}
}
function Elem($pkg,$key,$name,$type,$stereo,$notes) {
    $e=$elements[$key];$act='actualizado'
    if($null -eq $e){$e=$pkg.Elements.AddNew($name,$type);$act='creado'}
    $e.Name=$name;$e.Alias=$key;$e.Stereotype=$stereo;$e.Notes=$notes
    $e.Author='Modelo de análisis PJL';$e.Status='Proposed';Save $e
    $elements[$key]=$e
    Log $type $e.ElementID $e.ElementGUID $name $act
    return $e
}
function Tag($e,$name,$value) {
    $t=FindItem $e.TaggedValues $name
    if($null -eq $t){$t=$e.TaggedValues.AddNew($name,'')}
    if($value.Length -gt 220){$t.Value='<memo>';$t.Notes=$value}else{$t.Value=$value}
    Save $t
}
function Attribute($e,$signature,$notes,$enum=$false) {
    $p=$signature -split ':',2;$name=$p[0].Trim();$type=if($p.Count -gt 1){$p[1].Trim()}else{''}
    $derived=$name.StartsWith('/');$name=$name.TrimStart('/')
    $a=FindItem $e.Attributes $name
    if($null -eq $a){$a=$e.Attributes.AddNew($name,$type)}
    $a.Type=($type -replace '\s*\[0\.\.1\]','');$a.Visibility=if($enum){'Public'}else{'Private'}
    $a.LowerBound=if($type.Contains('[0..1]')){'0'}else{'1'};$a.UpperBound='1'
    $a.IsDerived=$derived;$a.Notes=$notes
    if($elements.ContainsKey('PJL.EN.'+$a.Type)){$a.ClassifierID=$elements['PJL.EN.'+$a.Type].ElementID}
    elseif($elements.ContainsKey('PJL.CL.'+$a.Type)){$a.ClassifierID=$elements['PJL.CL.'+$a.Type].ElementID}
    Save $a
}
function Operation($e,$detail) {
    if($detail.firma -notmatch '^([^\(]+)\((.*)\):\s*(.+)$'){throw ('Firma inválida '+$detail.firma)}
    $name=$matches[1];$parameters=$matches[2];$return=$matches[3]
    $op=FindItem $e.Methods $name
    if($null -eq $op){$op=$e.Methods.AddNew($name,$return)}
    $op.ReturnType=$return;$op.Visibility='Public'
    $op.IsQuery=($detail.tipo -eq 'Consulta')
    $op.Notes="Responsabilidad: $($detail.tipo).`r`n$($detail.estado)`r`nFuente: $($detail.fuente)"
    Save $op
    if($parameters.Trim()){
        $position=0
        foreach($param in ($parameters -split ',\s*')){
            $parts=$param -split ':',2
            $pa=FindItem $op.Parameters $parts[0].Trim()
            if($null -eq $pa){$pa=$op.Parameters.AddNew($parts[0].Trim(),$parts[1].Trim())}
            $pa.Type=$parts[1].Trim();$pa.Kind='in';$pa.Position=$position;$position++;Save $pa
        }
    }
}
$connectors=@{}
foreach($row in (Rows 'SELECT Connector_ID,Notes FROM t_connector')){
    if([string]$row.Notes -match '^\[PJL:([^\]]+)\]'){$connectors[$matches[1]]=$r.GetConnectorByID([int]$row.Connector_ID)}
}
function Link($key,$a,$b,$type,$name,$notes,$stereo='') {
    if($null -eq $a -or $null -eq $b){throw "Extremo nulo $key"}
    $co=$connectors[$key];$act='actualizado'
    if($null -eq $co){$co=$a.Connectors.AddNew($name,$type);$act='creado'}
    $co.SupplierID=$b.ElementID;$co.Name=$name;$co.Stereotype=$stereo
    $co.Notes="[PJL:$key]`r`n$notes";$co.Direction=if($type -eq 'Association'){'Unspecified'}else{'Source -> Destination'}
    Save $co;$connectors[$key]=$co
    Log 'Connector' $co.ConnectorID $co.ConnectorGUID $key $act
    return $co
}
if($Fase -eq 'Modelo'){
    $r.EnableUIUpdates=$false
    try {
        $pkgs=@{}
        foreach($c in $m.clases){if(-not $pkgs.ContainsKey($c.modulo)){$pkgs[$c.modulo]=Pkg $lp $c.modulo}}
        if($elements.ContainsKey('PJL.EN.EstadoCuenta')){$ep=$r.GetPackageByID($elements['PJL.EN.EstadoCuenta'].PackageID);$ep.Name='Tipos de análisis';Save $ep}else{$ep=Pkg $lp 'Tipos de análisis'}
        foreach($en in $m.enumeraciones){
            $e=Elem $ep ('PJL.EN.'+$en.nombre) $en.nombre 'Enumeration' '' ('Valores de análisis traducidos. Fuente: '+$en.fuente)
            foreach($value in $en.valores){Attribute $e $value ('Literal de '+$en.nombre) $true}
        }
        foreach($c in $m.clases){
            $sources=($c.fuentes | ForEach-Object {$_.id+': '+$_.fuente}) -join "`r`n"
            $notes=$c.nota+"`r`nEstado observado: "+$c.estado+"`r`nFuentes:`r`n"+$sources+"`r`nHU directas: "+($c.huDirectas -join ', ')+"`r`nHU de apoyo (no aceptación automática): "+($c.huApoyo -join ', ')
            $e=Elem $pkgs[$c.modulo] ('PJL.CL.'+$c.nombre) $c.nombre 'Class' $c.estereotipo $notes
            Tag $e 'estadoObservado' $c.estado; Tag $e 'nivelModelo' 'Análisis de negocio; responsabilidades conceptuales';Tag $e 'reglas' ($c.reglas -join ', ')
        }
        foreach($c in $m.clases){
            $e=$elements['PJL.CL.'+$c.nombre]
            foreach($a in $c.atributosDetalle){Attribute $e $a.firma ('Atributo de dominio de análisis. Estado observado: '+$a.estado+'. Fuente: '+$a.fuente)}
            foreach($op in $c.operacionesDetalle){Operation $e $op}
            foreach($rid in $c.reglas){
                $rule=$m.reglas | Where-Object id -EQ $rid
                $constraint=FindItem $e.Constraints $rid
                if($null -eq $constraint){$constraint=$e.Constraints.AddNew($rid,'Invariant')}
                $constraint.Notes=$rule.titulo+': '+$rule.texto+"`r`nEstado: "+$rule.estado+"`r`nFuente: "+$rule.fuente
                Save $constraint
            }
        }
        foreach($rel in $m.asociaciones){
            $label=($rel.nombre -split ';')[0]
            $label=(($label -split ' ' | Select-Object -First 4) -join ' ')
            $co=Link $rel.id $elements['PJL.CL.'+$rel.a] $elements['PJL.CL.'+$rel.b] 'Association' ($rel.id+' '+$label) ($rel.justificacion+"`r`nFuente: "+$rel.fuente)
            $co.ClientEnd.Cardinality=$rel.ma;$co.SupplierEnd.Cardinality=$rel.mb
            $co.ClientEnd.Role='';$co.SupplierEnd.Role=''
            if($rel.nombre -match '^responsable|^administrador|^actor|^cuenta afectada'){$co.ClientEnd.Role=if($rel.nombre -match 'entrega'){'responsableEntrega'}elseif($rel.nombre -match 'cuenta afectada'){'cuentaAfectada'}elseif($rel.nombre -match '^actor'){'actor'}else{'responsable'}}
            $co.ClientEnd.Aggregation=if($rel.composicion){2}else{0};$co.SupplierEnd.Aggregation=0
            Save $co
        }
        foreach($dep in $m.dependencias){$null=Link $dep.id $elements['PJL.CL.'+$dep.a] $elements['PJL.CL.'+$dep.b] 'Dependency' $dep.id ($dep.nombre+"`r`nFuente: "+$dep.fuente)}
        $rp=Pkg $lp '00 Requisitos y decisiones'
        $urpkg=Pkg $rp 'Necesidades UR';$rfpkg=Pkg $rp 'Requisitos RF';$hupkg=Pkg $rp 'Historias HU originales';$decpkg=Pkg $rp 'Decisiones posteriores'
        $urs=@{};$rfs=@{};$hus=@{};$families=@{}
        foreach($t in $m.trazabilidad){
            foreach($ur in [regex]::Matches($t.ur,'UR-\d+') | ForEach-Object {$_.Value}){
                if(-not $urs.ContainsKey($ur)){
                    $existing=@(Rows ("SELECT Object_ID,Name,Alias FROM t_object WHERE Object_Type='Requirement' AND (Name='"+$ur+"' OR Alias='"+$ur+"')"))
                    if($existing.Count -eq 1){$urs[$ur]=$r.GetElementByID([int]$existing[0].Object_ID)}else{
                        $urs[$ur]=Elem $urpkg ('PJL.REQ.'+$ur) $ur 'Requirement' '' ('Necesidad original referenciada por '+$t.hu+'. Fuente: Presentacion .(1) (1).xlsx, hoja de necesidades; '+$t.fuente)
                    }
                }
            }
            if($t.rf -notmatch '^(RF-\d+)'){throw ('RF inválido '+$t.rf)};$family=$matches[1]
            if(-not $families.ContainsKey($family)){$families[$family]=Elem $rfpkg ('PJL.REQ.'+$family) $family 'Requirement' '' ('Familia funcional original. Fuente: Presentacion .(1) (1).xlsx y product_con_subtareas.csv. No declara implementación.')}
            $rfs[$t.rf]=Elem $rfpkg ('PJL.REQ.'+$t.rf) $t.rf 'Requirement' '' ($t.titulo+"`r`nFuente: "+$t.fuente+"`r`nEstado: "+$t.estado+"`r`n"+$t.diferencia)
            $null=Link ('RF-FAMILIA.'+$t.rf) $rfs[$t.rf] $families[$family] 'Dependency' 'pertenece a familia' 'Agrupación original del catálogo RF' 'trace'
            foreach($ur in [regex]::Matches($t.ur,'UR-\d+') | ForEach-Object {$_.Value}){$null=Link ('RF-UR.'+$t.rf+'.'+$ur) $rfs[$t.rf] $urs[$ur] 'Dependency' 'deriva de' $t.fuente 'trace'}
            $hus[$t.hu]=Elem $hupkg ('PJL.REQ.'+$t.hu) $t.titulo 'Requirement' '' ("Referencia original $($t.hu), Work item $($t.workItem), tipo $($t.tipo), padre $($t.padreId): $($t.padre).`r`n$($t.fuente)`r`nEstado: $($t.estado).`r`nCobertura: $($t.cobertura).`r`n$($t.diferencia)")
            Tag $hus[$t.hu] 'idOriginal' $t.hu;Tag $hus[$t.hu] 'WorkItem' $t.workItem;Tag $hus[$t.hu] 'padreOriginal' ($t.padreId+': '+$t.padre)
            $null=Link ('HU-RF.'+$t.hu) $hus[$t.hu] $rfs[$t.rf] 'Dependency' 'especifica' $t.fuente 'trace'
            $cu=$r.GetElementByGuid($t.cu.guid)
            if($cu.Type -ne 'UseCase' -or $cu.Name -ne $t.cu.nombre){throw ('CU real cambió '+$t.hu)}
            $null=Link ('HU-CU.'+$t.hu) $hus[$t.hu] $cu 'Dependency' 'correspondencia de análisis' ('Vínculo creado hacia UseCase real; no certifica aceptación ni realiza todos los criterios. '+$t.cuCodigo+' es título de diagrama, no identificador nativo del CU. '+$t.fuente+ ' Correspondencia: '+$t.correspondenciaCU) 'trace'
            $null=Link ('CL-HU.'+$t.clase+'.'+$t.hu) $elements['PJL.CL.'+$t.clase] $hus[$t.hu] 'Dependency' 'responsabilidad de análisis' ($t.operacion+"`r`nReglas: "+($t.reglas -join ', ')+"`r`n"+$t.cobertura+"`r`nFuente: "+$t.fuente+ ' Correspondencia: '+$t.correspondenciaCU) 'trace'
        }
        foreach($t in $m.trazabilidad){if($t.tipo -eq 'Sub-task' -and $t.padre -match '^(HU-\d+)'){$null=Link ('HU-PADRE.'+$t.hu) $hus[$t.hu] $hus[$matches[1]] 'Dependency' 'subtarea de historia consolidada' 'Conserva referencia original; no sumar esfuerzo como historia independiente.' 'trace'}}
        foreach($c in $m.clases){
            if($c.huDirectas.Count -eq 0 -and $c.huApoyo.Count -gt 0){
                $support=$c.huApoyo[0]
                $null=Link ('APOYO.'+$c.nombre+'.'+$support) $elements['PJL.CL.'+$c.nombre] $hus[$support] 'Dependency' 'concepto de apoyo' ('Justificado por reglas '+($c.reglas -join ', ')+'. La nota del elemento conserva otras HU de apoyo; no representa aceptación completa.') 'trace'
            }
        }
        $de=Elem $decpkg 'PJL.REQ.DEC-TEMP' 'DEC-TEMP Validación administrativa temporal' 'Requirement' '' 'Ampliación posterior documentada, sin inventar equivalencia HU-018. Fuente: documentacion/sprint-1-valeria/conversion-administrativa-temporal.md y conversion_socio_service.py. Manual, temporal e idempotente; no conversión comercial.'
        $null=Link 'DEC-TEMP.SERVICIO' $elements['PJL.CL.ValidacionAdministrativaSocio'] $de 'Dependency' 'fundamentado por decisión posterior' 'Alcance implementado temporal; no autoconversión.' 'trace'
    } finally {$r.EnableUIUpdates=$true;$r.RefreshModelView($lp.PackageID)}
    Write-Output ('Modelo creado/actualizado. Vista_Logica: '+$lp.PackageGUID)
}
if($Fase -eq 'Diagramas'){
    $dp=Pkg $lp 'Diagramas de detalle'
    $export=Join-Path $out 'diagramas-ea';New-Item -ItemType Directory -Force $export | Out-Null
    $man=@()
    foreach($v in $m.vistas){
        $pkg=if($v.principal){$lp}else{$dp}
        $diagram=FindItem $pkg.Diagrams $v.nombre
        $act='actualizado'
        if($null -eq $diagram){$diagram=$pkg.Diagrams.AddNew($v.nombre,'Logical');$act='creado'}
        $diagram.Notes="[PJL:$($v.id)] Modelo de clases de análisis. Todos los miembros visibles; responsabilidades conceptuales. Fuente: modelo-revisado.json. Identificadores REL/DEP remiten a RELACIONES.md. Pendientes en REGLAS-Y-PENDIENTES.md."
        $r.CloseDiagram($diagram.DiagramID)
        $diagram.ShowDetails=0;$diagram.ShowPackageContents=$false
        $diagram.ShowPrivate=$true;$diagram.ShowPublic=$true;$diagram.ShowProtected=$true
        $diagram.HighlightImports=$false
        $diagram.ExtendedStyle=([regex]::Replace($diagram.ExtendedStyle,'OpParams=\d+;',''))+'OpParams=2;'
        $diagram.StyleEx=([regex]::Replace($diagram.StyleEx,'ShowOpRetType=\d+;',''))+'ShowOpRetType=1;'
        
        Save $diagram
        $positions=@{};$cols=if($v.clases.Count -le 4){2}else{3}
        $widths=@();$heights=@()
        foreach($name in $v.clases){
            $c=$m.clases | Where-Object nombre -EQ $name
            $max=($c.atributos+$c.operaciones | ForEach-Object {$_.Length} | Measure-Object -Maximum).Maximum
            $widths+=,[int][Math]::Max(340,($max*6.4+70))
            $heights+=,[int][Math]::Max(150,(100+($c.atributos.Count+$c.operaciones.Count)*19))
        }
        $cw=@();for($col=0;$col -lt $cols;$col++){$max=0;for($j=$col;$j -lt $widths.Count;$j+=$cols){$max=[Math]::Max($max,$widths[$j])};$cw+=,$max}
        $rh=@();for($j=0;$j -lt $v.clases.Count;$j+=$cols){$rh+=,([int](($heights[$j..([Math]::Min($j+$cols-1,$heights.Count-1))] | Measure-Object -Maximum).Maximum))}
        for($i=0;$i -lt $v.clases.Count;$i++){
            $name=$v.clases[$i];$e=$elements['PJL.CL.'+$name];$col=$i%$cols;$row=[Math]::Floor($i/$cols)
            $x=70;$y=80
            for($j=0;$j -lt $col;$j++){$x+=$cw[$j]+250}
            for($j=0;$j -lt $row;$j++){$y+=$rh[$j]+240}
            $obj=$null;$diagram.DiagramObjects.Refresh()
            for($j=0;$j -lt $diagram.DiagramObjects.Count;$j++){$candidate=$diagram.DiagramObjects.GetAt($j);if($candidate.ElementID -eq $e.ElementID){$obj=$candidate;break}}
            if($null -eq $obj){$obj=$diagram.DiagramObjects.AddNew("l=$x;r=$($x+$widths[$i]);t=$y;b=$($y+$heights[$i]);",'');$obj.ElementID=$e.ElementID}
            if($null -ne $v.posiciones){$pos=$v.posiciones.PSObject.Properties[$name].Value;$x=[int]$pos.x;$y=[int]$pos.y;$widths[$i]=[int]$pos.w;$heights[$i]=[int]$pos.h}
            $obj.left=$x;$obj.right=$x+$widths[$i];$obj.top=-$y;$obj.bottom=-($y+$heights[$i])
            $obj.FontName='Arial';$obj.FontSize='10';$obj.FontBold=$false
            $obj.FontColor=0
            $obj.ShowPrivateAttributes=$true;$obj.ShowPublicAttributes=$true;$obj.ShowPublicOperations=$true
            $obj.ShowPrivateOperations=$true;$obj.ShowProtectedAttributes=$true;$obj.ShowProtectedOperations=$true
            $obj.ShowConstraints=$false;$obj.ShowNotes=$false;$obj.ShowTags=$false
            $obj.BackgroundColor=if($e.Stereotype -eq 'ServicioDominio'){15921906}elseif($e.Stereotype -eq 'Registro'){15137518}else{16777215}
            Save $obj
        }
        # Se excluye de las vistas de negocio toda trazabilidad de requisitos.
        $diagram.DiagramLinks.Refresh()
        for($j=0;$j -lt $diagram.DiagramLinks.Count;$j++){$hide=$diagram.DiagramLinks.GetAt($j);$hide.IsHidden=$true;Save $hide}
        foreach($key in @($v.relaciones)+@($v.dependencias)){
            $co=$connectors[$key];$dl=$null
            for($j=0;$j -lt $diagram.DiagramLinks.Count;$j++){$candidate=$diagram.DiagramLinks.GetAt($j);if($candidate.ConnectorID -eq $co.ConnectorID){$dl=$candidate;break}}
            if($null -eq $dl){$dl=$diagram.DiagramLinks.AddNew('','');$dl.ConnectorID=$co.ConnectorID}
            $dl.IsHidden=$false;$dl.LineStyle=2
            if($co.ClientID -ne $co.SupplierID){
                $parallel=@(@($v.relaciones)+@($v.dependencias) | Where-Object { $cc=$connectors[$_]; ($cc.ClientID -eq $co.ClientID -and $cc.SupplierID -eq $co.SupplierID) -or ($cc.ClientID -eq $co.SupplierID -and $cc.SupplierID -eq $co.ClientID) })
                if($parallel.Count -gt 1){
                    $idx=[Array]::IndexOf([object[]]$parallel,$key)
                    $na=$r.GetElementByID($co.ClientID).Name;$nb=$r.GetElementByID($co.SupplierID).Name
                    $aa=$v.posiciones.PSObject.Properties[$na].Value;$bb=$v.posiciones.PSObject.Properties[$nb].Value
                    $acx=[int]($aa.x+$aa.w/2);$acy=[int]($aa.y+$aa.h/2);$bcx=[int]($bb.x+$bb.w/2);$bcy=[int]($bb.y+$bb.h/2)
                    $dl.LineStyle=3
                    if([Math]::Abs($acx-$bcx) -lt [Math]::Abs($acy-$bcy)){
                        $lane=if($idx%2 -eq 0){[Math]::Min($aa.x,$bb.x)-90}else{[Math]::Max(($aa.x+$aa.w),($bb.x+$bb.w))+90}
                        $dl.Path="$($lane):$(-$acy);$($lane):$(-$bcy);"
                    }else{
                        $lane=if($idx%2 -eq 0){[Math]::Min($aa.y,$bb.y)-90}else{[Math]::Max(($aa.y+$aa.h),($bb.y+$bb.h))+90}
                        $dl.Path="$($acx):$(-$lane);$($bcx):$(-$lane);"
                    }
                }
            }
            if($v.principal -and $key -eq 'REL-059'){$pa=$v.posiciones.Socio;$pb=$v.posiciones.Canje;$xx1=[int]($pa.x+$pa.w/2);$xx2=[int]($pb.x+$pb.w/2);$yy=[int]$pb.y-90;$dl.LineStyle=3;$dl.Path="$($xx1):$(-$yy);$($xx2):$(-$yy);"}
            if($key -eq 'REL-026'){$pm=$v.posiciones.MovimientoPuntos;$rx=[int]($pm.x+$pm.w+90);$ty=[int]($pm.y+45);$by=[int]($pm.y+$pm.h-35);$dl.LineStyle=3;$dl.Path="$($rx):$(-$ty);$($rx):$(-$by);"}
            Save $dl
        }
        Save $diagram;$r.ReloadDiagram($diagram.DiagramID)
        $file=Join-Path $export ($v.id+'.png')
        $guid=$project.GUIDtoXML($diagram.DiagramGUID)
        $ok=$project.PutDiagramImageToFile($guid,$file,1)
        if(-not $ok -or -not (Test-Path -LiteralPath $file)){throw ('No se exportó '+$v.nombre)}
        $man+=,[ordered]@{id=$v.id;nombre=$v.nombre;diagramId=$diagram.DiagramID;guid=$diagram.DiagramGUID;packageId=$diagram.PackageID;archivo=$file;clases=$v.clases;exportado=$ok}
        Log 'Diagram' $diagram.DiagramID $diagram.DiagramGUID $v.nombre $act
        Write-Output ('Exportado '+$v.id+' '+$v.nombre)
        $man | ConvertTo-Json -Depth 6 | Set-Content -Encoding UTF8 (Join-Path $out 'diagramas-ea.json')
    }
    $r.RefreshModelView($lp.PackageID)
    $main=@($man | Where-Object id -EQ 'V-00')[0]
    $r.OpenDiagram($main.diagramId)
}
if($Fase -eq 'Inventario'){
    foreach($tabla in @('t_package','t_object','t_diagram','t_connector','t_attribute','t_operation','t_operationparams','t_objectconstraint','t_objectscenarios','t_objectproperties','t_diagramobjects','t_diagramlinks')){
        [IO.File]::WriteAllText((Join-Path $out "despues-$tabla.xml"),$r.SQLQuery("SELECT * FROM $tabla"),[Text.UTF8Encoding]::new($false))
    }
    $native=@()
    foreach($k in $elements.Keys){$e=$elements[$k];$native+=,[ordered]@{clave=$k;nombre=$e.Name;id=$e.ElementID;guid=$e.ElementGUID;tipo=$e.Type;packageId=$e.PackageID;atributos=$e.Attributes.Count;operaciones=$e.Methods.Count}}
    $native | ConvertTo-Json -Depth 5 | Set-Content -Encoding UTF8 (Join-Path $out 'elementos-ea.json')
    $links=@();foreach($k in $connectors.Keys){$co=$connectors[$k];$links+=,[ordered]@{clave=$k;id=$co.ConnectorID;guid=$co.ConnectorGUID;cliente=$co.ClientID;proveedor=$co.SupplierID;tipo=$co.Type;estereotipo=$co.Stereotype;multA=$co.ClientEnd.Cardinality;multB=$co.SupplierEnd.Cardinality}}
    $links | ConvertTo-Json -Depth 5 | Set-Content -Encoding UTF8 (Join-Path $out 'conectores-ea.json')
    Write-Output ('Inventario nativo: '+$native.Count+' elementos; '+$links.Count+' conexiones')
}
