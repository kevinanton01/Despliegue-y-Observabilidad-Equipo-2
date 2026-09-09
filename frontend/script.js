async function cargarUsuario() {
    const mensaje = document.getElementById("mensaje");

    try {
        const respuesta = await fetch("/api/usuarios/1");

        if (!respuesta.ok) {
            throw new Error("No se pudo obtener el usuario");
        }

        const usuario = await respuesta.json();

        mensaje.textContent = `¡Bienvenido, ${usuario.nombre}!`;

    } catch (error) {
        console.error(error);
        mensaje.textContent = "Error al cargar el usuario";
    }
}

cargarUsuario();