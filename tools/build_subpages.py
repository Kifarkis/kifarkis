# -*- coding: utf-8 -*-
"""Generate the five kifarkis.com subpages from one template + locked copy."""
import base64, re, html as H

def uri(p):
    # tolerate missing optional assets (legacy slim-deco glyphs no longer used)
    import os
    if not os.path.exists(p):
        return ''
    return 'data:image/png;base64,' + base64.b64encode(open(p,'rb').read()).decode()

COMPASS = uri('/home/claude/atmo-compass.png')   # optional, unused since full-deco swap
ASTER   = uri('/home/claude/atmo-aster.png')     # optional, unused since full-deco swap

CSS = r"""
  :root {
    --bg: #EFEAE0; --bg-warmer: #ECE5D3;
    --ink: #15120E; --ink-soft: #4A4239;
    --accent: #9C4A2A; --accent-bright: #E88B6A;
    --muted: #7D7365;
    --rule: #D6CEC0; --rule-light: #B5AC9F;
    --size-l:clamp(1.9rem,3vw,2.5rem); --size-m:clamp(1.15rem,1.7vw,1.45rem); --size-s:clamp(1rem,1.2vw,1.12rem);
    --bg-soot:#C4BCB3;
    --footer-h: 56px;
  }
  *, *::before, *::after { box-sizing: border-box; }
  html, body { margin: 0; padding: 0; }
  html { scroll-behavior: smooth; }
  body {
    background: var(--bg-soot); color: var(--ink);
    font-family: 'Instrument Sans', system-ui, sans-serif;
    -webkit-font-smoothing: antialiased;
    overflow-x: hidden;
    padding-bottom: var(--footer-h);
  }
  ::selection { background: var(--accent); color: var(--bg); }

  /* HEADER (locked) */
  .header {
    position: fixed; top: 0; left: 0; right: 0; z-index: 50;
    padding: 8px clamp(20px, 4vw, 56px);
    display: flex; align-items: center; justify-content: space-between;
    transition: background-color 0.4s ease, backdrop-filter 0.4s ease, border-color 0.4s ease, padding 0.3s ease;
    border-bottom: 1px solid transparent;
  }
  .header.scrolled {
    background-color: rgba(239, 234, 224, 0.35);
    backdrop-filter: saturate(180%) blur(14px);
    -webkit-backdrop-filter: saturate(180%) blur(14px);
    border-bottom-color: var(--rule);
    padding: 6px clamp(20px, 4vw, 56px);
  }
  .header-brand { display: flex; align-items: center; gap: 18px; text-decoration: none; color: var(--ink); transition: opacity 0.2s ease; }
  .header-brand:hover { opacity: 0.75; }
  .logo-mark { display: flex; align-items: stretch; gap: 6px; line-height: 0; }
  .logo-word { font-family: 'Fraunces', serif; font-size: 16px; font-weight: 500; letter-spacing: 0.02em; line-height: 1; writing-mode: vertical-rl; transform: rotate(180deg); color: var(--ink); padding: 1px 0; white-space: nowrap; }
  .logo-rule-stack { display: flex; flex-direction: column; align-items: center; gap: 3px; }
  .logo-lock { width: 13px; height: 16px; flex-shrink: 0; color: var(--ink); display: block; }
  .logo-rule { width: 1.5px; flex: 1; background: var(--accent); min-height: 12px; }
  .header-label { font-family: 'JetBrains Mono', monospace; font-size: 11px; letter-spacing: 0.18em; text-transform: uppercase; color: var(--ink); }
  @media (max-width: 540px) { .header-label { display: none; } }
  .header-nav { display: flex; gap: clamp(12px, 2.5vw, 28px); align-items: center; font-family: 'JetBrains Mono', monospace; font-size: 11px; letter-spacing: 0.16em; }
  .header-nav a { text-decoration: none; color: var(--ink); padding: 6px 0; transition: color 0.2s ease; }
  .header-nav a:hover { color: var(--accent); }
  .header-nav a.nav-active { color: var(--accent); }
  .header-nav .lang { color: var(--rule-light); padding-left: clamp(6px, 1.5vw, 14px); border-left: 1px solid var(--rule); }
  .header-nav .lang .active { color: var(--accent); }
  .header-nav .lang a { color: var(--muted); text-decoration: none; transition: color 0.2s ease; }
  .header-nav .lang a:hover { color: var(--accent); }
  .header-nav .lang a.active { color: var(--accent); }
  @media (max-width: 720px) { .header-nav a:not(.lang) { display: none; } .header-nav .lang a { display: inline; } }

  /* FIELD */
  .page-bg { position:fixed; inset:0; z-index:-2; pointer-events:none; background:var(--bg-soot); }
  .grain {
    position: fixed; inset: 0; pointer-events: none;
    opacity: 0.20; mix-blend-mode: multiply; z-index: 1;
    background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='180' height='180'><filter id='n'><feTurbulence baseFrequency='0.85' numOctaves='2'/></filter><rect width='100%25' height='100%25' filter='url(%23n)'/></svg>");
  }
  .page-deco { position:fixed; inset:0; z-index:-1; pointer-events:none; overflow:visible; }
__DECOCSS__
  @media (max-width:860px) { .page-deco .deco, .page-deco .ast { display:none; } .page-deco .atm-1, .page-deco .brush-1 { display:block; } }

  /* CONTENT GRID (same template as homepage stage2) */
  .stage2 {
    position:relative; display:grid;
    grid-template-columns:120px minmax(0,660px) 1fr;
    column-gap:clamp(24px,4vw,64px);
    max-width:1600px; margin:0 auto; padding:0 clamp(20px,4vw,56px);
  }
  .stage2 > .s2 { grid-column:2; position:relative; z-index:2; }
  .subpage { padding-top:clamp(170px,24vh,300px); padding-bottom:clamp(90px,13vh,150px); }
  .arrival-glow { position:absolute; z-index:0; top:clamp(40px,8vh,120px); right:-6%; width:min(42vw,580px); aspect-ratio:1/1.05; border-radius:50%; pointer-events:none; filter:blur(9px);
    background:radial-gradient(circle at 50% 42%, rgba(156,74,42,0.14), rgba(156,74,42,0.05) 46%, rgba(156,74,42,0) 70%); }
  .aw { display:inline-block; white-space:nowrap; }
  .al { display:inline-block; will-change:transform; }

  /* SPINE */
  .spine { position:absolute; width:1.5px; z-index:2; }
  .spine-track { position:absolute; inset:0; background:var(--rule); }
  .spine-fill { position:absolute; top:0; left:0; right:0; height:0; background:var(--accent); }
  .spine-dot { position:absolute; left:50%; top:0; width:7px; height:7px; border-radius:50%; background:var(--accent); transform:translate(-50%,-50%); box-shadow:0 0 0 4px rgba(156,74,42,0.12); }
  .smark { position:absolute; left:0; top:4px; width:9px; height:1.5px; background:var(--rule-light); display:block; }
  .smark i { position:absolute; left:-34px; top:-7px; font-style:normal; font-family:'JetBrains Mono',monospace; font-size:10px; letter-spacing:0.12em; color:var(--muted); }

  /* TEXT COMPONENTS (locked values) */
  .eyebrow { font-family:'JetBrains Mono',monospace; font-size:10px; letter-spacing:0.22em; text-transform:uppercase; color:var(--accent); margin:0 0 20px; }
  .p-title { font-family:'Fraunces',serif; font-weight:400; color:var(--ink); margin:0 0 12px; letter-spacing:-0.02em; line-height:1.06; font-size:var(--size-l); }
  .p-lede { font-family:'Fraunces',serif; font-style:italic; font-size:var(--size-m); color:var(--ink-soft); margin:0 0 22px; line-height:1.3; }
  .p-body { font-family:'Instrument Sans',sans-serif; font-size:var(--size-s); line-height:1.62; color:var(--ink-soft); margin:0; max-width:600px; }
  .p-body + .p-body { margin-top:14px; }
  .sec { margin-top:clamp(42px,6vh,68px); }
  .mlabel { display:block; font-family:'JetBrains Mono',monospace; font-size:10px; letter-spacing:0.22em; text-transform:uppercase; color:var(--accent); margin:0 0 12px; }
  .rep { margin-top:26px; padding-left:22px; border-left:2px solid var(--accent); max-width:600px; }
  .rep-frame { display:block; font-family:'JetBrains Mono',monospace; font-size:10px; letter-spacing:0.22em; text-transform:uppercase; color:var(--accent); margin-bottom:12px; }
  .rep .scene { font-family:'Instrument Sans',sans-serif; font-size:var(--size-s); line-height:1.56; color:var(--ink-soft); margin:0; }
  .rep .scene + .scene { margin-top:13px; }
  .rep .agg { font-family:'Fraunces',serif; font-size:var(--size-m); line-height:1.4; color:var(--ink); margin:0 0 13px; }
  .accent { color:var(--accent); font-style:italic; }

  /* CTA */
  .cta-block { margin-top:clamp(50px,8vh,84px); }
  .cta {
    display: inline-flex; align-items: center; gap: 10px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px; letter-spacing: 0.18em; text-transform: uppercase;
    text-decoration: none;
    padding: 16px 26px;
    transition: transform 0.2s ease, background 0.2s ease, color 0.2s ease;
    cursor: pointer;
    border: 1px solid var(--ink);
    background: var(--ink); color: var(--bg);
  }
  .cta:hover { transform: translateY(-2px); background: var(--accent); border-color: var(--accent); }
  .cta .arr { font-size: 14px; transition: transform 0.3s cubic-bezier(0.2, 0.8, 0.2, 1); }
  .cta:hover .arr { transform: translateX(4px); }
  .cta-note { font-family:'Instrument Sans',sans-serif; font-size:var(--size-s); line-height:1.6; color:var(--muted); margin:16px 0 0; max-width:600px; }

  /* FORM (Kontakt) */
  .kform { margin-top:26px; max-width:600px; display:grid; gap:18px; }
  .kfield { display:grid; gap:8px; }
  .kfield label { font-family:'JetBrains Mono',monospace; font-size:10px; letter-spacing:0.22em; text-transform:uppercase; color:var(--muted); }
  .kfield input, .kfield textarea {
    background: transparent; border: 1px solid var(--rule);
    font-family:'Instrument Sans',sans-serif; font-size:var(--size-s); color:var(--ink);
    padding: 12px 14px; border-radius: 0; width: 100%;
    transition: border-color 0.2s ease;
  }
  .kfield input:focus, .kfield textarea:focus { outline: none; border-color: var(--accent); }
  .kfield textarea { min-height: 150px; resize: vertical; line-height: 1.55; }
  .kform-small { font-family:'JetBrains Mono',monospace; font-size:10px; letter-spacing:0.12em; color:var(--muted); margin:0; line-height:1.7; }
  .kform-thanks { font-family:'Fraunces',serif; font-size:var(--size-m); color:var(--ink); margin:10px 0 0; }
  .kform-error { font-family:'Instrument Sans',sans-serif; font-size:var(--size-s); color:var(--accent); margin:0; display:none; }

  /* MOBILE MENU */
  .menu-btn { display:none; background:none; border:none; cursor:pointer; padding:8px 0 8px 8px; z-index:70; }
  .menu-btn span { display:block; width:22px; height:1.5px; background:var(--ink); margin:5px 0; transition:transform 0.3s ease, opacity 0.3s ease; }
  .menu-btn.open span:nth-child(1) { transform:translateY(6.5px) rotate(45deg); }
  .menu-btn.open span:nth-child(2) { opacity:0; }
  .menu-btn.open span:nth-child(3) { transform:translateY(-6.5px) rotate(-45deg); }
  @media (max-width:720px) { .menu-btn { display:block; } }
  .mobile-menu {
    position:fixed; inset:0; z-index:60;
    background:rgba(196,188,179,0.96);
    backdrop-filter:saturate(160%) blur(16px);
    -webkit-backdrop-filter:saturate(160%) blur(16px);
    display:flex; flex-direction:column; justify-content:center;
    padding:0 clamp(28px,8vw,56px);
    opacity:0; pointer-events:none; transition:opacity 0.35s ease;
  }
  .mobile-menu::after { content:""; position:absolute; inset:0; pointer-events:none; opacity:0.20; mix-blend-mode:multiply; background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='180' height='180'><filter id='n'><feTurbulence baseFrequency='0.85' numOctaves='2'/></filter><rect width='100%25' height='100%25' filter='url(%23n)'/></svg>"); }
  .mobile-menu.open { opacity:1; pointer-events:auto; }
  .mm-link { font-family:'Fraunces',serif; font-size:clamp(1.2rem,4.8vw,1.55rem); color:var(--ink); text-decoration:none; padding:10px 0; display:flex; align-items:baseline; gap:16px; border-bottom:1px solid var(--rule); }
  .mm-link .idx { font-family:'JetBrains Mono',monospace; font-size:10px; color:var(--accent); letter-spacing:0.12em; }
  .mm-link.nav-active { color:var(--accent); }
  .mm-lang { margin-top:24px; font-family:'JetBrains Mono',monospace; font-size:11px; letter-spacing:0.16em; color:var(--rule-light); }
  .mm-lang .active { color:var(--accent); }
  .mm-lang a { color:var(--muted); text-decoration:none; }
  .mm-lang a.active { color:var(--accent); }
  body.menu-open { overflow:hidden; }

  /* FOOTER (locked) */
  .footer {
    position: fixed; bottom: 0; left: 0; right: 0;
    z-index: 50;
    height: var(--footer-h);
    padding: 0 clamp(20px, 4vw, 56px);
    display: flex; align-items: center; justify-content: space-between;
    gap: 12px;
    background: rgba(239, 234, 224, 0.85);
    backdrop-filter: saturate(180%) blur(14px);
    -webkit-backdrop-filter: saturate(180%) blur(14px);
    border-top: 1px solid var(--rule);
  }
  .footer .meta {
    font-family: 'JetBrains Mono', ui-monospace, monospace;
    font-size: 10px; letter-spacing: 0.18em; text-transform: uppercase;
    color: var(--muted); line-height: 1.4;
    overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
    min-width: 0;
  }
  .footer .meta .sep { color: var(--rule-light); margin: 0 6px; }
  .footer-link {
    font-family: 'JetBrains Mono', ui-monospace, monospace;
    font-size: 10px; letter-spacing: 0.2em; text-transform: uppercase;
    color: var(--muted); text-decoration: none;
    transition: color 0.2s ease;
    flex-shrink: 0;
    cursor: pointer; background: none; border: none; padding: 0;
  }
  .footer-link:hover { color: var(--accent); }
  @media (max-width: 720px) { .footer .meta .full { display: none; } }

  /* mobile */
  @media (max-width:860px) {
    .stage2 { grid-template-columns:1fr; }
    .stage2 > .s2 { grid-column:1; }
    .spine { display:none; }
  }
"""

