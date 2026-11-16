# Fuente y evidencia del Sprint 1

`codigo_fuente_sprint_1.zip` contiene el código versionado del estado local revisado: backend, frontend, scripts SQL, pruebas, dependencias declaradas, documentación de planificación y configuración de CI. `manifiesto-codigo.json` identifica sus archivos y SHA-256. Se excluyeron entornos virtuales, dependencias instaladas, builds, `.env`, claves privadas y datos de base; el ZIP no contiene el historial Git.

La entrega cubre el registro vigente, padrón de prueba, unicidad y consentimiento; login y bloqueo; roles y autorización de las áreas; cierre, revocación e inactividad de sesiones. Recuperación de contraseña y validación administrativa temporal se conservan como implementación existente/ampliación documentada. Los paneles de módulos posteriores no se presentan como funcionalidad desarrollada por usar datos de ejemplo.

## Cómo revisar

1. Descomprimir el fuente en una carpeta de trabajo propia. Leer README.md del proyecto y documentacion-equipo/operacion-sesiones-y-https.md.
2. Instalar las dependencias declaradas de backend y frontend. Preparar PostgreSQL local y configurar variables de entorno propias; no se entregan credenciales reales.
3. Para una base nueva, seguir el orden SQL 01–06 del README. No volver a ejecutar el esquema completo sobre una base con datos.
4. Ejecutar los comandos del informe verificacion-actual.md. El runner backend exige una base de pruebas `test_*` y prepara sus scripts SQL.
5. Mostrar registro de cuenta general/socio según padrón, acceso con roles, cierre de sesión y rechazo de tokens revocados. La validación temporal exige revisión administrativa expresa.

Las pruebas de esta revisión son 135 backend y 20 frontend aprobadas. El lint conserva 14 advertencias preexistentes. Hay evidencia histórica de HTTPS, con sus límites; no se confunde con un despliegue público ni con certificados instalados en el equipo receptor.

Los documentos copiados conservan enlaces relativos del repositorio original. Para navegación dentro del paquete utilizar este LEEME y el índice principal. Las rutas mencionadas dentro de evidencias históricas se interpretan desde el repositorio descomprimido.

Las tareas remotas de Jira y la aceptación formal no se certifican desde el código. Los aspectos de accesibilidad completa, carga y disponibilidad pendientes están señalados en el informe de cumplimiento.
