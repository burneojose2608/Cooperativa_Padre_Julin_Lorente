# Registro de usuarios generales y socios

Ampliación posterior autorizada: ya está disponible el [proceso administrativo temporal](conversion-administrativa-temporal.md) para convertir cuentas existentes. Sustituye la limitación inicial que dejaba esa conversión pendiente. No se permite autoconversión ni cambio de roles desde el cliente.

Actualización posterior: una cédula válida significa ahora [exactamente diez dígitos](decision-cedula-diez-digitos.md), sin verificador. Se preparó el esquema faltante en la base original para resolver el 503, preservando sus cuentas y sin cargar socios sintéticos. Las referencias a verificador y base original sin cambios de este documento describen la revisión anterior; la decisión enlazada tiene prioridad.

## Decisión funcional del usuario

El 9 de noviembre de 2026 el usuario indicó: «si yo pongo número de cedula y no está en el padron deberia dejarme ingresar como usuario nuevo no socio». Esta instrucción posterior reemplaza la restricción original que impedía registrar cualquier cuenta si la cédula no estaba en el padrón. El CSV y el encargo original se conservan como referencia histórica, sin modificarlos.

| Condición de la cédula | Cuenta creada | Permisos |
| --- | --- | --- |
| Válida y activa en padrón | Usuario, socio, rol Socio y consentimiento | Área socio |
| Válida y no encontrada en padrón | Usuario y consentimiento | Mi cuenta y perfil propio |
| Válida pero inactiva en padrón | Ninguna | Sin acceso nuevo; se conserva el rechazo existente |
| Verificador inválido | Ninguna | Se solicita corregir la cédula |
| Padrón inaccesible o resultado desconocido | Ninguna | 503; no confundir fallo con ausencia de socio |
| Cédula, correo o username duplicado | Ninguna adicional | 409 controlado |

La cuenta general se representa con `roles=[]` y `area=null`, aprovechando la autenticación existente. No se crea un nuevo rol ni se cambia el esquema SQL. El servidor consulta los roles para autorizar las áreas; el cliente no puede declarar que es socio. Tampoco se añade un proceso automático para convertir una cuenta general existente en socio. Una futura incorporación al padrón requiere un proceso de validación separado antes de otorgar el rol.

La pantalla `/mi-cuenta` permite al usuario general entrar, ver su nombre, usuario y correo, y cerrar sesión. La ruta anterior `/sin-rol` redirige a esa pantalla. No se muestran campañas, puntos ni beneficios de socio a una cuenta general. El registro confirma si la cuenta fue creada como socio o usuario general antes de dirigir al login.

## Arquitectura y transacción

El puerto pasa de `consultar_activo() -> bool` a `consultar_estado() -> EstadoPadron`, con tres estados explícitos. La decisión sobre las filas y permisos corresponde al servicio; el repositorio solo interpreta el padrón y no asigna roles.

Se mantiene `atomic`: usuario, consentimiento y auditoría siempre se guardan juntos; socio y rol solo se añaden para ACTIVO. Ante fallo, se revierte el conjunto. Las comprobaciones e índices únicos se aplican a ambas clases de cuenta, incluidas solicitudes concurrentes. Se conservan consentimiento explícito, Argon2id, verificador y límite de solicitudes.

Esta regla modifica la privacidad de la respuesta original: ausente produce éxito de cuenta general e inactivo produce rechazo. La interfaz no publica una consulta de padrón, pero el resultado del registro permite distinguir estos casos. Se documenta como consecuencia de la nueva regla solicitada, sin afirmar que el comportamiento anterior se conserva.

## Verificación del cambio

- Suite completa: **80 pruebas aprobadas**, PostgreSQL real, 20.073 s.
- Registro ausente: 201, `codigo_socio=null`, `roles=[]`, usuario y consentimiento persistidos sin socio ni rol.
- Login general: 200; perfil propio: 200; las cinco áreas protegidas: 403.
- Socio activo e inactivo: comportamiento preservado.
- Fallo de padrón y adaptador con resultado desconocido: no crean cuenta.
- Fallo intermedio y duplicados de cuenta general: rollback y rechazo verificados.
- Cuatro carreras con conexiones independientes: tres de socio y una de cuenta general; una sola cuenta por carrera.
- React: build correcto, lint con salida 0 y las 14 advertencias previas de paneles sin modificar.
- Rutas: cuatro comprobaciones Node/assert aprobadas para cuenta general, socio, administrador y Marketing.
- Demo real: registro 201, login 200, perfil 200 y acceso a socio/admin/marketing 403 para `usuario.demo`. La ruta `/mi-cuenta` respondió 200; no se realizó inspección visual en navegador.

Archivos de evidencia: `test_registro_sprint1.py` y `test_concurrencia_registro.py`. La matriz general y los diagramas están actualizados en los documentos de esta carpeta.

La demo usa `sprint1_valeria_demo_1c8c1dff`. No se modificó cooperativa_db ni .env. Los cambios siguen locales, sin commits ni publicaciones.
