# Informe de verificación del Sprint 1

Fecha: 10 de noviembre de 2026. Entorno comprobado: Windows, Python 3.14.7 en backend/venv, Django 6.1.2, Node 26.13.0 y PostgreSQL real. Las pruebas backend utilizan una base aislada test_*; la comprobación HTTPS utiliza la base demo separada.

## Resultados finales

| Comprobación ejecutada | Resultado |
| --- | --- |
| manage.py check | Sin incidencias |
| manage.py test --noinput | **135 pruebas aprobadas**, 27.232 s |
| npm test | **20 pruebas aprobadas**, cinco archivos, 2.30 s |
| npm run lint | Salida 0; 14 advertencias anteriores de Fast Refresh en paneles |
| npm run build | Correcto, 58 módulos, sin errores |
| pip check | Sin dependencias rotas |
| npm audit de la instalación de dependencias de prueba | Cero vulnerabilidades reportadas en esa ejecución |
| HTTPS real con cadena y hostname verificados | Página/login/perfil 200; logout 204; access/refresh reutilizados e inactividad 401 |
| Diagramas | Tres SVG nuevos de autenticación, login y sesiones renderizados y revisados como imágenes |

Las 135 pruebas incluyen las 108 del cierre previo y las nuevas verificaciones de sesiones, bloqueo, consulta de identificadores y recuperación. No se suman dos veces las pruebas dirigidas o las ejecuciones intermedias.

Los logs de errores que aparecen durante algunas pruebas son intencionales: se inyectan errores de infraestructura o ejecución para comprobar rollback y respuestas seguras. Esas pruebas finalizan aprobadas; el log solo muestra el tipo de excepción.

## Escenarios comprobados

- Sesión persistida y sid firmado compartido por access/refresh, sin guardar tokens en claro.
- Logout revoca la familia; perfil, refresh y otro logout con tokens revocados responden 401.
- Una sesión independiente del mismo usuario permanece vigente al cerrar otra.
- Un sid de otro usuario, un token sin sesión, un refresh inválido o sin usuario no habilitan acceso.
- Quince minutos sin uso, vencimiento absoluto y cuenta suspendida impiden acceder o renovar.
- La actividad anterior al plazo actualiza ultimo_uso; una petición después de vencer no revive la sesión.
- Un fallo al auditar logout revierte la revocación y no informa un cierre exitoso.
- Cinco fallos simultáneos, con cinco conexiones PostgreSQL distintas, conservan el contador y bloquean la cuenta.
- Cuenta inexistente, clave incorrecta, cuenta inactiva y bloqueo producen el mismo contrato público 401.
- Login correcto, formato inválido, JSON mal formado y límite de solicitudes quedan auditados con IP según corresponda.
- El servidor consulta los cinco roles actuales; retirar un rol lo deniega aunque un JWT anterior lo conserve.
- Se normalizan consultas de cuentas históricas con espacios; un username numérico tiene prioridad sobre la extensión de login por cédula.
- Restablecer la contraseña revoca las familias de sesión previas.
- El formulario conserva la contraseña oculta, valida obligatorios, evita duplicar un envío pendiente y dirige al área del rol.
- Tus áreas incluye RSE/contenidos y no muestra roles no asignados ni entradas duplicadas.
- Inactividad exacta en interfaz, actividad real, sincronización entre pestañas y limpieza de temporizadores.
- La interfaz no anuncia logout confirmado ante fallo de red; una respuesta o refresh tardío no restaura una sesión cerrada ni sobrescribe otra cuenta.
- HTTPS obligatorio en configuración segura, sin confiar por defecto en un X-Forwarded-Proto suministrado por el cliente.

## Límites reales

No se realizó revisión visual interactiva a 320, 600, 900 y 1920 px. La herramienta informó que el host de acceso al navegador no estaba disponible. Se ajustó el CSS y se probó el DOM, pero esos resultados no equivalen a validar geometría, recortes o alineación en un navegador real.

La CA de desarrollo solo se confió dentro del cliente de red de pruebas. No se instaló en Windows, no se omitieron verificaciones TLS y no se atravesaron advertencias del navegador. La operación con un certificado confiable del entorno requiere su configuración correspondiente; no hubo despliegue ni publicación.

No se probaron SMTP real, integraciones institucionales ni funcionalidades de campañas, puntos, sorteos o canjes, que no son historias programadas en Sprint 1. El CSV original no se modificó y no se hicieron commits ni push.

El workflow de CI queda preparado localmente, sin ejecución remota. La revisión en Figma, la validación WCAG completa y la aceptación formal no se declaran realizadas; su alcance figura en [arquitectura y tareas transversales](arquitectura-y-entornos.md).
