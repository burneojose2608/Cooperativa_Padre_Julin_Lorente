# Validación de diez dígitos y corrección del registro local

## Regla vigente

El 9 de noviembre de 2026 el usuario pidió comprobar únicamente diez números, sin cálculo del verificador. Esta instrucción posterior reemplaza la exigencia de verificador de HU-001 en el CSV y en la primera entrega. El código admite exactamente diez dígitos ASCII del 0 al 9 y conserva la cédula como texto, incluidos ceros iniciales. No comprueba provincia, tercer dígito, checksum ni existencia oficial de la identificación.

Se rechazan signos positivos o negativos, decimales, letras, espacios interiores y longitudes distintas de diez. Como el requisito es únicamente formato, también se aceptan secuencias como `0000000000`; no se inventan reglas adicionales para excluirlas. El servicio mantiene el trim exterior acordado antes de validar. La API exige texto JSON para conservar ceros iniciales.

| Ejemplo | Resultado de formato |
| --- | --- |
| 0127805968 | Aceptado |
| 1234567890 | Aceptado, sin comprobar verificador |
| 9999999999 | Aceptado, sin comprobar provincia |
| -123456789 | Rechazado por signo |
| 12345678.9 | Rechazado por punto decimal |
| 123456789 | Rechazado por longitud |

Continúa vigente la decisión anterior de cuentas generales: una cédula ausente del padrón crea usuario general sin permisos de socio. Una activa crea socio; una inactiva conserva el bloqueo. No se eliminan controles de duplicados, contraseña, consentimiento ni autorización.

## Causa y resolución del error 503

La aplicación habitual en 5173 consultaba el backend 8000 con cooperativa_db. Esa base no tenía la tabla padron_prueba, por lo que el servicio devolvía 503. Cambiar el verificador por sí solo no solucionaba ese fallo.

Después de validar los cambios en una base aislada, se aplicaron SQL 05 y SQL 06 al esquema de la base local original. Se verificaron previamente ausencia de conflictos normalizados de correo/username y cumplimiento del formato de cédula. La aplicación se realizó transaccionalmente, con bloqueo temporal de escrituras y verificación de conteos iguales antes y después en usuario, socio, usuario_rol, consentimiento y auditoria. No se cambiaron valores, no se borraron cuentas y no se cargaron socios sintéticos en la base original. La tabla nueva de padrón queda vacía en esa base: los nuevos registros allí son cuentas generales hasta que exista una fuente de padrón gestionada explícitamente.

También se aplicó SQL 06 a la demo separada y se reinició su backend. No se cambió .env ni se hicieron commits o publicaciones.

## Esquema y reversión

- SQL 05 actual usa la regla de diez dígitos tanto en usuario como en padron_prueba para instalaciones nuevas.
- SQL 06 actualiza las restricciones de instalaciones que habían aplicado la revisión inicial de SQL 05 con verificador. Puede aplicarse otra vez sin cambiar datos.
- Los índices únicos anteriores y normalizados permanecen.
- La función histórica cedula_ec_valida se conserva para compatibilidad y reversión, pero el registro vigente no la utiliza.
- reversiones/06 permite restaurar deliberadamente la política histórica con verificador; aborta sin pérdida si hay cédulas incompatibles. En una instalación nueva con SQL 05 ya actualizado, esa reversión es una restauración de la política histórica, no un cambio necesario para retirar SQL 06.
- Para retirar íntegramente la funcionalidad de padrón, retirar primero el backend que la usa, exportar el padrón y seguir reversiones/05. No borrar ni corregir automáticamente cuentas para hacer posible una reversión.

## Evidencia

- Suite completa: **83 pruebas aprobadas**, PostgreSQL real, 34.989 s.
- Validación JavaScript: 14 casos aprobados, incluidos dígitos con ceros iniciales, sin checksum, signos, decimales, letras, longitudes y tipos incorrectos.
- React: build correcto; lint salida 0 con las 14 advertencias de paneles ya documentadas.
- SQL: acepta diez dígitos sin verificador, rechaza caracteres no numéricos y conserva unicidad; actualización desde esquema anterior y reversión fallida sin pérdida verificadas.
- Base original: registro completo por APIClient con 201 dentro de una transacción revertida. Se confirmó que no quedó la cuenta temporal.
- Aplicación habitual: prueba por http://localhost:5173/api/auth/registro/ con cédula sin checksum y contraseña deliberadamente débil devuelve 400 clave_debil, lo que confirma que el backend activo ya acepta el formato simplificado sin crear una cuenta de prueba persistente.

No se promete ausencia absoluta de errores: duplicados, datos incompletos, consentimiento ausente, contraseña débil o indisponibilidad real de PostgreSQL siguen produciendo respuestas controladas. No se realizó inspección visual manual del formulario.
