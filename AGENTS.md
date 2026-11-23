# Trabajo en la plataforma de la cooperativa

El usuario ha solicitado adoptar Spec Kit y aprovechar la documentación existente.
Leer `documentacion/FLUJO-SPEC-KIT.md` al comenzar cambios de funcionalidades.

- Usar las skills oficiales `speckit-*` cuando estén instaladas en `.agents/skills/`. La preparación del instalador no equivale a una instalación completada.
- Antes de definir un cambio, revisar sus requisitos, decisiones vigentes, evidencia de sprint y código. Conservar la trazabilidad HU/RF/UR/RNF/CU.
- Distinguir comportamiento implementado, verificación histórica, diseño planificado y preguntas institucionales pendientes. Un diagrama, un menú o un estado de CSV no certifican implementación.
- Mantener React, Django REST Framework y PostgreSQL y las convenciones existentes, salvo cambio solicitado y documentado.
- Conservar los originales de documentación y backlog; registrar las decisiones posteriores y actualizar las matrices afectadas. Modificar Enterprise Architect únicamente dentro del alcance solicitado y conservar GUID y trazabilidad.
- Probar cambios de datos sobre bases aisladas. Para bases existentes, usar actualizaciones aditivas; no repetir scripts de instalación inicial sobre datos existentes.
- Comprobar autorización en servidor, auditoría, protección de datos y revocación de sesiones según el alcance. No incluir `.env`, credenciales ni archivos privados en entregas.
- Actualizar especificación, implementación y evidencias del cambio conjuntamente. Informar verificaciones realizadas y pendientes con precisión.
- No hacer commit, push ni despliegue sin instrucción del usuario.
