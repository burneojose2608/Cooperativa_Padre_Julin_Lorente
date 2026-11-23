# Tareas de sorteos

Conservar el sprint planificado y la relación padre de cada ítem. No sumar otra vez los puntos de las subtareas incluidos en la historia consolidada.

La [evidencia por criterio](aceptacion.md) documenta la aceptación técnica local verificada en PostgreSQL aislado y Vitest.

## Sprint 3 HU-048

- [x] HU-048-V (RF-07-1) Revisar código y evidencia existente frente a los criterios de la historia.
- [x] HU-048-B (RF-07-1) Completar dominio, transacciones, autorización y API requeridos.
- [x] HU-048-U (RF-07-1) Completar la pantalla conectada al servidor con validaciones y estados vacíos.
- [x] HU-048-P (RF-07-1) Verificar «Configurar sorteo» con los criterios de [HU-048](spec.md#hu-048-configurar-sorteos). Registrar resultado y evidencia de cada criterio, incluidos los rechazos aplicables.
- [x] HU-048-D (RF-07-1) Actualizar trazabilidad, documentación y resultado de aceptación.

## Sprint 4 HU-049

- [x] HU-049-V (RF-07-2) Revisar código y evidencia existente frente a los criterios de la historia.
- [x] HU-049-B (RF-07-2) Completar dominio, transacciones, autorización y API requeridos.
- [x] HU-049-U (RF-07-2) Completar la pantalla conectada al servidor con validaciones y estados vacíos.
- [x] HU-049-P (RF-07-2) Verificar «Generar participaciones» con los criterios de [HU-049](spec.md#hu-049-generar-participaciones-en-sorteos). Registrar resultado y evidencia de cada criterio, incluidos los rechazos aplicables.
- [x] HU-049-D (RF-07-2) Actualizar trazabilidad, documentación y resultado de aceptación.

## Sprint 5 HU-050

- [x] HU-050-V (RF-07-3) Revisar código y evidencia existente frente a los criterios de la historia.
- [x] HU-050-B (RF-07-3) Completar dominio, transacciones, autorización y API requeridos.
- [x] HU-050-U (RF-07-3) Completar la pantalla conectada al servidor con validaciones y estados vacíos.
- [x] HU-050-P (RF-07-3) Verificar «Ejecutar sorteo y registrar ganadores» con los criterios de [HU-050](spec.md#hu-050-ejecutar-sorteos-notificar-ganadores-y-auditar-resultados). Registrar resultado y evidencia de cada criterio, incluidos los rechazos aplicables.
- [x] HU-050-D (RF-07-3) Actualizar trazabilidad, documentación y resultado de aceptación.

## Sprint 5 HU-051

- [x] HU-051-V (RF-07-4) Revisar código y evidencia existente frente a los criterios de la historia.
- [x] HU-051-B (RF-07-4) Completar dominio, transacciones, autorización y API requeridos.
- [x] HU-051-U (RF-07-4) Completar la pantalla conectada al servidor con validaciones y estados vacíos.
- [x] HU-051-P (RF-07-4) Verificar «Consultar resultados» con los criterios de [HU-051](spec.md#hu-051-consultar-resultados-de-sorteos). Registrar resultado y evidencia de cada criterio, incluidos los rechazos aplicables.
- [x] HU-051-D (RF-07-4) Actualizar trazabilidad, documentación y resultado de aceptación.

## Sprint 5 HU-052

- [x] HU-052-V (RF-07-5) Revisar código y evidencia existente frente a los criterios de la historia.
- [x] HU-052-B (RF-07-5) Completar dominio, transacciones, autorización y API requeridos.
- [x] HU-052-U (RF-07-5) Completar la pantalla conectada al servidor con validaciones y estados vacíos.
- [x] HU-052-P (RF-07-5) Verificar «Notificar ganadores» con los criterios de [HU-052](spec.md#hu-052-notificar-a-los-ganadores). Registrar resultado y evidencia de cada criterio, incluidos los rechazos aplicables.
- [x] HU-052-D (RF-07-5) Actualizar trazabilidad, documentación y resultado de aceptación.

## Sprint 5 HU-053

- [x] HU-053-V (RF-07-6) Revisar código y evidencia existente frente a los criterios de la historia.
- [x] HU-053-B (RF-07-6) Completar dominio, transacciones, autorización y API requeridos.
- [x] HU-053-U (RF-07-6) Completar la pantalla conectada al servidor con validaciones y estados vacíos.
- [x] HU-053-P (RF-07-6) Verificar «Consultar historial de sorteos» con los criterios de [HU-053](spec.md#hu-053-consultar-el-historial-de-sorteos). Registrar resultado y evidencia de cada criterio, incluidos los rechazos aplicables.
- [x] HU-053-D (RF-07-6) Actualizar trazabilidad, documentación y resultado de aceptación.

## Phase 1: Convergence

- [x] T001 Mostrar la evidencia de auditoría (hash SHA-256 de la lista congelada y conteo de participantes elegibles) al personal autorizado en la vista de sorteos ejecutados según RF-07-6 y HU-053 (partial)
- [x] T002 Completar pruebas de aceptación de configuración de sorteos, generación sin duplicados, ejecución con ganadores y suplentes, notificación con premio y condiciones, y consulta de historial/resultados, documentando `specs/007-sorteos/aceptacion.md` según RF-07-1 a RF-07-6 (partial)
