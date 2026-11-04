# Replaces the tests card (S9t) with the Placewell web + mobile output showcase and adds the pitch line to the end card.
import re
P = '/Users/abhiram/Documents/kissflow-blueprint-film/index.html'
s = open(P).read()

a = s.index('  <section id="s9t" class="layer" data-om-id="s9-test">')
b = s.index('  </section>', a) + len('  </section>')
roles = ['Account Executive', 'Broker Support', 'Claims Manager', 'Compliance Officer', 'Finance', 'Broking Manager', 'Executive', 'Admin']
chips = ''.join(f'<span><i class="tick"></i>{r}</span>' for r in roles)
html = f'''  <section id="s9t" class="layer" data-om-id="s9-output">
    <div class="label lbo">The output · built on Kissflow, web and mobile</div>
    <div class="browser" id="pwWeb"><div class="bar"><i></i><i></i><i></i><span>placewell · Today</span></div>
      <video class="rec" id="vpw" src="assets/rec/placewell-web.mp4" muted playsinline data-start="66.429" data-duration="6.43" data-media-start="6" data-playback-rate="2.5"></video></div>
    <div class="phone" id="pwMob"><video class="rec" id="vpm" src="assets/rec/placewell-mobile.mp4" muted playsinline data-start="66.429" data-duration="6.43" data-media-start="4" data-playback-rate="1.25"></video></div>
    <div class="chips" id="pwChips"><b>Every journey tested</b>{chips}</div>
  </section>'''
s = s[:a] + html + s[b:]

css = '''#s9t .lbo{left:90px;top:84px}
#s9t #pwWeb{left:90px;top:130px;width:1200px;height:681px}
#s9t .phone{position:absolute;left:1370px;top:70px;width:410px;height:891px;border-radius:58px;border:14px solid #0E1726;overflow:hidden;background:#fff;box-shadow:0 40px 100px rgba(14,23,38,.32)}
#s9t .phone video{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:50% 0}
#s9t .chips{position:absolute;left:90px;top:850px;width:1200px;display:flex;flex-wrap:wrap;gap:10px;align-items:center}
#s9t .chips b{font:600 22px Graphik;margin-right:10px;color:var(--ink)}
#s9t .chips span{display:inline-flex;align-items:center;gap:9px;font:500 19px Graphik;background:#fff;border:1.5px solid #E3E9F2;border-radius:999px;padding:8px 14px 8px 8px}
#s9t .chips .tick{width:24px;height:24px;opacity:.15}
#s9t .chips .tick:after{left:8px;top:4px;width:6px;height:12px;border-width:0 3px 3px 0}
'''
s, n = re.subn(r"#s9t \.tst\{.*?\n#s9t \.analyst2\{[^}]*\}\n", css, s, flags=re.S)
assert n == 1, 'css block'

t0 = s.index("xf('#s9', '#s9t', BAR(32))")
t1 = s.index("xf('#s9t', '#s10', BAR(35));")
new_tl = '''xf('#s9', '#s9t', BAR(32))
  .fromTo('#pwWeb', { y: 60, opacity: 0 }, { y: 0, opacity: 1, duration: .7, ease: 'expo.out', immediateRender: false }, BAR(32))
  .fromTo('#pwMob', { y: 140, rotate: 4, opacity: 0 }, { y: 0, rotate: 0, opacity: 1, duration: .8, ease: 'expo.out', immediateRender: false }, BAR(32) + .25)
  .fromTo('#pwChips', { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: .5, ease: 'expo.out', immediateRender: false }, BAR(32) + .6)
  .to('#pwWeb', { scale: 1.03, duration: BAR(35) - BAR(32) - .7, ease: 'none' }, BAR(32) + .7)
  .to('#pwMob', { y: -10, duration: BAR(35) - BAR(32) - 1.05, ease: 'none' }, BAR(32) + 1.05);
$$('#pwChips .tick').forEach((el, i) => { const t = BAR(33) + B(.5 * i); tl.fromTo(el, { opacity: .15, scale: .6 }, { opacity: 1, scale: 1, duration: .25, ease: 'back.out(3)', immediateRender: false }, t); OM.sfx('tick', t, { gain: .28 }); });

'''
s = s[:t0] + new_tl + s[t1:]

# pitch line on the end card
old_end = '<section id="end" class="layer" data-om-id="end-card"><div class="tg" data-om-var="tagline" id="tg"></div>'
assert old_end in s
s = s.replace(old_end, old_end + '<div class="pitch" id="pitch" data-var-text="pitch">Agentic Builder with Enterprise SDLC Governance Blueprint</div>')
s = s.replace("#end .lk{display:flex;align-items:center;gap:26px;margin-top:70px}",
              "#end .pitch{margin-top:34px;font:500 34px Graphik;color:#45506A;letter-spacing:.005em}\n#end .lk{display:flex;align-items:center;gap:26px;margin-top:64px}")
s = s.replace('{"id":"product","type":"string","label":"Product name","default":"Agentic App Builder"},',
              '{"id":"product","type":"string","label":"Product name","default":"Agentic App Builder"},\n  {"id":"pitch","type":"string","label":"Pitch line","default":"Agentic Builder with Enterprise SDLC Governance Blueprint"},')
s = s.replace("  .fromTo('#end .lk', { opacity: 0 },",
              "  .fromTo('#pitch', { opacity: 0, y: 16 }, { opacity: 1, y: 0, duration: .6, ease: 'expo.out', immediateRender: false }, BAR(41) + B(1))\n  .fromTo('#end .lk', { opacity: 0 },")
open(P, 'w').write(s)
print('ok', 'pwWeb' in s, '#pitch' in s)
