# Fase 4 – Pruebas (Test)

## 1. Matriz de casos de prueba

| ID | Prueba | Pasos | Resultado esperado | Resultado obtenido | Estado |
|---|---|---|---|---|---|
| CP01 | Registrar una tarea | Nombre "Elaborar documentación", descripción, prioridad Alta → Guardar | La tarea se guarda correctamente y aparece en el listado | Se guardó y apareció con mensaje "Tarea registrada correctamente." | ✅ Aprobada |
| CP02 | Registrar una tarea sin nombre | Dejar el nombre vacío → Guardar | El sistema muestra una validación | Mensaje "El nombre de la tarea es obligatorio." y no se guarda | ✅ Aprobada |
| CP03 | Consultar tareas | Abrir el sistema con tareas registradas | Se muestra el listado | Se muestran las tareas y el contador total | ✅ Aprobada |
| CP04 | Editar una tarea | Pulsar *Editar*, cambiar nombre → Guardar | Se actualiza la información | Mensaje "Tarea actualizada correctamente." y el listado cambia | ✅ Aprobada |
| CP05 | Eliminar una tarea | Pulsar *Eliminar* → Aceptar | La tarea desaparece del listado | Desaparece y el contador baja | ✅ Aprobada |
| CP06 | Cambiar estado | En la tabla elegir *Terminada* | Se actualiza el estado | El estado queda en *Terminada* al recargar | ✅ Aprobada |
| CP07 | Seleccionar prioridad | Registrar tarea con prioridad Baja | Se guarda la prioridad elegida | Aparece con etiqueta verde "Baja" | ✅ Aprobada |
| CP08 | Registrar tarea sin descripción | Solo nombre → Guardar | Se guarda con descripción vacía | Se guardó sin error | ✅ Aprobada |
| CP09 | Cancelar edición | *Editar* → *Cancelar edición* | El formulario vuelve a "Nueva tarea" sin cambios | Correcto | ✅ Aprobada |

> Las pruebas manuales se ejecutaron en local (`python app.py`) y en la URL pública de Render.
> Adjuntar capturas de cada caso en la carpeta de evidencias.

## 2. Pruebas automatizadas (pytest)

Archivo `tests/test_app.py` – 21 pruebas, todas usan una base de datos temporal.

| Prueba | Requerimiento / Caso |
|---|---|
| `test_registro_tarea` | Ejemplo del documento |
| `test_pagina_principal_carga` | Página principal |
| `test_registrar_tarea` | RF01 / CP01 |
| `test_registrar_tarea_sin_nombre` | CP02 |
| `test_registrar_tarea_sin_descripcion` | CP08 |
| `test_registrar_sin_json` | Validación de entrada |
| `test_consultar_tareas`, `test_consultar_tarea_inexistente` | RF02 / CP03 |
| `test_editar_tarea`, `test_editar_tarea_inexistente` | RF03 / CP04 |
| `test_eliminar_tarea`, `test_eliminar_tarea_inexistente` | RF04 / CP05 |
| `test_cambiar_estado` (×3), `test_cambiar_estado_invalido` | RF05 / CP06 |
| `test_asignar_prioridad` (×3), `test_prioridad_invalida` | RF06 / CP07 |
| `test_health` | Monitoreo |

Resultado local: **21 passed**.

## 3. Errores encontrados (Issues de bug)

| Issue | Título | Funcionalidad | Pasos para reproducir | Obtenido | Esperado | Prioridad | Corrección (rama / PR) | Estado |
|---|---|---|---|---|---|---|---|---|
| [#26](https://github.com/xXRCLMXx/TaskManager-DevOps/issues/26) | Error en CI: pytest no ejecutaba ninguna prueba | Integración continua | Abrir PR #25 con solo `ci.yml` (commit 7a51cde) | Job `pruebas` en rojo: *no tests ran* | La CI ejecuta y aprueba las pruebas | Alta | Commit 876e1e8 en `feature/pruebas-ci` → [PR #25](https://github.com/xXRCLMXx/TaskManager-DevOps/pull/25) | Cerrado ✅ |

Evidencias en GitHub Actions:
- Ejecución fallida: <https://github.com/xXRCLMXx/TaskManager-DevOps/actions/runs/45667008977>
- Nueva ejecución exitosa: <https://github.com/xXRCLMXx/TaskManager-DevOps/actions/runs/45667090646>
