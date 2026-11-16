# Catálogo revisado de clases de análisis

Las firmas son responsabilidades conceptuales. Estado indica evidencia de comportamiento, no aprobación del diseño. Tipos Texto/Entero/Decimal/Booleano/Fecha/FechaHora, enumeraciones y conceptos. Coleccion y Conjunto indican multiplicidad de valores. Texto en entrada clave es transitorio y nunca atributo persistido. Los servicios no tienen atributos ficticios.

## Usuario

Dominio: Identidad. Estereotipo: Entidad. Estado: **Implementado parcialmente**.

Titular de la cuenta. Campos principales implementados; foto y gestión completa de estado/contacto son planificados. HU-001–008; models/usuario.py. Secreto es un parámetro transitorio, nunca un atributo público ni texto almacenado. Estado se refiere al comportamiento observado; toda organización en clases y sus firmas es análisis, no equivalencia literal con métodos Python.

```text
- id: Texto
- cedula: Texto
- nombres: Texto
- apellidos: Texto
- correo: Texto
- nombreUsuario: Texto
- telefono: Texto
- fechaNacimiento: Fecha
- estado: EstadoCuenta
- foto: Texto [0..1]
- intentosFallidos: Entero
- bloqueadoHasta: FechaHora [0..1]
+ calcularEdad(fecha: Fecha): Entero
+ actualizarContacto(correo: Texto, telefono: Texto, foto: Texto [0..1]): Booleano
+ cambiarContrasena(actual: Texto, nueva: Texto): Booleano
+ cambiarEstado(estado: EstadoCuenta, motivo: Texto, responsable: Usuario): Booleano
+ consultarPerfil(solicitante: Usuario): Texto
```

- Atributo `id: Texto` — Implementado; fuente: decision-cedula-diez-digitos.md; decision-registro-general.md; registro_service.py; SQL 05–06; HU-009/010/012/014/015; roles_service.py; sesiones_service.py; HU-011; recuperacion_service.py; token_recuperacion.py; SQL 03; test_recuperacion.py y test_sprint1_sesiones.py.
- Atributo `cedula: Texto` — Implementado; fuente: decision-cedula-diez-digitos.md; decision-registro-general.md; registro_service.py; SQL 05–06; HU-009/010/012/014/015; roles_service.py; sesiones_service.py; HU-011; recuperacion_service.py; token_recuperacion.py; SQL 03; test_recuperacion.py y test_sprint1_sesiones.py.
- Atributo `nombres: Texto` — Implementado; fuente: decision-cedula-diez-digitos.md; decision-registro-general.md; registro_service.py; SQL 05–06; HU-009/010/012/014/015; roles_service.py; sesiones_service.py; HU-011; recuperacion_service.py; token_recuperacion.py; SQL 03; test_recuperacion.py y test_sprint1_sesiones.py.
- Atributo `apellidos: Texto` — Implementado; fuente: decision-cedula-diez-digitos.md; decision-registro-general.md; registro_service.py; SQL 05–06; HU-009/010/012/014/015; roles_service.py; sesiones_service.py; HU-011; recuperacion_service.py; token_recuperacion.py; SQL 03; test_recuperacion.py y test_sprint1_sesiones.py.
- Atributo `correo: Texto` — Implementado; fuente: decision-cedula-diez-digitos.md; decision-registro-general.md; registro_service.py; SQL 05–06; HU-009/010/012/014/015; roles_service.py; sesiones_service.py; HU-011; recuperacion_service.py; token_recuperacion.py; SQL 03; test_recuperacion.py y test_sprint1_sesiones.py.
- Atributo `nombreUsuario: Texto` — Implementado; fuente: decision-cedula-diez-digitos.md; decision-registro-general.md; registro_service.py; SQL 05–06; HU-009/010/012/014/015; roles_service.py; sesiones_service.py; HU-011; recuperacion_service.py; token_recuperacion.py; SQL 03; test_recuperacion.py y test_sprint1_sesiones.py.
- Atributo `telefono: Texto` — Implementado; fuente: decision-cedula-diez-digitos.md; decision-registro-general.md; registro_service.py; SQL 05–06; HU-009/010/012/014/015; roles_service.py; sesiones_service.py; HU-011; recuperacion_service.py; token_recuperacion.py; SQL 03; test_recuperacion.py y test_sprint1_sesiones.py.
- Atributo `fechaNacimiento: Fecha` — Implementado; fuente: decision-cedula-diez-digitos.md; decision-registro-general.md; registro_service.py; SQL 05–06; HU-009/010/012/014/015; roles_service.py; sesiones_service.py; HU-011; recuperacion_service.py; token_recuperacion.py; SQL 03; test_recuperacion.py y test_sprint1_sesiones.py.
- Atributo `estado: EstadoCuenta` — Implementado; fuente: decision-cedula-diez-digitos.md; decision-registro-general.md; registro_service.py; SQL 05–06; HU-009/010/012/014/015; roles_service.py; sesiones_service.py; HU-011; recuperacion_service.py; token_recuperacion.py; SQL 03; test_recuperacion.py y test_sprint1_sesiones.py.
- Atributo `foto: Texto [0..1]` — Propuesta de análisis; fuente: decision-cedula-diez-digitos.md; decision-registro-general.md; registro_service.py; SQL 05–06; HU-009/010/012/014/015; roles_service.py; sesiones_service.py; HU-011; recuperacion_service.py; token_recuperacion.py; SQL 03; test_recuperacion.py y test_sprint1_sesiones.py.
- Atributo `intentosFallidos: Entero` — Implementado; fuente: decision-cedula-diez-digitos.md; decision-registro-general.md; registro_service.py; SQL 05–06; HU-009/010/012/014/015; roles_service.py; sesiones_service.py; HU-011; recuperacion_service.py; token_recuperacion.py; SQL 03; test_recuperacion.py y test_sprint1_sesiones.py.
- Atributo `bloqueadoHasta: FechaHora [0..1]` — Implementado; fuente: decision-cedula-diez-digitos.md; decision-registro-general.md; registro_service.py; SQL 05–06; HU-009/010/012/014/015; roles_service.py; sesiones_service.py; HU-011; recuperacion_service.py; token_recuperacion.py; SQL 03; test_recuperacion.py y test_sprint1_sesiones.py.
Reglas: R01, R02, R19. HU directas: HU-002, HU-003, HU-004, HU-007.
Fuentes: decision-cedula-diez-digitos.md; decision-registro-general.md; registro_service.py; SQL 05–06; HU-009/010/012/014/015; roles_service.py; sesiones_service.py; HU-011; recuperacion_service.py; token_recuperacion.py; SQL 03; test_recuperacion.py y test_sprint1_sesiones.py.

- `calcularEdad(fecha: Fecha): Entero` — Consulta; Responsabilidad conceptual; Planificado. Fuente: decision-cedula-diez-digitos.md; decision-registro-general.md; registro_service.py; SQL 05–06; HU-009/010/012/014/015; roles_service.py; sesiones_service.py; HU-011; recuperacion_service.py; token_recuperacion.py; SQL 03; test_recuperacion.py y test_sprint1_sesiones.py.
- `actualizarContacto(correo: Texto, telefono: Texto, foto: Texto [0..1]): Booleano` — Cambio de estado; Responsabilidad conceptual; Planificado. Fuente: decision-cedula-diez-digitos.md; decision-registro-general.md; registro_service.py; SQL 05–06; HU-009/010/012/014/015; roles_service.py; sesiones_service.py; HU-011; recuperacion_service.py; token_recuperacion.py; SQL 03; test_recuperacion.py y test_sprint1_sesiones.py.
- `cambiarContrasena(actual: Texto, nueva: Texto): Booleano` — Cambio de estado; Responsabilidad conceptual; Planificado. Fuente: decision-cedula-diez-digitos.md; decision-registro-general.md; registro_service.py; SQL 05–06; HU-009/010/012/014/015; roles_service.py; sesiones_service.py; HU-011; recuperacion_service.py; token_recuperacion.py; SQL 03; test_recuperacion.py y test_sprint1_sesiones.py.
- `cambiarEstado(estado: EstadoCuenta, motivo: Texto, responsable: Usuario): Booleano` — Cambio de estado; Responsabilidad conceptual; Planificado. Fuente: decision-cedula-diez-digitos.md; decision-registro-general.md; registro_service.py; SQL 05–06; HU-009/010/012/014/015; roles_service.py; sesiones_service.py; HU-011; recuperacion_service.py; token_recuperacion.py; SQL 03; test_recuperacion.py y test_sprint1_sesiones.py.
- `consultarPerfil(solicitante: Usuario): Texto` — Consulta; Responsabilidad conceptual; Comportamiento equivalente implementado en servicios. Fuente: decision-cedula-diez-digitos.md; decision-registro-general.md; registro_service.py; SQL 05–06; HU-009/010/012/014/015; roles_service.py; sesiones_service.py; HU-011; recuperacion_service.py; token_recuperacion.py; SQL 03; test_recuperacion.py y test_sprint1_sesiones.py.
## Socio

Dominio: Identidad. Estereotipo: Entidad. Estado: **Implementado parcialmente**.

Condición cooperativa asociada a una cuenta. Código y validación implementados; datos de segmentación propuestos y pendientes de fuente P05. models/socio.py; HU-028. Los datos de segmentación no se afirman disponibles; P05 exige definir una fuente autorizada. Estado se refiere al comportamiento observado; toda organización en clases y sus firmas es análisis, no equivalencia literal con métodos Python.

```text
- codigoSocio: Texto
- validadoEn: FechaHora
+ esElegibleParaParticipar(fecha: FechaHora): Booleano
```

- Atributo `codigoSocio: Texto` — Implementado; fuente: decision-cedula-diez-digitos.md; decision-registro-general.md; registro_service.py; SQL 05–06; conversion-administrativa-temporal.md; conversion_socio_service.py.
- Atributo `validadoEn: FechaHora` — Implementado; fuente: decision-cedula-diez-digitos.md; decision-registro-general.md; registro_service.py; SQL 05–06; conversion-administrativa-temporal.md; conversion_socio_service.py.
Reglas: R01, R03. HU directas: concepto de apoyo.
Fuentes: decision-cedula-diez-digitos.md; decision-registro-general.md; registro_service.py; SQL 05–06; conversion-administrativa-temporal.md; conversion_socio_service.py.

- `esElegibleParaParticipar(fecha: FechaHora): Booleano` — Consulta; Responsabilidad conceptual; Planificado. Fuente: decision-cedula-diez-digitos.md; decision-registro-general.md; registro_service.py; SQL 05–06; conversion-administrativa-temporal.md; conversion_socio_service.py.
## Rol

Dominio: Identidad. Estereotipo: Entidad. Estado: **Implementado parcialmente**.

Conjunto de autorizaciones. Roles múltiples implementados; administración completa de permisos planificada. HU-012–014. Estado se refiere al comportamiento observado; toda organización en clases y sus firmas es análisis, no equivalencia literal con métodos Python.

```text
- nombre: Texto
+ habilita(permiso: Permiso): Booleano
```

- Atributo `nombre: Texto` — Implementado; fuente: HU-009/010/012/014/015; roles_service.py; sesiones_service.py.
Reglas: R02. HU directas: concepto de apoyo.
Fuentes: HU-009/010/012/014/015; roles_service.py; sesiones_service.py.

- `habilita(permiso: Permiso): Booleano` — Consulta; Responsabilidad conceptual; Planificado. Fuente: HU-009/010/012/014/015; roles_service.py; sesiones_service.py.
## Permiso

Dominio: Identidad. Estereotipo: Entidad. Estado: **Planificado**.

Capacidad autorizada; diseño SQL permiso/rol_permiso y HU-013. No presupone administración operativa completa. Estado se refiere al comportamiento observado; toda organización en clases y sus firmas es análisis, no equivalencia literal con métodos Python.

```text
- codigo: Texto
- descripcion: Texto
```
Sin operaciones propias: evidencia o dato cuya invariante aplica su dueño.
- Atributo `codigo: Texto` — Planificado; fuente: HU-009/010/012/014/015; roles_service.py; sesiones_service.py.
- Atributo `descripcion: Texto` — Planificado; fuente: HU-009/010/012/014/015; roles_service.py; sesiones_service.py.
Reglas: R02. HU directas: concepto de apoyo.
Fuentes: HU-009/010/012/014/015; roles_service.py; sesiones_service.py.

## ConsentimientoCuenta

Dominio: Identidad. Estereotipo: Registro. Estado: **Implementado parcialmente**.

Evidencia inmutable de aceptación expresa. Solo se conserva si aceptado=true, con fecha y versión; finalidad explícita es propuesta de análisis pendiente de texto aprobado. Fecha/versión implementadas; HU-001, consentimiento.py; RNF-02. Estado se refiere al comportamiento observado; toda organización en clases y sus firmas es análisis, no equivalencia literal con métodos Python.

```text
- finalidad: Texto
- aceptado: Booleano
- aceptadoEn: FechaHora
- versionPolitica: Texto
```
Sin operaciones propias: evidencia o dato cuya invariante aplica su dueño.
- Atributo `finalidad: Texto` — Propuesta de análisis; fuente: HU-001/023; RNF-02/25; SQL 02; consentimiento.py.
- Atributo `aceptado: Booleano` — Propuesta de análisis; fuente: HU-001/023; RNF-02/25; SQL 02; consentimiento.py.
- Atributo `aceptadoEn: FechaHora` — Implementado; fuente: HU-001/023; RNF-02/25; SQL 02; consentimiento.py.
- Atributo `versionPolitica: Texto` — Implementado; fuente: HU-001/023; RNF-02/25; SQL 02; consentimiento.py.
Reglas: R04. HU directas: concepto de apoyo.
Fuentes: HU-001/023; RNF-02/25; SQL 02; consentimiento.py.

## EntradaPadron

Dominio: Identidad. Estereotipo: Entidad. Estado: **Implementado**.

Registro de prueba independiente de cuentas. No encontrado es resultado de consulta, no una fila ficticia. HU-006; models/padron.py. Estado se refiere al comportamiento observado; toda organización en clases y sus firmas es análisis, no equivalencia literal con métodos Python.

```text
- cedula: Texto
- activo: Booleano
+ habilitaCondicionSocio(): Booleano
```

- Atributo `cedula: Texto` — Implementado; fuente: decision-cedula-diez-digitos.md; decision-registro-general.md; registro_service.py; SQL 05–06.
- Atributo `activo: Booleano` — Implementado; fuente: decision-cedula-diez-digitos.md; decision-registro-general.md; registro_service.py; SQL 05–06.
Reglas: R01. HU directas: HU-006.
Fuentes: decision-cedula-diez-digitos.md; decision-registro-general.md; registro_service.py; SQL 05–06.

- `habilitaCondicionSocio(): Booleano` — Consulta; Responsabilidad conceptual; Comportamiento equivalente implementado en servicios. Fuente: decision-cedula-diez-digitos.md; decision-registro-general.md; registro_service.py; SQL 05–06.
## ValidacionAdministrativaSocio

Dominio: Identidad. Estereotipo: ServicioDominio. Estado: **Implementado**.

Servicio manual temporal implementado por conversion_socio_service.py. Confirmación true estricta, administrador activo, cuenta general activa sin roles, padrón no inactivo; transacción e idempotencia. Evidencia en EventoAuditoria. No crea conversión comercial ni puntos. Fuente: conversion-administrativa-temporal.md; ampliación sin HU original exacta. Estado se refiere al comportamiento observado; toda organización en clases y sus firmas es análisis, no equivalencia literal con métodos Python.

```text
+ validarYHabilitar(cuenta: Usuario, administrador: Usuario, confirmacion: Booleano): Socio
```

Reglas: R03. HU directas: concepto de apoyo.
Fuentes: conversion-administrativa-temporal.md; conversion_socio_service.py.

- `validarYHabilitar(cuenta: Usuario, administrador: Usuario, confirmacion: Booleano): Socio` — Coordinación; Responsabilidad conceptual; Comportamiento equivalente implementado en servicios. Fuente: conversion-administrativa-temporal.md; conversion_socio_service.py.
## Sesion

Dominio: Seguridad. Estereotipo: Entidad. Estado: **Implementado**.

Sesión revocable implementada; iniciadaEn es atributo conceptual propuesto. No almacena JWT en claro. HU-009/HU-015; models/sesion.py. Estado se refiere al comportamiento observado; toda organización en clases y sus firmas es análisis, no equivalencia literal con métodos Python.

```text
- iniciadaEn: FechaHora
- venceEn: FechaHora
- ultimoUso: FechaHora [0..1]
- revocadaEn: FechaHora [0..1]
+ estaVigente(ahora: FechaHora): Booleano
+ registrarActividad(ahora: FechaHora): Booleano
+ cerrar(ahora: FechaHora): Booleano
+ expirarPorInactividad(ahora: FechaHora): Booleano
```

