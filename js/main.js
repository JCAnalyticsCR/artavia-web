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
