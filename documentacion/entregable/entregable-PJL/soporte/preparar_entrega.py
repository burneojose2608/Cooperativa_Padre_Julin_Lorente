"""Exporta requisitos y reúne la entrega académica sin modificar sus fuentes.
Ejecutar con el Python del runtime de artefactos (reportlab, PIL, pypdf).
Las hojas se leen de OOXML: la plantilla se copia byte por byte, no se reautoriza.
"""
from pathlib import Path
import csv
import hashlib
import json
import re
import shutil
import subprocess
import textwrap
import zipfile
import xml.etree.ElementTree as ET
from collections import Counter
from html import escape
from PIL import Image, ImageDraw, ImageFont
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A3, landscape
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pypdf import PdfReader

OUT = Path(__file__).resolve().parents[1]
ROOT = OUT.parents[1]
SRC = ROOT/'documentacion/modelo-clases/entrega-20261110-021751'
NS = {'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
DATE = '2026-11-10'
BASE_SPRINT = {1,6,8,9,10,12,15}

def load(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def save(p, obj): p.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding='utf-8')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def write_csv(p, records, fields=None):
    assert records, p
    with p.open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields or list(records[0]),extrasaction='ignore')
        w.writeheader(); w.writerows(records)
def ids(text, pattern): return list(dict.fromkeys(re.findall(pattern,text or '')))
def uniq(values): return list(dict.fromkeys(values))
def joined(values): return '; '.join(uniq(values))
def read_table(p):
    return [{c.tag:c.text or '' for c in r} for r in ET.parse(p).findall('.//Row')]