JS = r"""
  // mobile menu
  (function () {
    var btn = document.getElementById('menuBtn');
    var menu = document.getElementById('mobileMenu');
    if (!btn || !menu) return;
    function setOpen(open) {
      btn.classList.toggle('open', open);
      menu.classList.toggle('open', open);
      document.body.classList.toggle('menu-open', open);
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
      menu.setAttribute('aria-hidden', open ? 'false' : 'true');
    }
    btn.addEventListener('click', function () { setOpen(!menu.classList.contains('open')); });
    menu.querySelectorAll('a').forEach(function (a) { a.addEventListener('click', function () { setOpen(false); }); });
  })();

  // header scrolled state
  (function() {
    const header = document.getElementById('header');
    if (!header) return;
    function update() { header.classList.toggle('scrolled', window.scrollY > 12); }
    update();
    window.addEventListener('scroll', update, { passive: true });
  })();

  // mouse parallax + scroll drift (same loop as the homepage)
  (function() {
    const layers = document.querySelectorAll('.parallax');
    if (!layers.length) return;
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

    let mouseX = 0, mouseY = 0;
    let targetX = 0, targetY = 0;

    function tick() {
      mouseX += (targetX - mouseX) * 0.05;
      mouseY += (targetY - mouseY) * 0.05;
      layers.forEach(el => {
        const depth = parseFloat(el.dataset.depth || '1');
        const sy = window.scrollY || window.pageYOffset || 0;
        const x = mouseX * depth * -28;
        const y = mouseY * depth * -28 + sy * depth * -0.045;
        el.style.translate = x + 'px ' + y + 'px';
      });
      requestAnimationFrame(tick);
    }

    document.addEventListener('mousemove', (e) => {
      const w = window.innerWidth, h = window.innerHeight;
      targetX = (e.clientX / w - 0.5) * 2;
      targetY = (e.clientY / h - 0.5) * 2;
    });
    tick();
  })();

  // compact arrival: eyebrow -> title letters -> lede, with the glow warming in
  (function() {
    if (!window.gsap) return;
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    var eyebrow = document.querySelector('.arr-eyebrow');
    var title = document.querySelector('.arr-title');
    var lede = document.querySelector('.arr-lede');
    var glow = document.querySelector('.arrival-glow');
    if (!title) return;
    // split title into word spans of letter spans (kerning-safe wrapping)
    var words = title.textContent.split(' ');
    title.textContent = '';
    words.forEach(function (w, wi) {
      var ws = document.createElement('span'); ws.className = 'aw';
      for (var i = 0; i < w.length; i++) {
        var ls = document.createElement('span'); ls.className = 'al';
        ls.textContent = w[i]; ws.appendChild(ls);
      }
      title.appendChild(ws);
      if (wi < words.length - 1) title.appendChild(document.createTextNode(' '));
    });
    var letters = title.querySelectorAll('.al');
    var tl = gsap.timeline();
    if (glow) tl.fromTo(glow, { opacity: 0 }, { opacity: 1, duration: 1.6, ease: 'power1.out' }, 0);
    if (eyebrow) tl.fromTo(eyebrow, { y: 10, opacity: 0 }, { y: 0, opacity: 1, duration: 0.6, ease: 'power2.out' }, 0);
    tl.fromTo(letters, { y: '0.42em', opacity: 0 },
      { y: 0, opacity: 1, duration: 0.55, ease: 'power3.out', stagger: 0.022 }, 0.22);
    if (lede) tl.fromTo(lede, { y: 14, opacity: 0 }, { y: 0, opacity: 1, duration: 0.7, ease: 'power2.out' }, '-=0.3');
    var first = document.querySelector('.s2 .reveal');
    if (first) {
      first.dataset.claimed = '1';
      tl.fromTo(first, { y: 18, opacity: 0 }, { y: 0, opacity: 1, duration: 0.7, ease: 'power2.out' }, '-=0.35');
    }
  })();

  // scroll reveals (GSAP; content stays visible if GSAP is absent or reduced motion)
  (function() {
    if (!window.gsap || !window.ScrollTrigger) return;
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    gsap.registerPlugin(ScrollTrigger);
    gsap.utils.toArray('.reveal').forEach(function (el) {
      if (el.dataset.claimed) return;
      gsap.fromTo(el, { y: 24, opacity: 0 }, {
        y: 0, opacity: 1, duration: 0.9, ease: 'power2.out',
        scrollTrigger: { trigger: el, start: 'top 88%', toggleActions: 'play none none reverse' }
      });
    });
  })();

  // spine: direct, deterministic fill + dot (same approach as the homepage)
  (function() {
    const spine = document.querySelector('.spine');
    const content = document.querySelector('.stage2 > .s2');
    if (!spine || !content) return;
    const fill = spine.querySelector('.spine-fill');
    const dot = spine.querySelector('.spine-dot');
    let topDoc = 0, bottomDoc = 0, railH = 0;
    function measure() {
      const sy = window.pageYOffset;
      const r = content.getBoundingClientRect();
      const hostEl = spine.offsetParent;
      const host = hostEl ? hostEl.getBoundingClientRect() : { left: 0, top: -sy };
      topDoc = r.top + sy; bottomDoc = r.bottom + sy;
      railH = Math.max(0, bottomDoc - topDoc);
      spine.style.left = (r.left - host.left - 26) + 'px';
      spine.style.top = (r.top - host.top) + 'px';
      spine.style.height = railH + 'px';
    }
    function progress() {
      const vh = window.innerHeight;
      const startS = topDoc - 0.68 * vh;
      const endS = bottomDoc - vh;
      const range = endS - startS;
      if (range <= 0) return 1;
      const p = (window.pageYOffset - startS) / range;
      return p < 0 ? 0 : (p > 1 ? 1 : p);
    }
    let curr = 0, targ = 0, raf = null;
    function render() {
      curr += (targ - curr) * 0.14;
      if (Math.abs(targ - curr) < 0.0006) curr = targ;
      const h = railH * curr;
      if (fill) fill.style.height = h + 'px';
      if (dot) dot.style.top = h + 'px';
      raf = (curr !== targ) ? requestAnimationFrame(render) : null;
    }
    function sync(re) {
      if (re) measure();
      targ = progress();
      if (raf === null) raf = requestAnimationFrame(render);
    }
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      measure();
      if (fill) fill.style.height = railH + 'px';
      if (dot) dot.style.top = railH + 'px';
      return;
    }
    measure();
    curr = targ = progress();
    const h0 = railH * curr;
    if (fill) fill.style.height = h0 + 'px';
    if (dot) dot.style.top = h0 + 'px';
    window.addEventListener('scroll', function () { sync(false); }, { passive: true });
    let rt;
    function onResize() { clearTimeout(rt); rt = setTimeout(function () { sync(true); }, 80); }
    window.addEventListener('resize', onResize);
    document.addEventListener('fullscreenchange', onResize);
    if (window.ResizeObserver) { try { new ResizeObserver(onResize).observe(document.documentElement); } catch (e) {} }
    window.addEventListener('load', function () { sync(true); });
  })();
"""

