"""
TaskManager - Sistema web para la gestión de tareas (TechSolutions).

Backend hecho con Flask + SQLite.
Expone:
  - La página principal (templates/index.html).
  - Una API REST en /api/tareas para registrar, consultar, editar,
    eliminar, cambiar estado y asignar prioridad a las tareas.
  - Un endpoint /health para el monitoreo (fase Operate & Monitor).
"""

import logging
import os
import sqlite3
import time

from flask import Flask, g, jsonify, render_template, request

# Valores permitidos (RF05 y RF06)
ESTADOS = ["Pendiente", "En proceso", "Terminada"]
PRIORIDADES = ["Alta", "Media", "Baja"]

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger("taskmanager")


def create_app(test_config=None):
    """Fábrica de la aplicación: crea y configura la app de Flask."""
    app = Flask(__name__)
    app.config["DATABASE"] = os.environ.get("DATABASE", "tasks.db")
    if test_config:
        app.config.update(test_config)

    # ------------------------------------------------------------------
    # Base de datos
    # ------------------------------------------------------------------
    def get_db():
        """Abre (una sola vez por petición) la conexión a SQLite."""
        if "db" not in g:
            g.db = sqlite3.connect(app.config["DATABASE"])
            g.db.row_factory = sqlite3.Row  # filas como diccionarios
        return g.db

    @app.teardown_appcontext
    def close_db(_error=None):
        """Cierra la conexión al terminar cada petición."""
        db = g.pop("db", None)
        if db is not None:
            db.close()

    def init_db():
        """Crea la tabla 'tareas' si no existe."""
        db = get_db()
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS tareas (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre      TEXT NOT NULL,
                descripcion TEXT DEFAULT '',
                prioridad   TEXT NOT NULL DEFAULT 'Media',
                estado      TEXT NOT NULL DEFAULT 'Pendiente',
                creada_en   TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        db.commit()

    with app.app_context():
        init_db()

    # ------------------------------------------------------------------
    # Validación
    # ------------------------------------------------------------------
    def validar_tarea(datos):
        """Regresa (datos_limpios, error). Si hay error, datos es None."""
        if not isinstance(datos, dict):
            return None, "Se esperaba un JSON con los datos de la tarea."

        nombre = (datos.get("nombre") or "").strip()
        if not nombre:
            return None, "El nombre de la tarea es obligatorio."
        if len(nombre) > 100:
            return None, "El nombre no puede tener más de 100 caracteres."

        descripcion = (datos.get("descripcion") or "").strip()

        prioridad = datos.get("prioridad") or "Media"
        if prioridad not in PRIORIDADES:
            return None, f"Prioridad inválida. Usa: {', '.join(PRIORIDADES)}."

        estado = datos.get("estado") or "Pendiente"
        if estado not in ESTADOS:
            return None, f"Estado inválido. Usa: {', '.join(ESTADOS)}."

        return {
            "nombre": nombre,
            "descripcion": descripcion,
            "prioridad": prioridad,
            "estado": estado,
        }, None

    def buscar_tarea(tarea_id):
        fila = get_db().execute(
            "SELECT * FROM tareas WHERE id = ?", (tarea_id,)
        ).fetchone()
        return dict(fila) if fila else None

    def no_encontrada():
        return jsonify({"error": "Tarea no encontrada."}), 404

    # ------------------------------------------------------------------
    # Monitoreo: se mide el tiempo de respuesta de cada petición
    # ------------------------------------------------------------------
    @app.before_request
    def iniciar_cronometro():
        g.inicio = time.perf_counter()

    @app.after_request
    def registrar_peticion(respuesta):
        ms = (time.perf_counter() - g.get("inicio", time.perf_counter())) * 1000
        logger.info(
            "%s %s -> %s (%.1f ms)",
            request.method, request.path, respuesta.status_code, ms,
        )
        return respuesta

    # ------------------------------------------------------------------
    # Rutas
    # ------------------------------------------------------------------
    @app.route("/")
    def index():
        return render_template(
            "index.html", estados=ESTADOS, prioridades=PRIORIDADES
        )

    # RF02 - Consultar tareas
    @app.route("/api/tareas", methods=["GET"])
    def listar_tareas():
        filas = get_db().execute(
            "SELECT * FROM tareas ORDER BY id DESC"
        ).fetchall()
        return jsonify([dict(f) for f in filas])

    @app.route("/api/tareas/<int:tarea_id>", methods=["GET"])
    def obtener_tarea(tarea_id):
        tarea = buscar_tarea(tarea_id)
        return jsonify(tarea) if tarea else no_encontrada()

    # RF01 - Registrar tareas (y RF06 - asignar prioridad)
    @app.route("/api/tareas", methods=["POST"])
    def crear_tarea():
        datos, error = validar_tarea(request.get_json(silent=True))
        if error:
            return jsonify({"error": error}), 400

        db = get_db()
        cursor = db.execute(
            "INSERT INTO tareas (nombre, descripcion, prioridad, estado) "
            "VALUES (?, ?, ?, ?)",
            (datos["nombre"], datos["descripcion"],
             datos["prioridad"], datos["estado"]),
        )
        db.commit()
        tarea = buscar_tarea(cursor.lastrowid)
        return jsonify(
            {"mensaje": "Tarea registrada correctamente.", "tarea": tarea}
        ), 201

    # RF03 - Editar tareas
    @app.route("/api/tareas/<int:tarea_id>", methods=["PUT"])
    def editar_tarea(tarea_id):
        if not buscar_tarea(tarea_id):
            return no_encontrada()

        datos, error = validar_tarea(request.get_json(silent=True))
        if error:
            return jsonify({"error": error}), 400

        db = get_db()
        db.execute(
            "UPDATE tareas SET nombre = ?, descripcion = ?, prioridad = ?, "
            "estado = ? WHERE id = ?",
            (datos["nombre"], datos["descripcion"], datos["prioridad"],
             datos["estado"], tarea_id),
        )
        db.commit()
        return jsonify(
            {"mensaje": "Tarea actualizada correctamente.",
             "tarea": buscar_tarea(tarea_id)}
        )

    # RF05 - Cambiar estado
    @app.route("/api/tareas/<int:tarea_id>/estado", methods=["PATCH"])
    def cambiar_estado(tarea_id):
        if not buscar_tarea(tarea_id):
            return no_encontrada()

        datos = request.get_json(silent=True) or {}
        estado = datos.get("estado")
        if estado not in ESTADOS:
            return jsonify(
                {"error": f"Estado inválido. Usa: {', '.join(ESTADOS)}."}
            ), 400

        db = get_db()
        db.execute("UPDATE tareas SET estado = ? WHERE id = ?",
                   (estado, tarea_id))
        db.commit()
        return jsonify(
            {"mensaje": "Estado actualizado.", "tarea": buscar_tarea(tarea_id)}
        )

    # RF04 - Eliminar tareas
    @app.route("/api/tareas/<int:tarea_id>", methods=["DELETE"])
    def eliminar_tarea(tarea_id):
        if not buscar_tarea(tarea_id):
            return no_encontrada()

        db = get_db()
        db.execute("DELETE FROM tareas WHERE id = ?", (tarea_id,))
        db.commit()
        return jsonify({"mensaje": "Tarea eliminada correctamente."})

    # Fase 7 - Monitoreo: revisa que la app y la base de datos respondan
    @app.route("/health")
    def health():
        inicio = time.perf_counter()
        try:
            total = get_db().execute("SELECT COUNT(*) FROM tareas").fetchone()[0]
            estado_db = "ok"
        except sqlite3.Error as exc:
            logger.error("Fallo en la base de datos: %s", exc)
            return jsonify({"status": "error", "database": str(exc)}), 500
        ms = round((time.perf_counter() - inicio) * 1000, 2)
        return jsonify(
            {"status": "ok", "database": estado_db,
             "total_tareas": total, "tiempo_respuesta_ms": ms}
        )

    return app


# Objeto que usa gunicorn en producción:  gunicorn app:app
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
