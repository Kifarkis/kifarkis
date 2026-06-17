# -*- coding: utf-8 -*-
"""Homepage builder.
Step 1: patch canonical SV homepage (site-linked.html) -> functional lang switch,
        publish as index.html.
Step 2: generate home.html from the patched SV via asserted
        literal replacements (count-verified, nothing silently missed)."""

PATH = '/home/claude/site-linked.html'
s = open(PATH, encoding='utf-8').read()

def rep1(text, old, new, n=1, label=''):
    c = text.count(old)
    assert c == n, f'{label or old[:60]!r}: expected {n}, found {c}'
    return text.replace(old, new)

# ─────────────── STEP 1 · SV PATCH (idempotent guard) ───────────────
if '<a class="active" href="index.html">SV</a>' not in s:
    # CSS: lang anchors (desktop)
    s = rep1(s, "  .header-nav .lang .active { color: var(--accent); }",
"""  .header-nav .lang .active { color: var(--accent); }
  .header-nav .lang a { color: var(--muted); text-decoration: none; transition: color 0.2s ease; }
  .header-nav .lang a:hover { color: var(--accent); }
  .header-nav .lang a.active { color: var(--accent); }""", 1, 'lang css')

    s = rep1(s, "  @media (max-width: 720px) { .header-nav a:not(.lang) { display: none; } }",
             "  @media (max-width: 720px) { .header-nav a:not(.lang) { display: none; } .header-nav .lang a { display: inline; } }",
             1, '720px css')

    s = rep1(s, "  .mm-lang .active { color:var(--accent); }",
"""  .mm-lang .active { color:var(--accent); }
  .mm-lang a { color:var(--muted); text-decoration:none; }
  .mm-lang a.active { color:var(--accent); }""", 1, 'mm-lang css')

    # markup: desktop + mobile lang
    s = rep1(s, '<span class="lang"><span class="active">SV</span> / EN</span>',
             '<span class="lang"><a class="active" href="index.html">SV</a> / <a href="home.html">EN</a></span>',
             1, 'desktop lang')
    s = rep1(s, '<p class="mm-lang"><span class="active">SV</span> / EN</p>',
             '<p class="mm-lang"><a class="active" href="index.html">SV</a> / <a href="home.html">EN</a></p>',
             1, 'mobile lang')

    open(PATH, 'w', encoding='utf-8').write(s)
open('/mnt/user-data/outputs/index.html', 'w', encoding='utf-8').write(s)
print('SV homepage patched + published')

# ─────────────── Toolbox nav item (idempotent, runs regardless of patch state) ───────────────
# Self-guarding so it works whether the canonical is the pre-launch or the
# already-patched version, and never double-inserts. Label is language-neutral,
# so the same markup serves both index.html (SV) and home.html (EN).
if 'href="toolbox.html"' not in s:
    s = rep1(s, '<a href="om.html">Om</a>',
             '<a href="om.html">Om</a>\n    <a href="toolbox.html">Toolbox</a>',
             1, 'desktop toolbox')
    s = rep1(s, '<a class="mm-link" href="kontakt.html"><span class="idx">05</span> Kontakt</a>',
             '<a class="mm-link" href="kontakt.html"><span class="idx">05</span> Kontakt</a>\n  <a class="mm-link" href="toolbox.html"><span class="idx">06</span> Toolbox</a>',
             1, 'mobile toolbox')
    open(PATH, 'w', encoding='utf-8').write(s)
    open('/mnt/user-data/outputs/index.html', 'w', encoding='utf-8').write(s)
    print('Toolbox nav item inserted')
else:
    print('Toolbox nav item already present, skipped')

# ─────────────── STEP 2 · EN HOMEPAGE ───────────────
e = s

# document language
e = rep1(e, '<html lang="sv">', '<html lang="en">')
e = rep1(e, '<meta name="description" content="AI-automation, webb och säker drift för företag som tar säkerhet på allvar. Vi bygger det som bör byggas, och inget mer. Vellinge, Skåne.">', '<meta name="description" content="AI automation, web and secure operations for companies that take security seriously. We build what should be built, and nothing more. Vellinge, Sweden.">')

# lang switch flips
e = rep1(e, '<span class="lang"><a class="active" href="index.html">SV</a> / <a href="home.html">EN</a></span>',
         '<span class="lang"><a href="index.html">SV</a> / <a class="active" href="home.html">EN</a></span>')
e = rep1(e, '<p class="mm-lang"><a class="active" href="index.html">SV</a> / <a href="home.html">EN</a></p>',
         '<p class="mm-lang"><a href="index.html">SV</a> / <a class="active" href="home.html">EN</a></p>')