FORM_JS = r"""
  // Kontakt form via Formspree (AJAX, inline confirmation)
  (function() {
    const form = document.getElementById('kform');
    if (!form) return;
    const err = document.getElementById('kform-error');
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      const btn = form.querySelector('button[type=submit]');
      if (btn) btn.disabled = true;
      fetch(form.action, {
        method: 'POST',
        body: new FormData(form),
        headers: { 'Accept': 'application/json' }
      }).then(function (r) {
        if (r.ok) {
          form.innerHTML = '<p class="kform-thanks">Tack. Vi l\u00e4ser och \u00e5terkommer.</p>';
        } else {
          if (err) err.style.display = 'block';
          if (btn) btn.disabled = false;
        }
      }).catch(function () {
        if (err) err.style.display = 'block';
        if (btn) btn.disabled = false;
      });
    });
  })();
"""

def MM_OVERLAY(active, self_file, en_file):
    def cls(k):
        return ' nav-active' if k == active else ''
    return f"""  <button class="menu-btn" id="menuBtn" aria-label="Meny" aria-expanded="false">
    <span></span><span></span><span></span>
  </button>
</header>
<div class="mobile-menu" id="mobileMenu" aria-hidden="true">
  <a class="mm-link{cls('ai')}" href="ai-automation.html"><span class="idx">01</span> AI-automation</a>
  <a class="mm-link{cls('webb')}" href="webb.html"><span class="idx">02</span> Webb &amp; design</a>
  <a class="mm-link{cls('arbeten')}" href="arbeten.html"><span class="idx">03</span> Arbeten</a>
  <a class="mm-link{cls('om')}" href="om.html"><span class="idx">04</span> Om</a>
  <a class="mm-link" href="kontakt.html"><span class="idx">05</span> Kontakt</a>
  <a class="mm-link{cls('toolbox')}" href="toolbox.html"><span class="idx">06</span> Toolbox</a>
  <p class="mm-lang"><a class="active" href="{self_file}">SV</a> / <a href="{en_file}">EN</a></p>
</div>"""

