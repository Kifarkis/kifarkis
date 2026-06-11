# -*- coding: utf-8 -*-
"""Generate the English kifarkis.com subpages. Reuses the SV build machinery
(CSS/JS/deco slice/helpers) by exec'ing build_subpages.py, then emits EN chrome
and translated copy. Run AFTER build_subpages.py logic executes (it runs on exec)."""

ns = {}
exec(open('/home/claude/build_subpages.py', encoding='utf-8').read(), ns)

CSS, JS, FORM_JS = ns['CSS'], ns['JS'], ns['FORM_JS']
DECO, DECO_CSS = ns['DECO'], ns['DECO_CSS']
COMPASS, ASTER = ns['COMPASS'], ns['ASTER']
sec, rep = ns['sec'], ns['rep']
priv_en_body = ns['priv_en_body']
SV_MAP = ns['SV_MAP']

FORM_JS_EN = FORM_JS.replace(
    "form.innerHTML = '<p class=\"kform-thanks\">Tack. Vi l\\u00e4ser och \\u00e5terkommer.</p>';",
    "form.innerHTML = '<p class=\"kform-thanks\">Thank you. We read and reply.</p>';")
assert FORM_JS_EN != FORM_JS, 'FORM_JS thanks string not replaced'

def cta_en(label, note, href='contact.html'):
    return f'''<div class="cta-block reveal">
      <a class="cta" href="{href}">{label} <span class="arr">\u2192</span></a>
      <p class="cta-note">{note}</p>
    </div>'''

def MM_OVERLAY_EN(active, self_file, sv_file):
    def cls(k):
        return ' nav-active' if k == active else ''
    return f"""  <button class="menu-btn" id="menuBtn" aria-label="Menu" aria-expanded="false">
    <span></span><span></span><span></span>
  </button>
</header>
<div class="mobile-menu" id="mobileMenu" aria-hidden="true">
  <a class="mm-link{cls('ai')}" href="automation.html"><span class="idx">01</span> AI automation</a>
  <a class="mm-link{cls('webb')}" href="web.html"><span class="idx">02</span> Web &amp; design</a>
  <a class="mm-link{cls('arbeten')}" href="work.html"><span class="idx">03</span> Work</a>
  <a class="mm-link{cls('om')}" href="about.html"><span class="idx">04</span> About</a>
  <a class="mm-link" href="contact.html"><span class="idx">05</span> Contact</a>
  <p class="mm-lang"><a href="{sv_file}">SV</a> / <a class="active" href="{self_file}">EN</a></p>
</div>"""

def header_en(active, self_file, sv_file):
    def cls(k):
        return ' class="nav-active"' if k == active else ''
    return f'''<header class="header" id="header">
  <a href="home.html" class="header-brand" aria-label="Kifarkis Design &amp; Automation">
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
    <a href="automation.html"{cls('ai')}>AI automation</a>
    <a href="web.html"{cls('webb')}>Web</a>
    <a href="work.html"{cls('arbeten')}>Work</a>
    <a href="about.html"{cls('om')}>About</a>
    <span class="lang"><a href="{sv_file}">SV</a> / <a class="active" href="{self_file}">EN</a></span>
  </nav>
''' + MM_OVERLAY_EN(active, self_file, sv_file)

FOOTER_EN = '''<footer class="footer" id="footer">
  <div class="meta">
    <span>Kifarkis Design &amp; Automation</span>
    <span class="sep full">\u00b7</span>
    <span class="full">Design &amp; Animation i Vellinge AB</span>
    <span class="sep full">\u00b7</span>
    <span class="full">Vellinge, Sweden</span>
    <span class="sep">\u00b7</span>
    <a href="privacy-policy.html" style="color:inherit; text-decoration:none;">Privacy</a>
  </div>
  <a class="footer-link" href="home.html">\u2190 Back</a>
</footer>'''

