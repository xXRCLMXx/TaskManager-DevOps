// Lógica del frontend de TaskManager.
// Se comunica con la API de Flask usando fetch() y JSON.

const API = "/api/tareas";

const form = document.getElementById("form-tarea");
const campoId = document.getElementById("tarea-id");
const campoNombre = document.getElementById("nombre");
const campoDescripcion = document.getElementById("descripcion");
const campoPrioridad = document.getElementById("prioridad");
const campoEstado = document.getElementById("estado");
const tituloForm = document.getElementById("titulo-form");
const btnCancelar = document.getElementById("btn-cancelar");
const cajaMensaje = document.getElementById("mensaje");
const tbody = document.getElementById("lista-tareas");
const sinTareas = document.getElementById("sin-tareas");
const contador = document.getElementById("contador");

function mostrarMensaje(texto, tipo = "ok") {
    cajaMensaje.textContent = texto;
    cajaMensaje.className = tipo;
    setTimeout(() => { cajaMensaje.textContent = ""; cajaMensaje.className = ""; }, 3500);
}

// Evita que el texto del usuario se interprete como HTML (seguridad XSS)
function escapar(texto) {
    const div = document.createElement("div");
    div.textContent = texto ?? "";
    return div.innerHTML;
}

// RF02 - Consultar tareas
async function cargarTareas() {
    const resp = await fetch(API);
    const tareas = await resp.json();

    tbody.innerHTML = "";
    sinTareas.hidden = tareas.length > 0;
    contador.textContent = `(${tareas.length})`;

    for (const t of tareas) {
        const opciones = ESTADOS.map(e =>
            `<option value="${e}" ${e === t.estado ? "selected" : ""}>${e}</option>`
        ).join("");

        const fila = document.createElement("tr");
        fila.innerHTML = `
            <td>${t.id}</td>
            <td><strong>${escapar(t.nombre)}</strong><br><small>${escapar(t.descripcion)}</small></td>
            <td><span class="prioridad prioridad-${t.prioridad}">${t.prioridad}</span></td>
            <td><select data-id="${t.id}" class="select-estado">${opciones}</select></td>
            <td class="acciones">
                <button class="chico" data-editar="${t.id}">Editar</button>
                <button class="chico peligro" data-eliminar="${t.id}">Eliminar</button>
            </td>`;
        tbody.appendChild(fila);
    }
}

// RF01 (registrar) y RF03 (editar) comparten el mismo formulario
form.addEventListener("submit", async (evento) => {
    evento.preventDefault();

    const tarea = {
        nombre: campoNombre.value.trim(),
        descripcion: campoDescripcion.value.trim(),
        prioridad: campoPrioridad.value,
        estado: campoEstado.value,
    };

    // Validación en el navegador (CP02)
    if (!tarea.nombre) {
        mostrarMensaje("El nombre de la tarea es obligatorio.", "error");
        campoNombre.focus();
        return;
    }

    const id = campoId.value;
    const resp = await fetch(id ? `${API}/${id}` : API, {
        method: id ? "PUT" : "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(tarea),
    });
    const datos = await resp.json();

    if (!resp.ok) {
        mostrarMensaje(datos.error, "error");
        return;
    }
    mostrarMensaje(datos.mensaje);
    limpiarFormulario();
    cargarTareas();
});

function limpiarFormulario() {
    form.reset();
    campoId.value = "";
    campoPrioridad.value = "Media";
    tituloForm.textContent = "Nueva tarea";
    btnCancelar.hidden = true;
}

btnCancelar.addEventListener("click", limpiarFormulario);

// Botones de la tabla (delegación de eventos)
tbody.addEventListener("click", async (evento) => {
    const idEditar = evento.target.dataset.editar;
    const idEliminar = evento.target.dataset.eliminar;

    // RF03 - Editar: carga la tarea en el formulario
    if (idEditar) {
        const resp = await fetch(`${API}/${idEditar}`);
        const t = await resp.json();
        campoId.value = t.id;
        campoNombre.value = t.nombre;
        campoDescripcion.value = t.descripcion;
        campoPrioridad.value = t.prioridad;
        campoEstado.value = t.estado;
        tituloForm.textContent = `Editando tarea #${t.id}`;
        btnCancelar.hidden = false;
        campoNombre.focus();
    }

    // RF04 - Eliminar
    if (idEliminar && confirm("¿Seguro que deseas eliminar esta tarea?")) {
        const resp = await fetch(`${API}/${idEliminar}`, { method: "DELETE" });
        const datos = await resp.json();
        mostrarMensaje(datos.mensaje || datos.error, resp.ok ? "ok" : "error");
        cargarTareas();
    }
});

// RF05 - Cambiar estado directamente desde el listado
tbody.addEventListener("change", async (evento) => {
    if (!evento.target.classList.contains("select-estado")) return;
    const id = evento.target.dataset.id;
    const resp = await fetch(`${API}/${id}/estado`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ estado: evento.target.value }),
    });
    const datos = await resp.json();
    mostrarMensaje(resp.ok ? `Estado cambiado a "${evento.target.value}".` : datos.error,
                   resp.ok ? "ok" : "error");
    cargarTareas();
});

cargarTareas();
