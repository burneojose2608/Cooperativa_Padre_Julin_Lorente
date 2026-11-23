# Tareas de beneficios y recompensas

Conservar el sprint planificado y la relación padre de cada ítem. No sumar otra vez los puntos de las subtareas incluidos en la historia consolidada.

La [evidencia por criterio](aceptacion.md) documenta la aceptación técnica local verificada en PostgreSQL aislado y Vitest.

## Sprint 3 HU-054

- [x] HU-054-V (RF-08-1) Revisar código y evidencia existente frente a los criterios de la historia.
- [x] HU-054-B (RF-08-1) Completar dominio, transacciones, autorización y API requeridos.
- [x] HU-054-U (RF-08-1) Completar la pantalla conectada al servidor con validaciones y estados vacíos.
- [x] HU-054-P (RF-08-1) Verificar «Configurar beneficios» con los criterios de [HU-054](spec.md#hu-054-configurar-beneficios). Registrar resultado y evidencia de cada criterio, incluidos los rechazos aplicables.
- [x] HU-054-D (RF-08-1) Actualizar trazabilidad, documentación y resultado de aceptación.

## Sprint 4 HU-055

- [x] HU-055-V (RF-08-2) Revisar código y evidencia existente frente a los criterios de la historia.
- [x] HU-055-B (RF-08-2) Completar dominio, transacciones, autorización y API requeridos. Aplicar la restricción de `Canje.clave` definida en [data-model.md](data-model.md).
- [x] HU-055-U (RF-08-2) Completar la pantalla conectada al servidor con validaciones y estados vacíos.
- [x] HU-055-P (RF-08-2, RF-08-3, RF-08-6) Verificar en [HU-055](spec.md#hu-055-solicitar-canjes-con-reserva-descuento-y-liberación-segura-de-puntos) la reserva con saldo, stock y convenio válidos. Repetir con la misma clave, competir por saldo y stock y comparar movimientos al aprobar, rechazar y entregar. Confirmar que la aprobación descuenta una vez y el rechazo devuelve puntos y stock.
- [x] HU-055-D (RF-08-2) Actualizar trazabilidad, documentación y resultado de aceptación.

## Sprint 4 HU-056

- [x] HU-056-V (RF-08-3) Revisar código y evidencia existente frente a los criterios de la historia.
- [x] HU-056-B (RF-08-3) Completar dominio, transacciones, autorización y API requeridos.
- [x] HU-056-U (RF-08-3) Completar la pantalla conectada al servidor con validaciones y estados vacíos.
- [x] HU-056-P (RF-08-3) Verificar «Gestionar y entregar canjes» con los criterios de [HU-056](spec.md#hu-056-gestionar-y-entregar-canjes). Registrar resultado y evidencia de cada criterio, incluidos los rechazos aplicables.
- [x] HU-056-D (RF-08-3) Actualizar trazabilidad, documentación y resultado de aceptación.

## Sprint 3 HU-057

- [x] HU-057-V (RF-08-4) Revisar código y evidencia existente frente a los criterios de la historia.
- [x] HU-057-B (RF-08-4) Completar dominio, transacciones, autorización y API requeridos.
- [x] HU-057-U (RF-08-4) Completar la pantalla conectada al servidor con validaciones y estados vacíos.
- [x] HU-057-P (RF-08-4) Verificar «Consultar beneficios disponibles» con los criterios de [HU-057](spec.md#hu-057-consultar-beneficios-disponibles). Registrar resultado y evidencia de cada criterio, incluidos los rechazos aplicables.
- [x] HU-057-D (RF-08-4) Actualizar trazabilidad, documentación y resultado de aceptación.

## Sprint 4 HU-058

- [x] HU-058-V (RF-08-5) Revisar código y evidencia existente frente a los criterios de la historia.
- [x] HU-058-B (RF-08-5) Completar dominio, transacciones, autorización y API requeridos.
- [x] HU-058-U (RF-08-5) Completar la pantalla conectada al servidor con validaciones y estados vacíos.
- [x] HU-058-P (RF-08-5) Verificar «Consultar historial de canjes» con los criterios de [HU-058](spec.md#hu-058-consultar-historial-de-canjes). Registrar resultado y evidencia de cada criterio, incluidos los rechazos aplicables.
- [x] HU-058-D (RF-08-5) Actualizar trazabilidad, documentación y resultado de aceptación.

## Sprint 4 HU-059

- [x] HU-059-V (RF-08-6) Revisar código y evidencia existente frente a los criterios de la historia.
- [x] HU-059-B (RF-08-6) Completar dominio, transacciones, autorización y API requeridos.
- [x] HU-059-U (RF-08-6) Completar la pantalla conectada al servidor con validaciones y estados vacíos.
- [x] HU-059-P (RF-08-6) Verificar «Reservar y descontar puntos» con los criterios de [HU-059](spec.md#hu-059-reservar-descontar-y-liberar-puntos-de-canjes). Registrar resultado y evidencia de cada criterio, incluidos los rechazos aplicables.
- [x] HU-059-D (RF-08-6) Actualizar trazabilidad, documentación y resultado de aceptación.

## Phase 1: Convergence

- [x] T001 Completar pruebas de edición y desactivación de beneficios, filtrado del catálogo de disponibles y filtrado por estado en el historial de canjes, y documentar `specs/008-recompensas/aceptacion.md` según RF-08-1 a RF-08-6 (partial)
