# Relaciones y dependencias revisadas

Las multiplicidades junto a A cuentan cuántos A corresponden a un B; las de B, cuántos B corresponden a un A. Las asociaciones derivadas o de consulta se señalan en su significado; no afirman persistencia física.

| ID | A | mult A | B | mult B | Tipo | Significado y justificación | Fuente |
|---|---|---|---|---|---|---|---|
| REL-001 | Usuario | 1 | Socio | 0..1 | Asociación | cuenta de la condición de socio; asociación sin propiedad de ciclo de vida | decision-cedula-diez-digitos.md; decision-registro-general.md; registro_service.py; SQL 05–06 |
| REL-002 | Usuario | 0..* | Rol | 0..* | Asociación | roles asignados, sin herencia; asociación sin propiedad de ciclo de vida | HU-009/010/012/014/015; roles_service.py; sesiones_service.py |
| REL-003 | Rol | 0..* | Permiso | 0..* | Asociación | capacidades concedidas; asociación sin propiedad de ciclo de vida | HU-009/010/012/014/015; roles_service.py; sesiones_service.py |
| REL-004 | Usuario | 1 | ConsentimientoCuenta | 1..* | Asociación | aceptaciones versionadas de la cuenta; asociación sin propiedad de ciclo de vida | HU-001/023; RNF-02/25; SQL 02; consentimiento.py |
| REL-005 | Usuario | 1 | Sesion | 0..* | Asociación | sesiones de la cuenta; asociación sin propiedad de ciclo de vida | HU-009/010/012/014/015; roles_service.py; sesiones_service.py; HU-011; recuperacion_service.py; token_recuperacion.py; SQL 03; test_recuperacion.py y test_sprint1_sesiones.py |
| REL-006 | Usuario | 1 | RecuperacionAcceso | 0..* | Asociación | solicitudes de recuperación; asociación sin propiedad de ciclo de vida | HU-011; recuperacion_service.py; token_recuperacion.py; SQL 03; test_recuperacion.py y test_sprint1_sesiones.py |
| REL-007 | Usuario | 0..1 | EventoAuditoria | 0..* | Asociación | actor de evento; anónimo permitido; asociación sin propiedad de ciclo de vida | conversion-administrativa-temporal.md; conversion_socio_service.py; HU-087–091; RNF-06/13/14; SQL 01–02 |
| REL-008 | Usuario | 0..1 | CambioEstado | 0..* | Asociación | responsable del cambio; sistema permitido; asociación sin propiedad de ciclo de vida | HU-016/017/018/020/024; SQL 01; CU-G04/G15/G16; HU-087–091; RNF-06/13/14; SQL 01–02 |
| REL-009 | Socio | 1 | CodigoReferido | 0..* | Asociación | códigos históricos; como máximo uno activo; asociación sin propiedad de ciclo de vida | HU-016/017/018/020/024; SQL 01; CU-G04/G15/G16 |
| REL-010 | CodigoReferido | 1 | Referido | 0..* | Asociación | código utilizado al registrar; asociación sin propiedad de ciclo de vida | HU-016/017/018/020/024; SQL 01; CU-G04/G15/G16 |
| REL-011 | Prospecto | 1 | Referido | 0..* | Asociación | historial; a lo sumo un referido activo; asociación sin propiedad de ciclo de vida | HU-001/023; RNF-02/25; SQL 02; consentimiento.py; HU-016/017/018/020/024; SQL 01; CU-G04/G15/G16 |
| REL-012 | Referido | 1 | ConsentimientoProspecto | 0..* | Asociación | solicitudes y evidencia versionada; a lo sumo una confirmación vigente; asociación sin propiedad de ciclo de vida | HU-001/023; RNF-02/25; SQL 02; consentimiento.py |
| REL-013 | Referido | 1 | Conversion | 0..1 | Asociación | hecho de conversión; también único por prospecto; asociación sin propiedad de ciclo de vida | HU-016/017/018/020/024; SQL 01; CU-G04/G15/G16 |
| REL-014 | Usuario | 1 | Conversion | 0..* | Asociación | responsable que valida evidencia comercial; asociación sin propiedad de ciclo de vida | HU-016/017/018/020/024; SQL 01; CU-G04/G15/G16; HU-087–091; RNF-06/13/14; SQL 01–02 |
| REL-015 | Campana | 0..1 | Referido | 0..* | Asociación | campaña cuando corresponde; asociación sin propiedad de ciclo de vida | HU-001/023; RNF-02/25; SQL 02; consentimiento.py; HU-016/017/018/020/024; SQL 01; CU-G04/G15/G16 |
| REL-016 | Usuario | 1 | Campana | 0..* | Asociación | creador autorizado; asociación sin propiedad de ciclo de vida | HU-025–030; Presentacion RF-04; SQL 01–02 |
| REL-017 | Campana | 0..* | Segmento | 0..* | Asociación | público objetivo; asociación sin propiedad de ciclo de vida | HU-025–030; Presentacion RF-04; SQL 01–02 |
| REL-018 | Campana | 1 | IncentivoCampana | 0..* | Asociación | condiciones de reconocimiento por versión; asociación sin propiedad de ciclo de vida | HU-025–030; Presentacion RF-04; SQL 01–02 |
| REL-019 | Campana | 1 | ParticipacionCampana | 0..* | Asociación | participaciones para monitoreo; asociación sin propiedad de ciclo de vida | HU-025–030; Presentacion RF-04; SQL 01–02 |
| REL-020 | Socio | 1 | ParticipacionCampana | 0..* | Asociación | participante validado; asociación sin propiedad de ciclo de vida | HU-025–030; Presentacion RF-04; SQL 01–02 |
| REL-021 | Socio | 1 | CuentaPuntos | 1 | Asociación | cuenta conceptual de puntos; asociación sin propiedad de ciclo de vida | HU-031/032/036/038/059; SQL 01; HU-055/059; CU reservar sin doble débito; SQL 01; decisión P07; HU-054–059; SQL 01–02 |
| REL-022 | CuentaPuntos | 1 | MovimientoPuntos | 0..* | Asociación | libro inmutable del socio; asociación sin propiedad de ciclo de vida | HU-031/032/036/038/059; SQL 01; HU-055/059; CU reservar sin doble débito; SQL 01; decisión P07 |
| REL-023 | ReglaPuntos | 0..1 | MovimientoPuntos | 0..* | Asociación | regla aplicada cuando hay acreditación; asociación sin propiedad de ciclo de vida | HU-031/032/036/038/059; SQL 01 |
| REL-024 | ActividadValidada | 0..1 | MovimientoPuntos | 0..* | Asociación | origen de reconocimiento; canjes/reversos usan sus enlaces específicos; asociación sin propiedad de ciclo de vida | HU-031/032/036/038/059; SQL 01 |
| REL-025 | Socio | 1 | ActividadValidada | 0..* | Asociación | beneficiario del hecho reconocido; asociación sin propiedad de ciclo de vida | HU-031/032/036/038/059; SQL 01 |
| REL-026 | MovimientoPuntos | 0..1 | MovimientoPuntos | 0..* | Asociación | original del reverso; validar no exceder importe reversible; asociación sin propiedad de ciclo de vida | HU-031/032/036/038/059; SQL 01; HU-055/059; CU reservar sin doble débito; SQL 01; decisión P07; HU-087–091; RNF-06/13/14; SQL 01–02 |
| REL-027 | CuentaPuntos | 0..* | Nivel | 0..1 | Asociación | nivel derivado; base de puntos y descensos pendientes P06; asociación sin propiedad de ciclo de vida | HU-033/035/037/083 |
| REL-028 | Socio | 1 | InsigniaObtenida | 0..* | Asociación | logros propios; asociación sin propiedad de ciclo de vida | HU-033/035/037/083 |
| REL-029 | Insignia | 1 | InsigniaObtenida | 0..* | Asociación | tipo de logro obtenido una vez por socio; asociación sin propiedad de ciclo de vida | HU-033/035/037/083 |
| REL-030 | Socio | 1 | PerfilPublico | 0..1 | Asociación | privacidad y alias; valores seguros por defecto al faltar; asociación sin propiedad de ciclo de vida | HU-033/035/037/083; HU-060–065/079–083; SQL 01–02 |
| REL-031 | Capacitacion | 1 | ModuloCapacitacion | 1..* | Composición | pertenencia exclusiva; composición conceptual; pertenencia exclusiva y ciclo de configuración; preservar evidencia histórica antes de retirar | HU-039–047; SQL 01–02 |
| REL-032 | ModuloCapacitacion | 0..* | MaterialEducativo | 0..* | Asociación | material reutilizable; asociación sin propiedad de ciclo de vida | HU-060–065/079–083; SQL 01–02 |
| REL-033 | Socio | 1 | InscripcionCapacitacion | 0..* | Asociación | inscrito, único por capacitación; asociación sin propiedad de ciclo de vida | HU-039–047; SQL 01–02 |
| REL-034 | Capacitacion | 1 | InscripcionCapacitacion | 0..* | Asociación | oferta elegida; asociación sin propiedad de ciclo de vida | HU-039–047; SQL 01–02 |
| REL-035 | InscripcionCapacitacion | 1 | ProgresoModulo | 0..* | Asociación | avance de la persona; asociación sin propiedad de ciclo de vida | HU-039–047; SQL 01–02 |
| REL-036 | ModuloCapacitacion | 1 | ProgresoModulo | 0..* | Asociación | unidad completada; pertenece a la misma capacitación; asociación sin propiedad de ciclo de vida | HU-039–047; SQL 01–02 |
| REL-037 | Capacitacion | 1 | Evaluacion | 0..* | Asociación | evaluaciones de la capacitación; SQL 01 permite varias, una final no aprobada; asociación sin propiedad de ciclo de vida | HU-039–047; SQL 01–02 |
| REL-038 | InscripcionCapacitacion | 1 | IntentoEvaluacion | 0..* | Asociación | intentos del inscrito; asociación sin propiedad de ciclo de vida | HU-039–047; SQL 01–02 |
| REL-039 | Evaluacion | 1 | IntentoEvaluacion | 0..* | Asociación | evaluación rendida; asociación sin propiedad de ciclo de vida | HU-039–047; SQL 01–02; HU-041/072/074; SQL 02, ck_pregunta_dueno |
| REL-040 | InscripcionCapacitacion | 1 | Certificado | 0..1 | Asociación | certificado tras aprobación; asociación sin propiedad de ciclo de vida | HU-039–047; SQL 01–02 |
| REL-041 | Evaluacion | 0..1 | Pregunta | 0..* | Asociación | propietario exclusivo XOR Juego; asociación sin propiedad de ciclo de vida | HU-041/072/074; SQL 02, ck_pregunta_dueno |
| REL-042 | Juego | 0..1 | Pregunta | 0..* | Asociación | propietario exclusivo XOR Evaluacion; asociación sin propiedad de ciclo de vida | HU-041/072/074; SQL 02, ck_pregunta_dueno |
| REL-043 | Pregunta | 1 | OpcionPregunta | 0..* | Composición | alternativas exclusivas; composición conceptual; pertenencia exclusiva y ciclo de configuración; preservar evidencia histórica antes de retirar | HU-041/072/074; SQL 02, ck_pregunta_dueno |
| REL-044 | Pregunta | 1 | RespuestaActividad | 0..* | Asociación | pregunta respondida; asociación sin propiedad de ciclo de vida | HU-041/072/074; SQL 02, ck_pregunta_dueno |
| REL-045 | IntentoEvaluacion | 0..1 | RespuestaActividad | 0..* | Asociación | propietario de respuesta XOR Partida; asociación sin propiedad de ciclo de vida | HU-041/072/074; SQL 02, ck_pregunta_dueno |
| REL-046 | Partida | 0..1 | RespuestaActividad | 0..* | Asociación | propietario de respuesta XOR IntentoEvaluacion; asociación sin propiedad de ciclo de vida | HU-041/072/074; SQL 02, ck_pregunta_dueno |
| REL-047 | Socio | 1 | InscripcionTaller | 0..* | Asociación | inscripción/asistencia única por taller; asociación sin propiedad de ciclo de vida | HU-039–047; SQL 01–02 |
| REL-048 | Taller | 1 | InscripcionTaller | 0..* | Asociación | asistencia con cupo controlado; asociación sin propiedad de ciclo de vida | HU-039–047; SQL 01–02 |
| REL-049 | Usuario | 0..1 | InscripcionTaller | 0..* | Asociación | responsable que confirma asistencia; asociación sin propiedad de ciclo de vida | HU-039–047; SQL 01–02 |
| REL-050 | Campana | 1 | Sorteo | 0..* | Asociación | campaña de sorteo según SQL; obligatoriedad pendiente P04; asociación sin propiedad de ciclo de vida | HU-048–053; SQL 01–02 |
| REL-051 | Sorteo | 1 | ParticipacionSorteo | 0..* | Asociación | participaciones registradas; asociación sin propiedad de ciclo de vida | HU-048–053; SQL 01–02 |
| REL-052 | Socio | 1 | ParticipacionSorteo | 0..* | Asociación | socio participante; asociación sin propiedad de ciclo de vida | HU-048–053; SQL 01–02 |
| REL-053 | ActividadValidada | 1 | ParticipacionSorteo | 0..* | Asociación | origen validado de participación; asociación sin propiedad de ciclo de vida | HU-048–053; SQL 01–02 |
| REL-054 | Sorteo | 1 | PremioSorteo | 1..* | Asociación | premios del sorteo; asociación sin propiedad de ciclo de vida | HU-048–053; SQL 01–02 |
| REL-055 | Sorteo | 1 | EvidenciaSorteo | 0..1 | Asociación | lista y evidencia tras congelación; asociación sin propiedad de ciclo de vida | HU-048–053; SQL 01–02 |
| REL-056 | Sorteo | 1 | ResultadoSorteo | 0..* | Asociación | ganadores y suplentes, antes de ejecución vacío; asociación sin propiedad de ciclo de vida | HU-048–053; SQL 01–02 |
| REL-057 | ParticipacionSorteo | 1 | ResultadoSorteo | 0..1 | Asociación | participación seleccionada del mismo sorteo; asociación sin propiedad de ciclo de vida | HU-048–053; SQL 01–02 |
| REL-058 | PremioSorteo | 0..1 | ResultadoSorteo | 0..* | Asociación | premio para ganador; suplente puede no tener asignación, política de adjudicación pendiente; asociación sin propiedad de ciclo de vida | HU-048–053; SQL 01–02 |
| REL-059 | Socio | 1 | Canje | 0..* | Asociación | solicitudes propias; asociación sin propiedad de ciclo de vida | HU-055/059; CU reservar sin doble débito; SQL 01; decisión P07; HU-054–059; SQL 01–02 |
| REL-060 | Beneficio | 1 | Canje | 0..* | Asociación | beneficio solicitado; asociación sin propiedad de ciclo de vida | HU-054–059; SQL 01–02 |
| REL-061 | Canje | 0..1 | MovimientoPuntos | 0..* | Asociación | reserva, descuento o liberación del canje; asociación sin propiedad de ciclo de vida | HU-055/059; CU reservar sin doble débito; SQL 01; decisión P07 |
| REL-062 | Usuario | 0..1 | Canje | 0..* | Asociación | responsable de decisión; asociación sin propiedad de ciclo de vida | HU-055/059; CU reservar sin doble débito; SQL 01; decisión P07; HU-054–059; SQL 01–02 |
| REL-063 | Usuario | 0..1 | Canje | 0..* | Asociación | responsable de entrega, rol separado de aprobación; asociación sin propiedad de ciclo de vida | HU-055/059; CU reservar sin doble débito; SQL 01; decisión P07; HU-054–059; SQL 01–02 |
| REL-064 | ConvenioBienestar | 0..1 | Beneficio | 0..* | Asociación | origen del beneficio, opcional; asociación sin propiedad de ciclo de vida | Acta, alcance; HU-084–086; RNF-24 |
| REL-065 | Usuario | 1 | ContenidoInstitucional | 0..* | Asociación | autor o gestor; asociación sin propiedad de ciclo de vida | HU-060–065/079–083; SQL 01–02 |
| REL-066 | ContenidoInstitucional | 1 | AprobacionContenido | 0..* | Asociación | decisiones versionadas de aprobación opcional; asociación sin propiedad de ciclo de vida | HU-060–065/079–083; SQL 01–02 |
| REL-067 | Usuario | 1 | AprobacionContenido | 0..* | Asociación | responsable designado; asociación sin propiedad de ciclo de vida | HU-060–065/079–083; SQL 01–02 |
| REL-068 | ContenidoInstitucional | 1 | MaterialEducativo | 0..* | Asociación | organización de material según diseño SQL; revisar con repositorio reutilizable; asociación sin propiedad de ciclo de vida | HU-060–065/079–083; SQL 01–02 |
| REL-069 | ContenidoInstitucional | 1 | RecursoBienestar | 0..* | Asociación | contenido informativo de bienestar; asociación sin propiedad de ciclo de vida | Acta, alcance; HU-084–086; RNF-24 |
| REL-070 | ConvenioBienestar | 0..1 | RecursoBienestar | 0..* | Asociación | convenio asociado cuando corresponde; asociación sin propiedad de ciclo de vida | Acta, alcance; HU-084–086; RNF-24 |
| REL-071 | Usuario | 1 | PreferenciaNotificacion | 0..* | Asociación | preferencias por evento y canal; asociación sin propiedad de ciclo de vida | HU-052/066–070; RNF-18; SQL 01 |
| REL-072 | Usuario | 1 | Notificacion | 0..* | Asociación | destinatario; asociación sin propiedad de ciclo de vida | HU-052/066–070; RNF-18; SQL 01 |
| REL-073 | Notificacion | 1 | EnvioNotificacion | 0..* | Asociación | entregas por canal; asociación sin propiedad de ciclo de vida | HU-052/066–070; RNF-18; SQL 01 |
| REL-074 | PlantillaNotificacion | 1 | EnvioNotificacion | 0..* | Asociación | plantilla usada para evento/canal; asociación sin propiedad de ciclo de vida | HU-052/066–070; RNF-18; SQL 01 |
| REL-075 | Socio | 1 | Partida | 0..* | Asociación | jugador; asociación sin propiedad de ciclo de vida | HU-041/072/074; SQL 02, ck_pregunta_dueno; HU-071–078; SQL 01 |
| REL-076 | Juego | 1 | Partida | 0..* | Asociación | configuración del juego; asociación sin propiedad de ciclo de vida | HU-041/072/074; SQL 02, ck_pregunta_dueno; HU-071–078; SQL 01 |
| REL-077 | Socio | 1 | ProgresoReto | 0..* | Asociación | progreso propio; asociación sin propiedad de ciclo de vida | HU-071–078; SQL 01 |
| REL-078 | Reto | 1 | ProgresoReto | 0..* | Asociación | reto medible; asociación sin propiedad de ciclo de vida | HU-071–078; SQL 01 |
| REL-079 | ReglaPuntos | 0..1 | Reto | 0..* | Asociación | regla de recompensa; referencia histórica a preservar; asociación sin propiedad de ciclo de vida | HU-071–078; SQL 01 |
| REL-080 | Socio | 1 | PublicacionComunidad | 0..* | Asociación | autor socio; asociación sin propiedad de ciclo de vida | HU-060–065/079–083; SQL 01–02 |
| REL-081 | PublicacionComunidad | 1 | Comentario | 0..* | Asociación | comentarios recibidos; asociación sin propiedad de ciclo de vida | HU-060–065/079–083; SQL 01–02 |
| REL-082 | Socio | 1 | Comentario | 0..* | Asociación | autor del comentario; asociación sin propiedad de ciclo de vida | HU-060–065/079–083; SQL 01–02 |
| REL-083 | PublicacionComunidad | 1 | Reaccion | 0..* | Asociación | reacciones recibidas; asociación sin propiedad de ciclo de vida | HU-060–065/079–083; SQL 01–02 |
| REL-084 | Socio | 1 | Reaccion | 0..* | Asociación | una por publicación según SQL; asociación sin propiedad de ciclo de vida | HU-060–065/079–083; SQL 01–02 |
| REL-085 | Socio | 1 | ReporteComunidad | 0..* | Asociación | persona que reporta; asociación sin propiedad de ciclo de vida | HU-060–065/079–083; SQL 01–02 |
| REL-086 | PublicacionComunidad | 0..1 | ReporteComunidad | 0..* | Asociación | objeto reportado XOR Comentario; asociación sin propiedad de ciclo de vida | HU-060–065/079–083; SQL 01–02 |
| REL-087 | Comentario | 0..1 | ReporteComunidad | 0..* | Asociación | objeto reportado XOR PublicacionComunidad; asociación sin propiedad de ciclo de vida | HU-060–065/079–083; SQL 01–02 |
| REL-088 | ReporteComunidad | 1 | DecisionModeracion | 0..* | Asociación | decisiones con motivo; asociación sin propiedad de ciclo de vida | HU-060–065/079–083; SQL 01–02 |
| REL-089 | Usuario | 1 | DecisionModeracion | 0..* | Asociación | gestor autorizado; asociación sin propiedad de ciclo de vida | HU-060–065/079–083; SQL 01–02 |
| REL-090 | Socio | 0..1 | DecisionModeracion | 0..* | Asociación | socio afectado si hay suspensión temporal; asociación sin propiedad de ciclo de vida | HU-060–065/079–083; SQL 01–02 |
| REL-091 | FiltroReporte | 1 | ResultadoReporte | 0..* | Asociación | filtros aplicados al resultado; asociación sin propiedad de ciclo de vida | HU-087–091; RNF-06/13/14; SQL 01–02 |
| REL-092 | EvidenciaSorteo | 1 | ElegibleCongelado | 0..* | Asociación | entradas congeladas preservadas con su evidencia; ejecución requiere conjunto no vacío; asociación sin propiedad de ciclo de vida | HU-048–053; SQL 01–02 |
| REL-093 | ParticipacionSorteo | 1 | ElegibleCongelado | 0..1 | Asociación | participación de origen identificable aunque cambie elegibilidad posterior; asociación sin propiedad de ciclo de vida | HU-048–053; SQL 01–02 |
| REL-094 | IncentivoCampana | 1 | ReconocimientoIncentivo | 0..* | Asociación | versión que originó condiciones reconocidas; no se modifica retroactivamente; asociación sin propiedad de ciclo de vida | HU-025–030; Presentacion RF-04; SQL 01–02 |
| REL-095 | ActividadValidada | 1 | ReconocimientoIncentivo | 0..* | Asociación | hecho que fundamenta incentivo; unicidad por actividad, beneficiario e incentivo; asociación sin propiedad de ciclo de vida | HU-025–030; Presentacion RF-04; SQL 01–02 |
| REL-096 | ReconocimientoIncentivo | 0..1 | MovimientoPuntos | 0..* | Asociación | origen promocional cuando aplica; no exige puntos a todo incentivo; asociación sin propiedad de ciclo de vida | HU-031/032/036/038/059; SQL 01; HU-055/059; CU reservar sin doble débito; SQL 01; decisión P07; HU-087–091; RNF-06/13/14; SQL 01–02 |
| REL-097 | Referido | 0..1 | CambioEstado | 0..* | Asociación | historial propio conservado; sujeto exclusivo XOR campaña/canje/usuario; asociación sin propiedad de ciclo de vida | HU-016/017/018/020/024; SQL 01; CU-G04/G15/G16 |
| REL-098 | Campana | 0..1 | CambioEstado | 0..* | Asociación | historial propio conservado; sujeto exclusivo XOR referido/canje/usuario; asociación sin propiedad de ciclo de vida | HU-016/017/018/020/024; SQL 01; CU-G04/G15/G16; HU-087–091; RNF-06/13/14; SQL 01–02 |
| REL-099 | Canje | 0..1 | CambioEstado | 0..* | Asociación | historial propio conservado; sujeto exclusivo XOR referido/campaña/usuario; asociación sin propiedad de ciclo de vida | HU-016/017/018/020/024; SQL 01; CU-G04/G15/G16; HU-087–091; RNF-06/13/14; SQL 01–02 |
| REL-100 | Usuario | 0..1 | CambioEstado | 0..* | Asociación | cuenta afectada por cambio; distinto del responsable, sujeto exclusivo; asociación sin propiedad de ciclo de vida | HU-016/017/018/020/024; SQL 01; CU-G04/G15/G16; HU-087–091; RNF-06/13/14; SQL 01–02 |
| REL-101 | Campana | 0..1 | FiltroReporte | 0..* | Asociación | campaña seleccionada opcionalmente como filtro de consulta; asociación sin propiedad de ciclo de vida | HU-087–091; RNF-06/13/14; SQL 01–02 |
| REL-102 | Segmento | 0..1 | FiltroReporte | 0..* | Asociación | segmento seleccionado opcionalmente como filtro de consulta; asociación sin propiedad de ciclo de vida | HU-087–091; RNF-06/13/14; SQL 01–02 |
| REL-103 | Usuario | 1 | EvidenciaSorteo | 0..* | Asociación | responsable de ejecución que queda conservado en la evidencia del sorteo; asociación sin propiedad de ciclo de vida | HU-048–053; SQL 01–02 |