# desktop nav
e = rep1(e, '<a href="ai-automation.html">AI-automation</a>', '<a href="automation.html">AI automation</a>')
e = rep1(e, '<a href="webb.html">Webb</a>', '<a href="web.html">Web</a>')
e = rep1(e, '<a href="arbeten.html">Arbeten</a>', '<a href="work.html">Work</a>')
e = rep1(e, '<a href="om.html">Om</a>', '<a href="about.html">About</a>')

# mobile menu
e = rep1(e, 'aria-label="Meny"', 'aria-label="Menu"')
e = rep1(e, '<a class="mm-link" href="ai-automation.html"><span class="idx">01</span> AI-automation</a>',
         '<a class="mm-link" href="automation.html"><span class="idx">01</span> AI automation</a>')
e = rep1(e, '<a class="mm-link" href="webb.html"><span class="idx">02</span> Webb &amp; design</a>',
         '<a class="mm-link" href="web.html"><span class="idx">02</span> Web &amp; design</a>')
e = rep1(e, '<a class="mm-link" href="arbeten.html"><span class="idx">03</span> Arbeten</a>',
         '<a class="mm-link" href="work.html"><span class="idx">03</span> Work</a>')
e = rep1(e, '<a class="mm-link" href="om.html"><span class="idx">04</span> Om</a>',
         '<a class="mm-link" href="about.html"><span class="idx">04</span> About</a>')
e = rep1(e, '<a class="mm-link" href="kontakt.html"><span class="idx">05</span> Kontakt</a>',
         '<a class="mm-link" href="contact.html"><span class="idx">05</span> Contact</a>')

# hero
e = rep1(e, '<span>25 års erfarenhet</span>', '<span>25 years of experience</span>')
e = rep1(e, '<span>klar · väntar</span>', '<span>done · waiting</span>')
e = rep1(e, '<a class="cta" href="kontakt.html">Boka kostnadsfri workflow-audit <span class="arr">→</span></a>',
         '<a class="cta" href="contact.html">Book a free workflow audit <span class="arr">→</span></a>')
e = rep1(e, '<a class="cta secondary" href="arbeten.html">Se arbeten <span class="arr">→</span></a>',
         '<a class="cta secondary" href="work.html">See our work <span class="arr">→</span></a>')
e = rep1(e, 'från en faktisk automation', 'from an actual automation')
e = rep1(e, '<span>Scrolla</span>', '<span>Scroll</span>')

# ─── §00 MANIFESTO (kan/bör → can/should; the em-dash beat is the lone copy exception, kept) ───
e = rep1(e, '<p>Jag har jobbat med andras system i tjugofem år. Det har lärt mig att den viktiga frågan sällan är om något <span class="accent">kan</span> automatiseras — utan om det <span class="accent">bör</span>. Det är skillnaden som blivit mitt arbete.</p>',
         '<p>I have worked in other people\u2019s systems for twenty-five years. It has taught me that the important question is rarely whether something <span class="accent">can</span> be automated — but whether it <span class="accent">should</span>. That difference has become my work.</p>')
e = rep1(e, '<p class="method-lead">Vi tittar på arbetsflöden med fyra frågor:</p>',
         '<p class="method-lead">We look at workflows with four questions:</p>')
e = rep1(e, '<li><span class="qn">01</span><span>var arbetet börjar</span></li>',
         '<li><span class="qn">01</span><span>where the work begins</span></li>')
e = rep1(e, '<li><span class="qn">02</span><span>vad som upprepas</span></li>',
         '<li><span class="qn">02</span><span>what repeats</span></li>')
e = rep1(e, '<li><span class="qn">03</span><span>var fel obemärkt passerar</span></li>',
         '<li><span class="qn">03</span><span>where errors pass unnoticed</span></li>')
e = rep1(e, '<li><span class="qn">04</span><span>vad som finns men inte används</span></li>',
         '<li><span class="qn">04</span><span>what exists but goes unused</span></li>')
e = rep1(e, '<p class="method-tail">Svaren är inte automationer. De är kandidater. Sedan frågar vi vilka av dem som tjänar på automation, och vilka som ska lämnas som de är.</p>',
         '<p class="method-tail">The answers are not automations. They are candidates. Then we ask which of them gain from automation, and which should be left as they are.</p>')
e = rep1(e, '<p>Det är där jag arbetar, i gränsen mellan vad som <span class="accent">kan</span> och vad som <span class="accent">bör</span>. Om du tänker likadant, då skriver du till rätt person.</p>',
         '<p>That is where I work, on the line between what <span class="accent">can</span> and what <span class="accent">should</span>. If you think the same way, you are writing to the right person.</p>')

