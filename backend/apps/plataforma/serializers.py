from rest_framework import serializers
from apps.usuarios.serializers.gestion_serializers import EstrictoSerializer
from apps.usuarios.models import Usuario
from .models import ReglaPuntos
from .notificaciones import EVENTOS, CANALES, EVENTOS_OBLIGATORIOS


class ReglaSerializer(EstrictoSerializer):
    tipo_actividad = serializers.ChoiceField(choices=ReglaPuntos.ACTIVIDADES)
    puntos = serializers.IntegerField(min_value=1, max_value=1000000)
    limite_periodo = serializers.IntegerField(min_value=1, max_value=1000000)
    periodo = serializers.ChoiceField(choices=["DIA", "MES", "ANIO"])
    vigente_desde = serializers.DateField()
    vigente_hasta = serializers.DateField(allow_null=True, required=False, default=None)

    def validate(self, datos):
        if datos["vigente_hasta"] and datos["vigente_hasta"] < datos["vigente_desde"]:
            raise serializers.ValidationError({"vigente_hasta": "La fecha de fin debe ser posterior al inicio."})
        return datos


class ContenidoSerializer(EstrictoSerializer):
    titulo = serializers.CharField(max_length=200)
    cuerpo = serializers.CharField(max_length=100000)
    categoria = serializers.CharField(max_length=100)
    tipo = serializers.ChoiceField(choices=["NOTICIA", "ANUNCIO", "MULTIMEDIA"])
    desde = serializers.DateField(allow_null=True, required=False)
    hasta = serializers.DateField(allow_null=True, required=False)
    requiere_aprobacion = serializers.BooleanField(required=False)
    aprobador = serializers.PrimaryKeyRelatedField(queryset=Usuario.objects.filter(
        estado='ACTIVA', roles_asignados__rol__nombre='Gestor de contenidos').distinct(), allow_null=True, required=False)

    def validate(self, datos):
        if datos.get("desde") and datos.get("hasta") and datos["hasta"] < datos["desde"]:
            raise serializers.ValidationError({"hasta": "La fecha de fin debe ser posterior al inicio."})
        if datos.get('requiere_aprobacion') and not datos.get('aprobador'):
            raise serializers.ValidationError({'aprobador': 'Selecciona el responsable de aprobación.'})
        return datos


class MaterialSerializer(EstrictoSerializer):
    titulo = serializers.CharField(max_length=200)
    categoria = serializers.CharField(max_length=100)
    archivo = serializers.FileField(required=False)
    contenido = serializers.IntegerField(min_value=1, allow_null=True, required=False)
    modulos = serializers.JSONField(required=False)

    def validate_modulos(self, valor):
        if not isinstance(valor, list) or any(type(v) is not int or v <= 0 for v in valor):
            raise serializers.ValidationError("Indica una lista de identificadores de módulos.")
        return valor


class PreferenciaSerializer(EstrictoSerializer):
    evento = serializers.ChoiceField(choices=list(EVENTOS))
    canal = serializers.ChoiceField(choices=CANALES)
    habilitada = serializers.BooleanField()

    def validate(self, datos):
        if datos['evento'] in EVENTOS_OBLIGATORIOS and not datos['habilitada']:
            raise serializers.ValidationError('Esta comunicación de seguridad es obligatoria.')
        return datos


class RetirarSerializer(EstrictoSerializer):
    motivo = serializers.CharField(max_length=1000)
