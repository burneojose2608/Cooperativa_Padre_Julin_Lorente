# Decisiones y reglas del modelo de análisis

## Fuentes y alcance de esta revisión

Se revisaron el inventario de paquetes, diagramas y casos de uso del `.eapx`; el texto de los tres DOCX; las 91 filas HU del backlog; README, matriz de trazabilidad y decisiones del sprint; modelos y responsabilidades de servicios de usuarios; scripts SQL 01 y 02 y referencias a sus ajustes posteriores; y la declaración de datos demostrativos del frontend. No se ejecutaron las suites ni se comprobó visualmente EA. El archivo Excel está inventariado en el repositorio, pero su contenido no se usó como evidencia en esta propuesta; el prompt solicita contrastarlo cuando aporte requisitos.

Fuentes concretas:

- `documentacion/Anexo 01 - Acta de Constitución Proyecto1 (1) (4).docx`: propósito, MVP académico y alcance.
- `documentacion/Anexo 02 - Documento Vision Proyecto1 (1) (7).docx`: actores y capacidades del dominio.
- `documentacion/PROYECTO 1 (4) (2).docx`: especificación general del reto.
- `documentacion/product_con_subtareas.csv`: IDs, criterios de aceptación y vínculos UR/RF/RNF.
- `documentacion/sprint-1-equipo/matriz-trazabilidad.md`: cobertura del primer sprint y cambios de línea base.
- `documentacion/sprint-1-valeria/decision-registro-general.md`, `decision-cedula-diez-digitos.md` y `conversion-administrativa-temporal.md`: reglas posteriores al backlog.
- `backend/apps/usuarios/models/`, `services/`, `permissions.py`: implementación de identidad y autorización.
- `backend/sql/01_base_datos_cooperativa.sql` y `02_ajustes_recomendados.sql`: diseño de persistencia de los módulos futuros, con brechas respecto al backlog.
- `frontend/src/datos/demo.js`: declara explícitamente que los módulos posteriores no tienen backend y usan ejemplos.

Las operaciones y asignaciones de responsabilidad del catálogo son propuestas de análisis. Incluso cuando existe comportamiento equivalente en un servicio, no se afirma que el método conceptual esté implementado sobre esa clase.

## Decisiones sustentadas

| ID | Decisión | Sustento e implicación |
| --- | --- | --- |
| D01 | Usuario se relaciona con 0..1 Socio | `models/socio.py`, README y registro general. Un usuario puede existir sin condición de socio. |
| D02 | Roles múltiples mediante asociación | HU-012, HU-013 y `models/rol.py`. Los actores administrativos no son subclases. La cuenta general puede tener cero roles. |
| D03 | Cédula como Texto de diez dígitos | Decisión posterior y SQL 06. Conserva ceros iniciales; no calcula verificador. |
| D04 | Padrón ausente crea cuenta general; activo habilita socio | Decisión posterior, registro_service.py. Inactivo rechaza; fallo de padrón no equivale a ausente. |
| D05 | Validación administrativa de cuenta es temporal | conversion_socio_service.py y documento temporal. No es la conversión comercial de un prospecto ni concede puntos por referido. |
| D06 | Código de socio y código de referido son conceptos diferentes | `socio.codigo_socio` frente a tabla `codigo_referido` y HU-016. No hay generación operativa del segundo demostrada. |
| D07 | Prospecto no requiere cuenta | Registro desde enlace público, HU-017 y consentimiento HU-023. Consentimiento del prospecto se modela separado del consentimiento de cuenta. |
| D08 | Referido y conversión comercial conservan evidencia | HU-018/HU-024 y CU-G15/G16. Una conversión por prospecto, aunque el SQL limita directamente por referido: debe comprobarse la regla de mayor alcance. |
| D09 | Movimientos y bitácora son inmutables | HU-036/HU-038, triggers SQL y modelo Auditoria. Correcciones mediante movimientos compensatorios. |
| D10 | Material educativo se reutiliza | HU-044/HU-062. Asociación a módulos; no composición con una única capacitación. |
| D11 | Bienestar es informativo y de beneficios | HU-084 y RNF-24. No se modelan historiales clínicos, diagnósticos ni atención médica. |
| D12 | Reportes son consultas derivadas | HU-087–091. Servicio de dominio sin estado artificial, con resultado y filtros como objetos de valor. |

## Reglas para documentar junto a las operaciones

