# Modelo de datos de formacion

Tablas y atributos principales: capacitacion, unidad, material_modulo, inscripcion, progreso, evaluacion, intento_evaluacion, certificado, taller, asistencia_taller.

Publicar requiere módulos y evaluación. El alumno inscrito accede al material privado, completa módulos y responde; el servidor calcula la nota. Los intentos son acotados; aprobar genera certificado y actividad idempotente. Los talleres bloquean cupo y validan asistencia.

El mapeo vigente está en los modelos Django y los scripts SQL 01 a 08. La actualización 08 conserva datos y permisos existentes; el UML original requiere conciliación con esta evolución.

- **`Certificado.inscripcion`**. Cada inscripción tiene como máximo un certificado, según `backend/apps/plataforma/models_negocio.py`.
