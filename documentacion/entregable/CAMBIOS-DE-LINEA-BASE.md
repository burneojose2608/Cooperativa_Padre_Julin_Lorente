# Cambios documentados de la línea base

Se conservan sin modificar el Excel original y el backlog completo para comparar la planificación con las decisiones posteriores del usuario. Los CSV de requisitos distinguen descripción vigente y descripción original cuando corresponde. La aprobación formal del docente no se da por realizada.

| Decisión del usuario | Requisitos afectados | Regla vigente |
| --- | --- | --- |
| DEC-CEDULA-10-DIGITOS | UR-01, RF-01-1, HU-001 | Cédula textual de exactamente diez dígitos ASCII del 0 al 9; conserva ceros iniciales. No calcula provincia ni dígito verificador. |
| DEC-REGISTRO-GENERAL | UR-01, RF-01-1, RF-01-6, HU-001/HU-006 | Padrón activo permite crear Socio; ausente permite cuenta general sin roles; inactivo rechaza; fallo del padrón impide completar el alta. |
| DEC-VALIDACION-TEMPORAL | Ampliación posterior del flujo de cuentas | Administrador activo revisa y confirma manualmente que una cuenta general corresponde a un socio activo. La operación es transaccional, auditada e idempotente; conserva usuario y contraseña. No permite reactivar padrón inactivo ni convertir cuentas con otros roles. |

Las decisiones proceden de instrucciones explícitas del usuario durante la implementación, resumidas aquí al consolidar los documentos históricos. El respaldo externo de la depuración conserva las explicaciones anteriores completas.

## Conversión temporal

En Administración → Validar socios se busca la cuenta general y se confirma expresamente su condición. El servidor vuelve a comprobar que quien actúa sea administrador y que la cuenta sea elegible. La interfaz no puede asignar el rol por sí sola.

Para impedir nuevas conversiones, configurar `CONVERSION_SOCIOS_TEMPORAL_HABILITADA=False` en el entorno del backend y reiniciarlo. Deshabilitar el proceso no borra las conversiones ni su auditoría. Las reglas institucionales definitivas siguen pendientes de definición.

La conversión comercial de referido HU-018/RF-03-3 y CodigoReferido son conceptos diferentes de esta habilitación y de codigo_socio. No se atribuyen puntos por convertir una cuenta general en socio.

El MVP utiliza padrón local de prueba, sin conexión institucional de producción. Los estados To Do del CSV histórico no prueban que el código esté pendiente; las pruebas locales tampoco prueban que Jira haya sido actualizado. Véase la [conciliación](backlog-jira/conciliacion_sprint_1.csv).

## Revisión de la representación de casos de uso

El usuario pidió representar objetivos de negocio y retirar comprobaciones técnicas como casos autónomos. La revisión no cambia requisitos funcionales ni programación: 37 elementos conservan su GUID y se reclasifican como reglas internas; las historias se trazan al caso de negocio que las contiene y mantienen su enlace a la regla original. Se conservan las condiciones en la descripción y se corrigen los subtipos y direcciones UML. El usuario pidió no presentar extension points ni sus notas en los diagramas. La explicación consolidada está en [el resumen](../RESUMEN-PROYECTO.md#casos-de-uso-orientados-al-negocio).

## Recuperación temporal por consola - Sprint 2

DEC-RECUPERACION-CONSOLA (17/11/2026): por instrucción explícita del usuario, HU-011 / RF-02-3
entrega su código temporal y enlace en la consola del backend, sin integración con correo.
Se conservan respuesta genérica, token aleatorio con hash, expiración de 30 minutos,
un solo uso, política de contraseña y revocación de sesiones. El backlog original mantiene
su redacción por correo; esta excepción queda trazada en el Sprint 2.
