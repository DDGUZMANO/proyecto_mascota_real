async function cargarCompatibles() {
    console.log("¡Función cargarCompatibles() ejecutándose!");
    // Datos del cuidador (esto simularía la entrada del usuario)
    const datosCuidador = {
        ubicacion: "Sevilla", // Ejemplo
        experiencia: 3,      // Ejemplo
        acepta_perro: true,  // Ejemplo
        acepta_gato: false   // Ejemplo
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

        console.log("Respuesta del servidor:", response); // Añade esto

        if (!response.ok) {
            console.error(`Error al llamar a /compatibilidad: ${response.status}`);
            return;
        }

        const data = await response.json();

        console.log("Datos recibidos del servidor:", data); // Añade esto

        let html = '';
        data.forEach(mascota => {
            html += `<p>Mascota compatible: ${mascota.nombre}, Compatibilidad: ${mascota.compatibilidad} puntos</p>`;
            // Puedes añadir más información de la mascota si lo deseas
        });

        document.getElementById('resultados').innerHTML = html;

    } catch (error) {
        console.error("Error al cargar compatibles:", error);
    }
}

cargarCompatibles();