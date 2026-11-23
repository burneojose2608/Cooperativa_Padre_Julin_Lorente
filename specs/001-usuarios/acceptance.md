# Aceptación técnica de usuarios y perfiles

La API devuelve en la misma respuesta 400 los errores de correo, teléfono y fecha de nacimiento futura. El servicio conserva la regla de 18 años. La prueba `test_registro_formato_invalido_400` y la suite de registro pasaron en PostgreSQL aislado (HU-001, RF-01-1, UR-01, CU-G02, RNF-17 y RNF-20).

Se verificaron los ocho requisitos funcionales del módulo. Pasaron 162 pruebas de usuarios y Sprint 2 en PostgreSQL aislado y 48 pruebas de frontend.

| Historia | Requisito | Evidencia |
| --- | --- | --- |
| HU-001 | RF-01-1 | `test_registro_sprint1.py` comprueba alta, consentimiento fechado, hash Argon2id, formato de cédula y reversión ante fallos. |
| HU-002 | RF-01-2 | `test_sprint2.py` verifica que el perfil requiere autenticación y deniega acceso a otro titular. La pantalla de perfil redirige a ingreso sin sesión. |
| HU-003 | RF-01-3 | `test_sprint2.py` verifica edición permitida, identidad protegida y fotos privadas con formato real y límite de tamaño. `sprint2.test.jsx` verifica edición, validación de fotos y confirmación visual en componentes. |
| HU-004 | RF-01-4 | `test_sprint2.py` verifica contraseña actual, política, hash y revocación de sesiones. Los campos de contraseña son de tipo password. |
| HU-005 | RF-01-5 | `test_sprint2.py` verifica alta de personal, filtros, edición, auditoría y denegación en servidor. `sprint2.test.jsx` cubre la administración desde el panel lateral. |
| HU-006 | RF-01-6 | `test_registro_sprint1.py` comprueba padrón activo, ausente, inactivo y errores de consulta con el adaptador de prueba. |
| HU-007 | RF-01-7 | `test_sprint2.py` comprueba suspensión, motivo, responsable, revocación de sesiones y protección del último administrador. |
| HU-008 | RF-01-8 | `test_concurrencia_registro.py` y `test_persistencia_registro.py` comprueban unicidad bajo concurrencia y restricciones de PostgreSQL. |

La revisión de aceptación cruzó las ocho HU con sus RF, el plan, las tareas y los cambios de línea base. Se corrigieron los criterios heredados sobre el dígito verificador y el padrón ausente. Posteriormente, la revisión documental volvió a comprobar los prerrequisitos de Spec Kit desde una copia aislada, según el [flujo del proyecto](../../documentacion/FLUJO-SPEC-KIT.md).

El cierre cubre la aceptación técnica local. La revisión visual en navegadores reales y los requisitos de calidad transversales conservan su seguimiento en la aceptación general de la plataforma.

## Edad mínima en el registro público

Para HU-001 (RF-01-1, UR-01 y CU-G02), la API rechaza una fecha de nacimiento de hoy o de quien cumple 18 mañana, y admite el cumpleaños número 18. `test_registro_sprint1.py` comprueba estos casos en PostgreSQL aislado y `FormRegistro.test.jsx` comprueba el límite y el mensaje del formulario.

## Foto de perfil al iniciar y restaurar sesión

Para HU-003 (RF-01-3, UR-03, CU-G02 y RNF-10), el inicio de sesión y la consulta del perfil indican si el titular tiene una foto. La sesión conserva ese dato al recargar o renovar el acceso. La imagen se descarga por la ruta privada del titular. `test_sprint2.py` comprueba el contrato y `PanelLayout.test.jsx` verifica la barra superior al iniciar sesión, recargar, subir, reemplazar y quitar la foto.

Para HU-005 (RF-01-5, UR-04, CU-G17 y RNF-10), Usuarios y Validar socios consultan la foto de la misma cuenta a través de un endpoint de solo lectura para administradores activos. Se actualizan al volver a la ventana. `test_sprint2.py` comprueba el permiso y la retirada de la foto, y `sprint2.test.jsx` verifica que el listado refleje el reemplazo y la eliminación.

## Fichas de socio pendientes

La validación administrativa temporal incluye cuentas cuyo único rol es Socio y cuya ficha sigue sin fecha de validación. El administrador confirma que la persona es socia activa desde la pantalla existente. La operación conserva la ficha y su código, registra la validación en el padrón de prueba, habilita el código de referido y deja una sola entrada de auditoría ante reintentos. El padrón inactivo sigue bloqueando la operación.

La prueba `test_ficha_existente_pendiente_se_valida_desde_la_misma_lista` verifica el caso en PostgreSQL aislado, con trazabilidad al alta y validación de socios (HU-001, HU-006, RF-01-1, RF-01-6, UR-01, CU-G02) y al control administrativo y la auditoría (RNF-10, RNF-06).
