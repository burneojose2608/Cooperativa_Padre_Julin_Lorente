# Sprint 2 - implementación y revisión local

Fecha: 17/11/2026. Alcance tomado de `documentacion/product_con_subtareas.csv`, columna **Sprint planificado**: 11 historias y 6 subtareas. HU-064 se incluye porque quedó consolidada y planificada en Sprint 2. Se conserva el CSV original, con sus responsables y estados de Jira.

## Funcionalidades y acceso

| Cuenta | Pantalla | Funcionalidad disponible |
|---|---|---|
| Toda cuenta autenticada | Mi perfil | Consulta de identidad, edición de correo, teléfono y foto privada; cambio de contraseña con contraseña actual |
| Administrador | Usuarios | Crear personal, consultar y filtrar cuentas, editar contacto, activar/suspender/desactivar con motivo, consultar historial, asignar y revocar roles |
| Administrador | Roles y permisos | Permisos efectivos desde la siguiente petición y registro de cada cambio |
| Administrador | Parámetros | Versiones de reglas de puntos por actividad, período, límite y fechas; conserva reglas y movimientos anteriores |
| Socio validado | Referidos y Mi perfil | Código aleatorio persistente de 16 caracteres, enlace de invitación, copiar y compartir desde el dispositivo |
| Gestor de contenidos | Gestionar contenidos | Borradores, edición, publicación, programación de inicio/fin y retiro de noticias, anuncios y multimedia |
| Gestor de contenidos / Responsabilidad Social | Material educativo | Biblioteca por categoría y formato; alta, edición, descarga privada, eliminación y reutilización en varios módulos |
| Toda cuenta autenticada | Publicaciones | Contenido publicado que esté dentro de su vigencia; texto codificado por React y archivos autorizados |
| Toda cuenta autenticada | Notificaciones | Bandeja propia, indicador de pendientes, marcar como leída y preferencias por evento/canal |

Marketing conserva el acceso por rol, su perfil, las publicaciones y notificaciones. Sus campañas, prospectos, sorteos y reportes se habilitan en los sprints que los planifican. Los paneles activos muestran datos del servidor. Las pantallas de demostración anteriores no están enlazadas en la navegación activa.

## Ejecución local

Desde la raíz del repositorio, con PostgreSQL iniciado y `backend/.env` configurado:

```powershell
.\.venv\Scripts\python.exe -m pip install -r backend/requirements.txt
.\.venv\Scripts\python.exe backend/manage.py actualizar_sprint2
.\.venv\Scripts\python.exe backend/manage.py runserver
```

En otra terminal:

```powershell
cd frontend
npm install
npm run dev
```

En una tercera terminal, desde la raíz, mantén activo el trabajador de notificaciones:

```powershell
.\.venv\Scripts\python.exe backend/manage.py procesar_notificaciones --continuo
```

Para procesar una tanda y terminar, ejecuta `procesar_notificaciones --limite 100`. Al detener el trabajador se conservan los pendientes en PostgreSQL y se retoman al iniciarlo. Publicar registra un evento; el trabajador resuelve los destinatarios y entrega las notificaciones después de la petición.

Abre `http://localhost:5173/ingresar` y utiliza tus cuentas existentes. La cuenta general dispone de enlaces a Mi perfil y Mis notificaciones. Las cinco áreas mantienen la autorización del servidor. El último administrador activo está protegido frente a la suspensión o retirada de su rol.

### Recuperación temporal solicitada

En **Olvidé mi contraseña**, escribe usuario, cédula o correo. La terminal donde corre Django muestra **Código de recuperación** y un enlace completo. Copia el código y entra en **Ingresar el código**, o abre el enlace. La recuperación nunca utiliza SMTP, aunque exista configuración de correo para otras notificaciones. El código es aleatorio, expira en 30 minutos, se almacena únicamente como SHA-256, admite un solo uso y tiene un intervalo mínimo de 120 segundos entre solicitudes. La respuesta HTTP es igual para cuentas existentes e inexistentes. Cambiar o restablecer contraseña revoca las sesiones anteriores.

