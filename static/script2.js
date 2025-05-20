// Rellenar las opciones del selector de tiempo
const tiempoSelect = document.getElementById('tiempo');
for (let i = 30; i <= 150; i += 10) {
  const option = document.createElement('option');
  option.value = i;
  option.textContent = i;
  tiempoSelect.appendChild(option);
}

async function activarEstado() {
  const codigo = document.getElementById('codigo').value.trim();
  const tiempo = parseInt(document.getElementById('tiempo').value);
  const mensajeDiv = document.getElementById('mensaje');

  if (!codigo) {
    mensajeDiv.textContent = "Por favor ingresa un código.";
    mensajeDiv.style.color = "red";
    return;
  }

  try {
    const res = await fetch('/activar', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ codigo, tiempo })
    });

    const data = await res.json();
    console.log(data.expiracion);

    if (res.ok) {
      // Extraemos la hora de expiración y la mostramos en hora local
      if (data.expiracion) {
        const fechaExpiracion = new Date(data.expiracion); // Convertir la fecha ISO a objeto Date
        const horaLocal = fechaExpiracion.toLocaleTimeString(); // Convertir a hora local

        mensajeDiv.textContent = `Estado activado para ${codigo} hasta ${horaLocal}`;
      } else {
        mensajeDiv.textContent = data.mensaje;
      }
      mensajeDiv.style.color = "green";
    } else {
      mensajeDiv.textContent = data.error || "Error desconocido.";
      mensajeDiv.style.color = "red";
    }

  } catch (err) {
    console.error(err);
    mensajeDiv.textContent = "No se pudo conectar al servidor.";
    mensajeDiv.style.color = "red";
  }
}
