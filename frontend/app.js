async function cargarCompatibles() {
    console.log("¡Función cargarCompatibles() ejecutándose!");
    // Datos del cuidador (esto simularía la entrada del usuario)
    const datosCuidador = {
        ubicacion: document.getElementById('ubicacion').value,
        experiencia: parseInt(document.getElementById('experiencia').value),
        acepta_perro: document.getElementById('acepta_perro').checked,
        acepta_gato: document.getElementById('acepta_gato').checked
        // ... otros datos del cuidador que tu backend espera
    };
    console.log("Datos del cuidador a enviar:", datosCuidador);

    try {
        const response = await fetch('http://localhost:5000/compatibilidad', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(datosCuidador)
        });

        console.log("Respuesta del servidor (cargarCompatibles):", response); // Añade esto

        if (!response.ok) {
            console.error(`Error al llamar a /compatibilidad: ${response.status}`);
            return;
        }

        const data = await response.json();

        console.log("Datos recibidos del servidor (cargarCompatibles):", data); // Añade esto

        let html = '';
        data.forEach(mascota => {
            html += `<p>Mascota compatible: ${mascota.nombre}, Compatibilidad: ${mascota.compatibilidad} puntos</p>`;
            // Puedes añadir más información de la mascota si lo deseas
        });

        document.getElementById('resultados_mascotas').innerHTML = html; // Cambiado al ID correcto

    } catch (error) {
        console.error("Error al cargar compatibles:", error);
    }
}

async function cargarCuidadoresCompatibles() {
    console.log("¡Función cargarCuidadoresCompatibles() ejecutándose!");
    const tipoMascota = document.getElementById('tipo_mascota').value;
    const ubicacionMascota = document.getElementById('ubicacion_mascota').value;
    const necesidadesEspecialesMascota = document.getElementById('necesidades_especiales_mascota').checked;

    const datosMascota = {
        tipo: tipoMascota,
        ubicacion: ubicacionMascota,
        necesidades_especiales: necesidadesEspecialesMascota
        // ... otros datos de la mascota según tu formulario
    };
    console.log("Datos de la mascota a enviar:", datosMascota);

    try {
        const response = await fetch('http://localhost:5000/compatibilidad_mascota', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(datosMascota)
        });

        console.log("Respuesta del servidor (cargarCuidadoresCompatibles):", response); // Añade esto

        if (!response.ok) {
            console.error(`Error al llamar a /compatibilidad_mascota: ${response.status}`);
            return;
        }

        const data = await response.json();
        console.log("Datos recibidos del servidor (cargarCuidadoresCompatibles):", data); // Añade esto
        mostrarResultadosCuidadores(data);

    } catch (error) {
        console.error("Error al cargar cuidadores compatibles:", error);
    }
}

function mostrarResultadosCuidadores(cuidadoresCompatibles) {
    let html = '';
    cuidadoresCompatibles.forEach(cuidador => {
        html += `<p>Cuidador compatible: ${cuidador.nombre}, Compatibilidad: ${cuidador.compatibilidad} puntos</p>`;
        // Puedes añadir más información del cuidador si lo deseas
    });
    document.getElementById('resultados_cuidadores').innerHTML = html;
}