- Atributo `iniciadaEn: FechaHora` — Propuesta de análisis; fuente: HU-009/010/012/014/015; roles_service.py; sesiones_service.py; HU-011; recuperacion_service.py; token_recuperacion.py; SQL 03; test_recuperacion.py y test_sprint1_sesiones.py.
- Atributo `venceEn: FechaHora` — Implementado; fuente: HU-009/010/012/014/015; roles_service.py; sesiones_service.py; HU-011; recuperacion_service.py; token_recuperacion.py; SQL 03; test_recuperacion.py y test_sprint1_sesiones.py.
- Atributo `ultimoUso: FechaHora [0..1]` — Implementado; fuente: HU-009/010/012/014/015; roles_service.py; sesiones_service.py; HU-011; recuperacion_service.py; token_recuperacion.py; SQL 03; test_recuperacion.py y test_sprint1_sesiones.py.
- Atributo `revocadaEn: FechaHora [0..1]` — Implementado; fuente: HU-009/010/012/014/015; roles_service.py; sesiones_service.py; HU-011; recuperacion_service.py; token_recuperacion.py; SQL 03; test_recuperacion.py y test_sprint1_sesiones.py.
Reglas: R02, R19. HU directas: HU-015.
Fuentes: HU-009/010/012/014/015; roles_service.py; sesiones_service.py; HU-011; recuperacion_service.py; token_recuperacion.py; SQL 03; test_recuperacion.py y test_sprint1_sesiones.py.

- `estaVigente(ahora: FechaHora): Booleano` — Consulta; Responsabilidad conceptual; Comportamiento equivalente implementado en servicios. Fuente: HU-009/010/012/014/015; roles_service.py; sesiones_service.py; HU-011; recuperacion_service.py; token_recuperacion.py; SQL 03; test_recuperacion.py y test_sprint1_sesiones.py.
- `registrarActividad(ahora: FechaHora): Booleano` — Cambio de estado; Responsabilidad conceptual; Comportamiento equivalente implementado en servicios. Fuente: HU-009/010/012/014/015; roles_service.py; sesiones_service.py; HU-011; recuperacion_service.py; token_recuperacion.py; SQL 03; test_recuperacion.py y test_sprint1_sesiones.py.
- `cerrar(ahora: FechaHora): Booleano` — Cambio de estado; Responsabilidad conceptual; Comportamiento equivalente implementado en servicios. Fuente: HU-009/010/012/014/015; roles_service.py; sesiones_service.py; HU-011; recuperacion_service.py; token_recuperacion.py; SQL 03; test_recuperacion.py y test_sprint1_sesiones.py.
- `expirarPorInactividad(ahora: FechaHora): Booleano` — Cambio de estado; Responsabilidad conceptual; Comportamiento equivalente implementado en servicios. Fuente: HU-009/010/012/014/015; roles_service.py; sesiones_service.py; HU-011; recuperacion_service.py; token_recuperacion.py; SQL 03; test_recuperacion.py y test_sprint1_sesiones.py.
## RecuperacionAcceso

Dominio: Seguridad. Estereotipo: Entidad. Estado: **Implementado**.

Enlace de un uso, modelo TokenRecuperacion y servicio existentes. HU-011. Vigencia actual 30 minutos en servicio; no extender a todos los consentimientos. Estado se refiere al comportamiento observado; toda organización en clases y sus firmas es análisis, no equivalencia literal con métodos Python.

```text
- solicitadaEn: FechaHora
- venceEn: FechaHora
- usadaEn: FechaHora [0..1]
- huellaEnlace: Texto
+ esUtilizable(ahora: FechaHora): Booleano
+ restablecerContrasena(nueva: Texto): Booleano
```

- Atributo `solicitadaEn: FechaHora` — Implementado; fuente: HU-011; recuperacion_service.py; token_recuperacion.py; SQL 03; test_recuperacion.py y test_sprint1_sesiones.py.
- Atributo `venceEn: FechaHora` — Implementado; fuente: HU-011; recuperacion_service.py; token_recuperacion.py; SQL 03; test_recuperacion.py y test_sprint1_sesiones.py.
- Atributo `usadaEn: FechaHora [0..1]` — Implementado; fuente: HU-011; recuperacion_service.py; token_recuperacion.py; SQL 03; test_recuperacion.py y test_sprint1_sesiones.py.
- Atributo `huellaEnlace: Texto` — Implementado; fuente: HU-011; recuperacion_service.py; token_recuperacion.py; SQL 03; test_recuperacion.py y test_sprint1_sesiones.py.
Reglas: R19. HU directas: HU-011.
Fuentes: HU-011; recuperacion_service.py; token_recuperacion.py; SQL 03; test_recuperacion.py y test_sprint1_sesiones.py.

- `esUtilizable(ahora: FechaHora): Booleano` — Consulta; Responsabilidad conceptual; Comportamiento equivalente implementado en servicios. Fuente: HU-011; recuperacion_service.py; token_recuperacion.py; SQL 03; test_recuperacion.py y test_sprint1_sesiones.py.
- `restablecerContrasena(nueva: Texto): Booleano` — Cambio de estado; Responsabilidad conceptual; Comportamiento equivalente implementado en servicios. Fuente: HU-011; recuperacion_service.py; token_recuperacion.py; SQL 03; test_recuperacion.py y test_sprint1_sesiones.py.
## ControlAcceso

Dominio: Seguridad. Estereotipo: ServicioDominio. Estado: **Implementado**.

Servicio de autenticación, sin estado propio. Lee cuenta activa y bloqueo; cinco fallos bloquean quince minutos. Los contadores pertenecen a Usuario. HU-009/010; autenticacion_service.py. Estado se refiere al comportamiento observado; toda organización en clases y sus firmas es análisis, no equivalencia literal con métodos Python.

```text
+ validarCredenciales(identificador: Texto, clave: Texto): Sesion
+ registrarIntentoFallido(ahora: FechaHora): Booleano
```

Reglas: R02. HU directas: HU-009, HU-010.
Fuentes: HU-009/010/012/014/015; roles_service.py; sesiones_service.py.

- `validarCredenciales(identificador: Texto, clave: Texto): Sesion` — Coordinación; Responsabilidad conceptual; Comportamiento equivalente implementado en servicios. Fuente: HU-009/010/012/014/015; roles_service.py; sesiones_service.py.
- `registrarIntentoFallido(ahora: FechaHora): Booleano` — Coordinación; Responsabilidad conceptual; Comportamiento equivalente implementado en servicios. Fuente: HU-009/010/012/014/015; roles_service.py; sesiones_service.py.
## EventoAuditoria

Dominio: Auditoria. Estereotipo: Registro. Estado: **Implementado**.

Registro inmutable; actor opcional para acciones anónimas. Implementado para eventos concretos, no interfaz general completa. models/auditoria.py; RNF-06. Estado se refiere al comportamiento observado; toda organización en clases y sus firmas es análisis, no equivalencia literal con métodos Python.

```text
- accion: Texto
- entidad: Texto
- referencia: Texto [0..1]
- fecha: FechaHora
- resultado: Texto
- origenConexion: Texto [0..1]
```
Sin operaciones propias: evidencia o dato cuya invariante aplica su dueño.
- Atributo `accion: Texto` — Implementado; fuente: conversion-administrativa-temporal.md; conversion_socio_service.py; HU-087–091; RNF-06/13/14; SQL 01–02.
- Atributo `entidad: Texto` — Implementado; fuente: conversion-administrativa-temporal.md; conversion_socio_service.py; HU-087–091; RNF-06/13/14; SQL 01–02.
- Atributo `referencia: Texto [0..1]` — Implementado; fuente: conversion-administrativa-temporal.md; conversion_socio_service.py; HU-087–091; RNF-06/13/14; SQL 01–02.
- Atributo `fecha: FechaHora` — Implementado; fuente: conversion-administrativa-temporal.md; conversion_socio_service.py; HU-087–091; RNF-06/13/14; SQL 01–02.
- Atributo `resultado: Texto` — Implementado; fuente: conversion-administrativa-temporal.md; conversion_socio_service.py; HU-087–091; RNF-06/13/14; SQL 01–02.
- Atributo `origenConexion: Texto [0..1]` — Implementado; fuente: conversion-administrativa-temporal.md; conversion_socio_service.py; HU-087–091; RNF-06/13/14; SQL 01–02.
Reglas: R03, R18. HU directas: concepto de apoyo.
Fuentes: conversion-administrativa-temporal.md; conversion_socio_service.py; HU-087–091; RNF-06/13/14; SQL 01–02.

## CambioEstado

Dominio: Auditoria. Estereotipo: Registro. Estado: **Planificado**.

Historial inmutable compartido por referido, campaña y canje. Diseño SQL historial_estado; motivo/observación propuestos por HU-024/HU-056. Estado se refiere al comportamiento observado; toda organización en clases y sus firmas es análisis, no equivalencia literal con métodos Python.

```text
- entidad: Texto
- referencia: Texto
- anterior: Texto [0..1]
- nuevo: Texto
- fecha: FechaHora
- motivo: Texto [0..1]
```
Sin operaciones propias: evidencia o dato cuya invariante aplica su dueño.
- Atributo `entidad: Texto` — Planificado; fuente: HU-016/017/018/020/024; SQL 01; CU-G04/G15/G16; HU-087–091; RNF-06/13/14; SQL 01–02.
- Atributo `referencia: Texto` — Planificado; fuente: HU-016/017/018/020/024; SQL 01; CU-G04/G15/G16; HU-087–091; RNF-06/13/14; SQL 01–02.
- Atributo `anterior: Texto [0..1]` — Planificado; fuente: HU-016/017/018/020/024; SQL 01; CU-G04/G15/G16; HU-087–091; RNF-06/13/14; SQL 01–02.
- Atributo `nuevo: Texto` — Planificado; fuente: HU-016/017/018/020/024; SQL 01; CU-G04/G15/G16; HU-087–091; RNF-06/13/14; SQL 01–02.
- Atributo `fecha: FechaHora` — Planificado; fuente: HU-016/017/018/020/024; SQL 01; CU-G04/G15/G16; HU-087–091; RNF-06/13/14; SQL 01–02.
- Atributo `motivo: Texto [0..1]` — Planificado; fuente: HU-016/017/018/020/024; SQL 01; CU-G04/G15/G16; HU-087–091; RNF-06/13/14; SQL 01–02.
Reglas: R05, R18. HU directas: concepto de apoyo.
Fuentes: HU-016/017/018/020/024; SQL 01; CU-G04/G15/G16; HU-087–091; RNF-06/13/14; SQL 01–02.

## CodigoReferido

Dominio: Referidos. Estereotipo: Entidad. Estado: **Planificado**.

Identificador comercial no secuencial distinto de codigoSocio. SQL permite historial y un código activo por socio. HU-016/HU-019; módulo planificado. Estado se refiere al comportamiento observado; toda organización en clases y sus firmas es análisis, no equivalencia literal con métodos Python.

```text
- valor: Texto
- activo: Booleano
+ esValido(): Booleano
+ generarEnlace(base: Texto): Texto
+ generarPara(socio: Socio): CodigoReferido
```

- Atributo `valor: Texto` — Planificado; fuente: HU-016/017/018/020/024; SQL 01; CU-G04/G15/G16.
- Atributo `activo: Booleano` — Planificado; fuente: HU-016/017/018/020/024; SQL 01; CU-G04/G15/G16.
Reglas: R05. HU directas: HU-016, HU-019.
Fuentes: HU-016/017/018/020/024; SQL 01; CU-G04/G15/G16.

- `esValido(): Booleano` — Consulta; Responsabilidad conceptual; Planificado. Fuente: HU-016/017/018/020/024; SQL 01; CU-G04/G15/G16.
- `generarEnlace(base: Texto): Texto` — Cambio de estado; Responsabilidad conceptual; Planificado. Fuente: HU-016/017/018/020/024; SQL 01; CU-G04/G15/G16.
- `generarPara(socio: Socio): CodigoReferido` — Cambio de estado; Responsabilidad conceptual; Planificado. Fuente: HU-016/017/018/020/024; SQL 01; CU-G04/G15/G16.
## Prospecto

Dominio: Referidos. Estereotipo: Entidad. Estado: **Planificado**.

Persona recomendada sin cuenta obligatoria. HU-017/HU-020. Al menos un contacto; datos mínimos de comparación pendientes de precisar. Estado se refiere al comportamiento observado; toda organización en clases y sus firmas es análisis, no equivalencia literal con métodos Python.

```text
- id: Texto
- nombres: Texto
- huellaIdentificacion: Texto [0..1]
- telefono: Texto [0..1]
- correo: Texto [0..1]
- productoInteres: Texto [0..1]
+ coincideCon(persona: Texto): Booleano
+ tieneContactoUtilizable(): Booleano
```

- Atributo `id: Texto` — Planificado; fuente: HU-001/023; RNF-02/25; SQL 02; consentimiento.py; HU-016/017/018/020/024; SQL 01; CU-G04/G15/G16.
- Atributo `nombres: Texto` — Planificado; fuente: HU-001/023; RNF-02/25; SQL 02; consentimiento.py; HU-016/017/018/020/024; SQL 01; CU-G04/G15/G16.
- Atributo `huellaIdentificacion: Texto [0..1]` — Planificado; fuente: HU-001/023; RNF-02/25; SQL 02; consentimiento.py; HU-016/017/018/020/024; SQL 01; CU-G04/G15/G16.
- Atributo `telefono: Texto [0..1]` — Planificado; fuente: HU-001/023; RNF-02/25; SQL 02; consentimiento.py; HU-016/017/018/020/024; SQL 01; CU-G04/G15/G16.
- Atributo `correo: Texto [0..1]` — Planificado; fuente: HU-001/023; RNF-02/25; SQL 02; consentimiento.py; HU-016/017/018/020/024; SQL 01; CU-G04/G15/G16.
- Atributo `productoInteres: Texto [0..1]` — Planificado; fuente: HU-001/023; RNF-02/25; SQL 02; consentimiento.py; HU-016/017/018/020/024; SQL 01; CU-G04/G15/G16.
Reglas: R04, R05. HU directas: concepto de apoyo.
Fuentes: HU-001/023; RNF-02/25; SQL 02; consentimiento.py; HU-016/017/018/020/024; SQL 01; CU-G04/G15/G16.

- `coincideCon(persona: Texto): Booleano` — Consulta; Responsabilidad conceptual; Planificado. Fuente: HU-001/023; RNF-02/25; SQL 02; consentimiento.py; HU-016/017/018/020/024; SQL 01; CU-G04/G15/G16.
- `tieneContactoUtilizable(): Booleano` — Consulta; Responsabilidad conceptual; Planificado. Fuente: HU-001/023; RNF-02/25; SQL 02; consentimiento.py; HU-016/017/018/020/024; SQL 01; CU-G04/G15/G16.
## ConsentimientoProspecto

Dominio: Referidos. Estereotipo: Entidad. Estado: **Propuesta de análisis**.

Objeto propuesto de evidencia de consentimiento para un referido; SQL 02 solo cubre parte de las fechas. HU-023; no reutiliza ConsentimientoCuenta. Aceptado=false mientras no confirma; aceptadoEn presente si y solo si aceptado=true. El plazo es configurable, sin duración inventada. Estado se refiere al comportamiento observado; toda organización en clases y sus firmas es análisis, no equivalencia literal con métodos Python.

```text
- finalidad: Texto
- versionPolitica: Texto
- solicitadoEn: FechaHora
- limiteConfirmacion: FechaHora
- aceptadoEn: FechaHora [0..1]
- aceptado: Booleano
+ confirmar(ahora: FechaHora): Booleano
+ estaConfirmado(): Booleano
+ plazoVencido(ahora: FechaHora): Booleano
```

- Atributo `finalidad: Texto` — Propuesta de análisis; fuente: HU-001/023; RNF-02/25; SQL 02; consentimiento.py.
- Atributo `versionPolitica: Texto` — Propuesta de análisis; fuente: HU-001/023; RNF-02/25; SQL 02; consentimiento.py.
- Atributo `solicitadoEn: FechaHora` — Propuesta de análisis; fuente: HU-001/023; RNF-02/25; SQL 02; consentimiento.py.
- Atributo `limiteConfirmacion: FechaHora` — Propuesta de análisis; fuente: HU-001/023; RNF-02/25; SQL 02; consentimiento.py.
- Atributo `aceptadoEn: FechaHora [0..1]` — Propuesta de análisis; fuente: HU-001/023; RNF-02/25; SQL 02; consentimiento.py.
- Atributo `aceptado: Booleano` — Propuesta de análisis; fuente: HU-001/023; RNF-02/25; SQL 02; consentimiento.py.
Reglas: R04. HU directas: HU-023.
Fuentes: HU-001/023; RNF-02/25; SQL 02; consentimiento.py.

- `confirmar(ahora: FechaHora): Booleano` — Cambio de estado; Responsabilidad conceptual; Propuesta de análisis. Fuente: HU-001/023; RNF-02/25; SQL 02; consentimiento.py.
- `estaConfirmado(): Booleano` — Consulta; Responsabilidad conceptual; Propuesta de análisis. Fuente: HU-001/023; RNF-02/25; SQL 02; consentimiento.py.
- `plazoVencido(ahora: FechaHora): Booleano` — Cambio de estado; Responsabilidad conceptual; Propuesta de análisis. Fuente: HU-001/023; RNF-02/25; SQL 02; consentimiento.py.
## Referido

Dominio: Referidos. Estereotipo: Entidad. Estado: **Planificado**.

Vínculo de recomendación. Valida código, autorreferido, padrón, duplicados y transición; conserva historial. HU-017–024; módulo planificado. Estado se refiere al comportamiento observado; toda organización en clases y sus firmas es análisis, no equivalencia literal con métodos Python.

