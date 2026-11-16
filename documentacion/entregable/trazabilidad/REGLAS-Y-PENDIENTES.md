# Reglas y decisiones de la entrega

No se aprueba una política por incluirla en el modelo. Las propuestas siguen explícitamente pendientes.

## R01 Registro vigente

Cédula Texto con diez dígitos ASCII y trim exterior; sin provincia ni verificador. Unicidad de cédula y de correo/usuario normalizados. Padrón activo crea socio; ausente cuenta general sin roles; inactivo rechaza; indisponible aborta. Alta atómica.

Estado: Sustentada. Fuente: decision-cedula-diez-digitos.md; decision-registro-general.md; registro_service.py; SQL 05–06.

## R02 Roles y condición de socio

Usuario con cero o varios roles, y cero o un Socio; no herencia de actores. La autorización consulta roles actuales y titularidad. Cinco fallos bloquean quince minutos; inactividad de quince minutos invalida sesión.

Estado: Sustentada. Fuente: HU-009/010/012/014/015; roles_service.py; sesiones_service.py.

## R03 Validación temporal

Manual, confirmación estricta de administrador activo; destino general activo sin roles. Inactivo o inconsistencia rechaza. Repetición devuelve mismo socio. No cambia credenciales ni consentimiento. No reconoce puntos comerciales.

Estado: Sustentada. Fuente: conversion-administrativa-temporal.md; conversion_socio_service.py.

## R04 Consentimientos separados

Cuenta y prospecto conservan finalidad, aceptación, fecha y versión. Prospecto no exige cuenta. Sin confirmación dentro del plazo configurable expira referido; no se inventa duración ni política completa de revocación. Finalidad/versionado del prospecto aún no completos en SQL.

Estado: Parcial y propuesta explícita. Fuente: HU-001/023; RNF-02/25; SQL 02; consentimiento.py.

## R05 Referido y conversión

Código referido no equivale a codigoSocio. Evitar autorreferido, duplicado activo y prospecto ya socio. Conversión comercial con evidencia de prueba, responsable y fecha; una por prospecto y reconocimiento único. Aristas exactas del ciclo y retiro de consentimiento pendientes.

Estado: Sustentada con brecha de unicidad SQL por referido. Fuente: HU-016/017/018/020/024; SQL 01; CU-G04/G15/G16.

## R06 Campaña e incentivo

Vigencia y elegibilidad antes de participar. Cambios versionan condiciones sin alterar lo reconocido; instantánea propuesta en ReconocimientoIncentivo. Tasa de conversión según HU-030; meta requiere unidad definida. Fuente y combinación de segmentos pendientes P05.

Estado: Sustentada; estructura de instantánea propuesta. Fuente: HU-025–030; Presentacion RF-04; SQL 01–02.

## R07 Libro e idempotencia

Movimientos inmutables con cantidad positiva, tipo y origen identificable; clave de idempotencia por beneficiario/origen/tipo. Reversos compensan y referencian original, nunca lo editan. Límites por período configurables: unidad, zona horaria y efecto del reverso pendientes P16. HU-036 exige saldo no negativo; HU-038 exige motivo obligatorio y rechazar reverso que lo deje negativo. Se conserva esta regla explícita; queda pendiente la interacción con reservas abiertas, no permitir deuda.

Estado: Sustentada, detalle pendiente. Fuente: HU-031/032/036/038/059; SQL 01.

## R08 Saldos y reserva

Propuesta a validar P07: contable = acreditaciones - descuentos - reversos de acreditación; reservado = reservas abiertas; disponible = contable - reservado. Reserva no es descuento definitivo. Aprobar cierra reserva y registra un único descuento; rechazar libera. Ejemplo: 100 contable, reserva 30 => disponible 70; aprobar => contable 70, reservado 0, disponible 70. No se inventa saldo negativo, caducidad, ni política de reverso ya gastado.

Estado: Propuesta de análisis, no implementación. Fuente: HU-055/059; CU reservar sin doble débito; SQL 01; decisión P07.

## R09 Niveles y clasificación

Umbrales y criterios configurados; base acumulada/disponible, descensos, empates y períodos pendientes P06. No deducir descenso por canje. Alias y exclusión pública respetados.

Estado: Sustentada con política pendiente. Fuente: HU-033/035/037/083.

## R10 Formación y asistencia

