# Fase 1 – Planificación (Plan)

## 1. Roles del equipo (3 integrantes)

El documento recomienda 4 roles; al ser 3 integrantes, un integrante cubre dos roles.

| Rol | Integrante | Responsabilidades |
|---|---|---|
| Product Owner + Desarrollador | Integrante 1 | Requerimientos, prioridades, tablero, historias de usuario; RF01 registro y RF02 consulta |
| Desarrollador backend | Integrante 2 | API Flask, base de datos SQLite, RF03 edición y RF05 estados |
| Desarrollador frontend + DevOps/QA | Integrante 3 | Interfaz, RF04 eliminación, RF06 prioridad, GitHub Actions, pruebas y despliegue |

Todos revisamos Pull Requests de los demás.

## 2. Tablero (GitHub Projects)

Vista **Board** con columnas: **Backlog → To Do → In Progress → Review → Done**.

Campos personalizados del proyecto:

| Propiedad | Tipo de campo | Valores |
|---|---|---|
| Tarea | Título | Nombre de la actividad |
| Responsable | Assignees | Integrante asignado |
| Estado | Status | Backlog, To Do, In Progress, Review, Done |
| Prioridad | Single select | Crítica, Alta, Media, Baja |
| Estimación | Number | Horas estimadas |
| Fase DevOps | Single select | Plan, Code, Build, Test, Release, Deploy, Operate, Monitor |
| Fecha límite | Date | Fecha de entrega |

## 3. Historias de usuario

Registradas como issues con la etiqueta `historia de usuario`: HU-01 a HU-06 = issues #16 a #21.

### HU-01 Registrar tareas (RF01)
**Como** usuario del sistema, **quiero** registrar nuevas tareas **para** organizar mis actividades.

Criterios de aceptación:
- El sistema debe permitir ingresar el nombre de la tarea.
- El sistema debe permitir agregar una descripción.
- El sistema debe permitir seleccionar una prioridad.
- El sistema debe guardar la tarea.
- El sistema debe mostrar un mensaje de confirmación.
- Si el nombre está vacío, el sistema muestra una validación y no guarda.

### HU-02 Consultar tareas (RF02)
**Como** usuario, **quiero** ver todas las tareas registradas **para** saber qué está pendiente y qué está terminado.

Criterios de aceptación:
- Se muestra un listado con nombre, descripción, prioridad y estado.
- Se muestra el total de tareas.
- Si no hay tareas se muestra el mensaje "No hay tareas registradas".
- Las tareas más recientes aparecen primero.

### HU-03 Editar tareas (RF03)
**Como** usuario, **quiero** modificar la información de una tarea **para** corregir errores o actualizar sus datos.

Criterios de aceptación:
- Al pulsar *Editar*, los datos de la tarea se cargan en el formulario.
- Se pueden cambiar nombre, descripción, prioridad y estado.
- Al guardar se muestra "Tarea actualizada correctamente".
- Se puede cancelar la edición sin guardar cambios.
- No se permite dejar el nombre vacío.

### HU-04 Eliminar tareas (RF04)
**Como** usuario, **quiero** eliminar tareas **para** quitar actividades duplicadas o que ya no aplican.

Criterios de aceptación:
- Cada tarea tiene un botón *Eliminar*.
- El sistema pide confirmación antes de eliminar.
- La tarea desaparece del listado.
- Se muestra "Tarea eliminada correctamente".

### HU-05 Cambiar estado de tareas (RF05)
**Como** usuario, **quiero** cambiar el estado de una tarea **para** conocer su progreso.

Criterios de aceptación:
- Debe permitir seleccionar *Pendiente*.
- Debe permitir seleccionar *En proceso*.
- Debe permitir seleccionar *Terminada*.
- El cambio debe reflejarse en el listado de tareas.
- No se aceptan estados distintos a los tres anteriores.

### HU-06 Asignar prioridad (RF06)
**Como** usuario, **quiero** clasificar las tareas por prioridad **para** atender primero las más importantes.

Criterios de aceptación:
- Se puede elegir *Alta*, *Media* o *Baja* (por defecto *Media*).
- La prioridad se muestra con un color distinto en el listado.
- La prioridad se puede cambiar al editar la tarea.
- No se aceptan prioridades distintas a las tres anteriores.

## 4. Issues (actividades)

| # | Issue | Responsable | Prioridad | Estimación (h) | Fase DevOps | Fecha límite |
|---|---|---|---|---|---|---|
| 1 | Crear la estructura inicial del proyecto | Integrante 1 | Crítica | 2 | Plan | 2026-11-18 |
| 2 | Diseñar la interfaz del sistema | Integrante 3 | Alta | 3 | Code | 2026-11-19 |
| 3 | Implementar el registro de tareas (RF01) | Integrante 1 | Crítica | 3 | Code | 2026-11-20 |
| 4 | Implementar la consulta de tareas (RF02) | Integrante 1 | Alta | 2 | Code | 2026-11-20 |
| 5 | Implementar la edición de tareas (RF03) | Integrante 2 | Alta | 3 | Code | 2026-11-21 |
| 6 | Implementar la eliminación de tareas (RF04) | Integrante 3 | Alta | 2 | Code | 2026-11-21 |
| 7 | Implementar el cambio de estado (RF05) | Integrante 2 | Alta | 2 | Code | 2026-11-21 |
| 8 | Implementar la asignación de prioridad (RF06) | Integrante 3 | Media | 1 | Code | 2026-11-21 |
| 9 | Implementar las pruebas unitarias | Integrante 3 | Alta | 3 | Test | 2026-11-22 |
| 10 | Configurar integración continua (ci.yml) | Integrante 3 | Alta | 2 | Build | 2026-11-22 |
| 11 | Ejecutar matriz de pruebas funcionales | Integrante 2 | Media | 2 | Test | 2026-11-23 |
| 12 | Publicar Release v1.0.0 y workflow de entrega | Integrante 1 | Media | 1 | Release | 2026-11-23 |
| 13 | Desplegar la aplicación en Render | Integrante 3 | Alta | 2 | Deploy | 2026-11-24 |
| 14 | Configurar monitoreo y registro de incidencias | Integrante 2 | Media | 2 | Monitor | 2026-11-24 |
| 15 | Documentación, resultados y conclusiones | Integrante 1 | Media | 2 | Operate | 2026-11-25 |