```text
- id: Texto
- creadoEn: FechaHora
- estado: EstadoReferido
+ validarRegistro(): Booleano
+ confirmarConsentimiento(ahora: FechaHora): Booleano
+ iniciarSeguimiento(responsable: Usuario): Booleano
+ rechazar(motivo: Texto, responsable: Usuario): Booleano
+ expirar(ahora: FechaHora): Booleano
+ confirmarConversion(tipo: TipoConversion, evidencia: Texto, responsable: Usuario): Conversion
+ consultarSeguimiento(solicitante: Usuario): Texto
```

- Atributo `id: Texto` — Planificado; fuente: HU-001/023; RNF-02/25; SQL 02; consentimiento.py; HU-016/017/018/020/024; SQL 01; CU-G04/G15/G16.
- Atributo `creadoEn: FechaHora` — Planificado; fuente: HU-001/023; RNF-02/25; SQL 02; consentimiento.py; HU-016/017/018/020/024; SQL 01; CU-G04/G15/G16.
- Atributo `estado: EstadoReferido` — Planificado; fuente: HU-001/023; RNF-02/25; SQL 02; consentimiento.py; HU-016/017/018/020/024; SQL 01; CU-G04/G15/G16.
Reglas: R04, R05. HU directas: HU-017, HU-018, HU-020, HU-021, HU-024.
Fuentes: HU-001/023; RNF-02/25; SQL 02; consentimiento.py; HU-016/017/018/020/024; SQL 01; CU-G04/G15/G16.

- `validarRegistro(): Booleano` — Cambio de estado; Responsabilidad conceptual; Planificado. Fuente: HU-001/023; RNF-02/25; SQL 02; consentimiento.py; HU-016/017/018/020/024; SQL 01; CU-G04/G15/G16.
- `confirmarConsentimiento(ahora: FechaHora): Booleano` — Cambio de estado; Responsabilidad conceptual; Planificado. Fuente: HU-001/023; RNF-02/25; SQL 02; consentimiento.py; HU-016/017/018/020/024; SQL 01; CU-G04/G15/G16.
- `iniciarSeguimiento(responsable: Usuario): Booleano` — Cambio de estado; Responsabilidad conceptual; Planificado. Fuente: HU-001/023; RNF-02/25; SQL 02; consentimiento.py; HU-016/017/018/020/024; SQL 01; CU-G04/G15/G16.
- `rechazar(motivo: Texto, responsable: Usuario): Booleano` — Cambio de estado; Responsabilidad conceptual; Planificado. Fuente: HU-001/023; RNF-02/25; SQL 02; consentimiento.py; HU-016/017/018/020/024; SQL 01; CU-G04/G15/G16.
- `expirar(ahora: FechaHora): Booleano` — Cambio de estado; Responsabilidad conceptual; Planificado. Fuente: HU-001/023; RNF-02/25; SQL 02; consentimiento.py; HU-016/017/018/020/024; SQL 01; CU-G04/G15/G16.
- `confirmarConversion(tipo: TipoConversion, evidencia: Texto, responsable: Usuario): Conversion` — Cambio de estado; Responsabilidad conceptual; Planificado. Fuente: HU-001/023; RNF-02/25; SQL 02; consentimiento.py; HU-016/017/018/020/024; SQL 01; CU-G04/G15/G16.
- `consultarSeguimiento(solicitante: Usuario): Texto` — Consulta; Responsabilidad conceptual; Planificado. Fuente: HU-001/023; RNF-02/25; SQL 02; consentimiento.py; HU-016/017/018/020/024; SQL 01; CU-G04/G15/G16.
## Conversion

Dominio: Referidos. Estereotipo: Registro. Estado: **Planificado**.

Hecho comercial validado una vez por prospecto; dispara reconocimiento único. SQL conversion y HU-018; evidencia detallada propuesta. Estado se refiere al comportamiento observado; toda organización en clases y sus firmas es análisis, no equivalencia literal con métodos Python.

```text
- tipo: TipoConversion
- validadaEn: FechaHora
- evidenciaPrueba: Texto
- claveOrigen: Texto
```
Sin operaciones propias: evidencia o dato cuya invariante aplica su dueño.
- Atributo `tipo: TipoConversion` — Planificado; fuente: HU-016/017/018/020/024; SQL 01; CU-G04/G15/G16; HU-087–091; RNF-06/13/14; SQL 01–02.
- Atributo `validadaEn: FechaHora` — Planificado; fuente: HU-016/017/018/020/024; SQL 01; CU-G04/G15/G16; HU-087–091; RNF-06/13/14; SQL 01–02.
- Atributo `evidenciaPrueba: Texto` — Planificado; fuente: HU-016/017/018/020/024; SQL 01; CU-G04/G15/G16; HU-087–091; RNF-06/13/14; SQL 01–02.
- Atributo `claveOrigen: Texto` — Planificado; fuente: HU-016/017/018/020/024; SQL 01; CU-G04/G15/G16; HU-087–091; RNF-06/13/14; SQL 01–02.
Reglas: R05, R18. HU directas: concepto de apoyo.
Fuentes: HU-016/017/018/020/024; SQL 01; CU-G04/G15/G16; HU-087–091; RNF-06/13/14; SQL 01–02.

## Campana

Dominio: Campanas. Estereotipo: Entidad. Estado: **Planificado**.

Organiza objetivos, vigencia e incentivos. HU-025–030; planificado. unidadMeta propuesta pendiente de definición. Estado se refiere al comportamiento observado; toda organización en clases y sus firmas es análisis, no equivalencia literal con métodos Python.

```text
- nombre: Texto
- tipo: Texto
- objetivo: Texto
- meta: Entero
- unidadMeta: Texto
- inicio: Fecha
- fin: Fecha
- estado: EstadoCampana
+ activar(fecha: Fecha): Booleano
+ suspender(motivo: Texto): Booleano
+ finalizar(fecha: Fecha): Booleano
+ admiteParticipacion(socio: Socio, fecha: Fecha): Booleano
+ modificarCondiciones(cambios: Texto, responsable: Usuario): Booleano
+ calcularTasaConversion(): Decimal
+ calcularAvanceMeta(): Decimal
```

- Atributo `nombre: Texto` — Planificado; fuente: HU-025–030; Presentacion RF-04; SQL 01–02.
- Atributo `tipo: Texto` — Planificado; fuente: HU-025–030; Presentacion RF-04; SQL 01–02.
- Atributo `objetivo: Texto` — Planificado; fuente: HU-025–030; Presentacion RF-04; SQL 01–02.
- Atributo `meta: Entero` — Planificado; fuente: HU-025–030; Presentacion RF-04; SQL 01–02.
- Atributo `unidadMeta: Texto` — Planificado; fuente: HU-025–030; Presentacion RF-04; SQL 01–02.
- Atributo `inicio: Fecha` — Planificado; fuente: HU-025–030; Presentacion RF-04; SQL 01–02.
- Atributo `fin: Fecha` — Planificado; fuente: HU-025–030; Presentacion RF-04; SQL 01–02.
- Atributo `estado: EstadoCampana` — Planificado; fuente: HU-025–030; Presentacion RF-04; SQL 01–02.
Reglas: R06. HU directas: HU-025, HU-026, HU-027, HU-029, HU-030.
Fuentes: HU-025–030; Presentacion RF-04; SQL 01–02.

- `activar(fecha: Fecha): Booleano` — Cambio de estado; Responsabilidad conceptual; Planificado. Fuente: HU-025–030; Presentacion RF-04; SQL 01–02.
- `suspender(motivo: Texto): Booleano` — Cambio de estado; Responsabilidad conceptual; Planificado. Fuente: HU-025–030; Presentacion RF-04; SQL 01–02.
- `finalizar(fecha: Fecha): Booleano` — Cambio de estado; Responsabilidad conceptual; Planificado. Fuente: HU-025–030; Presentacion RF-04; SQL 01–02.
- `admiteParticipacion(socio: Socio, fecha: Fecha): Booleano` — Consulta; Responsabilidad conceptual; Planificado. Fuente: HU-025–030; Presentacion RF-04; SQL 01–02.
- `modificarCondiciones(cambios: Texto, responsable: Usuario): Booleano` — Cambio de estado; Responsabilidad conceptual; Planificado. Fuente: HU-025–030; Presentacion RF-04; SQL 01–02.
- `calcularTasaConversion(): Decimal` — Consulta; Responsabilidad conceptual; Planificado. Fuente: HU-025–030; Presentacion RF-04; SQL 01–02.
- `calcularAvanceMeta(): Decimal` — Consulta; Responsabilidad conceptual; Planificado. Fuente: HU-025–030; Presentacion RF-04; SQL 01–02.
## Segmento

Dominio: Campanas. Estereotipo: Entidad. Estado: **Planificado**.

Selecciona por edad, tipo de socio, producto y agencia; combinación de criterios pendiente P05. HU-028. Estado se refiere al comportamiento observado; toda organización en clases y sus firmas es análisis, no equivalencia literal con métodos Python.

```text
- nombre: Texto
- criteriosAutorizados: Conjunto<Texto>
+ incluye(socio: Socio, fecha: Fecha): Booleano
+ contarElegibles(socios: Coleccion<Socio>): Entero
```

- Atributo `nombre: Texto` — Planificado; fuente: HU-025–030; Presentacion RF-04; SQL 01–02.
- Atributo `criteriosAutorizados: Conjunto<Texto>` — Planificado; fuente: HU-025–030; Presentacion RF-04; SQL 01–02.
Reglas: R06. HU directas: HU-028.
Fuentes: HU-025–030; Presentacion RF-04; SQL 01–02.

- `incluye(socio: Socio, fecha: Fecha): Booleano` — Cambio de estado; Responsabilidad conceptual; Planificado. Fuente: HU-025–030; Presentacion RF-04; SQL 01–02.
- `contarElegibles(socios: Coleccion<Socio>): Entero` — Consulta; Responsabilidad conceptual; Planificado. Fuente: HU-025–030; Presentacion RF-04; SQL 01–02.
## IncentivoCampana

Dominio: Campanas. Estereotipo: Entidad. Estado: **Propuesta de análisis**.

Descomposición conceptual propuesta de incentivos de campaña (SQL los guarda como texto). Puntos o participaciones, sin efecto retroactivo. HU-025/HU-029. Estado se refiere al comportamiento observado; toda organización en clases y sus firmas es análisis, no equivalencia literal con métodos Python.

```text
- tipo: Texto
- cantidad: Entero
- condiciones: Texto
- version: Texto
- vigenteDesde: Fecha
- vigenteHasta: Fecha [0..1]
+ correspondeA(actividad: ActividadValidada): Booleano
```

- Atributo `tipo: Texto` — Propuesta de análisis; fuente: HU-025–030; Presentacion RF-04; SQL 01–02.
- Atributo `cantidad: Entero` — Propuesta de análisis; fuente: HU-025–030; Presentacion RF-04; SQL 01–02.
- Atributo `condiciones: Texto` — Propuesta de análisis; fuente: HU-025–030; Presentacion RF-04; SQL 01–02.
- Atributo `version: Texto` — Propuesta de análisis; fuente: HU-025–030; Presentacion RF-04; SQL 01–02.
- Atributo `vigenteDesde: Fecha` — Propuesta de análisis; fuente: HU-025–030; Presentacion RF-04; SQL 01–02.
- Atributo `vigenteHasta: Fecha [0..1]` — Propuesta de análisis; fuente: HU-025–030; Presentacion RF-04; SQL 01–02.
Reglas: R06. HU directas: concepto de apoyo.
Fuentes: HU-025–030; Presentacion RF-04; SQL 01–02.

- `correspondeA(actividad: ActividadValidada): Booleano` — Cambio de estado; Responsabilidad conceptual; Propuesta de análisis. Fuente: HU-025–030; Presentacion RF-04; SQL 01–02.
## ParticipacionCampana

Dominio: Campanas. Estereotipo: Entidad. Estado: **Propuesta de análisis**.

Registro propuesto de participación validada para monitoreo y CU-G06. No se exige inscripción manual universal ni se afirma tabla existente. Estado se refiere al comportamiento observado; toda organización en clases y sus firmas es análisis, no equivalencia literal con métodos Python.

```text
- registradaEn: FechaHora
- validadaEn: FechaHora [0..1]
- versionCondiciones: Texto
+ validarElegibilidad(fecha: Fecha): Booleano
```

- Atributo `registradaEn: FechaHora` — Propuesta de análisis; fuente: HU-025–030; Presentacion RF-04; SQL 01–02.
- Atributo `validadaEn: FechaHora [0..1]` — Propuesta de análisis; fuente: HU-025–030; Presentacion RF-04; SQL 01–02.
- Atributo `versionCondiciones: Texto` — Propuesta de análisis; fuente: HU-025–030; Presentacion RF-04; SQL 01–02.
Reglas: R06. HU directas: concepto de apoyo.
Fuentes: HU-025–030; Presentacion RF-04; SQL 01–02.

- `validarElegibilidad(fecha: Fecha): Booleano` — Cambio de estado; Responsabilidad conceptual; Propuesta de análisis. Fuente: HU-025–030; Presentacion RF-04; SQL 01–02.
## ActividadValidada

Dominio: Gamificacion. Estereotipo: ObjetoValor. Estado: **Propuesta de análisis**.

Hecho reconocido tras validación de conversión, capacitación, asistencia, juego o reto. Objeto de valor inmutable, no tabla ni endpoint genérico. La referencia y el beneficiario identifican el origen; no se convierte la validación administrativa en actividad. HU-032/049/075/078. Estado se refiere al comportamiento observado; toda organización en clases y sus firmas es análisis, no equivalencia literal con métodos Python.

```text
- tipo: TipoActividad
- referenciaOrigen: Texto
- fecha: FechaHora
```
Sin operaciones propias: evidencia o dato cuya invariante aplica su dueño.
- Atributo `tipo: TipoActividad` — Propuesta de análisis; fuente: HU-031/032/036/038/059; SQL 01.
- Atributo `referenciaOrigen: Texto` — Propuesta de análisis; fuente: HU-031/032/036/038/059; SQL 01.
- Atributo `fecha: FechaHora` — Propuesta de análisis; fuente: HU-031/032/036/038/059; SQL 01.
Reglas: R07. HU directas: concepto de apoyo.
Fuentes: HU-031/032/036/038/059; SQL 01.

## ReglaPuntos

Dominio: Gamificacion. Estereotipo: Entidad. Estado: **Planificado**.

Regla sin efecto retroactivo. HU-031/HU-032; límites y versión no completos en SQL. Estado se refiere al comportamiento observado; toda organización en clases y sus firmas es análisis, no equivalencia literal con métodos Python.

```text
- tipoActividad: TipoActividad
- puntos: Entero
- limitePeriodo: Entero [0..1]
- periodo: Texto [0..1]
- vigenteDesde: Fecha
- vigenteHasta: Fecha [0..1]
- version: Texto
+ calcularPuntos(actividad: ActividadValidada, acumuladoPeriodo: Entero): Entero
+ estaVigente(fecha: Fecha): Booleano
+ configurarVersion(condiciones: Texto, administrador: Usuario): ReglaPuntos
```

- Atributo `tipoActividad: TipoActividad` — Planificado; fuente: HU-031/032/036/038/059; SQL 01.
- Atributo `puntos: Entero` — Planificado; fuente: HU-031/032/036/038/059; SQL 01.
- Atributo `limitePeriodo: Entero [0..1]` — Planificado; fuente: HU-031/032/036/038/059; SQL 01.
- Atributo `periodo: Texto [0..1]` — Planificado; fuente: HU-031/032/036/038/059; SQL 01.
- Atributo `vigenteDesde: Fecha` — Planificado; fuente: HU-031/032/036/038/059; SQL 01.
- Atributo `vigenteHasta: Fecha [0..1]` — Planificado; fuente: HU-031/032/036/038/059; SQL 01.
- Atributo `version: Texto` — Planificado; fuente: HU-031/032/036/038/059; SQL 01.
Reglas: R07. HU directas: HU-031.
Fuentes: HU-031/032/036/038/059; SQL 01.

- `calcularPuntos(actividad: ActividadValidada, acumuladoPeriodo: Entero): Entero` — Consulta; Responsabilidad conceptual; Planificado. Fuente: HU-031/032/036/038/059; SQL 01.
- `estaVigente(fecha: Fecha): Booleano` — Consulta; Responsabilidad conceptual; Planificado. Fuente: HU-031/032/036/038/059; SQL 01.
- `configurarVersion(condiciones: Texto, administrador: Usuario): ReglaPuntos` — Cambio de estado; Responsabilidad conceptual; Planificado. Fuente: HU-031/032/036/038/059; SQL 01.
## CuentaPuntos

Dominio: Gamificacion. Estereotipo: Entidad. Estado: **Propuesta de análisis**.

Agregado conceptual propuesto, derivado del libro; no tabla de saldo. HU-032/HU-034/HU-036/HU-038/HU-059. Semántica de reserva según propuesta R6. Estado se refiere al comportamiento observado; toda organización en clases y sus firmas es análisis, no equivalencia literal con métodos Python.

```text
- /saldoContable: Entero
- /saldoReservado: Entero
- /saldoDisponible: Entero
+ calcularSaldoContable(): Entero
+ calcularSaldoReservado(): Entero
+ calcularSaldoDisponible(): Entero
+ acreditar(actividad: ActividadValidada, regla: ReglaPuntos): MovimientoPuntos
+ reservar(canje: Canje, cantidad: Entero): MovimientoPuntos
+ confirmarDescuento(canje: Canje): MovimientoPuntos
+ liberarReserva(canje: Canje): MovimientoPuntos
+ revertir(original: MovimientoPuntos, motivo: Texto, responsable: Usuario): MovimientoPuntos
```

