# 13 · Cumplimiento académico y rúbrica — Kitchi Studio

Alineación con el proyecto final de Programación Avanzada A1 · Versión 1.0 · 28 de octubre de 2026

> **Fuente vigente:** [`Proyecto-final-Programacion-Avanzada-A1-20262.pdf`](Proyecto-final-Programacion-Avanzada-A1-20262.pdf). Este documento traduce la rúbrica a requisitos verificables y evidencia esperada; no sustituye al PDF del profesor ni las instrucciones del aula.

## 1. Datos de la entrega

| Aspecto | Requisito del curso | Situación del proyecto |
| --- | --- | --- |
| Fecha límite | Miércoles 25 de noviembre de 2026, 12:00 m. (hora Colombia) | Plan de 4 semanas; entrega interna el 24 de noviembre |
| Modalidad | Repositorio Git + sustentación presencial | Repositorio en GitHub; guion en [`11_DEMO_SCRIPT.md`](11_DEMO_SCRIPT.md) |
| Duración de la defensa | 10 minutos por grupo: demo en vivo + preguntas individuales | Guion de 6–7 min + 3–4 min de preguntas |
| Integrantes | De 2 a 4 personas | 4: 3 desarrollo + 1 diseño |
| Interfaz | No se acepta solo consola | Flet Web móvil + API REST |
| Base de datos | SQLite o PostgreSQL son ejemplos; no hay motor obligatorio | MySQL 8 mediante Django ORM |
| Documentación de API | Swagger/OpenAPI recomendado | `/api/schema/` y `/api/docs/` con drf-spectacular |
| README | Nombre, problema, instalación/ejecución, uso de IA y nombres | [`README.md`](../README.md) (nombres pendientes) |
| Repositorio | Público, organizado, dependencias y `.gitignore` correctos | Remoto configurado; falta verificar visibilidad y auditoría final |
| Commits | Mínimo 5 por integrante, descriptivos | Política definida; pendiente de acumularlos |
| IA | Permitida; cada integrante debe entender el código | Ver sección 6 y [`07_AI_INTEGRATION.md`](07_AI_INTEGRATION.md) |

## 2. Requisitos académicos verificables

| ID | Requisito | Cómo se cumple | Evidencia | Responsable | Estado |
| --- | --- | --- | --- | --- | --- |
| AR-01 | Aplicación real, no solo consola | Flet Web + API REST | Demo y capturas | A | Diseño |
| AR-02 | Interfaz o punto de acceso real | Editor web móvil, hub, login | URL local y capturas | A | Diseño |
| AR-03 | Backend con endpoints y persistencia | Django REST Framework + MySQL | Swagger y pruebas | B | Diseño |
| AR-04 | Base de datos | Modelos y migraciones Django | `docs/reports/clean-install.md` | B | Diseño |
| AR-05 | Al menos 3 funcionalidades completas | Editor + stickers, autenticación + hub, IA | Escenario de aceptación | A/B/C | Pendiente |
| AR-06 | Datos que persisten | Cuentas, gatos, publicaciones, paquetes | Prueba de integración | B | Pendiente |
| AR-07 | Manejo de errores visible | Códigos y mensajes en UI/API | Pruebas de error | A/B | Pendiente |
| AR-08 | Documentación automática de API | drf-spectacular (`/api/docs/`) | Captura y prueba | B | Pendiente |
| AR-09 | README completo | Secciones obligatorias | Revisión con checklist | A | En progreso |
| AR-10 | Sección “Uso de IA” en README | Herramientas y partes del proyecto | README | Todo el equipo | En progreso |
| AR-11 | Nombres de todos los integrantes | Tabla en README | README | Todo el equipo | Pendiente |
| AR-12 | Repositorio público y organizado | GitHub + estructura modular | Enlace y revisión | Integración | Pendiente |
| AR-13 | Mínimo 5 commits por integrante | Ramas y commits pequeños | `git shortlog -sne` | Todo el equipo | Pendiente |
| AR-14 | `requirements.txt` o `pyproject.toml` | Dependencias fijadas | Archivos versionados | B/A | Pendiente |
| AR-15 | `.gitignore` correcto | Sin `.env`, `__pycache__`, temporales | Revisión de Git | Integración | Cumplido |
| AR-16 | Sin secretos en el repositorio | `.env` + python-dotenv | Auditoría de secretos | Integración | Cumplido (inicial) |
| AR-17 | Sustentación de 10 minutos | Guion cronometrado | Ensayo registrado | Todo el equipo | Pendiente |
| AR-18 | Defensa individual | Guía viva + revisión cruzada | Preguntas de ensayo | Todo el equipo | Pendiente |
| AR-19 | Entrega antes del plazo | Congelación el 24 de noviembre | Etiqueta y envío | Integración | Pendiente |
| AR-20 | Documentación actualizada | Docs 00–13 + reportes | Revisión final | Todo el equipo | En progreso |