def page_en(filename, title, desc, active, smark, eyebrow, h1, lede, body, extra_js=''):
    sv_file = SV_MAP[filename]
    head_meta = f'''<!DOCTYPE html>
<html lang="en">
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
{header_en(active, filename, sv_file)}

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

{FOOTER_EN}

<script src="vendor/gsap.min.js"></script>
<script src="vendor/ScrollTrigger.min.js"></script>
<script>{JS}{extra_js}</script>
</body>
</html>'''
    doc = doc.replace('__DECOCSS__', DECO_CSS).replace('__COMPASS__', COMPASS).replace('__ASTER__', ASTER)
    out = f'/mnt/user-data/outputs/{filename}'
    open(out, 'w', encoding='utf-8').write(doc)
    return out

# \u2500\u2500\u2500 AI AUTOMATION (EN) \u2500\u2500\u2500
ai_body = '\n    '.join([
  '<p class="p-body reveal">Most automation projects do not fail in the technology. They fail in the selection. The wrong things get automated, for the wrong reasons, and a year later someone is maintaining a system nobody asked for. That is what we are here to avoid. Before we build anything we ask a simpler and harder question: should this be built at all?</p>',
  sec('The mapping', [
    'We never start with tools. We start with a walkthrough of how the work actually moves through the company, with the same four questions as always: where the work begins, what repeats, where errors pass unnoticed, and what exists but goes unused. The answers become a list of candidates. Most get crossed out. What remains is the small part that truly should be built, and then we also know why.'
  ]),
  sec('The way we work', [
    'We start small. The first version gets the least possible access and few users, and capabilities open at the pace you confirm they deserve it. It is slower on paper and faster in reality, because what gets built rarely needs to be redone.',
    'We also plan for AI being wrong sometimes. That is not a footnote, it is a design principle: where an error costs something, a human sits in the flow, and the system is built so it shows what was reviewed and by whom. You should be able to trust the result without having to believe in it.',
    'Once it is running we do not disappear. Automation that nobody maintains stops working quietly, so we update, monitor and fix in the background. If you work in a regulated industry, that is our home ground, ask us about it.'
  ]),
  rep('What it can look like', [
    'Every incoming contract is read the same day it lands. You get what matters. Terms, commitments, notice periods, and a mark at the places where a human needs to make the decision. The rest you never have to read.',
    'Every Monday a summary sits in your inbox: what your competitors said, released and filed for in the past week, from public sources. The analysis you would otherwise have paid an analyst for, every week, without hiring anyone.',
    'Ten years of documents that suddenly answer when spoken to. Ask the question, what did we promise the client, what did the report say last time, where does it say that. The answer comes with the source pointed out, instead of an hour of digging through folders.'
  ]),
  sec('And what we do not build', [
    'Sometimes the answer to the mapping is that nothing should be automated yet. Then we say so. An honest no costs us an engagement and saves you a year.'
  ]),
  cta_en('Book a free workflow audit',
      'Thirty minutes about your workflows. No slides, no salespeople, just the questions above, asked for real.')
])

# \u2500\u2500\u2500 SECURE OPERATIONS (EN) \u2500\u2500\u2500
drift_body = '\n    '.join([
  '<p class="p-body reveal">Operations is what nobody thinks about when everything works. That is the point. This is the page about the work that does not show, the updates that can never be missed, the backup that actually restores, and the eye on the systems when nobody else is watching.</p>',
  sec('What we take care of', [
    'The foundation first: the security of your Microsoft 365 environment, the computers, the permissions, the backups and the updates. Security is built into all of this when we do it, not an add-on, not a separate project, but the way we set things up from the start. It comes along from twenty-five years in other people\u2019s systems, many of them in industries where errors are not an option.',
    'For several of our clients we are the managed service provider with end-to-end responsibility for the whole stack, one place to call no matter what it concerns.',
    'And these days also the new part: the AI tools coming into the business, sanctioned and unsanctioned. We make sure that what is used is set up right, and that what nobody approved gets discovered before it becomes a problem. We have GenAI protection.'
  ]),
  sec('What never shows', [
    'Most of our work is noticed only through its absence. Ransomware stopped before it manages to encrypt anything, usually after someone clicked the wrong thing. An intrusion attempt that dies at the login. A disk replaced before it crashes. We work preventively so that alarms at three in the morning stay rare, not because we are good at putting out fires. Although we are that too.'
  ]),
  rep('The proof', [], agg='Most of our operations clients have been with us for over ten years. You do not change operations partner when everything just works.'),
  sec('And when something happens anyway', [
    'We do not promise that nothing happens. No honest provider does. We promise that it gets discovered early, contained quickly and fixed properly, and that you get to know what actually happened, not a version that sounds better.'
  ]),
  cta_en('Talk operations with us',
      'A review of how your environment is doing costs nothing. It is usually enough to know where you stand.')
])

