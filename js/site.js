/* Vape Recyclers — site behaviour */
(function () {
  'use strict';

  /* ---------- CONFIG: where form submissions are delivered ---------- */
  // Every form posts here. FormSubmit emails each submission as a table to the inbox below.
  // First submission triggers a one-off activation email to that inbox — click the link once.
  // To change the inbox, edit this one line.
  var FORM_INBOX = 'info@recycle.net.au';
  var FORM_ENDPOINT = 'https://formsubmit.co/ajax/' + FORM_INBOX;

  /* ---------- mobile nav ---------- */
  var btn = document.querySelector('.menu-btn');
  var nav = document.getElementById('nav');
  if (btn && nav) {
    btn.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
      btn.innerHTML = open
        ? '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M6 6l12 12M18 6L6 18"/></svg><span class="skip">Close menu</span>'
        : '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h16"/></svg><span class="skip">Open menu</span>';
    });
    nav.addEventListener('click', function (e) {
      if (e.target.closest('a')) { nav.classList.remove('open'); btn.setAttribute('aria-expanded', 'false'); }
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && nav.classList.contains('open')) btn.click();
    });
  }

  /* ---------- hide mobile CTA bar when a form is on screen ---------- */
  var mcta = document.querySelector('.m-cta');
  var forms = document.querySelectorAll('form[data-form]');
  if (mcta && forms.length && 'IntersectionObserver' in window) {
    var visible = new Set();
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { en.isIntersecting ? visible.add(en.target) : visible.delete(en.target); });
      mcta.classList.toggle('hide', visible.size > 0);
    }, { threshold: 0.05 });
    forms.forEach(function (f) { io.observe(f.closest('.form-card') || f); });
  }

  /* ---------- reveal on scroll ---------- */
  var rev = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    var ro = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('in'); ro.unobserve(en.target); } });
    }, { threshold: 0.12 });
    rev.forEach(function (el) { ro.observe(el); });
  } else { rev.forEach(function (el) { el.classList.add('in'); }); }

  /* ---------- chooser (home) ---------- */
  var chooser = document.querySelector('[data-chooser]');
  if (chooser) {
    var answers = {
      home: { text: '<strong>Drop them off.</strong> Bring household vapes to our North Geelong facility — no booking needed for small amounts. Tape any loose battery terminals first.', href: 'drop-off.html', label: 'Drop-off details' },
      ongoing: { text: '<strong>Get a collection bin.</strong> We supply a lidded bin and signage, then collect and swap it when it fills — ideal for pharmacies, schools, councils and workplaces.', href: 'bins.html#request', label: 'Request a bin' },
      bulk: { text: '<strong>Book a bulk drop-off.</strong> Confiscated vapes, seized stock or a backlog in storage — tell us roughly how many first so we can receive them safely.', href: 'drop-off.html#bulk', label: 'Book a bulk drop-off' }
    };
    var ans = chooser.querySelector('.answer');
    chooser.querySelectorAll('.choice').forEach(function (c) {
      c.addEventListener('click', function () {
        chooser.querySelectorAll('.choice').forEach(function (o) { o.setAttribute('aria-pressed', 'false'); });
        c.setAttribute('aria-pressed', 'true');
        var a = answers[c.dataset.choice];
        ans.querySelector('p').innerHTML = a.text;
        var link = ans.querySelector('a');
        link.href = a.href; link.querySelector('span').textContent = a.label;
        ans.classList.add('show');
      });
    });
  }

  /* ---------- pre-select a value from the URL (?type=pharmacy) ---------- */
  var params = new URLSearchParams(location.search);
  if (params.get('type')) {
    var sel = document.querySelector('select[name="Organisation type"]');
    if (sel) { Array.prototype.forEach.call(sel.options, function (o) { if (o.value.toLowerCase().indexOf(params.get('type').toLowerCase()) === 0) sel.value = o.value; }); }
  }

  /* ---------- forms ---------- */
  function ref() {
    var c = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789', s = '';
    for (var i = 0; i < 6; i++) s += c[Math.floor(Math.random() * c.length)];
    return 'VR-' + s;
  }
  function fieldOf(el) { return el.closest('.field'); }
  function validate(form) {
    var ok = true, first = null;
    form.querySelectorAll('.field').forEach(function (f) { f.classList.remove('invalid'); });
    form.querySelectorAll('[required]').forEach(function (el) {
      var bad = false;
      if (el.type === 'radio') {
        bad = !form.querySelector('input[name="' + el.name + '"]:checked');
      } else if (el.type === 'checkbox') {
        bad = !el.checked;
      } else {
        bad = !el.value.trim() || !el.checkValidity();
      }
      if (el.name === 'Phone' && el.value.trim()) {
        var digits = el.value.replace(/\D/g, '');
        if (digits.length < 8 || digits.length > 12) bad = true;
      }
      if (el.name === 'Postcode' && el.value.trim() && !/^\d{4}$/.test(el.value.trim())) bad = true;
      if (bad) { var f = fieldOf(el); if (f) f.classList.add('invalid'); ok = false; if (!first) first = el; }
    });
    if (first) { first.focus({ preventScroll: true }); first.scrollIntoView({ behavior: 'smooth', block: 'center' }); }
    return ok;
  }
  function collect(form) {
    var data = {};
    new FormData(form).forEach(function (v, k) {
      if (k === '_honey') return;
      if (data[k]) data[k] += ', ' + v; else data[k] = v;
    });
    return data;
  }

  forms.forEach(function (form) {
    form.setAttribute('novalidate', '');
    form.querySelectorAll('input,select,textarea').forEach(function (el) {
      el.addEventListener('input', function () { var f = fieldOf(el); if (f) f.classList.remove('invalid'); });
      el.addEventListener('change', function () { var f = fieldOf(el); if (f) f.classList.remove('invalid'); });
    });

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var card = form.closest('.form-card');
      var err = card.querySelector('.form-error');
      err.classList.remove('show');
      if (form.querySelector('[name="_honey"]').value) return; // bot
      if (!validate(form)) return;

      var submit = form.querySelector('button[type=submit]');
      submit.disabled = true; submit.classList.add('busy');

      var r = ref();
      var data = collect(form);
      data['Reference'] = r;
      data['Page'] = location.href.split('?')[0];
      data._subject = form.dataset.subject + ' — ' + r + (data['Organisation'] ? ' — ' + data['Organisation'] : (data['Name'] ? ' — ' + data['Name'] : ''));
      data._template = 'table';
      data._captcha = 'false';
      if (data['Email']) data._replyto = data['Email'];

      fetch(FORM_ENDPOINT, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
        body: JSON.stringify(data)
      }).then(function (res) {
        return res.json().catch(function () { return {}; }).then(function (j) {
          if (!res.ok || (j && (j.success === false || j.success === 'false'))) throw new Error((j && j.message) || 'Send failed');
          return j;
        });
      }).then(function () {
        var done = card.querySelector('.form-done');
        done.querySelector('.ref').textContent = r;
        var nm = done.querySelector('[data-name]');
        if (nm) nm.textContent = (data['Name'] || '').split(' ')[0] || 'there';
        form.style.display = 'none';
        card.querySelectorAll('[data-hide-on-done]').forEach(function (h) { h.style.display = 'none'; });
        done.classList.add('show');
        card.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }).catch(function () {
        // Fallback: let the person send the same details by email so nothing is lost.
        var body = Object.keys(data).filter(function (k) { return k.charAt(0) !== '_'; })
          .map(function (k) { return k + ': ' + data[k]; }).join('\n');
        var mail = 'mailto:' + FORM_INBOX + '?subject=' + encodeURIComponent(data._subject) + '&body=' + encodeURIComponent(body);
        err.innerHTML = 'Sorry — that didn’t send. Please <a href="' + mail + '">email your details instead</a> (we’ve filled it in for you) or call <a href="tel:0460555222">0460 555 222</a>.';
        err.classList.add('show');
      }).finally(function () {
        submit.disabled = false; submit.classList.remove('busy');
      });
    });
  });

  /* ---------- year ---------- */
  var y = document.querySelector('[data-year]');
  if (y) y.textContent = new Date().getFullYear();
})();