def header(active, self_file, en_file):
    def cls(k):
        return ' class="nav-active"' if k == active else ''
    return f'''<header class="header" id="header">
  <a href="index.html" class="header-brand" aria-label="Kifarkis Design &amp; Automation">
    <span class="logo-mark" aria-hidden="true">
      <span class="logo-word">kifarkis</span>
      <span class="logo-rule-stack">
        <svg class="logo-lock" viewBox="0 0 44 56" aria-hidden="true">
          <path d="M 12 24 L 12 16 A 10 10 0 0 1 32 16 L 32 24" stroke="currentColor" stroke-width="3" fill="none" stroke-linecap="round"/>
          <rect x="6" y="22" width="32" height="28" rx="2" fill="var(--accent)"/>
          <circle cx="22" cy="34" r="2.2" fill="var(--bg)"/>
          <rect x="20.9" y="34" width="2.2" height="6" fill="var(--bg)"/>
        </svg>
        <span class="logo-rule"></span>
      </span>
    </span>
    <span class="header-label">Design &amp; Automation</span>
  </a>
  <nav class="header-nav">
    <a href="ai-automation.html"{cls('ai')}>AI-automation</a>
    <a href="webb.html"{cls('webb')}>Webb</a>
    <a href="arbeten.html"{cls('arbeten')}>Arbeten</a>
    <a href="om.html"{cls('om')}>Om</a>
    <a href="toolbox.html"{cls('toolbox')}>Toolbox</a>
    <span class="lang"><a class="active" href="{self_file}">SV</a> / <a href="{en_file}">EN</a></span>
  </nav>
''' + MM_OVERLAY(active, self_file, en_file)

FOOTER = '''<footer class="footer" id="footer">
  <div class="meta">
    <span>Kifarkis Design &amp; Automation</span>
    <span class="sep full">\u00b7</span>
    <span class="full">Design &amp; Animation i Vellinge AB</span>
    <span class="sep full">\u00b7</span>
    <span class="full">Vellinge, Sverige</span>
    <span class="sep">\u00b7</span>
    <a href="privacy.html" style="color:inherit; text-decoration:none;">Integritet</a>
  </div>
  <a class="footer-link" href="index.html">\u2190 Tillbaka</a>
</footer>'''

_home = open('/home/claude/site-linked.html', encoding='utf-8').read()
_ds = _home.index('  .deco {')
_de = _home.index('  .eyebrow {')
DECO_CSS = _home[_ds:_de].rstrip()
_hs = _home.index('<div class="page-deco">')
_he = _home.index('\n</div>', _home.index('data-depth="1.30"')) + len('\n</div>')
DECO_HTML = _home[_hs:_he]
DECO = '<div class="page-bg"></div>\n' + DECO_HTML + '\n<div class="grain" aria-hidden="true"></div>' 

def sec(label, paras):
    ps = '\n      '.join(f'<p class="p-body">{p}</p>' for p in paras)
    return f'''<div class="sec reveal">
      <span class="mlabel">{label}</span>
      {ps}
    </div>'''

def rep(label, scenes, agg=None):
    inner = f'<span class="rep-frame">{label}</span>\n      '
    if agg:
        inner += f'<p class="agg">{agg}</p>\n      '
    inner += '\n      '.join(f'<p class="scene">{s}</p>' for s in scenes)
    return f'''<div class="sec reveal">
      <div class="rep">
      {inner}
      </div>
    </div>'''

def cta(label, note, href='kontakt.html'):
    return f'''<div class="cta-block reveal">
      <a class="cta" href="{href}">{label} <span class="arr">\u2192</span></a>
      <p class="cta-note">{note}</p>
    </div>'''

EN_MAP = {
    'index.html': 'home.html',
    'ai-automation.html': 'automation.html',
    'webb.html': 'web.html',
    'drift.html': 'operations.html',
    'arbeten.html': 'work.html',
    'om.html': 'about.html',
    'kontakt.html': 'contact.html',
    'privacy.html': 'privacy-policy.html',
    'toolbox.html': 'toolbox.html',
}
SV_MAP = {v: k for k, v in EN_MAP.items()}

def page(filename, title, desc, active, smark, eyebrow, h1, lede, body, extra_js=''):
    en_file = EN_MAP[filename]
    head_meta = f'''<!DOCTYPE html>
<html lang="sv">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='-6 0 56 56'%3E%3Cpath d='M 12 24 L 12 16 A 10 10 0 0 1 32 16 L 32 24' stroke='%2315120E' stroke-width='3' fill='none' stroke-linecap='round'/%3E%3Crect x='6' y='22' width='32' height='28' rx='2' fill='%239C4A2A'/%3E%3Ccircle cx='22' cy='34' r='2.2' fill='%23EFEAE0'/%3E%3Crect x='20.9' y='34' width='2.2' height='6' fill='%23EFEAE0'/%3E%3C/svg%3E">
<link rel="stylesheet" href="fonts/fonts.css">
<style>{CSS}</style>
</head>'''
    smark_html = f'<span class="smark"><i>{smark}</i></span>' if smark else ''
    doc = f'''{head_meta}
<body>
{DECO}
{header(active, filename, en_file)}

<main class="stage2 subpage">
  <div class="arrival-glow" aria-hidden="true"></div>
  <div class="spine" aria-hidden="true">
    <div class="spine-track"></div>
    <div class="spine-fill"></div>
    <div class="spine-dot"></div>
    {smark_html}
  </div>
  <article class="s2">
    <p class="eyebrow arr-eyebrow">{eyebrow}</p>
    <h1 class="p-title arr-title">{h1}</h1>
    <p class="p-lede arr-lede">{lede}</p>
    {body}
  </article>
</main>

{FOOTER}

<script src="vendor/gsap.min.js"></script>
<script src="vendor/ScrollTrigger.min.js"></script>
<script>{JS}{extra_js}</script>
</body>
</html>'''
    doc = doc.replace('__DECOCSS__', DECO_CSS).replace('__COMPASS__', COMPASS).replace('__ASTER__', ASTER)
    out = f'/mnt/user-data/outputs/{filename}'
    open(out, 'w', encoding='utf-8').write(doc)
    return out

E = '\u2026'  # not used; David writes spaced dots " ... " literally

# ─────────────────────────── AI-AUTOMATION ───────────────────────────
ai_body = '\n    '.join([
  '<p class="p-body reveal">De flesta automationsprojekt misslyckas inte i tekniken. De misslyckas i urvalet. Fel saker automatiseras, av fel sk\u00e4l, och ett \u00e5r senare underh\u00e5ller n\u00e5gon ett system som ingen bad om. Det \u00e4r det vi \u00e4r till f\u00f6r att undvika. Innan vi bygger n\u00e5gonting st\u00e4ller vi en enklare och sv\u00e5rare fr\u00e5ga: b\u00f6r det h\u00e4r byggas alls?</p>',
  sec('Kartl\u00e4ggningen', [
    'Vi b\u00f6rjar aldrig med verktyg. Vi b\u00f6rjar med en genomg\u00e5ng av hur arbetet faktiskt r\u00f6r sig genom f\u00f6retaget, med samma fyra fr\u00e5gor som alltid: var arbetet b\u00f6rjar, vad som upprepas, var fel obem\u00e4rkt passerar, och vad som finns men inte anv\u00e4nds. Svaren blir en lista med kandidater. De flesta stryks. Det som blir kvar \u00e4r det lilla som verkligen b\u00f6r byggas, och d\u00e5 vet vi ocks\u00e5 varf\u00f6r.'
  ]),
  sec('Arbetsg\u00e5ngen', [
    'Vi b\u00f6rjar i liten skala. Den f\u00f6rsta versionen f\u00e5r minsta m\u00f6jliga \u00e5tkomst och f\u00e5 anv\u00e4ndare, och f\u00f6rm\u00e5gor \u00f6ppnas i den takt ni bekr\u00e4ftar att de f\u00f6rtj\u00e4nar det. Det \u00e4r l\u00e5ngsammare p\u00e5 pappret och snabbare i verkligheten, f\u00f6r det som byggs beh\u00f6ver s\u00e4llan g\u00f6ras om.',
    'Vi planerar ocks\u00e5 f\u00f6r att AI har fel ibland. Det \u00e4r inte en fotnot, det \u00e4r en designprincip: d\u00e4r ett fel kostar n\u00e5got sitter en m\u00e4nniska i fl\u00f6det, och systemet \u00e4r byggt s\u00e5 att det syns vad som granskats av vem. Ni ska kunna lita p\u00e5 resultatet utan att beh\u00f6va tro p\u00e5 det.',
    'N\u00e4r det \u00e4r i drift f\u00f6rsvinner vi inte. Automation som ingen underh\u00e5ller slutar fungera tyst, s\u00e5 vi uppdaterar, \u00f6vervakar och \u00e5tg\u00e4rdar i bakgrunden. Arbetar ni i en reglerad bransch \u00e4r det v\u00e5r hemmaplan, fr\u00e5ga oss om det.'
  ]),
  rep('S\u00e5 h\u00e4r kan det se ut', [
    'Varje inkommande avtal l\u00e4ses samma dag det landar. Du f\u00e5r det som spelar roll. Villkor, \u00e5taganden, upps\u00e4gningstider, samt en markering vid de st\u00e4llen d\u00e4r en m\u00e4nniska beh\u00f6ver fatta beslutet. Resten slipper du l\u00e4sa.',
    'Varje m\u00e5ndag ligger en sammanst\u00e4llning i din inkorg: vad konkurrenterna sagt, sl\u00e4ppt och ans\u00f6kt om den g\u00e5ngna veckan, ur offentliga k\u00e4llor. Den analys du annars hade betalat en analytiker f\u00f6r, varje vecka, utan att anst\u00e4lla n\u00e5gon.',
    'Tio \u00e5rs dokument som pl\u00f6tsligt svarar p\u00e5 tilltal. St\u00e4ll fr\u00e5gan, vad lovade vi kunden, vad sa rapporten senast, var st\u00e5r det. Svaret kommer med k\u00e4llan utpekad, i st\u00e4llet f\u00f6r en timmes letande i mappar.'
  ]),
  sec('Och det vi inte bygger', [
    'Ibland \u00e4r svaret p\u00e5 kartl\u00e4ggningen att ingenting b\u00f6r automatiseras \u00e4nnu. D\u00e5 s\u00e4ger vi det. Ett \u00e4rligt nej kostar oss ett uppdrag och sparar er ett \u00e5r.'
  ]),
  cta('Boka kostnadsfri workflow-audit',
      'Trettio minuter om era arbetsfl\u00f6den. Inga slides, inga s\u00e4ljare, bara fr\u00e5gorna ovan, st\u00e4llda p\u00e5 riktigt.')
])

