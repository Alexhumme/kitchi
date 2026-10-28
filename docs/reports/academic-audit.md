# Auditoría académica de entrega — plantilla

Evidencia de P40 · Completar antes de la entrega del 25 de noviembre de 2026 · Estado: **pendiente**

> Registrar fecha, commit auditado, integrantes presentes y resultados reales. No marcar una casilla sin evidencia. Ver criterios en [`13_CUMPLIMIENTO_ACADEMICO.md`](../13_CUMPLIMIENTO_ACADEMICO.md).

## 1. Datos de la auditoría

| Campo | Valor |
| --- | --- |
| Fecha | — |
| Commit / etiqueta | — |
| Auditor | — |
| Integrantes | — |

## 2. README

- [ ] Nombre del proyecto.
- [ ] Descripción del problema y usuario.
- [ ] Instrucciones de instalación y ejecución verificadas.
- [ ] Sección “Uso de IA” con herramientas y partes.
- [ ] Nombres de todos los integrantes.
- [ ] Enlace al repositorio y a la documentación.
- [ ] Capturas o evidencias de la demo.

## 3. Repositorio

- [ ] Repositorio público.
- [ ] `requirements.txt` o `pyproject.toml` con versiones fijadas.
- [ ] `.gitignore` sin `.env`, `__pycache__`, bases locales ni temporales.
- [ ] Mínimo 5 commits descriptivos por integrante.
- [ ] Sin secretos, tokens ni fotografías privadas en el historial.
- [ ] Estructura modular y documentación actualizada.

### Comandos de auditoría

```bash
git shortlog -sne --all
git log --oneline --all
git ls-files | Select-String -Pattern "\.env$|__pycache__|\.pyc$"
git grep -n -I -E "API_KEY|SECRET_KEY|PASSWORD|TOKEN" -- ":!*.example" ":!docs/**"
```

Resultado: _pendiente_

## 4. Producto

- [ ] La aplicación arranca desde un clon limpio.
- [ ] Existe una interfaz real, no solo consola.
- [ ] El editor permite modificar las seis categorías.
- [ ] Se generan seis PNG transparentes y se descargan.
- [ ] Registro e inicio de sesión funcionan.
- [ ] Se publica un gato, se encuentra desde otra sesión y se copia.
- [ ] La IA ejecuta una inferencia real o se muestra la contingencia declarada.
- [ ] Los errores se muestran al usuario sin exponer trazas internas.
- [ ] Los datos persisten tras reiniciar la aplicación.
- [ ] Swagger/OpenAPI disponible en `/api/docs/`.

## 5. Sustentación

- [ ] Guion de 10 minutos ensayado y cronometrado.
- [ ] Cada integrante expone al menos un bloque.
- [ ] Cada integrante puede explicar un módulo ajeno.
- [ ] Cada integrante navega el repositorio en vivo.
- [ ] Respaldo de demo y resultados disponible.
- [ ] Se distingue lo real de lo simulado.

## 6. Resultado

| Área | Resultado | Observaciones |
| --- | --- | --- |
| README | — | — |
| Repositorio | — | — |
| Producto | — | — |
| Sustentación | — | — |
| Decisión | — | — |