def read_workbook(path):
    with zipfile.ZipFile(path) as z:
        strings=[]
        if 'xl/sharedStrings.xml' in z.namelist():
            strings=[''.join(t.text or '' for t in e.findall('.//s:t',NS)) for e in ET.fromstring(z.read('xl/sharedStrings.xml')).findall('s:si',NS)]
        wb=ET.fromstring(z.read('xl/workbook.xml'))
        rels={r.get('Id'):r.get('Target') for r in ET.fromstring(z.read('xl/_rels/workbook.xml.rels'))}
        sheets={}
        for sheet in wb.findall('s:sheets/s:sheet',NS):
            target=rels[sheet.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id')]
            target=target.lstrip('/') if target.startswith('/') else 'xl/'+target
            rows=[]
            for r in ET.fromstring(z.read(target)).findall('.//s:sheetData/s:row',NS):
                values={}
                for c in r.findall('s:c',NS):
                    raw=c.find('s:v',NS)
                    value=raw.text or '' if raw is not None else ''.join(t.text or '' for t in c.findall('.//s:t',NS))
                    if c.get('t')=='s': value=strings[int(value)]
                    if value: values[re.sub(r'\d','',c.get('r'))]=value.strip()
                if values: rows.append((int(r.get('r')),values))
            sheets[sheet.get('name')]=rows
        broken=[n.get('name') for n in wb.findall('s:definedNames/s:definedName',NS) if '#REF!' in (n.text or '')]
    return sheets, broken

def descripcion_vigente(rid, original):
    # Se conserva en columna independiente el enunciado histórico de la plantilla.
    changes={
      'UR-01': 'Se requiere registrar cuentas sin duplicados y con consentimiento. Una cédula activa en el padrón habilita la condición de socio; una ausente permite una cuenta general sin funciones de socio; una inactiva impide el registro. La cédula debe contener exactamente diez dígitos ASCII, sin calcular verificador.',
      'RF-01-1': 'El sistema deberá registrar cuentas con cédula, nombres, apellidos, fecha de nacimiento, celular, correo, usuario y contraseña, validando obligatorios, cédula como texto de diez dígitos ASCII, unicidad y consentimiento. Con padrón activo crea socio; con cédula ausente crea cuenta general; con padrón inactivo rechaza; si el padrón falla no crea una cuenta.',
      'RF-01-6': 'El sistema deberá consultar el padrón de prueba antes de habilitar la condición de socio. Activo permite habilitarla, ausente permite crear cuenta general sin privilegios de socio, inactivo impide el registro e indisponibilidad del padrón impide completar el alta.',
    }
    return changes.get(rid,original)

def reunir_datos():
    for name in ['plantilla-original','backlog-jira','sprint-1','trazabilidad','fuente-enterprise','soporte/qa']:
        (OUT/name).mkdir(parents=True,exist_ok=True)
    template=ROOT/'documentacion/Presentacion .(1) (1).xlsx'
    shutil.copy2(template,OUT/'plantilla-original'/template.name)
    assert sha(template)==sha(OUT/'plantilla-original'/template.name)
    sheets,broken=read_workbook(template)
    traces=load(SRC/'TRAZABILIDAD-VERIFICADA.json')
    model=load(SRC/'modelo-revisado.json')
    ea=load(OUT/'soporte/inventario-entrega-ea.json')
    hu_by_rf={t['rf']:t for t in traces}
    rf_det=set(hu_by_rf)
    ur_records=[]; rf_records=[]; rnf_records=[]

    for row,v in sheets['UserReq.']:
        rid=v.get('A','')
        if not re.fullmatch(r'UR-\d{2}',rid): continue
        ts=[t for t in traces if rid in ids(t['ur'],r'UR-\d{2}')]
        original=v.get('C','')
        ur_records.append(dict(id_requisito=rid,nombre=v.get('B',''),descripcion=descripcion_vigente(rid,original),
            actores=v.get('D',''),rf_asociados=joined(t['rf'] for t in ts),hu_asociadas=joined(t['hu'] for t in ts),
            fuente=f'{template.name} | UserReq. | fila {row}',descripcion_original=original,
            decision_aplicable='DEC-REGISTRO-GENERAL; DEC-CEDULA-10-DIGITOS' if rid=='UR-01' else '',
            cobertura='Trazada al diseño; aceptación no certificada'))

    for row,v in sheets['Req. Funcionales']:
        rid=v.get('A','')
        if not re.fullmatch(r'RF-\d{2}(?:-\d+)?',rid): continue
        familia=re.match(r'RF-\d{2}',rid)[0]
        detailed=rid.count('-')==2
        ts=[hu_by_rf[rid]] if detailed and rid in hu_by_rf else [t for t in traces if t['rf'].startswith(rid+'-')]
        original=v.get('D','')
        rf_records.append(dict(id_requisito=rid,nivel='Detalle' if detailed else 'Familia',id_padre=familia if detailed else '',
            nombre=v.get('B',''),descripcion=descripcion_vigente(rid,original),funcionalidad=v.get('C',''),
            prioridad_moscow=v.get('F',''),dependencias_originales=v.get('G',''),
            ur_asociados=joined(t['ur'] for t in ts),hu_asociadas=joined(t['hu'] for t in ts),
            cu_asociados=joined(t['cuCodigo'] for t in ts),
            clases_asociadas=joined(t['clase'] for t in ts),
            estado_implementacion=ts[0]['estado'] if detailed and ts else 'Cobertura agregada; consultar requisitos detallados',
            fuente=f'{template.name} | Req. Funcionales | fila {row}',descripcion_original=original,
            decision_aplicable='DEC-REGISTRO-GENERAL; DEC-CEDULA-10-DIGITOS' if rid in {'RF-01-1','RF-01-6'} else ''))

    titulos=['Protección de contraseñas','Consentimiento de datos','Compatibilidad y adaptación de interfaz','Tiempo de respuesta','Concurrencia y errores',
      'Auditoría inmutable','Validación y accesibilidad','Disponibilidad','HTTPS y HSTS','Autorización y titularidad','Inactividad de sesión',
      'Atomicidad e idempotencia de puntos','Historial de estados','Enmascaramiento y privacidad','Copias de seguridad y restauración',
      'Verificación de certificados','Mensajes de operación','Notificaciones asíncronas','Arquitectura y cobertura de pruebas',
      'Validación y prevención de inyección','Bloqueo y límite de solicitudes','Sorteos verificables','Datos del MVP','Exclusión de datos clínicos',
      'Retención de prospectos','Validación de archivos']
    for row,v in sheets['Req. No Funcionales']:
        rid=v.get('A','')
        if not re.fullmatch(r'RNF-\d{2}',rid): continue
        raw=v.get('D','')
        range_match=re.fullmatch(r'RF-(\d{2})\s+a\s+RF-(\d{2})',raw)
        rfs=[f'RF-{i:02}' for i in range(int(range_match[1]),int(range_match[2])+1)] if range_match else ids(raw,r'RF-\d{2}(?:-\d+)?')
        ts=[t for t in traces if rid in ids(t['rnf'],r'RNF-\d{2}')]
        status='Planificado; no certificado para todo el alcance'
        evidence='Requisito de calidad; su traza documental no acredita medición o cumplimiento.'
        if rid in {'RNF-01','RNF-02','RNF-06','RNF-09','RNF-10','RNF-11','RNF-20','RNF-21'}:
            status='Verificado parcialmente en el alcance de identidad y seguridad del Sprint 1'
            evidence='sprint-1/verificacion-actual.md; matriz de criterios del Sprint 1. No extrapolar a módulos futuros.'
        if rid in {'RNF-03','RNF-07'}:
            evidence='Hay pruebas DOM y validaciones; sin acreditación completa de geometría, todos los navegadores ni WCAG AA.'
        if rid in {'RNF-04','RNF-05','RNF-08'}:
            evidence='No hay medición de carga/disponibilidad suficiente; no se inventa un resultado.'
        if rid=='RNF-15':
            evidence='Sin evidencia de tarea automática cada 24 h, retención de siete días y restauración probada. Una copia del modelo EA no satisface este requisito de operación.'
        rnf_records.append(dict(id_requisito=rid,nombre=titulos[int(rid[-2:])-1],descripcion=v.get('B',''),
            prioridad_moscow=v.get('C',''),rf_asociados_originales=raw,rf_asociados=joined(rfs),
            hu_asociadas_explicitas=joined(t['hu'] for t in ts),estado_verificacion=status,evidencia_o_brecha=evidence,
            fuente=f'{template.name} | Req. No Funcionales | fila {row}'))

    write_csv(OUT/'requisitos_usuario.csv',ur_records)
    write_csv(OUT/'requisitos_funcionales.csv',rf_records)
    write_csv(OUT/'requisitos_no_funcionales.csv',rnf_records)
    save(OUT/'soporte/requisitos-extraidos.json',dict(ur=ur_records,rf=rf_records,rnf=rnf_records,definiciones_excel_rotas=broken))

    # Matriz normalizada RNF-RF y alcance explícito: no adjudica pruebas inexistentes.
    rnf_links=[dict(rnf=r['id_requisito'],rf=rf,origen=r['fuente'],tipo_vinculo='Asociación de calidad declarada por la plantilla',
                    estado=r['estado_verificacion']) for r in rnf_records for rf in r['rf_asociados'].split('; ') if rf]
    write_csv(OUT/'trazabilidad/RNF-RF.csv',rnf_links)
    for name in ['TRAZABILIDAD-VERIFICADA.csv','TRAZABILIDAD-VERIFICADA.json','RELACIONES-VERIFICADAS.csv']:
        shutil.copy2(SRC/name,OUT/'trazabilidad'/name)
    for name in ['CATALOGO-REVISADO.md','REGLAS-Y-PENDIENTES.md','RELACIONES.md','ANALISIS-ALCANCE.md']:
        shutil.copy2(SRC/name,OUT/'trazabilidad'/name)

    # Verificación independiente sobre la copia extraída del EA vigente.
    objects={int(x['Object_ID']):x for x in read_table(OUT/'soporte/ea-t_object.xml')}
    connectors={x['ea_guid'].upper():x for x in read_table(OUT/'soporte/ea-t_connector.xml')}
    ops=read_table(OUT/'soporte/ea-t_operation.xml')
    valid_links=[]
    for t in traces:
        for field in ['claseEA','huEA','rfEA']:
            e=t[field]; assert objects[e['id']]['ea_guid'].upper()==e['guid'].upper(),(t['hu'],field)
        assert objects[t['cu']['id']]['ea_guid'].upper()==t['cu']['guid'].upper(),t['hu']
        assert objects[t['cu']['id']]['Object_Type']=='UseCase'
        assert any(int(o['Object_ID'])==t['claseEA']['id'] and o['Name']==t['operacion'].split('(')[0] for o in ops),t['hu']
        for key,c in t['conectoresEA'].items():
            # Los IDs y GUID de cada arco se comprueban, además de existir sus extremos.
            guid=c.get('guid') or c.get('ea_guid')
            live=connectors[guid.upper()]
            assert int(live['Start_Object_ID'])==int(c['cliente'])
            assert int(live['End_Object_ID'])==int(c['proveedor'])
        valid_links.append(t['hu'])

    original=ROOT/'documentacion/product_con_subtareas.csv'
    shutil.copy2(original,OUT/'backlog-jira'/original.name)
    with original.open(encoding='utf-8-sig',newline='') as f: backlog=list(csv.DictReader(f))
    sprint=[r for r in backlog if r.get('Sprint planificado')=='Sprint 1']
    write_csv(OUT/'backlog-jira/sprint_1_planificado.csv',sprint)
    reconc=[]
    for r in sprint:
        match=re.match(r'HU-(\d+)',r['Summary'])
        reconc.append(dict(work_item_id=r['Work item ID'],elemento=r['Summary'],tipo=r['Work Type'],estado_original_csv=r['Status'],
            estado_evidencia_local='Implementado en alcance vigente; pruebas aprobadas' if match and int(match[1]) in BASE_SPRINT else 'Consultar evidencia de tareas transversales',
            estado_jira='Presentación directa del usuario al profesor; fuera del alcance del paquete',evidencia='sprint-1/verificacion-actual.md; sprint-1/documentacion-equipo/matriz-trazabilidad.md'))
    write_csv(OUT/'backlog-jira/conciliacion_sprint_1.csv',reconc)

    for folder,dest in [('documentacion/sprint-1-equipo','sprint-1/documentacion-equipo'),('documentacion/sprint-1-valeria','sprint-1/documentacion-registro')]:
        shutil.copytree(ROOT/folder,OUT/dest,dirs_exist_ok=True)
    for src,dest in [('docs/plan-sprint-1-equipo.md','sprint-1/plan-sprint-1-equipo.md'),('README.md','sprint-1/README-proyecto.md')]:
        shutil.copy2(ROOT/src,OUT/dest)
    # Los enlaces relativos históricos se conservan como contexto; guía principal usa rutas del paquete.
    source_paths=subprocess.check_output(['git','ls-files','-z','--','backend','frontend','.github','README.md','.gitignore','docs'],cwd=ROOT).decode().split('\0')
    excluded=[]; included=[]
    with zipfile.ZipFile(OUT/'sprint-1/codigo_fuente_sprint_1.zip','w',zipfile.ZIP_DEFLATED) as z:
        for rel in source_paths:
            if not rel: continue
            p=ROOT/rel
            if (not p.is_file() or any(part in {'node_modules','venv','.venv','__pycache__','dist','.git','certs','tls'} for part in p.parts)
                or p.name.startswith('.env') or p.suffix.lower() in {'.pem','.key','.pfx','.p12','.pyc','.db','.sqlite3'}):
                excluded.append(rel); continue
            z.write(p,arcname=rel); included.append(dict(ruta=rel,sha256=sha(p)))
    save(OUT/'sprint-1/manifiesto-codigo.json',dict(archivos=included,excluidos=excluded,nota='Fuente versionada del estado local actual; sin entornos, dependencias instaladas, .env, claves privadas ni datos de base. No incluye el historial Git.'))
    save(OUT/'sprint-1/resultados-pruebas.json',dict(fecha=DATE,backend=dict(comando='backend/venv/Scripts/python.exe manage.py test --noinput',exit_code=0,pruebas=135,segundos=30.953,base='Aislada test_*; creada y destruida por runner'),frontend=dict(comando='npm test',exit_code=0,pruebas=20,archivos=5,segundos=4.45),lint=dict(comando='npm run lint',exit_code=0,advertencias=14),build=dict(comando='npm run build',exit_code=0,modulos=58),nota='Resultados ejecutados en esta revisión. Mensajes OperationalError/RuntimeError/IntegrityError pertenecen a pruebas que inyectan fallos y terminaron OK. No se ejecutó carga, SMTP ni evaluación completa WCAG.'))
    (OUT/'sprint-1/verificacion-actual.md').write_text('''# Verificación actual del Sprint 1

Ejecutada el 10 de noviembre de 2026 sobre el código entregado. La suite backend creó y destruyó su base aislada `test_*`; no se ejecutaron migraciones manuales sobre la base de trabajo.

| Comando | Resultado |
| --- | --- |
| backend/venv/Scripts/python.exe manage.py test --noinput | 135 pruebas aprobadas en 30.953 s; comprobación Django sin incidencias |
| npm test | 20 pruebas aprobadas, cinco archivos, 4.45 s |
| npm run lint | Salida 0; 14 advertencias preexistentes de Fast Refresh |
| npm run build | Correcto; 58 módulos; 744 ms |

Los logs de fallos inyectados en tests no equivalen a tests fallidos. La evidencia previa de HTTPS se incluye en documentacion-equipo/verificacion.md; no se presenta como una prueba TLS reejecutada ahora. No se certifica cobertura completa de RNF por pasar estas suites.

El CSV de planificación mantiene sus estados originales. No se cambiaron tareas en Jira ni se declara terminado un sprint remoto sin verificarlo. Registro y acceso cubren el alcance vigente; las diferencias respecto a la plantilla histórica se explican en CAMBIOS-DE-LINEA-BASE.md.
''',encoding='utf-8')

    # Controles de integridad y ausencia de referencias huérfanas.
    ur_ids={r['id_requisito'] for r in ur_records};rf_ids={r['id_requisito'] for r in rf_records};rnf_ids={r['id_requisito'] for r in rnf_records}
    assert len(ur_records)==len(ur_ids)==57
    assert len(rf_records)==len(rf_ids)==105
    assert len(rnf_records)==len(rnf_ids)==26
    assert {r['id_requisito'] for r in rf_records if r['nivel']=='Detalle'}==rf_det
    assert len(valid_links)==len(set(valid_links))==91
    ur_linked=set();rnf_explicit=set()
    for t in traces:
        u=set(ids(t['ur'],r'UR-\d{2}'));n=set(ids(t['rnf'],r'RNF-\d{2}'))
        assert u<=ur_ids and n<=rnf_ids
        ur_linked |= u;rnf_explicit |= n
        assert t['rf'] in rf_ids
    assert ur_linked==ur_ids
    assert all(r['rf'] in rf_ids for r in rnf_links)
    assert {r['rnf'] for r in rnf_links}==rnf_ids
    counts=Counter(d['tipo'] for d in ea['diagramas'])
    assert counts=={'contexto':1,'casos-uso':26,'clases':31},counts
    assert len(model['clases'])==75
    validation=dict(fecha=DATE,requisitos_usuario=57,requisitos_funcionales_detallados=91,familias_funcionales=14,
        requisitos_funcionales_total=105,requisitos_no_funcionales=26,hu_trazadas=91,ur_con_rf=57,
        rnf_con_asociacion_rf=26,rnf_no_citados_directamente_en_hu=sorted(rnf_ids-rnf_explicit),
        enlaces_hu_cu_rf_clase_verificados=True,operaciones_de_traza_existentes=True,
        plantilla_original_sha256=sha(template),plantilla_copia_identica=True,diagrama_pdf_fuentes=dict(counts),
        definiciones_excel_rotas_preexistentes=broken,
        jira=dict(estado='Presentación directa del usuario al profesor',motivo='Por indicación del usuario, Jira se presenta por separado. No requiere enlace ni comprobación remota dentro del paquete.',pendiente_documental=False),
        nota='Integridad referencial del modelo y documentación; no certifica cumplimiento completo del software ni aceptación formal de requisitos.')
    save(OUT/'trazabilidad/VALIDACION-ENTREGA.json',validation)
    return ea,model,validation

def preparar_pdf(ea,solo=None):
    font=Path('C:/Windows/Fonts/arial.ttf')
    font_bold=Path('C:/Windows/Fonts/arialbd.ttf')
    pdfmetrics.registerFont(TTFont('Entrega',str(font)))
    pdfmetrics.registerFont(TTFont('EntregaBold',str(font_bold)))
    configs=[('contexto','diagrama_contexto.pdf','Diagrama de contexto'),('casos-uso','diagrama_casos_uso.pdf','Diagramas de casos de uso'),('clases','diagrama_clases.pdf','Diagrama de clases de negocio')]
    pdf_info=[x for x in load(OUT/'soporte/pdf-generados.json') if not x['archivo'].startswith('diagrama_'+('casos_uso' if solo=='casos-uso' else solo))] if solo else []
    for tipo,filename,title in configs:
        if solo and tipo!=solo: continue
        ds=[d for d in ea['diagramas'] if d['tipo']==tipo]
        ds.sort(key=lambda d:(0 if d['id'] in {1,6,58} else 1,int(re.search(r'G(\d+)',d['nombre'])[1]) if 'CU-G' in d['nombre'] else d['id']))
        doc=canvas.Canvas(str(OUT/filename),pageCompression=1)
        doc.setTitle(title+' - Cooperativa Padre Julián Lorente');doc.setAuthor('Equipo del proyecto Padre Julián Lorente')
        for index,d in enumerate(ds,1):
            img=Image.open(OUT/d['archivo']).convert('RGB')
            # Tamaño de página adaptado al diagrama para no reducir su letra a un A4 ilegible.
            w=max(842,min(3300,img.width*.75+72));h=max(595,min(3300,img.height*.75+150))
            doc.setPageSize((w,h));doc.bookmarkPage('d'+str(d['id']));doc.addOutlineEntry(d['nombre'],'d'+str(d['id']),0)
            doc.setFillColorRGB(.08,.11,.15);doc.setFont('EntregaBold',15);doc.drawString(36,h-30,title)
            doc.setFont('Entrega',10)
            doc.drawString(36,h-48,d['nombre'])
            doc.setFont('Entrega',8)
            doc.drawString(36,h-63,'Cooperativa Padre Julián Lorente | Exportación del modelo UML nativo | 10 de noviembre de 2026')
            if tipo=='contexto':
                doc.drawString(36,h-77,'MVP: el sistema institucional es una referencia de contexto; se usa un padrón local de prueba, sin conexión productiva.')
            scale=min((w-72)/img.width,(h-125)/img.height)
            iw,ih=img.width*scale,img.height*scale
            doc.drawImage(ImageReader(img),(w-iw)/2,43+(h-125-ih)/2,width=iw,height=ih)
            doc.setFillColorRGB(.3,.3,.3);doc.setFont('Entrega',8)
            doc.drawString(36,23,f"EA Diagram_ID {d['id']} | {d['guid']} | Página {index} de {len(ds)}")
            if tipo=='clases': doc.drawRightString(w-36,23,'Modelo de análisis; el alcance implementado se informa por separado.')
            doc.showPage()
        doc.save()
        check=PdfReader(str(OUT/filename));assert len(check.pages)==len(ds)
        pdf_info.append(dict(archivo=filename,paginas=len(ds),sha256=sha(OUT/filename),diagramas=[d['id'] for d in ds]))
    save(OUT/'soporte/pdf-generados.json',pdf_info)

def contactos():
    # Hojas de contacto para revisar cada exportación, sin incluirlas como entregables finales.
    ea=load(OUT/'soporte/inventario-entrega-ea.json')
    for group in ['contexto','casos-uso','clases']:
        ds=[d for d in ea['diagramas'] if d['tipo']==group]
        for start in range(0,len(ds),6):
            subset=ds[start:start+6];thumb=Image.new('RGB',(1800,1800),'#e6e9ed');draw=ImageDraw.Draw(thumb)
            f=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',18)
            for i,d in enumerate(subset):
                x=(i%2)*900;y=(i//2)*600
                draw.text((x+15,y+12),f"{d['id']} - {d['nombre'][:80]}",font=f,fill='black')
                im=Image.open(OUT/d['archivo']).convert('RGB');im.thumbnail((870,548))
                thumb.paste(im,(x+(900-im.width)//2,y+45+(548-im.height)//2))
            thumb.save(OUT/'soporte/qa'/f'{group}-{start//6+1:02}.jpg',quality=90)

if __name__=='__main__':
    ea,model,validation=reunir_datos()
    preparar_pdf(ea)
    contactos()
    print(json.dumps(dict(clases=len(model['clases']),validacion=validation,pdf=load(OUT/'soporte/pdf-generados.json')),ensure_ascii=False))
