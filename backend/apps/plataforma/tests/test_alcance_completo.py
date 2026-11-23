from ast import literal_eval
from datetime import datetime, timedelta
import csv
from io import BytesIO, StringIO
from tempfile import TemporaryDirectory
from unittest.mock import patch
from uuid import uuid4

from django.core import mail
from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management import call_command
from django.db import connection, transaction, DatabaseError
from django.test import TestCase, override_settings
from django.utils import timezone
from pypdf import PdfReader
from rest_framework.test import APIClient

from apps.usuarios.models import Auditoria, HistorialEstado, Socio, PadronPrueba, RolPermiso, Usuario
from apps.usuarios.services.codigos_socio import ServicioSocios
from apps.plataforma import models as m, negocio as n
from apps.plataforma.api_reportes import celda_csv_segura
from apps.plataforma.tests.test_sprint2 import crear_usuario, imagen

BASE='/api/plataforma/negocio/'
BANCO=[{'enunciado':'¿Es útil ahorrar?','opciones':['Sí','No'],'correcta':0}]


class AlcanceCompletoTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin=crear_usuario(8101,'Administrador')
        cls.marketing=crear_usuario(8102,'Responsable de Marketing')
        cls.rse=crear_usuario(8103,'Responsable de Responsabilidad Social')
        cls.gestor=crear_usuario(8104,'Gestor de contenidos')
        cls.usuario=crear_usuario(8105,'Socio')
        cls.otro=crear_usuario(8106,'Socio')
        cls.general=crear_usuario(8107)
        cls.socio=ServicioSocios.crear_socio_validado(cls.usuario)
        cls.socio2=ServicioSocios.crear_socio_validado(cls.otro)
        cls.codigo=m.CodigoReferido.generar_para(cls.socio)
        for actividad in m.ReglaPuntos.ACTIVIDADES:
            m.ReglaPuntos.objects.create(tipo_actividad=actividad,puntos=100,limite_periodo=10,periodo='DIA',
                                         vigente_desde=timezone.localdate(),version=actividad)

    def setUp(self):
        self.c=APIClient();self.c.force_authenticate(self.usuario)
        self.tmp=TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        s=override_settings(MEDIA_ROOT=self.tmp.name,MAILERS={'default':{'BACKEND':'django.core.mail.backends.locmem.EmailBackend'}})
        s.enable();self.addCleanup(s.disable)

    def como(self,u): self.c.force_authenticate(u)

    def post(self,path,data=None,esperado=200):
        r=self.c.post(BASE+path,data or {},format='json')
        self.assertEqual(r.status_code,esperado,r.data)
        return r.json() if r.status_code!=204 else None

    def campana(self,**extra):
        datos=dict(nombre='Ahorra',inicio=timezone.localdate()-timedelta(days=1),fin=timezone.localdate()+timedelta(days=10),
            tipo='REFERIDOS',objetivo='Captación',meta=10,incentivos='Puntos',condiciones='Socios activos',creado_por=self.marketing)
        datos.update(extra);return m.Campana.objects.create(**datos)

    def beneficio(self,**extra):
        datos=dict(nombre='Libro',costo_puntos=70,stock=1,descripcion='Educación',condiciones='Retiro en agencia',desde=timezone.localdate())
        datos.update(extra);return m.Beneficio.objects.create(**datos)

    def credito(self,origen=1): return n.acreditar(self.socio,'CONVERSION',origen)

    def curso(self):
        c=m.Capacitacion.objects.create(titulo='Ahorro',modalidad='VIRTUAL',estado='PUBLICADA',descripcion='Aprende',duracion=2)
        u=m.ModuloCapacitacion.objects.create(capacitacion=c,orden=1,titulo='Presupuesto')
        e=m.Evaluacion.objects.create(capacitacion=c,nota_minima=60,max_intentos=2,preguntas=BANCO)
        return c,u,e

    def test_campana_segmentada_y_permiso_revocado(self):
        c=self.campana(estado='ACTIVA',segmentacion={'RANGO_EDAD':[18,40]})
        self.assertEqual(len(self.c.get(BASE+'campanas/').json()['resultados']),1)
        c.segmentacion={'AGENCIA':['Loja']};c.save()
        self.assertEqual(self.c.get(BASE+'campanas/').json()['resultados'],[])
        self.socio.segmento={'AGENCIA':'Loja'};self.socio.save()
        self.assertEqual(len(self.c.get(BASE+'campanas/').json()['resultados']),1)
        self.como(self.marketing)
        RolPermiso.objects.filter(rol__nombre='Responsable de Marketing',permiso__modulo='campanas').delete()
        self.post(f'campanas/{c.pk}/estado/',{'estado':'SUSPENDIDA','motivo':'Pausa'},403)

    def test_campana_publicada_llega_solo_al_segmento_tras_filtrar_el_catalogo(self):
        self.socio.segmento = {'AGENCIA': 'Loja'}
        self.socio.save(update_fields=['segmento'])
        self.como(self.marketing)
        hoy = timezone.localdate()
        datos = {'nombre': 'Invitación de Loja', 'tipo': 'REFERIDOS', 'objetivo': 'Captar', 'meta': 2,
                 'incentivos': 'Puntos', 'condiciones': 'Socios de Loja', 'inicio': hoy.isoformat(),
                 'fin': (hoy+timedelta(days=5)).isoformat(), 'segmentacion': {'AGENCIA': ['Loja']}}
        campana = self.post('campanas/', datos, 201)
        self.como(self.usuario)
        self.assertEqual(self.c.get(BASE+'campanas/').json()['resultados'], [])
        self.como(self.marketing)
        self.post(f'campanas/{campana["id"]}/estado/', {'estado': 'ACTIVA', 'motivo': 'Inicio de campaña'})
        m.Campana.objects.bulk_create([
            m.Campana(nombre='Otra agencia', tipo='REFERIDOS', objetivo='Captar', meta=1,
                      incentivos='Puntos', condiciones='Socios', inicio=hoy, fin=hoy+timedelta(days=1),
                      creado_por=self.marketing, estado='ACTIVA', segmentacion={'AGENCIA': ['Cuenca']})
            for _ in range(200)
        ])
        self.como(self.usuario)
        self.assertEqual([c['id'] for c in self.c.get(BASE+'campanas/').json()['resultados']], [campana['id']])
        self.como(self.otro)
        self.assertEqual(self.c.get(BASE+'campanas/').json()['resultados'], [])
        self.como(self.marketing)
        self.post(f'campanas/{campana["id"]}/estado/', {'estado': 'SUSPENDIDA', 'motivo': 'Pausa'})
        self.como(self.usuario)
        self.assertEqual(self.c.get(BASE+'campanas/').json()['resultados'], [])

    def test_rol_socio_sin_validacion_recibe_un_mensaje_en_espanol(self):
        Socio.objects.filter(pk=self.socio.pk).update(validado_en=None)
        for ruta in ('/api/plataforma/referidos/codigo/', BASE+'campanas/'):
            respuesta = self.c.get(ruta)
            self.assertEqual(respuesta.status_code, 403)
            self.assertIn('validada como socio', str(respuesta.data))

    def test_catalogos_rechazan_campos_y_valores_invalidos(self):
        self.como(self.admin)
        self.post('beneficios/',{'nombre':'X','costo_puntos':-1,'stock':2,'descripcion':'x','condiciones':'x','desde':str(timezone.localdate()),'hasta':None,'convenio':None,'activo':True},400)
        self.post('niveles/',{'nombre':'Bronce','umbral_puntos':0,'usuario':self.usuario.pk},400)
        self.post('niveles/',{'nombre':'Bronce','umbral_puntos':0},201)
        self.post('niveles/',{'nombre':'Plata','umbral_puntos':0},400)

    def test_referido_confirmacion_y_conversion_con_credito_unico(self):
        datos={'codigo':self.codigo.valor,'cedula':'9999999999','nombre':'Prospecto','correo':'persona@example.com',
               'producto':'Cuenta de ahorro','acepta_terminos':True}
        with patch('apps.plataforma.negocio.secrets.token_urlsafe',return_value='token-confirmacion'):
            self.post('referidos/',datos,201)
        r=m.Referido.objects.get()
        self.assertEqual(r.estado,'REGISTRADO')
        self.assertIsNone(r.prospecto.consentimiento_en)
        publico=APIClient()
        token=n.huella('contacto:token-confirmacion')
        respuesta=publico.post(f'/api/plataforma/referidos/confirmar/{token}/',{},format='json')
        self.assertEqual(respuesta.status_code,200,respuesta.data)
        r.prospecto.refresh_from_db();self.assertIsNotNone(r.prospecto.consentimiento_en)
        self.assertEqual(publico.post(f'/api/plataforma/referidos/confirmar/{token}/',{},format='json').status_code,404)
        self.como(self.marketing)
        self.post(f'referidos/{r.pk}/estado/',{'estado':'CONVERTIDO','motivo':'No sigue ciclo'},400)
        self.post(f'referidos/{r.pk}/estado/',{'estado':'EN_SEGUIMIENTO','motivo':'Contactado'})
        self.post(f'referidos/{r.pk}/estado/',{'estado':'CONVERTIDO','motivo':'Apertura validada','tipo_evento':'APERTURA_CUENTA'})
        self.post(f'referidos/{r.pk}/estado/',{'estado':'CONVERTIDO','motivo':'Reintento','tipo_evento':'APERTURA_CUENTA'},400)
        self.assertEqual(m.Conversion.objects.count(),1)
        self.assertEqual(n.saldo(self.socio),100)

    def test_referidos_privacidad_autorreferido_padron_y_duplicado(self):
        datos={'codigo':self.codigo.valor,'cedula':self.usuario.cedula,'nombre':'Prospecto','correo':'otra@example.com','producto':'Ahorro','acepta_terminos':True}
        rechazo = self.post('referidos/',datos,400)
        self.assertEqual(self.post('referidos/', {**datos, 'cedula': '9999999991',
                                                 'correo': self.usuario.correo}, 400), rechazo)
        datos['cedula']='9999999998';PadronPrueba.objects.create(cedula=datos['cedula'],activo=True)
        self.assertEqual(self.post('referidos/',datos,400), rechazo)
        datos['cedula']='9999999997';datos['telefono']='0990000099';self.post('referidos/',datos,201)
        publico = APIClient()
        codigo2 = m.CodigoReferido.generar_para(self.socio2)
        ruta = f'/api/plataforma/invitaciones/{codigo2.valor}/referir/'
        for cambios in [
            {'correo': 'nuevo@example.com', 'telefono': '0990000001'},
            {'cedula': '9999999996', 'telefono': '0990000001'},
            {'cedula': '9999999996', 'correo': 'nuevo@example.com'},
        ]:
            respuesta = publico.post(ruta, {**datos, **cambios}, format='json')
            self.assertEqual(respuesta.status_code, 400)
            self.assertEqual(respuesta.json(), rechazo)
        self.assertEqual(m.Referido.objects.get().codigo_id, self.codigo.pk)
        lista=self.c.get(BASE+'referidos/').json()['resultados']
        self.assertNotEqual(lista[0]['contacto'],datos['correo'])
        self.como(self.otro)
        self.assertEqual(self.c.get(BASE+'referidos/').json()['resultados'],[])
        self.post('referidos/',{**datos,'cedula':'9999999996'},403)

    def test_registro_publico_valida_datos_codigo_y_frecuencia(self):
        publico = APIClient()
        ruta = f'/api/plataforma/invitaciones/{self.codigo.valor}/referir/'
        datos = {'cedula': '9999999995', 'nombre': 'Prospecto', 'producto': 'Ahorro'}
        self.addCleanup(cache.clear)
        cache.clear()
        self.assertEqual(publico.post(ruta, ['dato'], format='json').status_code, 400)
        self.assertEqual(publico.post(ruta, {**datos, 'acepta_terminos': True}, format='json').status_code, 400)
        datos['correo'] = 'publico@example.com'
        self.assertEqual(publico.post(ruta, {**datos, 'acepta_terminos': False}, format='json').status_code, 400)
        datos['acepta_terminos'] = True
        invalido = '/api/plataforma/invitaciones/INVALIDO/referir/'
        self.assertEqual(publico.post(invalido, datos, format='json').status_code, 404)
        # Los cuatro intentos previos consumen el mismo límite anónimo.
        for _ in range(56):
            self.assertEqual(publico.post(invalido, datos, format='json').status_code, 404)
        self.assertEqual(publico.post(ruta, datos, format='json').status_code, 429)
        self.assertFalse(m.Referido.objects.exists())

    def test_marketing_filtra_referidos_sin_permiso_de_campanas_y_respeta_consentimiento(self):
        campana = self.campana(estado='ACTIVA')
        datos = {'codigo': self.codigo.valor, 'cedula': '9999999994', 'nombre': 'Prospecto',
                 'correo': 'privado@example.com', 'producto': 'Ahorro', 'acepta_terminos': True}
        self.post('referidos/', {**datos, 'campana': self.campana(estado='SUSPENDIDA').pk}, 400)
        self.post('referidos/', {**datos, 'campana': campana.pk}, 201)
        self.post('referidos/', {**datos, 'cedula': '9999999993', 'correo': 'otro@example.com'}, 201)
        r = m.Referido.objects.get(campana=campana)
        self.assertEqual(r.codigo.socio_id, self.socio.pk)
        RolPermiso.objects.filter(rol__nombre='Responsable de Marketing', permiso__modulo='campanas').delete()
        self.como(self.marketing)
        hoy = timezone.localdate().isoformat()
        filtros = {'campana': campana.pk, 'socio': self.socio.pk, 'desde': hoy, 'hasta': hoy,
                   'estado': 'REGISTRADO'}
        respuesta = self.c.get(BASE+'referidos/', filtros)
        self.assertEqual(respuesta.status_code, 200)
        self.assertTrue(respuesta.json()['puede_gestionar'])
        fila, = respuesta.json()['resultados']
        self.assertEqual(fila['id'], r.pk)
        self.assertTrue(fila['creado_en'])
        self.assertNotEqual(fila['nombre'], datos['nombre'])
        self.assertEqual(fila['contacto'], '••••')
        for campo, valor in {'socio': self.socio2.pk, 'estado': 'CONVERTIDO',
                             'hasta': (timezone.localdate()-timedelta(days=1)).isoformat()}.items():
            self.assertEqual(self.c.get(BASE+'referidos/', {**filtros, campo: valor}).json()['resultados'], [])
        n.confirmar_referido(n.huella('contacto:'+r.prospecto.token_nonce))
        fila, = self.c.get(BASE+'referidos/', {**filtros, 'estado': 'CONFIRMADO'}).json()['resultados']
        self.assertEqual(fila['contacto'], datos['correo'])
        ruta_estado = f'referidos/{r.pk}/estado/'
        self.post(ruta_estado, {'estado': 'RECHAZADO', 'motivo': 'Prospecto desistió'})
        self.post(ruta_estado, {'estado': 'EN_SEGUIMIENTO', 'motivo': 'Reintento'}, 400)
        self.assertEqual(n.saldo(self.socio), 0)
        self.como(self.otro)
        self.assertEqual(self.c.get(BASE+'referidos/', filtros).json()['resultados'], [])
        self.como(self.rse)
        self.assertEqual(self.c.get(BASE+'referidos/').status_code, 403)

    @override_settings(CONSENTIMIENTO_REFERIDO_HORAS=1)
    def test_plazo_de_consentimiento_bloquea_seguimiento_y_expira(self):
        datos = {'codigo': self.codigo.valor, 'cedula': '9999999992', 'nombre': 'Prospecto',
                 'correo': 'plazo@example.com', 'producto': 'Ahorro', 'acepta_terminos': True}
        self.post('referidos/', datos, 201)
        r = m.Referido.objects.get()
        p = r.prospecto
        self.assertAlmostEqual((p.expira_en-timezone.now()).total_seconds(), 3600, delta=10)
        self.como(self.marketing)
        self.post(f'referidos/{r.pk}/estado/', {'estado': 'EN_SEGUIMIENTO', 'motivo': 'Sin confirmar'}, 400)
        self.post(f'referidos/{r.pk}/estado/', {'estado': 'EXPIRADO', 'motivo': 'Aún vigente'}, 400)
        p.expira_en = timezone.now()-timedelta(seconds=1)
        p.save(update_fields=['expira_en'])
        token = n.huella('contacto:'+p.token_nonce)
        self.assertEqual(APIClient().post(f'/api/plataforma/referidos/confirmar/{token}/').status_code, 400)
        call_command('mantener_prospectos', '--aplicar')
        r.refresh_from_db()
        p.refresh_from_db()
        self.assertEqual(r.estado, 'EXPIRADO')
        self.assertIsNone(p.consentimiento_en)

    def test_acreditacion_limite_idempotencia_e_inmutabilidad(self):
        regla=m.ReglaPuntos.objects.get(tipo_actividad='CONVERSION_REFERIDO');regla.limite_periodo=1;regla.save()
        primero=self.credito()
        self.assertEqual(n.acreditar(self.socio,'CONVERSION',1).pk,primero.pk)
        self.assertIsNone(n.acreditar(self.socio,'CONVERSION',2))
        self.assertEqual(n.saldo(self.socio),100)
        with self.assertRaises(DatabaseError),transaction.atomic():
            m.MovimientoPuntos.objects.filter(pk=primero.pk).update(cantidad=9999)

    def test_reserva_aprobacion_entrega_no_descuenta_dos_veces(self):
        self.credito();b=self.beneficio();clave=str(uuid4())
        c=self.post(f'beneficios/{b.pk}/canjear/',{'clave':clave,'acepta_condiciones':True},201)
        c2=self.post(f'beneficios/{b.pk}/canjear/',{'clave':clave,'acepta_condiciones':True},201)
        self.assertEqual(c['id'],c2['id']);self.assertEqual(n.saldo(self.socio),30)
        self.como(self.admin)
        self.post(f'canjes/{c["id"]}/estado/',{'estado':'APROBADA','motivo':'Revisado'})
        self.assertEqual(n.saldo(self.socio),30)
        self.post(f'canjes/{c["id"]}/estado/',{'estado':'ENTREGADA','motivo':'Recibido en agencia'})
        self.assertEqual(n.saldo(self.socio),30)
        self.post(f'canjes/{c["id"]}/estado/',{'estado':'ENTREGADA','motivo':'Repetido'},400)

    def test_rechazo_libera_stock_y_puntos_y_reverso_no_negativo(self):
        mov=self.credito();b=self.beneficio()
        c=self.post(f'beneficios/{b.pk}/canjear/',{'clave':str(uuid4()),'acepta_condiciones':True},201)
        self.como(self.admin)
        self.post(f'movimientos/{mov.pk}/revertir/',{'motivo':'Acción invalidada'},400)
        self.post(f'canjes/{c["id"]}/estado/',{'estado':'RECHAZADA','motivo':'No cumple'})
        self.assertEqual(n.saldo(self.socio),100);b.refresh_from_db();self.assertEqual(b.stock,1)
        self.post(f'movimientos/{mov.pk}/revertir/',{'motivo':'Acción invalidada'})
        self.assertEqual(n.saldo(self.socio),0)
        self.post(f'movimientos/{mov.pk}/revertir/',{'motivo':'Repetido'},400)

    def test_stock_saldo_convenio_y_titularidad(self):
        b=self.beneficio();self.post(f'beneficios/{b.pk}/canjear/',{'clave':str(uuid4()),'acepta_condiciones':True},400)
        self.credito();c=self.post(f'beneficios/{b.pk}/canjear/',{'clave':str(uuid4()),'acepta_condiciones':True},201)
        self.post(f'beneficios/{b.pk}/canjear/',{'clave':str(uuid4()),'acepta_condiciones':True},400)
        self.como(self.otro);self.assertEqual(self.c.get(BASE+'canjes/').json()['resultados'],[])
        self.post(f'canjes/{c["id"]}/estado/',{'estado':'APROBADA','motivo':'Intento ajeno'},403)

    def test_formacion_evaluacion_servidor_certificado_y_acceso_ajeno(self):
        c,u,e=self.curso()
        self.post(f'capacitaciones/{c.pk}/inscribir/',{'acepta_requisitos':True},201)
        self.post(f'capacitaciones/{c.pk}/evaluar/',{'respuestas':[0]},400)
        self.post(f'capacitaciones/{c.pk}/progreso/',{'unidad':u.pk})
        aula=self.c.get(BASE+f'capacitaciones/{c.pk}/aula/').json()
        self.assertNotIn('correcta',aula['preguntas'][0])
        self.post(f'capacitaciones/{c.pk}/evaluar/',{'respuestas':[0],'nota':100},400)
        resultado=self.post(f'capacitaciones/{c.pk}/evaluar/',{'respuestas':[0]})
        self.assertTrue(resultado['aprobado']);self.assertEqual(n.saldo(self.socio),100)
        cert=m.Certificado.objects.get();respuesta=self.c.get(BASE+f'certificados/{cert.pk}/pdf/')
        lector=PdfReader(BytesIO(respuesta.content));self.assertIn('Ahorro',lector.pages[0].extract_text())
        self.como(self.otro)
        self.assertEqual(self.c.get(BASE+f'certificados/{cert.pk}/pdf/').status_code,404)
        publico=APIClient();r=publico.get('/api/plataforma/certificados/verificar/'+cert.codigo_verificacion+'/')
        self.assertTrue(r.json()['valido']);self.assertNotIn(self.usuario.cedula,str(r.json()))

    def test_evaluacion_limite_y_banco_no_modificable(self):
        c,u,e=self.curso();i=n.inscribir(self.usuario,c.pk)
        m.Progreso.objects.create(inscripcion=i,unidad=u,porcentaje=100)
        for _ in range(2): self.post(f'capacitaciones/{c.pk}/evaluar/',{'respuestas':[1]})
        self.post(f'capacitaciones/{c.pk}/evaluar/',{'respuestas':[0]},400)
        self.como(self.rse)
        self.assertEqual(self.c.put(BASE+f'evaluaciones/{e.pk}/',{'nota_minima':0},format='json').status_code,400)

    def test_t043_formacion_puntos_reto_y_sorteo_elegible(self):
        hoy = timezone.localdate()
        self.socio.segmento = {'AGENCIA': 'Loja'}
        self.socio.save(update_fields=['segmento'])
        campana = self.campana(estado='ACTIVA', segmentacion={'AGENCIA': ['Loja']})
        otra_campana = self.campana(estado='ACTIVA', segmentacion={'AGENCIA': ['Otra agencia']})
        for candidata in (campana, otra_campana):
            m.Sorteo.objects.create(campana=candidata, nombre='Sorteo de formación', premio='Libro',
                                    fecha=timezone.now()+timedelta(days=1), estado='ACTIVO', origen='CAPACITACION')
        reto = m.Reto.objects.create(objetivo='Aprobar una capacitación', meta=1, inicio=hoy, fin=hoy,
                                     actividad='CAPACITACION')
        self.como(self.rse)
        curso = self.post('capacitaciones/', {'titulo': 'Ahorro', 'modalidad': 'VIRTUAL',
            'descripcion': 'Aprender a ahorrar', 'duracion': 2, 'requisitos': 'Ser socio activo'}, 201)
        ruta = f'capacitaciones/{curso["id"]}/'
        unidad = self.post('modulos/', {'capacitacion': curso['id'], 'orden': 1, 'titulo': 'Presupuesto'}, 201)
        segunda = self.post('modulos/', {'capacitacion': curso['id'], 'orden': 2, 'titulo': 'Ahorro'}, 201)
        self.post(ruta+'estado/', {'estado': 'PUBLICADA', 'motivo': 'Curso listo'}, 400)
        self.post('evaluaciones/', {'capacitacion': curso['id'], 'nota_minima': 100,
                                    'max_intentos': 2, 'preguntas': BANCO}, 201)
        archivo = imagen()
        contenido = archivo.read()
        archivo.seek(0)
        material = self.c.post('/api/plataforma/materiales/', {
            'titulo': 'Guía privada', 'categoria': 'Ahorro', 'archivo': archivo, 'modulos': f'[{unidad["id"]}]',
        }, format='multipart')
        self.assertEqual(material.status_code, 201, material.data)
        ruta_material = f'/api/plataforma/materiales/{material.data["id"]}/archivo/'
        self.post(ruta+'estado/', {'estado': 'PUBLICADA', 'motivo': 'Curso listo'})

        self.como(self.usuario)
        visibles = self.c.get(BASE+'campanas/').json()['resultados']
        self.assertEqual([c['id'] for c in visibles], [campana.pk])
        listado = self.c.get(BASE+'capacitaciones/').json()['resultados']
        self.assertEqual(listado[0]['requisitos'], 'Ser socio activo')
        self.assertEqual(self.c.get(BASE+ruta+'aula/').status_code, 404)
        self.assertEqual(self.c.get(ruta_material).status_code, 404)
        self.post(ruta+'inscribir/', {}, 400)
        inscripcion = self.post(ruta+'inscribir/', {'acepta_requisitos': True}, 201)['id']
        self.assertEqual(self.post(ruta+'inscribir/', {'acepta_requisitos': True}, 201)['id'], inscripcion)
        self.assertEqual(m.Inscripcion.objects.filter(socio=self.socio).count(), 1)

        material = self.c.get(ruta_material)
        self.assertEqual(material.status_code, 200)
        self.assertEqual(material['Cache-Control'], 'private, no-store')
        self.assertEqual(b''.join(material.streaming_content), contenido)
        self.post(ruta+'progreso/', {'unidad': unidad['id']})
        self.post(ruta+'progreso/', {'unidad': unidad['id']})
        otra_sesion = APIClient()
        login = otra_sesion.post('/api/auth/login/', {
            'identificador': self.usuario.username, 'clave': 'Inicial12345',
        }, format='json')
        self.assertEqual(login.status_code, 200, login.data)
        otra_sesion.credentials(HTTP_AUTHORIZATION=f'Bearer {login.data["access"]}')
        aula = otra_sesion.get(BASE+ruta+'aula/').json()
        self.assertEqual(aula['porcentaje_avance'], 50)
        self.assertNotIn('correcta', aula['preguntas'][0])
        self.post(ruta+'evaluar/', {'respuestas': [0]}, 400)
        self.post(ruta+'progreso/', {'unidad': segunda['id']})
        self.assertEqual(self.c.get(BASE+ruta+'aula/').json()['porcentaje_avance'], 100)
        self.assertFalse(self.post(ruta+'evaluar/', {'respuestas': [1]})['aprobado'])
        self.assertEqual(self.c.get(BASE+ruta+'aula/').json()['intentos_restantes'], 1)
        self.assertEqual(self.c.get(BASE+'mis-actividades/').json()['certificados'], [])
        self.assertFalse(m.ActividadValidada.objects.filter(socio=self.socio).exists())

        self.assertTrue(self.post(ruta+'evaluar/', {'respuestas': [0]})['aprobado'])
        self.post(ruta+'evaluar/', {'respuestas': [0]}, 400)
        evaluacion = m.IntentoEvaluacion.objects.get(inscripcion_id=inscripcion, aprobado=True)
        self.assertEqual((evaluacion.respuestas, evaluacion.nota), ([0], 100))
        auditoria = Auditoria.objects.get(usuario=self.usuario, entidad='intento_evaluacion',
                                         registro_id=str(evaluacion.pk), accion='APROBAR_CAPACITACION')
        self.assertEqual(auditoria.detalle, {'inscripcion': inscripcion})
        actividades = self.c.get(BASE+'mis-actividades/').json()
        self.assertEqual(len(actividades['certificados']), 1)
        cert, = actividades['certificados']
        pdf = self.c.get(BASE+f'certificados/{cert["id"]}/pdf/')
        self.assertEqual(pdf.status_code, 200)
        texto_pdf = PdfReader(BytesIO(pdf.content)).pages[0].extract_text()
        for dato in (self.usuario.nombre, curso['titulo'], cert['codigo'], cert['fecha'][:10]):
            self.assertIn(dato, texto_pdf)
        verificacion = APIClient().get(f'/api/plataforma/certificados/verificar/{cert["codigo"]}/').json()
        self.assertEqual(set(verificacion), {'valido', 'titulo', 'emitido_en', 'codigo'})
        self.assertTrue(verificacion['valido'])
        self.assertRegex(cert['codigo'], r'^[0-9a-f]{32}$')
        movimientos = self.c.get(BASE+'puntos/').json()
        self.assertEqual(movimientos['saldo'], 200)
        self.assertCountEqual([p['origen_tipo'] for p in movimientos['movimientos']], ['CAPACITACION', 'RETO'])
        self.assertEqual(m.ActividadValidada.objects.filter(socio=self.socio, origen_tipo='CAPACITACION',
                                                          origen_id=inscripcion).count(), 1)
        avance, = actividades['retos']
        self.assertEqual(avance['avance'], 1)
        self.assertTrue(avance['completado_en'])
        self.assertTrue(m.ProgresoReto.objects.filter(reto=reto, socio=self.socio).exists())
        participacion = m.ParticipacionSorteo.objects.get(origen_tipo='CAPACITACION', origen_id=inscripcion)
        self.assertEqual((participacion.socio_id, participacion.sorteo.campana_id), (self.socio.pk, campana.pk))

        self.como(self.otro)
        self.assertEqual(self.c.get(BASE+ruta+'aula/').status_code, 404)
        self.assertEqual(self.c.get(ruta_material).status_code, 404)
        self.assertEqual(self.c.get(BASE+f'certificados/{cert["id"]}/pdf/').status_code, 404)
        self.assertEqual(self.c.get(BASE+'mis-actividades/').json()['certificados'], [])

        RolPermiso.objects.filter(rol__nombre='Socio', permiso__modulo='formacion', permiso__accion='participar').delete()
        self.assertEqual(otra_sesion.get(BASE+ruta+'aula/').status_code, 403)
        self.assertEqual(otra_sesion.get(ruta_material).status_code, 404)
        self.assertEqual(otra_sesion.post('/api/auth/logout/', {}, format='json').status_code, 204)
        self.assertEqual(otra_sesion.get(ruta_material).status_code, 401)
        self.como(self.rse)
        inscritos = self.c.get(BASE+ruta+'participantes/').json()['resultados']
        self.assertEqual(len(inscritos), 1)
        self.assertEqual(inscritos[0]['modulos_completados'], 2)
        self.assertEqual(inscritos[0]['porcentaje_avance'], 100)
        self.assertEqual(inscritos[0]['intentos'], 2)
        self.assertEqual(float(inscritos[0]['nota_maxima']), 100)
        social = self.c.get(BASE+'reportes/', {'tipo': 'social', 'desde': hoy.isoformat()}).json()['resultados']
        valores = {fila['indicador']: fila['valor'] for fila in social}
        self.assertEqual([valores[k] for k in ('Inscritos', 'Aprobados', 'Certificados',
                                               'Horas de formación aprobadas')], [1, 1, 1, 2])
        self.assertEqual(sum(v for k, v in valores.items() if k.startswith('Inscripciones por edad')), 1)
        self.como(self.otro)
        self.assertEqual(self.c.get(BASE+ruta+'participantes/').status_code, 403)

    def test_taller_cupo_asistencia_y_acreditacion_unica(self):
        t=m.Taller.objects.create(titulo='Taller',fecha=timezone.now()+timedelta(days=1),cupo=1,modalidad='VIRTUAL',lugar='Enlace')
        a=self.post(f'talleres/{t.pk}/inscribir/',{},201)
        self.como(self.otro);self.post(f'talleres/{t.pk}/inscribir/',{},400)
        self.como(self.rse);self.post(f'asistencias/{a["id"]}/confirmar/',{},400)
        t.fecha=timezone.now()-timedelta(hours=1);t.save()
        self.post(f'asistencias/{a["id"]}/confirmar/')
        self.post(f'asistencias/{a["id"]}/confirmar/')
        self.assertEqual(n.saldo(self.socio),100)

    def test_juego_resultado_servidor_limite_y_puntos(self):
        juego=m.Juego.objects.create(nombre='Trivia',tipo='TRIVIA',max_intentos=1,instrucciones='Responde',preguntas=BANCO,estado='ACTIVO')
        self.assertEqual(self.c.get(BASE+'juegos/').json()['resultados'][0]['intentos_restantes'], 1)
        partida=self.post(f'juegos/{juego.pk}/iniciar/',{},201)
        self.assertEqual(self.c.get(BASE+'juegos/').json()['resultados'][0]['intentos_restantes'], 0)
        self.assertNotIn('correcta',partida['preguntas'][0])
        self.post(f'juegos/{juego.pk}/iniciar/',{},400)
        self.post(f'partidas/{partida["id"]}/finalizar/',{'respuestas':[0],'puntuacion':100},400)
        self.post(f'partidas/{partida["id"]}/finalizar/',{'respuestas':[0]})
        self.post(f'partidas/{partida["id"]}/finalizar/',{'respuestas':[0]})
        self.assertEqual(n.saldo(self.socio),100)
        self.como(self.otro)
        self.assertEqual(self.c.get(BASE+'juegos/').json()['resultados'][0]['intentos_restantes'], 1)

    def test_sorteo_congela_elegibles_y_no_repite(self):
        c=self.campana(estado='ACTIVA')
        s=m.Sorteo.objects.create(campana=c,nombre='Sorteo',premio='Libro',fecha=timezone.now()-timedelta(hours=1),estado='ACTIVO')
        m.ParticipacionSorteo.objects.create(sorteo=s,socio=self.socio,origen_tipo='CONVERSION',origen_id=1)
        self.como(self.marketing)
        r=self.post(f'sorteos/{s.pk}/ejecutar/')
        self.assertEqual(len(r['evidencia']['sha256']),64)
        self.assertEqual(m.Ganador.objects.count(),1)
        self.post(f'sorteos/{s.pk}/ejecutar/',{},400)
        self.como(self.usuario)
        self.assertNotIn('evidencia',self.c.get(BASE+'sorteos/').json()['resultados'][0])
        self.como(self.admin)
        informe = self.c.get(BASE+'reportes/?tipo=gamificacion').json()['resultados']
        valores = {fila['indicador']: fila['valor'] for fila in informe}
        self.assertEqual(valores['Sorteos ejecutados'], 1)
        self.assertEqual(valores['Ganadores de Sorteo'], 1)
        self.assertEqual(valores['Suplentes de Sorteo'], 0)

    def test_comunidad_privacidad_reaccion_reporte_moderacion(self):
        self.post('perfil-publico/',{},405)
        self.assertEqual(self.c.put(BASE+'perfil-publico/',{'alias':'Ahorrador','ranking_publico':False},format='json').status_code,200)
        p=self.post('comunidad/',{'texto':'Aprendí a ahorrar <script>alert(1)</script>'},201)
        self.assertEqual(p['alias'],'Ahorrador');self.assertNotIn('correo',p)
        self.post(f'comunidad/{p["id"]}/reaccionar/',{'tipo':'ME_GUSTA'})
        self.post(f'comunidad/{p["id"]}/reaccionar/',{'tipo':'ME_GUSTA'})
        self.assertEqual(m.Reaccion.objects.count(),1)
        ruta = f'comunidad/{p["id"]}/'
        self.como(self.otro)
        self.post(ruta+'comentar/', {'texto': 'Comentario'})
        publicaciones = self.c.get(BASE+'comunidad/').json()['resultados']
        self.assertEqual(publicaciones[0]['comentarios'][0]['alias'], self.otro.nombre.split()[0])
        self.assertNotIn('usuario', publicaciones[0]['comentarios'][0])
        self.post(ruta+'reportar/', {'motivo': 'Revisar'})
        self.assertEqual(self.c.get(BASE+'moderacion/').status_code, 403)
        reporte = m.ReporteComunidad.objects.get(usuario=self.otro)
        self.assertIsNotNone(reporte.creado_en)
        self.como(self.gestor)
        cola = self.c.get(BASE+'moderacion/').json()['resultados']
        self.assertEqual(cola[0]['id'], reporte.pk)
        self.post('moderacion/', {'reporte': reporte.pk, 'accion': 'OCULTAR', 'motivo': ''}, 400)
        decision = {'reporte': reporte.pk, 'accion': 'OCULTAR', 'motivo': 'Contenido revisado', 'suspension_dias': 1}
        self.post('moderacion/', decision)
        self.post('moderacion/', decision, 404)
        reporte.refresh_from_db()
        self.assertEqual(reporte.resolucion, decision['motivo'])
        self.assertTrue(Auditoria.objects.filter(usuario=self.gestor, accion='MODERAR_COMUNIDAD',
                                                registro_id=str(reporte.pk)).exists())
        self.como(self.otro)
        self.post(ruta+'comentar/', {'texto': 'Contenido oculto'}, 404)
        self.post(ruta+'reaccionar/', {'tipo': 'ME_GUSTA'}, 404)
        self.como(self.usuario)
        self.assertEqual(self.c.get(BASE+'comunidad/').json()['resultados'],[])
        self.post('comunidad/',{'texto':'Otra publicación'},403)

    def test_comunidad_foto_privada_y_reporte_de_comentario(self):
        ruta = BASE+'comunidad/'
        for archivo in (imagen('foto.pdf'), SimpleUploadedFile('foto.png', b'contenido invalido', 'image/png'),
                        SimpleUploadedFile('grande.png', b'x' * (10*1024*1024+1), 'image/png')):
            with self.subTest(archivo=archivo.name):
                self.assertEqual(self.c.post(ruta, {'texto': 'Ilustración', 'imagen': archivo}, format='multipart').status_code, 400)
        respuesta = self.c.post(ruta, {'texto': 'Ilustración', 'imagen': imagen()}, format='multipart')
        self.assertEqual(respuesta.status_code, 201)
        pk = respuesta.data['id']
        self.assertEqual(respuesta.data['alias'], 'Socio')
        self.assertTrue(respuesta.data['imagen'])
        publicacion = m.Publicacion.objects.get(pk=pk)
        self.usuario.foto = publicacion.imagen
        self.usuario.save(update_fields=['foto'])
        avatar = f'{ruta}{pk}/foto-autor/'
        archivo = f'{ruta}{pk}/imagen/'
        self.assertEqual(APIClient().get(archivo).status_code, 401)
        self.assertEqual(APIClient().get(avatar).status_code, 401)
        self.como(self.general)
        self.assertEqual(self.c.get(ruta).status_code, 403)
        self.assertEqual(self.c.get(archivo).status_code, 403)
        self.assertEqual(self.c.get(avatar).status_code, 403)
        self.como(self.otro)
        self.assertTrue(self.c.get(ruta).data['resultados'][0]['tiene_foto'])
        foto = self.c.get(avatar)
        self.assertEqual(foto.status_code, 200)
        self.assertEqual(foto['Cache-Control'], 'private, no-store')
        self.assertTrue(b''.join(foto.streaming_content).startswith(b'\x89PNG'))
        descarga = self.c.get(archivo)
        self.assertEqual(descarga.status_code, 200)
        self.assertEqual(descarga['Cache-Control'], 'private, no-store')
        self.assertTrue(descarga['Content-Disposition'].startswith('inline'))
        self.assertTrue(b''.join(descarga.streaming_content).startswith(b'\x89PNG'))
        self.post(f'comunidad/{pk}/comentar/', {'texto': 'Comentario de prueba'})
        comentario = m.Comentario.objects.get(publicacion_id=pk)
        datos_comentario = self.c.get(ruta).data['resultados'][0]['comentarios'][0]
        self.assertEqual(datos_comentario['alias'], self.otro.nombre.split()[0])
        self.assertEqual(set(datos_comentario), {'id', 'alias', 'texto', 'fecha', 'tiene_foto'})
        avatar_comentario = f'{ruta}{pk}/comentarios/{comentario.pk}/foto-autor/'
        self.assertEqual(self.c.get(avatar_comentario).status_code, 404)
        self.otro.foto = publicacion.imagen
        self.otro.save(update_fields=['foto'])
        self.assertEqual(APIClient().get(avatar_comentario).status_code, 401)
        self.assertTrue(self.c.get(ruta).data['resultados'][0]['comentarios'][0]['tiene_foto'])
        foto_comentario = self.c.get(avatar_comentario)
        self.assertEqual(foto_comentario.status_code, 200)
        self.assertTrue(b''.join(foto_comentario.streaming_content).startswith(b'\x89PNG'))
        Socio.objects.filter(usuario=self.otro).update(alias='Alias elegido')
        self.assertEqual(self.c.get(ruta).data['resultados'][0]['comentarios'][0]['alias'], 'Alias elegido')
        self.como(self.usuario)
        self.post(f'comunidad/{pk}/reportar/', {'motivo': 'Revisar comentario', 'comentario': comentario.pk})
        reporte = m.ReporteComunidad.objects.get(comentario=comentario)
        self.como(self.gestor)
        self.post('moderacion/', {'reporte': reporte.pk, 'accion': 'ELIMINAR', 'motivo': 'Se retira el comentario'})
        self.como(self.usuario)
        self.assertEqual(self.c.get(ruta).json()['resultados'][0]['comentarios'], [])
        self.assertEqual(self.c.get(avatar_comentario).status_code, 404)

    def test_ranking_opt_in_y_reportes_por_rol_y_exportacion(self):
        self.credito()
        self.assertEqual(self.c.get(BASE+'ranking/').json()['resultados'],[])
        self.assertEqual(self.c.get(BASE+'ranking/').json()['mi_posicion'],1)
        self.socio.alias='Alias privado';self.socio.ranking_publico=True;self.socio.save()
        self.assertEqual(self.c.get(BASE+'ranking/').json()['resultados'][0]['alias'],'Alias privado')
        self.assertEqual(self.c.get(BASE+'reportes/?tipo=general').status_code,403)
        self.como(self.marketing);self.assertEqual(self.c.get(BASE+'reportes/?tipo=social').status_code,403)
        self.como(self.admin)
        general = {f['indicador']: f['valor'] for f in self.c.get(BASE+'reportes/?tipo=general').json()['resultados']}
        self.assertEqual(general['Usuarios activos'], Usuario.objects.filter(estado='ACTIVA').count())
        self.assertEqual(general['Puntos emitidos'], 100)
        self.assertEqual(general['Puntos canjeados'], 0)
        self.assertEqual(self.c.get(BASE+'reportes/?tipo=general&formato=csv').status_code,200)
        pdf=self.c.get(BASE+'reportes/?tipo=general&formato=pdf')
        self.assertGreater(len(PdfReader(BytesIO(pdf.content)).pages),0)

    def test_t043_reportes_conservan_alcance_filtros_y_privacidad_al_exportar(self):
        hoy = timezone.localdate()
        campana = self.campana(nombre='Campaña de Loja', estado='ACTIVA', segmentacion={'AGENCIA': ['Loja']})
        otra = self.campana(nombre='Otra campaña', estado='ACTIVA')
        for indice, candidata in enumerate((campana, campana, otra), start=1):
            prospecto = m.Prospecto.objects.create(nombre='Nombre privado', producto='Ahorro',
                                                   contacto=f'privado{indice}@ejemplo.com')
            referido = m.Referido.objects.create(codigo=self.codigo, prospecto=prospecto, campana=candidata)
            if indice == 1:
                m.Referido.objects.filter(pk=referido.pk).update(creado_en=timezone.now()-timedelta(days=5))

        filtros = {'tipo': 'referidos', 'campana': str(campana.pk), 'segmento': 'AGENCIA',
                   'desde': hoy.isoformat(), 'hasta': hoy.isoformat()}
        ruta = BASE+'reportes/'
        self.assertEqual(self.c.get(ruta, {**filtros, 'formato': 'csv'}).status_code, 403)
        self.como(self.rse)
        self.assertEqual(self.c.get(ruta, {**filtros, 'formato': 'pdf'}).status_code, 403)
        self.assertEqual(self.c.get(ruta, {'tipo': 'social'}).status_code, 200)
        self.como(self.marketing)
        self.assertEqual(self.c.get(ruta, {**filtros, 'desde': (hoy+timedelta(days=1)).isoformat()}).status_code, 400)
        datos = self.c.get(ruta, filtros).json()
        self.assertEqual(datos['filtros'], filtros)
        valores = {fila['indicador']: fila['valor'] for fila in datos['resultados']}
        self.assertEqual(valores['Referidos'], 1)
        self.assertNotIn('Conversiones en Otra campaña', valores)
        self.assertEqual(self.c.get(ruta, {**filtros, 'segmento': 'PRODUCTO'}).json()['resultados'][0]['valor'], 0)

        exportado = self.c.get(ruta, {**filtros, 'formato': 'csv'})
        self.assertEqual(exportado.status_code, 200)
        self.assertEqual(exportado['Cache-Control'], 'private, no-store')
        texto = exportado.content.decode('utf-8-sig')
        filas = list(csv.reader(StringIO(texto)))
        self.assertEqual(filas[0][0], 'Generado')
        self.assertEqual(timezone.localtime(datetime.fromisoformat(filas[0][1])).date(), hoy)
        self.assertEqual(filas[1][0], 'Filtros')
        self.assertEqual(literal_eval(filas[1][1]), filtros)
        self.assertIn(['Referidos', '1'], filas)
        pdf = self.c.get(ruta, {**filtros, 'formato': 'pdf'})
        texto_pdf = PdfReader(BytesIO(pdf.content)).pages[0].extract_text()
        self.assertIn('AGENCIA', texto_pdf)
        for respuesta in (str(datos), texto, texto_pdf):
            self.assertNotIn('Nombre privado', respuesta)
            self.assertNotIn('@ejemplo.com', respuesta)
        for celda in ('=demo', '+demo', '-demo', '@demo', '  =demo', '\ttexto'):
            self.assertEqual(celda_csv_segura(celda), "'" + celda)

    def test_actualizacion_repetible_conserva_revocacion(self):
        RolPermiso.objects.filter(rol__nombre='Socio',permiso__modulo='juegos',permiso__accion='participar').delete()
        with connection.cursor() as cur:
            cur.execute((__import__('pathlib').Path(__file__).resolve().parents[3]/'sql/08_alcance_completo.sql').read_text(encoding='utf-8').replace('BEGIN;','').replace('COMMIT;',''))
        self.assertFalse(RolPermiso.objects.filter(rol__nombre='Socio',permiso__modulo='juegos',permiso__accion='participar').exists())

    def test_general_y_anonimo_no_acceden_a_modulos(self):
        self.como(self.general)
        for recurso in ['campanas','beneficios','comunidad','puntos','capacitaciones','juegos','reportes']:
            self.assertEqual(self.c.get(BASE+recurso+'/').status_code,403,recurso)
        self.c=APIClient();self.assertEqual(self.c.get(BASE+'campanas/').status_code,401)

    def test_reto_cuenta_actividades_aunque_se_agote_limite_de_puntos(self):
        regla=m.ReglaPuntos.objects.get(tipo_actividad='JUEGO');regla.limite_periodo=1;regla.save()
        r=m.Reto.objects.create(objetivo='Dos juegos',actividad='JUEGO',meta=2,inicio=timezone.localdate(),fin=timezone.localdate())
        n.acreditar(self.socio,'JUEGO',1);n.acreditar(self.socio,'JUEGO',2)
        self.assertEqual(n.saldo(self.socio),200)  # Un juego y una recompensa de reto.
        self.assertTrue(m.ProgresoReto.objects.get(reto=r).completado_en)
        n.acreditar(self.socio,'JUEGO',2);self.assertEqual(n.saldo(self.socio),200)
        catalogo = self.c.get(BASE+'retos/').json()['resultados']
        self.assertEqual((catalogo[0]['avance'], catalogo[0]['completado']), (2, True))
        self.como(self.otro)
        otro = self.c.get(BASE+'retos/').json()['resultados']
        self.assertEqual((otro[0]['avance'], otro[0]['completado']), (0, False))

    def test_convenio_vencido_oculta_beneficio_y_rechaza_canje(self):
        convenio=m.Convenio.objects.create(entidad='Proveedor',tipo='BIENESTAR',descripcion='Descuento',
            beneficio='Lectura',condiciones='Socios',vigencia=timezone.localdate())
        b=self.beneficio(convenio=convenio);self.credito()
        self.assertEqual(self.c.get(BASE+'beneficios/').json()['resultados'][0]['entidad_convenio'], 'Proveedor')
        convenio.vigencia = timezone.localdate()-timedelta(days=1)
        convenio.save(update_fields=['vigencia'])
        self.assertEqual(self.c.get(BASE+'convenios/').json()['resultados'], [])
        self.assertEqual(self.c.get(BASE+'beneficios/').json()['resultados'],[])
        self.post(f'beneficios/{b.pk}/canjear/',{'clave':str(uuid4()),'acepta_condiciones':True},400)

    def test_aprobacion_contenido_designado_y_reaprobacion_tras_editar(self):
        from apps.plataforma.contenidos import guardar_contenido,publicar_contenido
        c=guardar_contenido(self.gestor,{'titulo':'Noticia','cuerpo':'Texto','categoria':'General','tipo':'NOTICIA',
            'desde':timezone.localdate(),'requiere_aprobacion':True,'aprobador':self.gestor})
        self.como(self.gestor)
        self.assertEqual(self.c.post(f'/api/plataforma/contenidos/{c.pk}/publicar/').status_code,400)
        self.assertEqual(self.c.post(f'/api/plataforma/contenidos/{c.pk}/aprobar/').status_code,200)
        self.assertEqual(self.c.post(f'/api/plataforma/contenidos/{c.pk}/publicar/').status_code,200)
        guardar_contenido(self.gestor,{'titulo':'Modificada'},c.pk)
        self.assertEqual(self.c.post(f'/api/plataforma/contenidos/{c.pk}/publicar/').status_code,400)

    def test_plantilla_por_canal_y_comunicaciones_obligatorias(self):
        from apps.plataforma.notificaciones import notificar,procesar_uno
        from django.core import mail
        self.como(self.admin)
        self.post('plantillas/',{'evento':'PUNTOS','canal':'CORREO','titulo':'Reconocimiento','cuerpo':'Detalle: {mensaje}'},201)
        m.EnvioNotificacion.objects.all().update(estado='OMITIDA')
        notificar(self.usuario,'PUNTOS','Recibiste cien puntos')
        for _ in range(2): procesar_uno()
        self.assertEqual(mail.outbox[0].subject,'Reconocimiento')
        self.assertIn('Detalle: Recibiste cien puntos',mail.outbox[0].body)
        self.como(self.usuario)
        self.assertEqual(self.c.put('/api/plataforma/preferencias/',{'evento':'CLAVE_ACTUALIZADA','canal':'CORREO','habilitada':False},format='json').status_code,400)
        self.assertEqual(self.c.get(BASE+'envios/').status_code,403)

    def test_mantenimiento_expira_y_anonimiza_sin_borrar_historial(self):
        p=m.Prospecto.objects.create(nombre='Datos privados',contacto='persona@example.com',correo='persona@example.com',
            producto='Ahorro',expira_en=timezone.now()-timedelta(hours=1),token_hash='x'*64)
        r=m.Referido.objects.create(codigo=self.codigo,prospecto=p)
        call_command('mantener_prospectos',aplicar=True,solicitud=p.pk,stdout=StringIO())
        p.refresh_from_db();r.refresh_from_db()
        self.assertEqual(p.contacto,'ANONIMIZADO');self.assertIsNone(p.correo);self.assertIsNone(p.token_hash)
        self.assertEqual(r.estado,'EXPIRADO')

    def test_material_de_aula_requiere_inscripcion(self):
        from apps.plataforma.contenidos import guardar_material
        c,u,e=self.curso()
        material=guardar_material(self.rse,{'titulo':'Guía','categoria':'Ahorro','archivo':imagen(),'modulos':[u.pk]})
        self.assertEqual(self.c.get(f'/api/plataforma/materiales/{material.pk}/archivo/').status_code,404)
        n.inscribir(self.usuario,c.pk)
        respuesta=self.c.get(f'/api/plataforma/materiales/{material.pk}/archivo/')
        self.assertEqual(respuesta.status_code,200)
        respuesta._resource_closers[0]()  # Cierra el archivo sin emitir request_finished dentro del TestCase.

    def test_indicadores_cac_y_captacion_usan_datos_confirmados(self):
        c=self.campana(estado='ACTIVA')
        p=m.Prospecto.objects.create(nombre='Persona',contacto='indicadores@example.com',producto='Cuenta')
        r=m.Referido.objects.create(codigo=self.codigo,prospecto=p,campana=c,estado='EN_SEGUIMIENTO')
        self.como(self.marketing)
        self.post('gastos/',{'campana':c.pk,'fecha':str(timezone.localdate()),'concepto':'Difusión','importe':'50.00'},201)
        self.post(f'referidos/{r.pk}/estado/',{'estado':'CONVERTIDO','tipo_evento':'TARJETA_ENTREGADA','motivo':'Entrega confirmada','monto_captado':'500.00'})
        datos=self.c.get(BASE+f'reportes/?tipo=referidos&campana={c.pk}').json()
        valores={v['indicador']:v['valor'] for v in datos['resultados']}
        self.assertEqual(float(valores['CAC por conversión']),50)
        self.assertEqual(float(valores['Volumen de captación confirmado']),500)

    def test_recorrido_integrado_referido_puntos_canje_entrega(self):
        from apps.plataforma.contacto import procesar_contacto

        publico = APIClient()
        ruta = f'/api/plataforma/invitaciones/{self.codigo.valor}/referir/'
        datos = {'cedula': '9888888888', 'nombre': 'Prospecto de prueba', 'correo': 'flujo@example.com',
                 'producto': 'Cuenta', 'acepta_terminos': True}
        self.assertEqual(publico.post(ruta, datos, format='json').status_code, 201)
        self.assertTrue(procesar_contacto())
        correo, = mail.outbox
        self.assertEqual(correo.to, [datos['correo']])
        token = correo.body.rsplit('/', 1)[-1]
        confirmar = f'/api/plataforma/referidos/confirmar/{token}/'
        self.assertEqual(publico.post(confirmar).status_code, 200)
        self.assertEqual(publico.post(confirmar).status_code, 404)
        r = m.Referido.objects.get()
        self.assertEqual(r.estado, 'CONFIRMADO')
        self.assertTrue(timezone.is_aware(r.prospecto.consentimiento_en))
        self.assertEqual(r.prospecto.version_politica, '1.0')
        self.assertEqual(r.codigo.socio_id, self.socio.pk)
        self.post(f'referidos/{r.pk}/estado/', {'estado': 'EN_SEGUIMIENTO', 'motivo': 'Intento del socio'}, 403)
        self.como(self.marketing)
        self.post(f'referidos/{r.pk}/estado/',{'estado':'EN_SEGUIMIENTO','motivo':'Contacto confirmado'})
        conversion = {'estado': 'CONVERTIDO', 'motivo': 'Apertura comprobada', 'tipo_evento': 'APERTURA_CUENTA'}
        self.post(f'referidos/{r.pk}/estado/', conversion)
        self.post(f'referidos/{r.pk}/estado/', conversion, 400)
        fila, = self.c.get(BASE+'referidos/', {'estado': 'CONVERTIDO'}).json()['resultados']
        self.assertEqual(fila['id'], r.pk)
        c = m.Conversion.objects.get(referido=r)
        self.assertEqual(c.validado_por_id, self.marketing.pk)
        self.assertEqual(m.MovimientoPuntos.objects.filter(
            socio=self.socio, tipo='ACREDITACION', origen_tipo='CONVERSION', origen_id=c.pk).count(), 1)
        eventos = HistorialEstado.objects.filter(entidad='referido', registro_id=r.pk).order_by('pk')
        self.assertEqual(list(eventos.values_list('estado_anterior', 'estado_nuevo', 'usuario_id')), [
            ('', 'REGISTRADO', None), ('REGISTRADO', 'CONFIRMADO', None),
            ('CONFIRMADO', 'EN_SEGUIMIENTO', self.marketing.pk),
            ('EN_SEGUIMIENTO', 'CONVERTIDO', self.marketing.pk),
        ])
        self.assertTrue(all(timezone.is_aware(e.fecha) and e.motivo for e in eventos))
        self.assertEqual(n.saldo(self.socio), 100)
        self.assertEqual(n.saldo(self.socio2), 0)
        b = self.beneficio()
        ruta_canje = f'beneficios/{b.pk}/canjear/'
        self.como(self.usuario)
        solicitud = {'clave': str(uuid4()), 'acepta_condiciones': True}
        rechazado = self.post(ruta_canje, solicitud, 201)
        self.assertEqual(self.post(ruta_canje, solicitud, 201)['id'], rechazado['id'])
        self.assertEqual(n.saldo(self.socio), 30)
        b.refresh_from_db()
        self.assertEqual(b.stock, 0)
        self.como(self.otro)
        self.assertEqual(self.c.get(BASE+'canjes/').json()['resultados'], [])
        self.post(f'canjes/{rechazado["id"]}/estado/', {'estado': 'APROBADA', 'motivo': 'Intento ajeno'}, 403)
        self.como(self.admin)
        rechazo = {'estado': 'RECHAZADA', 'motivo': 'Solicitud rechazada'}
        self.post(f'canjes/{rechazado["id"]}/estado/', rechazo)
        self.post(f'canjes/{rechazado["id"]}/estado/', rechazo, 400)
        self.assertEqual(n.saldo(self.socio), 100)
        b.refresh_from_db()
        self.assertEqual(b.stock, 1)
        self.como(self.usuario)
        canje = self.post(ruta_canje, {**solicitud, 'clave': str(uuid4())}, 201)
        self.como(self.admin)
        entrega = {'estado': 'ENTREGADA', 'motivo': 'Entrega registrada'}
        self.post(f'canjes/{canje["id"]}/estado/', entrega, 400)
        self.post(f'canjes/{canje["id"]}/estado/',{'estado':'APROBADA','motivo':'Solicitud aprobada'})
        self.assertEqual(n.saldo(self.socio), 30)
        self.post(f'canjes/{canje["id"]}/estado/', entrega)
        self.post(f'canjes/{canje["id"]}/estado/', entrega, 400)
        b.refresh_from_db()
        self.assertEqual(b.stock, 0)
        self.como(self.usuario)
        self.assertEqual(self.c.get(BASE+'puntos/').json()['saldo'],30)
        entregado = self.c.get(BASE+'canjes/').json()['resultados'][0]
        self.assertEqual(entregado['estado'], 'ENTREGADA')
        self.assertTrue(entregado['entrega'])

    def test_registro_publico_encola_confirmacion_y_reintenta_smtp_sin_bloquear_http(self):
        from apps.plataforma.contacto import procesar_contacto
        datos={'codigo':self.codigo.valor,'cedula':'9777777777','nombre':'Persona','correo':'cola@example.com','producto':'Cuenta','acepta_terminos':True}
        with patch('apps.plataforma.contacto.send_mail',side_effect=RuntimeError('Proveedor caído')) as enviar:
            self.post('referidos/',datos,201);enviar.assert_not_called()
            self.assertTrue(procesar_contacto())
        solicitud=m.SolicitudContacto.objects.get();self.assertEqual(solicitud.estado,'PENDIENTE');self.assertEqual(solicitud.intentos,1)
        solicitud.disponible_en=timezone.now()-timedelta(seconds=1);solicitud.save(update_fields=['disponible_en'])
        with patch('apps.plataforma.contacto.send_mail',return_value=1) as enviar:
            self.assertTrue(procesar_contacto());self.assertIn('/confirmar-referido/',enviar.call_args.args[1])
        solicitud.refresh_from_db();self.assertEqual(solicitud.estado,'ENVIADA')

    def test_confirmacion_vencida_no_envia_correo(self):
        from apps.plataforma.contacto import procesar_contacto
        p=m.Prospecto.objects.create(nombre='Persona',contacto='vencida@example.com',correo='vencida@example.com',producto='Cuenta',
            token_nonce='nonce',expira_en=timezone.now()-timedelta(hours=1))
        s=m.SolicitudContacto.objects.create(prospecto=p)
        with patch('apps.plataforma.contacto.send_mail') as enviar:
            self.assertTrue(procesar_contacto());enviar.assert_not_called()
        s.refresh_from_db();self.assertEqual(s.estado,'OMITIDA')

    def test_campana_ciclo_previsualizacion_edicion_historial_e_indicadores(self):
        hoy = timezone.localdate()
        self.socio.segmento = {'AGENCIA': 'Loja', 'TIPO_SOCIO': 'ACTIVO', 'PRODUCTO': 'Ahorro'}
        self.socio.save(update_fields=['segmento'])
        self.socio2.segmento = {'AGENCIA': 'Zamora'}
        self.socio2.save(update_fields=['segmento'])
        self.como(self.usuario)
        self.post('campanas/', {'nombre': 'Denegada'}, 403)
        self.como(self.rse)
        self.post('campanas/', {
            'nombre': 'Invalida', 'tipo': 'REFERIDOS', 'objetivo': 'Captar', 'meta': 2,
            'incentivos': '100 puntos', 'condiciones': 'Socios activos',
            'inicio': str(hoy), 'fin': str(hoy - timedelta(days=1)), 'segmentacion': {},
        }, 400)
        self.post('campanas/', {
            'nombre': 'Invalida seg', 'tipo': 'REFERIDOS', 'objetivo': 'Captar', 'meta': 2,
            'incentivos': '100 puntos', 'condiciones': 'Socios activos',
            'inicio': str(hoy), 'fin': str(hoy + timedelta(days=5)), 'segmentacion': {'OTRO': ['X']},
        }, 400)
        creada = self.post('campanas/', {
            'nombre': 'Campaña Joven Loja', 'tipo': 'REFERIDOS', 'objetivo': 'Captar jóvenes', 'meta': 2,
            'incentivos': '100 puntos', 'condiciones': 'Socios de Loja',
            'inicio': str(hoy), 'fin': str(hoy + timedelta(days=10)),
            'segmentacion': {'RANGO_EDAD': [18, 45], 'AGENCIA': ['Loja']},
        }, 201)
        cid = creada['id']
        self.assertEqual(creada['estado'], 'BORRADOR')
        self.assertEqual(creada['indicadores'], {
            'participantes': 0, 'referidos': 0, 'conversiones': 0,
            'tasa_conversion': 0, 'puntos_otorgados': 0, 'avance_meta': 0,
        })
        self.como(self.marketing)
        prev = self.post(f'campanas/{cid}/previsualizar/')
        self.assertEqual(prev['socios_elegibles'], 1)
        editada = self.c.put(BASE + f'campanas/{cid}/', {'meta': 4}, format='json')
        self.assertEqual(editada.status_code, 200)
        self.assertEqual(editada.json()['meta'], 4)
        self.post(f'campanas/{cid}/estado/', {'estado': 'ACTIVA', 'motivo': 'Lanzamiento'})
        self.assertEqual(self.c.put(BASE + f'campanas/{cid}/', {'incentivos': '500 puntos'}, format='json').status_code, 400)
        self.assertEqual(self.c.put(BASE + f'campanas/{cid}/', {'condiciones': 'Socios activos de Loja'}, format='json').status_code, 200)

        self.como(self.usuario)
        self.post('referidos/', {
            'codigo': self.codigo.valor, 'cedula': '9666666661', 'nombre': 'Prospecto Uno',
            'correo': 'p1@example.com', 'producto': 'Ahorro', 'campana': cid, 'acepta_terminos': True,
        }, 201)
        r = m.Referido.objects.get(campana_id=cid)
        n.confirmar_referido(n.huella('contacto:' + r.prospecto.token_nonce))
        self.como(self.marketing)
        self.post(f'referidos/{r.pk}/estado/', {'estado': 'EN_SEGUIMIENTO', 'motivo': 'Llamada'})
        self.post(f'referidos/{r.pk}/estado/', {'estado': 'CONVERTIDO', 'motivo': 'Apertura', 'tipo_evento': 'APERTURA_CUENTA'})
        self.assertEqual(self.c.put(BASE + f'campanas/{cid}/', {'objetivo': 'Captar socios en Loja'}, format='json').status_code, 200)
        self.assertEqual(n.saldo(self.socio), 100)
        listado = [c for c in self.c.get(BASE + 'campanas/').json()['resultados'] if c['id'] == cid][0]
        self.assertEqual(listado['indicadores'], {
            'participantes': 1, 'referidos': 1, 'conversiones': 1,
            'tasa_conversion': 100.0, 'puntos_otorgados': 100, 'avance_meta': 25.0,
        })
        self.post(f'campanas/{cid}/estado/', {'estado': 'SUSPENDIDA', 'motivo': 'Pausa'})
        self.post(f'campanas/{cid}/estado/', {'estado': 'FINALIZADA', 'motivo': 'Cierre'})
        self.como(self.usuario)
        self.post('referidos/', {
            'codigo': self.codigo.valor, 'cedula': '9666666662', 'nombre': 'Prospecto Dos',
            'correo': 'p2@example.com', 'producto': 'Ahorro', 'campana': cid, 'acepta_terminos': True,
        }, 400)
        eventos = list(HistorialEstado.objects.filter(entidad='campana', registro_id=cid).order_by('pk'))
        self.assertGreaterEqual(len(eventos), 5)
        self.assertTrue(any('Modificación de campaña' in e.motivo for e in eventos))

    def test_gamificacion_niveles_insignias_notificaciones_y_ranking_periodo(self):
        self.como(self.admin)
        self.post('niveles/', {'nombre': 'Bronce', 'umbral_puntos': 0}, 201)
        self.post('niveles/', {'nombre': 'Plata', 'umbral_puntos': 100}, 201)
        self.post('insignias/', {'nombre': 'Primer Referido', 'criterio': 'CONVERSION', 'umbral': 1, 'icono': 'estrella'}, 201)
        self.post('insignias/', {'nombre': 'Centenario', 'criterio': 'PUNTOS', 'umbral': 100, 'icono': 'medalla'}, 201)
        self.como(self.usuario)
        inicial = self.c.get(BASE + 'puntos/').json()
        self.assertEqual((inicial['saldo'], inicial['nivel'], inicial['insignias'], inicial['movimientos']), (0, 'Bronce', [], []))
        mov = self.credito(501)
        despues = self.c.get(BASE + 'puntos/').json()
        self.assertEqual(despues['saldo'], 100)
        self.assertEqual(despues['nivel'], 'Plata')
        self.assertCountEqual([i['nombre'] for i in despues['insignias']], ['Primer Referido', 'Centenario'])
        self.assertEqual(despues['movimientos'][0]['origen_tipo'], 'CONVERSION')
        self.credito(502)
        self.assertEqual(m.SocioInsignia.objects.filter(socio=self.socio).count(), 2)
        self.assertTrue(m.Notificacion.objects.filter(destinatario=self.usuario, evento='LOGRO').exists())
        ayer = (timezone.localdate() - timedelta(days=2)).isoformat()
        self.assertIsNone(self.c.get(BASE + 'ranking/', {'hasta': ayer}).json()['mi_posicion'])
        self.como(self.admin)
        self.post(f'movimientos/{mov.pk}/revertir/', {'motivo': ''}, 400)

    def test_formacion_verificacion_invalida_frecuencia_y_gestion_talleres(self):
        self.addCleanup(cache.clear)
        cache.clear()
        publico = APIClient()
        ruta_invalida = '/api/plataforma/certificados/verificar/00000000000000000000000000000000/'
        r = publico.get(ruta_invalida)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json(), {'valido': False, 'titulo': None, 'emitido_en': None, 'codigo': None})
        for _ in range(59):
            self.assertEqual(publico.get(ruta_invalida).status_code, 200)
        self.assertEqual(publico.get(ruta_invalida).status_code, 429)

        self.como(self.rse)
        self.post('talleres/', {
            'titulo': 'Taller inválido', 'fecha': (timezone.now() + timedelta(days=2)).isoformat(),
            'cupo': 0, 'modalidad': 'PRESENCIAL', 'lugar': 'Agencia Central', 'duracion': 2,
        }, 400)
        taller = self.post('talleres/', {
            'titulo': 'Taller de Presupuesto', 'fecha': (timezone.now() + timedelta(days=2)).isoformat(),
            'cupo': 2, 'modalidad': 'PRESENCIAL', 'lugar': 'Agencia Central', 'duracion': 2,
        }, 201)
        editado = self.c.put(BASE + f'talleres/{taller["id"]}/', {'lugar': 'Salón Cooperativo', 'cupo': 3}, format='json')
        self.assertEqual(editado.status_code, 200)
        self.assertEqual(editado.json()['lugar'], 'Salón Cooperativo')
        self.como(self.usuario)
        insc = self.post(f'talleres/{taller["id"]}/inscribir/', {}, 201)
        self.como(self.rse)
        part = self.c.get(BASE + f'talleres/{taller["id"]}/participantes/').json()['resultados']
        self.assertEqual(len(part), 1)
        self.assertEqual((part[0]['id'], part[0]['asistio']), (insc['id'], False))

    def test_sorteos_configuracion_suplentes_notificacion_y_evidencia_restringida(self):
        c = self.campana(estado='ACTIVA')
        self.como(self.usuario)
        self.post('sorteos/', {'nombre': 'No autorizado'}, 403)
        self.como(self.marketing)
        self.post('sorteos/', {
            'campana': c.pk, 'nombre': 'Invalido', 'premio': 'Bono',
            'fecha': (timezone.now() + timedelta(days=1)).isoformat(),
            'condiciones': 'Activos', 'num_ganadores': 0, 'num_suplentes': 0, 'origen': 'CONVERSION',
        }, 400)
        sorteo = self.post('sorteos/', {
            'campana': c.pk, 'nombre': 'Sorteo Anual', 'premio': 'Tablet Educativa',
            'fecha': (timezone.now() + timedelta(days=1)).isoformat(),
            'condiciones': 'Reclamar con cédula en 15 días', 'num_ganadores': 1, 'num_suplentes': 1, 'origen': 'CONVERSION',
        }, 201)
        sid = sorteo['id']
        self.como(self.usuario)
        self.assertEqual(self.c.get(BASE + 'sorteos/').json()['resultados'], [])
        self.como(self.marketing)
        self.post(f'sorteos/{sid}/estado/', {'estado': 'ACTIVO', 'motivo': 'Apertura'})
        p1 = m.Prospecto.objects.create(nombre='P1', contacto='s1@example.com', producto='Ahorro')
        ref1 = m.Referido.objects.create(codigo=self.codigo, prospecto=p1, campana=c, estado='EN_SEGUIMIENTO')
        self.post(f'referidos/{ref1.pk}/estado/', {'estado': 'CONVERTIDO', 'motivo': 'Ok', 'tipo_evento': 'APERTURA_CUENTA'})
        c2 = m.CodigoReferido.generar_para(self.socio2)
        p2 = m.Prospecto.objects.create(nombre='P2', contacto='s2@example.com', producto='Ahorro')
        ref2 = m.Referido.objects.create(codigo=c2, prospecto=p2, campana=c, estado='EN_SEGUIMIENTO')
        self.post(f'referidos/{ref2.pk}/estado/', {'estado': 'CONVERTIDO', 'motivo': 'Ok', 'tipo_evento': 'APERTURA_CUENTA'})
        self.assertEqual(m.ParticipacionSorteo.objects.filter(sorteo_id=sid).count(), 2)
        self.como(self.usuario)
        previo = self.c.get(BASE + 'sorteos/').json()['resultados'][0]
        self.assertEqual(previo['ganadores'], [])
        self.assertNotIn('evidencia', previo)

        m.Sorteo.objects.filter(pk=sid).update(fecha=timezone.now() - timedelta(minutes=5))
        self.como(self.marketing)
        ejecutado = self.post(f'sorteos/{sid}/ejecutar/')
        self.assertEqual(len(ejecutado['ganadores']), 2)
        self.assertEqual([g['suplente'] for g in ejecutado['ganadores']], [False, True])
        self.assertEqual(len(ejecutado['evidencia']['elegibles']), 2)
        self.assertEqual(len(ejecutado['evidencia']['sha256']), 64)
        aviso = m.Notificacion.objects.filter(evento='SORTEO').first()
        self.assertIsNotNone(aviso)
        self.assertIn('Tablet Educativa', aviso.mensaje)
        self.assertIn('Reclamar con cédula', aviso.mensaje)
        self.como(self.usuario)
        publicado = self.c.get(BASE + 'sorteos/').json()['resultados'][0]
        self.assertEqual(len(publicado['ganadores']), 2)
        self.assertNotIn('evidencia', publicado)

    def test_recompensas_edicion_desactivacion_y_filtros_de_canjes(self):
        self.como(self.marketing)
        b = self.post('beneficios/', {
            'nombre': 'Agenda', 'descripcion': 'Agenda anual', 'costo_puntos': 50,
            'stock': 2, 'condiciones': 'Retiro presencial', 'desde': str(timezone.localdate()),
            'hasta': None, 'activo': True, 'convenio': None,
        }, 201)
        bid = b['id']
        self.assertEqual(self.c.put(BASE + f'beneficios/{bid}/', {'activo': False}, format='json').status_code, 200)
        self.como(self.usuario)
        self.assertEqual(self.c.get(BASE + 'beneficios/').json()['resultados'], [])
        self.como(self.marketing)
        self.assertEqual(self.c.put(BASE + f'beneficios/{bid}/', {'activo': True, 'costo_puntos': 40}, format='json').status_code, 200)
        self.credito(801)
        self.como(self.usuario)
        disponibles = self.c.get(BASE + 'beneficios/').json()['resultados']
        self.assertEqual(len(disponibles), 1)
        canje = self.post(f'beneficios/{bid}/canjear/', {'clave': str(uuid4()), 'acepta_condiciones': True}, 201)
        self.assertEqual(len(self.c.get(BASE + 'canjes/', {'estado': 'PENDIENTE'}).json()['resultados']), 1)
        self.assertEqual(self.c.get(BASE + 'canjes/', {'estado': 'ENTREGADA'}).json()['resultados'], [])
        self.assertTrue(HistorialEstado.objects.filter(entidad='canje', registro_id=canje['id'], estado_nuevo='PENDIENTE').exists())

    def test_contenidos_aprobador_no_designado_y_notificaciones_envios_filtrados(self):
        from apps.plataforma.contenidos import guardar_contenido
        otro_gestor = crear_usuario(8199, 'Gestor de contenidos')
        c = guardar_contenido(self.gestor, {
            'titulo': 'Comunicado oficial', 'cuerpo': 'Contenido institucional', 'categoria': 'Institucional',
            'tipo': 'ANUNCIO', 'desde': timezone.localdate(), 'requiere_aprobacion': True, 'aprobador': self.gestor,
        })
        self.como(otro_gestor)
        self.assertEqual(self.c.post(f'/api/plataforma/contenidos/{c.pk}/aprobar/').status_code, 403)
        self.como(self.gestor)
        self.assertGreaterEqual(len(self.c.get('/api/plataforma/contenidos/aprobadores/').json()), 2)

        self.como(self.admin)
        plantilla = self.post('plantillas/', {
            'evento': 'CANJE', 'canal': 'INTERNA', 'titulo': 'Actualización de canje', 'cuerpo': 'Estado: {mensaje}',
        }, 201)
        self.assertEqual(self.c.put(BASE + f'plantillas/{plantilla["id"]}/', {'titulo': 'Aviso de canje'}, format='json').status_code, 200)
        n.notificar(self.usuario, 'CANJE', 'aprobada')
        from apps.plataforma.notificaciones import procesar_uno
        while procesar_uno():
            pass
        envios_internos = self.c.get(BASE + 'envios/', {'estado': 'ENVIADA', 'canal': 'INTERNA'}).json()['resultados']
        self.assertTrue(any(e['evento'] == 'CANJE' for e in envios_internos))
        self.assertTrue(all('•••@' in e['destinatario'] for e in envios_internos))

    def test_juegos_tipos_validacion_y_reto_vencido_no_acredita(self):
        self.como(self.gestor)
        self.post('juegos/', {
            'nombre': 'Sin instrucciones', 'tipo': 'TRIVIA', 'max_intentos': 2,
            'instrucciones': '', 'preguntas': BANCO, 'nota_minima': 60,
        }, 400)
        for tipo in ('TRIVIA', 'VERDADERO_FALSO', 'EMPAREJAR'):
            j = self.post('juegos/', {
                'nombre': f'Juego {tipo}', 'tipo': tipo, 'max_intentos': 2,
                'instrucciones': 'Sigue las indicaciones', 'preguntas': BANCO, 'nota_minima': 60,
            }, 201)
            self.assertEqual(self.c.put(BASE + f'juegos/{j["id"]}/', {'max_intentos': 3}, format='json').status_code, 200)
            self.post(f'juegos/{j["id"]}/estado/', {'estado': 'ACTIVO', 'motivo': 'Disponible'})
            if tipo == 'EMPAREJAR':
                juego_id = j['id']
        ayer = timezone.localdate() - timedelta(days=1)
        reto_vencido = m.Reto.objects.create(objetivo='Reto pasado', meta=1, inicio=ayer, fin=ayer, actividad='JUEGO')
        self.como(self.usuario)
        self.assertEqual(self.c.get(BASE + 'retos/').json()['resultados'], [])
        partida = self.post(f'juegos/{juego_id}/iniciar/', {}, 201)
        self.assertEqual(partida['tipo'], 'EMPAREJAR')
        fin = self.post(f'partidas/{partida["id"]}/finalizar/', {'respuestas': [0]})
        self.assertEqual(float(fin['puntuacion']), 100.0)
        self.assertFalse(m.ProgresoReto.objects.filter(reto=reto_vencido, socio=self.socio).exists())
        act = self.c.get(BASE + 'mis-actividades/').json()['partidas']
        self.assertEqual(len(act), 1)
        self.assertEqual(act[0]['juego'], 'Juego EMPAREJAR')

    def test_bienestar_edicion_consulta_y_ausencia_de_campos_clinicos(self):
        self.como(self.gestor)
        self.post('convenios/', {
            'entidad': 'Clínica', 'tipo': 'SALUD', 'descripcion': 'Atención',
            'beneficio': '20 %', 'condiciones': 'Socio activo', 'vigencia': str(timezone.localdate()),
            'diagnostico': 'No permitido',
        }, 400)
        conv = self.post('convenios/', {
            'entidad': 'Centro Óptico', 'tipo': 'SALUD', 'descripcion': 'Salud visual',
            'beneficio': '15 % descuento', 'condiciones': 'Presentar certificado', 'vigencia': str(timezone.localdate() + timedelta(days=30)),
        }, 201)
        campos = [c['nombre'] for c in self.c.get(BASE + 'convenios/').json()['campos']]
        self.assertEqual(set(campos), {'entidad', 'tipo', 'descripcion', 'beneficio', 'condiciones', 'vigencia'})
        editado = self.c.put(BASE + f'convenios/{conv["id"]}/', {'beneficio': '25 % descuento'}, format='json')
        self.assertEqual(editado.status_code, 200)
        self.como(self.usuario)
        visibles = self.c.get(BASE + 'convenios/').json()['resultados']
        self.assertEqual(len(visibles), 1)
        self.assertEqual(visibles[0]['beneficio'], '25 % descuento')
