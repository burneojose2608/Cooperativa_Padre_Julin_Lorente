# Operación y verificación de sesiones y HTTPS

## Preparación

Usar las credenciales locales ya configuradas sin copiarlas en documentos ni comandos compartidos. Para una instalación vacía, aplicar SQL 01–06 en orden. La tabla sesion existe en SQL 01 y ultimo_uso se añade en SQL 02; esta entrega no introduce otra tabla ni necesita nuevas migraciones de esquema.

Desde la raíz del repositorio:

```powershell
Push-Location backend
& .\venv\Scripts\python.exe -m pip install -r requirements.txt
& .\venv\Scripts\python.exe manage.py check
& .\venv\Scripts\python.exe manage.py test --noinput
Pop-Location
Push-Location frontend
npm.cmd ci
npm.cmd test
npm.cmd run lint
npm.cmd run build
Pop-Location
```

El runner solo admite bases test_* y ejecuta sus scripts en una base temporal. No usar keepdb con los scripts iniciales de creación. Las pruebas no recrean ni eliminan cooperativa_db.

## Contrato y compatibilidad de sesión

Login conserva access, refresh y usuario. Cada token incorpora sid, identificado en una fila de sesion que guarda usuario, vencimiento, último uso y revocación. No se almacenan los tokens en claro. Access dura 30 minutos y refresh un día, como la configuración previa; ambos quedan sujetos además a la sesión revocable y al límite de quince minutos de inactividad.

Los tokens emitidos antes de esta actualización sin sid se rechazan. Para usuarios existentes basta iniciar sesión de nuevo: no cambia su contraseña, cuenta ni roles. No debe mantenerse otro backend antiguo admitiendo los mismos tokens durante una publicación real.

| Ruta | Operación |
| --- | --- |
| POST /api/auth/login/ | Validar, auditar y crear familia de sesión |
| POST /api/auth/refresh/ | Renovar access solamente si la familia sigue vigente; roles actuales |
| POST /api/auth/logout/ | Revocar la familia autenticada y auditar LOGOUT; respuesta 204 |
| POST /api/auth/actividad/ | Confirmar actividad de una sesión vigente; no puede revivirla |
| GET /api/auth/yo/ | Perfil y roles actuales, sujeto a sesión vigente |

Tras logout, reutilizar access o refresh devuelve 401; también se rechaza otro logout secuencial con el token revocado. El servicio de revocación evita duplicar escrituras si dos peticiones ya autenticadas llegan simultáneamente. Cerrar una sesión no cierra otra familia independiente del mismo usuario.

El servidor revisa el vencimiento absoluto y ultimo_uso en cada petición autenticada, bajo bloqueo de fila. A los quince minutos marca la expiración y registra SESION_EXPIRADA antes de responder 401. No es necesario un proceso cron para impedir reutilización. El registro de la fila puede conservarse; una política futura de retención no forma parte de este sprint.

La interfaz detecta actividad mediante teclado, puntero, desplazamiento y toque, con avisos de actividad limitados a uno por minuto. No genera peticiones periódicas para mantener viva una pestaña inactiva. Comparte la actividad y el cierre entre pestañas. Una respuesta o refresh tardío de una sesión anterior no restaura la cuenta cerrada ni sobrescribe un login nuevo.

Un fallo de red en cierre manual no se presenta como revocación confirmada: se informa y se permite reintentar. Al vencer el plazo local se retira la interfaz; el servidor mantiene su propio límite aunque el navegador quede sin conexión. La recuperación de contraseña existente también revoca las familias previas.

## Login y roles

Todos los rechazos de credenciales, inactividad de cuenta o bloqueo de acceso usan el mismo 401 credenciales_invalidas. Tras cinco fallos de contraseña de una cuenta activa se conserva bloqueado_hasta durante quince minutos. Los contadores se actualizan dentro de una transacción con la fila del usuario bloqueada; no se pierden por peticiones simultáneas.

Todos los intentos auditables generan LOGIN EXITO/FALLO con IP; los errores de formato y el límite de solicitudes también se registran. La bitácora no contiene contraseñas, tokens ni identificadores personales completos. El manejador global evita mensajes de SQL, rutas y trazas.

