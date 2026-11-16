# Implementación del Sprint 1 completo del equipo

Esta entrega del 10 de noviembre de 2026 completa la programación de las historias planificadas en Sprint 1, sin limitarse al responsable original. Se preservan las modificaciones funcionales solicitadas durante la revisión del registro. No se implementan campañas, referidos, puntos, canjes ni otros módulos de sprints posteriores.

## Documentos para revisar

- [Plan de ejecución y decisiones](../../docs/plan-sprint-1-equipo.md).
- [Matriz completa de criterios, implementación y evidencia](matriz-trazabilidad.md).
- [Arquitectura, CI y tareas transversales](arquitectura-y-entornos.md).
- [Operación de sesiones, HTTPS y pruebas](operacion-sesiones-y-https.md).
- [Resultados finales y límites de verificación](verificacion.md).
- [Diagramas actualizados de login, roles y sesiones](diagramas/README.md).
- [Entrega previa de registro y conversión](../sprint-1-valeria/README.md).

## Alcance programado

| Historia | ID | Responsable original del CSV | Resultado de implementación |
| --- | --- | --- | --- |
| HU-001 | 101 | lizriofrio557@gmail.com | Registro, consentimiento y hash; integra HU-006/HU-008 |
| HU-006 | 106 | vale0401g@gmail.com | Solo socio activo obtiene rol; ausente puede crear cuenta general según decisión posterior |
| HU-008 | 108 | vale0401g@gmail.com | Unicidad normalizada y concurrencia garantizada en PostgreSQL |
| HU-009 | 109 | lizriofrio557@gmail.com | Login, sesión persistida, bloqueo, navegación y configuración HTTPS; integra HU-010/HU-012/HU-015 |
| HU-010 | 110 | jgabriel2608@gmail.com | Fallo de credenciales uniforme y auditoría de intentos con IP |
| HU-012 | 112 | jgabriel2608@gmail.com | Roles vigentes, unión de accesos de las cinco áreas y autorización de servidor |
| HU-015 | 115 | jgabriel2608@gmail.com | Logout revocable, rechazo de reutilización y expiración por inactividad |

Los responsables y estados del CSV no fueron editados. Esta tabla refleja el resultado del código y conserva su trazabilidad de planificación.

## Resultados y límites de aceptación

La suite final suma **135 pruebas backend y 20 pruebas de interfaz aprobadas**. Se probaron PostgreSQL real, revocación, inactividad, bloqueo concurrente, roles, formulario, temporizadores y renovación de tokens. También se verificó HTTPS real en loopback con validación de la cadena y del nombre del certificado, sin desactivar la verificación TLS ni instalar confianza en el sistema operativo.

La revisión visual interactiva del rango 320–1920 px permanece **no verificada**: el host de control del navegador no está disponible. El CSS conserva el diseño móvil primero y se ajustaron restricciones de ancho y cabeceras; las pruebas de interfaz verifican el comportamiento del DOM, no los píxeles de un navegador real. Esta limitación no se presenta como una prueba aprobada.

La configuración HTTPS local usa certificados de desarrollo. Para un navegador o despliegue con confianza establecida debe suministrarse un certificado confiable del entorno. No se publicaron servicios, no se desplegó el sitio y no se modificó la confianza de Windows o del navegador.

## Cómo corroborar el flujo

En la aplicación habitual http://localhost:5173, cerrar la sesión previa e iniciar de nuevo: los tokens antiguos sin identificador de sesión ya no se admiten. Las contraseñas y los roles guardados no se cambiaron. Cada nuevo login crea su sesión revocable.

Probar login con usuario/correo, navegar por las áreas permitidas, cerrar y comprobar que el token anterior ya no sirve. Una cuenta con varios roles dispone del bloque Tus áreas, incluidos Responsabilidad Social y Contenidos. Las funciones de esos módulos que pertenecen a otros sprints conservan sus pantallas de Próximamente.

La conversión administrativa temporal continúa en Administración → Validar socios. El perfil actualizado permite reconocer el nuevo rol sin cambiar credenciales.

Cambios locales para corroboración. Sin commits, push ni despliegue.