- Atributo `/saldoContable: Entero` — Propuesta de análisis; fuente: HU-031/032/036/038/059; SQL 01; HU-055/059; CU reservar sin doble débito; SQL 01; decisión P07; HU-054–059; SQL 01–02.
- Atributo `/saldoReservado: Entero` — Propuesta de análisis; fuente: HU-031/032/036/038/059; SQL 01; HU-055/059; CU reservar sin doble débito; SQL 01; decisión P07; HU-054–059; SQL 01–02.
- Atributo `/saldoDisponible: Entero` — Propuesta de análisis; fuente: HU-031/032/036/038/059; SQL 01; HU-055/059; CU reservar sin doble débito; SQL 01; decisión P07; HU-054–059; SQL 01–02.
Reglas: R07, R08, R13. HU directas: HU-032, HU-034, HU-036, HU-038, HU-059.
Fuentes: HU-031/032/036/038/059; SQL 01; HU-055/059; CU reservar sin doble débito; SQL 01; decisión P07; HU-054–059; SQL 01–02.

- `calcularSaldoContable(): Entero` — Consulta; Responsabilidad conceptual; Propuesta de análisis. Fuente: HU-031/032/036/038/059; SQL 01; HU-055/059; CU reservar sin doble débito; SQL 01; decisión P07; HU-054–059; SQL 01–02.
- `calcularSaldoReservado(): Entero` — Consulta; Responsabilidad conceptual; Propuesta de análisis. Fuente: HU-031/032/036/038/059; SQL 01; HU-055/059; CU reservar sin doble débito; SQL 01; decisión P07; HU-054–059; SQL 01–02.
- `calcularSaldoDisponible(): Entero` — Consulta; Responsabilidad conceptual; Propuesta de análisis. Fuente: HU-031/032/036/038/059; SQL 01; HU-055/059; CU reservar sin doble débito; SQL 01; decisión P07; HU-054–059; SQL 01–02.
- `acreditar(actividad: ActividadValidada, regla: ReglaPuntos): MovimientoPuntos` — Cambio de estado; Responsabilidad conceptual; Propuesta de análisis. Fuente: HU-031/032/036/038/059; SQL 01; HU-055/059; CU reservar sin doble débito; SQL 01; decisión P07; HU-054–059; SQL 01–02.
- `reservar(canje: Canje, cantidad: Entero): MovimientoPuntos` — Cambio de estado; Responsabilidad conceptual; Propuesta de análisis. Fuente: HU-031/032/036/038/059; SQL 01; HU-055/059; CU reservar sin doble débito; SQL 01; decisión P07; HU-054–059; SQL 01–02.
- `confirmarDescuento(canje: Canje): MovimientoPuntos` — Cambio de estado; Responsabilidad conceptual; Propuesta de análisis. Fuente: HU-031/032/036/038/059; SQL 01; HU-055/059; CU reservar sin doble débito; SQL 01; decisión P07; HU-054–059; SQL 01–02.
- `liberarReserva(canje: Canje): MovimientoPuntos` — Cambio de estado; Responsabilidad conceptual; Propuesta de análisis. Fuente: HU-031/032/036/038/059; SQL 01; HU-055/059; CU reservar sin doble débito; SQL 01; decisión P07; HU-054–059; SQL 01–02.
- `revertir(original: MovimientoPuntos, motivo: Texto, responsable: Usuario): MovimientoPuntos` — Cambio de estado; Responsabilidad conceptual; Propuesta de análisis. Fuente: HU-031/032/036/038/059; SQL 01; HU-055/059; CU reservar sin doble débito; SQL 01; decisión P07; HU-054–059; SQL 01–02.
## MovimientoPuntos

Dominio: Gamificacion. Estereotipo: Registro. Estado: **Planificado**.

Registro inmutable con cantidad positiva y signo semántico según tipo. Origen, beneficiario y reverso trazables; HU-036/HU-038/HU-059. Estado se refiere al comportamiento observado; toda organización en clases y sus firmas es análisis, no equivalencia literal con métodos Python.

```text
- id: Texto
- tipo: TipoMovimiento
- cantidad: Entero
- fecha: FechaHora
- claveIdempotencia: Texto
- motivo: Texto [0..1]
```
Sin operaciones propias: evidencia o dato cuya invariante aplica su dueño.
- Atributo `id: Texto` — Planificado; fuente: HU-031/032/036/038/059; SQL 01; HU-055/059; CU reservar sin doble débito; SQL 01; decisión P07; HU-087–091; RNF-06/13/14; SQL 01–02.
- Atributo `tipo: TipoMovimiento` — Planificado; fuente: HU-031/032/036/038/059; SQL 01; HU-055/059; CU reservar sin doble débito; SQL 01; decisión P07; HU-087–091; RNF-06/13/14; SQL 01–02.
- Atributo `cantidad: Entero` — Planificado; fuente: HU-031/032/036/038/059; SQL 01; HU-055/059; CU reservar sin doble débito; SQL 01; decisión P07; HU-087–091; RNF-06/13/14; SQL 01–02.
- Atributo `fecha: FechaHora` — Planificado; fuente: HU-031/032/036/038/059; SQL 01; HU-055/059; CU reservar sin doble débito; SQL 01; decisión P07; HU-087–091; RNF-06/13/14; SQL 01–02.
- Atributo `claveIdempotencia: Texto` — Planificado; fuente: HU-031/032/036/038/059; SQL 01; HU-055/059; CU reservar sin doble débito; SQL 01; decisión P07; HU-087–091; RNF-06/13/14; SQL 01–02.
- Atributo `motivo: Texto [0..1]` — Planificado; fuente: HU-031/032/036/038/059; SQL 01; HU-055/059; CU reservar sin doble débito; SQL 01; decisión P07; HU-087–091; RNF-06/13/14; SQL 01–02.
Reglas: R07, R08, R18. HU directas: concepto de apoyo.
Fuentes: HU-031/032/036/038/059; SQL 01; HU-055/059; CU reservar sin doble débito; SQL 01; decisión P07; HU-087–091; RNF-06/13/14; SQL 01–02.

## Nivel

Dominio: Gamificacion. Estereotipo: Entidad. Estado: **Planificado**.

Umbrales únicos. Base de puntos y descensos pendientes P06. HU-033/HU-037. Estado se refiere al comportamiento observado; toda organización en clases y sus firmas es análisis, no equivalencia literal con métodos Python.

```text
- nombre: Texto
- umbralPuntos: Entero
+ seAlcanzaCon(puntosBase: Entero): Booleano
+ definirUmbral(puntos: Entero, administrador: Usuario): Booleano
```

- Atributo `nombre: Texto` — Planificado; fuente: HU-033/035/037/083.
- Atributo `umbralPuntos: Entero` — Planificado; fuente: HU-033/035/037/083.
Reglas: R09. HU directas: HU-033, HU-037.
Fuentes: HU-033/035/037/083.

- `seAlcanzaCon(puntosBase: Entero): Booleano` — Consulta; Responsabilidad conceptual; Planificado. Fuente: HU-033/035/037/083.
- `definirUmbral(puntos: Entero, administrador: Usuario): Booleano` — Cambio de estado; Responsabilidad conceptual; Planificado. Fuente: HU-033/035/037/083.
## Insignia

Dominio: Gamificacion. Estereotipo: Entidad. Estado: **Planificado**.

Define logro; icono requerido por HU-037 aunque no completo en SQL. HU-033/HU-037. Estado se refiere al comportamiento observado; toda organización en clases y sus firmas es análisis, no equivalencia literal con métodos Python.

```text
- nombre: Texto
- icono: Texto
- criterio: Texto
+ seCumplePara(socio: Socio, actividades: Coleccion<ActividadValidada>): Booleano
+ definirCriterio(criterio: Texto, administrador: Usuario): Booleano
```

- Atributo `nombre: Texto` — Planificado; fuente: HU-033/035/037/083.
- Atributo `icono: Texto` — Planificado; fuente: HU-033/035/037/083.
- Atributo `criterio: Texto` — Planificado; fuente: HU-033/035/037/083.
Reglas: R09. HU directas: concepto de apoyo.
Fuentes: HU-033/035/037/083.

- `seCumplePara(socio: Socio, actividades: Coleccion<ActividadValidada>): Booleano` — Consulta; Responsabilidad conceptual; Planificado. Fuente: HU-033/035/037/083.
- `definirCriterio(criterio: Texto, administrador: Usuario): Booleano` — Cambio de estado; Responsabilidad conceptual; Planificado. Fuente: HU-033/035/037/083.
## InsigniaObtenida

Dominio: Gamificacion. Estereotipo: Registro. Estado: **Planificado**.

Registro único socio–insignia; no borrar al cambiar criterios. HU-033; SQL socio_insignia. Estado se refiere al comportamiento observado; toda organización en clases y sus firmas es análisis, no equivalencia literal con métodos Python.

```text
- obtenidaEn: FechaHora
```
Sin operaciones propias: evidencia o dato cuya invariante aplica su dueño.
- Atributo `obtenidaEn: FechaHora` — Planificado; fuente: HU-033/035/037/083.
Reglas: R09. HU directas: concepto de apoyo.
Fuentes: HU-033/035/037/083.

## Clasificacion

Dominio: Gamificacion. Estereotipo: Entidad. Estado: **Propuesta de análisis**.

Consulta derivada con alias y exclusión pública. No necesita tabla propia. Criterio y empates pendientes P06. HU-035. Estado se refiere al comportamiento observado; toda organización en clases y sus firmas es análisis, no equivalencia literal con métodos Python.

```text
- desde: Fecha
- hasta: Fecha
- criterioOrden: Texto
+ calcularPosicion(socio: Socio): Entero
+ generarVistaPublica(): Coleccion<Texto>
```

- Atributo `desde: Fecha` — Propuesta de análisis; fuente: HU-033/035/037/083.
- Atributo `hasta: Fecha` — Propuesta de análisis; fuente: HU-033/035/037/083.
- Atributo `criterioOrden: Texto` — Propuesta de análisis; fuente: HU-033/035/037/083.
Reglas: R09. HU directas: HU-035.
Fuentes: HU-033/035/037/083.

- `calcularPosicion(socio: Socio): Entero` — Consulta; Responsabilidad conceptual; Propuesta de análisis. Fuente: HU-033/035/037/083.
- `generarVistaPublica(): Coleccion<Texto>` — Consulta; Responsabilidad conceptual; Propuesta de análisis. Fuente: HU-033/035/037/083.
## Capacitacion

Dominio: Formacion. Estereotipo: Entidad. Estado: **Planificado**.

Oferta de educación financiera. Varias propiedades derivadas de HU aún sin persistencia completa. HU-039/HU-044. Estado se refiere al comportamiento observado; toda organización en clases y sus firmas es análisis, no equivalencia literal con métodos Python.

```text
- titulo: Texto
- descripcion: Texto
- duracionHoras: Decimal
- requisitos: Texto
- estado: Texto
+ puedeInscribirse(socio: Socio): Booleano
+ publicar(responsable: Usuario): Booleano
+ calcularTasaAprobacion(): Decimal
```

- Atributo `titulo: Texto` — Planificado; fuente: HU-039–047; SQL 01–02.
- Atributo `descripcion: Texto` — Planificado; fuente: HU-039–047; SQL 01–02.
- Atributo `duracionHoras: Decimal` — Planificado; fuente: HU-039–047; SQL 01–02.
- Atributo `requisitos: Texto` — Planificado; fuente: HU-039–047; SQL 01–02.
- Atributo `estado: Texto` — Planificado; fuente: HU-039–047; SQL 01–02.
Reglas: R10. HU directas: HU-039, HU-044.
Fuentes: HU-039–047; SQL 01–02.

- `puedeInscribirse(socio: Socio): Booleano` — Consulta; Responsabilidad conceptual; Planificado. Fuente: HU-039–047; SQL 01–02.
- `publicar(responsable: Usuario): Booleano` — Cambio de estado; Responsabilidad conceptual; Planificado. Fuente: HU-039–047; SQL 01–02.
- `calcularTasaAprobacion(): Decimal` — Consulta; Responsabilidad conceptual; Planificado. Fuente: HU-039–047; SQL 01–02.
## ModuloCapacitacion

Dominio: Formacion. Estereotipo: Entidad. Estado: **Planificado**.

Corresponde a unidad del SQL; obligatoriedad propuesta para explicar avance. HU-040/HU-044. Estado se refiere al comportamiento observado; toda organización en clases y sus firmas es análisis, no equivalencia literal con métodos Python.

```text
- titulo: Texto
- orden: Entero
- obligatorio: Booleano
+ estaCompletado(progreso: ProgresoModulo): Booleano
```

- Atributo `titulo: Texto` — Planificado; fuente: HU-039–047; SQL 01–02.
- Atributo `orden: Entero` — Planificado; fuente: HU-039–047; SQL 01–02.
- Atributo `obligatorio: Booleano` — Planificado; fuente: HU-039–047; SQL 01–02.
Reglas: R10. HU directas: concepto de apoyo.
Fuentes: HU-039–047; SQL 01–02.

- `estaCompletado(progreso: ProgresoModulo): Booleano` — Consulta; Responsabilidad conceptual; Planificado. Fuente: HU-039–047; SQL 01–02.
## InscripcionCapacitacion

Dominio: Formacion. Estereotipo: Entidad. Estado: **Planificado**.

Vínculo único socio–capacitación. Fórmula y acceso a evaluación por definir P06. HU-039–041. Estado se refiere al comportamiento observado; toda organización en clases y sus firmas es análisis, no equivalencia literal con métodos Python.

```text
- fecha: FechaHora
- estado: Texto
- /porcentajeAvance: Decimal
+ completarModulo(modulo: ModuloCapacitacion): ProgresoModulo
+ calcularAvance(): Decimal
+ puedeRendir(evaluacion: Evaluacion): Booleano
+ emitirCertificado(ahora: FechaHora): Certificado
```

- Atributo `fecha: FechaHora` — Planificado; fuente: HU-039–047; SQL 01–02.
- Atributo `estado: Texto` — Planificado; fuente: HU-039–047; SQL 01–02.
- Atributo `/porcentajeAvance: Decimal` — Planificado; fuente: HU-039–047; SQL 01–02.
Reglas: R10. HU directas: HU-040, HU-042.
Fuentes: HU-039–047; SQL 01–02.

- `completarModulo(modulo: ModuloCapacitacion): ProgresoModulo` — Cambio de estado; Responsabilidad conceptual; Planificado. Fuente: HU-039–047; SQL 01–02.
- `calcularAvance(): Decimal` — Consulta; Responsabilidad conceptual; Planificado. Fuente: HU-039–047; SQL 01–02.
- `puedeRendir(evaluacion: Evaluacion): Booleano` — Consulta; Responsabilidad conceptual; Planificado. Fuente: HU-039–047; SQL 01–02.
- `emitirCertificado(ahora: FechaHora): Certificado` — Cambio de estado; Responsabilidad conceptual; Planificado. Fuente: HU-039–047; SQL 01–02.
## ProgresoModulo

Dominio: Formacion. Estereotipo: Entidad. Estado: **Planificado**.

Seguimiento por inscripción y módulo; entre 0 y 100. HU-040; SQL progreso. Estado se refiere al comportamiento observado; toda organización en clases y sus firmas es análisis, no equivalencia literal con métodos Python.

```text
- porcentaje: Decimal
- completadoEn: FechaHora [0..1]
+ registrarFinalizacion(ahora: FechaHora): Booleano
```

- Atributo `porcentaje: Decimal` — Planificado; fuente: HU-039–047; SQL 01–02.
- Atributo `completadoEn: FechaHora [0..1]` — Planificado; fuente: HU-039–047; SQL 01–02.
Reglas: R10. HU directas: concepto de apoyo.
Fuentes: HU-039–047; SQL 01–02.

- `registrarFinalizacion(ahora: FechaHora): Booleano` — Cambio de estado; Responsabilidad conceptual; Planificado. Fuente: HU-039–047; SQL 01–02.
## Evaluacion

Dominio: Formacion. Estereotipo: Entidad. Estado: **Planificado**.

Calificación en servidor y límite. HU-041/HU-044; reglas y máximo no completos en SQL. Estado se refiere al comportamiento observado; toda organización en clases y sus firmas es análisis, no equivalencia literal con métodos Python.

```text
- notaMinima: Decimal
- maximoIntentos: Entero
- reglasCalificacion: Texto
+ permiteNuevoIntento(inscripcion: InscripcionCapacitacion): Booleano
+ calcularNota(respuestas: Coleccion<RespuestaActividad>): Decimal
```

- Atributo `notaMinima: Decimal` — Planificado; fuente: HU-039–047; SQL 01–02; HU-041/072/074; SQL 02, ck_pregunta_dueno.
- Atributo `maximoIntentos: Entero` — Planificado; fuente: HU-039–047; SQL 01–02; HU-041/072/074; SQL 02, ck_pregunta_dueno.
- Atributo `reglasCalificacion: Texto` — Planificado; fuente: HU-039–047; SQL 01–02; HU-041/072/074; SQL 02, ck_pregunta_dueno.
Reglas: R10, R11. HU directas: concepto de apoyo.
Fuentes: HU-039–047; SQL 01–02; HU-041/072/074; SQL 02, ck_pregunta_dueno.

