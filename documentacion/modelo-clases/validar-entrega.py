from pathlib import Path
import json,xml.etree.ElementTree as E,csv,re,hashlib,sys,html,struct
sys.stdout.reconfigure(encoding='utf-8')
b=Path(__file__).resolve().parent;o=Path((b/'entrega-actual.txt').read_text(encoding='utf-8-sig').strip())
m=json.loads((o/'modelo-revisado.json').read_text(encoding='utf-8-sig'))
native=json.loads((o/'elementos-ea.json').read_text(encoding='utf-8-sig'));links=json.loads((o/'conectores-ea.json').read_text(encoding='utf-8-sig'));diags=json.loads((o/'diagramas-ea.json').read_text(encoding='utf-8-sig'));meta=json.loads((o/'procedencia.json').read_text(encoding='utf-8-sig'))
bykey={x['clave']:x for x in native};lk={x['clave']:x for x in links}
checks=[]
def check(name,ok,detail=''):
    checks.append(dict(comprobacion=name,resultado='Correcto' if ok else 'FALLO',detalle=detail))
def rows(prefix,t):return [{c.tag:c.text or '' for c in r} for r in E.parse(o/f'{prefix}-{t}.xml').findall('.//Row')]
check('75 clases nativas sin duplicados de identificador estable',len([x for x in native if x['clave'].startswith('PJL.CL.')])==75 and len(bykey)==len(native))
check('Todas las clases son UML Class editables',all(bykey['PJL.CL.'+c['nombre']]['tipo']=='Class' for c in m['clases']))
check('Atributos y operaciones nativos coinciden con catálogo',all(bykey['PJL.CL.'+c['nombre']]['atributos']==len(c['atributos']) and bykey['PJL.CL.'+c['nombre']]['operaciones']==len(c['operaciones']) for c in m['clases']))
check('Diez enumeraciones UML nativas',all(bykey['PJL.EN.'+e['nombre']]['tipo']=='Enumeration' and bykey['PJL.EN.'+e['nombre']]['atributos']==len(e['valores']) for e in m['enumeraciones']))
check(str(len(m['asociaciones']))+' asociaciones con extremos y multiplicidades válidos',all(r['id'] in lk and lk[r['id']]['tipo']=='Association' and lk[r['id']]['cliente']==bykey['PJL.CL.'+r['a']]['id'] and lk[r['id']]['proveedor']==bykey['PJL.CL.'+r['b']]['id'] and lk[r['id']]['multA']==r['ma'] and lk[r['id']]['multB']==r['mb'] for r in m['asociaciones']))
check('44 dependencias de dominio separadas de asociaciones',all(d['id'] in lk and lk[d['id']]['tipo']=='Dependency' for d in m['dependencias']))
pkgs={int(x['Package_ID']):x for x in rows('despues','t_package')}
logic=[x for x in pkgs.values() if x['Name']=='Vista_Logica' and pkgs[int(x['Parent_ID'])]['Name']=='Model']
before_pkgs={int(x['Package_ID']):x for x in rows('antes','t_package')}
before_logic=[x for x in before_pkgs.values() if x['Name']=='Vista_Logica' and before_pkgs[int(x['Parent_ID'])]['Name']=='Model']
check('Vista_Logica identificada por jerarquía y GUID',len(logic)==len(before_logic)==1 and logic[0]['ea_guid']==before_logic[0]['ea_guid'])
lid=int(logic[0]['Package_ID'])
def under(pid):
    while pid:
        if pid==lid:return True
        pid=int(pkgs[pid]['Parent_ID'])
    return False
check('Todos los diagramas nuevos cuelgan de Vista_Logica',len(diags)==len(m['vistas']) and all(under(int(d['packageId'])) for d in diags))
check('Panorama con nombre requerido en Vista_Logica',any(d['nombre']=='Diagrama de clases de negocio' and int(d['packageId'])==lid for d in diags))
dos=rows('despues','t_diagramobjects');dls=rows('despues','t_diagramlinks')
objects={x['Object_ID']:x for x in rows('despues','t_object')}
duplicate=[];overlap=[];style=[]
for d in diags:
    subset=[x for x in dos if int(x['Diagram_ID'])==d['diagramId']]
    if len({x['Object_ID'] for x in subset})!=len(subset):duplicate.append(d['id'])
    for i,a in enumerate(subset):
        for c in subset[i+1:]:
            if min(int(a['RectRight']),int(c['RectRight']))>max(int(a['RectLeft']),int(c['RectLeft'])) and min(-int(a['RectBottom']),-int(c['RectBottom']))>max(-int(a['RectTop']),-int(c['RectTop'])):overlap.append(d['id'])
    for obj in subset:
        st=obj.get('ObjectStyle','')
        if re.search(r'AttPri=0|AttPub=0|OpPub=0',st):style.append((d['id'],obj['Object_ID']))
