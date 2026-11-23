"""Añade contratos y el estado de revisión a los specs obtenidos del backlog."""
from pathlib import Path
import ast
import csv
import json

ROOT=Path(__file__).resolve().parents[1]
SPECS=ROOT/'specs'
MODULOS={
 '001-usuarios':('usuario, socio, rol, usuario_rol','/api/auth/yo/; /api/administracion/','backend/apps/usuarios/services/gestion_cuentas_service.py','frontend/src/panel/sprint2/Usuarios.jsx','Identidad inmutable desde el perfil; gestión de contacto, estado y roles con auditoría.','Sprint 1 y Sprint 2'),
 '002-autenticacion':('sesion, token_recuperacion, auditoria','/api/auth/','backend/apps/usuarios/services/sesiones_service.py','frontend/src/context/AuthContext.jsx','Access y refresh ligados a sesión revocable; roles y permisos consultados en cada solicitud.','Sprint 1 y Sprint 2'),
 '003-referidos':('codigo_referido, prospecto, referido, conversion, historial_estado','/api/plataforma/negocio/referidos/; /api/plataforma/invitaciones/{codigo}/referir/; /api/plataforma/referidos/confirmar/{token}/','backend/apps/plataforma/negocio.py','frontend/src/panel/negocio/Modulos.jsx','Código persistente del socio, consentimiento versionado, confirmación de un solo uso, primer contacto, ciclo controlado y conversión única. Los datos se enmascaran para el socio.','Sprint 2 y Sprint 3'),
 '004-campanas':('campana, gasto_campana, socio.segmento','/api/plataforma/negocio/campanas/; /api/plataforma/negocio/gastos/; /api/plataforma/negocio/segmentos/{socio}/','backend/apps/plataforma/api_negocio.py','frontend/src/panel/negocio/Modulos.jsx','Campañas en borrador; estado y vigencia controlan elegibilidad. Segmentación por rango de edad y atributos comerciales confirmados. Tras activar, la edición conserva incentivos y público.','Sprint 3 y Sprint 4'),
 '005-gamificacion':('actividad_validada, regla_puntos, movimiento_puntos, nivel, insignia, socio_insignia','/api/plataforma/negocio/puntos/; /api/plataforma/negocio/niveles/; /api/plataforma/negocio/insignias/; /api/plataforma/negocio/ranking/; /api/plataforma/negocio/movimientos/{id}/revertir/','backend/apps/plataforma/negocio.py','frontend/src/panel/negocio/Modulos.jsx','Libro inmutable. Disponible = acreditaciones + liberaciones - reservas - descuentos - reversos. Los puntos de logro excluyen canjes. Un origen se valida y acredita una sola vez, con límite por período. Reverso justificado sin saldo negativo.','Sprint 2 a Sprint 4'),
 '006-formacion':('capacitacion, unidad, material_modulo, inscripcion, progreso, evaluacion, intento_evaluacion, certificado, taller, asistencia_taller','/api/plataforma/negocio/capacitaciones/; /api/plataforma/negocio/talleres/; /api/plataforma/negocio/mis-actividades/; /api/plataforma/negocio/certificados/{id}/pdf/; /api/plataforma/certificados/verificar/{codigo}/','backend/apps/plataforma/negocio.py','frontend/src/panel/negocio/Modulos.jsx','Publicar requiere módulos y evaluación. El alumno inscrito accede al material privado, completa módulos y responde; el servidor calcula la nota. Los intentos son acotados; aprobar genera certificado y actividad idempotente. Los talleres bloquean cupo y validan asistencia.','Sprint 3 a Sprint 5'),
 '007-sorteos':('sorteo, participacion_sorteo, ganador','/api/plataforma/negocio/sorteos/; /api/plataforma/negocio/sorteos/{id}/ejecutar/','backend/apps/plataforma/negocio.py','frontend/src/panel/negocio/Modulos.jsx','Participaciones desde actividades validadas y campañas elegibles. La ejecución congela candidatos y SHA-256, usa secrets y conserva ganadores y suplentes; un socio recibe como máximo un premio por sorteo. La evidencia completa se restringe al personal.','Sprint 3 a Sprint 5'),
 '008-recompensas':('beneficio, canje, movimiento_puntos, historial_estado','/api/plataforma/negocio/beneficios/; /api/plataforma/negocio/beneficios/{id}/canjear/; /api/plataforma/negocio/canjes/; /api/plataforma/negocio/canjes/{id}/estado/','backend/apps/plataforma/negocio.py','frontend/src/panel/negocio/Modulos.jsx','Reservar bloquea socio y beneficio, verifica saldo, stock y convenio y conserva el costo de la solicitud. Aprobar libera la reserva y registra el descuento, sin descontar dos veces; rechazar libera puntos y stock. La entrega conserva fecha y responsable.','Sprint 3 y Sprint 4'),
 '009-contenidos':('contenido, material, material_modulo, aviso_contenido','/api/plataforma/contenidos/; /api/plataforma/publicaciones/; /api/plataforma/materiales/; /api/plataforma/contenidos/{id}/aprobar/','backend/apps/plataforma/contenidos.py','frontend/src/panel/sprint2/Contenidos.jsx','Borrador, aprobación opcional por responsable designado y publicación por vigencia. Editar invalida la aprobación. Las descargas requieren autorización y validación del archivo real.','Sprint 2, Sprint 3 y Sprint 5'),
 '010-notificaciones':('plantilla_notificacion, preferencia_notificacion, notificacion, envio_notificacion','/api/plataforma/notificaciones/; /api/plataforma/preferencias/; /api/plataforma/negocio/plantillas/; /api/plataforma/negocio/envios/','backend/apps/plataforma/notificaciones.py','frontend/src/panel/negocio/Supervision.jsx','Cola duradera, reserva de trabajador, preferencias por evento y canal y hasta tres reintentos. Cambio de contraseña y validación de socio son comunicaciones obligatorias. Las plantillas por canal pueden usar {mensaje}. El correo tiene semántica al menos una vez.','Sprint 2, Sprint 3 y Sprint 5'),
 '011-juegos-retos':('juego, partida, reto, progreso_reto, actividad_validada','/api/plataforma/negocio/juegos/; /api/plataforma/negocio/juegos/{id}/iniciar/; /api/plataforma/negocio/partidas/{id}/finalizar/; /api/plataforma/negocio/retos/','backend/apps/plataforma/negocio.py','frontend/src/panel/negocio/Modulos.jsx','El cliente envía índices de respuestas; el servidor conserva la configuración y calcula el resultado. Un inicio consume un intento. Los retos cuentan actividades validadas dentro de su vigencia y acreditan una recompensa única.','Sprint 4 y Sprint 5'),
 '012-comunidad':('publicacion, comentario, reaccion, reporte_comunidad, suspension_comunidad, socio.alias','/api/plataforma/negocio/comunidad/; /api/plataforma/negocio/moderacion/; /api/plataforma/negocio/perfil-publico/','backend/apps/plataforma/api_comunidad.py','frontend/src/panel/negocio/Comunidad.jsx','Comunidad solo para socios; alias y ranking público desactivado por defecto. El texto se muestra con escape de React. Los reportes se resuelven con motivo y permiten ocultar, retirar o suspender temporalmente la participación.','Sprint 5'),
 '013-bienestar':('convenio, beneficio','/api/plataforma/negocio/convenios/; /api/plataforma/negocio/beneficios/','backend/apps/plataforma/api_negocio.py','frontend/src/panel/negocio/Modulos.jsx','Catálogo de convenios y beneficios por vigencia; el vencimiento también bloquea el canje. Los formularios no incluyen datos clínicos de socios.','Sprint 3 y Sprint 5'),
 '014-reportes':('consultas agregadas sobre referidos, conversiones, gastos, movimientos, formación, canjes y sorteos','/api/plataforma/negocio/reportes/?tipo={general|referidos|social|gamificacion}&desde=AAAA-MM-DD&hasta=AAAA-MM-DD&formato={json|csv|pdf}','backend/apps/plataforma/api_reportes.py','frontend/src/panel/negocio/Modulos.jsx','Reportes por rol y período con fecha y filtros. Los montos y gastos confirmados permiten mostrar captación y CAC; sin datos se informa la ausencia. Los CSV neutralizan prefijos de fórmula y el PDF es paginado.','Sprint 4 y Sprint 5'),
}


