from rest_framework import serializers


class SolicitarRecuperacionSerializer(serializers.Serializer):
    identificador = serializers.CharField(max_length=254)  # correo, cédula o usuario


class RestablecerClaveSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=200)
    clave = serializers.CharField(max_length=128, trim_whitespace=False)
