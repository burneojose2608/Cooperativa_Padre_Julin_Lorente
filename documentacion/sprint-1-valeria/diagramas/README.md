# Diagramas de la entrega de Valeria en Sprint 1

Las fuentes Mermaid corresponden al comportamiento actual, con las reglas modificadas por el usuario: diez dígitos sin verificador, cuenta general si no consta en padrón y conversión administrativa temporal.

| Diagrama | Fuente editable | Imagen SVG |
| --- | --- | --- |
| Clases del módulo de usuarios y puerto de padrón | [Mermaid](fuentes/clases-usuarios.mmd) | [Abrir SVG](clases-usuarios.svg) |
| Registro y prevención de duplicados | [Mermaid](fuentes/registro.mmd) | [Abrir SVG](registro.svg) |
| Login existente y límites de este alcance | [Mermaid](fuentes/login.mmd) | [Abrir SVG](login.svg) |
| Conversión administrativa temporal | [Mermaid](fuentes/conversion-administrativa.mmd) | [Abrir SVG](conversion-administrativa.svg) |

El diagrama de login describe la implementación existente y señala las brechas de HU-010/HU-015; su inclusión cumple el apoyo documental T-004 de Sprint 1 y no atribuye esas implementaciones a Valeria. Los diagramas de conversión de referidos a puntos y canjes dependen de sprints posteriores. La conversión administrativa de una cuenta a socio es un proceso diferente y está identificada como tal.

Los SVG se generan con Mermaid CLI; para regenerarlos, utilizar mmdc con cada fuente .mmd y salida .svg. El renderizador necesita un navegador compatible para trabajar sin interfaz. No se necesita cambiar dependencias de la aplicación.