- `permiteNuevoIntento(inscripcion: InscripcionCapacitacion): Booleano` — Consulta; Responsabilidad conceptual; Planificado. Fuente: HU-039–047; SQL 01–02; HU-041/072/074; SQL 02, ck_pregunta_dueno.
- `calcularNota(respuestas: Coleccion<RespuestaActividad>): Decimal` — Consulta; Responsabilidad conceptual; Planificado. Fuente: HU-039–047; SQL 01–02; HU-041/072/074; SQL 02, ck_pregunta_dueno.
## IntentoEvaluacion

Dominio: Formacion. Estereotipo: Entidad. Estado: **Planificado**.

Intento asociado a inscripción y evaluación; aprobación válida genera actividad única. HU-041. Estado se refiere al comportamiento observado; toda organización en clases y sus firmas es análisis, no equivalencia literal con métodos Python.

```text
- numero: Entero
- iniciadoEn: FechaHora
- finalizadoEn: FechaHora [0..1]
- nota: Decimal [0..1]
- aprobado: Booleano [0..1]
+ calificar(): Decimal
+ alcanzaAprobacion(): Booleano
```

- Atributo `numero: Entero` — Planificado; fuente: HU-039–047; SQL 01–02; HU-041/072/074; SQL 02, ck_pregunta_dueno.
- Atributo `iniciadoEn: FechaHora` — Planificado; fuente: HU-039–047; SQL 01–02; HU-041/072/074; SQL 02, ck_pregunta_dueno.
- Atributo `finalizadoEn: FechaHora [0..1]` — Planificado; fuente: HU-039–047; SQL 01–02; HU-041/072/074; SQL 02, ck_pregunta_dueno.
- Atributo `nota: Decimal [0..1]` — Planificado; fuente: HU-039–047; SQL 01–02; HU-041/072/074; SQL 02, ck_pregunta_dueno.
- Atributo `aprobado: Booleano [0..1]` — Planificado; fuente: HU-039–047; SQL 01–02; HU-041/072/074; SQL 02, ck_pregunta_dueno.
Reglas: R10, R11. HU directas: HU-041.
Fuentes: HU-039–047; SQL 01–02; HU-041/072/074; SQL 02, ck_pregunta_dueno.

- `calificar(): Decimal` — Cambio de estado; Responsabilidad conceptual; Planificado. Fuente: HU-039–047; SQL 01–02; HU-041/072/074; SQL 02, ck_pregunta_dueno.
- `alcanzaAprobacion(): Booleano` — Cambio de estado; Responsabilidad conceptual; Planificado. Fuente: HU-039–047; SQL 01–02; HU-041/072/074; SQL 02, ck_pregunta_dueno.
## Certificado

Dominio: Formacion. Estereotipo: Registro. Estado: **Planificado**.

Solo tras aprobar, código único no secuencial y acceso al documento autorizado. HU-042/HU-043/HU-045. Estado se refiere al comportamiento observado; toda organización en clases y sus firmas es análisis, no equivalencia literal con métodos Python.

```text
- codigoVerificacion: Texto
- emitidoEn: FechaHora
- documento: Texto
+ verificarAutenticidad(codigo: Texto): Booleano
+ obtenerDocumento(solicitante: Usuario): Texto
```

- Atributo `codigoVerificacion: Texto` — Planificado; fuente: HU-039–047; SQL 01–02.
- Atributo `emitidoEn: FechaHora` — Planificado; fuente: HU-039–047; SQL 01–02.
- Atributo `documento: Texto` — Planificado; fuente: HU-039–047; SQL 01–02.
Reglas: R10. HU directas: HU-043, HU-045.
Fuentes: HU-039–047; SQL 01–02.

- `verificarAutenticidad(codigo: Texto): Booleano` — Consulta; Responsabilidad conceptual; Planificado. Fuente: HU-039–047; SQL 01–02.
- `obtenerDocumento(solicitante: Usuario): Texto` — Consulta; Responsabilidad conceptual; Planificado. Fuente: HU-039–047; SQL 01–02.
## Taller

Dominio: Formacion. Estereotipo: Entidad. Estado: **Planificado**.

Actividad con aforo; sin integración de videoconferencia inventada. HU-046/HU-047. Estado se refiere al comportamiento observado; toda organización en clases y sus firmas es análisis, no equivalencia literal con métodos Python.

```text
- titulo: Texto
- modalidad: Texto
- lugarOEnlace: Texto
- fecha: FechaHora
- cupo: Entero
- estado: EstadoTaller
+ calcularCuposDisponibles(): Entero
+ admiteInscripcion(socio: Socio): Booleano
+ programar(condiciones: Texto, responsable: Usuario): Booleano
```

- Atributo `titulo: Texto` — Planificado; fuente: HU-039–047; SQL 01–02.
- Atributo `modalidad: Texto` — Planificado; fuente: HU-039–047; SQL 01–02.
- Atributo `lugarOEnlace: Texto` — Planificado; fuente: HU-039–047; SQL 01–02.
- Atributo `fecha: FechaHora` — Planificado; fuente: HU-039–047; SQL 01–02.
- Atributo `cupo: Entero` — Planificado; fuente: HU-039–047; SQL 01–02.
- Atributo `estado: EstadoTaller` — Planificado; fuente: HU-039–047; SQL 01–02.
Reglas: R10. HU directas: HU-046.
Fuentes: HU-039–047; SQL 01–02.

- `calcularCuposDisponibles(): Entero` — Consulta; Responsabilidad conceptual; Planificado. Fuente: HU-039–047; SQL 01–02.
- `admiteInscripcion(socio: Socio): Booleano` — Consulta; Responsabilidad conceptual; Planificado. Fuente: HU-039–047; SQL 01–02.
- `programar(condiciones: Texto, responsable: Usuario): Booleano` — Cambio de estado; Responsabilidad conceptual; Planificado. Fuente: HU-039–047; SQL 01–02.
## InscripcionTaller

Dominio: Formacion. Estereotipo: Entidad. Estado: **Planificado**.

Representa inscripción y asistencia (tabla asistencia_taller). Una por socio–taller, premio una vez. HU-047. Estado se refiere al comportamiento observado; toda organización en clases y sus firmas es análisis, no equivalencia literal con métodos Python.

```text
- inscritaEn: FechaHora
- asistio: Booleano
- asistenciaRegistradaEn: FechaHora [0..1]
+ registrarAsistencia(responsable: Usuario): Booleano
+ habilitaReconocimiento(): Booleano
```

- Atributo `inscritaEn: FechaHora` — Planificado; fuente: HU-039–047; SQL 01–02.
- Atributo `asistio: Booleano` — Planificado; fuente: HU-039–047; SQL 01–02.
- Atributo `asistenciaRegistradaEn: FechaHora [0..1]` — Planificado; fuente: HU-039–047; SQL 01–02.
Reglas: R10. HU directas: HU-047.
Fuentes: HU-039–047; SQL 01–02.

- `registrarAsistencia(responsable: Usuario): Booleano` — Cambio de estado; Responsabilidad conceptual; Planificado. Fuente: HU-039–047; SQL 01–02.
- `habilitaReconocimiento(): Booleano` — Consulta; Responsabilidad conceptual; Planificado. Fuente: HU-039–047; SQL 01–02.
## Pregunta

Dominio: Preguntas. Estereotipo: Entidad. Estado: **Planificado**.

Propietario exclusivo evaluación XOR juego según SQL 02. Parejas para emparejar pendientes P08. HU-041/HU-072. Estado se refiere al comportamiento observado; toda organización en clases y sus firmas es análisis, no equivalencia literal con métodos Python.

```text
- enunciado: Texto
- tipo: Texto
- criterioCorreccion: Texto
+ evaluar(respuesta: RespuestaActividad): Decimal
```

- Atributo `enunciado: Texto` — Planificado; fuente: HU-041/072/074; SQL 02, ck_pregunta_dueno.
- Atributo `tipo: Texto` — Planificado; fuente: HU-041/072/074; SQL 02, ck_pregunta_dueno.
- Atributo `criterioCorreccion: Texto` — Planificado; fuente: HU-041/072/074; SQL 02, ck_pregunta_dueno.
Reglas: R11. HU directas: concepto de apoyo.
Fuentes: HU-041/072/074; SQL 02, ck_pregunta_dueno.

- `evaluar(respuesta: RespuestaActividad): Decimal` — Cambio de estado; Responsabilidad conceptual; Planificado. Fuente: HU-041/072/074; SQL 02, ck_pregunta_dueno.
## OpcionPregunta

Dominio: Preguntas. Estereotipo: Entidad. Estado: **Planificado**.

Alternativa de pregunta. SQL solo permite una correcta; no extrapolar a todos los juegos. HU-041/HU-072. Estado se refiere al comportamiento observado; toda organización en clases y sus firmas es análisis, no equivalencia literal con métodos Python.

```text
- texto: Texto
- correcta: Booleano
```
Sin operaciones propias: evidencia o dato cuya invariante aplica su dueño.
- Atributo `texto: Texto` — Planificado; fuente: HU-041/072/074; SQL 02, ck_pregunta_dueno.
- Atributo `correcta: Booleano` — Planificado; fuente: HU-041/072/074; SQL 02, ck_pregunta_dueno.
Reglas: R11. HU directas: concepto de apoyo.
Fuentes: HU-041/072/074; SQL 02, ck_pregunta_dueno.

## RespuestaActividad

Dominio: Preguntas. Estereotipo: ObjetoValor. Estado: **Propuesta de análisis**.

Objeto de valor propuesto, propiedad exclusiva de un intento de evaluación o una partida; referencia la pregunta respondida. HU-041/HU-074. Estado se refiere al comportamiento observado; toda organización en clases y sus firmas es análisis, no equivalencia literal con métodos Python.

```text
- contenido: Texto
- respondidaEn: FechaHora
```
Sin operaciones propias: evidencia o dato cuya invariante aplica su dueño.
- Atributo `contenido: Texto` — Propuesta de análisis; fuente: HU-041/072/074; SQL 02, ck_pregunta_dueno.
- Atributo `respondidaEn: FechaHora` — Propuesta de análisis; fuente: HU-041/072/074; SQL 02, ck_pregunta_dueno.
Reglas: R11. HU directas: concepto de apoyo.
Fuentes: HU-041/072/074; SQL 02, ck_pregunta_dueno.

## Sorteo

Dominio: Sorteos. Estereotipo: Entidad. Estado: **Planificado**.

Ejecución única con lista congelada y selección segura. HU-048–053; campos de evidencia son propuesta, no funcionalidad existente. Estado se refiere al comportamiento observado; toda organización en clases y sus firmas es análisis, no equivalencia literal con métodos Python.

```text
- nombre: Texto
- fecha: FechaHora
- condiciones: Texto
- numeroGanadores: Entero
- numeroSuplentes: Entero
- estado: Texto
+ verificarElegibilidad(socio: Socio): Booleano
+ congelarElegibles(): EvidenciaSorteo
+ ejecutar(responsable: Usuario): Coleccion<ResultadoSorteo>
+ publicarResultados(): Booleano
+ configurar(condiciones: Texto, responsable: Usuario): Booleano
+ consultarHistorial(solicitante: Usuario): EvidenciaSorteo
```

- Atributo `nombre: Texto` — Planificado; fuente: HU-048–053; SQL 01–02.
- Atributo `fecha: FechaHora` — Planificado; fuente: HU-048–053; SQL 01–02.
- Atributo `condiciones: Texto` — Planificado; fuente: HU-048–053; SQL 01–02.
- Atributo `numeroGanadores: Entero` — Planificado; fuente: HU-048–053; SQL 01–02.
- Atributo `numeroSuplentes: Entero` — Planificado; fuente: HU-048–053; SQL 01–02.
- Atributo `estado: Texto` — Planificado; fuente: HU-048–053; SQL 01–02.
Reglas: R12. HU directas: HU-048, HU-050, HU-053.
Fuentes: HU-048–053; SQL 01–02.

- `verificarElegibilidad(socio: Socio): Booleano` — Consulta; Responsabilidad conceptual; Planificado. Fuente: HU-048–053; SQL 01–02.
- `congelarElegibles(): EvidenciaSorteo` — Cambio de estado; Responsabilidad conceptual; Planificado. Fuente: HU-048–053; SQL 01–02.
- `ejecutar(responsable: Usuario): Coleccion<ResultadoSorteo>` — Cambio de estado; Responsabilidad conceptual; Planificado. Fuente: HU-048–053; SQL 01–02.
- `publicarResultados(): Booleano` — Cambio de estado; Responsabilidad conceptual; Planificado. Fuente: HU-048–053; SQL 01–02.
- `configurar(condiciones: Texto, responsable: Usuario): Booleano` — Cambio de estado; Responsabilidad conceptual; Planificado. Fuente: HU-048–053; SQL 01–02.
- `consultarHistorial(solicitante: Usuario): EvidenciaSorteo` — Consulta; Responsabilidad conceptual; Planificado. Fuente: HU-048–053; SQL 01–02.
## ParticipacionSorteo

Dominio: Sorteos. Estereotipo: Entidad. Estado: **Planificado**.

Participación por socio, sorteo y actividad; sin duplicados no permitidos. HU-049. Estado se refiere al comportamiento observado; toda organización en clases y sus firmas es análisis, no equivalencia literal con métodos Python.

```text
- registradaEn: FechaHora
- claveOrigen: Texto
- elegibleAlCierre: Booleano
+ validarOrigen(): Booleano
```

- Atributo `registradaEn: FechaHora` — Planificado; fuente: HU-048–053; SQL 01–02.
- Atributo `claveOrigen: Texto` — Planificado; fuente: HU-048–053; SQL 01–02.
- Atributo `elegibleAlCierre: Booleano` — Planificado; fuente: HU-048–053; SQL 01–02.
Reglas: R12. HU directas: HU-049.
Fuentes: HU-048–053; SQL 01–02.

- `validarOrigen(): Booleano` — Cambio de estado; Responsabilidad conceptual; Planificado. Fuente: HU-048–053; SQL 01–02.
## PremioSorteo

Dominio: Sorteos. Estereotipo: Registro. Estado: **Planificado**.

Premio configurado; SQL 02 premio_sorteo. HU-048/HU-052. Estado se refiere al comportamiento observado; toda organización en clases y sus firmas es análisis, no equivalencia literal con métodos Python.

```text
- descripcion: Texto
- posicion: Entero
- condicionesReclamo: Texto
```
Sin operaciones propias: evidencia o dato cuya invariante aplica su dueño.
- Atributo `descripcion: Texto` — Planificado; fuente: HU-048–053; SQL 01–02.
- Atributo `posicion: Entero` — Planificado; fuente: HU-048–053; SQL 01–02.
- Atributo `condicionesReclamo: Texto` — Planificado; fuente: HU-048–053; SQL 01–02.
Reglas: R12. HU directas: concepto de apoyo.
Fuentes: HU-048–053; SQL 01–02.

## EvidenciaSorteo

Dominio: Sorteos. Estereotipo: Registro. Estado: **Propuesta de análisis**.

Registro propuesto para lista congelada, proceso y resultado; conservar inmutable tras ejecución. HU-050/HU-053. Estado se refiere al comportamiento observado; toda organización en clases y sus firmas es análisis, no equivalencia literal con métodos Python.

```text
- hashLista: Texto
- congeladaEn: FechaHora
- ejecutadoEn: FechaHora [0..1]
- referenciaMetodoSeleccion: Texto
- evidenciaEjecucion: Texto [0..1]
+ verificarIntegridad(): Booleano
```

- Atributo `hashLista: Texto` — Propuesta de análisis; fuente: HU-048–053; SQL 01–02.
- Atributo `congeladaEn: FechaHora` — Propuesta de análisis; fuente: HU-048–053; SQL 01–02.
- Atributo `ejecutadoEn: FechaHora [0..1]` — Propuesta de análisis; fuente: HU-048–053; SQL 01–02.
- Atributo `referenciaMetodoSeleccion: Texto` — Propuesta de análisis; fuente: HU-048–053; SQL 01–02.
- Atributo `evidenciaEjecucion: Texto [0..1]` — Propuesta de análisis; fuente: HU-048–053; SQL 01–02.
Reglas: R12. HU directas: concepto de apoyo.
Fuentes: HU-048–053; SQL 01–02.

- `verificarIntegridad(): Booleano` — Consulta; Responsabilidad conceptual; Propuesta de análisis. Fuente: HU-048–053; SQL 01–02.
## ResultadoSorteo

Dominio: Sorteos. Estereotipo: Registro. Estado: **Planificado**.

Vincula participación de ese mismo sorteo; premio opcional para suplente. HU-050/HU-051; SQL ganador. Estado se refiere al comportamiento observado; toda organización en clases y sus firmas es análisis, no equivalencia literal con métodos Python.

```text
- posicion: Entero
- esSuplente: Booleano
- registradoEn: FechaHora
+ obtenerDatosPublicos(): Texto
```

- Atributo `posicion: Entero` — Planificado; fuente: HU-048–053; SQL 01–02.
- Atributo `esSuplente: Booleano` — Planificado; fuente: HU-048–053; SQL 01–02.
- Atributo `registradoEn: FechaHora` — Planificado; fuente: HU-048–053; SQL 01–02.
Reglas: R12. HU directas: HU-051.
Fuentes: HU-048–053; SQL 01–02.

- `obtenerDatosPublicos(): Texto` — Consulta; Responsabilidad conceptual; Planificado. Fuente: HU-048–053; SQL 01–02.
## Beneficio

Dominio: Recompensas. Estereotipo: Entidad. Estado: **Planificado**.

