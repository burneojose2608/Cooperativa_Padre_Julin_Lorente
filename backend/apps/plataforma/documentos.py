"""PDF paginado de texto con fuentes estándar; no ejecuta HTML ni recursos remotos."""
import textwrap


def pdf_texto(titulo, lineas):
    texto = [titulo, '']
    for linea in lineas:
        texto.extend(textwrap.wrap(str(linea), width=90) or [''])
    paginas=[texto[i:i+45] for i in range(0,len(texto),45)]
    objetos=[b'', b'', b'<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>']
    ids=[]
    for pagina in paginas:
        pid=len(objetos)+1;cid=pid+1;ids.append(pid)
        objetos.append(f'<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Resources << /Font << /F1 3 0 R >> >> /Contents {cid} 0 R >>'.encode())
        comandos=['BT /F1 11 Tf 50 750 Td 15 TL']
        for linea in pagina:
            valor=linea.replace('\\','\\\\').replace('(','\\(').replace(')','\\)').replace('\r',' ').replace('\n',' ')
            comandos.append(f'({valor}) Tj T*')
        contenido=('\n'.join(comandos)+'\nET').encode('cp1252',errors='replace')
        objetos.append(f'<< /Length {len(contenido)} >>\nstream\n'.encode()+contenido+b'\nendstream')
    objetos[0]=b'<< /Type /Catalog /Pages 2 0 R >>'
    objetos[1]=f'<< /Type /Pages /Count {len(ids)} /Kids [{" ".join(f"{i} 0 R" for i in ids)}] >>'.encode()
    salida=bytearray(b'%PDF-1.4\n%\xe2\xe3\xcf\xd3\n');offsets=[0]
    for i,objeto in enumerate(objetos,1):
        offsets.append(len(salida));salida.extend(f'{i} 0 obj\n'.encode()+objeto+b'\nendobj\n')
    xref=len(salida)
    salida.extend(f'xref\n0 {len(offsets)}\n0000000000 65535 f \n'.encode())
    for offset in offsets[1:]: salida.extend(f'{offset:010} 00000 n \n'.encode())
    salida.extend(f'trailer\n<< /Size {len(offsets)} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n'.encode())
    return bytes(salida)
