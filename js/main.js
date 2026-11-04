// Foco de luz del hero que sigue al puntero. Solo PC con hover real y sin
// reduced-motion: en teléfono ni se registra el listener. El gradiente vive
// en CSS; JS solo escribe dos custom properties, una vez por frame.
(function () {
  var media = window.matchMedia('(min-width: 1024px) and (hover: hover) and (prefers-reduced-motion: no-preference)');
  var hero = document.getElementById('hero');
  if (!hero || !media.matches) return;
  var raf = 0, x = 0, y = 0;
  function pintar() {
    raf = 0;
    hero.style.setProperty('--mx', x.toFixed(1) + '%');
    hero.style.setProperty('--my', y.toFixed(1) + '%');
  }
  hero.addEventListener('pointermove', function (e) {
    var r = hero.getBoundingClientRect();
    x = ((e.clientX - r.left) / r.width) * 100;
    y = ((e.clientY - r.top) / r.height) * 100;
    if (!raf) raf = requestAnimationFrame(pintar);
  }, { passive: true });
  hero.addEventListener('pointerleave', function () {
    x = 50; y = 40;
    if (!raf) raf = requestAnimationFrame(pintar);
  });
})();

// Formulario de contacto: arma el mensaje y lo abre en WhatsApp del negocio.
// No depende de servicios externos ni cuentas: el mensaje llega directo al
// 7290-7799, que es donde el cliente ya atiende. También registra la
// conversión de Google Ads con la etiqueta "formulario".
(function () {
  var form = document.getElementById('form-contacto');
  if (!form) return;
  var status = document.getElementById('form-status');
  var WHATSAPP = '50672907799';
  var SEND_TO = 'AW-18411203647/uJPiCJ_Vy6IdEL_YkstE';
  var enviadoEn = 0;

  function aviso(texto, tipo) {
    status.textContent = texto;
    status.className = 'form-status form-status--' + tipo;
  }

  function campo(nombre, max) {
    var el = form.elements[nombre];
    return el ? String(el.value || '').trim().slice(0, max) : '';
  }

  form.addEventListener('submit', function (e) {
    e.preventDefault();

    // Trampa anti-bots: si el campo oculto viene lleno, se ignora en silencio.
    if (campo('_gotcha', 100)) return;

    if (!form.checkValidity()) {
      aviso('Complete nombre, teléfono y el mensaje.', 'error');
      var primero = form.querySelector(':invalid');
      if (primero) primero.focus();
      return;
    }

    // Evita abrir WhatsApp dos veces por un doble toque.
    var ahora = Date.now();
    if (ahora - enviadoEn < 3000) return;
    enviadoEn = ahora;

    var texto =
      'Hola, les escribo desde la página web.\n' +
      'Nombre: ' + campo('nombre', 80) + '\n' +
      'Teléfono: ' + campo('telefono', 30) + '\n' +
      'Necesito: ' + campo('mensaje', 800);
    var url = 'https://wa.me/' + WHATSAPP + '?text=' + encodeURIComponent(texto);

    if (typeof window.gtag === 'function') {
      window.gtag('event', 'conversion', {
        send_to: SEND_TO,
        event_label: 'formulario',
        transport_type: 'beacon'
      });
    }

    // Pestaña nueva (como los demás botones de WhatsApp); si el navegador la
    // bloquea, abre WhatsApp en la misma pestaña. (No se usa el flag 'noopener'
    // en window.open porque hace que devuelva null y se abriría dos veces.)
    var win = window.open(url, '_blank');
    if (win) { win.opener = null; } else { window.location.href = url; }

    form.reset();
    aviso('Listo: se abrió WhatsApp con su mensaje. Solo toque "Enviar" ahí.', 'ok');
  });
})();

// Animaciones continuas (marquee, radar): solo corren mientras se ven.
// Fuera de cuadro se pausan; un bucle vivo fuera de pantalla es tirar frames.
(function () {
  if (!('IntersectionObserver' in window)) return;
  var vivos = document.querySelectorAll('.marquee, .radar');
  if (!vivos.length) return;
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (en) { en.target.classList.toggle('is-off', !en.isIntersecting); });
  }, { rootMargin: '35%' });
  vivos.forEach(function (el) { io.observe(el); });
})();

// Mapa: facade. El iframe de Google Maps solo se crea cuando el usuario lo pide.
(function () {
  var map = document.getElementById('map');
  var btn = document.getElementById('map-load');
  if (!map || !btn) return;
  btn.addEventListener('click', function () {
    var f = document.createElement('iframe');
    f.title = 'Mapa: Corina Rodríguez, Alajuelita';
    f.src = map.dataset.src;
    f.loading = 'lazy';
    f.referrerPolicy = 'no-referrer-when-downgrade';
    f.allowFullscreen = true;
    map.innerHTML = '';
    map.appendChild(f);
  });
})();

// Catálogo: en pantallas táctiles (sin hover) un toque despliega la lista.
(function () {
  if (window.matchMedia('(hover: hover)').matches) return;
  document.querySelectorAll('.cat').forEach(function (c) {
    c.addEventListener('click', function () { c.classList.toggle('is-open'); });
  });
})();
