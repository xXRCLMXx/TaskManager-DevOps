# Fase 2 – Desarrollo (Code)

## Flujo de trabajo

1. `git checkout -b feature/<nombre>` – cada funcionalidad en su propia rama.
2. `git add .` → `git commit -m "mensaje"` → `git push origin feature/<nombre>`.
3. Pull Request hacia `main`, con la descripción de los cambios y `Closes #<issue>`.
4. GitHub Actions ejecuta las pruebas (`ci.yml`) en el PR.
5. El otro integrante revisa y aprueba; después se hace *merge* y la tarjeta pasa a **Done**.

## Ramas y Pull Requests

| PR | Rama | Contenido | Issues |
|---|---|---|---|
| [#22](https://github.com/xXRCLMXx/TaskManager-DevOps/pull/22) | `feature/registro-tareas` | Backend Flask + SQLite, registro y consulta, interfaz | #2, #3, #4, #8 |
| [#23](https://github.com/xXRCLMXx/TaskManager-DevOps/pull/23) | `feature/editar-tareas` | Edición (PUT) y cambio de estado (PATCH) | #5, #7 |
| [#24](https://github.com/xXRCLMXx/TaskManager-DevOps/pull/24) | `feature/eliminar-tareas` | Eliminación (DELETE) | #6 |
| [#25](https://github.com/xXRCLMXx/TaskManager-DevOps/pull/25) | `feature/pruebas-ci` | Pruebas unitarias y `ci.yml` (incluye el error #26 detectado por la CI) | #9, #10 |
| [#27](https://github.com/xXRCLMXx/TaskManager-DevOps/pull/27) | `feature/monitoreo-entrega` | `/health`, `cd.yml`, `monitoreo.yml`, `render.yaml`, documentación | #11 |
| [#28](https://github.com/xXRCLMXx/TaskManager-DevOps/pull/28) | `docs/nombres-equipo` | Integrantes y roles | — |
| [#29](https://github.com/xXRCLMXx/TaskManager-DevOps/pull/29) | `docs/url-despliegue` | URL pública de Render | #13 |
| [#37](https://github.com/xXRCLMXx/TaskManager-DevOps/pull/37) | `docs/monitoreo` | Registro de monitoreo, incidencias y mejoras | #14, #15 |
| [#38](https://github.com/xXRCLMXx/TaskManager-DevOps/pull/38) | `docs/fase-desarrollo` | Documentación de la fase de desarrollo (abierto por Roberto, revisado e integrado por Eduardo) | — |
| [#40](https://github.com/xXRCLMXx/TaskManager-DevOps/pull/40) | `feature/pie-de-pagina` | Pie de página con versión e integrantes (abierto por Eduardo, revisado e integrado por Roberto) | #39 |

## Convención de nombres de ramas

- `feature/...` – nueva funcionalidad
- `fix/...` – corrección de un error
- `docs/...` – documentación

## Historial

El historial completo se consulta con:

```bash
git log --oneline --graph
```

o en GitHub: *Insights → Network* y la pestaña *Commits*.
