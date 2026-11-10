from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.usuarios.permissions import tiene_rol
from apps.usuarios.repositories import UsuarioRepository
from apps.usuarios.serializers.conversion_serializers import ConfirmarSocioSerializer, CuentaGeneralSerializer
from apps.usuarios.services.conversion_socio_service import comprobar_conversion_habilitada, convertir_cuenta_a_socio


class CuentasGeneralesView(APIView):
    permission_classes = [IsAuthenticated, tiene_rol("Administrador")]

    def get(self, request):
        comprobar_conversion_habilitada()
        cuentas = UsuarioRepository.listar_cuentas_generales(request.query_params.get("q", "").strip()[:100])
        paginador = PageNumberPagination()
        paginador.page_size = 20
        pagina = paginador.paginate_queryset(cuentas, request)
        return paginador.get_paginated_response(CuentaGeneralSerializer(pagina, many=True).data)


class ConvertirSocioView(APIView):
    permission_classes = [IsAuthenticated, tiene_rol("Administrador")]

    def post(self, request, id_usuario):
        entrada = ConfirmarSocioSerializer(data=request.data)
        entrada.is_valid(raise_exception=True)
        socio, convertido = convertir_cuenta_a_socio(
            administrador=request.user, id_usuario=id_usuario,
            **entrada.validated_data, ip=request.META.get("REMOTE_ADDR"))
        return Response({"id": id_usuario, "convertido": convertido,
                         "codigo_socio": socio.codigo_socio, "validado_en": socio.validado_en,
                         "mensaje": "Cuenta validada y convertida a socio." if convertido else "La cuenta ya es socia."})
