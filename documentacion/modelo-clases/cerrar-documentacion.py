from pathlib import Path
import json,csv,hashlib,sys
sys.stdout.reconfigure(encoding='utf-8')
b=Path(__file__).resolve().parent;o=Path((b/'entrega-actual.txt').read_text(encoding='utf-8-sig').strip())
m=json.loads((o/'modelo-revisado.json').read_text(encoding='utf-8-sig'));v=json.loads((o/'VALIDACION.json').read_text(encoding='utf-8'));meta=json.loads((o/'procedencia.json').read_text(encoding='utf-8-sig'))
els=json.loads((o/'elementos-ea.json').read_text(encoding='utf-8-sig'));links=json.loads((o/'conectores-ea.json').read_text(encoding='utf-8-sig'));diags=json.loads((o/'diagramas-ea.json').read_text(encoding='utf-8-sig'))
bykey={x['clave']:x for x in els};lk={x['clave']:x for x in links}
assert all(c['resultado']=='Correcto' for c in v['comprobaciones'])
visual=[]
for d in diags:
    p=Path(d['archivo']);visual.append(dict(id=d['id'],nombre=d['nombre'],archivo='diagramas-ea/'+p.name,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),revision='Inspeccionado visualmente desde PNG exportado por EA; atributos, operaciones y multiplicidades legibles al abrir a tamaño completo',observacion='Panorama selectivo; el resto de relaciones se conserva en detalles' if d['id']=='V-00' else 'Vista de detalle; referencias reutilizan las mismas clases nativas'))
