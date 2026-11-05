// Medición de comportamiento para Google Analytics 4 (G-ZBZ5SG4BJM).
// Sirve para ver PATRONES de la gente que entra desde los anuncios: hasta
// dónde baja, qué secciones mira de verdad, qué preguntas abre y si empieza
// el formulario. Nada de esto es una conversión de Google Ads (no le dice a
// Google que puje más): solo informa. Las conversiones siguen siendo
// únicamente Llamar / WhatsApp / formulario (ver conversiones.js).
//
// Reglas: nada corre si gtag no cargó; cada evento se manda una sola vez por
// visita; el scroll se lee en rAF (pasivo) para no costar fluidez.
(function () {
  var GA = 'G-ZBZ5SG4BJM';
  var inicio = Date.now();
  var maxPct = 0;

  function enviar(nombre, params) {
    if (typeof window.gtag !== 'function') return;
    params = params || {};
    params.send_to = GA;
    window.gtag('event', nombre, params);
  }

  function pctActual() {
    var doc = document.documentElement;
    var alto = Math.max(doc.scrollHeight - window.innerHeight, 1);
    return Math.min(100, Math.round((window.scrollY / alto) * 100));
  }

  // Lo usa conversiones.js para adjuntar contexto a cada contacto.
  window.artaviaMedicion = {
    profundidad: function () { return Math.max(maxPct, pctActual()); },
    segundos: function () { return Math.round((Date.now() - inicio) / 1000); }
  };

  // 1) Profundidad de lectura: 25 / 50 / 75 / 100 %.
  var hitos = [25, 50, 75, 100];
  var raf = 0;
  function medirScroll() {
    raf = 0;
    var p = pctActual();
    if (p > maxPct) maxPct = p;
    while (hitos.length && maxPct >= hitos[0]) {
      enviar('profundidad_pagina', { porcentaje: hitos.shift() });
    }
    if (!hitos.length) window.removeEventListener('scroll', alScroll);
  }
  function alScroll() { if (!raf) raf = requestAnimationFrame(medirScroll); }
  window.addEventListener('scroll', alScroll, { passive: true });

  // 2) Secciones vistas de verdad: ocupando al menos media pantalla (o la
  //    mitad de la sección, si es más baja que eso) durante 1 s seguido.
  //    Pasar de largo con el dedo no cuenta. Se mide contra la pantalla y no
  //    solo contra la sección: una sección más alta que el teléfono nunca
  //    llega a estar "50 % visible" y jamás se contaría.
  if ('IntersectionObserver' in window) {
    var timers = {};
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        var el = en.target;
        var nombre = el.getAttribute('data-zona') || el.id;
        var vista = en.isIntersecting &&
          (en.intersectionRatio >= 0.5 || en.intersectionRect.height >= window.innerHeight * 0.5);
        if (vista) {
          if (timers[nombre]) return;
          timers[nombre] = setTimeout(function () {
            enviar('seccion_vista', { seccion: nombre, segundos: window.artaviaMedicion.segundos() });
            io.unobserve(el);
          }, 1000);
        } else {
          clearTimeout(timers[nombre]);
          timers[nombre] = 0;
        }
      });
    }, { threshold: [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.75, 1] });
    document.querySelectorAll('section[id]:not(#hero), section[data-zona]').forEach(function (s) { io.observe(s); });
  }

  // 3) Preguntas frecuentes abiertas: dicen qué duda frena a la gente.
  document.querySelectorAll('details.faq').forEach(function (d) {
    var hecho = false;
    d.addEventListener('toggle', function () {
      if (!d.open || hecho) return;
      hecho = true;
      var s = d.querySelector('summary');
      enviar('pregunta_abierta', { pregunta: s ? s.textContent.trim().slice(0, 80) : '' });
    });
  });

  // 4) Empezó a llenar el formulario (aunque no lo envíe).
  var form = document.getElementById('form-contacto');
  if (form) {
    form.addEventListener('focusin', function una() {
      form.removeEventListener('focusin', una);
      enviar('formulario_inicio', { segundos: window.artaviaMedicion.segundos() });
    });
  }
})();