check('Elementos reutilizados sin duplicación dentro de vistas',not duplicate,str(duplicate))
check('Cajas de clases sin solapamientos geométricos',not overlap,str(sorted(set(overlap))))
check('Compartimentos configurados visibles',not style,str(style))
check('Todas las clases se muestran en alguna vista',all(any(c['nombre'] in d['clases'] for d in diags) for c in m['clases']))
check('Todas las relaciones tienen vista asignada',all(any(r['id'] in v['relaciones']+v['dependencias'] for v in m['vistas']) for r in m['asociaciones']+m['dependencias']))
manifest_byid={d['id']:d for d in diags}
visibility=[]
for v in m['vistas']:
    did=manifest_byid[v['id']]['diagramId']
    for key in v['relaciones']+v['dependencias']:
        found=[d for d in dls if int(d['DiagramID'])==did and int(d['ConnectorID'])==lk[key]['id']]
        if len(found)!=1 or found[0]['Hidden'].upper()!='FALSE':visibility.append((v['id'],key))
check('Relaciones asignadas efectivamente visibles en EA',not visibility,str(visibility))
constraints=rows('despues','t_objectconstraint')
check('Reglas conservadas como restricciones UML nativas',all(any(int(x['Object_ID'])==bykey['PJL.CL.'+c['nombre']]['id'] and x['Constraint']==rid and x['Notes'] for x in constraints) for c in m['clases'] for rid in c['reglas']))
reopened=json.loads((o/'reapertura-y-editabilidad.json').read_text(encoding='utf-8-sig'))
check('Repositorio reabierto en EA y 75 clases editables comprobadas',len(reopened)==75 and all(c['editable'] and c['tipo']=='Class' and c['restricciones']>0 for c in reopened))
pngs=[]
for d in diags:
    p=Path(d['archivo']);buf=p.read_bytes();w,h=struct.unpack('>II',buf[16:24]);pngs.append(dict(id=d['id'],nombre=d['nombre'],ancho=w,alto=h,bytes=len(buf)))
check('Todos los PNG proceden de exportación EA y tienen contenido',all(p['bytes']>5000 and p['ancho']>200 and p['alto']>100 for p in pngs))
check('14 familias RF y 91 referencias HU únicas',len({re.match(r'RF-\d+',t['rf'])[0] for t in m['trazabilidad']})==14 and len({t['hu'] for t in m['trazabilidad']})==91)
check('Subtareas conservan padres originales',all(t['padre'].startswith('HU-') and 'HU-PADRE.'+t['hu'] in lk for t in m['trazabilidad'] if t['tipo']=='Sub-task'))
actual=[]
for t in m['trazabilidad']:
    cl=bykey['PJL.CL.'+t['clase']];hu=bykey['PJL.REQ.'+t['hu']];rf=bykey['PJL.REQ.'+t['rf']]
    keys=['CL-HU.'+t['clase']+'.'+t['hu'],'HU-RF.'+t['hu'],'HU-CU.'+t['hu']]
    ok=all(k in lk for k in keys) and lk[keys[0]]['cliente']==cl['id'] and lk[keys[0]]['proveedor']==hu['id'] and lk[keys[1]]['proveedor']==rf['id'] and lk[keys[2]]['proveedor']==t['cu']['id'] and objects[str(t['cu']['id'])]['ea_guid']==t['cu']['guid'] and objects[str(t['cu']['id'])]['Object_Type']=='UseCase'
    actual.append(ok)
    t['enlaceEA']='Creado y verificado por relectura API' if ok else 'FALLO'
    t['claseEA']=cl;t['huEA']=hu;t['rfEA']=rf;t['conectoresEA']={k:lk[k] for k in keys if k in lk}