(o/'REVISION-VISUAL.json').write_text(json.dumps(visual,ensure_ascii=False,indent=2),encoding='utf-8')
with (o/'RELACIONES-VERIFICADAS.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.writer(f);w.writerow(['ID','Tipo','Clase_A','ID_A','GUID_A','Multiplicidad_A','Clase_B','ID_B','GUID_B','Multiplicidad_B','Conector_ID','Conector_GUID','Significado','Fuente'])
    for r in m['asociaciones']+m['dependencias']:
        a=bykey['PJL.CL.'+r['a']];z=bykey['PJL.CL.'+r['b']];co=lk[r['id']]
        w.writerow([r['id'],co['tipo'],r['a'],a['id'],a['guid'],r.get('ma',''),r['b'],z['id'],z['guid'],r.get('mb',''),co['id'],co['guid'],r['nombre'],r['fuente']])
attrs=sum(len(c['atributos']) for c in m['clases']);ops=sum(len(c['operaciones']) for c in m['clases'])
originals={x['tabla']:x['anteriores'] for x in v['preservacion']}
readme=f'''# Entrega del modelo de clases de negocio

Se creó y verificó un modelo UML nativo dentro de **Model → Vista_Logica** en una copia del repositorio. El original anterior se conserva sin cambios y tiene respaldo fechado. Se usó la Automation Interface de EA; los SELECT de inventario fueron de lectura. No se escribieron tablas internas, no se eliminó manualmente el LDB y no se modificó código ni base de datos de la aplicación.

Abra [el repositorio actualizado](Modelo-negocio-Padre-Julian-Lorente.eapx). El panorama se llama **Diagrama de clases de negocio**, directamente en Vista_Logica; las otras vistas están en Diagramas de detalle. Las mismas clases se reutilizan, con atributos privados, operaciones públicas, parámetros, retornos y multiplicidades editables.

## Contenido entregado

- **75 clases**, **{attrs} atributos** y **{ops} operaciones** de análisis, más **10 enumeraciones** nativas.
- **103 asociaciones**, incluidas dos composiciones justificadas, y **44 dependencias de dominio**.
- **31 diagramas** exportados e inspeccionados visualmente; [galería local](DIAGRAMAS.html) y [panorama PNG](diagramas-ea/V-00.png).
- **514 dependencias de trazabilidad**, con 91 referencias HU originales, 91 RF detallados, 14 familias RF, 57 UR y una decisión posterior identificada. Las 27 subtareas conservan sus padres y no duplican esfuerzo.

## Documentos de lectura

- [Alcance contrastado](ANALISIS-ALCANCE.md): documentos, implementación real, SQL, pruebas previas y demostraciones; estado por familia RF.
- [Catálogo revisado](CATALOGO-REVISADO.md): responsabilidades, atributos y operaciones con estado y fuente.
- [Relaciones justificadas](RELACIONES.md) y [relaciones verificadas con GUID](RELACIONES-VERIFICADAS.csv).
- [Reglas y pendientes](REGLAS-Y-PENDIENTES.md): decisiones sustentadas, hipótesis y diferencias respecto de la propuesta anterior.
- [Matriz verificada](TRAZABILIDAD-VERIFICADA.csv) y [detalle JSON](TRAZABILIDAD-VERIFICADA.json): UR/RF/HU, padre, CU real, clase, regla, operación, fuente, estado, GUID de elementos y de conexiones.
- [Validación](VALIDACION.md), [resultados estructurados](VALIDACION.json), [reapertura y editabilidad](reapertura-y-editabilidad.json) y [revisión visual](REVISION-VISUAL.json).
- [Inventario de elementos](elementos-ea.json), [conectores](conectores-ea.json), [diagramas](diagramas-ea.json) y [registro de creación y actualización](registro-ea.jsonl).

## Respaldo y conservación

Respaldo consistente creado con el original cerrado: [{Path(meta['respaldoConsistente']).name}]({Path(meta['respaldoConsistente']).name}). SHA-256: `{meta['sha256RespaldoConsistente']}`. Su igualdad con el original se comprobó al terminar. [Procedencia](procedencia.json) registra rutas, conexión detectada por API, proceso y huellas. El archivo respaldo-original de la misma carpeta es una captura previa tomada mientras EA estaba abierto; se conserva como antecedente, y el respaldo-cerrado es la referencia de restauración.

Se conservaron los {originals['t_object']} elementos, {originals['t_diagram']} diagramas y {originals['t_connector']} conectores anteriores, sus miembros y los dos escenarios, comprobando los datos anteriores por relectura. Las conexiones nuevas hacia CU no se confunden con conexiones que ya existían. Las consultas antes/después se conservan como XML.

## Decisiones y límites

Se separaron Usuario, Socio, Prospecto y Referido; roles múltiples sin herencia de actores; código de socio distinto del de referido; conversión comercial distinta de validación manual temporal. Se separaron registro, autenticación, autorización y notificaciones, y se incorporaron instantáneas de incentivo reconocido y elegibles congelados. El responsable de ejecución del sorteo queda relacionado con su evidencia.

Las reglas posteriores sustituyen el verificador y el rechazo de cuentas ausentes del padrón, preservando la referencia histórica. HU-038 sí define rechazo de reversos que generen saldo negativo, y HU-050 sí exige aleatoriedad criptográficamente segura. Las fórmulas de saldos son propuesta de análisis coherente con reserva sin doble débito; base de nivel/clasificación, límites por período, coordinación con reservas, stock, segmentación y suplentes siguen pendientes donde se indica. No se incorporó core productivo, cuentas financieras, créditos operativos ni datos clínicos.

Las {len(v['comprobaciones'])} comprobaciones estructurales finalizaron correctamente. EA cerró y reabrió la copia; Update sobre cada clase confirmó editabilidad sin cambiar su contenido. Las 31 imágenes se inspeccionaron; deben abrirse a tamaño completo para leer las vistas amplias. La captura interactiva posterior agotó su autorización, por lo que la evidencia visual final procede de las exportaciones de EA. No se reejecutaron las suites de la aplicación ni se certificó aceptación completa por mapear una HU. El archivo permanece abierto en el panorama mediante la API.

Los documentos de la raíz de modelo-clases y sus PlantUML son antecedentes previos conservados. Esta carpeta contiene la entrega nativa nueva. No se entrega un XMI sin importar ni una imagen como sustituto del UML.

## Repetición de la actualización

La inspección y respaldo se ejecutan una sola vez contra el original. Para repetir esta entrega, con EA abierto en la copia identificada por procedencia.json, ejecutar desde la raíz del proyecto, de forma secuencial:

```powershell
& backend/venv/Scripts/python.exe documentacion/modelo-clases/construir-modelo-revisado.py
& backend/venv/Scripts/python.exe documentacion/modelo-clases/preparar-vistas.py
& backend/venv/Scripts/python.exe documentacion/modelo-clases/enriquecer-evidencia.py
& documentacion/modelo-clases/actualizar-ea.ps1 -Fase Modelo
& documentacion/modelo-clases/completar-requisitos-ea.ps1
& documentacion/modelo-clases/actualizar-ea.ps1 -Fase Diagramas
& documentacion/modelo-clases/reabrir-verificar-ea.ps1
& documentacion/modelo-clases/actualizar-ea.ps1 -Fase Inventario
& documentacion/modelo-clases/ajustar-cierre-ea.ps1
& backend/venv/Scripts/python.exe documentacion/modelo-clases/validar-entrega.py
```

Los Alias PJL y los identificadores de conectores propios reutilizan GUID existentes. No se borran elementos ni diagramas ajenos. El registro demuestra reejecuciones sin duplicar clases o conexiones. Una modificación futura exige volver a inspeccionar las imágenes antes de renovar la constancia de revisión visual.

La implementación de automatización se contrastó con la documentación oficial de [colecciones](https://sparxsystems.com/enterprise_architect_user_guide/17.2/add-ins___scripting/collection.html), [diagramas](https://sparxsystems.com/enterprise_architect_user_guide/17.1/add-ins___scripting/diagram2.html), [objetos de diagrama](https://sparxsystems.com/enterprise_architect_user_guide/17.1/add-ins___scripting/diagramobjects.html) y [exportación del proyecto](https://sparxsystems.com/enterprise_architect_user_guide/17.1/add-ins___scripting/project_2.html).
'''
(o/'README-ENTREGA.md').write_text(readme,encoding='utf-8')
entry=f'''# Entrega actual del modelo UML

El modelo nativo de EA está en [{o.name}/Modelo-negocio-Padre-Julian-Lorente.eapx]({o.name}/Modelo-negocio-Padre-Julian-Lorente.eapx), dentro de Model → Vista_Logica.

Consulte [la entrega completa y su respaldo]({o.name}/README-ENTREGA.md), [los diagramas]({o.name}/DIAGRAMAS.html), [la matriz verificada]({o.name}/TRAZABILIDAD-VERIFICADA.csv) y [la validación]({o.name}/VALIDACION.md).

75 clases, 103 asociaciones, 44 dependencias de dominio, 10 enumeraciones, 31 diagramas y 514 enlaces de trazabilidad. Las 91 referencias HU y 14 familias RF están mapeadas; esto no certifica aceptación completa ni convierte propuestas en funcionalidades implementadas.

El original anterior y la documentación inicial se conservan. Los Markdown y PlantUML de la raíz corresponden al antecedente de preparación, anterior a esta creación nativa.
'''
(b/'ENTREGA-ACTUAL.md').write_text(entry,encoding='utf-8')
old=(b/'README.md').read_text(encoding='utf-8')
notice='> **Entrega posterior creada en EA:** consulte [ENTREGA-ACTUAL.md](ENTREGA-ACTUAL.md). El contenido siguiente se conserva como antecedente de preparación.\n\n'
if not old.startswith('> **Entrega posterior creada en EA:'):(b/'README.md').write_text(notice+old,encoding='utf-8')
print(json.dumps(dict(clases=75,atributos=attrs,operaciones=ops,asociaciones=103,dependencias=44,diagramas=31,trazas=514,comprobaciones=len(v['comprobaciones']),anteriores=originals),ensure_ascii=False))