# ─────────────────────────── SÄKER DRIFT ───────────────────────────
drift_body = '\n    '.join([
  '<p class="p-body reveal">Drift \u00e4r det ingen som t\u00e4nker p\u00e5 n\u00e4r allt fungerar. Det \u00e4r po\u00e4ngen. Det h\u00e4r \u00e4r sidan om arbetet som inte syns, uppdateringarna som aldrig f\u00e5r missas, s\u00e4kerhetskopian som faktiskt g\u00e5r att \u00e5terst\u00e4lla, och blicken p\u00e5 systemen n\u00e4r ingen annan tittar.</p>',
  sec('Vad vi tar hand om', [
    'Grunden f\u00f6rst: S\u00e4kerheten i er Microsoft 365-milj\u00f6, datorerna, beh\u00f6righeterna, s\u00e4kerhetskopiorna och uppdateringarna. S\u00e4kerheten \u00e4r inbyggd i allt detta n\u00e4r vi g\u00f6r det, inte ett tillval, inte ett separat projekt, utan s\u00e4ttet vi s\u00e4tter upp saker p\u00e5 fr\u00e5n b\u00f6rjan. Det f\u00f6ljer med fr\u00e5n tjugofem \u00e5r i andras system, m\u00e5nga av dem i branscher d\u00e4r fel inte \u00e4r ett alternativ.',
    'F\u00f6r flera av v\u00e5ra kunder \u00e4r vi managed service provider med helhetsansvar f\u00f6r hela stacken, ett st\u00e4lle att ringa oavsett vad det g\u00e4ller.',
    'Och numera \u00e4ven det nya: AI-verktygen som tas in i verksamheten, till\u00e5tna och otill\u00e5tna. Vi ser till att det som anv\u00e4nds \u00e4r uppsatt r\u00e4tt, och att det som ingen godk\u00e4nt uppt\u00e4cks innan det blir ett problem. Vi har GenAI-skydd.'
  ]),
  sec('Det som aldrig syns', [
    'Det mesta av v\u00e5rt arbete m\u00e4rks bara genom sin fr\u00e5nvaro. Ransomware som stoppas innan den hinner kryptera n\u00e5got, oftast efter att n\u00e5gon klickat p\u00e5 fel sak. Ett intr\u00e5ngsf\u00f6rs\u00f6k som d\u00f6r i inloggningen. En disk som byts innan den kraschar. Vi jobbar f\u00f6rebyggande f\u00f6r att larm klockan tre p\u00e5 natten ska f\u00f6rbli ovanliga, inte f\u00f6r att vi \u00e4r bra p\u00e5 att sl\u00e4cka br\u00e4nder. \u00c4ven om vi \u00e4r det ocks\u00e5.'
  ]),
  rep('Beviset', [], agg='De flesta av v\u00e5ra driftkunder har varit med oss i \u00f6ver tio \u00e5r. Man byter inte driftpartner n\u00e4r allt bara fungerar.'),
  sec('Och n\u00e4r n\u00e5got \u00e4nd\u00e5 h\u00e4nder', [
    'Vi lovar inte att inget h\u00e4nder. Ingen \u00e4rlig leverant\u00f6r g\u00f6r det. Vi lovar att det uppt\u00e4cks tidigt, begr\u00e4nsas snabbt och \u00e5tg\u00e4rdas ordentligt, och att ni f\u00e5r veta vad som h\u00e4nde p\u00e5 riktigt, inte en version som l\u00e5ter b\u00e4ttre.'
  ]),
  cta('Prata drift med oss',
      'En genomg\u00e5ng av hur er milj\u00f6 m\u00e5r kostar ingenting. Det brukar vara nog f\u00f6r att veta var ni st\u00e5r.')
])

# ─────────────────────────── WEBB ───────────────────────────
webb_body = '\n    '.join([
  '<p class="p-body reveal">Det mesta p\u00e5 webben g\u00f6rs om minst vart tredje \u00e5r om inte oftare. Inte f\u00f6r att det slutat fungera, utan f\u00f6r att det aldrig var byggt att h\u00e5lla. Trenden gick \u00f6ver ... plattformen blev tung ... den som byggde f\u00f6rsvann. Vi ritar och bygger f\u00f6r en l\u00e4ngre horisont \u00e4n s\u00e5.</p>',
  sec('Vad vi g\u00f6r', [
    'Webbplatser, varum\u00e4rken och logotyper. Oftast tillsammans, f\u00f6r det \u00e4r i helheten det h\u00e5ller ihop. En identitet som t\u00e5l att anv\u00e4ndas ... en sajt som b\u00e4r den utan att g\u00e5 s\u00f6nder ... och r\u00f6relse d\u00e4r den tillf\u00f6r n\u00e5got, aldrig bara f\u00f6r att vi kan.'
  ]),
  sec('Hur det h\u00e5ller', [
    'Att best\u00e5 \u00e4r ett tekniskt beslut lika mycket som ett estetiskt. Vi bygger l\u00e4tt och snabbt, utan tunga plattformar som kr\u00e4ver st\u00e4ndig omsorg, och varje grafiskt val ska f\u00f6rtj\u00e4na sin plats innan det f\u00e5r vara kvar. Det som inte tillf\u00f6r stryks. Kvar blir n\u00e5got ni inte beh\u00f6ver g\u00f6ra om varje \u00e5r, och som fortfarande k\u00e4nns r\u00e4tt n\u00e4r trenden fr\u00e5n lanseringen \u00e4r borta.'
  ]),
  sec('R\u00f6relse', [
    'R\u00f6relse \u00e4r en del av hantverket, inte en effekt vi l\u00e4gger p\u00e5 i slutet. Den anv\u00e4nds d\u00e4r den hj\u00e4lper \u00f6gat att f\u00f6rst\u00e5 sidan, och tas bort d\u00e4r den bara drar uppm\u00e4rksamhet. Du ser den arbeta p\u00e5 den h\u00e4r sidan just nu.'
  ]),
  sec('Beviset', [
    'Sidan du l\u00e4ser \u00e4r exemplet. Typografin, r\u00f6relsen, tempot. Allt h\u00e4r \u00e4r v\u00e5rt eget hantverk, och det \u00e4r s\u00e5 h\u00e4r vi bygger \u00e5t andra. Den \u00e4ldsta logotypen vi ritat \u00e4r fortfarande i bruk efter mer \u00e4n tio \u00e5r. Det enda som \u00e4ndrats \u00e4r f\u00e4rgtemperaturen.'
  ]),
  sec('Och det vi inte g\u00f6r om', [
    'Ibland \u00e4r svaret att er nuvarande webb duger, att den beh\u00f6ver justeras, inte ers\u00e4ttas. D\u00e5 s\u00e4ger vi det. Att g\u00f6ra om allt \u00e4r s\u00e4llan r\u00e4tt svar, och aldrig v\u00e5rt standardsvar.'
  ]),
  cta('Prata design med oss',
      'Visa oss vad ni har. Ni f\u00e5r en \u00e4rlig bed\u00f6mning av vad som h\u00e5ller och vad som inte g\u00f6r det.')
])

