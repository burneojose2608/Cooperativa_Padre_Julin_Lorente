# Aceptación técnica local de Salud y bienestar

Verificación local con datos sintéticos en PostgreSQL aislado (`test_`), el cliente HTTP de Django y Vitest con jsdom.

| Historia y trazabilidad | Resultado por criterio | Código y evidencia ejecutable |
| --- | --- | --- |
| HU-084 · RF-13-1 · UR-55 · RNF-24, RNF-26 · CU-G13 | 1. Gestor de contenidos, Responsabilidad Social y Administración registran convenios con `entidad`, `tipo`, `descripcion`, `beneficio`, `condiciones` y `vigencia`. 2. Ninguna tabla, serializador ni formulario solicita o almacena datos clínicos o de salud de los socios; cualquier campo extra enviado a la API es rechazado con 400. 3. Los convenios se consultan y editan con auditoría. | `RECURSOS['convenios']`, `Convenio`, `CatalogoView`, `RecursoDetalleView`, `Modulos.jsx`. `test_bienestar_edicion_consulta_y_ausencia_de_campos_clinicos`. |
| HU-085 · RF-13-2 · UR-54 · RNF-24 · CU-G13 | 1. El socio consulta los convenios de bienestar vigentes y las publicaciones institucionales vigentes por categoría. 2. Cuando la fecha de `vigencia` vence, `CatalogoView` excluye automáticamente el convenio de la vista del socio. 3. La interfaz utiliza la rejilla adaptable común de paneles. | `CatalogoView.get` (`recurso == 'convenios'`), `PublicacionesView`, `Modulos.jsx`. `test_convenio_vencido_oculta_beneficio_y_rechaza_canje` y `test_bienestar_edicion_consulta_y_ausencia_de_campos_clinicos`. |
| HU-086 · RF-13-3 · UR-55 · CU-G13 | 1. Un convenio puede publicarse como beneficio canjeable con puntos asignando `convenio` al crear o editar el beneficio. 2. El beneficio expone `convenio` y `entidad_convenio` en el catálogo. 3. Si el convenio vence, el beneficio desaparece del catálogo de beneficios disponibles para el socio y `solicitar_canje` rechaza el canje con 400 («El convenio ya venció.»). | `Beneficio.convenio`, `CatalogoView.get`, `solicitar_canje`, `Modulos.jsx`. `test_convenio_vencido_oculta_beneficio_y_rechaza_canje`. |

## Pendientes externos

- Revisión visual mobile-first en navegadores reales (RNF-03).
