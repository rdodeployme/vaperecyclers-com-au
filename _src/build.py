#!/usr/bin/env python3
"""Builds the static pages for vaperecyclers.com.au.

Edit the page bodies in _src/pages/*.html, then run:  python3 _src/build.py
Each page file starts with three lines:  title | description | nav-key
Icons are written as {{i:name}} and swapped for inline SVG.
"""
import pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / '_src' / 'pages'
SITE = 'https://www.vaperecyclers.com.au'

def svg(inner, sw=2):
    return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{inner}</svg>'

ICONS = {
  'check': svg('<path d="M20 6L9 17l-5-5"/>', 2.4),
  'x': svg('<path d="M18 6L6 18M6 6l12 12"/>', 2.4),
  'arrow': svg('<path d="M5 12h14M13 6l6 6-6 6"/>'),
  'plus': svg('<path d="M12 5v14M5 12h14"/>', 2.4),
  'phone': svg('<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/>'),
  'mail': svg('<rect x="2" y="4" width="20" height="16" rx="2"/><path d="M22 6l-10 7L2 6"/>'),
  'pin': svg('<path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/>'),
  'clock': svg('<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>'),
  'flame': svg('<path d="M8.5 14.5A2.5 2.5 0 0 0 11 12c0-1.4-.5-2-1-3-1.1-2.1-.2-4 2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 1 1-14 0c0-1.2.4-2.3 1-3.3.3 1.5 1.3 2.8 2.5 2.8z"/>'),
  'drop': svg('<path d="M12 2.7l5.7 5.7a8 8 0 1 1-11.3 0z"/>'),
  'cycle': svg('<path d="M21 12a9 9 0 0 1-15.5 6.2M3 12a9 9 0 0 1 15.5-6.2"/><path d="M21 3v6h-6M3 21v-6h6"/>'),
  'shield': svg('<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="M9 12l2 2 4-4"/>'),
  'bin': svg('<path d="M3 6h18M8 6V4a1 1 0 0 1 1-1h6a1 1 0 0 1 1 1v2M5 6l1 14a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2l1-14"/><path d="M10 11v6M14 11v6"/>'),
  'building': svg('<path d="M3 21h18M5 21V8l7-5 7 5v13"/><path d="M9 21v-6h6v6"/>'),
  'truck': svg('<path d="M1 4h14v12H1zM15 8h4l3 3v5h-7"/><circle cx="6" cy="18.5" r="2"/><circle cx="18" cy="18.5" r="2"/>'),
  'pharmacy': svg('<rect x="3" y="3" width="18" height="18" rx="3"/><path d="M12 8v8M8 12h8"/>'),
  'school': svg('<path d="M22 10L12 5 2 10l10 5 10-5z"/><path d="M6 12v5c3 2 9 2 12 0v-5"/>'),
  'council': svg('<path d="M3 21h18M4 10h16M12 3l9 7H3z"/><path d="M6 10v8M10 10v8M14 10v8M18 10v8"/>'),
  'office': svg('<rect x="4" y="2" width="16" height="20" rx="1"/><path d="M9 22v-4h6v4M8 6h.01M12 6h.01M16 6h.01M8 10h.01M12 10h.01M16 10h.01M8 14h.01M12 14h.01M16 14h.01"/>'),
  'venue': svg('<path d="M9 18V5l12-2v13"/><circle cx="6" cy="18" r="3"/><circle cx="18" cy="16" r="3"/>'),
  'health': svg('<path d="M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.7l-1-1.1a5.5 5.5 0 0 0-7.8 7.8l1 1.1L12 21l7.8-7.5 1-1.1a5.5 5.5 0 0 0 0-7.8z"/>'),
  'strata': svg('<path d="M3 21h18M6 21V5h12v16"/><path d="M10 9h4M10 13h4M10 17h4"/>'),
  'store': svg('<path d="M3 9l1.5-5h15L21 9M3 9v11h18V9M3 9h18"/><path d="M9 20v-6h6v6"/>'),
  'tape': svg('<rect x="7" y="2" width="10" height="20" rx="3"/><path d="M7 9h10M7 15h10"/>'),
  'box': svg('<path d="M21 8l-9-5-9 5 9 5 9-5z"/><path d="M3 8v8l9 5 9-5V8M12 13v8"/>'),
  'nobin': svg('<path d="M3 6h18M5 6l1 14a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2l1-14"/><path d="M2 2l20 20"/>'),
  'warn': svg('<path d="M10.3 3.9L1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0z"/><path d="M12 9v4M12 17h.01"/>'),
  'battery': svg('<rect x="2" y="7" width="17" height="10" rx="2"/><path d="M22 11v2M6 10v4M10 10v4"/>'),
  'doc': svg('<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M8 13h8M8 17h5"/>'),
  'menu': svg('<path d="M4 7h16M4 12h16M4 17h16"/>'),
  'sun': svg('<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>'),
  'compact': svg('<path d="M4 4h16M12 4v6M8 7l4 4 4-4M4 20h16M12 20v-6M8 17l4-4 4 4"/>'),
  'heat': svg('<path d="M14 14.8V4a2 2 0 0 0-4 0v10.8a4 4 0 1 0 4 0z"/><path d="M12 9v7"/>'),
  'factory': svg('<path d="M2 20h20M4 20V10l5 3V10l5 3V6h6v14"/><path d="M8 16h.01M12 16h.01M16 16h.01"/>'),
  'law': svg('<path d="M12 3v18M5 7h14M8 21h8M5 7l-3 7a3 3 0 0 0 6 0zM19 7l-3 7a3 3 0 0 0 6 0z"/>'),
  'chip': svg('<rect x="6" y="6" width="12" height="12" rx="2"/><path d="M9 2v4M15 2v4M9 18v4M15 18v4M2 9h4M2 15h4M18 9h4M18 15h4"/>'),
  'users': svg('<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.9M16 3.1a4 4 0 0 1 0 7.8"/>'),
  'child': svg('<circle cx="12" cy="5" r="2.5"/><path d="M12 8v7M8 11h8M9 22l3-7 3 7"/>'),
}