# ─────────────────────────── OM ───────────────────────────
om_body = '\n    '.join([
  '<p class="p-body reveal">Jag heter David Kifarkis. Jag byggde min f\u00f6rsta dator som barn, fick mitt f\u00f6rsta jobb i IT-support, och har i \u00e4rlighetens namn aldrig slutat med n\u00e5gotdera. Tekniken har bytt skepnad m\u00e5nga g\u00e5nger sedan dess. Nyfikenheten \u00e4r densamma.</p>',
  sec('V\u00e4gen hit', [
    'Karri\u00e4ren gick via Telenor International i Oslo till biotechbolagen i Sk\u00e5ne, 2002 startade jag eget, f\u00f6r jag visste att jag kunde g\u00f6ra det h\u00e4r b\u00e4ttre. Life science kom in tidigt, som konsult \u00e5t mindre biotechbolag i regionen, och v\u00e4xte med \u00e5ren till roller som IT-chef och IT Director, senast p\u00e5 Camurus. P\u00e5 Zealand Pharma v\u00e4xte bolaget fr\u00e5n sjuttio anst\u00e4llda till \u00f6ver trehundra medan jag byggde upp IT-funktionen, fr\u00e5n tre personer till sjutton. Jag l\u00e4rde mig hur man skalar, budgeterar, upphandlar och vad som kommer n\u00e4r, b\u00e5de n\u00e4r det \u00e4r tidigt och n\u00e4r det \u00e4r f\u00f6r sent. Jag l\u00e4rde mig ocks\u00e5 varf\u00f6r jag trivs b\u00e4st som konsult.',
    'S\u00e5 jag gick tillbaka. Inte som retr\u00e4tt, utan som val. Som konsult sitter jag n\u00e4rmare arbetet och l\u00e4ngre fr\u00e5n politiken, och det \u00e4r d\u00e4r jag trivs b\u00e4st och ger st\u00f6rst avtryck.'
  ]),
  sec('Varf\u00f6r det h\u00e4r', [
    'Sm\u00e5 bolag i reglerade branscher hamnar i ett glapp. F\u00f6r sm\u00e5 f\u00f6r de stora leverant\u00f6rerna, f\u00f6r reglerade f\u00f6r den vanliga IT-firman. Samtidigt beh\u00f6ver de IT, s\u00e4kerhet, regelefterlevnad och numera AI, och helst fr\u00e5n n\u00e5gon som ser helheten i st\u00e4llet f\u00f6r att s\u00e4lja delarna var f\u00f6r sig. Det glappet \u00e4r min hemmaplan. Kombinationen av GxP-kunskap, hands-on IT och AI \u00e4r ovanlig, och det \u00e4r precis den som beh\u00f6vs d\u00e4r.'
  ]),
  sec('Familjen av varum\u00e4rken', [
    'Kifarkis \u00e4r design och automation. Systervarum\u00e4rket MSET arbetar med life science, validering och styrning, d\u00e4r kraven \u00e4r som h\u00f6gst. Och IT-supporten f\u00f6r Lund, Malm\u00f6 och Vellinge tar hand om vardagen f\u00f6r f\u00f6retag i n\u00e4romr\u00e5det. Olika namn, samma h\u00e4nder, samma s\u00e4tt att t\u00e4nka.'
  ]),
  cta('Skriv till r\u00e4tt person',
      'info@kifarkis.com, eller boka en halvtimme. Vi b\u00f6rjar i era arbetsfl\u00f6den, inte i en s\u00e4ljpresentation.')
])

# ─────────────────────────── KONTAKT ───────────────────────────
kontakt_body = '\n    '.join([
  '<p class="p-body reveal">Ber\u00e4tta kort vad ni g\u00f6r och var det skaver, s\u00e5 \u00e5terkommer vi med \u00e4rliga tankar och ett f\u00f6rslag p\u00e5 n\u00e4sta steg.</p>',
  '''<div class="sec reveal">
      <form class="kform" id="kform" action="https://formspree.io/f/mvznbwzy" method="POST">
        <div class="kfield">
          <label for="kf-name">Namn</label>
          <input type="text" id="kf-name" name="namn" required autocomplete="name">
        </div>
        <div class="kfield">
          <label for="kf-email">E-post</label>
          <input type="email" id="kf-email" name="epost" required autocomplete="email">
        </div>
        <div class="kfield">
          <label for="kf-company">F\u00f6retag (valfritt)</label>
          <input type="text" id="kf-company" name="foretag" autocomplete="organization">
        </div>
        <div class="kfield">
          <label for="kf-msg">Meddelande</label>
          <textarea id="kf-msg" name="meddelande" required placeholder="Vad g\u00f6r ni, och var skaver det?"></textarea>
        </div>
        <input type="text" name="_gotcha" style="display:none" tabindex="-1" autocomplete="off">
        <div>
          <button type="submit" class="cta">Skicka <span class="arr">\u2192</span></button>
        </div>
        <p class="kform-error" id="kform-error">Det gick inte att skicka just nu. Mejla oss direkt: info@kifarkis.com</p>
        <p class="kform-small">Uppgifterna anv\u00e4nds bara f\u00f6r att svara dig. Inga listor, inga utskick. <a href="privacy.html" style="color:inherit;">Integritetspolicy</a>.</p>
      </form>
    </div>''',
  sec('Hellre direkt?', [
    '<a href="mailto:info@kifarkis.com" style="color:var(--ink); text-decoration:underline; text-decoration-color:var(--accent); text-underline-offset:3px;">info@kifarkis.com</a>'
  ]),
  sec('Plats', [
    'Vellinge, Sk\u00e5ne. Vi arbetar i hela \u00d6resundsregionen, och p\u00e5 distans d\u00e4r det passar b\u00e4ttre.'
  ]),
  sec('Vill ni b\u00f6rja konkret?', [
    'Boka en kostnadsfri workflow-audit. Trettio minuter om era arbetsfl\u00f6den, inga slides, inga s\u00e4ljare.'
  ])
])

