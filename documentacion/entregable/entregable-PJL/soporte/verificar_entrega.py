from pathlib import Path
import csv,json,hashlib,re,zipfile
from PIL import Image,ImageDraw,ImageFont
from pypdf import PdfReader

OUT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def hojas_contacto_pdf():
    qa=OUT/'soporte/qa'
    font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',19)
    for grupo in ['contexto','casos-uso','clases']:
        files=sorted(qa.glob('pdf-'+grupo+'-*.png'))
        for start in range(0,len(files),6):
            im=Image.new('RGB',(1800,1800),'#e5e7eb');draw=ImageDraw.Draw(im)
            for i,p in enumerate(files[start:start+6]):
                x=(i%2)*900;y=(i//2)*600
                draw.text((x+15,y+8),p.name,font=font,fill='black')
                tile=Image.open(p).convert('RGB');tile.thumbnail((875,550))
                im.paste(tile,(x+(900-tile.width)//2,y+38+(550-tile.height)//2))
            im.save(qa/f'revision-pdf-{grupo}-{start//6+1:02}.jpg',quality=92)

def validar():
    counts={}
    for name,n in [('requisitos_usuario.csv',57),('requisitos_funcionales.csv',105),('requisitos_no_funcionales.csv',26)]:
        with (OUT/name).open(encoding='utf-8-sig',newline='') as f:
            rows=list(csv.DictReader(f))
        assert len(rows)==n and len({r['id_requisito'] for r in rows})==n
        assert all(r['descripcion'].strip() for r in rows)
        counts[name]=n
    rendered={}
    for name,grupo,n in [('diagrama_contexto.pdf','contexto',1),('diagrama_casos_uso.pdf','casos-uso',26),('diagrama_clases.pdf','clases',31)]:
        pdf=PdfReader(str(OUT/name));assert len(pdf.pages)==n
        assert all(p.extract_text().strip() for p in pdf.pages)
        imgs=list((OUT/'soporte/qa').glob('pdf-'+grupo+'-*.png'))
        assert len(imgs)==n,(name,len(imgs))
        for p in imgs:
            with Image.open(p) as im:
                assert im.width>200 and im.height>200
        rendered[name]=dict(paginas=n,renderizadas=n)
    with zipfile.ZipFile(OUT/'sprint-1/codigo_fuente_sprint_1.zip') as z:
        assert z.testzip() is None
        assert 'backend/manage.py' in z.namelist() and 'frontend/package.json' in z.namelist()
        assert not any(Path(n).name.startswith('.env') for n in z.namelist())
    native=OUT/'fuente-enterprise/Modelo-negocio-Padre-Julian-Lorente.eapx'
    ea=json.loads((OUT/'soporte/inventario-entrega-ea.json').read_text(encoding='utf-8-sig'))
    assert sha(native).upper()==ea['sha256'].upper()
    return dict(csv=counts,pdf=rendered,fuente_ea_sha256_coincide=True,zip_codigo_integro=True)

def empaquetar():
    final=[]
    for p in sorted(OUT.rglob('*')):
        if not p.is_file():continue
        rel=p.relative_to(OUT).as_posix()
        if rel.startswith(('soporte/qa/','soporte/exportaciones-ea/','soporte/__pycache__/')) or rel in {'MANIFIESTO.csv','entregable-PJL.zip'} or p.suffix.lower()=='.ldb':continue
        final.append(dict(archivo=rel,bytes=p.stat().st_size,sha256=sha(p)))
    with (OUT/'MANIFIESTO.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=['archivo','bytes','sha256']);w.writeheader();w.writerows(final)
    with zipfile.ZipFile(OUT/'entregable-PJL.zip','w',zipfile.ZIP_DEFLATED) as z:
        for r in final:z.write(OUT/r['archivo'],arcname=r['archivo'])
        z.write(OUT/'MANIFIESTO.csv',arcname='MANIFIESTO.csv')
    with zipfile.ZipFile(OUT/'entregable-PJL.zip') as z:assert z.testzip() is None
    print(json.dumps(dict(archivos_finales=len(final)+1,zip_bytes=(OUT/'entregable-PJL.zip').stat().st_size),ensure_ascii=False))

if __name__=='__main__':
    import sys
    if '--contactos' in sys.argv:hojas_contacto_pdf()
    elif '--empaquetar' in sys.argv:empaquetar()
    else:print(json.dumps(validar(),ensure_ascii=False))