Stock nulo puede representar ilimitado según SQL; política de costo cero pendiente P02. Convenio vencido bloquea disponibilidad. HU-054/HU-057/HU-086. Estado se refiere al comportamiento observado; toda organización en clases y sus firmas es análisis, no equivalencia literal con métodos Python.

```text
- nombre: Texto
- descripcion: Texto
- costoPuntos: Entero
- stock: Entero [0..1]
- condiciones: Texto
- inicio: Fecha [0..1]
- fin: Fecha [0..1]
- activo: Booleano
+ estaDisponible(fecha: Fecha): Booleano
+ cumpleCondiciones(socio: Socio): Booleano
+ calcularStockDisponible(): Entero
+ configurar(condiciones: Texto, responsable: Usuario): Booleano
```

- Atributo `nombre: Texto` — Planificado; fuente: HU-054–059; SQL 01–02; Acta, alcance; HU-084–086; RNF-24.
- Atributo `descripcion: Texto` — Planificado; fuente: HU-054–059; SQL 01–02; Acta, alcance; HU-084–086; RNF-24.
- Atributo `costoPuntos: Entero` — Planificado; fuente: HU-054–059; SQL 01–02; Acta, alcance; HU-084–086; RNF-24.
- Atributo `stock: Entero [0..1]` — Planificado; fuente: HU-054–059; SQL 01–02; Acta, alcance; HU-084–086; RNF-24.
- Atributo `condiciones: Texto` — Planificado; fuente: HU-054–059; SQL 01–02; Acta, alcance; HU-084–086; RNF-24.
- Atributo `inicio: Fecha [0..1]` — Planificado; fuente: HU-054–059; SQL 01–02; Acta, alcance; HU-084–086; RNF-24.
- Atributo `fin: Fecha [0..1]` — Planificado; fuente: HU-054–059; SQL 01–02; Acta, alcance; HU-084–086; RNF-24.
- Atributo `activo: Booleano` — Planificado; fuente: HU-054–059; SQL 01–02; Acta, alcance; HU-084–086; RNF-24.
Reglas: R13, R16. HU directas: HU-054, HU-057.
Fuentes: HU-054–059; SQL 01–02; Acta, alcance; HU-084–086; RNF-24.

- `estaDisponible(fecha: Fecha): Booleano` — Consulta; Responsabilidad conceptual; Planificado. Fuente: HU-054–059; SQL 01–02; Acta, alcance; HU-084–086; RNF-24.
- `cumpleCondiciones(socio: Socio): Booleano` — Consulta; Responsabilidad conceptual; Planificado. Fuente: HU-054–059; SQL 01–02; Acta, alcance; HU-084–086; RNF-24.
- `calcularStockDisponible(): Entero` — Consulta; Responsabilidad conceptual; Planificado. Fuente: HU-054–059; SQL 01–02; Acta, alcance; HU-084–086; RNF-24.
- `configurar(condiciones: Texto, responsable: Usuario): Booleano` — Cambio de estado; Responsabilidad conceptual; Planificado. Fuente: HU-054–059; SQL 01–02; Acta, alcance; HU-084–086; RNF-24.
## Canje

Dominio: Recompensas. Estereotipo: Entidad. Estado: **Planificado**.

Coordina reserva, descuento/liberación y stock con CuentaPuntos; evidencia de condiciones propuesta. HU-055/HU-056/HU-058/HU-059. Estado se refiere al comportamiento observado; toda organización en clases y sus firmas es análisis, no equivalencia literal con métodos Python.

```text
- solicitadoEn: FechaHora
- puntosComprometidos: Entero
- condicionesReconocidas: Texto
- estado: EstadoCanje
- entregadoEn: FechaHora [0..1]
+ solicitar(): Booleano
+ aprobar(responsable: Usuario): Booleano
+ rechazar(motivo: Texto, responsable: Usuario): Booleano
+ registrarEntrega(responsable: Usuario): Booleano
+ consultarEstado(solicitante: Usuario): EstadoCanje
```

- Atributo `solicitadoEn: FechaHora` — Planificado; fuente: HU-055/059; CU reservar sin doble débito; SQL 01; decisión P07; HU-054–059; SQL 01–02.
- Atributo `puntosComprometidos: Entero` — Planificado; fuente: HU-055/059; CU reservar sin doble débito; SQL 01; decisión P07; HU-054–059; SQL 01–02.
- Atributo `condicionesReconocidas: Texto` — Planificado; fuente: HU-055/059; CU reservar sin doble débito; SQL 01; decisión P07; HU-054–059; SQL 01–02.
- Atributo `estado: EstadoCanje` — Planificado; fuente: HU-055/059; CU reservar sin doble débito; SQL 01; decisión P07; HU-054–059; SQL 01–02.
- Atributo `entregadoEn: FechaHora [0..1]` — Planificado; fuente: HU-055/059; CU reservar sin doble débito; SQL 01; decisión P07; HU-054–059; SQL 01–02.
Reglas: R08, R13. HU directas: HU-055, HU-056, HU-058.
Fuentes: HU-055/059; CU reservar sin doble débito; SQL 01; decisión P07; HU-054–059; SQL 01–02.

- `solicitar(): Booleano` — Cambio de estado; Responsabilidad conceptual; Planificado. Fuente: HU-055/059; CU reservar sin doble débito; SQL 01; decisión P07; HU-054–059; SQL 01–02.
- `aprobar(responsable: Usuario): Booleano` — Cambio de estado; Responsabilidad conceptual; Planificado. Fuente: HU-055/059; CU reservar sin doble débito; SQL 01; decisión P07; HU-054–059; SQL 01–02.
- `rechazar(motivo: Texto, responsable: Usuario): Booleano` — Cambio de estado; Responsabilidad conceptual; Planificado. Fuente: HU-055/059; CU reservar sin doble débito; SQL 01; decisión P07; HU-054–059; SQL 01–02.
- `registrarEntrega(responsable: Usuario): Booleano` — Cambio de estado; Responsabilidad conceptual; Planificado. Fuente: HU-055/059; CU reservar sin doble débito; SQL 01; decisión P07; HU-054–059; SQL 01–02.
- `consultarEstado(solicitante: Usuario): EstadoCanje` — Consulta; Responsabilidad conceptual; Planificado. Fuente: HU-055/059; CU reservar sin doble débito; SQL 01; decisión P07; HU-054–059; SQL 01–02.
## ContenidoInstitucional

Dominio: Contenidos. Estereotipo: Entidad. Estado: **Planificado**.

Noticias, comunicados y multimedia; distinta de publicación comunitaria. HU-060/HU-061/HU-063/HU-064/HU-065. Estado se refiere al comportamiento observado; toda organización en clases y sus firmas es análisis, no equivalencia literal con métodos Python.

```text
- titulo: Texto
- cuerpo: Texto
- categoria: Texto
- tipo: Texto
- estado: Texto
- desde: Fecha [0..1]
- hasta: Fecha [0..1]
- requiereAprobacion: Booleano
+ solicitarAprobacion(): Booleano
+ publicar(responsable: Usuario): Booleano
+ retirar(motivo: Texto): Booleano
+ esVisible(fecha: Fecha): Booleano
+ decidirAprobacion(aprobar: Booleano, motivo: Texto, responsable: Usuario): AprobacionContenido
```

- Atributo `titulo: Texto` — Planificado; fuente: HU-060–065/079–083; SQL 01–02.
- Atributo `cuerpo: Texto` — Planificado; fuente: HU-060–065/079–083; SQL 01–02.
- Atributo `categoria: Texto` — Planificado; fuente: HU-060–065/079–083; SQL 01–02.
- Atributo `tipo: Texto` — Planificado; fuente: HU-060–065/079–083; SQL 01–02.
- Atributo `estado: Texto` — Planificado; fuente: HU-060–065/079–083; SQL 01–02.
- Atributo `desde: Fecha [0..1]` — Planificado; fuente: HU-060–065/079–083; SQL 01–02.
- Atributo `hasta: Fecha [0..1]` — Planificado; fuente: HU-060–065/079–083; SQL 01–02.
- Atributo `requiereAprobacion: Booleano` — Planificado; fuente: HU-060–065/079–083; SQL 01–02.
Reglas: R14. HU directas: HU-060, HU-061, HU-063, HU-064, HU-065.
Fuentes: HU-060–065/079–083; SQL 01–02.

- `solicitarAprobacion(): Booleano` — Cambio de estado; Responsabilidad conceptual; Planificado. Fuente: HU-060–065/079–083; SQL 01–02.
- `publicar(responsable: Usuario): Booleano` — Cambio de estado; Responsabilidad conceptual; Planificado. Fuente: HU-060–065/079–083; SQL 01–02.
- `retirar(motivo: Texto): Booleano` — Cambio de estado; Responsabilidad conceptual; Planificado. Fuente: HU-060–065/079–083; SQL 01–02.
- `esVisible(fecha: Fecha): Booleano` — Consulta; Responsabilidad conceptual; Planificado. Fuente: HU-060–065/079–083; SQL 01–02.
- `decidirAprobacion(aprobar: Booleano, motivo: Texto, responsable: Usuario): AprobacionContenido` — Cambio de estado; Responsabilidad conceptual; Planificado. Fuente: HU-060–065/079–083; SQL 01–02.
## AprobacionContenido

Dominio: Contenidos. Estereotipo: Registro. Estado: **Propuesta de análisis**.

Evidencia propuesta de aprobación opcional por responsable designado; no tabla existente confirmada. HU-065. Estado se refiere al comportamiento observado; toda organización en clases y sus firmas es análisis, no equivalencia literal con métodos Python.

```text
- decididaEn: FechaHora
- decision: Texto
- observacion: Texto [0..1]
```
Sin operaciones propias: evidencia o dato cuya invariante aplica su dueño.
- Atributo `decididaEn: FechaHora` — Propuesta de análisis; fuente: HU-060–065/079–083; SQL 01–02.
- Atributo `decision: Texto` — Propuesta de análisis; fuente: HU-060–065/079–083; SQL 01–02.
- Atributo `observacion: Texto [0..1]` — Propuesta de análisis; fuente: HU-060–065/079–083; SQL 01–02.
Reglas: R14. HU directas: concepto de apoyo.
Fuentes: HU-060–065/079–083; SQL 01–02.

## MaterialEducativo

Dominio: Contenidos. Estereotipo: Entidad. Estado: **Planificado**.

Repositorio reutilizable; archivo máximo 10 MB y tipos autorizados. SQL material/contenido; HU-062/HU-044. Estado se refiere al comportamiento observado; toda organización en clases y sus firmas es análisis, no equivalencia literal con métodos Python.

```text
- titulo: Texto
- categoria: Texto
- formato: Texto
- tamanoBytes: Entero
- recurso: Texto
+ esAdmisible(): Booleano
```

- Atributo `titulo: Texto` — Planificado; fuente: HU-060–065/079–083; SQL 01–02.
- Atributo `categoria: Texto` — Planificado; fuente: HU-060–065/079–083; SQL 01–02.
- Atributo `formato: Texto` — Planificado; fuente: HU-060–065/079–083; SQL 01–02.
- Atributo `tamanoBytes: Entero` — Planificado; fuente: HU-060–065/079–083; SQL 01–02.
- Atributo `recurso: Texto` — Planificado; fuente: HU-060–065/079–083; SQL 01–02.
Reglas: R14. HU directas: HU-062.
Fuentes: HU-060–065/079–083; SQL 01–02.

- `esAdmisible(): Booleano` — Consulta; Responsabilidad conceptual; Planificado. Fuente: HU-060–065/079–083; SQL 01–02.
## PlantillaNotificacion

Dominio: Notificaciones. Estereotipo: Entidad. Estado: **Planificado**.

Plantilla por evento y canal; naturaleza obligatoria propuesta pendiente P14. HU-066. Estado se refiere al comportamiento observado; toda organización en clases y sus firmas es análisis, no equivalencia literal con métodos Python.

```text
- titulo: Texto
- cuerpo: Texto
- evento: Texto
- canal: Canal
- obligatoria: Booleano
+ prepararMensaje(datos: Texto): Texto
+ definirContenido(titulo: Texto, cuerpo: Texto, responsable: Usuario): Booleano
```

- Atributo `titulo: Texto` — Planificado; fuente: HU-052/066–070; RNF-18; SQL 01.
- Atributo `cuerpo: Texto` — Planificado; fuente: HU-052/066–070; RNF-18; SQL 01.
- Atributo `evento: Texto` — Planificado; fuente: HU-052/066–070; RNF-18; SQL 01.
- Atributo `canal: Canal` — Planificado; fuente: HU-052/066–070; RNF-18; SQL 01.
- Atributo `obligatoria: Booleano` — Planificado; fuente: HU-052/066–070; RNF-18; SQL 01.
Reglas: R17. HU directas: HU-066.
Fuentes: HU-052/066–070; RNF-18; SQL 01.

- `prepararMensaje(datos: Texto): Texto` — Cambio de estado; Responsabilidad conceptual; Planificado. Fuente: HU-052/066–070; RNF-18; SQL 01.
- `definirContenido(titulo: Texto, cuerpo: Texto, responsable: Usuario): Booleano` — Cambio de estado; Responsabilidad conceptual; Planificado. Fuente: HU-052/066–070; RNF-18; SQL 01.
## PreferenciaNotificacion

Dominio: Notificaciones. Estereotipo: Entidad. Estado: **Planificado**.

No puede desactivar comunicación obligatoria. HU-067; SQL preferencia_notificacion. Estado se refiere al comportamiento observado; toda organización en clases y sus firmas es análisis, no equivalencia literal con métodos Python.

```text
- evento: Texto
- canal: Canal
- habilitada: Booleano
+ permiteEnvio(obligatoria: Booleano): Booleano
```

- Atributo `evento: Texto` — Planificado; fuente: HU-052/066–070; RNF-18; SQL 01.
- Atributo `canal: Canal` — Planificado; fuente: HU-052/066–070; RNF-18; SQL 01.
- Atributo `habilitada: Booleano` — Planificado; fuente: HU-052/066–070; RNF-18; SQL 01.
Reglas: R17. HU directas: HU-067.
Fuentes: HU-052/066–070; RNF-18; SQL 01.

- `permiteEnvio(obligatoria: Booleano): Booleano` — Consulta; Responsabilidad conceptual; Planificado. Fuente: HU-052/066–070; RNF-18; SQL 01.
## Notificacion

Dominio: Notificaciones. Estereotipo: Entidad. Estado: **Planificado**.

Aviso de bandeja y sus envíos; separación conceptual propuesta respecto de fila SQL por canal. HU-068/HU-069. Estado se refiere al comportamiento observado; toda organización en clases y sus firmas es análisis, no equivalencia literal con métodos Python.

```text
- evento: Texto
- creadaEn: FechaHora
- leidaEn: FechaHora [0..1]
- titulo: Texto
- mensaje: Texto
+ marcarLeida(destinatario: Usuario): Booleano
```

- Atributo `evento: Texto` — Planificado; fuente: HU-052/066–070; RNF-18; SQL 01.
- Atributo `creadaEn: FechaHora` — Planificado; fuente: HU-052/066–070; RNF-18; SQL 01.
- Atributo `leidaEn: FechaHora [0..1]` — Planificado; fuente: HU-052/066–070; RNF-18; SQL 01.
- Atributo `titulo: Texto` — Planificado; fuente: HU-052/066–070; RNF-18; SQL 01.
- Atributo `mensaje: Texto` — Planificado; fuente: HU-052/066–070; RNF-18; SQL 01.
Reglas: R17. HU directas: HU-069.
Fuentes: HU-052/066–070; RNF-18; SQL 01.

- `marcarLeida(destinatario: Usuario): Booleano` — Cambio de estado; Responsabilidad conceptual; Planificado. Fuente: HU-052/066–070; RNF-18; SQL 01.
## EnvioNotificacion

Dominio: Notificaciones. Estereotipo: Entidad. Estado: **Planificado**.

Historial de entrega por canal sin bloquear operación principal; hasta tres reintentos, número total de intentos requiere convención explícita. HU-068/HU-070. Estado se refiere al comportamiento observado; toda organización en clases y sus firmas es análisis, no equivalencia literal con métodos Python.

```text
- canal: Canal
- estado: Texto
- intentos: Entero
- enviadaEn: FechaHora [0..1]
- ultimoError: Texto [0..1]
+ programar(): Booleano
+ puedeReintentarse(): Booleano
+ registrarResultado(exito: Booleano, fecha: FechaHora): Booleano
```

- Atributo `canal: Canal` — Planificado; fuente: HU-052/066–070; RNF-18; SQL 01.
- Atributo `estado: Texto` — Planificado; fuente: HU-052/066–070; RNF-18; SQL 01.
- Atributo `intentos: Entero` — Planificado; fuente: HU-052/066–070; RNF-18; SQL 01.
- Atributo `enviadaEn: FechaHora [0..1]` — Planificado; fuente: HU-052/066–070; RNF-18; SQL 01.
- Atributo `ultimoError: Texto [0..1]` — Planificado; fuente: HU-052/066–070; RNF-18; SQL 01.
Reglas: R17. HU directas: concepto de apoyo.
Fuentes: HU-052/066–070; RNF-18; SQL 01.

