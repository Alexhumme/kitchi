# Auditoría de commits y secretos

Evidencia de P34 · Estado: **pendiente** · Fecha: — · Commit auditado: —

## Commits por integrante

```bash
git shortlog -sne --all
```

| Integrante | Commits | ¿≥ 5? | Observaciones |
| --- | ---: | --- | --- |
| — | — | — | — |
| — | — | — | — |
| — | — | — | — |
| — | — | — | — |

## Archivos sensibles versionados

```bash
git ls-files | Select-String -Pattern "\.env$|__pycache__|\.pyc$|\.sqlite3?$"
```

Resultado: —

## Búsqueda de secretos

```bash
git grep -n -I -E "API_KEY|SECRET_KEY|PASSWORD|TOKEN" -- ":!*.example" ":!docs/**"
```

Resultado: —

## Revisión del historial

- [ ] No hay `.env` real en el historial.
- [ ] No hay `__pycache__`, `.pyc` ni bases locales.
- [ ] No hay tokens, contraseñas ni claves.
- [ ] No hay fotografías privadas ni datos personales reales.
- [ ] Los mensajes de commit son descriptivos.
- [ ] El repositorio es público.

## Resultado

- Aprobado / con incidencias: —
- Acciones correctivas: —
