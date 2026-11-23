# Tareas de autenticación y control de acceso

Conservar el sprint planificado y la relación padre de cada ítem. No sumar otra vez los puntos de las subtareas incluidos en la historia consolidada.

[Evidencia local por historia](aceptacion.md). HU-009-P conserva la revisión visual y de HTTPS en el entorno desplegado. HU-011-P-SMTP conserva la entrega definitiva por correo.

## Sprint 1 HU-009

- [x] HU-009-V (RF-02-1) Revisar código y evidencia existente frente a los criterios de la historia.
- [x] HU-009-B (RF-02-1) Completar dominio, transacciones, autorización y API requeridos.
- [x] HU-009-U (RF-02-1) Completar la pantalla conectada al servidor con validaciones y estados vacíos.
- [ ] HU-009-P (RF-02-1) Verificar «Iniciar sesión» con los criterios de [HU-009](spec.md#hu-009-iniciar-y-cerrar-sesión-con-validación-de-credenciales-y-roles). Registrar resultado y evidencia de cada criterio, incluidos los rechazos aplicables.
- [x] HU-009-D (RF-02-1) Actualizar trazabilidad, documentación y resultado de aceptación.

## Sprint 2 HU-011

- [x] HU-011-V (RF-02-3) Revisar código y evidencia existente frente a los criterios de la historia.
- [x] HU-011-B (RF-02-3) Completar dominio, transacciones, autorización y API requeridos. Aplicar la restricción de `TokenRecuperacion.token_hash` definida en [data-model.md](data-model.md).
- [x] HU-011-U (RF-02-3) Completar la pantalla conectada al servidor con validaciones y estados vacíos.
- [x] HU-011-P (RF-02-3) Verificar la aceptación de Sprint 2 en [spec.md](spec.md#hu-011-recuperar-la-contraseña-por-correo). Cubrir respuesta genérica, emisión por consola y huella persistida, caducidad a 30 minutos, uso único, límite de solicitudes, rechazo de clave débil y revocación de sesiones. Evidencia de referencia: `backend/apps/usuarios/tests/test_recuperacion.py`.
- [ ] HU-011-P-SMTP (RF-02-3, RF-10-3) Verificar la entrega definitiva de correo en el entorno acordado y repetir los casos de uso único y expiración con el enlace recibido.
- [x] HU-011-D (RF-02-3) Actualizar trazabilidad, documentación y resultado de aceptación.

## Sprint 2 HU-013

- [x] HU-013-V (RF-02-5) Revisar código y evidencia existente frente a los criterios de la historia.
- [x] HU-013-B (RF-02-5) Completar dominio, transacciones, autorización y API requeridos.
- [x] HU-013-U (RF-02-5) Completar la pantalla conectada al servidor con validaciones y estados vacíos.
- [x] HU-013-P (RF-02-5) Verificar «Gestionar roles y permisos» con los criterios de [HU-013](spec.md#hu-013-administrar-roles-permisos-y-acceso-seguro). Registrar resultado y evidencia de cada criterio, incluidos los rechazos aplicables.
- [x] HU-013-D (RF-02-5) Actualizar trazabilidad, documentación y resultado de aceptación.

## Sprint 1 HU-010

- [x] HU-010-V (RF-02-2) Revisar código y evidencia existente frente a los criterios de la historia.
- [x] HU-010-B (RF-02-2) Completar dominio, transacciones, autorización y API requeridos.
- [x] HU-010-U (RF-02-2) Completar la pantalla conectada al servidor con validaciones y estados vacíos.
- [x] HU-010-P (RF-02-2) Verificar «Validar credenciales» con los criterios de [HU-010](spec.md#hu-010-validar-credenciales-de-acceso). Registrar resultado y evidencia de cada criterio, incluidos los rechazos aplicables.
- [x] HU-010-D (RF-02-2) Actualizar trazabilidad, documentación y resultado de aceptación.

## Sprint 1 HU-012

- [x] HU-012-V (RF-02-4) Revisar código y evidencia existente frente a los criterios de la historia.
- [x] HU-012-B (RF-02-4) Completar dominio, transacciones, autorización y API requeridos.
- [x] HU-012-U (RF-02-4) Completar la pantalla conectada al servidor con validaciones y estados vacíos.
- [x] HU-012-P (RF-02-4) Verificar «Identificar rol» con los criterios de [HU-012](spec.md#hu-012-identificar-los-roles-del-usuario-autenticado). Registrar resultado y evidencia de cada criterio, incluidos los rechazos aplicables.
- [x] HU-012-D (RF-02-4) Actualizar trazabilidad, documentación y resultado de aceptación.

## Sprint 2 HU-014

- [x] HU-014-V (RF-02-6) Revisar código y evidencia existente frente a los criterios de la historia.
- [x] HU-014-B (RF-02-6) Completar dominio, transacciones, autorización y API requeridos.
- [x] HU-014-U (RF-02-6) Completar la pantalla conectada al servidor con validaciones y estados vacíos.
- [x] HU-014-P (RF-02-6) Verificar «Autorizar acceso según rol» con los criterios de [HU-014](spec.md#hu-014-autorizar-el-acceso-según-rol-en-el-servidor). Registrar resultado y evidencia de cada criterio, incluidos los rechazos aplicables.
- [x] HU-014-D (RF-02-6) Actualizar trazabilidad, documentación y resultado de aceptación.

## Sprint 1 HU-015

- [x] HU-015-V (RF-02-7) Revisar código y evidencia existente frente a los criterios de la historia.
- [x] HU-015-B (RF-02-7) Completar dominio, transacciones, autorización y API requeridos. Aplicar la restricción de `Sesion.revocada_en` definida en [data-model.md](data-model.md).
- [x] HU-015-U (RF-02-7) Completar la pantalla conectada al servidor con validaciones y estados vacíos.
- [x] HU-015-P (RF-02-7) Verificar «Cerrar sesión» con los criterios de [HU-015](spec.md#hu-015-cerrar-sesión-e-invalidarla-en-el-servidor). Registrar resultado y evidencia de cada criterio, incluidos los rechazos aplicables.
- [x] HU-015-D (RF-02-7) Actualizar trazabilidad, documentación y resultado de aceptación.