# ─── §01 AUTOMATION ───
e = rep1(e, '<h3 class="p-title">Automation värd att bygga</h3>', '<h3 class="p-title">Automation worth building</h3>')
e = rep1(e, '<p class="p-lede">Vi bygger det som tjänar på att byggas, och inget mer.</p>',
         '<p class="p-lede">We build what gains from being built, and nothing more.</p>')
e = rep1(e, '<p class="p-body">Vi tittar på ett arbetsflöde och letar inte efter allt som kan automatiseras. Vi letar efter det lilla som verkligen bör. Det är en konstig affärsmodell. Den fungerar för att den största risken med automation inte är att avstå. Den är att bygga något som aldrig borde finnas. När vi väl bygger gör vi det för din verklighet. Din storlek, ditt regelverk, hur dina människor faktiskt arbetar. Resultatet är inget verktyg från hyllan. Det tål förändring och växer med dig istället för att stå i vägen.</p>',
         '<p class="p-body">We look at a workflow and we are not searching for everything that can be automated. We are searching for the small part that truly should be. It is a strange business model. It works because the biggest risk with automation is not holding back. It is building something that never should have existed. When we do build, we build for your reality. Your size, your regulations, how your people actually work. The result is no off-the-shelf tool. It tolerates change and grows with you instead of standing in the way.</p>')
e = rep1(e, '<span class="rep-frame">Så här kan det se ut</span>', '<span class="rep-frame">What it can look like</span>')
e = rep1(e, '<p class="scene">Varje inkommande avtal läses samma dag det landar. Du får det som spelar roll. Villkor, åtaganden, uppsägningstider, samt en markering vid de ställen där en människa behöver fatta beslutet. Resten slipper du läsa.</p>',
         '<p class="scene">Every incoming contract is read the same day it lands. You get what matters. Terms, commitments, notice periods, and a mark at the places where a human needs to make the decision. The rest you never have to read.</p>')
e = rep1(e, '<p class="scene">Varje måndag ligger en sammanställning i din inkorg: vad konkurrenterna sagt, släppt och ansökt om den gångna veckan, ur offentliga källor. Den analys du annars hade betalat en analytiker för, varje vecka, utan att anställa någon.</p>',
         '<p class="scene">Every Monday a summary sits in your inbox: what your competitors said, released and filed for in the past week, from public sources. The analysis you would otherwise have paid an analyst for, every week, without hiring anyone.</p>')

# ─── §02 DESIGN ───
e = rep1(e, '<h3 class="p-title">Design som består</h3>', '<h3 class="p-title">Design that lasts</h3>')
e = rep1(e, '<p class="p-lede">Vi gör färre saker. De håller längre.</p>',
         '<p class="p-lede">We do fewer things. They last longer.</p>')
e = rep1(e, '<p class="p-body">Bra design börjar inte med att se bra ut. Den börjar med att bestå, när nyheten är borta och prioriteringarna har ändrats. Vi låter varje val förtjäna sin plats. Det blir webb och varumärke du inte behöver göra om varje år. Grafiska beslut som klär din röst, det är din röst som är viktig, inte årets trender.</p>',
         '<p class="p-body">Good design does not begin with looking good. It begins with lasting, when the novelty is gone and the priorities have changed. We let every choice earn its place. The result is web and brand you do not need to redo every year. Graphic decisions that dress your voice, it is your voice that matters, not this year\u2019s trends.</p>')
e = rep1(e, '<p class="proof-gesture">Sidan du läser är exemplet.</p>',
         '<p class="proof-gesture">The page you are reading is the example.</p>')

# ─── §03 SECURE OPERATIONS ───
e = rep1(e, '<h3 class="p-title">Säker drift</h3>', '<h3 class="p-title">Secure operations</h3>')
e = rep1(e, '<p class="p-lede">Det vi bygger ska finnas kvar, i morgon, och året därpå.</p>',
         '<p class="p-lede">What we build should still be there, tomorrow, and the year after.</p>')
e = rep1(e, '<p class="p-body">En automation som inte underhålls slutar fungera tyst. Vi tar hand om det vi bygger. Uppdaterar, övervakar, åtgärdar i bakgrunden. Säkerhet är inbyggd, inte påklistrad efteråt; det följer med från tjugofem år i andras system. Du ska inte behöva tänka på det. Det är hela poängen.</p>',
         '<p class="p-body">An automation that no one maintains stops working quietly. We take care of what we build. Updating, monitoring, fixing in the background. Security is built in, not pasted on afterwards, it comes along from twenty-five years in other people\u2019s systems. You should not have to think about it. That is the whole point.</p>')