# ─────────────────────────── ARBETEN ───────────────────────────
arbeten_body = '\n    '.join([
  '<p class="p-body reveal">Det mesta vi g\u00f6r just nu handlar om att implementera AI p\u00e5 riktigt, s\u00e4kert och i r\u00e4tt ordning, hos bolag d\u00e4r fel inte \u00e4r ett alternativ. H\u00e4r \u00e4r ett urval, beskrivet som det \u00e4r.</p>',
  sec('Medicinteknik \u00b7 Genomf\u00f6rd implementation', [
    'Fem anv\u00e4ndare, fr\u00e5n st\u00e4ngd konfiguration till full utrullning. En pilotanv\u00e4ndare f\u00f6rst, resten n\u00e4r piloten bekr\u00e4ftat att det fungerar, d\u00e4refter workshop f\u00f6r hela teamet. Det centrala temat genom allt: att veta n\u00e4r man kan lita p\u00e5 ett svar, och n\u00e4r man inte kan.'
  ]),
  sec('Kontraktsutveckling \u00b7 P\u00e5g\u00e5ende', [
    'Workshoppar utf\u00f6rda, uppf\u00f6ljning klar. Den viktigaste uppt\u00e4ckten var inte AI:n utan infrastrukturen, dokumenten l\u00e5g d\u00e4r verktygen inte kunde n\u00e5 dem. Nu flyttas grunden f\u00f6rst, sedan \u00f6ppnas f\u00f6rm\u00e5gorna. R\u00e4tt ordning sparar ett \u00e5r av frustration.'
  ]),
  sec('Biotech \u00b7 P\u00e5g\u00e5ende', [
    'H\u00e4r b\u00f6rjade vi i andra \u00e4nden, med styrningen. S\u00e4kerhetsh\u00e4rdning av milj\u00f6n och ett komplett policypaket f\u00f6r AI-anv\u00e4ndning, framtaget och f\u00f6rankrat innan bredare \u00e5tkomst \u00f6ppnas. En anv\u00e4ndare har tillg\u00e5ng idag. Resten f\u00e5r det n\u00e4r reglerna \u00e4r p\u00e5 plats, inte f\u00f6re.'
  ]),
  sec('Noterat bolag \u00b7 P\u00e5g\u00e5ende', [
    'Fem platser i en milj\u00f6 d\u00e4r alla anv\u00e4nder egna datorer, vilket st\u00e4ller andra krav p\u00e5 konfigurationen. Vissa f\u00f6rm\u00e5gor \u00e4r avst\u00e4ngda med flit. Kunden administrerar medlemskapen sj\u00e4lv, vi \u00e4ger plattformsansvaret. Tydliga roller, inga \u00f6verraskningar.'
  ]),
  sec('F\u00f6rvaltning \u00b7 Hela stacken', [
    'Det l\u00e4ngsta arbetet \u00e4r det som syns minst. F\u00f6r ett antal bolag \u00e4r vi managed service provider med helhetsansvar. Microsoft 365, datorerna, beh\u00f6righeterna, s\u00e4kerheten, backupen och supporten, hela stacken, ett st\u00e4lle att ringa. De flesta av de relationerna har passerat tio \u00e5r. Det \u00e4r det arbetsprov vi \u00e4r mest stolta \u00f6ver.'
  ]),
  sec('Design', [
    'Och designsp\u00e5ret? Du tittar p\u00e5 det. Sidan du l\u00e4ser \u00e4r v\u00e5rt eget hantverk, och hur vi t\u00e4nker finns under <a href="webb.html" style="color:var(--ink); text-decoration:underline; text-decoration-color:var(--accent); text-underline-offset:3px;">Design som best\u00e5r</a>.'
  ]),
  cta('Boka kostnadsfri workflow-audit',
      'Trettio minuter om era arbetsfl\u00f6den. Vi s\u00e4ger \u00e4rligt vart AI h\u00f6r hemma hos er.')
])

outs = []
outs.append(page('arbeten.html', 'P\u00e5g\u00e5ende arbete \u00b7 Kifarkis',
  'Anonymiserade AI-implementationer och f\u00f6rvaltning med helhetsansvar. Inga namn, bara arbetet.',
  'arbeten', None, 'Arbeten', 'P\u00e5g\u00e5ende arbete',
  'V\u00e5ra kunder arbetar i branscher d\u00e4r diskretion ing\u00e5r i leveransen. D\u00e4rf\u00f6r inga namn h\u00e4r, bara arbetet.', arbeten_body))
outs.append(page('ai-automation.html', 'Automation v\u00e4rd att bygga \u00b7 Kifarkis',
  'Vi bygger det som tj\u00e4nar p\u00e5 att byggas, och inget mer. AI-automation f\u00f6r f\u00f6retag som tar s\u00e4kerhet p\u00e5 allvar.',
  'ai', '\u00a701', '\u00a701 \u00b7 AI-automation', 'Automation v\u00e4rd att bygga',
  'Vi bygger det som tj\u00e4nar p\u00e5 att byggas, och inget mer.', ai_body))

outs.append(page('drift.html', 'S\u00e4ker drift \u00b7 Kifarkis',
  'Det vi bygger ska finnas kvar, i morgon, och \u00e5ret d\u00e4rp\u00e5. Drift, s\u00e4kerhet och vaksamhet i bakgrunden.',
  None, '\u00a703', '\u00a703 \u00b7 S\u00e4ker drift', 'S\u00e4ker drift',
  'Det vi bygger ska finnas kvar, i morgon, och \u00e5ret d\u00e4rp\u00e5.', drift_body))

outs.append(page('webb.html', 'Design som best\u00e5r \u00b7 Kifarkis',
  'Vi g\u00f6r f\u00e4rre saker. De h\u00e5ller l\u00e4ngre. Webb, varum\u00e4rke och r\u00f6relse byggda f\u00f6r att best\u00e5.',
  'webb', '\u00a702', '\u00a702 \u00b7 Webb &amp; design', 'Design som best\u00e5r',
  'Vi g\u00f6r f\u00e4rre saker. De h\u00e5ller l\u00e4ngre.', webb_body))

outs.append(page('om.html', 'Om \u00b7 Kifarkis',
  'Tjugofem \u00e5r i andras system. Kifarkis \u00e4r i grunden en person, och det \u00e4r med flit.',
  'om', None, 'Om \u00b7 Vellinge, Sk\u00e5ne', 'Tjugofem \u00e5r i andras system',
  'Kifarkis \u00e4r i grunden en person. Det \u00e4r med flit.', om_body))

outs.append(page('kontakt.html', 'Kontakt \u00b7 Kifarkis',
  'Skriv till r\u00e4tt person. Det du skriver h\u00e4r landar direkt hos den som svarar.',
  None, None, 'Kontakt', 'Skriv till r\u00e4tt person',
  'Det du skriver h\u00e4r landar direkt hos den som svarar.', kontakt_body, extra_js=FORM_JS))



# ─────────────────────────── PRIVACY (SV display, EN binding) ───────────────────────────
def legal(label, paras):
    return sec(label, paras)