## Dependencias de coordinación y consulta

| ID | Cliente | Proveedor | Responsabilidad | Fuente |
|---|---|---|---|---|
| DEP-001 | ValidacionAdministrativaSocio | EntradaPadron | consulta/añade confirmación temporal autorizada | conversion-administrativa-temporal.md; conversion_socio_service.py |
| DEP-002 | ValidacionAdministrativaSocio | Socio | habilita condición, no conversión comercial | conversion-administrativa-temporal.md; conversion_socio_service.py |
| DEP-003 | RecuperacionAcceso | Sesion | revoca sesiones al restablecer | HU-011; recuperacion_service.py; token_recuperacion.py; SQL 03; test_recuperacion.py y test_sprint1_sesiones.py |
| DEP-004 | Referido | EntradaPadron | descarta prospecto ya socio | HU-001/023; RNF-02/25; SQL 02; consentimiento.py; HU-016/017/018/020/024; SQL 01; CU-G04/G15/G16 |
| DEP-005 | Referido | ActividadValidada | conversión validada produce actividad | HU-001/023; RNF-02/25; SQL 02; consentimiento.py; HU-016/017/018/020/024; SQL 01; CU-G04/G15/G16 |
| DEP-006 | IntentoEvaluacion | ActividadValidada | aprobación produce actividad | HU-039–047; SQL 01–02; HU-041/072/074; SQL 02, ck_pregunta_dueno |
| DEP-007 | InscripcionTaller | ActividadValidada | asistencia produce actividad | HU-039–047; SQL 01–02 |
| DEP-008 | Partida | ActividadValidada | resultado válido produce actividad | HU-041/072/074; SQL 02, ck_pregunta_dueno; HU-071–078; SQL 01 |
| DEP-009 | ProgresoReto | ActividadValidada | cumplimiento produce actividad | HU-071–078; SQL 01 |
| DEP-010 | Canje | CuentaPuntos | coordina reserva/descuento/liberación | HU-055/059; CU reservar sin doble débito; SQL 01; decisión P07; HU-054–059; SQL 01–02 |
| DEP-011 | Clasificacion | CuentaPuntos | consulta puntos con política pendiente | HU-033/035/037/083 |
| DEP-012 | Clasificacion | PerfilPublico | respeta alias y exclusión | HU-033/035/037/083 |
| DEP-013 | ServicioReportes | Referido | consulta captación | HU-087–091; RNF-06/13/14; SQL 01–02 |
| DEP-014 | ServicioReportes | Campana | consulta resultados | HU-087–091; RNF-06/13/14; SQL 01–02 |
| DEP-015 | ServicioReportes | InscripcionCapacitacion | consulta formación | HU-087–091; RNF-06/13/14; SQL 01–02 |
| DEP-016 | ServicioReportes | Certificado | consulta certificados | HU-087–091; RNF-06/13/14; SQL 01–02 |
| DEP-017 | ServicioReportes | MovimientoPuntos | consulta puntos | HU-087–091; RNF-06/13/14; SQL 01–02 |
| DEP-018 | ServicioReportes | Canje | consulta recompensas | HU-087–091; RNF-06/13/14; SQL 01–02 |
| DEP-019 | ServicioReportes | ResultadoSorteo | consulta resultados enmascarados | HU-087–091; RNF-06/13/14; SQL 01–02 |
| DEP-020 | ServicioReportes | Usuario | autoriza según roles vigentes | HU-087–091; RNF-06/13/14; SQL 01–02 |
| DEP-021 | ServicioReportes | ResultadoReporte | genera salida y aplica privacidad | HU-087–091; RNF-06/13/14; SQL 01–02 |
| DEP-022 | CuentaPuntos | Notificacion | comunica reconocimientos | HU-031/032/036/038/059; SQL 01; HU-055/059; CU reservar sin doble débito; SQL 01; decisión P07; HU-054–059; SQL 01–02 |
| DEP-023 | Sorteo | Notificacion | comunica ganadores | HU-048–053; SQL 01–02 |
| DEP-024 | DecisionModeracion | Usuario | aplica suspensión autorizada cuando corresponde | HU-060–065/079–083; SQL 01–02 |
| DEP-025 | ControlAcceso | Usuario | comprueba credenciales y estado; conserva contador en la cuenta | HU-009/010/012/014/015; roles_service.py; sesiones_service.py |
| DEP-026 | ControlAcceso | Sesion | abre sesión revocable | HU-009/010/012/014/015; roles_service.py; sesiones_service.py |
| DEP-027 | ControlAcceso | EventoAuditoria | registra éxito o rechazo | HU-009/010/012/014/015; roles_service.py; sesiones_service.py |
| DEP-028 | ServicioRegistro | Usuario | valida unicidad y registra cuenta | decision-cedula-diez-digitos.md; decision-registro-general.md; registro_service.py; SQL 05–06 |
| DEP-029 | ServicioRegistro | EntradaPadron | consulta estado sin interpretar fallo como ausencia | decision-cedula-diez-digitos.md; decision-registro-general.md; registro_service.py; SQL 05–06 |
| DEP-030 | ServicioRegistro | ConsentimientoCuenta | exige y conserva aceptación | decision-cedula-diez-digitos.md; decision-registro-general.md; registro_service.py; SQL 05–06 |
| DEP-031 | ServicioRegistro | Socio | habilita solo ante padrón activo | decision-cedula-diez-digitos.md; decision-registro-general.md; registro_service.py; SQL 05–06 |
| DEP-032 | ServicioRegistro | Rol | asigna roles autorizados | decision-cedula-diez-digitos.md; decision-registro-general.md; registro_service.py; SQL 05–06 |
| DEP-033 | ServicioRegistro | EventoAuditoria | conserva evidencia del alta | decision-cedula-diez-digitos.md; decision-registro-general.md; registro_service.py; SQL 05–06 |
| DEP-034 | ServicioAutorizacion | Usuario | comprueba estado y titularidad | HU-009/010/012/014/015; roles_service.py; sesiones_service.py |
| DEP-035 | ServicioAutorizacion | Rol | consulta roles vigentes | HU-009/010/012/014/015; roles_service.py; sesiones_service.py |
| DEP-036 | ServicioAutorizacion | Permiso | aplica capacidades; gestión completa planificada | HU-009/010/012/014/015; roles_service.py; sesiones_service.py |
| DEP-037 | ValidacionAdministrativaSocio | Usuario | comprueba cuenta y administrador activo | conversion-administrativa-temporal.md; conversion_socio_service.py |
| DEP-038 | ValidacionAdministrativaSocio | Rol | asigna Socio sin autoconversión | conversion-administrativa-temporal.md; conversion_socio_service.py |
| DEP-039 | ValidacionAdministrativaSocio | EventoAuditoria | audita confirmación manual temporal | conversion-administrativa-temporal.md; conversion_socio_service.py |
| DEP-040 | ServicioNotificaciones | PlantillaNotificacion | prepara aviso por evento | HU-052/066–070; RNF-18; SQL 01 |
| DEP-041 | ServicioNotificaciones | PreferenciaNotificacion | respeta canales opcionales | HU-052/066–070; RNF-18; SQL 01 |
| DEP-042 | ServicioNotificaciones | Notificacion | genera aviso | HU-052/066–070; RNF-18; SQL 01 |
| DEP-043 | ServicioNotificaciones | EnvioNotificacion | coordina entrega e historial | HU-052/066–070; RNF-18; SQL 01 |
| DEP-044 | ServicioNotificaciones | Sorteo | consulta ganadores autorizados | HU-052/066–070; RNF-18; SQL 01 |