LOGO = ('<svg viewBox="0 0 40 40" aria-hidden="true">'
        '<rect width="40" height="40" rx="11" fill="#1FE3A0"/>'
        '<path d="M31.3 15.9 A12 12 0 1 1 22.1 8.2" fill="none" stroke="#08130F" stroke-width="3" stroke-linecap="round"/>'
        '<path d="M25.6 8.8 L21.4 11.6 L22.6 5.1 Z" fill="#08130F"/>'
        '<rect x="17.6" y="14.2" width="4.8" height="13.6" rx="2.4" fill="#08130F"/>'
        '<rect x="18.7" y="11.6" width="2.6" height="3.4" rx="1.1" fill="#08130F"/>'
        '<rect x="19.3" y="17.4" width="1.4" height="4.4" rx=".7" fill="#1FE3A0"/>'
        '</svg>')

NAV = [('index.html', 'Home', 'home'), ('bins.html', 'Bins', 'bins'),
       ('drop-off.html', 'Drop-off', 'drop'), ('who-we-help.html', 'Who we help', 'who'),
       ('fire-risk.html', 'Fire risk', 'fire'), ('how-we-recycle.html', 'How we recycle', 'how'),
       ('faq.html', 'FAQ', 'faq'), ('contact.html', 'Contact', 'contact')]
SECTOR_KEYS = {'pharmacies', 'schools', 'councils', 'workplaces'}

def header(active):
    links = ''.join(
        f'<a href="{h}"{" aria-current=\"page\"" if (k == active or (k == "who" and active in SECTOR_KEYS)) else ""}>{t}</a>' for h, t, k in NAV if k != 'home')
    return f'''<a class="skip" href="#main">Skip to content</a>
<header class="site-head">
  <div class="wrap head-in">
    <a class="logo" href="index.html" aria-label="Vape Recyclers home">{LOGO}<span>Vape<b>Recyclers</b></span></a>
    <button class="menu-btn" aria-expanded="false" aria-controls="nav">{ICONS['menu']}<span class="skip">Open menu</span></button>
    <nav class="nav" id="nav" aria-label="Main">{links}<a class="btn btn-mint" href="bins.html#request">Request a bin</a></nav>
  </div>
</header>'''

