// Registro de IP de visitas que llegan desde un anuncio de Google.
// Objetivo: detectar IP que hacen clic en el anuncio una y otra vez (clics
// inválidos o de competencia) para excluirlas en Google Ads
// (Configuración de la campaña → Exclusiones de IP).
//
// Cómo funciona, sin servidor propio (el sitio es estático):
//   1. Solo actúa si la URL trae un identificador de clic de Google Ads
//      (gclid / gbraid / wbraid). Las visitas normales no se registran.
//   2. Pregunta la IP pública a api.ipify.org (servicio gratuito, sin cuenta).
//   3. La manda a un formulario de Google de la cuenta de la cerrajería, que
//      la guarda en la hoja "Registro de IP de anuncios - Cerrajeria Artavia".
//      La pestaña "IP repetidas" cuenta visitas por IP en los últimos 7 días.
//
// Nunca bloquea ni retrasa la página: corre cuando el navegador está libre,
// con tiempo límite, y si algo falla simplemente no registra.
(function () {
  var FORM = 'https://docs.google.com/forms/d/e/1FAIpQLSfw3Ty1k30QiIzjHsD9kN3ZcvjdURtyJQkAxo-UW6qDLMjycg/formResponse';
  var CAMPO_IP = 'entry.658735947';
  var CAMPO_CLIC = 'entry.948886282';
  var CAMPO_DISPOSITIVO = 'entry.1933471517';

  var params;
  try { params = new URLSearchParams(window.location.search); } catch (e) { return; }
  var tipo = ['gclid', 'gbraid', 'wbraid'].filter(function (k) { return params.get(k); })[0];
  if (!tipo || !window.fetch) return;
  var clic = tipo + ':' + String(params.get(tipo)).slice(0, 150);

  // Recargar la página con el mismo clic no cuenta como otra visita.
  try {
    if (sessionStorage.getItem('artavia_clic') === clic) return;
    sessionStorage.setItem('artavia_clic', clic);
  } catch (e) { /* sin sessionStorage: se registra igual */ }

  function conLimite(promesa, ms) {
    return Promise.race([promesa, new Promise(function (_, no) { setTimeout(no, ms); })]);
  }

  function registrar() {
    conLimite(fetch('https://api.ipify.org?format=json', { cache: 'no-store' }), 5000)
      .then(function (r) { return r.json(); })
      .then(function (d) {
        if (!d || !d.ip) return;
        var movil = window.matchMedia('(hover: none) and (pointer: coarse)').matches;
        var cuerpo = new URLSearchParams();
        cuerpo.append(CAMPO_IP, d.ip);
        cuerpo.append(CAMPO_CLIC, clic);
        cuerpo.append(CAMPO_DISPOSITIVO, (movil ? 'movil' : 'escritorio') + ' ' + screen.width + 'x' + screen.height);
        // no-cors: Google Forms no responde con CORS; la respuesta no se lee,
        // solo importa que el envío llegue.
        return fetch(FORM, { method: 'POST', mode: 'no-cors', body: cuerpo, keepalive: true });
      })
      .catch(function () { /* sin registro: no afecta al visitante */ });
  }

  if ('requestIdleCallback' in window) {
    window.requestIdleCallback(registrar, { timeout: 4000 });
  } else {
    window.addEventListener('load', function () { setTimeout(registrar, 1500); });
  }
})();