priv_sv_body = '\n    '.join([
  '<p class="p-body reveal">Den engelska versionen av denna policy (<a href="privacy-policy.html" style="color:inherit;">Privacy Policy</a>) \u00e4r det juridiskt bindande dokumentet. Den svenska texten tillhandah\u00e5lls som en l\u00e4sarservice. Policyn g\u00e4ller webbplatsen kifarkis.com och v\u00e5ra kunduppdrag. Senast uppdaterad: 11 juni 2026.</p>',
  legal('1 \u00b7 Vem vi \u00e4r', [
    'Personuppgiftsansvarig \u00e4r Design & Animation i Vellinge AB, Vellinge, Sverige, som driver varum\u00e4rket Kifarkis Design & Automation. Kontakt: info@kifarkis.com. Vi behandlar personuppgifter enligt EU:s dataskyddsf\u00f6rordning (GDPR) och svensk dataskyddslag.'
  ]),
  legal('2 \u00b7 Vad vi samlar in', [
    'Via kontaktformul\u00e4ret: namn, e-postadress, f\u00f6retag (frivilligt) och ditt meddelande. Inget annat. Vi beg\u00e4r aldrig mer \u00e4n vad som beh\u00f6vs f\u00f6r att svara dig.',
    'I kunduppdrag kan vi behandla personuppgifter f\u00f6r din r\u00e4kning. D\u00e5 styrs behandlingen av ett separat personuppgiftsbitr\u00e4desavtal, och vi behandlar bara uppgifterna f\u00f6r de \u00e4ndam\u00e5l som avtalats.',
    'V\u00e5r webbplats levereras av GitHub Pages (GitHub, Inc., USA), som f\u00f6r tekniska loggar f\u00f6r s\u00e4kerhet och drift (IP-adress, webbl\u00e4sare, tidpunkt). Vi anv\u00e4nder Google Search Console f\u00f6r aggregerad s\u00f6kstatistik, som inte sp\u00e5rar enskilda bes\u00f6kare. Vi anv\u00e4nder ingen beteendesp\u00e5rning, ingen Google Analytics, ingen annonspixel.'
  ]),
  legal('3 \u00b7 R\u00e4ttslig grund och anv\u00e4ndning', [
    'Vi behandlar uppgifter med st\u00f6d av ditt samtycke (n\u00e4r du skickar formul\u00e4ret), avtal (n\u00e4r vi levererar ett uppdrag), ber\u00e4ttigat intresse (s\u00e4kerhetsloggar) eller r\u00e4ttslig f\u00f6rpliktelse (till exempel bokf\u00f6ring). Uppgifterna anv\u00e4nds bara f\u00f6r det \u00e4ndam\u00e5l de l\u00e4mnades f\u00f6r. Vi s\u00e4ljer aldrig personuppgifter och anv\u00e4nder dem inte f\u00f6r marknadsf\u00f6ring du inte bett om.'
  ]),
  legal('4 \u00b7 Personuppgiftsbitr\u00e4den', [
    'Formul\u00e4rsvar hanteras av Formspree Inc. (USA), som vidarebefordrar dem till v\u00e5r e-post och \u00e4r bundet av EU:s standardavtalsklausuler. Vi raderar rutinm\u00e4ssigt inskickade meddelanden fr\u00e5n Formspree n\u00e4r de \u00e4r hanterade. E-postkorrespondens lagras hos v\u00e5r e-postleverant\u00f6r s\u00e5 l\u00e4nge relationen \u00e4r aktiv plus lagstadgad tid. Webbplatsen levereras av GitHub Pages (GitHub, Inc., USA). Vid \u00f6verf\u00f6ring utanf\u00f6r EES anv\u00e4nds EU:s standardavtalsklausuler och kompletterande skydds\u00e5tg\u00e4rder.'
  ]),
  legal('5 \u00b7 Lagringstider', [
    'Formul\u00e4rsvar: upp till 12 m\u00e5nader efter senaste kontakt, om ingen kundrelation inletts. Uppdragsdata: uppdragstiden plus 7 \u00e5r enligt bokf\u00f6ringslagen, eller enligt bitr\u00e4desavtalet. Serverloggar: kort teknisk lagring hos v\u00e5rt webbhotell. Nyhetsbrev och marknadslistor: finns inte, vi driver inga.'
  ]),
  legal('6 \u00b7 Dina r\u00e4ttigheter', [
    'Du har r\u00e4tt till tillg\u00e5ng, r\u00e4ttelse, radering, begr\u00e4nsning, dataportabilitet och inv\u00e4ndning, samt r\u00e4tt att \u00e5terkalla samtycke. Mejla info@kifarkis.com s\u00e5 svarar vi inom 30 dagar, utan kostnad f\u00f6r en f\u00f6rsta beg\u00e4ran. Du kan ocks\u00e5 klaga hos Integritetsskyddsmyndigheten (imy.se).'
  ]),
  legal('7 \u00b7 S\u00e4kerhet och cookies', [
    'Vi skyddar uppgifter med kryptering under \u00f6verf\u00f6ring, \u00e5tkomstkontroller och ett arbetss\u00e4tt format av tjugofem \u00e5r i IT-s\u00e4kerhet. Vid en incident som medf\u00f6r risk f\u00f6r dina r\u00e4ttigheter anm\u00e4ler vi till Integritetsskyddsmyndigheten inom 72 timmar och informerar ber\u00f6rda utan on\u00f6digt dr\u00f6jsm\u00e5l. Webbplatsen s\u00e4tter inga sp\u00e5rningscookies. Webbplatsen och tj\u00e4nsterna riktar sig till f\u00f6retag, vi samlar inte medvetet in uppgifter om barn under 16 \u00e5r.'
  ]),
  legal('8 \u00b7 \u00c4ndringar och fr\u00e5gor', [
    'Vid v\u00e4sentliga \u00e4ndringar av policyn informerar vi aktiva kunder via e-post. Undrar du n\u00e5got, mejla info@kifarkis.com med \u00e4mnesraden Integritetsfr\u00e5ga s\u00e5 f\u00f6rklarar vi g\u00e4rna.'
  ]),
])

priv_en_body = '\n    '.join([
  '<p class="p-body reveal">This English version is the legally binding document. The Swedish translation (<a href="privacy.html" style="color:inherit;">Integritetspolicy</a>) is provided as a reader service. The policy covers the website kifarkis.com and our client engagements. Last updated: 11 June 2026.</p>',
  legal('1 \u00b7 Who we are', [
    'The data controller is Design & Animation i Vellinge AB, Vellinge, Sweden, operating the brand Kifarkis Design & Automation. Contact: info@kifarkis.com. We process personal data under the EU General Data Protection Regulation (GDPR) and the Swedish Data Protection Act.'
  ]),
  legal('2 \u00b7 What we collect', [
    'Through the contact form: your name, email address, company (optional) and your message. Nothing else. We never ask for more than what is needed to reply to you.',
    'During client engagements we may process personal data on your behalf. That processing is governed by a separate Data Processing Agreement, and we process the data only for the purposes agreed there.',
    'Our host, GitHub Pages (GitHub, Inc., USA), keeps technical logs for security and operations (IP address, browser, timestamp). We use Google Search Console for aggregated search statistics, which does not track individual visitors. We use no behavioural tracking, no Google Analytics, no advertising pixels.'
  ]),
  legal('3 \u00b7 Legal basis and use', [
    'We process data based on your consent (when you submit the form), contract (when delivering an engagement), legitimate interest (security logs) or legal obligation (accounting, for example). Data is used only for the purpose it was given for. We never sell personal data and never use it for marketing you did not ask for.'
  ]),
  legal('4 \u00b7 Processors', [
    'Form submissions are handled by Formspree Inc. (USA), which forwards them to our email and is bound by the EU Standard Contractual Clauses. We routinely delete submissions from Formspree once actioned. Email correspondence is stored with our email provider for as long as the relationship is active plus any statutory period. The website is served by GitHub Pages (GitHub, Inc., USA). Transfers outside the EEA rely on the EU Standard Contractual Clauses and supplementary safeguards.'
  ]),
  legal('5 \u00b7 Retention', [
    'Form submissions: up to 12 months after last contact, unless a client relationship has started. Engagement data: the duration of the engagement plus 7 years under Swedish accounting law, or as specified in the Data Processing Agreement. Server logs: brief technical retention with our host. Newsletters and marketing lists: none, we do not operate any.'
  ]),
  legal('6 \u00b7 Your rights', [
    'You have the right of access, rectification, erasure, restriction, data portability and objection, and the right to withdraw consent. Email info@kifarkis.com and we respond within 30 days, free of charge for a first request. You may also lodge a complaint with the Swedish data protection authority, Integritetsskyddsmyndigheten (imy.se).'
  ]),
  legal('7 \u00b7 Security and cookies', [
    'We protect data with encryption in transit, access controls and working habits shaped by twenty-five years in IT security. If an incident puts your rights at risk, we notify the Swedish data protection authority within 72 hours and inform those affected without undue delay. This website sets no tracking cookies. The site and services are aimed at businesses, and we do not knowingly collect data about children under 16.'
  ]),
  legal('8 \u00b7 Changes and questions', [
    'For material changes to this policy we notify active clients by email. If anything is unclear, email info@kifarkis.com with the subject line Privacy enquiry and we will gladly explain.'
  ]),
])

outs.append(page('privacy.html', 'Integritetspolicy \u00b7 Kifarkis',
  'Hur Kifarkis Design & Automation samlar in, anv\u00e4nder och skyddar personuppgifter.',
  None, None, 'Juridik', 'Integritetspolicy',
  'S\u00e5 samlar vi in, anv\u00e4nder och skyddar personuppgifter.', priv_sv_body))

# privacy-en.html is generated by build_en.py (EN chrome)

# ── validation ──
import os
print('generated:')
for o in outs:
    s = open(o, encoding='utf-8').read()
    checks = {
        'size_kb': round(os.path.getsize(o)/1024),
        'style_balance': s.count('<style>') == 1 and s.count('</style>') == 1,
        'script_balance': s.count('<script') == s.count('</script>'),
        'div_balance': s.count('<div') == s.count('</div>'),
        'no_em_dash': '\u2014' not in s,
        'header': '<header class="header"' in s,
        'footer': '<footer class="footer"' in s,
        'spine': 'class="spine"' in s,
        'reveals': s.count('class="reveal"') + s.count(' reveal"'),
    }
    print(' ', os.path.basename(o), checks)
