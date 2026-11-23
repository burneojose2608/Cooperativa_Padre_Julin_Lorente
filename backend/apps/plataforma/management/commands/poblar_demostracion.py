"""Carga aditiva de catálogos y actividad sintética para la demostración local."""

from datetime import date, timedelta
from unittest.mock import patch

from django.core.management.base import BaseCommand, CommandError
from django.db import connection, transaction
from django.utils import timezone

from apps.plataforma import models as m, negocio as n
from apps.usuarios.models import Socio, Usuario
from apps.usuarios.repositories import RolRepository
from apps.usuarios.services.codigos_socio import ServicioSocios


PREFIJO = "Demo · "


class Command(BaseCommand):
    help = "Añade registros sintéticos de demostración sin modificar catálogos existentes."

    def add_arguments(self, parser):
        parser.add_argument("--base", required=True, help="Nombre exacto de la base local autorizada.")

    @transaction.atomic
    def handle(self, *args, **options):
        config = connection.settings_dict
        if config["NAME"] != options["base"] or config["HOST"] not in ("localhost", "127.0.0.1", "::1", ""):
            raise CommandError("La base activa debe coincidir con el nombre indicado y ser local.")

        hoy = timezone.localdate()
        fin = hoy + timedelta(days=90)
        creados = []

        def obtener(modelo, clave, nombre, **datos):
            objeto, nuevo = modelo.objects.get_or_create(**{clave: PREFIJO + nombre}, defaults=datos)
            if nuevo:
                creados.append(modelo.__name__)
            return objeto

        cuenta, nueva = Usuario.objects.get_or_create(username="pjl_catalogo_demo", defaults={
            "cedula": "9900000151", "nombre": "Equipo", "apellido": "Demostración",
            "correo": "catalogo@pjl.example.test", "telefono": "0900000151",
            "password": "!", "fecha_nacimiento": date(1995, 1, 1),
        })
        if cuenta.correo != "catalogo@pjl.example.test" or cuenta.has_usable_password():
            raise CommandError("El usuario reservado para la demostración pertenece a otra cuenta.")
        if nueva:
            RolRepository.asignar(cuenta, RolRepository.obtener_por_nombre("Socio"))
        socio, _ = Socio.objects.get_or_create(usuario=cuenta, defaults={
            "codigo_socio": ServicioSocios.generar_codigo_socio(), "validado_en": timezone.now(),
            "alias": "Equipo demo",
        })

        for titulo, categoria, cuerpo in [
            ("Cinco pasos para organizar tu presupuesto", "Educación financiera",
             "Anota tus ingresos, separa los gastos fijos y pon un límite a los gastos variables. Revisa el resultado al final de cada mes."),
            ("Cómo prepararte para un imprevisto", "Bienestar",
             "Define una meta para tu fondo de emergencia y empieza con aportes pequeños que puedas sostener."),
            ("Agenda de formación cooperativa", "Comunidad",
             "Revisa el taller de metas de ahorro y la capacitación de presupuesto disponibles en esta demostración."),
        ]:
            obtener(m.ContenidoInstitucional, "titulo", titulo, autor=cuenta, tipo="NOTICIA",
                    categoria=categoria, cuerpo=cuerpo, estado="PUBLICADO", desde=hoy, hasta=fin)

        campana = obtener(m.Campana, "nombre", "Ahorra con propósito", creado_por=cuenta, tipo="REFERIDOS",
                          objetivo="Promover hábitos de ahorro", meta=20, incentivos="Puntos por participación validada",
                          condiciones="Actividad de demostración para socios activos.", inicio=hoy, fin=fin, estado="ACTIVA")
        curso = obtener(m.Capacitacion, "titulo", "Presupuesto personal", modalidad="VIRTUAL", estado="PUBLICADA",
                        descripcion="Ordena tus gastos y prepara una meta mensual de ahorro.", duracion=2,
                        requisitos="Ser socio activo.")
        pregunta = {"enunciado": "¿Qué conviene hacer primero al armar un presupuesto?",
                    "opciones": ["Anotar ingresos y gastos", "Comprar antes de planificar"], "correcta": 0}
        unidad, _ = m.ModuloCapacitacion.objects.get_or_create(capacitacion=curso, orden=1,
                                                              defaults={"titulo": "Ingresos y gastos"})
        m.Evaluacion.objects.get_or_create(capacitacion=curso, defaults={
            "nota_minima": 60, "max_intentos": 3, "preguntas": [pregunta],
        })
        obtener(m.Taller, "titulo", "Mi meta de ahorro", fecha=timezone.now()+timedelta(days=14),
                cupo=25, modalidad="VIRTUAL", lugar="Sala virtual de demostración", duracion=1)
        obtener(m.Juego, "nombre", "Trivia de ahorro", tipo="TRIVIA", estado="ACTIVO", max_intentos=3,
                instrucciones="Elige la mejor respuesta para organizar tus finanzas.", preguntas=[pregunta])
        obtener(m.Reto, "objetivo", "Completa una capacitación", meta=1, inicio=hoy, fin=fin, actividad="CAPACITACION")
        convenio = obtener(m.Convenio, "entidad", "Biblioteca de bienestar", tipo="EDUCACION", vigencia=fin,
                          descripcion="Convenio de demostración con material educativo.", beneficio="Guías de finanzas",
                          condiciones="Disponible para la demostración.")
        obtener(m.Beneficio, "nombre", "Guía de ahorro", convenio=convenio, costo_puntos=40, stock=20,
                descripcion="Material educativo canjeable con puntos de demostración.",
                condiciones="Canje de prueba.", desde=hoy, hasta=fin)
        obtener(m.Sorteo, "nombre", "Sorteo de educación financiera", campana=campana, premio="Kit educativo",
                condiciones="Participa al aprobar una capacitación.", origen="CAPACITACION",
                fecha=timezone.now()+timedelta(days=30), estado="ACTIVO")
        obtener(m.Insignia, "nombre", "Primer aprendizaje", criterio="CAPACITACION", umbral=1)
        m.Nivel.objects.get_or_create(umbral_puntos=100, defaults={"nombre": PREFIJO + "Aprendiz"})
        for actividad in m.ReglaPuntos.ACTIVIDADES:
            if not m.ReglaPuntos.objects.filter(tipo_actividad=actividad).exists():
                m.ReglaPuntos.objects.create(tipo_actividad=actividad, puntos=50, limite_periodo=5,
                                              vigente_desde=hoy, version="demostracion-1")
        m.Publicacion.objects.get_or_create(usuario=cuenta, texto=PREFIJO + "¿Qué meta de ahorro te gustaría alcanzar?")
        m.CodigoReferido.generar_para(socio)

        # Los datos históricos de demostración no generan envíos reales ni pendientes.
        if not m.Inscripcion.objects.filter(socio=socio, capacitacion=curso).exists():
            with patch.object(n, "notificar"):
                inscripcion = n.inscribir(cuenta, curso.pk, acepta_requisitos=True)
                m.Progreso.objects.create(inscripcion=inscripcion, unidad=unidad, porcentaje=100)
                n.evaluar(cuenta, curso.pk, [0])

        self.stdout.write(self.style.SUCCESS(f"Demostración disponible. Nuevos registros de catálogo: {len(creados)}."))
