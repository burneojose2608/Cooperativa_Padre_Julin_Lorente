# Matriz de trazabilidad del Sprint 1

Fuente: documentacion/product_con_subtareas.csv. Los criterios C1, C2 y siguientes conservan el orden de aceptación de cada fila. HU-001 y HU-009 son historias consolidadas; sus subtareas no se cuentan como historias independientes adicionales al estimar el sprint.

## Cadena UR a RF, historia y RNF

| UR | RF | HU | RNF del CSV |
| --- | --- | --- | --- |
| UR-01 | RF-01-1 | HU-001 | RNF-01, RNF-02, RNF-07, RNF-20, RNF-23 |
| UR-01 | RF-01-6 | HU-006 | RNF-23 |
| UR-01 | RF-01-8 | HU-008 | RNF-20 |
| UR-05 | RF-02-1 | HU-009 | RNF-03, RNF-09, RNF-21 |
| UR-05 | RF-02-2 | HU-010 | RNF-01, RNF-06, RNF-21 |
| UR-07 | RF-02-4 | HU-012 | RNF-10 |
| UR-05 | RF-02-7 | HU-015 | RNF-11 |

Las decisiones posteriores del usuario se registran como cambios de línea base. La aprobación formal de PO/docente no se da por realizada automáticamente.

## Criterios de registro

| Requisito | Criterio | Implementación | Evidencia o decisión |
| --- | --- | --- | --- |
| HU-001 C1 | Campos obligatorios del registro | FormRegistro, RegistroSerializer y servicio | Obligatoriedad en servidor, validaciones y pruebas de formato |
| HU-001 C2 | Verificador de cédula | Sustituido por diez dígitos ASCII, con ceros iniciales | [Decisión explícita del usuario](../sprint-1-valeria/decision-cedula-diez-digitos.md); no se afirma cumplir el criterio original sin cambios |
| HU-001 C3 | Padrón y ausencia de duplicados | ACTIVO obtiene Socio; ausente crea general; inactivo se rechaza; unicidad SQL | [Decisión de cuenta general](../sprint-1-valeria/decision-registro-general.md), pruebas de registro y concurrencia |
| HU-001 C4 | Argon2id/bcrypt y consentimiento con fecha/versión | Argon2id, lectores históricos, consentimiento true y persistencia versionada | Prueba de hash Argon2id, actualización de PBKDF2 y consentimiento |
| HU-006 C1 | Consultar padrón antes de habilitar Socio | Puerto EstadoPadron y repositorio independiente dentro de atomic | Activo, inactivo, ausente, manipulación y fallo del padrón |
| HU-006 C2 | Bloqueo idéntico de ausente e inactivo | Sustituido por general para ausente y rechazo para inactivo | Decisión posterior documentada; no se expone consulta pública de padrón |
| HU-006 C3 | Datos de prueba, sin integración de producción | Padrón local y carga sintética limitada a bases aisladas | Pruebas de persistencia y carga reproducible; sin conexiones institucionales |
| HU-008 C1 | Cédula única | Comprobación previa y UNIQUE | Escritura directa y carrera PostgreSQL |
| HU-008 C2 | Correo y username únicos | Normalización y consulta coherente con espacios/mayúsculas | Duplicados normales y cuentas generales |
| HU-008 C3 | Garantía de base de datos | Índices únicos, atomic y clasificación selectiva de restricciones | Tres carreras de socio y una general; colisiones del código con savepoint |

Evidencia de estos criterios: [pruebas de registro](../../backend/apps/usuarios/tests/test_registro_sprint1.py), [concurrencia](../../backend/apps/usuarios/tests/test_concurrencia_registro.py), [persistencia](../../backend/apps/usuarios/tests/test_persistencia_registro.py) y [códigos de socio](../../backend/apps/usuarios/tests/test_codigos_socio.py).

## Criterios de autenticación y acceso