# \u2500\u2500\u2500 WEB (EN) \u2500\u2500\u2500
webb_body = '\n    '.join([
  '<p class="p-body reveal">Most things on the web get redone at least every three years if not more often. Not because they stopped working, but because they were never built to last. The trend passed ... the platform grew heavy ... the person who built it left. We draw and build for a longer horizon than that.</p>',
  sec('What we do', [
    'Websites, brands and logos. Usually together, because it is in the whole that it holds together. An identity that survives being used ... a site that carries it without breaking ... and motion where it adds something, never just because we can.'
  ]),
  sec('How it lasts', [
    'Lasting is a technical decision as much as an aesthetic one. We build light and fast, without heavy platforms that demand constant care, and every graphic choice has to earn its place before it gets to stay. What does not add gets cut. What remains is something you do not need to redo every year, and that still feels right when the trend from the launch is gone.'
  ]),
  sec('Motion', [
    'Motion is part of the craft, not an effect we add at the end. It is used where it helps the eye understand the page, and removed where it only draws attention. You can see it working on this page right now.'
  ]),
  sec('The proof', [
    'The page you are reading is the example. The typography, the motion, the pace. Everything here is our own craft, and this is how we build for others. The oldest logo we have drawn is still in use after more than ten years. The only thing that has changed is the colour temperature.'
  ]),
  sec('And what we do not redo', [
    'Sometimes the answer is that your current web is good enough, that it needs adjusting, not replacing. Then we say so. Redoing everything is rarely the right answer, and never our default one.'
  ]),
  cta_en('Talk design with us',
      'Show us what you have. You get an honest assessment of what holds up and what does not.')
])

# \u2500\u2500\u2500 ABOUT (EN) \u2500\u2500\u2500
om_body = '\n    '.join([
  '<p class="p-body reveal">My name is David Kifarkis. I built my first computer as a child, got my first job in IT support, and have honestly never stopped doing either. The technology has changed shape many times since then. The curiosity is the same.</p>',
  sec('The road here', [
    'The career went via Telenor International in Oslo to biotechs in Sk\u00e5ne, in 2002 I started my own company, because I knew I could do this better. Life science came in early, as a consultant to smaller biotech companies in the region, and grew over the years into roles as Head of IT and IT Director, most recently at Camurus. At Zealand Pharma the company grew from seventy employees to over three hundred while I built up the IT function, from three people to seventeen. I learned how to scale, budget, procure and what comes when, both when it is early and when it is too late. I also learned why I am at my best as a consultant.',
    'So I went back. Not as a retreat, but as a choice. As a consultant I sit closer to the work and further from the politics, and that is where I am at my best and leave the biggest mark.'
  ]),
  sec('Why this', [
    'Small companies in regulated industries end up in a gap. Too small for the big providers, too regulated for the ordinary IT firm. At the same time they need IT, security, compliance and these days AI, preferably from someone who sees the whole instead of selling the parts separately. That gap is my home ground. The combination of GxP knowledge, hands-on IT and AI is unusual, and it is exactly what is needed there.'
  ]),
  sec('The family of brands', [
    'Kifarkis is design and automation. The sister brand MSET works with life science, validation and governance, where the demands are at their highest. And the IT support for Lund, Malm\u00f6 and Vellinge takes care of the everyday for companies nearby. Different names, same hands, same way of thinking.'
  ]),
  cta_en('Write to the right person',
      'info@kifarkis.com, or book half an hour. We start in your workflows, not in a sales presentation.')
])

