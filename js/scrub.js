// Cerradura 3D atada al scroll: secuencia de fotogramas dibujada en canvas.
//
// Nunca <video>.currentTime: una secuencia de imágenes es acceso aleatorio
// real, el fotograma 47 cuesta lo mismo que el 3. Reglas que se pagaron con
// bugs reales (ver skill frontend-cinematografico):
//  - img.decode() con .catch() y fallback, nunca solo onload.
//  - Nada descarga hasta que un IntersectionObserver lo pida.
//  - La posición dibujada persigue al scroll con un lerp (0.09).
//  - DPR tope 2. Redibujados idénticos se saltan.
//  - reduced-motion: UN fotograma, no 90.
//  - El bucle rAF solo corre con la escena cerca de cuadro.
(function () {
  var stage = document.getElementById('lock-stage');
  if (!stage) return;
  // La escena solo existe en escritorio (en móvil está en display:none):
  // no se descarga ni un fotograma en teléfono.
  if (!window.matchMedia('(min-width: 901px)').matches) return;
  var canvas = stage.querySelector('canvas');
  var poster = stage.querySelector('img');
  var hero = document.getElementById('hero');
  var pinEl = hero.querySelector('.hero__pin');
  if (!canvas || !hero || !pinEl) return;

  var FRAMES = Number(stage.dataset.frames || 90);
  var PATH = stage.dataset.path || 'img/frames/cerradura';
  var ANIM_FIN = 0.78;   // la secuencia termina al 78% del pin; el resto es cola quieta
  var ALCANCE = 0.09;    // lerp: más bajo = más peso en cada click de rueda

  var ctx = canvas.getContext('2d');
  var loaded = new Array(FRAMES);
  var lastLow = -1, lastHigh = -1;
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var pad = function (n) { return String(n).padStart(3, '0'); };
  var src = function (i) { return PATH + '/f' + pad(i + 1) + '.webp'; };

  function draw(frac) {
    var dpr = Math.min(window.devicePixelRatio || 1, 2);
    var w = stage.clientWidth, h = stage.clientHeight;
    if (!w || !h) return;
    if (canvas.width !== w * dpr || canvas.height !== h * dpr) {
      canvas.width = w * dpr; canvas.height = h * dpr;
      lastLow = -1;
    }
    var exact = frac * (FRAMES - 1);
    var low = Math.max(0, Math.min(FRAMES - 1, Math.floor(exact)));
    var high = Math.min(FRAMES - 1, low + 1);
    var blend = exact - low;
    // Si el fotograma pedido aún no llegó, se dibuja el más cercano ya
    // decodificado hacia atrás: la escena avanza a saltos mientras carga,
    // nunca se queda pegada en un fotograma viejo.
    while (low > 0 && !loaded[low]) low--;
    if (!loaded[high]) { high = low; blend = 0; }
    var a = loaded[low], b = loaded[high];
    // Sin ningún fotograma listo el canvas queda vacío (un resize lo borra):
    // que se vea el póster, nunca un hueco.
    if (!a || !a.complete || a.naturalWidth === 0) { if (poster) poster.style.opacity = ''; return; }
    if (low === lastLow && high === lastHigh && blend < 0.015) return;
    lastLow = low; lastHigh = high;

    // contain: la cerradura entera siempre visible, centrada
    var contain = function (img, alpha) {
      var rc = w / h, ri = img.naturalWidth / img.naturalHeight;
      var dw, dh;
      if (ri > rc) { dw = w; dh = w / ri; } else { dh = h; dw = h * ri; }
      var dx = (w - dw) / 2, dy = (h - dh) / 2;
      ctx.globalAlpha = alpha;
      ctx.drawImage(img, dx * dpr, dy * dpr, dw * dpr, dh * dpr);
    };
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    contain(a, 1);
    if (b && b.complete && b.naturalWidth > 0 && blend > 0.008) contain(b, blend);
    ctx.globalAlpha = 1;
    if (poster && poster.style.opacity !== '0') poster.style.opacity = '0';
  }

  // --- rama reduced-motion: un solo fotograma (la cerradura cerrada) ---
  if (reduced) {
    var ultimo = new Image();
    var pintar = function () {
      if (ultimo.naturalWidth === 0) return;
      loaded[FRAMES - 1] = ultimo; draw(1);
    };
    ultimo.onload = function () { ultimo.decode().then(pintar).catch(pintar); };
    ultimo.src = src(FRAMES - 1);
    return;
  }

  // --- precarga perezosa: arranca cuando el observer lo pide ---
  var started = false;
  function preload() {
    if (started) return;
    started = true;
    var settled = 0;
    var listo = function (i, img, ok) {
      if (ok) {
        loaded[i] = img;
        if (i === 0) { draw(current); }
      }
      settled++;
      if (settled === FRAMES) stage.classList.add('is-ready');
    };
    for (var i = 0; i < FRAMES; i++) {
      (function (i) {
        var img = new Image();
        img.decoding = 'async';
        img.onload = function () {
          img.onload = null; img.onerror = null;
          img.decode()
            .then(function () { listo(i, img, true); })
            .catch(function () { listo(i, img, img.naturalWidth > 0); });
        };
        img.onerror = function () { img.onload = null; img.onerror = null; listo(i, img, false); };
        img.src = src(i);
      })(i);
    }
  }

  // --- progreso: derivado del pin del hero (sticky) ---
  // 0 cuando el hero está arriba del todo, 1 cuando el pin suelta.
  function progresoPin() {
    var rect = hero.getBoundingClientRect();
    var total = hero.offsetHeight - pinEl.offsetHeight;
    if (total <= 0) return 0;
    var p = -rect.top / total;
    return Math.max(0, Math.min(1, p));
  }

  var target = 0, current = 0, raf = 0, corriendo = false;
  window.__lock = { loaded: loaded, get target() { return target; }, get current() { return current; } };
  function tick() {
    current += (target - current) * ALCANCE;
    if (Math.abs(target - current) < 0.0006) current = target;
    draw(current);
    raf = requestAnimationFrame(tick);
  }
  function onScroll() {
    target = Math.min(1, progresoPin() / ANIM_FIN);
  }
  function arrancar() {
    if (corriendo) return;
    corriendo = true;
    onScroll(); current = target; draw(current);
    raf = requestAnimationFrame(tick);
  }
  function parar() {
    if (!corriendo) return;
    corriendo = false; cancelAnimationFrame(raf);
  }

  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', function () { lastLow = -1; onScroll(); }, { passive: true });

  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (en) {
      if (en.isIntersecting) { preload(); arrancar(); } else { parar(); }
    });
  }, { rootMargin: '50% 0px' });
  io.observe(hero);
  onScroll();
})();