## 3. Rúbrica y evidencia del proyecto

| Criterio | Peso | Qué evalúa | Evidencia que debe poder mostrar Kitchi Studio |
| --- | --- | --- | --- |
| 1. Utilidad real y alcance | 1.0 / 20 % | Usuario claro, problema delimitado, alcance ambicioso pero alcanzado | Problema de personalización de stickers, flujo completo y demo de un caso real |
| 2. Funcionalidad y ejecución | 1.5 / 30 % | App sin errores, casos prometidos, demo fluida, persistencia, errores visibles, 3+ funcionalidades | Editor, paquete de 6 PNG, cuentas y hub; IA y benchmark como diferenciadores |
| 3. Calidad técnica del código | 1.0 / 20 % | Módulos/apps separadas, framework bien usado, variables descriptivas, sin código muerto, `.env` | Estructura de [`03_ARCHITECTURE.md`](03_ARCHITECTURE.md), revisión cruzada y pruebas |
| 4. Sustentación individual | 1.0 / 20 % | Cada integrante explica su parte y el proyecto, navega el código y responde preguntas | Guía viva, ensayos por integrante y reparto explícito de módulos |
| 5. Repositorio y documentación | 0.5 / 10 % | Repo público, commits de todos, README completo, dependencias y `.gitignore` | Checklist de sección 5 y auditoría final |

> La nota del criterio 4 es individual. Si un integrante no comprende el código, su nota puede ser 0.0 aunque el resto del proyecto sea excelente.

## 4. Funcionalidades completas mínimas

Para el criterio 2, “completa” significa que el flujo se puede ejecutar de principio a fin, con persistencia y errores visibles:

1. **Editor de personajes:** crear un gato, cambiar las seis categorías, guardarlo y recuperarlo.
2. **Generación y descarga:** solicitar el paquete, ver el progreso y descargar seis PNG transparentes.
3. **Cuenta y comunidad:** registrarse, iniciar sesión, publicar un gato, verlo desde otra sesión y copiarlo sin alterar el original.

La **IA** es un cuarto flujo deseable y un diferenciador. Si falla, se documenta la contingencia y las tres funcionalidades anteriores siguen cumpliendo la rúbrica. La demostración de concurrencia, multiprocesamiento y paralelismo es un **diferenciador de calidad técnica**, no un requisito explícito del PDF. Ninguno de los diferenciadores debe poner en riesgo las tres funcionalidades mínimas.

## 5. Checklist de README y repositorio

### README

- [x] Nombre del proyecto.
- [x] Descripción del problema que resuelve.
- [x] Funcionalidades principales.
- [x] Stack y arquitectura en resumen.
- [ ] Instrucciones de instalación y ejecución verificadas desde un clon limpio.
- [x] Sección “Uso de IA” (se actualizará durante el desarrollo).
- [ ] Nombres de todos los integrantes.
- [x] Enlace al repositorio y a la documentación.
- [ ] Capturas o evidencias de la demo (cuando existan).

### Repositorio

- [ ] Repositorio público y enlace enviado al docente antes del plazo.
- [ ] `requirements.txt` o `pyproject.toml` con versiones fijadas.
- [x] `.gitignore` sin `.env`, `__pycache__`, bases locales ni temporales.
- [ ] Mínimo 5 commits descriptivos por integrante.
- [ ] Ningún secreto, token, contraseña ni fotografía privada en el historial.
- [ ] Estructura modular y documentación actualizada.