FOOTER = f'''<footer class="site-foot">
  <div class="wrap">
    <div class="foot-grid">
      <div>
        <a class="logo" href="index.html">{LOGO}<span>Vape<b>Recyclers</b></span></a>
        <p>Safe collection and recycling of vapes and e-cigarettes. Collection bins for organisations, and drop-off at our North&nbsp;Geelong facility.</p>
      </div>
      <div>
        <h4>Services</h4>
        <ul>
          <li><a href="bins.html">Collection bins</a></li>
          <li><a href="drop-off.html">Drop-off</a></li>
          <li><a href="drop-off.html#bulk">Bulk drop-off</a></li>
          <li><a href="bins.html#request">Request a bin</a></li>
          <li><a href="contact.html">Contact</a></li>
        </ul>
      </div>
      <div>
        <h4>Who we help</h4>
        <ul>
          <li><a href="pharmacies.html">Pharmacies</a></li>
          <li><a href="schools.html">Schools</a></li>
          <li><a href="councils.html">Councils</a></li>
          <li><a href="workplaces.html">Workplaces</a></li>
        </ul>
      </div>
      <div>
        <h4>Learn</h4>
        <ul>
          <li><a href="fire-risk.html">Vape fire risk</a></li>
          <li><a href="how-we-recycle.html">How we recycle</a></li>
          <li><a href="safe-handling.html">Safe handling</a></li>
          <li><a href="safe-handling.html#accepted">What we take</a></li>
          <li><a href="faq.html">FAQ</a></li>
        </ul>
      </div>
      <div>
        <h4>Get in touch</h4>
        <ul>
          <li><a href="tel:0460555222" class="nw">0460 555 222</a></li>
          <li><a href="mailto:info@recycle.net.au">info@recycle.net.au</a></li>
          <li>116 Furner Avenue<br>North Geelong VIC 3215</li>
        </ul>
      </div>
    </div>
    <div class="foot-base">
      <p>&copy; <span data-year>2026</span> Vape Recyclers. Drop-off at Recycle North Geelong.</p>
      <p>If a vape is smoking, swelling or on fire, move away and call <strong class="nw">000</strong>.</p>
    </div>
  </div>
</footer>
<div class="m-cta" aria-label="Quick actions">
  <a class="btn btn-ghost" href="drop-off.html">Drop off</a>
  <a class="btn btn-mint" href="bins.html#request">Request a bin</a>
</div>'''

def page(title, desc, active, body, fname):
    canonical = SITE + ('/' if fname == 'index.html' else '/' + fname)
    full_title = title if active == 'home' else f'{title} | Vape Recyclers'
    return f'''<!doctype html>
<html lang="en-AU">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{full_title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canonical}">
<meta property="og:title" content="{full_title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{SITE}/img/og.png">
<meta name="theme-color" content="#08130F">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Space+Grotesk:wght@500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="css/site.css">
</head>
<body>
{header(active)}
<main id="main">
{body}
</main>
{FOOTER}
<script src="js/site.js" defer></script>
</body>
</html>
'''

def main():
    for f in sorted(SRC.glob('*.html')):
        lines = f.read_text().split('\n')
        title, desc, active = lines[0].strip(), lines[1].strip(), lines[2].strip()
        body = '\n'.join(lines[3:])
        body = re.sub(r'\{\{i:([a-z]+)\}\}', lambda m: ICONS[m.group(1)], body)
        # glue the last two words of short text blocks so no word sits alone on the last line
        body = re.sub(r'(?<=[A-Za-z,;)]) ([A-Za-z][A-Za-z\-]{0,13}[.!?]?)</(p|small)>', r'&nbsp;\1</\2>', body)
        (ROOT / f.name).write_text(page(title, desc, active, body, f.name))
        print('built', f.name)
    (ROOT / 'favicon.svg').write_text(LOGO.replace('aria-hidden="true"', 'xmlns="http://www.w3.org/2000/svg"'))

if __name__ == '__main__':
    main()
