// Conversión de Google Ads "Clic saliente" (cuenta AW-18411203647).
// Cuenta un contacto SOLO cuando el visitante toca Llamar (tel:) o WhatsApp
// (wa.me). No cuenta visitas, ni clics a Facebook, Google Maps o reseñas.
//
// Todos los enlaces de contacto del sitio son tel: o abren en pestaña nueva
// (target="_blank"), así que el visitante no sale de la página y el aviso a
// Google se envía sin necesidad de retrasar la navegación.
//
// Se usa delegación de eventos: cubre cualquier botón de llamar o WhatsApp,
// incluidos los que se agreguen después, sin tocar cada enlace.
//
// Además del contacto, a Google Analytics se le dice DÓNDE se tocó el botón
// (ubicacion), qué servicio era (si vino de una tarjeta), cuánto había bajado
// la persona y cuántos segundos tardó en decidirse. Eso es lo que permite ver
// patrones: qué parte de la página realmente produce llamadas.
(function () {
  var SEND_TO = 'AW-18411203647/uJPiCJ_Vy6IdEL_YkstE';
  var ESPERA_MS = 1500; // anti doble toque: un contacto por ráfaga de clics
  var ultimo = 0;

  function tipoDeContacto(href) {
    if (/^tel:/i.test(href)) return 'llamada';
    if (/^https?:\/\/(wa\.me|api\.whatsapp\.com|web\.whatsapp\.com)\//i.test(href)) return 'whatsapp';
    return null;
  }

  // Zona de la página donde está el botón. data-zona manda; si no hay, el id
  // de la sección. Nombres cortos y estables: son los que se leen en GA4.
  function ubicacionDe(a) {
    if (a.closest('.sticky')) return 'barra_fija';
    if (a.closest('.header')) return 'encabezado';
    var z = a.closest('[data-zona], section[id]');
    if (!z) return 'otro';
    return z.getAttribute('data-zona') || z.id;
  }

  function servicioDe(a) {
    var h = a.classList.contains('svc') ? a.querySelector('h3, strong, b') : null;
    return h ? h.textContent.trim().slice(0, 60) : '';
  }

  document.addEventListener('click', function (e) {
    var a = e.target && e.target.closest ? e.target.closest('a[href]') : null;
    if (!a) return;

    var tipo = tipoDeContacto(a.getAttribute('href') || '');
    if (!tipo) return;

    // Si un bloqueador de anuncios impidió cargar gtag, el enlace sigue
    // funcionando normal; solo no se mide.
    if (typeof window.gtag !== 'function') return;

    var ahora = Date.now();
    if (ahora - ultimo < ESPERA_MS) return;
    ultimo = ahora;

    window.gtag('event', 'conversion', {
      send_to: SEND_TO,
      event_label: tipo,
      transport_type: 'beacon' // se envía aunque el navegador cambie a la app de llamadas
    });
    // Mismo contacto para Google Analytics 4 (G-ZBZ5SG4BJM), marcado allá como
    // evento clave "contacto". metodo = llamada | whatsapp.
    var m = window.artaviaMedicion;
    window.gtag('event', 'contacto', {
      metodo: tipo,
      ubicacion: ubicacionDe(a),
      servicio: servicioDe(a),
      profundidad: m ? m.profundidad() : 0,
      segundos: m ? m.segundos() : 0,
      send_to: 'G-ZBZ5SG4BJM',
      transport_type: 'beacon'
    });
  }, true);
})();
