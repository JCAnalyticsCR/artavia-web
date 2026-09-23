// Chat del hero: el visitante toca su situación y recibe la respuesta.
(function () {
  var replies = [{"t":"Se quedó afuera del carro","d":"Apertura de vehículos sin dañar la cerradura. Llegamos hasta donde esté."},{"t":"Perdió todas las llaves","d":"Hacemos llaves desde cero, sin necesidad de muestra. Con chip incluido."},{"t":"No le sirve el control","d":"Venta y reparación de controles para vehículo."},{"t":"Se le quebró la llave","d":"Extracción de tacos y reparación de la cerradura en el momento."},{"t":"Casa, oficina o caja fuerte","d":"Aperturas, instalación de cerraduras, cambio de combinación y amaestramiento."}];
  var thread = document.getElementById('chat-thread');
  var chips = document.querySelectorAll('#chat-chips .chip');
  chips.forEach(function (chip) {
    chip.addEventListener('click', function () {
      var r = replies[Number(chip.dataset.i)];
      chips.forEach(function (c) { c.setAttribute('aria-pressed', c === chip ? 'true' : 'false'); });
      thread.innerHTML =
        '<div class="bubble bubble--me">' + r.t + '</div>' +
        '<div class="bubble bubble--them">' + r.d + '</div>' +
        '<div class="bubble bubble--them bubble--cta">Si quiere, llámenos al <a href="tel:+50672907799">7290-7799</a> y coordinamos ya.</div>';
    });
  });
})();

// Formulario de contacto: envío por Formspree sin recargar la página.
(function () {
  var form = document.getElementById('form-contacto');
  if (!form) return;
  var status = document.getElementById('form-status');
  var button = form.querySelector('button[type="submit"]');
  var textoOriginal = button.textContent;

  function aviso(texto, tipo) {
    status.textContent = texto;
    status.className = 'form-status form-status--' + tipo;
  }

  form.addEventListener('submit', function (e) {
    e.preventDefault();

    if (!form.checkValidity()) {
      aviso('Complete nombre, teléfono y el mensaje.', 'error');
      var primero = form.querySelector(':invalid');
      if (primero) primero.focus();
      return;
    }
    if (form.action.indexOf('REEMPLAZAR_ID') !== -1) {
      aviso('El formulario aún no está conectado. Llámenos al 7290-7799.', 'error');
      return;
    }

    button.disabled = true;
    button.textContent = 'Enviando…';
    aviso('', 'info');

    fetch(form.action, {
      method: 'POST',
      body: new FormData(form),
      headers: { Accept: 'application/json' }
    })
      .then(function (res) {
        if (res.ok) {
          form.reset();
          aviso('Mensaje enviado. Le contestamos lo antes posible.', 'ok');
        } else {
          aviso('No se pudo enviar. Escríbanos por WhatsApp al 7290-7799.', 'error');
        }
      })
      .catch(function () {
        aviso('No se pudo enviar. Escríbanos por WhatsApp al 7290-7799.', 'error');
      })
      .finally(function () {
        button.disabled = false;
        button.textContent = textoOriginal;
      });
  });
})();
