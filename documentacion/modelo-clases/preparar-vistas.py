"""Reduce cruces en vistas pequeñas y conserva la identidad de todos los elementos."""
from pathlib import Path
import json,itertools,math,sys
sys.stdout.reconfigure(encoding='utf-8')
b=Path(__file__).resolve().parent;o=Path((b/'entrega-actual.txt').read_text(encoding='utf-8-sig').strip())
m=json.loads((o/'modelo-revisado.json').read_text(encoding='utf-8-sig'));classes={c['nombre']:c for c in m['clases']}
for v in m['vistas']:v['relaciones']=[r for r in v['relaciones'] if r!='REL-026']
for v in m['vistas']:
    if v['id']=='V-22':v['relaciones']=[r for r in v['relaciones'] if r not in ['REL-016','REL-062','REL-063']]
if not any(v['id']=='V-30' for v in m['vistas']):
    m['vistas'].append(dict(id='V-30',nombre='Reversos compensatorios',clases=['CuentaPuntos','MovimientoPuntos'],principal=False,relaciones=['REL-022','REL-026'],dependencias=[]))
else:
    next(v for v in m['vistas'] if v['id']=='V-30')['relaciones']=['REL-022','REL-026']
rels={x['id']:x for x in m['asociaciones']+m['dependencias']}
def cross(a,b,c,d):
    def orient(p,q,r):return (q[0]-p[0])*(r[1]-p[1])-(q[1]-p[1])*(r[0]-p[0])
    return orient(a,b,c)*orient(a,b,d)<0 and orient(c,d,a)*orient(c,d,b)<0
for v in m['vistas']:
    if v['principal']:
        pairs={('Usuario','Socio'),('Socio','CodigoReferido'),('CodigoReferido','Referido'),('Referido','Conversion'),('Socio','CuentaPuntos'),('Socio','Canje')}
        v['relaciones']=[i for i in v['relaciones'] if (rels[i]['a'],rels[i]['b']) in pairs]
        v['dependencias']=[i for i in v['dependencias'] if (rels[i]['a'],rels[i]['b']) in {('Referido','ActividadValidada'),('Canje','CuentaPuntos')}]
        names=['Usuario','Socio','CodigoReferido','Canje','CuentaPuntos','Referido','ActividadValidada','Conversion']
        slots=[(0,0),(1,0),(2,0),(0,1),(1,1),(2,1),(1,2),(2,2)]
        best=tuple(names)
    else:
        names=v['clases'];n=len(names)
        slots={2:[(0,0),(1,0)],3:[(0,0),(1,0),(0,1)],4:[(0,0),(1,0),(0,1),(1,1)],5:[(0,0),(1,0),(2,0),(0,1),(2,1)],6:[(0,0),(1,0),(2,0),(0,1),(1,1),(2,1)],7:[(0,0),(1,0),(2,0),(0,1),(1,1),(2,1),(1,2)]}[n]
        edges=set(tuple(sorted((rels[i]['a'],rels[i]['b']))) for i in v['relaciones']+v['dependencias'] if rels[i]['a']!=rels[i]['b'])
        edgeidx=[(names.index(a),names.index(b)) for a,b in edges]
        distances={(i,j):(slots[i][0]-slots[j][0])**2+(slots[i][1]-slots[j][1])**2 for i in range(n) for j in range(n)}
        paircost={}
        for a in range(n):
            for c in range(a+1,n):
                for d in range(n):
                    for e in range(d+1,n):
                        paircost[a,c,d,e]=cross(slots[a],slots[c],slots[d],slots[e]) if len({a,c,d,e})==4 else False
        best=None;bestscore=float('inf')
        for placement in itertools.permutations(range(n)):
            es=[tuple(sorted((placement[a],placement[c]))) for a,c in edgeidx]
            score=sum(distances[a,c]*3 for a,c in es)
            for a,c in es:
                p,q=slots[a],slots[c]
                for j in range(n):
                    if j in (a,c):continue
                    t=slots[j]
                    if (q[0]-p[0])*(t[1]-p[1])==(q[1]-p[1])*(t[0]-p[0]) and min(p[0],q[0])<=t[0]<=max(p[0],q[0]) and min(p[1],q[1])<=t[1]<=max(p[1],q[1]):score+=150
            score+=sum(45 for e1,e2 in itertools.combinations(es,2) if paircost[e1+e2])
            if score<bestscore:bestscore=score;best=placement
        order=[None]*n
        for i,p in enumerate(best):order[p]=names[i]
        best=tuple(order)
    dims={}
    for name in names:
        c=classes[name];width=max(370,int(max([len(x) for x in c['atributos']+c['operaciones']]+[len(name)])*6.4+85));height=max(145,90+18*(len(c['atributos'])+len(c['operaciones'])))
        dims[name]=(width,height)
    maxw=max(x[0] for x in dims.values());maxh=max(x[1] for x in dims.values())
    v['posiciones']={name:dict(x=70+sx*(maxw+240)+(maxw-dims[name][0])//2,y=70+sy*(maxh+200),w=dims[name][0],h=dims[name][1]) for name,(sx,sy) in zip(best,slots)}
    v['clases']=list(best)
# Panorama selectivo: las conexiones omitidas siguen visibles en detalles.
for r in rels.values():assert any(r['id'] in v['relaciones']+v['dependencias'] for v in m['vistas']),r['id']
(o/'modelo-revisado.json').write_text(json.dumps(m,ensure_ascii=False,indent=2),encoding='utf-8')
print('Posiciones revisadas para',len(m['vistas']),'diagramas; todas las relaciones conservan una vista.')