# \u2500\u2500\u2500 CONTACT (EN) \u2500\u2500\u2500
kontakt_body = '\n    '.join([
  '<p class="p-body reveal">Tell us briefly what you do and where it chafes, and we come back with honest thoughts and a suggested next step.</p>',
  '''<div class="sec reveal">
      <form class="kform" id="kform" action="https://formspree.io/f/mvznbwzy" method="POST">
        <div class="kfield">
          <label for="kf-name">Name</label>
          <input type="text" id="kf-name" name="namn" required autocomplete="name">
        </div>
        <div class="kfield">
          <label for="kf-email">Email</label>
          <input type="email" id="kf-email" name="epost" required autocomplete="email">
        </div>
        <div class="kfield">
          <label for="kf-company">Company (optional)</label>
          <input type="text" id="kf-company" name="foretag" autocomplete="organization">
        </div>
        <div class="kfield">
          <label for="kf-msg">Message</label>
          <textarea id="kf-msg" name="meddelande" required placeholder="What do you do, and where does it chafe?"></textarea>
        </div>
        <input type="text" name="_gotcha" style="display:none" tabindex="-1" autocomplete="off">
        <div>
          <button type="submit" class="cta">Send <span class="arr">\u2192</span></button>
        </div>
        <p class="kform-error" id="kform-error">It did not go through just now. Email us directly: info@kifarkis.com</p>
        <p class="kform-small">Your details are used only to reply to you. No lists, no mailings. <a href="privacy-policy.html" style="color:inherit;">Privacy policy</a>.</p>
      </form>
    </div>''',
  sec('Prefer direct?', [
    '<a href="mailto:info@kifarkis.com" style="color:var(--ink); text-decoration:underline; text-decoration-color:var(--accent); text-underline-offset:3px;">info@kifarkis.com</a>'
  ]),
  sec('Location', [
    'Vellinge, Sk\u00e5ne. We work across the whole \u00d6resund region, and remotely where that fits better.'
  ]),
  sec('Want to start with something concrete?', [
    'Book a free workflow audit. Thirty minutes about your workflows, no slides, no salespeople.'
  ])
])

# \u2500\u2500\u2500 WORK (EN) \u2500\u2500\u2500
arbeten_body = '\n    '.join([
  '<p class="p-body reveal">Most of what we do right now is about implementing AI for real, safely and in the right order, at companies where errors are not an option. Here is a selection, described as it is.</p>',
  sec('Medical technology \u00b7 Completed implementation', [
    'Five users, from closed configuration to full rollout. One pilot user first, the rest once the pilot confirmed it works, then a workshop for the whole team. The central theme throughout: knowing when you can trust an answer, and when you cannot.'
  ]),
  sec('Contract development \u00b7 Ongoing', [
    'Workshops delivered, follow-up done. The most important discovery was not the AI but the infrastructure, the documents sat where the tools could not reach them. Now the foundation moves first, then the capabilities open. The right order saves a year of frustration.'
  ]),
  sec('Biotech \u00b7 Ongoing', [
    'Here we started at the other end, with the governance. Security hardening of the environment and a complete policy package for AI use, produced and anchored before broader access opens. One user has access today. The rest get it when the rules are in place, not before.'
  ]),
  sec('Listed company \u00b7 Ongoing', [
    'Five seats in an environment where everyone uses their own computers, which puts different demands on the configuration. Some capabilities are switched off on purpose. The client administers the memberships themselves, we own the platform responsibility. Clear roles, no surprises.'
  ]),
  sec('Managed services \u00b7 The whole stack', [
    'The longest work is the one that shows the least. For a number of companies we are the managed service provider with end-to-end responsibility. Microsoft 365, the computers, the permissions, the security, the backup and the support, the whole stack, one place to call. Most of those relationships have passed ten years. It is the work sample we are most proud of.'
  ]),
  sec('Design', [
    'And the design track? You are looking at it. The page you are reading is our own craft, and how we think is under <a href="web.html" style="color:var(--ink); text-decoration:underline; text-decoration-color:var(--accent); text-underline-offset:3px;">Design that lasts</a>.'
  ]),
  cta_en('Book a free workflow audit',
      'Thirty minutes about your workflows. We tell you honestly where AI belongs in your business.')
])

