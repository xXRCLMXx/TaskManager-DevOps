# Fase 7 – Operación y monitoreo (Operate & Monitor)

Aplicación publicada: <https://taskmanager-devops-peiz.onrender.com>

## 1. Cómo monitoreamos la aplicación

| Qué se revisa | Herramienta |
|---|---|
| Disponibilidad | Endpoint `/health` + workflow `monitoreo.yml` (cada 6 h y manual) |
| Tiempo de respuesta | Campo `tiempo_respuesta_ms` de `/health`, tiempo total de `curl` en el workflow y los logs (`GET /api/tareas -> 200 (0.9 ms)`) |
| Errores | Logs de Render (pestaña *Logs*) y fallos del workflow *Monitoreo* |
| Almacenamiento | `total_tareas` en `/health` y prueba de registrar/consultar en la URL pública |
| Funcionalidades principales | Prueba de registrar, editar, cambiar estado y eliminar sobre la URL pública |
| Despliegue | Historial de *Deploys* en Render (disparador *Auto-Deploy* al integrar en `main`) |

## 2. Registro de monitoreo

| Fecha y hora | Disponible | Código HTTP | Tiempo de respuesta | Tareas | Observaciones |
|---|---|---|---|---|---|
| 2026-11-25 11:55 | Sí | 200 | 0.87 ms (servidor) | 0 | Primer despliegue (PR #28), *First Deploy* en 37 s |
| 2026-11-25 11:55 | Sí | 200 | — | — | Prueba funcional en producción: validación sin nombre (400), registrar (201), editar, cambiar estado, eliminar ✅ |
| 2026-11-25 11:56 | Sí | 200 | 0.28 s total / 0.35 ms servidor | 3 | Workflow *Monitoreo* ejecutado a mano ([run](https://github.com/xXRCLMXx/TaskManager-DevOps/actions/runs/45669907536)) |
| 2026-11-25 11:57 | Sí | 200 | 0.27 s total / 0.32 ms servidor | 3 | Después del *Auto-Deploy* del PR #29 (10 s); los datos se conservaron |

*(Agregar filas con las siguientes ejecuciones automáticas del workflow Monitoreo: Actions → Monitoreo.)*

## 3. Incidencias (GitHub Issues)

| Issue | Título | Fecha de detección | Funcionalidad afectada | Evidencia | Responsable | Solución aplicada |
|---|---|---|---|---|---|---|
| [#30](https://github.com/xXRCLMXx/TaskManager-DevOps/issues/30) | La URL esperada del servicio pertenece a otra aplicación | 2026-11-25 | Disponibilidad / monitoreo | `taskmanager-devops.onrender.com/health` respondía sin los campos de TaskManager | Roberto Carlos Lancho Mastranzo | Secret `APP_URL` con la URL real (`-peiz`), README actualizado |
| [#31](https://github.com/xXRCLMXx/TaskManager-DevOps/issues/31) | La primera petición tras inactividad puede tardar 50 s o más | 2026-11-25 | Tiempo de respuesta | Aviso del dashboard de Render (plan Free) | Roberto Carlos Lancho Mastranzo | `--max-time 90` en el health check; propuesta: plan de pago o ping periódico |

Riesgo identificado: en el plan gratuito el disco no es permanente, así que el archivo SQLite podría perderse si Render reinicia la instancia → mejora #32.

## 4. Propuestas de mejora (v2.0.0)

| Issue | Mejora |
|---|---|
| [#32](https://github.com/xXRCLMXx/TaskManager-DevOps/issues/32) | Base de datos persistente con PostgreSQL |
| [#33](https://github.com/xXRCLMXx/TaskManager-DevOps/issues/33) | Filtros y búsqueda de tareas |
| [#34](https://github.com/xXRCLMXx/TaskManager-DevOps/issues/34) | Autenticación de usuarios |
| [#35](https://github.com/xXRCLMXx/TaskManager-DevOps/issues/35) | Notificaciones de fecha límite |
| [#36](https://github.com/xXRCLMXx/TaskManager-DevOps/issues/36) | Reportes de productividad |

## 5. Planeación de la nueva versión (v2.0.0)

| Orden | Issue | Mejora | Prioridad | Estimación (h) | Responsable |
|---|---|---|---|---|---|
| 1 | #32 | Migrar a PostgreSQL | Crítica | 4 | Eduardo Dominguez Mendez |
| 2 | #33 | Filtros y búsqueda | Alta | 3 | Eduardo Dominguez Mendez |
| 3 | #34 | Login de usuarios | Alta | 6 | Eduardo Dominguez Mendez |
| 4 | #35 | Notificaciones | Media | 4 | Roberto Carlos Lancho Mastranzo |
| 5 | #36 | Reportes de productividad | Baja | 4 | Roberto Carlos Lancho Mastranzo |

Mejoras al proceso para v2: proteger la rama `main` (PR aprobado + CI en verde obligatorios) y agregar análisis de estilo y cobertura al pipeline.
