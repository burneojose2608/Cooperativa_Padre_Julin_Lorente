"""Validan el FORMATO de lo que llega. Las reglas de negocio viven en services/."""
import re
from datetime import date

from rest_framework import serializers


class RegistroSerializer(serializers.Serializer):
    cedula = serializers.CharField(max_length=10)
    nombre = serializers.CharField(max_length=100)
    apellido = serializers.CharField(max_length=100)
    correo = serializers.EmailField(max_length=254)
    username = serializers.CharField(min_length=4, max_length=50)
    telefono = serializers.CharField(max_length=15)
    fecha_nacimiento = serializers.DateField()
    clave = serializers.CharField(write_only=True, max_length=128, trim_whitespace=False)

    def validate_username(self, valor):
        if not re.fullmatch(r"[A-Za-z0-9_.]+", valor):
            raise serializers.ValidationError("Solo letras, números, punto y guion bajo.")
        return valor

    def validate_telefono(self, valor):
        if not re.fullmatch(r"[0-9+]{7,15}", valor):
            raise serializers.ValidationError("Teléfono inválido: use solo números (7 a 15 dígitos).")
        return valor

    def validate_fecha_nacimiento(self, valor):
        if valor > date.today() or valor.year < 1900:
            raise serializers.ValidationError("Fecha de nacimiento inválida.")
        return valor


class LoginSerializer(serializers.Serializer):
    identificador = serializers.CharField(max_length=254)  # cédula, correo o username
    clave = serializers.CharField(max_length=128, trim_whitespace=False)