- `programar(): Booleano` — Cambio de estado; Responsabilidad conceptual; Planificado. Fuente: HU-052/066–070; RNF-18; SQL 01.
- `puedeReintentarse(): Booleano` — Consulta; Responsabilidad conceptual; Planificado. Fuente: HU-052/066–070; RNF-18; SQL 01.
- `registrarResultado(exito: Booleano, fecha: FechaHora): Booleano` — Cambio de estado; Responsabilidad conceptual; Planificado. Fuente: HU-052/066–070; RNF-18; SQL 01.
## Juego

Dominio: JuegosRetos. Estereotipo: Entidad. Estado: **Planificado**.

Juego educativo configurable; criterios derivados de HU pendientes de persistencia completa. HU-071/HU-072/HU-073/HU-076. Estado se refiere al comportamiento observado; toda organización en clases y sus firmas es análisis, no equivalencia literal con métodos Python.

```text
- nombre: Texto
- instrucciones: Texto
- tipo: TipoJuego
- activo: Booleano
- maximoIntentos: Entero
- criteriosPuntuacion: Texto
- criteriosFinalizacion: Texto
+ admitePartida(socio: Socio): Booleano
+ calcularIntentosRestantes(socio: Socio): Entero
+ activar(): Booleano
+ desactivar(): Booleano
+ definirContenido(instrucciones: Texto, preguntas: Coleccion<Pregunta>, responsable: Usuario): Booleano
```

- Atributo `nombre: Texto` — Planificado; fuente: HU-041/072/074; SQL 02, ck_pregunta_dueno; HU-071–078; SQL 01.
- Atributo `instrucciones: Texto` — Planificado; fuente: HU-041/072/074; SQL 02, ck_pregunta_dueno; HU-071–078; SQL 01.
- Atributo `tipo: TipoJuego` — Planificado; fuente: HU-041/072/074; SQL 02, ck_pregunta_dueno; HU-071–078; SQL 01.
- Atributo `activo: Booleano` — Planificado; fuente: HU-041/072/074; SQL 02, ck_pregunta_dueno; HU-071–078; SQL 01.
- Atributo `maximoIntentos: Entero` — Planificado; fuente: HU-041/072/074; SQL 02, ck_pregunta_dueno; HU-071–078; SQL 01.
- Atributo `criteriosPuntuacion: Texto` — Planificado; fuente: HU-041/072/074; SQL 02, ck_pregunta_dueno; HU-071–078; SQL 01.
- Atributo `criteriosFinalizacion: Texto` — Planificado; fuente: HU-041/072/074; SQL 02, ck_pregunta_dueno; HU-071–078; SQL 01.
Reglas: R11, R15. HU directas: HU-071, HU-072, HU-073, HU-076.
Fuentes: HU-041/072/074; SQL 02, ck_pregunta_dueno; HU-071–078; SQL 01.

- `admitePartida(socio: Socio): Booleano` — Consulta; Responsabilidad conceptual; Planificado. Fuente: HU-041/072/074; SQL 02, ck_pregunta_dueno; HU-071–078; SQL 01.
- `calcularIntentosRestantes(socio: Socio): Entero` — Consulta; Responsabilidad conceptual; Planificado. Fuente: HU-041/072/074; SQL 02, ck_pregunta_dueno; HU-071–078; SQL 01.
- `activar(): Booleano` — Cambio de estado; Responsabilidad conceptual; Planificado. Fuente: HU-041/072/074; SQL 02, ck_pregunta_dueno; HU-071–078; SQL 01.
- `desactivar(): Booleano` — Cambio de estado; Responsabilidad conceptual; Planificado. Fuente: HU-041/072/074; SQL 02, ck_pregunta_dueno; HU-071–078; SQL 01.
- `definirContenido(instrucciones: Texto, preguntas: Coleccion<Pregunta>, responsable: Usuario): Booleano` — Cambio de estado; Responsabilidad conceptual; Planificado. Fuente: HU-041/072/074; SQL 02, ck_pregunta_dueno; HU-071–078; SQL 01.
## Partida

Dominio: JuegosRetos. Estereotipo: Entidad. Estado: **Planificado**.

Resultado calculado en servidor; no aceptar puntaje final del cliente. HU-074/HU-075. Estado se refiere al comportamiento observado; toda organización en clases y sus firmas es análisis, no equivalencia literal con métodos Python.

```text
- iniciadaEn: FechaHora
- finalizadaEn: FechaHora [0..1]
- puntuacion: Decimal [0..1]
- resultadoValido: Booleano
+ calcularResultado(): Decimal
+ finalizar(): Booleano
+ habilitaReconocimiento(): Booleano
```

- Atributo `iniciadaEn: FechaHora` — Planificado; fuente: HU-041/072/074; SQL 02, ck_pregunta_dueno; HU-071–078; SQL 01.
- Atributo `finalizadaEn: FechaHora [0..1]` — Planificado; fuente: HU-041/072/074; SQL 02, ck_pregunta_dueno; HU-071–078; SQL 01.
- Atributo `puntuacion: Decimal [0..1]` — Planificado; fuente: HU-041/072/074; SQL 02, ck_pregunta_dueno; HU-071–078; SQL 01.
- Atributo `resultadoValido: Booleano` — Planificado; fuente: HU-041/072/074; SQL 02, ck_pregunta_dueno; HU-071–078; SQL 01.
Reglas: R11, R15. HU directas: HU-074, HU-075.
Fuentes: HU-041/072/074; SQL 02, ck_pregunta_dueno; HU-071–078; SQL 01.

- `calcularResultado(): Decimal` — Consulta; Responsabilidad conceptual; Planificado. Fuente: HU-041/072/074; SQL 02, ck_pregunta_dueno; HU-071–078; SQL 01.
- `finalizar(): Booleano` — Cambio de estado; Responsabilidad conceptual; Planificado. Fuente: HU-041/072/074; SQL 02, ck_pregunta_dueno; HU-071–078; SQL 01.
- `habilitaReconocimiento(): Booleano` — Consulta; Responsabilidad conceptual; Planificado. Fuente: HU-041/072/074; SQL 02, ck_pregunta_dueno; HU-071–078; SQL 01.
## Reto

Dominio: JuegosRetos. Estereotipo: Entidad. Estado: **Planificado**.

Tipo de actividad y cantidad medible; recompensa por regla vigente. HU-077. Estado se refiere al comportamiento observado; toda organización en clases y sus firmas es análisis, no equivalencia literal con métodos Python.

```text
- objetivo: Texto
- tipoActividad: Texto
- meta: Entero
- inicio: Fecha
- fin: Fecha
- recompensa: Entero
+ estaVigente(fecha: Fecha): Booleano
+ cumpleObjetivo(progreso: ProgresoReto): Booleano
+ definirObjetivo(tipoActividad: Texto, cantidad: Entero, responsable: Usuario): Booleano
```

- Atributo `objetivo: Texto` — Planificado; fuente: HU-071–078; SQL 01.
- Atributo `tipoActividad: Texto` — Planificado; fuente: HU-071–078; SQL 01.
- Atributo `meta: Entero` — Planificado; fuente: HU-071–078; SQL 01.
- Atributo `inicio: Fecha` — Planificado; fuente: HU-071–078; SQL 01.
- Atributo `fin: Fecha` — Planificado; fuente: HU-071–078; SQL 01.
- Atributo `recompensa: Entero` — Planificado; fuente: HU-071–078; SQL 01.
Reglas: R15. HU directas: HU-077.
Fuentes: HU-071–078; SQL 01.

- `estaVigente(fecha: Fecha): Booleano` — Consulta; Responsabilidad conceptual; Planificado. Fuente: HU-071–078; SQL 01.
- `cumpleObjetivo(progreso: ProgresoReto): Booleano` — Consulta; Responsabilidad conceptual; Planificado. Fuente: HU-071–078; SQL 01.
- `definirObjetivo(tipoActividad: Texto, cantidad: Entero, responsable: Usuario): Booleano` — Cambio de estado; Responsabilidad conceptual; Planificado. Fuente: HU-071–078; SQL 01.
## ProgresoReto

Dominio: JuegosRetos. Estereotipo: Entidad. Estado: **Planificado**.

Una recompensa por socio–reto; excluir duplicación de actividad. HU-078. Estado se refiere al comportamiento observado; toda organización en clases y sus firmas es análisis, no equivalencia literal con métodos Python.

```text
- avance: Entero
- completadoEn: FechaHora [0..1]
- recompensaReconocida: Booleano
+ incorporarActividad(actividad: ActividadValidada): Booleano
+ calcularPorcentaje(): Decimal
+ reconocerCumplimiento(fecha: Fecha): Booleano
```

- Atributo `avance: Entero` — Planificado; fuente: HU-071–078; SQL 01.
- Atributo `completadoEn: FechaHora [0..1]` — Planificado; fuente: HU-071–078; SQL 01.
- Atributo `recompensaReconocida: Booleano` — Planificado; fuente: HU-071–078; SQL 01.
Reglas: R15. HU directas: HU-078.
Fuentes: HU-071–078; SQL 01.

- `incorporarActividad(actividad: ActividadValidada): Booleano` — Cambio de estado; Responsabilidad conceptual; Planificado. Fuente: HU-071–078; SQL 01.
- `calcularPorcentaje(): Decimal` — Consulta; Responsabilidad conceptual; Planificado. Fuente: HU-071–078; SQL 01.
- `reconocerCumplimiento(fecha: Fecha): Booleano` — Cambio de estado; Responsabilidad conceptual; Planificado. Fuente: HU-071–078; SQL 01.
## PerfilPublico

Dominio: Comunidad. Estereotipo: Entidad. Estado: **Propuesta de análisis**.

Información personal oculta por defecto; vista propia de clasificación incluso excluido de pública. HU-083/HU-035. Estado se refiere al comportamiento observado; toda organización en clases y sus firmas es análisis, no equivalencia literal con métodos Python.

```text
- alias: Texto
- camposVisibles: Conjunto<Texto>
- participaClasificacionPublica: Booleano
+ definirPrivacidad(campos: Conjunto<Texto>): Booleano
+ obtenerDatosPublicos(): Texto
```

- Atributo `alias: Texto` — Propuesta de análisis; fuente: HU-033/035/037/083; HU-060–065/079–083; SQL 01–02.
- Atributo `camposVisibles: Conjunto<Texto>` — Propuesta de análisis; fuente: HU-033/035/037/083; HU-060–065/079–083; SQL 01–02.
- Atributo `participaClasificacionPublica: Booleano` — Propuesta de análisis; fuente: HU-033/035/037/083; HU-060–065/079–083; SQL 01–02.
Reglas: R09, R14. HU directas: HU-083.
Fuentes: HU-033/035/037/083; HU-060–065/079–083; SQL 01–02.

- `definirPrivacidad(campos: Conjunto<Texto>): Booleano` — Cambio de estado; Responsabilidad conceptual; Propuesta de análisis. Fuente: HU-033/035/037/083; HU-060–065/079–083; SQL 01–02.
- `obtenerDatosPublicos(): Texto` — Consulta; Responsabilidad conceptual; Propuesta de análisis. Fuente: HU-033/035/037/083; HU-060–065/079–083; SQL 01–02.
## PublicacionComunidad

Dominio: Comunidad. Estereotipo: Entidad. Estado: **Planificado**.

Solo socios autenticados; imágenes autorizadas hasta 10 MB. HU-079/HU-080. Estado se refiere al comportamiento observado; toda organización en clases y sus firmas es análisis, no equivalencia literal con métodos Python.

```text
- texto: Texto
- imagenes: Coleccion<Texto>
- creadaEn: FechaHora
- estadoModeracion: Texto
+ admiteInteraccion(): Booleano
+ publicar(autor: Socio): Booleano
```

- Atributo `texto: Texto` — Planificado; fuente: HU-060–065/079–083; SQL 01–02.
- Atributo `imagenes: Coleccion<Texto>` — Planificado; fuente: HU-060–065/079–083; SQL 01–02.
- Atributo `creadaEn: FechaHora` — Planificado; fuente: HU-060–065/079–083; SQL 01–02.
- Atributo `estadoModeracion: Texto` — Planificado; fuente: HU-060–065/079–083; SQL 01–02.
Reglas: R14. HU directas: HU-079, HU-080.
Fuentes: HU-060–065/079–083; SQL 01–02.

- `admiteInteraccion(): Booleano` — Consulta; Responsabilidad conceptual; Planificado. Fuente: HU-060–065/079–083; SQL 01–02.
- `publicar(autor: Socio): Booleano` — Cambio de estado; Responsabilidad conceptual; Planificado. Fuente: HU-060–065/079–083; SQL 01–02.
## Comentario

Dominio: Comunidad. Estereotipo: Entidad. Estado: **Planificado**.

Asociado a publicación y socio; contenido oculto no admite interacción. HU-080. Estado se refiere al comportamiento observado; toda organización en clases y sus firmas es análisis, no equivalencia literal con métodos Python.

```text
- texto: Texto
- creadoEn: FechaHora
- estadoModeracion: Texto
+ puedeMostrarse(): Booleano
```

- Atributo `texto: Texto` — Planificado; fuente: HU-060–065/079–083; SQL 01–02.
- Atributo `creadoEn: FechaHora` — Planificado; fuente: HU-060–065/079–083; SQL 01–02.
- Atributo `estadoModeracion: Texto` — Planificado; fuente: HU-060–065/079–083; SQL 01–02.
Reglas: R14. HU directas: concepto de apoyo.
Fuentes: HU-060–065/079–083; SQL 01–02.

- `puedeMostrarse(): Booleano` — Consulta; Responsabilidad conceptual; Planificado. Fuente: HU-060–065/079–083; SQL 01–02.
## Reaccion

Dominio: Comunidad. Estereotipo: Entidad. Estado: **Planificado**.

Una reacción por socio–publicación según SQL; regla de cambio pendiente si se amplía. HU-080. Estado se refiere al comportamiento observado; toda organización en clases y sus firmas es análisis, no equivalencia literal con métodos Python.

```text
- tipo: Texto
- fecha: FechaHora
```
Sin operaciones propias: evidencia o dato cuya invariante aplica su dueño.
- Atributo `tipo: Texto` — Planificado; fuente: HU-060–065/079–083; SQL 01–02.
- Atributo `fecha: FechaHora` — Planificado; fuente: HU-060–065/079–083; SQL 01–02.
Reglas: R14. HU directas: concepto de apoyo.
Fuentes: HU-060–065/079–083; SQL 01–02.

## ReporteComunidad

Dominio: Comunidad. Estereotipo: Entidad. Estado: **Propuesta de análisis**.

Reporte de publicación o comentario, exclusivamente uno. HU-081; clase propuesta sin tabla equivalente confirmada. Estado se refiere al comportamiento observado; toda organización en clases y sus firmas es análisis, no equivalencia literal con métodos Python.

```text
- motivo: Texto
- fecha: FechaHora
- estado: Texto
+ enviarAModeracion(): Booleano
```

- Atributo `motivo: Texto` — Propuesta de análisis; fuente: HU-060–065/079–083; SQL 01–02.
- Atributo `fecha: FechaHora` — Propuesta de análisis; fuente: HU-060–065/079–083; SQL 01–02.
- Atributo `estado: Texto` — Propuesta de análisis; fuente: HU-060–065/079–083; SQL 01–02.
Reglas: R14. HU directas: HU-081.
Fuentes: HU-060–065/079–083; SQL 01–02.

- `enviarAModeracion(): Booleano` — Cambio de estado; Responsabilidad conceptual; Propuesta de análisis. Fuente: HU-060–065/079–083; SQL 01–02.
## DecisionModeracion

Dominio: Comunidad. Estereotipo: Entidad. Estado: **Propuesta de análisis**.

Oculta/elimina contenido o suspende temporalmente con motivo; alcance y plazo pendientes P14. HU-082. Estado se refiere al comportamiento observado; toda organización en clases y sus firmas es análisis, no equivalencia literal con métodos Python.

```text
- accion: Texto
- motivo: Texto
- fecha: FechaHora
- suspensionHasta: FechaHora [0..1]
+ aplicar(responsable: Usuario): Booleano
```

- Atributo `accion: Texto` — Propuesta de análisis; fuente: HU-060–065/079–083; SQL 01–02.
- Atributo `motivo: Texto` — Propuesta de análisis; fuente: HU-060–065/079–083; SQL 01–02.
- Atributo `fecha: FechaHora` — Propuesta de análisis; fuente: HU-060–065/079–083; SQL 01–02.
- Atributo `suspensionHasta: FechaHora [0..1]` — Propuesta de análisis; fuente: HU-060–065/079–083; SQL 01–02.
Reglas: R14. HU directas: HU-082.
Fuentes: HU-060–065/079–083; SQL 01–02.

- `aplicar(responsable: Usuario): Booleano` — Cambio de estado; Responsabilidad conceptual; Propuesta de análisis. Fuente: HU-060–065/079–083; SQL 01–02.
## ConvenioBienestar

Dominio: Bienestar. Estereotipo: Entidad. Estado: **Planificado**.

Convenio informativo, sin datos clínicos de socios. HU-084/HU-085/HU-086. Estado se refiere al comportamiento observado; toda organización en clases y sus firmas es análisis, no equivalencia literal con métodos Python.

```text
- proveedor: Texto
- descripcion: Texto
- beneficioDescriptivo: Texto
- condiciones: Texto
- inicio: Fecha [0..1]
- fin: Fecha [0..1]
+ estaVigente(fecha: Fecha): Booleano
+ habilitaBeneficio(fecha: Fecha): Booleano
+ configurar(condiciones: Texto, responsable: Usuario): Booleano
```

