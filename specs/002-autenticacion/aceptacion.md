# Aceptación técnica local de Autenticación

El 21 de noviembre de 2026 se ejecutaron las pruebas de Usuarios y Plataforma con datos sintéticos en PostgreSQL aislado. Las pruebas React de formularios y sesión se ejecutaron en Vitest con jsdom.

| Historia y trazabilidad | Resultado y evidencia |
| --- | --- |
| HU-009 · RF-02-1 · UR-05 · CU-G01 · RNF-03, RNF-09, RNF-21 | Inicio por usuario y correo, contraseña oculta, sesión persistida, redirección al área autorizada y bloqueo tras cinco fallos durante quince minutos. `test_servicios.py`, `test_roles.py`, `test_sprint1_sesiones.py` y `FormLogin.test.jsx`. Se comprobó la configuración HTTPS en Django y queda abierta su validación en el entorno desplegado y la revisión en navegadores reales. |
| HU-010 · RF-02-2 · UR-05 · CU-G01 · RNF-01, RNF-06, RNF-21 | Fallos de cuenta inexistente, desactivada o clave incorrecta con contrato genérico. Bitácora de éxitos, fallos y solicitudes inválidas con IP y sin credenciales. `test_sprint1_sesiones.py`, `test_servicios.py` y `test_registro_sprint1.py`. |
| HU-011 · RF-02-3 · UR-06 · CU-G01 · RNF-01, RNF-21 | Recuperación por consola según DEC-RECUPERACION-CONSOLA. Se comprobaron respuesta genérica, huella del token, expiración, uso único, límite de solicitudes, política de contraseña y revocación de access y refresh. `test_recuperacion.py`, `test_sprint2.py` y `sprint2.test.jsx`. La entrega definitiva por correo conserva su tarea propia. |
| HU-012 · RF-02-4 · UR-07 · CU-G01 · RNF-10 | El servidor recupera los roles actuales y selecciona el área inicial por prioridad. El menú combina las cinco áreas sin duplicarlas ni dar acceso protegido a cuentas generales. `test_roles.py`, `test_sprint1_sesiones.py` y `AccesosPorRol.test.jsx`. |
| HU-013 · RF-02-5 · UR-07 · CU-G17 · RNF-06, RNF-10 | Administración actualiza roles y permisos con auditoría. Su aplicación se comprueba en la siguiente petición, incluso con una sesión previa. `test_sprint2.py`, `test_sprint1_sesiones.py` y la prueba de guardado de permisos de `sprint2.test.jsx`. |
| HU-014 · RF-02-6 · UR-07 · CU-G17 · RNF-10, RNF-20 | La API deniega rutas administrativas para roles ajenos y bloquea lectura y edición de un perfil de otro titular. Las pruebas incluyen 401 sin sesión y 403 con rol insuficiente. `test_sprint2.py` y `test_roles.py`. |
| HU-015 · RF-02-7 · UR-05 · CU-G01 · RNF-11 | Access y refresh quedan inutilizables al cerrar o alcanzar quince minutos de inactividad. El cliente comprueba el temporizador y descarta respuestas tardías tras cerrar sesión. `test_sprint1_sesiones.py`, `useInactividad.test.jsx`, `cliente.test.js` y `AuthContext.test.jsx`. |

Las verificaciones externas de HTTPS, navegadores, móvil y correo se mantienen vinculadas a las [tareas transversales](../000-plataforma/tasks.md) y a [HU-011](spec.md#hu-011-recuperar-la-contraseña-por-correo).

La pantalla de HU-013 (RF-02-5, UR-07, CU-G17, RNF-06 y RNF-10) permite seleccionar un rol y consultar sus permisos asignados. Los interruptores aparecen al elegir «Editar permisos». Las pruebas de interfaz de `sprint2.test.jsx` verifican el cambio de rol, la lista correspondiente y el guardado de permisos del rol seleccionado.
