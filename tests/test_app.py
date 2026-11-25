"""
Pruebas unitarias de TaskManager (Fase 3 - Integración continua).

Cada prueba usa una base de datos SQLite temporal (tmp_path), así
las pruebas no tocan la base real y siempre empiezan "limpias".
"""

import pytest

from app import create_app


@pytest.fixture
def client(tmp_path):
    """Crea una app de prueba con su propia base de datos temporal."""
    app = create_app({"TESTING": True, "DATABASE": str(tmp_path / "test.db")})
    return app.test_client()


def crear(client, **datos):
    """Ayudante: registra una tarea y regresa la respuesta."""
    base = {"nombre": "Tarea de prueba", "descripcion": "Desc", "prioridad": "Media"}
    base.update(datos)
    return client.post("/api/tareas", json=base)


# Ejemplo que viene en el documento de la actividad
def test_registro_tarea():
    tarea = {"nombre": "Realizar actividad DevOps", "estado": "Pendiente"}
    assert tarea["nombre"] == "Realizar actividad DevOps"
    assert tarea["estado"] == "Pendiente"


# ---------------- Pruebas contra las funciones reales ----------------

def test_pagina_principal_carga(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"TaskManager" in resp.data


# RF01 - Registrar tareas (CP01)
def test_registrar_tarea(client):
    resp = crear(client, nombre="Elaborar documentación", prioridad="Alta")
    assert resp.status_code == 201
    datos = resp.get_json()
    assert datos["mensaje"] == "Tarea registrada correctamente."
    assert datos["tarea"]["nombre"] == "Elaborar documentación"
    assert datos["tarea"]["estado"] == "Pendiente"  # estado por defecto


# CP02 - Registrar tarea sin nombre -> validación
def test_registrar_tarea_sin_nombre(client):
    resp = crear(client, nombre="   ")
    assert resp.status_code == 400
    assert "obligatorio" in resp.get_json()["error"]


def test_registrar_tarea_sin_descripcion(client):
    resp = client.post("/api/tareas", json={"nombre": "Sin descripción"})
    assert resp.status_code == 201
    assert resp.get_json()["tarea"]["descripcion"] == ""


def test_registrar_sin_json(client):
    resp = client.post("/api/tareas", data="esto no es json")
    assert resp.status_code == 400


# RF02 - Consultar tareas (CP03)
def test_consultar_tareas(client):
    crear(client, nombre="Uno")
    crear(client, nombre="Dos")
    resp = client.get("/api/tareas")
    assert resp.status_code == 200
    nombres = [t["nombre"] for t in resp.get_json()]
    assert set(nombres) == {"Uno", "Dos"}


def test_consultar_tarea_inexistente(client):
    assert client.get("/api/tareas/999").status_code == 404


# RF03 - Editar tareas (CP04)
def test_editar_tarea(client):
    tarea_id = crear(client).get_json()["tarea"]["id"]
    resp = client.put(
        f"/api/tareas/{tarea_id}",
        json={"nombre": "Nombre editado", "descripcion": "Nueva",
              "prioridad": "Baja", "estado": "En proceso"},
    )
    assert resp.status_code == 200
    tarea = resp.get_json()["tarea"]
    assert tarea["nombre"] == "Nombre editado"
    assert tarea["prioridad"] == "Baja"
    assert tarea["estado"] == "En proceso"


def test_editar_tarea_inexistente(client):
    resp = client.put("/api/tareas/999", json={"nombre": "X"})
    assert resp.status_code == 404


# RF04 - Eliminar tareas (CP05)
def test_eliminar_tarea(client):
    tarea_id = crear(client).get_json()["tarea"]["id"]
    resp = client.delete(f"/api/tareas/{tarea_id}")
    assert resp.status_code == 200
    assert client.get(f"/api/tareas/{tarea_id}").status_code == 404
    assert client.get("/api/tareas").get_json() == []


def test_eliminar_tarea_inexistente(client):
    assert client.delete("/api/tareas/999").status_code == 404


# RF05 - Cambiar estado (CP06)
@pytest.mark.parametrize("estado", ["Pendiente", "En proceso", "Terminada"])
def test_cambiar_estado(client, estado):
    tarea_id = crear(client).get_json()["tarea"]["id"]
    resp = client.patch(f"/api/tareas/{tarea_id}/estado", json={"estado": estado})
    assert resp.status_code == 200
    assert client.get(f"/api/tareas/{tarea_id}").get_json()["estado"] == estado


def test_cambiar_estado_invalido(client):
    tarea_id = crear(client).get_json()["tarea"]["id"]
    resp = client.patch(f"/api/tareas/{tarea_id}/estado", json={"estado": "Cancelada"})
    assert resp.status_code == 400


# RF06 - Asignar prioridad (CP07)
@pytest.mark.parametrize("prioridad", ["Alta", "Media", "Baja"])
def test_asignar_prioridad(client, prioridad):
    resp = crear(client, prioridad=prioridad)
    assert resp.get_json()["tarea"]["prioridad"] == prioridad


def test_prioridad_invalida(client):
    resp = crear(client, prioridad="Urgentísima")
    assert resp.status_code == 400


# Fase 7 - Monitoreo
def test_health(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    datos = resp.get_json()
    assert datos["status"] == "ok"
    assert datos["database"] == "ok"