- Atributo `proveedor: Texto` — Planificado; fuente: Acta, alcance; HU-084–086; RNF-24.
- Atributo `descripcion: Texto` — Planificado; fuente: Acta, alcance; HU-084–086; RNF-24.
- Atributo `beneficioDescriptivo: Texto` — Planificado; fuente: Acta, alcance; HU-084–086; RNF-24.
- Atributo `condiciones: Texto` — Planificado; fuente: Acta, alcance; HU-084–086; RNF-24.
- Atributo `inicio: Fecha [0..1]` — Planificado; fuente: Acta, alcance; HU-084–086; RNF-24.
- Atributo `fin: Fecha [0..1]` — Planificado; fuente: Acta, alcance; HU-084–086; RNF-24.
Reglas: R16. HU directas: HU-084, HU-086.
Fuentes: Acta, alcance; HU-084–086; RNF-24.

- `estaVigente(fecha: Fecha): Booleano` — Consulta; Responsabilidad conceptual; Planificado. Fuente: Acta, alcance; HU-084–086; RNF-24.
- `habilitaBeneficio(fecha: Fecha): Booleano` — Consulta; Responsabilidad conceptual; Planificado. Fuente: Acta, alcance; HU-084–086; RNF-24.
- `configurar(condiciones: Texto, responsable: Usuario): Booleano` — Cambio de estado; Responsabilidad conceptual; Planificado. Fuente: Acta, alcance; HU-084–086; RNF-24.
## RecursoBienestar

Dominio: Bienestar. Estereotipo: Entidad. Estado: **Planificado**.

Vincula contenido institucional y opcionalmente convenio. HU-085; SQL recurso_bienestar. Estado se refiere al comportamiento observado; toda organización en clases y sus firmas es análisis, no equivalencia literal con métodos Python.

```text
- titulo: Texto
- categoria: Texto
+ esVisible(fecha: Fecha): Booleano
```

- Atributo `titulo: Texto` — Planificado; fuente: Acta, alcance; HU-084–086; RNF-24.
- Atributo `categoria: Texto` — Planificado; fuente: Acta, alcance; HU-084–086; RNF-24.
Reglas: R16. HU directas: HU-085.
Fuentes: Acta, alcance; HU-084–086; RNF-24.

- `esVisible(fecha: Fecha): Booleano` — Consulta; Responsabilidad conceptual; Planificado. Fuente: Acta, alcance; HU-084–086; RNF-24.
## ServicioReportes

Dominio: Reportes. Estereotipo: ServicioDominio. Estado: **Propuesta de análisis**.

Servicio de dominio propuesto para consultas y exportaciones según rol; sin atributos artificiales. HU-087–091. Estado se refiere al comportamiento observado; toda organización en clases y sus firmas es análisis, no equivalencia literal con métodos Python.

```text
+ generarSupervision(filtro: FiltroReporte, solicitante: Usuario): ResultadoReporte
+ generarReferidosCampanas(filtro: FiltroReporte, solicitante: Usuario): ResultadoReporte
+ generarImpactoSocial(filtro: FiltroReporte, solicitante: Usuario): ResultadoReporte
+ generarGamificacion(filtro: FiltroReporte, solicitante: Usuario): ResultadoReporte
+ exportar(resultado: ResultadoReporte, formato: Texto, solicitante: Usuario): Texto
```

Reglas: R18. HU directas: HU-022, HU-087, HU-088, HU-089, HU-090, HU-091.
Fuentes: HU-087–091; RNF-06/13/14; SQL 01–02.

- `generarSupervision(filtro: FiltroReporte, solicitante: Usuario): ResultadoReporte` — Coordinación; Responsabilidad conceptual; Propuesta de análisis. Fuente: HU-087–091; RNF-06/13/14; SQL 01–02.
- `generarReferidosCampanas(filtro: FiltroReporte, solicitante: Usuario): ResultadoReporte` — Coordinación; Responsabilidad conceptual; Propuesta de análisis. Fuente: HU-087–091; RNF-06/13/14; SQL 01–02.
- `generarImpactoSocial(filtro: FiltroReporte, solicitante: Usuario): ResultadoReporte` — Coordinación; Responsabilidad conceptual; Propuesta de análisis. Fuente: HU-087–091; RNF-06/13/14; SQL 01–02.
- `generarGamificacion(filtro: FiltroReporte, solicitante: Usuario): ResultadoReporte` — Coordinación; Responsabilidad conceptual; Propuesta de análisis. Fuente: HU-087–091; RNF-06/13/14; SQL 01–02.
- `exportar(resultado: ResultadoReporte, formato: Texto, solicitante: Usuario): Texto` — Coordinación; Responsabilidad conceptual; Propuesta de análisis. Fuente: HU-087–091; RNF-06/13/14; SQL 01–02.
## FiltroReporte

Dominio: Reportes. Estereotipo: ObjetoValor. Estado: **Propuesta de análisis**.

Objeto de valor propuesto, registra filtros aplicados sin datos técnicos del framework. HU-088–091. Estado se refiere al comportamiento observado; toda organización en clases y sus firmas es análisis, no equivalencia literal con métodos Python.

```text
- desde: Fecha [0..1]
- hasta: Fecha [0..1]
- estado: Texto [0..1]
+ esValido(): Booleano
```

- Atributo `desde: Fecha [0..1]` — Propuesta de análisis; fuente: HU-087–091; RNF-06/13/14; SQL 01–02.
- Atributo `hasta: Fecha [0..1]` — Propuesta de análisis; fuente: HU-087–091; RNF-06/13/14; SQL 01–02.
- Atributo `estado: Texto [0..1]` — Propuesta de análisis; fuente: HU-087–091; RNF-06/13/14; SQL 01–02.
Reglas: R18. HU directas: concepto de apoyo.
Fuentes: HU-087–091; RNF-06/13/14; SQL 01–02.

- `esValido(): Booleano` — Consulta; Responsabilidad conceptual; Propuesta de análisis. Fuente: HU-087–091; RNF-06/13/14; SQL 01–02.
## ResultadoReporte

Dominio: Reportes. Estereotipo: ObjetoValor. Estado: **Propuesta de análisis**.

Objeto de valor propuesto de salida; conserva fecha y filtros. HU-087–091. No obliga a persistir cada consulta. Estado se refiere al comportamiento observado; toda organización en clases y sus firmas es análisis, no equivalencia literal con métodos Python.

```text
- tipo: Texto
- generadoEn: FechaHora
- indicadores: Coleccion<Texto>
- datosEnmascarados: Booleano
```
Sin operaciones propias: evidencia o dato cuya invariante aplica su dueño.
- Atributo `tipo: Texto` — Propuesta de análisis; fuente: HU-087–091; RNF-06/13/14; SQL 01–02.
- Atributo `generadoEn: FechaHora` — Propuesta de análisis; fuente: HU-087–091; RNF-06/13/14; SQL 01–02.
- Atributo `indicadores: Coleccion<Texto>` — Propuesta de análisis; fuente: HU-087–091; RNF-06/13/14; SQL 01–02.
- Atributo `datosEnmascarados: Booleano` — Propuesta de análisis; fuente: HU-087–091; RNF-06/13/14; SQL 01–02.
Reglas: R18. HU directas: concepto de apoyo.
Fuentes: HU-087–091; RNF-06/13/14; SQL 01–02.

## ServicioRegistro

Dominio: Identidad. Estereotipo: ServicioDominio. Estado: **Implementado parcialmente**.

Coordina alta atómica, unicidad, padrón, consentimiento, socio opcional, roles y auditoría. Registro público implementado; alta de personal por comando/servicio; no administración completa. HU-001/005/006/008; registro_service.py y usuarios_internos_service.py. El parámetro cuenta es una cuenta propuesta con sus datos obligatorios, aún sin alta; no es DTO ni habilita credenciales en texto almacenado. La clave es entrada transitoria. Estado se refiere al comportamiento observado; toda organización en clases y sus firmas es análisis, no equivalencia literal con métodos Python.

```text
+ registrarCuenta(cuenta: Usuario, clave: Texto, consentimiento: ConsentimientoCuenta): Usuario
+ validarUnicidad(cuenta: Usuario): Booleano
+ registrarPersonal(cuenta: Usuario, roles: Coleccion<Rol>, administrador: Usuario): Usuario
```

Reglas: R01. HU directas: HU-001, HU-005, HU-008.
Fuentes: decision-cedula-diez-digitos.md; decision-registro-general.md; registro_service.py; SQL 05–06.

- `registrarCuenta(cuenta: Usuario, clave: Texto, consentimiento: ConsentimientoCuenta): Usuario` — Coordinación; Responsabilidad conceptual; Comportamiento equivalente implementado en servicios. Fuente: decision-cedula-diez-digitos.md; decision-registro-general.md; registro_service.py; SQL 05–06.
- `validarUnicidad(cuenta: Usuario): Booleano` — Consulta; Responsabilidad conceptual; Comportamiento equivalente implementado en servicios. Fuente: decision-cedula-diez-digitos.md; decision-registro-general.md; registro_service.py; SQL 05–06.
- `registrarPersonal(cuenta: Usuario, roles: Coleccion<Rol>, administrador: Usuario): Usuario` — Coordinación; Responsabilidad conceptual; Comportamiento equivalente implementado en servicios. Fuente: decision-cedula-diez-digitos.md; decision-registro-general.md; registro_service.py; SQL 05–06.
## ServicioAutorizacion

Dominio: Seguridad. Estereotipo: ServicioDominio. Estado: **Implementado parcialmente**.

Consulta roles actuales y titularidad. Unión de accesos implementada; configuración dinámica completa de permisos y revocación administrativa planificadas. HU-012/013/014; roles_service.py y permissions.py. Estado se refiere al comportamiento observado; toda organización en clases y sus firmas es análisis, no equivalencia literal con métodos Python.

```text
+ autorizar(usuario: Usuario, accion: Texto, recurso: Texto): Booleano
+ identificarRoles(usuario: Usuario): Coleccion<Rol>
+ asignarRol(usuario: Usuario, rol: Rol, administrador: Usuario): Booleano
+ revocarRol(usuario: Usuario, rol: Rol, administrador: Usuario): Booleano
```

Reglas: R02. HU directas: HU-012, HU-013, HU-014.
Fuentes: HU-009/010/012/014/015; roles_service.py; sesiones_service.py.

- `autorizar(usuario: Usuario, accion: Texto, recurso: Texto): Booleano` — Coordinación; Responsabilidad conceptual; Comportamiento equivalente implementado en servicios. Fuente: HU-009/010/012/014/015; roles_service.py; sesiones_service.py.
- `identificarRoles(usuario: Usuario): Coleccion<Rol>` — Consulta; Responsabilidad conceptual; Comportamiento equivalente implementado en servicios. Fuente: HU-009/010/012/014/015; roles_service.py; sesiones_service.py.
- `asignarRol(usuario: Usuario, rol: Rol, administrador: Usuario): Booleano` — Coordinación; Responsabilidad conceptual; Planificado. Fuente: HU-009/010/012/014/015; roles_service.py; sesiones_service.py.
- `revocarRol(usuario: Usuario, rol: Rol, administrador: Usuario): Booleano` — Coordinación; Responsabilidad conceptual; Planificado. Fuente: HU-009/010/012/014/015; roles_service.py; sesiones_service.py.
## ElegibleCongelado

Dominio: Sorteos. Estereotipo: Registro. Estado: **Propuesta de análisis**.

Instantánea inmutable de cada participación elegible al cierre, no consulta de lista viva. Conserva identidad seudonimizada y condiciones que fundamentaron inclusión. El hash de EvidenciaSorteo se calcula sobre estas entradas con orden y serialización documentados. HU-050/053; propuesta de análisis. Estado se refiere al comportamiento observado; toda organización en clases y sus firmas es análisis, no equivalencia literal con métodos Python.

```text
- referenciaParticipacion: Texto
- referenciaSocio: Texto
- condicionValidada: Texto
- ordenCanonico: Entero
```
Sin operaciones propias: evidencia o dato cuya invariante aplica su dueño.
- Atributo `referenciaParticipacion: Texto` — Propuesta de análisis; fuente: HU-048–053; SQL 01–02.
- Atributo `referenciaSocio: Texto` — Propuesta de análisis; fuente: HU-048–053; SQL 01–02.
- Atributo `condicionValidada: Texto` — Propuesta de análisis; fuente: HU-048–053; SQL 01–02.
- Atributo `ordenCanonico: Entero` — Propuesta de análisis; fuente: HU-048–053; SQL 01–02.
Reglas: R12. HU directas: concepto de apoyo.
Fuentes: HU-048–053; SQL 01–02.

## ReconocimientoIncentivo

Dominio: Campanas. Estereotipo: Registro. Estado: **Propuesta de análisis**.

Instantánea inmutable que impide alterar incentivos reconocidos cuando cambia la campaña. Tiene origen en actividad validada y versión del incentivo; no presupone tabla implementada. HU-029; Presentacion hoja RF-04, modificar campañas. Estado se refiere al comportamiento observado; toda organización en clases y sus firmas es análisis, no equivalencia literal con métodos Python.

```text
- fecha: FechaHora
- versionReconocida: Texto
- tipoReconocido: Texto
- cantidadReconocida: Entero
- condicionesReconocidas: Texto
```
Sin operaciones propias: evidencia o dato cuya invariante aplica su dueño.
- Atributo `fecha: FechaHora` — Propuesta de análisis; fuente: HU-025–030; Presentacion RF-04; SQL 01–02.
- Atributo `versionReconocida: Texto` — Propuesta de análisis; fuente: HU-025–030; Presentacion RF-04; SQL 01–02.
- Atributo `tipoReconocido: Texto` — Propuesta de análisis; fuente: HU-025–030; Presentacion RF-04; SQL 01–02.
- Atributo `cantidadReconocida: Entero` — Propuesta de análisis; fuente: HU-025–030; Presentacion RF-04; SQL 01–02.
- Atributo `condicionesReconocidas: Texto` — Propuesta de análisis; fuente: HU-025–030; Presentacion RF-04; SQL 01–02.
Reglas: R06. HU directas: concepto de apoyo.
Fuentes: HU-025–030; Presentacion RF-04; SQL 01–02.

## ServicioNotificaciones

Dominio: Notificaciones. Estereotipo: ServicioDominio. Estado: **Propuesta de análisis**.

Coordina eventos válidos, plantillas, preferencias y entregas sin bloquear negocio. Historial consultable con autorización. Módulo general planificado; recuperación por correo no demuestra su implementación. HU-052/068/070. Estado se refiere al comportamiento observado; toda organización en clases y sus firmas es análisis, no equivalencia literal con métodos Python.

```text
+ notificarEvento(evento: Texto, destinatario: Usuario): Notificacion
+ notificarGanadores(sorteo: Sorteo): Coleccion<Notificacion>
+ consultarHistorial(filtro: FiltroReporte, solicitante: Usuario): Coleccion<EnvioNotificacion>
```

Reglas: R17. HU directas: HU-052, HU-068, HU-070.
Fuentes: HU-052/066–070; RNF-18; SQL 01.

- `notificarEvento(evento: Texto, destinatario: Usuario): Notificacion` — Coordinación; Responsabilidad conceptual; Propuesta de análisis. Fuente: HU-052/066–070; RNF-18; SQL 01.
- `notificarGanadores(sorteo: Sorteo): Coleccion<Notificacion>` — Coordinación; Responsabilidad conceptual; Propuesta de análisis. Fuente: HU-052/066–070; RNF-18; SQL 01.
- `consultarHistorial(filtro: FiltroReporte, solicitante: Usuario): Coleccion<EnvioNotificacion>` — Consulta; Responsabilidad conceptual; Propuesta de análisis. Fuente: HU-052/066–070; RNF-18; SQL 01.

## Enumeraciones

- EstadoCuenta: Activa, Suspendida, Desactivada. Fuente: backend/sql/01_base_datos_cooperativa.sql; traducción al español de los valores físicos.
- EstadoReferido: Registrado, Confirmado, EnSeguimiento, Convertido, Rechazado, Expirado. Fuente: backend/sql/01_base_datos_cooperativa.sql; traducción al español de los valores físicos.
- EstadoCampana: Borrador, Activa, Suspendida, Finalizada. Fuente: backend/sql/01_base_datos_cooperativa.sql; traducción al español de los valores físicos.
- TipoMovimiento: Acreditacion, Reserva, Descuento, Liberacion, Reverso. Fuente: backend/sql/01_base_datos_cooperativa.sql; traducción al español de los valores físicos.
- EstadoCanje: Pendiente, Aprobada, Rechazada, Entregada. Fuente: backend/sql/01_base_datos_cooperativa.sql; traducción al español de los valores físicos.
- Canal: Plataforma, Correo. Fuente: backend/sql/01_base_datos_cooperativa.sql; traducción al español de los valores físicos.
- TipoJuego: Trivia, VerdaderoFalso, Emparejar. Fuente: backend/sql/01_base_datos_cooperativa.sql; traducción al español de los valores físicos.
- TipoConversion: AperturaCuenta, ProductoCrediticio. Fuente: backend/sql/01_base_datos_cooperativa.sql; traducción al español de los valores físicos.
- TipoActividad: ConversionReferido, CapacitacionAprobada, AsistenciaTaller, Juego, Reto. Fuente: backend/sql/01_base_datos_cooperativa.sql; traducción al español de los valores físicos.
- EstadoTaller: Programado, Realizado, Cancelado. Fuente: backend/sql/02_ajustes_recomendados.sql, ck_taller_estado.