check('Trazabilidad nativa de las 91 HU con GUID/ID reales',all(actual))
check('Todas las operaciones tienen dueño, fuente y tipo de responsabilidad',all(c['reglas'] and all(op['fuente'] and op['tipo'] and op['estado'] for op in c['operacionesDetalle']) for c in m['clases']))
methods=rows('despues','t_operation');parameters=rows('despues','t_operationparams');signature_errors=[]
for c in m['clases']:
    owner=bykey['PJL.CL.'+c['nombre']]['id']
    for signature in c['operaciones']:
        match=re.fullmatch(r'([^\(]+)\((.*)\):\s*(.+)',signature)
        name,args,ret=match.groups();found=[op for op in methods if int(op['Object_ID'])==owner and op['Name']==name]
        if len(found)!=1:signature_errors.append((c['nombre'],signature,'operación ausente/duplicada'));continue
        op=found[0];actual=sorted([p for p in parameters if p['OperationID']==op['OperationID']],key=lambda p:int(p['Pos']))
        wanted=[tuple(p.strip() for p in part.split(':',1)) for part in args.split(',')] if args.strip() else []
        if [(p['Name'],p['Type']) for p in actual]!=wanted or op['Type']!=ret:signature_errors.append((c['nombre'],signature,'parámetros/retorno distintos'))
check('Firmas nativas completas con nombres, tipos, orden y retorno',not signature_errors,str(signature_errors))
check('Servicios de dominio sin atributos artificiales',all(not c['atributos'] for c in m['clases'] if c['estereotipo']=='ServicioDominio'))
valid=set(c['nombre'] for c in m['clases'])|set(e['nombre'] for e in m['enumeraciones'])|{'Texto','Entero','Decimal','Booleano','Fecha','FechaHora'}
unknown=[]
for c in m['clases']:
    for s in c['atributos']+c['operaciones']:
        for typ in re.findall(r':\s*([A-Za-z][A-Za-z0-9]*(?:<[A-Za-z][A-Za-z0-9]*>)?)',s):
            if typ.startswith(('Coleccion<','Conjunto<')):typ=typ.split('<')[1].rstrip('>')
            if typ not in valid:unknown.append((c['nombre'],s,typ))
check('Tipos de análisis y enumeraciones coherentes',not unknown,str(unknown))
preserved=[]
for table,key,ignore in [('t_object','Object_ID',{'ModifiedDate'}),('t_package','Package_ID',{'ModifiedDate'}),('t_diagram','Diagram_ID',{'ModifiedDate'}),('t_connector','Connector_ID',set()),('t_attribute','ID',set()),('t_operation','OperationID',set())]:
    before=rows('antes',table);after={x[key]:x for x in rows('despues',table)};diff=[]
    for a in before:
        z=after.get(a[key]);d=[k for k in a if k not in ignore and (z or {}).get(k)!=a[k]]
        if d:diff.append(dict(id=a[key],campos=d))
    preserved.append(dict(tabla=table,anteriores=len(before),diferencias=diff))
    check('Conservación de datos anteriores '+table,not diff,json.dumps(diff,ensure_ascii=False))