outs = []
outs.append(page_en('work.html', 'Ongoing work \u00b7 Kifarkis',
  'Anonymized AI implementations and managed services with end-to-end responsibility. No names, just the work.',
  'arbeten', None, 'Work', 'Ongoing work',
  'Our clients work in industries where discretion is part of the delivery. So no names here, just the work.', arbeten_body))

outs.append(page_en('automation.html', 'Automation worth building \u00b7 Kifarkis',
  'We build what gains from being built, and nothing more. AI automation for companies that take security seriously.',
  'ai', '\u00a701', '\u00a701 \u00b7 AI automation', 'Automation worth building',
  'We build what gains from being built, and nothing more.', ai_body))

outs.append(page_en('operations.html', 'Secure operations \u00b7 Kifarkis',
  'What we build should still be there, tomorrow, and the year after. Operations, security and vigilance in the background.',
  None, '\u00a703', '\u00a703 \u00b7 Secure operations', 'Secure operations',
  'What we build should still be there, tomorrow, and the year after.', drift_body))

outs.append(page_en('web.html', 'Design that lasts \u00b7 Kifarkis',
  'We do fewer things. They last longer. Web, brand and motion built to last.',
  'webb', '\u00a702', '\u00a702 \u00b7 Web &amp; design', 'Design that lasts',
  'We do fewer things. They last longer.', webb_body))

outs.append(page_en('about.html', 'About \u00b7 Kifarkis',
  'Twenty-five years in other people\u2019s systems. Kifarkis is at its core one person, and that is on purpose.',
  'om', None, 'About \u00b7 Vellinge, Sk\u00e5ne', 'Twenty-five years in other people\u2019s systems',
  'Kifarkis is at its core one person. That is on purpose.', om_body))

outs.append(page_en('contact.html', 'Contact \u00b7 Kifarkis',
  'Write to the right person. What you write here lands directly with the person who replies.',
  None, None, 'Contact', 'Write to the right person',
  'What you write here lands directly with the person who replies.', kontakt_body, extra_js=FORM_JS_EN))

# \u2500\u2500\u2500 PRIVACY (EN, regenerated with EN chrome; body copy unchanged) \u2500\u2500\u2500
outs.append(page_en('privacy-policy.html', 'Privacy Policy \u00b7 Kifarkis',
  'How Kifarkis Design & Automation collects, uses and protects personal data.',
  None, None, 'Legal', 'Privacy Policy',
  'How we collect, use and protect personal data.', priv_en_body))

# \u2500\u2500 validation \u2500\u2500
import os
print('generated (EN):')
for o in outs:
    s = open(o, encoding='utf-8').read()
    checks = {
        'size_kb': round(os.path.getsize(o)/1024),
        'style_balance': s.count('<style>') == 1 and s.count('</style>') == 1,
        'script_balance': s.count('<script') == s.count('</script>'),
        'div_balance': s.count('<div') == s.count('</div>'),
        'no_em_dash': '\u2014' not in s,
        'lang_en': '<html lang="en">' in s,
        'header': '<header class="header"' in s,
        'footer': '<footer class="footer"' in s,
        'spine': 'class="spine"' in s,
        'sv_link_back': s.count('>SV</a>') == 2,
    }
    print(' ', os.path.basename(o), checks)