def main():
    estado=[]
    for carpeta,(tablas,rutas,backend,frontend,reglas,sprints) in MODULOS.items():
        destino=SPECS/carpeta
        (destino/'data-model.md').write_text(f'# Modelo de datos de {carpeta.split("-",1)[1]}\n\n'
            f'Tablas y atributos principales: {tablas}.\n\n{reglas}\n\n'
            'El mapeo vigente está en los modelos Django y los scripts SQL 01 a 08. '
            'La actualización 08 conserva datos y permisos existentes; el UML original requiere conciliación con esta evolución.\n',encoding='utf-8')
        (destino/'contracts.md').write_text(f'# Contratos de {carpeta.split("-",1)[1]}\n\n'
            f'Planificación original: {sprints}.\n\n## API\n\n'+ '\n'.join(f'- `{r}`.' for r in rutas.split('; '))+
            f'\n\n## Implementación\n\n- Dominio y API: `{backend}`.\n- Pantallas: `{frontend}`.\n\n'
            'Las escrituras validan los campos admitidos y la autorización en servidor. '
            'Los catálogos separan gestión y consulta del socio. Las acciones usan POST y '
            'los datos de negocio se calculan desde el servidor. Los rechazos de validación responden 400; '
            'la sesión ausente o inválida, 401; la falta de permisos, 403; el objeto inaccesible, 404.\n\n'
            'Las pruebas backend están en `backend/apps/usuarios/tests` y '
            '`backend/apps/plataforma/tests`; las pruebas de las nuevas pantallas están en '
            '`frontend/src/panel/negocio/negocio.test.jsx`. '
            'La aceptación completa por criterio y la revisión visual se registran separadamente de la existencia del código.\n',encoding='utf-8')
        estado.append({'spec':carpeta,'sprints':sprints,'backend':backend,'frontend':frontend,
                       'estado':'Implementación disponible; aceptación integral pendiente',
                       'evidencia':'Pruebas automatizadas del módulo; ver documentacion/EVOLUCION-PLATAFORMA.md'})
    with (SPECS/'estado-implementacion.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(estado[0]));w.writeheader();w.writerows(estado)
    clases=[]
    for archivo in (ROOT/'backend/apps').rglob('*.py'):
        if any(p in archivo.parts for p in ['tests','__pycache__']): continue
        arbol=ast.parse(archivo.read_text(encoding='utf-8-sig'))
        for clase in [c for c in arbol.body if isinstance(c,ast.ClassDef)]:
            clases.append({'clase':clase.name,'archivo':str(archivo.relative_to(ROOT)).replace('\\','/'),
                'linea':clase.lineno,'metodos':'; '.join(c.name for c in clase.body if isinstance(c,(ast.FunctionDef,ast.AsyncFunctionDef)))})
    with (ROOT/'documentacion/entregable/trazabilidad/CLASES-EVOLUCION.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(clases[0]));w.writeheader();w.writerows(clases)
    print(json.dumps({'contratos':len(estado),'clases_y_vistas_catalogadas':len(clases)}))


if __name__=='__main__':main()