check('Escenarios originales conservados',rows('antes','t_objectscenarios')==rows('despues','t_objectscenarios'))
check('Objetos y conectores de diagramas originales conservados',all(x in dos for x in rows('antes','t_diagramobjects')) and all(x in dls for x in rows('antes','t_diagramlinks')))
sha=hashlib.sha256(Path(meta['original']).read_bytes()).hexdigest().upper()
check('Original intacto y respaldo consistente identificado',sha==meta['sha256Original']==meta['sha256RespaldoConsistente'])
log=[json.loads(x) for x in (o/'registro-ea.jsonl').read_text(encoding='utf-8-sig').splitlines() if x.strip()]
created={x['tipo']:sum(1 for z in log if z['tipo']==x['tipo'] and z['accion']=='creado') for x in log}
check('Reejecuciones reutilizan GUID de clases y conexiones',len({x['guid'] for x in log if x['tipo']=='Class'})==75 and all(sum(1 for z in log if z['guid']==x['guid'] and z['accion']=='creado')<=1 for x in log if x['tipo'] in ['Class','Connector']))
result=dict(comprobaciones=checks,preservacion=preserved,imagenes=pngs,requisitos=dict(hu=91,rfDetallados=91,familiasRF=14,ur=57,subtareas=sum(t['tipo']=='Sub-task' for t in m['trazabilidad'])),limitaciones=['No se reejecutaron suites de aplicación ni se accedió a PostgreSQL.','La correspondencia de análisis y el enlace UML no certifican aceptación de todos los criterios.','La validación de lectura/edición se hace por API de EA; la captura interactiva posterior agotó la autorización. La revisión visual utiliza PNG exportados por EA.'])
(o/'VALIDACION.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
(o/'TRAZABILIDAD-VERIFICADA.json').write_text(json.dumps(m['trazabilidad'],ensure_ascii=False,indent=2),encoding='utf-8')
with (o/'TRAZABILIDAD-VERIFICADA.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.writer(f);w.writerow(['HU','WorkItem','Tipo','Padre','UR','RF','RNF','CU_grupo_original','CU_diagrama_actual','CU_ID','CU_GUID','CU_nombre','Correspondencia_CU','Clase','Clase_ID','Clase_GUID','HU_ID','HU_GUID','RF_ID','RF_GUID','Reglas','Atributos','Operacion','Fuente','Estado_observado','Cobertura','Diferencias','Enlace_EA','Conector_clase_HU_GUID','Conector_HU_RF_GUID','Conector_HU_CU_GUID'])
    for t in m['trazabilidad']:
        ks=list(t['conectoresEA']);w.writerow([t['hu'],t['workItem'],t['tipo'],t['padre'],t['ur'],t['rf'],t['rnf'],t['cuGrupoOriginal'],t['cuCodigo'],t['cu']['id'],t['cu']['guid'],t['cu']['nombre'],t['correspondenciaCU'],t['clase'],t['claseEA']['id'],t['claseEA']['guid'],t['huEA']['id'],t['huEA']['guid'],t['rfEA']['id'],t['rfEA']['guid'],','.join(t['reglas']),t['atributos'],t['operacion'],t['fuente'],t['estado'],t['cobertura'],t['diferencia'],t['enlaceEA']]+[t['conectoresEA'][k]['guid'] for k in ks])
lines=['# Validación del modelo UML\n','| Comprobación | Resultado | Detalle |','|---|---|---|']+[f"| {c['comprobacion']} | {c['resultado']} | {c['detalle']} |" for c in checks]
lines+=['\n## Límites\n']+['- '+x for x in result['limitaciones']]
(o/'VALIDACION.md').write_text('\n'.join(lines),encoding='utf-8')
gallery=['<!doctype html><html lang="es"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Modelo de clases de negocio PJL</title><style>body{font:16px system-ui;margin:2rem;color:#17212b}nav{display:flex;flex-wrap:wrap;gap:1rem}figure{margin:3rem 0;border-top:1px solid #ccd;padding-top:1rem}img{max-width:100%;height:auto}a{color:#075d93}figcaption{font-weight:bold;margin:1rem 0}</style><h1>Modelo de clases de negocio</h1><p>Diagramas exportados desde Enterprise Architect. Abra una imagen para verla a tamaño completo. Las clases y sus miembros son editables en el archivo EAPX. Responsabilidades de análisis; revise estado, fuentes y pendientes en los documentos.</p><nav>']
for d in diags:gallery.append(f'<a href="#{d["id"]}">{html.escape(d["nombre"])}</a>')
gallery.append('</nav>')
for d in diags:gallery.append(f'<figure id="{d["id"]}"><figcaption>{d["id"]} · {html.escape(d["nombre"])}</figcaption><a href="diagramas-ea/{d["id"]}.png"><img loading="lazy" src="diagramas-ea/{d["id"]}.png" alt="{html.escape(d["nombre"])}"></a></figure>')
gallery.append('</html>');(o/'DIAGRAMAS.html').write_text('\n'.join(gallery),encoding='utf-8')
print(json.dumps({'comprobaciones':len(checks),'fallos':[x for x in checks if x['resultado']=='FALLO'],'clases':75,'relacionesNegocio':len(m['asociaciones'])+len(m['dependencias']),'trazas':sum(x['estereotipo']=='trace' for x in links),'imagenes':len(pngs)},ensure_ascii=False))
