from pathlib import Path
import zipfile, xml.etree.ElementTree as E, json, csv, re, hashlib
base = Path(__file__).resolve().parent
root = base.parent.parent
out = Path((base/'entrega-actual.txt').read_text(encoding='utf-8-sig').strip())/'fuentes'
out.mkdir(exist_ok=True)
ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
for p in (root/'documentacion').glob('*.docx'):
    with zipfile.ZipFile(p) as z:
        doc=E.fromstring(z.read('word/document.xml'))
        lines=[''.join(t.text or '' for t in para.findall('.//w:t',ns)) for para in doc.findall('.//w:p',ns)]
    (out/(p.stem+'.txt')).write_text('\n'.join(lines),encoding='utf-8')
nsx={'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
for p in (root/'documentacion').glob('*.xlsx'):
    with zipfile.ZipFile(p) as z:
        strings=[]
        if 'xl/sharedStrings.xml' in z.namelist():
            strings=[''.join(t.text or '' for t in si.findall('.//s:t',nsx)) for si in E.fromstring(z.read('xl/sharedStrings.xml')).findall('s:si',nsx)]
        blocks=[]
        for name in z.namelist():
            if re.fullmatch(r'xl/worksheets/sheet\d+.xml',name):
                blocks.append(name)
                for row in E.fromstring(z.read(name)).findall('.//s:row',nsx):
                    cells=[]
                    for c in row.findall('s:c',nsx):
                        v=c.find('s:v',nsx); text=v.text if v is not None else ''.join(t.text or '' for t in c.findall('.//s:t',nsx))
                        if c.get('t')=='s': text=strings[int(text)]
                        if text: cells.append(c.get('r')+'='+str(text))
                    if cells: blocks.append(' | '.join(cells))
    (out/(p.stem+'.txt')).write_text('\n'.join(blocks),encoding='utf-8')
rows=list(csv.DictReader((root/'documentacion/product_con_subtareas.csv').open(encoding='utf-8-sig',newline='')))
(out/'backlog.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'salida':str(out),'filasBacklog':len(rows),'documentos':[p.name for p in out.glob('*.txt')]},ensure_ascii=False))
