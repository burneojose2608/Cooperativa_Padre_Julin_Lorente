from concurrent.futures import ThreadPoolExecutor
from threading import Barrier
from uuid import uuid4
from django.db import connection
from django.test import TransactionTestCase
from django.utils import timezone
from rest_framework.exceptions import ValidationError
from apps.usuarios.services.codigos_socio import ServicioSocios
from apps.plataforma import models as m, negocio as n
from .test_sprint2 import crear_usuario
from .test_concurrencia import en_conexion


class ConcurrenciaAlcanceTests(TransactionTestCase):
    def setUp(self):
        self.assertTrue(connection.settings_dict['NAME'].startswith('test_'))
        self.u=crear_usuario(9201,'Socio')
        self.s=ServicioSocios.crear_socio_validado(self.u)
        m.ReglaPuntos.objects.create(tipo_actividad='CONVERSION_REFERIDO',puntos=100,limite_periodo=10,
                                     periodo='DIA',vigente_desde=timezone.localdate(),version='prueba')

    def tearDown(self):
        if connection.settings_dict['NAME'].startswith('test_'):
            with connection.cursor() as c:
                c.execute('TRUNCATE usuario RESTART IDENTITY CASCADE')
            m.ReglaPuntos.objects.all().delete()

    def paralelas(self,funcion):
        barrera=Barrier(2)
        def ejecutar():
            barrera.wait(timeout=10)
            try: return funcion()
            except ValidationError: return 'RECHAZADA'
        with ThreadPoolExecutor(max_workers=2) as e:
            futuros=[e.submit(en_conexion,ejecutar) for _ in range(2)]
            return [f.result(timeout=20) for f in futuros]

    def test_evento_repetido_en_dos_conexiones_acredita_una_vez(self):
        resultados=self.paralelas(lambda:n.acreditar(self.s,'CONVERSION',1).pk)
        self.assertEqual(resultados[0],resultados[1])
        self.assertEqual(n.saldo(self.s),100)
        self.assertEqual(m.ActividadValidada.objects.count(),1)

    def test_dos_canjes_no_sobrevenden_ni_dejan_saldo_negativo(self):
        n.acreditar(self.s,'CONVERSION',1)
        b=m.Beneficio.objects.create(nombre='Libro',costo_puntos=70,stock=1,descripcion='Libro',condiciones='Retiro',desde=timezone.localdate())
        resultados=self.paralelas(lambda:n.solicitar_canje(self.u,b.pk,uuid4()).pk)
        self.assertEqual(resultados.count('RECHAZADA'),1)
        self.assertEqual(m.Canje.objects.count(),1)
        self.assertEqual(n.saldo(self.s),30)
        b.refresh_from_db();self.assertEqual(b.stock,0)

    def test_dos_partidas_respetan_maximo_de_un_intento(self):
        j=m.Juego.objects.create(nombre='Juego',tipo='TRIVIA',estado='ACTIVO',max_intentos=1,instrucciones='Responde',
                                preguntas=[{'enunciado':'Ahorro','opciones':['Sí','No'],'correcta':0}])
        resultados=self.paralelas(lambda:n.iniciar_partida(self.u,j.pk).pk)
        self.assertEqual(resultados.count('RECHAZADA'),1)
        self.assertEqual(m.Partida.objects.count(),1)
