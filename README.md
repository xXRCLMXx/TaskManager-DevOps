# TaskManager-DevOps

Sistema web para la gestión de tareas.

Proyecto remedial: **Implementación de las fases de DevOps utilizando GitHub**.
La empresa ficticia *TechSolutions* registraba sus tareas en hojas de cálculo; TaskManager
centraliza el registro, la asignación de prioridad y el seguimiento del estado de cada tarea.

[![Integracion Continua](https://github.com/xXRCLMXx/TaskManager-DevOps/actions/workflows/ci.yml/badge.svg)](https://github.com/xXRCLMXx/TaskManager-DevOps/actions/workflows/ci.yml)

## Funcionalidades

| Código | Funcionalidad | Cómo se usa |
|---|---|---|
| RF01 | Registrar tareas | Formulario "Nueva tarea" → *Guardar tarea* |
| RF02 | Consultar tareas | Tabla "Tareas registradas" |
| RF03 | Editar tareas | Botón *Editar* → se carga en el formulario → *Guardar* |
| RF04 | Eliminar tareas | Botón *Eliminar* (pide confirmación) |
| RF05 | Cambiar estado | Selector de estado en la tabla: Pendiente / En proceso / Terminada |
| RF06 | Asignar prioridad | Selector de prioridad: Alta / Media / Baja |

## Tecnologías

- **Frontend:** HTML, CSS y JavaScript (fetch API)
- **Backend:** Python 3.12 + Flask
- **Base de datos:** SQLite
- **Pruebas:** Pytest
- **CI/CD:** GitHub Actions
- **Despliegue:** Render (gunicorn)

## Estructura

```
TaskManager-DevOps/
├── app.py                  # Backend Flask + API REST
├── requirements.txt        # Dependencias
├── render.yaml             # Configuración de despliegue en Render
├── pytest.ini              # Configuración de pytest
├── templates/index.html    # Página principal
├── static/css/style.css    # Estilos
├── static/js/app.js        # Lógica del frontend
├── tests/test_app.py       # Pruebas unitarias
├── docs/                   # Documentación de las fases DevOps
└── .github/workflows/
    ├── ci.yml              # Integración continua (pruebas)
    ├── cd.yml              # Entrega continua (artefacto al publicar release)
    └── monitoreo.yml       # Health check programado
```

## Ejecutar en local

```bash
python -m venv .venv
# Windows:  .venv\Scripts\activate      Linux/Mac:  source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Abrir <http://localhost:5000>.

## Ejecutar las pruebas

```bash
pytest -v
```

## API REST

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/api/tareas` | Lista todas las tareas |
| GET | `/api/tareas/<id>` | Consulta una tarea |
| POST | `/api/tareas` | Registra una tarea (`nombre` obligatorio) |
| PUT | `/api/tareas/<id>` | Edita una tarea |
| PATCH | `/api/tareas/<id>/estado` | Cambia el estado |
| DELETE | `/api/tareas/<id>` | Elimina una tarea |
| GET | `/health` | Estado de la app y la base de datos (monitoreo) |

## Despliegue

- Plataforma: **Render** — comando de instalación `pip install -r requirements.txt`,
  comando de inicio `gunicorn app:app`.
- URL pública: *(pendiente de despliegue)*

## Documentación de las fases DevOps

- [Fase 1 – Planificación](docs/01-planificacion.md)
- [Fase 4 – Matriz de pruebas](docs/04-pruebas.md)
- [Fase 7 – Operación y monitoreo](docs/07-monitoreo.md)
- [Resultados, conclusiones y preguntas de análisis](docs/resultados-y-conclusiones.md)

## Equipo

| Rol | Integrante |
|---|---|
| Product Owner + Ingeniero DevOps / QA | Roberto Carlos Lancho Mastranzo |
| Desarrollador (backend e interfaz) | Eduardo Dominguez Mendez |