Usuario y correo se buscan con trim y minúsculas, sin modificar los registros históricos. Si un username numérico coincide con la cédula de otra cuenta, se prioriza username, después correo y finalmente la extensión opcional de acceso por cédula. Así se respeta el contrato principal de usuario/correo sin probar una clave contra varias cuentas.

El área inicial sigue una prioridad estable: Administrador, Marketing, Responsabilidad Social, Contenidos y Socio. Tus áreas ofrece la unión completa de áreas asignadas. El backend consulta los roles actuales y deniega los retirados, aunque el token antiguo aún los incluya. Las funciones de módulos posteriores siguen como Próximamente.

## Modo HTTPS local verificable

El desarrollo habitual HTTP en 5173 se conserva como entorno de desarrollo. Para la configuración HTTPS de aceptación se preparó un frontend local en 5175 y un backend de loopback en 8002 sobre la base demo separada, sin publicar el sitio.

Preparar certificados locales, desde backend:

```powershell
& .\venv\Scripts\python.exe -m pip install -r requirements-dev.txt
& .\venv\Scripts\python.exe scripts/generar_tls_local.py
```

El generador crea ca.crt, localhost.crt y localhost.key bajo backend/.local-tls, ignorado por Git. Genera una CA y un certificado localhost/127.0.0.1/::1 válidos treinta días; no guarda la clave privada de la CA, no instala confianza y no sobrescribe archivos existentes. Para otro directorio usar --salida. Mantener privada la clave localhost.key.

En una terminal del backend:

```powershell
$env:DB_NAME = 'sprint1_valeria_demo_1c8c1dff'
$env:EXIGIR_HTTPS = 'True'
$env:CONFIAR_PROXY_HTTPS = 'True'
& .\venv\Scripts\python.exe manage.py runserver 127.0.0.1:8002 --noreload
```

En otra terminal, dentro de frontend:

```powershell
$env:API_PROXY_TARGET = 'http://127.0.0.1:8002'
npm.cmd run dev:https -- --host localhost --port 5175 --strictPort
```

El modo https obliga al cliente a utilizar /api en su mismo origen, evitando peticiones mixtas HTTP desde una página HTTPS. Vite termina TLS y sustituye X-Forwarded-Proto; el backend se limita a loopback y solo confía en ese encabezado cuando se habilita explícitamente CONFIAR_PROXY_HTTPS. No habilitar esa confianza para encabezados que pueda suministrar directamente un cliente externo.

Para certificados propios, definir TLS_CERT_FILE y TLS_KEY_FILE en el entorno del frontend. Para operación fuera del desarrollo local deben utilizarse certificados confiables del entorno y EXIGIR_HTTPS=True. La entrega no instala certificados en Windows o el navegador y no automatiza el paso por advertencias de seguridad.

El certificado local no está instalado en la confianza del navegador. Las pruebas de red confiaron solo en ca.crt dentro de su SSLContext y verificaron cadena y nombre; no utilizaron un contexto sin verificación. El despliegue y la configuración de confianza institucional quedan fuera de esta ejecución local.

## Pruebas ejecutadas

El plan y el informe de cierre indican el conteo final de pruebas. Se verificó además el flujo HTTPS real con estos resultados:

| Comprobación HTTPS | Resultado |
| --- | --- |
| Página de login | 200 |
| Login | 200 |
| Perfil autenticado | 200 |
| Logout | 204 |
| Access reutilizado | 401 |
| Refresh reutilizado | 401 |
| Sesión con quince minutos sin uso | 401 |

La verificación de red se hizo exclusivamente sobre la base demo. Los tokens no se imprimieron. En la base original solo se comprobó con un token inválido que el backend había cargado el guard de sesión actualizado; no se crearon usuarios ni se cambiaron contraseñas durante esta entrega.

## Revisión manual pendiente

Con un navegador disponible, corroborar login y registro a 320, 600, 900 y 1920 px, navegación con teclado, cabecera, mensajes largos, cambio de área y cierre. Esa revisión no pudo ejecutarse porque el host de control del navegador no está disponible. No se presenta como validada por las pruebas DOM de interfaz.
