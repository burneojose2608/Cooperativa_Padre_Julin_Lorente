"""Construye especificaciones trazables desde el backlog original, sin modificarlo."""
from pathlib import Path
import csv
import hashlib
import json
import re
import zipfile
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / 'documentacion'
SPECS = ROOT / 'specs'
SLUGS = ['usuarios', 'autenticacion', 'referidos', 'campanas', 'gamificacion',
         'formacion', 'sorteos', 'recompensas', 'contenidos', 'notificaciones',
         'juegos-retos', 'comunidad', 'bienestar', 'reportes']


def rows(path):
    with path.open(encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + '\n', encoding='utf-8')


def main():
    backlog = rows(DOC / 'product_con_subtareas.csv')
    requirements = rows(DOC / 'entregable/requisitos_funcionales.csv')
    nonfunctional = rows(DOC / 'entregable/requisitos_no_funcionales.csv')
    index = {r['Work item ID']: r for r in backlog}
    source_hash = hashlib.sha256((DOC / 'product_con_subtareas.csv').read_bytes()).hexdigest()
    trace = []
    overview = ['# Alcance y sprints del proyecto', '',
        'Línea base documental del 20/11/2026. Los criterios se conservan desde las historias y subtareas consolidadas. '
        'Las casillas abiertas requieren implementación o comprobación actual; ningún estado se infiere del CSV de Jira.', '',
        '## Funcionalidades', '', '| Especificación | Historias | Subtareas | Sprints |', '| --- | --- | --- | --- |']
    for number, slug in enumerate(SLUGS, 1):
        epic = index[str(number)]
        group = []
        for row in backlog:
            parent = row['Parent']
            if row['Work Type'] == 'Sub-task':
                parent = index.get(parent, {}).get('Parent', '')
            if parent == str(number) and row['Work Type'] in ('Story', 'Sub-task'):
                group.append(row)
        folder = SPECS / f'{number:03}-{slug}'
        title = epic['Summary'].split(': ', 1)[-1]
        spec = [f'# {title}', '', '## Objetivo y alcance', '', epic['Description'], '',
                '## Reglas vigentes', '',
                'Aplican `../../documentacion/entregable/CAMBIOS-DE-LINEA-BASE.md` y '
                '`../../.specify/memory/constitution.md`. La recuperación de contraseña por consola y el padrón '
                'de prueba conservan su condición temporal. Las reglas institucionales sin respuesta se mantienen pendientes.', '',
                '## Historias y escenarios de aceptación', '']
        tasks = [f'# Tareas de {title.lower()}', '',
                 'Conservar el sprint planificado y la relación padre de cada ítem. '
                 'No sumar otra vez los puntos de las subtareas incluidos en la historia consolidada.', '']
        for row in group:
            hu = row['Summary'].split(':', 1)[0]
            spec.extend([f"### {row['Summary']}", '',
                         f"Sprint: {row['Sprint planificado']}. Tipo: {row['Work Type']}. "
                         f"Ítem original: {row['Work item ID']}. Padre: {row['Parent']}.", '', row['Description'], ''])
            # RF links come from the current matrix, including associations inherited by consolidation.
            linked = [r for r in requirements if r['nivel'] == 'Detalle' and hu in re.findall(r'HU-\d+', r['hu_asociadas'])]
            for r in linked:
                trace.append({'spec': folder.name, 'sprint': row['Sprint planificado'], 'item': row['Work item ID'],
                    'tipo': row['Work Type'], 'hu': hu, 'rf': r['id_requisito'], 'ur': r['ur_asociados'],
                    'cu': r['cu_asociados'], 'estado_fuente': r['estado_implementacion']})
            tasks.extend([f"## {row['Sprint planificado']} {hu}", '',
                f"- [ ] {hu}-V Revisar código y evidencia existente frente a los criterios de la historia.",
                f"- [ ] {hu}-B Completar dominio, transacciones, autorización y API requeridos.",
                f"- [ ] {hu}-U Completar la pantalla conectada al servidor con validaciones y estados vacíos.",
                f"- [ ] {hu}-P Verificar escenarios de éxito, rechazo, pertenencia e idempotencia aplicables.",
                f"- [ ] {hu}-D Actualizar trazabilidad, documentación y resultado de aceptación.", ''])
        relevant = [r for r in requirements if r['id_padre'] == f'RF-{number:02}']
        spec.extend(['## Requisitos funcionales vigentes', ''])
        for r in relevant:
            spec.extend([f"### {r['id_requisito']} {r['nombre']}", '', r['descripcion'], '',
                         f"UR: {r['ur_asociados']}. HU: {r['hu_asociadas']}. CU: {r['cu_asociados']}.", ''])
        spec.extend(['## Requisitos de calidad', ''])
        for r in nonfunctional:
            if f'RF-{number:02}' in re.findall(r'RF-\d{2}(?!-)', r.get('rf_asociados', '')) or any(
                    f'RF-{number:02}-' in r.get('rf_asociados', '') for _ in [0]):
                spec.extend([f"- **{r['id_requisito']} {r['nombre']}:** {r['descripcion']}"])
        spec.extend(['', '## Cierre', '',
            'Todos los escenarios de la funcionalidad deben tener evidencia actual. Revisar autorización por rol y '
            'permiso, acceso al objeto, tratamiento de datos, concurrencia y fallos. '
            'Las capacidades externas o mediciones no ejecutadas se registran como pendientes.'])
        write(folder / 'spec.md', '\n'.join(spec))
        write(folder / 'tasks.md', '\n'.join(tasks))
        write(folder / 'plan.md', f'''# Plan de {title.lower()}

## Arquitectura

Mantener React y su cliente HTTP autenticado, Django REST Framework y PostgreSQL. Reutilizar
usuarios, sesiones, permisos, auditoría, archivos privados y cola de notificaciones existentes.
El dominio se implementa en servicios, con validación explícita en los límites de la API.

## Datos y compatibilidad

Reutilizar las tablas del SQL inicial y sus nombres físicos. Añadir columnas y restricciones
mediante scripts transaccionales repetibles y un comando de actualización; probar en base test_*.
Conservar los registros existentes y las asignaciones de permisos revocadas. Ninguna operación
de interfaz ejecuta los scripts de instalación inicial.

## Contratos y seguridad

Documentar rutas y campos en los serializadores y la guía operativa. Separar consulta propia,
catálogo visible y gestión autorizada. El servidor calcula puntuaciones, saldos y elegibilidad;
los identificadores del cliente nunca deciden el titular ni el importe de una recompensa.
Bloquear los agregados que compiten por saldo, cupo, stock o cambios de estado. Las operaciones
repetidas conservan un resultado único por actividad de origen.

## Dependencias y orden

Respetar los RF de dependencia incluidos en spec.md y los sprints originales. La base común
es identidad y permisos, seguida de campañas y referidos, libro de puntos y formación;
los canjes, sorteos, juegos y reportes consumen esas actividades validadas.

## Verificación

Cubrir los criterios de cada HU, incluyendo las subtareas consolidadas. Ejecutar pruebas backend
en PostgreSQL aislado, pruebas de interfaz, lint y build. Registrar los comandos y resultados
actuales y las limitaciones de integraciones, revisión visual, carga y despliegue.
''')
        overview.append(f"| [{title}]({folder.name}/spec.md) | {sum(r['Work Type']=='Story' for r in group)} | "
                        f"{sum(r['Work Type']=='Sub-task' for r in group)} | {', '.join(sorted(set(r['Sprint planificado'] for r in group)))} |")
    overview.extend(['', '## Plan por sprint', ''])
    for sprint in sorted(set(r['Sprint planificado'] for r in backlog if r['Sprint planificado'])):
        overview.extend([f'### {sprint}', ''])
        for row in backlog:
            if row['Sprint planificado'] == sprint:
                overview.append(f"- {row['Summary']} ({row['Work Type']}, ítem {row['Work item ID']}, padre {row['Parent'] or 'sin padre'}).")
        overview.append('')
    overview.extend(['## Integridad de las fuentes', '', f'SHA-256 del backlog original: `{source_hash}`.', '',
                     'El catálogo `trazabilidad.csv` relaciona las historias y subtareas con los RF, UR y CU vigentes. '
                     'Las tareas técnicas de Sprint 0 están incluidas en el plan por sprint y conservadas en `backlog.json`.'])
    write(SPECS / 'README.md', '\n'.join(overview))
    write(SPECS / 'backlog.json', json.dumps(backlog, ensure_ascii=False, indent=2))
    with (SPECS / 'trazabilidad.csv').open('w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(trace[0]))
        writer.writeheader()
        writer.writerows(trace)
    # Read the original DOCX files as OOXML; preserve all originals.
    originals = {}
    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    for path in DOC.glob('*.docx'):
        with zipfile.ZipFile(path) as z:
            xml = ET.fromstring(z.read('word/document.xml'))
            originals[path.name] = '\n'.join(''.join(p.itertext()) for p in xml.findall('.//w:t', ns))
    write(ROOT / '.tools/documentos-originales.json', json.dumps(originals, ensure_ascii=False, indent=2))
    hu_covered = set(t['hu'] for t in trace)
    print(json.dumps({'modulos': 14, 'items': len(backlog), 'historias': sum(r['Work Type']=='Story' for r in backlog),
        'subtareas': sum(r['Work Type']=='Sub-task' for r in backlog), 'enlaces': len(trace),
        'hu_trazadas': len(hu_covered), 'originales_docx': list(originals)}, ensure_ascii=False))


if __name__ == '__main__':
    main()
