/* JANETO.NG – front-end behaviour (no dependencies) */
(function () {
  'use strict';
  var doc = document.documentElement;
  doc.classList.remove('no-js');
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };
  var EMAIL = 'ovationsglam@gmail.com';

  /* ---------- sticky header: 100px -> 80px, transparent -> solid on the home page ---------- */
  var nav = $('#mainNav');
  function onScrollNav() {
    if (nav) nav.classList.toggle('affix', window.pageYOffset > 0);
  }

  /* ---------- "More" dropdown when the menu doesn't fit ---------- */
  function layoutMenu() {
    if (!nav || getComputedStyle(nav).display === 'none') return;
    var ul = $('.navPages', nav), more = $('.nav-more', nav), dd = $('.nav-dropdown', more);
    // restore everything first
    $$('li', dd).forEach(function (li) { ul.insertBefore(li, more); });
    more.hidden = true;
    var container = $('.nav-container', nav), brand = $('.brand', nav), actions = $('.navActions', nav);
    var avail = function () {
      var cs = getComputedStyle(container);
      return container.clientWidth - parseFloat(cs.paddingLeft) - parseFloat(cs.paddingRight) - brand.offsetWidth - actions.offsetWidth - 20;
    };
    if (ul.scrollWidth <= avail()) return;
    more.hidden = false;
    var items = $$(':scope > li:not(.nav-more)', ul);
    while (items.length && ul.scrollWidth > avail()) {
      dd.insertBefore(items.pop(), dd.firstChild);
    }
  }
  if (nav) {
    var moreLink = $('.nav-more > a', nav);
    moreLink.addEventListener('click', function (e) {
      e.preventDefault();
      var li = moreLink.parentNode, open = !li.classList.contains('open');
      li.classList.toggle('open', open);
      moreLink.setAttribute('aria-expanded', open);
    });
    document.addEventListener('click', function (e) {
      var li = $('.nav-more', nav);
      if (li && !li.contains(e.target)) li.classList.remove('open');
    });
  }

  /* ---------- footer "More" drop-up (phones) ---------- */
  $$('.footer-more > a').forEach(function (a) {
    a.addEventListener('click', function (e) {
      e.preventDefault();
      var open = !a.parentNode.classList.contains('open');
      a.parentNode.classList.toggle('open', open);
      a.setAttribute('aria-expanded', open);
    });
  });
  document.addEventListener('click', function (e) {
    $$('.footer-more.open').forEach(function (li) { if (!li.contains(e.target)) li.classList.remove('open'); });
  });

  /* ---------- popups ---------- */
  var openStack = [];
  function openPopup(id) {
    var p = document.getElementById(id);
    if (!p) return;
    if (id !== 'popupMenu') closePopup('popupMenu');
    p.classList.add('open');
    p.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';
    openStack.push(p);
    var f = $('input, button.js-close', p);
    setTimeout(function () { if (f && f.tagName === 'INPUT' && window.innerWidth > 767) f.focus(); }, 700);
  }
  function closePopup(id) {
    var p = id ? document.getElementById(id) : openStack[openStack.length - 1];
    if (!p || !p.classList.contains('open')) return;
    p.classList.remove('open');
    p.setAttribute('aria-hidden', 'true');
    openStack = openStack.filter(function (x) { return x !== p; });
    if (!openStack.length) document.body.style.overflow = '';
  }
  document.addEventListener('click', function (e) {
    var t = e.target.closest ? e.target.closest('a, button') : null;
    if (!t) return;
    if (t.classList.contains('js-open-menu')) { e.preventDefault(); openPopup('popupMenu'); }
    else if (t.classList.contains('js-open-email')) { e.preventDefault(); openPopup('popupEmail'); }
    else if (t.classList.contains('js-open-client')) { e.preventDefault(); openPopup('popupClient'); }
    else if (t.classList.contains('js-close')) { e.preventDefault(); closePopup(t.closest('.popup').id); }
  });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') closePopup(); });

  /* ---------- forms: validation + mailto hand-off (no server on static hosting) ---------- */
  var EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
  var PHONE_RE = /^[0-9+()\-.\s]{5,}$/;
  function setError(input, msg) {
    var next = input.nextElementSibling;
    if (next && next.classList.contains('error-msg')) next.remove();
    input.classList.toggle('error', !!msg);
    if (msg) {
      var s = document.createElement('span');
      s.className = 'error-msg';
      s.textContent = msg;
      input.insertAdjacentElement('afterend', s);
    }
  }
  function validate(form) {
    var ok = true;
    $$('.form-control', form).forEach(function (input) {
      var v = input.value.trim(), msg = '';
      if (input.required && !v) msg = 'This field is required.';
      else if (v && input.hasAttribute('data-email') && !EMAIL_RE.test(v)) msg = 'Please enter a valid email.';
      else if (v && input.hasAttribute('data-phone') && !PHONE_RE.test(v)) msg = 'Please enter a valid phone number.';
      setError(input, msg);
      if (msg) ok = false;
    });
    return ok;
  }
  function note(form, text) {
    var n = $('.form-note', form);
    if (!n) return;
    n.textContent = text;
    n.hidden = false;
  }
  function mailtoFallback(form) {
    var lines = $$('.form-control', form).map(function (i) { return (i.getAttribute('data-label') || i.name) + ': ' + i.value.trim(); });
    window.location.href = 'mailto:' + EMAIL + '?subject=' + encodeURIComponent(form.getAttribute('data-subject') || 'Website enquiry') +
      '&body=' + encodeURIComponent(lines.join('\n'));
    note(form, 'We couldn’t send your message from the website, so your email app should open with it ready to send. If it doesn’t, email ' + EMAIL + ' directly.');
  }
  $$('.js-mail-form').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!validate(form) || form.classList.contains('sending')) return;
      var n = $('.form-note', form), btn = $('button[type=submit]', form);
      if (n) n.hidden = true;
      var data = new FormData(form);
      data.append('form', form.getAttribute('data-form') || '');
      form.classList.add('sending');
      btn.disabled = true;
      fetch(form.getAttribute('action'), { method: 'POST', body: data, headers: { 'Accept': 'application/json' } })
        .then(function (res) {
          return res.json().then(function (json) { return { status: res.status, json: json }; });
        })
        .then(function (r) {
          if (r.json && r.json.ok) {
            form.reset();
            note(form, 'Thank you for contacting us.');
          } else if (r.json && r.json.fields) {
            Object.keys(r.json.fields).forEach(function (k) {
              var input = form.querySelector('[name="' + k + '"]');
              if (input) setError(input, r.json.fields[k]);
            });
          } else if (r.json && r.status === 429) {
            note(form, r.json.error);
          } else {
            mailtoFallback(form);
          }
        })
        .catch(function () { mailtoFallback(form); }) // no PHP / not JSON / offline
        .then(function () { form.classList.remove('sending'); btn.disabled = false; });
    });
    form.addEventListener('input', function (e) { if (e.target.classList.contains('error')) setError(e.target, ''); });
  });
  var client = $('.client-form');
  if (client) {
    client.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!validate(client)) return;
      note(client, 'Client sign-in needs a server-side account system and isn’t available on this static website.');
    });
  }

  /* ---------- THE ME carousel (Bootstrap-style slide, 10s interval, pause on hover, swipe) ---------- */
  $$('.t-carousel').forEach(function (car) {
    var items = $$('.t-item', car), idx = 0, busy = false, timer = null;
    var interval = parseInt(car.getAttribute('data-interval'), 10) || 10000;
    function go(dir, to) {
      if (busy || items.length < 2) return;
      var next = typeof to === 'number' ? to : (idx + (dir === 'next' ? 1 : -1) + items.length) % items.length;
      var cur = items[idx], nx = items[next];
      var cls = dir === 'next' ? 'left' : 'right';
      busy = true;
      nx.classList.add(dir);
      void nx.offsetWidth; // reflow
      cur.classList.add(cls);
      nx.classList.add(cls);
      var done = function () {
        nx.classList.remove(dir, cls);
        nx.classList.add('active');
        cur.classList.remove('active', cls);
        idx = next;
        busy = false;
      };
      setTimeout(done, 600);
    }
    function start() { stop(); timer = setInterval(function () { go('next'); }, interval); }
    function stop() { if (timer) clearInterval(timer); timer = null; }
    $('.t-control.left', car).addEventListener('click', function () { go('prev'); start(); });
    $('.t-control.right', car).addEventListener('click', function () { go('next'); start(); });
    car.addEventListener('mouseenter', stop);
    car.addEventListener('mouseleave', start);
    var x0 = null;
    car.addEventListener('touchstart', function (e) { x0 = e.touches[0].clientX; }, { passive: true });
    car.addEventListener('touchend', function (e) {
      if (x0 === null) return;
      var dx = e.changedTouches[0].clientX - x0;
      if (Math.abs(dx) > 40) { go(dx < 0 ? 'next' : 'prev'); start(); }
      x0 = null;
    });
    // like SITE123: every slide gets the height of the tallest one
    function equalize() {
      var cards = $$('.t-card', car);
      cards.forEach(function (c) { c.style.minHeight = ''; });
      var max = 0;
      items.forEach(function (it) {
        var shown = it.classList.contains('active');
        if (!shown) { it.style.display = 'block'; it.style.position = 'absolute'; it.style.visibility = 'hidden'; it.style.width = '100%'; }
        max = Math.max(max, $('.t-card', it).offsetHeight);
        if (!shown) { it.style.display = it.style.position = it.style.visibility = it.style.width = ''; }
      });
      cards.forEach(function (c) { c.style.minHeight = max + 'px'; });
    }
    car._equalize = equalize;
    equalize();
    start();
  });

  /* ---------- Affiliation logo carousel (owl-style endless loop: 5 visible, 3s autoplay, 0.25s slide) ---------- */
  $$('.logo-carousel[data-enabled="true"]').forEach(function (car) {
    var track = $('.logo-track', car), busy = false, timer = null;
    var delay = parseInt(car.getAttribute('data-autoplay'), 10) || 3000;
    function step() {
      var first = track.firstElementChild;
      if (busy || !first || track.children.length < 2) return;
      busy = true;
      track.style.transition = 'transform .25s ease';
      track.style.transform = 'translateX(' + (-first.offsetWidth) + 'px)';
      setTimeout(function () {
        track.style.transition = 'none';
        track.appendChild(first);        // recycle the first logo to the end: endless loop
        track.style.transform = 'none';
        busy = false;
      }, 260);
    }
    function start() { stop(); timer = setInterval(step, delay); }
    function stop() { if (timer) clearInterval(timer); timer = null; }
    car.addEventListener('mouseenter', stop);
    car.addEventListener('mouseleave', start);
    start();
  });

  /* ---------- parallax images: same maths as jarallax (type "scroll", speed 0.5), desktop only ---------- */
  var parallax = $$('[data-parallax]');
  function coverParallax() {
    var wndH = window.innerHeight, off = window.innerWidth < 768;
    parallax.forEach(function (img) {
      if (off) { img.style.height = img.style.marginTop = img.style.transform = ''; img._dist = null; return; }
      var speed = parseFloat(img.getAttribute('data-parallax')) || 0.5;
      var contH = img.parentNode.getBoundingClientRect().height;
      var resultH = contH + (wndH - contH) * (1 - speed);
      img._dist = speed * (contH + wndH) / 2;
      img.style.height = resultH + 'px';
      img.style.marginTop = ((wndH - resultH) / 2) + 'px';
    });
  }
  function onScrollParallax() {
    var wndH = window.innerHeight;
    parallax.forEach(function (img) {
      if (img._dist == null) return;
      var rect = img.parentNode.getBoundingClientRect();
      if (rect.bottom < -50 || rect.top > wndH + 50) return;
      var fromCenter = 1 - 2 * ((wndH - rect.top) / (wndH + rect.height));
      img.style.transform = 'translate3d(0,' + (img._dist * fromCenter - rect.top).toFixed(2) + 'px,0)';
    });
  }

  /* ---------- AOS-style reveal (offset 120px, animates out again when scrolled back above) ---------- */
  var aos = $$('[data-aos]');
  var aosTops = [];
  function absTop(el) { var t = 0; while (el) { t += el.offsetTop; el = el.offsetParent; } return t; }
  function measureAos() { aosTops = aos.map(absTop); }
  function onScrollAos() {
    var bottom = window.pageYOffset + window.innerHeight;
    aos.forEach(function (el, i) {
      var top = aosTops[i];
      if (bottom - 120 > top || (window.pageYOffset + window.innerHeight >= document.body.scrollHeight - 2)) el.classList.add('aos-animate');
      else if (bottom < top) el.classList.remove('aos-animate');
    });
  }

  // scroll events already fire at most once per frame; updating synchronously keeps the
  // parallax in step with the page and doesn't stall when requestAnimationFrame is paused
  function onScroll() { onScrollNav(); onScrollAos(); onScrollParallax(); }
  function onResize() { layoutMenu(); coverParallax(); $$('.t-carousel').forEach(function (c) { if (c._equalize) c._equalize(); }); measureAos(); onScroll(); }
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onResize);
  window.addEventListener('load', onResize);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(onResize);
  onResize();
})();