Inscripción única socio-capacitación y socio-taller. Progreso de módulos de la misma capacitación entre cero y cien; fórmula agregada y acceso a evaluación pendientes. Calificación en servidor, umbral e intentos configurados; certificado tras aprobar con código único no secuencial. Asistencia validada por responsable, distinta de inscripción, acreditada una vez.

Estado: Sustentada; detalles pendientes. Fuente: HU-039–047; SQL 01–02.

## R11 Preguntas y respuestas

Pregunta pertenece a evaluación XOR juego; respuesta a intento XOR partida. Alternativas pertenecen exclusivamente a pregunta. SQL solo permite una correcta como máximo; emparejamiento necesita política P08 y no se simula con esta restricción.

Estado: Sustentada con brecha. Fuente: HU-041/072/074; SQL 02, ck_pregunta_dueno.

## R12 Sorteos verificables

Congelar entradas elegibles antes de selección; hash sobre contenido canónico congelado, registrar método, fecha, responsable, ganadores y suplentes. Ejecutar una sola vez, no reconsultar lista viva como evidencia. Resultado pertenece a participación del mismo sorteo. No define fórmula aleatoria ni adjudicación posterior sin política. HU-050 exige generador aleatorio criptográficamente seguro. Quedan pendientes método concreto y custodia, sin rebajar ese requisito.

Estado: Sustentada; evidencia estructurada propuesta. Fuente: HU-048–053; SQL 01–02.

## R13 Canjes y catálogo

Pendiente a Aprobada a Entregada, o Pendiente a Rechazada. Instantánea de costo y condiciones; saldo, reserva y stock coordinados sin doble descuento. Momento de reservar/devolver stock y costo cero pendientes P02/P07.

Estado: Sustentada con pendientes. Fuente: HU-054–059; SQL 01–02.

## R14 Contenido y comunidad

Institucional y comunitario tienen ciclo distinto. Aprobación institucional solo si aplica; responsable designado. Oculto no admite interacción. Reporte sobre publicación XOR comentario. Moderar con motivo/fecha/responsable; alcance y duración de suspensión pendientes. Material reutilizable, máximo diez MB y formatos de HU.

Estado: Sustentada, moderación estructurada propuesta. Fuente: HU-060–065/079–083; SQL 01–02.

## R15 Juegos y retos

Resultado calculado por servidor y límite configurado de intentos. Solo resultado válido reconoce puntos. Reto medible y vigente, una recompensa por socio-reto y actividades sin duplicación. Sin fórmula inventada.

Estado: Sustentada. Fuente: HU-071–078; SQL 01.

## R16 Bienestar

Convenios, recursos y beneficios informativos; convenio vencido impide ofrecer beneficio. Sin historiales clínicos, cuentas financieras reales, préstamos operativos ni integración productiva con core.

Estado: Sustentada. Fuente: Acta, alcance; HU-084–086; RNF-24.

## R17 Notificaciones

Eventos configurados y válidos, canales plataforma/correo, preferencias salvo obligatorias justificadas; catálogo obligatorio pendiente. Reintentos hasta tres según HU, convención de intento total por precisar. Historial autorizado y sin bloquear operación principal; SMTP real no verificado.

Estado: Planificado. Fuente: HU-052/066–070; RNF-18; SQL 01.

## R18 Reportes y conservación

Reportes como consultas derivadas con filtros, autorización, enmascaramiento y exportación PDF/Excel/CSV neutralizando fórmulas. Preservar auditoría, conversiones, movimientos e instantáneas aunque cambie estado del sujeto; composición no implica borrado físico de evidencia.

Estado: Planificado, auditoría parcial implementada. Fuente: HU-087–091; RNF-06/13/14; SQL 01–02.

## R19 Recuperación de acceso

Enlace de un solo uso, con huella en vez de token en claro y vencimiento. Al restablecer contraseña revoca sesiones previas. Vigencia actual de treinta minutos es implementación revisada, no política general de notificaciones.

Estado: Implementado. Fuente: HU-011; recuperacion_service.py; token_recuperacion.py; SQL 03; test_recuperacion.py y test_sprint1_sesiones.py.

## Diferencias respecto de la propuesta inicial

