# Alcance contrastado y evidencia

El repositorio implementa identidad y seguridad en el alcance vigente del Sprint 1. El modelo cubre el alcance de negocio posterior como análisis, sin presentar tablas o demostraciones como módulos operativos. No se cambió código ni base de datos de la aplicación. No se leyó .env ni se extrajeron credenciales.

No se encontraron AGENTS.md en el árbol del proyecto ni en los directorios antecesores consultados. Se conservaron los documentos, diagramas y fuentes previos.

## Precedencia de fuentes

Las decisiones documentadas posteriores gobiernan los cambios de registro: cuenta general ante ausencia del padrón y cédula de diez dígitos sin verificador. La validación temporal posterior permite conversión administrativa manual. Se preservan los criterios originales del CSV y Excel como antecedentes, sin afirmar cumplimiento del criterio sustituido. La propuesta inicial de modelo-clases fue contrastada y revisada; no constituye aprobación de requisitos.

Acta: propósito, alcance preliminar del MVP, exclusiones y criterios de éxito. Visión: necesidades de socios, Marketing, Responsabilidad Social, administración y contenidos; documento con restos de plantilla que no se convierten en reglas. PROYECTO 1: especificación general de referidos, gamificación, participación, bienestar y modularidad; menciones futuras no autorizan integraciones productivas o IA concreta.

El Excel aporta UR, RF, reglas y datos, no evidencia de aceptación ni implementación. Su regla histórica de verificador queda sustituida por la decisión posterior. Hojas inspeccionadas: Resumen, UserReq., Req. Funcionales, Req. No Funcionales, MODULOS. Se encontraron 57 UR, 91 RF detallados y 14 familias explícitas en celdas.

## Estado por familia funcional

| Familia | Estado observado | Evidencia y brecha |
|---|---|---|
| RF-01 Usuarios y perfiles | Implementado parcialmente | Alta pública, consulta propia, padrón, unicidad y alta interna por servicio/comando. Edición de contacto/foto, cambio autenticado de clave y administración completa de estados no acreditados por urls.py. Usuario–Socio opcional. |
| RF-02 Acceso y permisos | Implementado parcialmente | Login, bloqueo, recuperación, sesiones revocables, inactividad y autorización por roles vigentes. Administración dinámica completa de permisos pendiente. |
| RF-03 Referidos | Planificado | SQL 01–02, CSV y pantallas demo. Código de socio real no prueba código referido. Referido convertido en demo no es conversión comercial persistida. |
| RF-04 Campañas | Planificado | SQL y backlog. Objetivos/incentivos/segmentos sin servicios operativos; fuente institucional de segmentación pendiente. |
| RF-05 Puntos y reconocimientos | Planificado | Libro y triggers SQL no realizan motor de reglas. SocioProvider modifica puntos en memoria; no es reserva/contabilidad transaccional. CuentaPuntos es agregado conceptual propuesto. |
| RF-06 Formación y talleres | Planificado | Tablas y requisitos; progreso, evaluaciones, certificados y asistencia no acreditados por API operativa. |
| RF-07 Sorteos | Planificado | Persistencia parcial; faltan lista congelada y evidencia completas. Se exigen CSPRNG, ejecución única y hash por HU-050. |
| RF-08 Beneficios y canjes | Planificado | Catálogo y canjes demostrativos. Debe coordinar reserva, cierre, descuento/liberación y stock; no doble débito. |
| RF-09 Contenido | Planificado | Tablas y pantallas no acreditan autorización, aprobación ni vigencia operativas. |
| RF-10 Notificaciones | Planificado | Recuperación de clave por correo es independiente; no prueba servicio general asíncrono ni bandeja. |
| RF-11 Juegos y retos | Planificado | Configuración y resultados demo; fórmulas e intentos deben validarse por servidor. |
| RF-12 Comunidad | Planificado | Tablas y demo; privacidad, reportes, moderación y suspensiones requieren reglas/servicios. |
| RF-13 Bienestar | Planificado | Convenios y contenidos informativos, sin atención clínica o datos de salud personales. |
| RF-14 Reportes | Planificado | Paneles de ejemplos; sin agregaciones y exportación real del backend. ServicioReportes es propuesta de responsabilidad. |

## Evidencia concreta revisada

- Backend: config/urls.py y apps/usuarios/urls.py delimitan API real a autenticación, registro, perfil, sesiones, recuperación y validación administrativa temporal. Models, servicios, permisos y validadores contrastan el comportamiento. No hay backend de referidos, campañas o gamificación acreditado por esas rutas.
- Frontend: api/auth.js y api/administracion.js son llamadas reales; ValidarSocios.jsx usa listado y conversión reales. PanelSocio.jsx y PanelAdmin.jsx importan datos/demo.js; canjear modifica useState, sin garantía de libro o stock. La etiqueta demostrativa no se usa como requisito.
- SQL 01: esquema general, asociaciones, restricciones e inmutabilidad. SQL 02: campos complementarios, historial, talleres y preguntas XOR. SQL 03: recuperación de un uso. SQL 04: formato diez dígitos. SQL 05: padrón y unicidad normalizada. SQL 06: política final de formato. Ningún script se ejecutó.
- Pruebas inspeccionadas: test_registro_sprint1, test_conversion_socio, test_concurrencia_registro, test_codigos_socio, test_roles, test_recuperacion, test_sprint1_sesiones, test_esquema_registro, test_cedula; formularios, AuthContext y cliente HTTP. Evidencian alcance de identidad; no se extrapolan a módulos futuros.
- documentacion/sprint-1-equipo/verificacion.md informa 135 pruebas backend y 20 frontend previas. Esta entrega no reejecutó suites de aplicación ni accedió a PostgreSQL; sus verificaciones son del modelo UML. Se conserva la diferencia entre evidencia previa reportada y prueba ejecutada ahora.

## Límites del análisis

Mapear 91 HU y 14 familias RF verifica referencias, no aceptación completa. Las 27 subtareas originales conservan su padre y no se suman como historias independientes. La matriz enlaza operaciones representativas y reglas con conceptos de apoyo. Aristas exactas de transición, políticas de límites, niveles, stock, segmentos, adjudicación de suplentes y aprobación requieren decisión donde se indica.

La regla de no negatividad y rechazo de reverso negativo está definida por HU-036/038. Lo pendiente es su coordinación con reservas y límites, no autorizar saldo deudor. Los puntos reconocidos antes de una modificación de campaña se preservan mediante una instantánea propuesta.