| Requisito | Criterio | Implementación | Evidencia |
| --- | --- | --- | --- |
| HU-009 C1 | Usuario o correo y contraseña oculta | FormLogin, LoginSerializer y lookup normalizado | Pruebas de formulario, visibilidad y login por identificadores |
| HU-009 C2 | Crear sesión y dirigir según roles | emitir_tokens crea fila sesion y claim sid; perfil con todas las áreas | Sesión persistida, login y navegación de roles |
| HU-009 C3 | Vista entre 320–1920 px y solo HTTPS | CSS móvil primero, cabeceras flexibles, modo HTTPS y redirección obligatoria configurable | TLS real validado y pruebas de configuración; **revisión visual por píxeles no verificada** |
| HU-009 C4 | Cinco fallos bloquean 15 minutos | Contadores con bloqueo de fila y plazo en servidor | Cinco intentos simultáneos en cinco conexiones; bloqueo real y expiración |
| HU-010 C1 | Cuenta existente y activa, comparación de hash | Usuario vigente y check_password; hash equivalente para rechazos previos | Inactivo no entra; credenciales correctas y hashes históricos funcionan |
| HU-010 C2 | Mismo fallo público de credenciales | Inexistente, clave incorrecta, inactivo y bloqueado devuelven el mismo 401/código/mensaje | Comparación de las cuatro respuestas; el bloqueo no revela existencia |
| HU-010 C3 | Cada intento auditado con IP | LOGIN EXITO/FALLO dentro de transacción; también formato, JSON y throttling | Recuento, IP y recurso; auditoría sin contraseña ni token |
| HU-012 C1 | Obtener todos los roles | identificar_roles consulta la base y fija una prioridad determinista de área inicial | Cinco roles y perfil; refresh actualiza sus claims |
| HU-012 C2 | Menú limitado a funcionalidades permitidas | RutaPorArea, AccesosPorRol y permisos del backend | Accesos no asignados ocultos y API 403, incluso con JWT antiguo |
| HU-012 C3 | Unión de accesos multirrol | Tus áreas presenta las cinco áreas asignadas, sin duplicados | Pruebas de DOM para admin/Marketing/RSE/contenidos/socio y endpoints por área |
| HU-015 C1 | Invalidar sesión/token al cerrar | POST logout revoca una familia sid en PostgreSQL, con auditoría | Access y refresh dejan de servir; otra sesión independiente permanece válida |
| HU-015 C2 | Token invalidado no autorizado | AutenticacionConSesion y refresh verifican la misma fila | Perfil, refresh y reutilización secuencial de logout devuelven 401 tras revocar |
| HU-015 C3 | Cerrar por 15 minutos de inactividad | Servidor verifica ultimo_uso; interfaz temporiza y notifica actividad real | Expiración persistida, refresh/actividad no reviven, temporizadores exactos y sincronización entre pestañas |

Evidencia principal: [sesiones y bloqueo](../../backend/apps/usuarios/tests/test_sprint1_sesiones.py), [roles existentes](../../backend/apps/usuarios/tests/test_roles.py), [menú](../../frontend/src/components/AccesosPorRol.test.jsx), [formulario](../../frontend/src/components/FormLogin.test.jsx), [inactividad](../../frontend/src/hooks/useInactividad.test.jsx), [contexto](../../frontend/src/context/AuthContext.test.jsx) y [cliente HTTP](../../frontend/src/api/cliente.test.js).

Los errores de formato continúan siendo 400 y el límite de solicitudes 429: ninguno revela si una cuenta existe. La igualdad de HU-010 se aplica a los rechazos de credenciales, estado y bloqueo; esos detalles quedan solo en el estado de servidor y la auditoría autorizada.

## Dependencias y ampliaciones

| Elemento | Cobertura de Sprint 1 |
| --- | --- |
| T-004 | Diagramas reales de registro, login, clases, conversión y sesiones; no diseños ficticios de módulos posteriores |
| T-007 | Validación, ORM parametrizado y contrato seguro de errores |
| T-005 | Pipeline local preparado para backend/frontend y política de ramas; ejecución remota no realizada |
| T-009 | Validador de claves comunes, Argon2id y sal individual probados |
| T-010 | Diccionario y E-R de las once tablas de usuarios, generados en solo lectura |
| T-011 / T-012 | Reutilización de esquema SQL 01–06 y datos sintéticos; sesion y ultimo_uso ya existían, sin nueva tabla ni migración |
| Auditoría transversal | Eventos concretos de registro, login, logout, expiración y conversión; sin interfaz de edición de bitácora |
| Conversión administrativa temporal | Se conserva la ampliación autorizada, sus permisos, confirmación, auditoría e idempotencia |
| Recuperación existente | Regresión: cambiar la contraseña revoca access/refresh anteriores; no se añade otro módulo de recuperación |

El CSV y las asignaciones originales permanecen intactos. El código resuelve la entrega conjunta, independientemente de sus responsables originales.