1. **Acceso:** cada operación restringida requiere rol vigente y titularidad cuando corresponda; el menú no sustituye la autorización. Cinco fallos bloquean quince minutos; quince minutos de inactividad invalidan sesión. No se exponen contraseñas ni tokens en atributos de negocio públicos.
2. **Referido:** estados documentados Registrado, Confirmado, En seguimiento, Convertido, Rechazado y Expirado. Solo las transiciones autorizadas pueden ejecutarse. La fuente no define cada arista ni el efecto de retirar consentimiento después de confirmar: se debe precisar antes de cerrar la máquina de estados. No hay autorreferidos ni duplicados activos ni prospectos que ya sean socios del padrón.
3. **Consentimiento:** finalidad, versión y fecha son evidencia de aceptación. Sin confirmación del prospecto dentro del plazo configurable, expira el referido. El catálogo no atribuye al sistema actual un mecanismo completo de revocación o derechos de datos.
4. **Conversión:** apertura de cuenta o producto crediticio aprobado con datos de prueba, responsable y fecha; una sola conversión por prospecto y una acreditación de puntos por acción. La validación temporal de cuenta general no satisface automáticamente esta condición comercial.
5. **Campaña:** nueva en Borrador; admite Activa, Suspendida y Finalizada; participación solo activa, vigente y elegible. Los cambios no modifican incentivos reconocidos. Tasa de conversión = 100 × conversiones validadas / referidos; cero si no existen referidos. Avance frente a meta depende de la unidad de la meta, pendiente de precisar.
6. **Puntos:** para proponer una contabilidad coherente, definir A = acreditaciones, D = descuentos definitivos, V = reversos de acreditaciones y R = reservas todavía abiertas. Saldo contable = A − D − V; saldo disponible = saldo contable − R. Al aprobar un canje se cierra su reserva y se registra el descuento definitivo, sin un segundo débito disponible. Al rechazar se libera su reserva sin descuento. Esta convención es una propuesta por validar: el SQL registra cantidades positivas por tipo pero no implementa por sí solo toda esta semántica.
7. **Idempotencia:** la misma acción y tipo de operación no generan un segundo reconocimiento. Las claves deben considerar socio/destino cuando el tipo de origen no identifique globalmente al beneficiario. Las reservas, descuento y liberación de un canje se coordinan atómicamente con saldo y stock. No editar o borrar movimientos.
8. **Formación:** inscripción única socio–capacitación; evaluación calificada en servidor con umbral e intentos máximos; certificado solo después de aprobación, con código único no secuencial. Propuesta de avance = 100 × módulos completos / módulos requeridos; el caso cero módulos y las ponderaciones necesitan definición.
9. **Taller:** cupo mayor que cero según HU-046; inscripción sin sobrecupo y asistencia validada por personal habilitado; una sola acreditación por asistencia. No confundir inscripción con presencia efectiva.
10. **Sorteo:** congelar elegibles y conservar hash antes de seleccionar; selección segura, ganadores/suplentes y evidencia; ejecutable una sola vez. La verificación del hash compara contra el contenido congelado, no solo contra una lista actual mutable.
11. **Canje:** Pendiente → Aprobada → Entregada, o Pendiente → Rechazada. Puntos y condiciones se conservan como instantánea de la solicitud para evitar que cambios del catálogo alteren solicitudes anteriores. Historial con responsable y fecha. El momento de reservar stock y su devolución requiere decisión explícita.
12. **Contenido y comunidad:** publicación sujeta a permisos, vigencia y aprobación opcional. Contenido institucional y publicación comunitaria tienen reglas distintas. Contenido oculto no admite interacción. Imágenes y materiales cumplen límites y formatos; el dominio no necesita conocer rutas internas del servidor.
13. **Juegos y retos:** resultado calculado por servidor; límite de intentos; solo resultados válidos dan puntos. Retos con tipo de actividad, cantidad y vigencia; una recompensa por cumplimiento. No se fija una fórmula de puntuación sin reglas configuradas.
14. **Notificaciones y privacidad:** plataforma y correo según preferencias, sin desactivar las obligatorias; reintentos hasta tres y evidencia de fallo. Solo datos autorizados en comunidad, clasificación y reportes; neutralizar fórmulas al exportar CSV. El módulo asíncrono completo no se da por implementado por existir recuperación de contraseña por correo.

## Discrepancias y decisiones pendientes

| ID | Asunto | Acción para cerrar el modelo |
| --- | --- | --- |
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

## Convenciones UML propuestas

`Entidad` identifica conceptos con identidad y ciclo de vida; `ObjetoValor`, datos definidos por su contenido; `ServicioDominio`, reglas que coordinan varios conceptos; `Registro`, evidencia sin edición ordinaria. Estos estereotipos son una convención documental local, no un perfil UML instalado en EA.

Usar atributos privados y operaciones públicas como convención de representación. Los identificadores son conceptuales; no repetir FK. Las relaciones del catálogo son propuestas y cada fila declara multiplicidad en ambos extremos. No se usa herencia de roles ni composición de registros históricos. La composición de módulos y opciones de pregunta expresa pertenencia exclusiva, no una instrucción de borrado físico de historia.

Enumeraciones mínimas: EstadoCuenta {Activa, Suspendida, Desactivada}; EstadoPadron {Activo, Inactivo, NoEncontrado}; EstadoReferido {Registrado, Confirmado, EnSeguimiento, Convertido, Rechazado, Expirado}; EstadoCampana {Borrador, Activa, Suspendida, Finalizada}; TipoMovimiento {Acreditacion, Reserva, Descuento, Liberacion, Reverso}; EstadoCanje {Pendiente, Aprobada, Rechazada, Entregada}; Canal {Plataforma, Correo}; TipoJuego {Trivia, VerdaderoFalso, Emparejar}; TipoConversion {AperturaCuenta, ProductoCrediticio}. Los demás estados del catálogo son conjuntos propuestos que EA deberá definir con respaldo de los flujos.