### Auditoría rápida

```bash
git shortlog -sne --all
git log --oneline --all
git ls-files | Select-String -Pattern "\.env$|__pycache__|\.pyc$"
git grep -n -I -E "API_KEY|SECRET_KEY|PASSWORD|TOKEN" -- ":!*.example" ":!docs/**"
```

> Ejecutar la auditoría en PowerShell o Git Bash según el entorno. No imprimir valores reales de secretos en la salida compartida.

## 6. Uso de IA

- El uso de asistentes de IA está permitido, pero **no sustituye la comprensión**: cada integrante debe poder explicar y modificar cualquier parte del código durante la sustentación.
- El README debe indicar qué herramientas se usaron y en qué partes. Se actualiza a medida que avanza el desarrollo.
- La IA usada **dentro del producto** (transformación de fotografías) es distinta de la IA usada **para desarrollar**. Ambas deben declararse por separado.
- Las claves de proveedores viven en `.env`, nunca en el frontend, en capturas ni en el repositorio.
- No se presenta una selección aleatoria o una imagen de ejemplo como si fuera una inferencia real.

## 7. Sustentación de 10 minutos

| Bloque | Tiempo | Responsable sugerido | Contenido |
| --- | --- | --- | --- |
| Problema y producto | 1 min | Integrante A | Usuario, problema y flujo completo |
| Editor y stickers | 2 min | Integrante A/C | Seis categorías, capas, PNG transparentes |
| Backend y datos | 1.5 min | Integrante B | API, MySQL, permisos, Swagger |
| IA | 1.5 min | Integrante C | Inferencia real, privacidad, contingencia |
| Comunidad y demo | 2 min | Integrante A/B | Publicar, explorar y copiar |
| Calidad y evidencias | 1 min | Integrante C | Pruebas, benchmark, decisiones |
| Preguntas individuales | 3–4 min | Todo el equipo | Cada integrante responde sobre su módulo y sobre el flujo general |

Reglas:

- Ensayar al menos dos veces con cronómetro y con una persona distinta del ponente habitual.
- Tener respaldo de capturas y resultados, pero distinguir siempre la demo real de la simulación.
- Cada integrante debe poder abrir el repositorio y explicar cualquier módulo, no solo el suyo.

## 8. Riesgos académicos y mitigaciones

| Riesgo | Impacto | Mitigación |
| --- | --- | --- |
| Calendario de 4 semanas | Alto | Congelar P1, priorizar las tres funcionalidades mínimas y ensayar desde la semana 3 |
| MySQL difícil de instalar en un clon limpio | Medio | Documentar requisitos y validar instalación en P29; si bloquea la demo, registrar ADR de contingencia |
| IA sin API gratuita estable | Medio | Mantener el flujo manual y la contingencia documentada |
| Flet no se comporta como se espera en web móvil | Medio | Validarlo en la primera semana; si falla, registrar ADR antes de cambiar de interfaz |
| Un integrante no puede explicar su módulo | Alto | Guía viva, revisión cruzada y ensayos individuales |
| Commits concentrados en una persona | Alto | Repartir tareas y commits desde la primera semana; incluir a la diseñadora |
| Nombres o enlace del repositorio incompletos | Medio | Completar el README antes de la entrega interna |

## 9. Estado actual

- [x] Rúbrica del PDF transcrita y analizada ([`reports/rubric.md`](reports/rubric.md)).
- [x] Plan de 4 semanas alineado al plazo.
- [x] Guía viva creada como esqueleto.
- [x] Reglas académicas incorporadas a [`AGENTS.md`](../AGENTS.md).
- [ ] Nombres de los integrantes en el README.
- [ ] Repositorio verificado como público.
- [x] `backend/requirements.txt` y `frontend/pyproject.toml` con versiones verificadas.
- [ ] Instalación desde clon limpio.
- [x] Swagger/OpenAPI funcionando (`/api/docs/` y `/api/schema/`, verificado el 4 de noviembre).
- [ ] Tres funcionalidades completas demostrables (editor, cuentas y persistencia ya funcionan; faltan stickers, hub e IA).
- [ ] 5 commits por integrante.
- [ ] Ensayo de la defensa de 10 minutos.
