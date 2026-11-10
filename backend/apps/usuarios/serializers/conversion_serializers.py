from rest_framework import serializers


class ConfirmarSocioSerializer(serializers.Serializer):
    confirmar_socio_activo = serializers.BooleanField()

    def validate(self, datos):
        if set(self.initial_data) != {"confirmar_socio_activo"}:
            raise serializers.ValidationError("Solo se acepta la confirmación de socio activo.")
        if self.initial_data["confirmar_socio_activo"] is not True:
            raise serializers.ValidationError({"confirmar_socio_activo": "Debes confirmar expresamente la validación."})
        return datos


class CuentaGeneralSerializer(serializers.Serializer):
    id = serializers.IntegerField(source="id_usuario", read_only=True)
    nombre = serializers.CharField(read_only=True)
    apellido = serializers.CharField(read_only=True)
    username = serializers.CharField(read_only=True)
    cedula = serializers.CharField(read_only=True)
    estado = serializers.CharField(read_only=True)
    estado_padron = serializers.SerializerMethodField()

    def get_estado_padron(self, cuenta):
        if cuenta.activo_padron is None:
            return "no_encontrado"
        return "activo" if cuenta.activo_padron else "inactivo"