- Registro y autorización se separan de ControlAcceso. Los contadores se conservan en Usuario; los servicios carecen de estado artificial.
- ValidacionAdministrativaSocio pasa a servicio sin registro propio ficticio; su evidencia está en EventoAuditoria.
- Consentimientos explicitan aceptación; finalidad explícita continúa propuesta donde falta persistencia.
- Se agregan ElegibleCongelado y ReconocimientoIncentivo para explicar evidencia e irreversibilidad de reconocimientos.
- Se permite más de una Evaluacion por capacitación, conforme SQL; no se aprueba silenciosamente una única evaluación final.
- Emitir certificado es responsabilidad de InscripcionCapacitacion; la decisión de aprobación institucional pertenece a ContenidoInstitucional.
- Se corrigen HU-052/053/068/070 para distinguir envío/coordinación, consulta de historial y comprobación de integridad.
- Datos institucionales para segmentación se retiran de Socio hasta definir fuente; no se presume acceso al core.
- Se mantienen campos configurables como Texto cuando no hay catálogo de estados aprobado; no se inventan enumeraciones.

## Pendientes conservados

| P01 | SQL campaña permite fin = inicio; HU-025 pide fin posterior | Usar la regla HU en análisis; registrar brecha SQL, sin ejecutar migraciones aquí. |
| P02 | HU-054 acepta costo no negativo; SQL beneficio exige costo > 0 | Validar si existen beneficios gratuitos. No decidir silenciosamente entre ≥ 0 y > 0. |
| P03 | SQL taller permite cupo nulo; HU exige cupo > 0 | Confirmar si existe modalidad sin límite; propuesta inicial usa cupo positivo. |
| P04 | SQL sorteo exige campaña; HU-048 no la exige | Catálogo mantiene asociación obligatoria por diseño SQL; confirmar si se permitirán sorteos independientes. |
| P05 | Segmentación por edad, tipo, producto y agencia sin fuente completa implementada | Definir origen y combinaciones AND/OR. No inventar historial financiero ni integración productiva. |
| P06 | Fórmula de nivel, clasificación y horas de formación | Definir si nivel usa puntos acumulados o disponibles, descensos, período, empates, duración y agregación. El gasto de puntos no implica bajar de nivel sin decisión. |
| P07 | Reserva, stock y reverso | Aprobar semántica de saldos, cierre de reservas, vencimiento de solicitudes y tratamiento del stock antes de implementarlos. |
| P08 | Preguntas compartidas y tipos de juego | SQL usa propietario exclusivo evaluación XOR juego y máximo una opción correcta. El emparejamiento necesita pares y reglas propios; validar catálogo sin reutilizar preguntas contra la restricción SQL. |
| P09 | Consentimiento prospecto incompleto en SQL | SQL 02 guarda fechas, pero no toda la evidencia de versión/plazo. Se propone objeto dedicado; no se afirma una tabla ya existente. |
| P10 | Evidencia de sorteo, participación en campaña, perfil público, moderación y respuestas | Son necesidades derivadas de HU; varias carecen de estructura completa en los SQL revisados. Marcar clases y atributos propuestos. |
| P11 | Historial SQL carece de observación y varias propiedades de contenido/formación no están persistidas | Conservar requisitos y señalar brecha; no reducir el modelo de negocio a los campos existentes. |
| P12 | Casos genéricos Use Case A/B/1/2 y clases del contexto que representan actores | No trasladarlos al dominio ni borrarlos. No sirven como respaldo de un concepto sin revisar sus notas. |
| P13 | Padre del backlog y CU no equivalen a cobertura de aceptación | Conservar IDs originales y padre; comprobar criterios por separado. La matriz es una propuesta de trazabilidad, no certificación de implementación. |
| P14 | Roles de aprobación, moderación temporal y notificaciones obligatorias | Precisar responsable designado, alcance/duración de suspensión y catálogo de eventos obligatorios. |
| P15 | Código de referido histórico y unicidad de conversión | SQL permite varios códigos históricos y uno activo, pero HU solo exige un código único; confirmar ciclo de desactivación. Verificar unicidad comercial por prospecto, no solo por referido. |


| P16 | Límites por período y reversos | Precisar unidad de límite, ventana/calendario, zona horaria, si reversar restituye cupo y qué hacer si puntos ya se gastaron. |
| P17 | Versionado de materiales, evaluaciones e incentivos | Definir retiro sin alterar intentos, certificados ni reconocimientos previos. |
| P18 | Evidencia de sorteo | Definir contenido canónico, método aprobado, custodia y política de suplentes; no se impone tecnología criptográfica concreta. |