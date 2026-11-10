from pathlib import Path
import xml.etree.ElementTree as E, json, re
b=Path(__file__).resolve().parent
o=Path((b/'entrega-actual.txt').read_text(encoding='utf-8-sig').strip())
def rows(t): return [{c.tag:c.text or '' for c in r} for r in E.parse(o/f'antes-{t}.xml').findall('.//Row')]
objects={x['Object_ID']:x for x in rows('t_object')}
ds=rows('t_diagram'); dos=rows('t_diagramobjects')
for d in ds:
    print('DIAGRAMA',d['Diagram_ID'],d['Name'],'paquete',d['Package_ID'],'GUID',d['ea_guid'])
    for do in dos:
        if do['Diagram_ID']==d['Diagram_ID']:
            ob=objects.get(do['Object_ID'],{})
            if ob.get('Object_Type')=='UseCase': print('  CU',ob['Object_ID'],ob['Name'],ob['ea_guid'],'nota',ob.get('Note','')[:600])
print('escenarios',len(rows('t_objectscenarios')))
for p in (o/'fuentes').glob('*.txt'):
    if 'Vision' in p.name or 'Presentacion' in p.name:
        print('FUENTE',p.name)
        lines=p.read_text(encoding='utf-8').splitlines()
        print('\n'.join(x for x in lines if x.strip())[:15000])
backlog=json.loads((o/'fuentes/backlog.json').read_text(encoding='utf-8'))
for x in backlog:
    if re.match(r'HU-\d+',x['Summary']):
        print(x['Work item ID'],x['Work Type'],x['Summary'],'PADRE',x['Parent'],x['Description'])
