from rest_framework import serializers
from .auth_serializers import RegistroSerializer


class EstrictoSerializer(serializers.Serializer):
    def to_internal_value(self, data):
        desconocidos = set(data) - set(self.fields)
        if desconocidos:
            raise serializers.ValidationError({c: "Campo no permitido." for c in desconocidos})
        return super().to_internal_value(data)


class ContactoSerializer(EstrictoSerializer):
    correo = serializers.EmailField(max_length=254, required=False)
    telefono = serializers.RegexField(r"^[0-9+]{7,15}$", max_length=15, required=False)
    foto = serializers.FileField(required=False, max_length=255)


class CrearInternoSerializer(RegistroSerializer):
    rol = serializers.CharField(max_length=60)
    acepta_terminos = None


class CambiarClaveSerializer(EstrictoSerializer):
    actual = serializers.CharField(max_length=128, trim_whitespace=False)
    nueva = serializers.CharField(max_length=128, trim_whitespace=False)


class EstadoSerializer(EstrictoSerializer):
    estado = serializers.ChoiceField(choices=["ACTIVA", "SUSPENDIDA", "DESACTIVADA"])
    motivo = serializers.CharField(max_length=1000)


class RolesSerializer(EstrictoSerializer):
    roles = serializers.ListField(child=serializers.IntegerField(min_value=1), allow_empty=True)


class PermisosSerializer(EstrictoSerializer):
    permisos = serializers.ListField(child=serializers.IntegerField(min_value=1), allow_empty=True)
