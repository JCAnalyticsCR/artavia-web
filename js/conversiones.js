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
(function () {
  var SEND_TO = 'AW-18411203647/uJPiCJ_Vy6IdEL_YkstE';
  var ESPERA_MS = 1500; // anti doble toque: un contacto por ráfaga de clics
  var ultimo = 0;

  function tipoDeContacto(href) {
    if (/^tel:/i.test(href)) return 'llamada';
    if (/^https?:\/\/(wa\.me|api\.whatsapp\.com|web\.whatsapp\.com)\//i.test(href)) return 'whatsapp';
    return null;
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
  }, true);
})();
