from pathlib import Path
import json,re,hashlib,xml.etree.ElementTree as E,zipfile,sys
sys.stdout.reconfigure(encoding='utf-8')
b=Path(__file__).resolve().parent;root=b.parent.parent;o=Path((b/'entrega-actual.txt').read_text(encoding='utf-8-sig').strip())
backlog=json.loads((o/'fuentes/backlog.json').read_text(encoding='utf-8'));m=json.loads((o/'modelo-revisado.json').read_text(encoding='utf-8-sig'))
hu={re.match(r'HU-\d+',x['Summary'])[0]:x for x in backlog if re.match(r'HU-\d+',x['Summary'])}
source={}
for key,row in hu.items():
    text=re.split(r'\*Consolidación de historias|\*Registro de conversión',row['Description'])[0].strip()
    text=re.sub(r'[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}','[responsable omitido]',text)
    criteria=[x[1:].strip() for x in text.splitlines() if x.startswith('# ')]
    source[key]=dict(textoOriginal=text,criterios=criteria,workItem=row['Work item ID'])
urs={};families={};rfs={};sheets=[]
ns={'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
for p in (root/'documentacion').glob('*.xlsx'):
    with zipfile.ZipFile(p) as z:
        ss=[''.join(t.text or '' for t in x.findall('.//s:t',ns)) for x in E.fromstring(z.read('xl/sharedStrings.xml')).findall('s:si',ns)]
        wb=E.fromstring(z.read('xl/workbook.xml'))
        sheetnames=[x.get('name') for x in wb.findall('s:sheets/s:sheet',ns)]
        for sheetnum,name in enumerate(sheetnames,1):
            tab={}
            for row in E.fromstring(z.read(f'xl/worksheets/sheet{sheetnum}.xml')).findall('.//s:row',ns):
                cells={}
                for c in row.findall('s:c',ns):
                    v=c.find('s:v',ns);value=v.text if v is not None else ''.join(t.text or '' for t in c.findall('.//s:t',ns))
                    if c.get('t')=='s':value=ss[int(value)]
                    cells[re.sub(r'\d','',c.get('r'))]=value or ''
                tab[row.get('r')]=cells
                key=cells.get('A','')
                if re.fullmatch(r'UR-\d+',key):urs[key]=dict(nombre=cells.get('B',''),texto=cells.get('C',''),fuente=f'{p.name}; hoja {name}; fila {row.get("r")}')
                if re.fullmatch(r'RF-\d+-\d+',key):rfs[key]=dict(nombre=cells.get('B',''),texto=cells.get('D',''),fuente=f'{p.name}; hoja {name}; fila {row.get("r")}')
                if re.fullmatch(r'RF-\d+',key):families[key]=dict(nombre=cells.get('B',''),texto=cells.get('D',''),fuente=f'{p.name}; hoja {name}; fila {row.get("r")}')
            sheets.append(dict(nombre=name,filas=len(tab)))
(o/'requisitos-fuentes.json').write_text(json.dumps(dict(hu=source,ur=urs,rf=rfs,familias=families,hojas=sheets),ensure_ascii=False,indent=2),encoding='utf-8')
report=['# Alcance contrastado y evidencia\n',
'El repositorio implementa identidad y seguridad en el alcance vigente del Sprint 1. El modelo cubre el alcance de negocio posterior como análisis, sin presentar tablas o demostraciones como módulos operativos. No se cambió código ni base de datos de la aplicación. No se leyó .env ni se extrajeron credenciales.\n',
'No se encontraron AGENTS.md en el árbol del proyecto ni en los directorios antecesores consultados. Se conservaron los documentos, diagramas y fuentes previos.\n',
'## Precedencia de fuentes\n',
'Las decisiones documentadas posteriores gobiernan los cambios de registro: cuenta general ante ausencia del padrón y cédula de diez dígitos sin verificador. La validación temporal posterior permite conversión administrativa manual. Se preservan los criterios originales del CSV y Excel como antecedentes, sin afirmar cumplimiento del criterio sustituido. La propuesta inicial de modelo-clases fue contrastada y revisada; no constituye aprobación de requisitos.\n',
'Acta: propósito, alcance preliminar del MVP, exclusiones y criterios de éxito. Visión: necesidades de socios, Marketing, Responsabilidad Social, administración y contenidos; documento con restos de plantilla que no se convierten en reglas. PROYECTO 1: especificación general de referidos, gamificación, participación, bienestar y modularidad; menciones futuras no autorizan integraciones productivas o IA concreta.\n',
'El Excel aporta UR, RF, reglas y datos, no evidencia de aceptación ni implementación. Su regla histórica de verificador queda sustituida por la decisión posterior. Hojas inspeccionadas: '+', '.join(s['nombre'] for s in sheets)+'. Se encontraron '+str(len(urs))+' UR, '+str(len(rfs))+' RF detallados y '+str(len(families))+' familias explícitas en celdas.\n',
'## Estado por familia funcional\n',
'| Familia | Estado observado | Evidencia y brecha |','|---|---|---|',
'| RF-01 Usuarios y perfiles | Implementado parcialmente | Alta pública, consulta propia, padrón, unicidad y alta interna por servicio/comando. Edición de contacto/foto, cambio autenticado de clave y administración completa de estados no acreditados por urls.py. Usuario–Socio opcional. |',
'| RF-02 Acceso y permisos | Implementado parcialmente | Login, bloqueo, recuperación, sesiones revocables, inactividad y autorización por roles vigentes. Administración dinámica completa de permisos pendiente. |',
'| RF-03 Referidos | Planificado | SQL 01–02, CSV y pantallas demo. Código de socio real no prueba código referido. Referido convertido en demo no es conversión comercial persistida. |',
'| RF-04 Campañas | Planificado | SQL y backlog. Objetivos/incentivos/segmentos sin servicios operativos; fuente institucional de segmentación pendiente. |',
'| RF-05 Puntos y reconocimientos | Planificado | Libro y triggers SQL no realizan motor de reglas. SocioProvider modifica puntos en memoria; no es reserva/contabilidad transaccional. CuentaPuntos es agregado conceptual propuesto. |',
'| RF-06 Formación y talleres | Planificado | Tablas y requisitos; progreso, evaluaciones, certificados y asistencia no acreditados por API operativa. |',
'| RF-07 Sorteos | Planificado | Persistencia parcial; faltan lista congelada y evidencia completas. Se exigen CSPRNG, ejecución única y hash por HU-050. |',
'| RF-08 Beneficios y canjes | Planificado | Catálogo y canjes demostrativos. Debe coordinar reserva, cierre, descuento/liberación y stock; no doble débito. |',
'| RF-09 Contenido | Planificado | Tablas y pantallas no acreditan autorización, aprobación ni vigencia operativas. |',
'| RF-10 Notificaciones | Planificado | Recuperación de clave por correo es independiente; no prueba servicio general asíncrono ni bandeja. |',
'| RF-11 Juegos y retos | Planificado | Configuración y resultados demo; fórmulas e intentos deben validarse por servidor. |',
'| RF-12 Comunidad | Planificado | Tablas y demo; privacidad, reportes, moderación y suspensiones requieren reglas/servicios. |',
'| RF-13 Bienestar | Planificado | Convenios y contenidos informativos, sin atención clínica o datos de salud personales. |',
'| RF-14 Reportes | Planificado | Paneles de ejemplos; sin agregaciones y exportación real del backend. ServicioReportes es propuesta de responsabilidad. |',
'\n## Evidencia concreta revisada\n',
'- Backend: config/urls.py y apps/usuarios/urls.py delimitan API real a autenticación, registro, perfil, sesiones, recuperación y validación administrativa temporal. Models, servicios, permisos y validadores contrastan el comportamiento. No hay backend de referidos, campañas o gamificación acreditado por esas rutas.',
'- Frontend: api/auth.js y api/administracion.js son llamadas reales; ValidarSocios.jsx usa listado y conversión reales. PanelSocio.jsx y PanelAdmin.jsx importan datos/demo.js; canjear modifica useState, sin garantía de libro o stock. La etiqueta demostrativa no se usa como requisito.',
'- SQL 01: esquema general, asociaciones, restricciones e inmutabilidad. SQL 02: campos complementarios, historial, talleres y preguntas XOR. SQL 03: recuperación de un uso. SQL 04: formato diez dígitos. SQL 05: padrón y unicidad normalizada. SQL 06: política final de formato. Ningún script se ejecutó.',
'- Pruebas inspeccionadas: test_registro_sprint1, test_conversion_socio, test_concurrencia_registro, test_codigos_socio, test_roles, test_recuperacion, test_sprint1_sesiones, test_esquema_registro, test_cedula; formularios, AuthContext y cliente HTTP. Evidencian alcance de identidad; no se extrapolan a módulos futuros.',
'- documentacion/sprint-1-equipo/verificacion.md informa 135 pruebas backend y 20 frontend previas. Esta entrega no reejecutó suites de aplicación ni accedió a PostgreSQL; sus verificaciones son del modelo UML. Se conserva la diferencia entre evidencia previa reportada y prueba ejecutada ahora.',
'\n## Límites del análisis\n',
'Mapear 91 HU y 14 familias RF verifica referencias, no aceptación completa. Las 27 subtareas originales conservan su padre y no se suman como historias independientes. La matriz enlaza operaciones representativas y reglas con conceptos de apoyo. Aristas exactas de transición, políticas de límites, niveles, stock, segmentos, adjudicación de suplentes y aprobación requieren decisión donde se indica.\n',
'La regla de no negatividad y rechazo de reverso negativo está definida por HU-036/038. Lo pendiente es su coordinación con reservas y límites, no autorizar saldo deudor. Los puntos reconocidos antes de una modificación de campaña se preservan mediante una instantánea propuesta.']
(o/'ANALISIS-ALCANCE.md').write_text('\n'.join(report),encoding='utf-8')
manifest=[]
paths=[root/'README.md']+list((root/'documentacion').glob('*.docx'))+list((root/'documentacion').glob('*.xlsx'))+[root/'documentacion/product_con_subtareas.csv']+list((root/'docs').glob('*.md'))+list((root/'documentacion/sprint-1-equipo').glob('*.md'))+list((root/'documentacion/sprint-1-valeria').glob('*.md'))+list((root/'backend/sql').glob('0[1-6]*.sql'))
for folder in ['backend/apps/usuarios/models','backend/apps/usuarios/services','backend/apps/usuarios/tests','backend/apps/usuarios/validators','frontend/src/api','frontend/src/context']:
    paths+=list((root/folder).glob('*.py'))+list((root/folder).glob('*.js'))+list((root/folder).glob('*.jsx'))
paths+=[root/p for p in ['backend/apps/usuarios/urls.py','backend/apps/usuarios/permissions.py','backend/config/urls.py','frontend/src/datos/demo.js','frontend/src/panel/PanelSocio.jsx','frontend/src/panel/PanelAdmin.jsx','frontend/src/panel/ValidarSocios.jsx']]
for p in sorted(set(paths)):manifest.append(dict(ruta=str(p.relative_to(root)),sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
(o/'fuentes/manifest-fuentes.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print('Fuentes:',len(manifest),'HU:',len(source),'UR:',len(urs),'RF detallados:',len(rfs),'familias:',len(families))