e = rep1(e, '<p class="agg">De flesta av våra driftkunder har varit med oss i över tio år. Man byter inte driftpartner när allt bara fungerar.</p>',
         '<p class="agg">Most of our operations clients have been with us for over ten years. You do not change operations partner when everything just works.</p>')
e = rep1(e, '<p class="scene">Det innebär ransomware som stoppas innan den hinner kryptera något, oftast efter att någon klickat på fel sak. Och numera även AI-verktyg som tagits in utan att någon sanktionerat dem. Vi fångar det innan det blir ditt problem.</p>',
         '<p class="scene">That means ransomware stopped before it manages to encrypt anything, usually after someone clicked the wrong thing. And these days also AI tools brought in without anyone approving them. We catch it before it becomes your problem.</p>')

# ─── SPACER ───
e = rep1(e, '<span id="spacerType">Det här är inte allt vi gör ...</span>',
         '<span id="spacerType">This is not all we do ...</span>')
e = rep1(e, '<p class="spacer-sub" id="spacerSub">Tre varumärken · Samma händer</p>',
         '<p class="spacer-sub" id="spacerSub">Three brands · Same hands</p>')

# ─── VENTURES ───
e = rep1(e, 'aria-label="Andra verksamheter"', 'aria-label="Other ventures"')
e = rep1(e, '<span class="ventures-eyebrow">Driver också</span>', '<span class="ventures-eyebrow">Also operating</span>')
e = rep1(e, '<span class="venture-desc">Lokal IT för Skåne</span>', '<span class="venture-desc">Local IT for Skåne</span>')

# ─── FOOTER ───
e = rep1(e, '<span class="full">Vellinge, Sverige</span>', '<span class="full">Vellinge, Sweden</span>')
e = rep1(e, '<a href="privacy.html" style="color:inherit; text-decoration:none;">Integritet</a>',
         '<a href="privacy-policy.html" style="color:inherit; text-decoration:none;">Privacy</a>')
e = rep1(e, 'aria-label="Tillbaka till toppen">↑ Tillbaka till toppen</button>',
         'aria-label="Back to top">↑ Back to top</button>')

# ─── JS STRINGS ───
e = rep1(e, 'const variations = ["AI-automation och webb för företag som tar säkerhet på allvar.", "AI-automation för företag som vill ha tid över för det som spelar roll.", "AI-automation där det räknas. Webb där det märks.", "AI-automation från en operatör med 25 år i IT-säkerhet."];',
         'const variations = ["AI automation and web for companies that take security seriously.", "AI automation for companies that want time left over for what matters.", "AI automation where it counts. Web where it shows.", "AI automation from one operator with 25 years in IT security."];')
e = rep1(e, 'const branchPoint = "AI-automation".length;', 'const branchPoint = "AI automation".length;')
e = rep1(e, 'await setMetaText(`skriver · utkast ${i + 1} av ${variations.length}`);',
         'await setMetaText(`writing · draft ${i + 1} of ${variations.length}`);')
e = rep1(e, 'await setMetaText(`klar · utkast ${i + 1} av ${variations.length}`);',
         'await setMetaText(`done · draft ${i + 1} of ${variations.length}`);')
e = rep1(e, "await setMetaText('skriver om · omformulerar');",
         "await setMetaText('rewriting · rephrasing');")

OUT = '/mnt/user-data/outputs/home.html'
open(OUT, 'w', encoding='utf-8').write(e)

# ── validation ──
import os, re
checks = {
    'size_kb': round(os.path.getsize(OUT)/1024),
    'lang_en': '<html lang="en">' in e,
    'style_balance': e.count('<style>') == 1 and e.count('</style>') == 1,
    'script_balance': e.count('<script') == e.count('</script>'),
    'div_balance': e.count('<div') == e.count('</div>'),
    'no_sv_nav': 'Arbeten</a>' not in e and '>Webb<' not in e,
    'no_sv_phrases': all(p not in e for p in ['värd att bygga', 'Säker drift', 'Driver också', 'Scrolla', 'väntar', 'utkast']),
    'poems_kept': 'Tack&nbsp;för&nbsp;ditt&nbsp;mejl' in e,
    'en_active': e.count('<a class="active" href="home.html">EN</a>') == 2,
    'links_en': all(f'href="{f}"' in e for f in ['automation.html','web.html','work.html','about.html','contact.html','privacy-policy.html']),
}
print('home.html', checks)