Esta entrega por consola sustituye temporalmente el correo de HU-011 / RF-02-3 por instrucción explícita del usuario. El CSV original conserva el criterio por correo; la excepción se registra en la matriz de aceptación y en el resumen del proyecto. Es una modalidad de práctica local.

### Archivos y contenido

Fotos: JPG, PNG y WebP. Materiales: esos formatos, PDF legible sin cifrado y MP4. Máximo **10 MB** por archivo, con cotejo de extensión, MIME y contenido real. Se usan nombres aleatorios en `backend/archivos_privados`, fuera del frontend y del directorio público. Las descargas requieren autenticación y permisos; incluyen `nosniff` y no se entregan como HTML ejecutable. Los materiales pueden asociarse a varios módulos ya registrados. El alta de capacitaciones corresponde a su sprint posterior.

El contenido necesita título, cuerpo, categoría, tipo y fecha de inicio antes de publicarse. Multimedia requiere un archivo asociado. Editar una publicación la devuelve a borrador. La visibilidad se calcula en el servidor con fecha de Ecuador en cada consulta; un inicio futuro o un fin vencido impide mostrarla y descargar sus adjuntos. Para cambiar adjuntos de un contenido publicado, primero debe pasar a borrador.

### Notificaciones y reglas

Eventos conectados: perfil actualizado, contraseña cambiada desde sesión, socio validado y contenido publicado. Los eventos de referidos, acreditación de puntos, campañas, sorteos y canjes se conectarán cuando se implementen esos módulos, según HU-068. La recuperación de contraseña utiliza su salida por consola independiente.

Cada envío tiene reserva temporal para coordinar trabajadores, entrega inicial y hasta **3 reintentos** con espera creciente. El error persistido identifica su tipo sin almacenar credenciales SMTP. Se verifican preferencias al registrar y al entregar. La bandeja evita duplicados por evento; el correo tiene semántica de entrega al menos una vez y puede duplicarse si el proceso cae inmediatamente después de entregarlo al proveedor. El backend de correo configurado en Django se usa únicamente en el trabajador. Sin SMTP configurado, sus mensajes aparecen en consola.

Cada configuración de puntos crea una nueva versión. Para nuevas actividades se seleccionará la versión vigente más reciente. Se rechazan fechas de inicio retroactivas; los movimientos existentes permanecen inmutables. Este sprint configura reglas; la acreditación y el canje pertenecen a sus historias posteriores.

## Trazabilidad y verificación

`TRAZABILIDAD-SPRINT-2.csv` relaciona los 17 ítems con RF, UR, RNF, actores, casos de uso, clases, métodos, endpoints, pantallas y pruebas. `ACEPTACION-SPRINT-2.csv` desglosa sus criterios y evidencia automatizada. Las fuentes generales se actualizan en `../trazabilidad/CLASES-CODIGO.csv`, `TRAZABILIDAD-VERIFICADA.csv` y `RELACIONES-VERIFICADAS.csv`, conservando los GUID del modelo.

El archivo Enterprise conserva su diagrama de clases único, la presentación uniforme, los casos generales y sus detalles, contexto y actividades. Los campos y firmas implementados se cotejan con el código; los miembros futuros se documentan como planificados en el catálogo. La tabla física histórica conserva sus nombres mediante `db_table` y `db_column`.

```powershell
.\.venv\Scripts\python.exe backend/manage.py test apps.usuarios apps.plataforma --noinput
cd frontend
npm test
npm run lint
npm run build
```

La base del proyecto se actualiza únicamente con el script aditivo `07_sprint_2.sql`, protegido por transacción y bloqueo de actualización. El comando es repetible y no reasigna permisos ya revocados. Los scripts 01-06 se ejecutan únicamente para instalaciones vacías y pruebas aisladas. El respaldo de la base previa quedó fuera del repositorio, junto con las verificaciones de esta revisión.

Los resultados finales y las limitaciones observadas se registran en `VERIFICACION.md`. Los cambios quedan locales para revisión.
