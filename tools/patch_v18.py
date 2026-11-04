import re
p='index.html'; h=open('tools/index-v17.html').read()
def R(a,b,n=1):
    global h
    c=h.count(a)
    assert c>=1 and (n==0 or c==n),(a[:70],c)
    h=h.replace(a,b)
def S(start,end,b):
    "replace from start marker up to (not including) end marker"
    global h
    i=h.index(start); j=h.index(end,i); h=h[:i]+b+h[j:]

# ---------- variables / title
R('"default":"You write the spec. The agents build exactly that."','"default":"You write the spec. The agents build enterprise-grade software with governance built right in."')
R('the SDLC behind the speed (v5)','the SDLC behind the speed (v18)')
R('#s2,#s4a,#s6,#s7,#s7b,#s8b,#s9,#s9t,#s10,#s11{background','#s2,#s4a,#s6,#s7,#s7b,#s8b,#s9,#s9t,#s10,#s10v,#s11{background')

# ---------- CSS
css=r'''
/* v18 · neutral vibe-coding tool (no Kissflow UI before V4) */
#s1 .motion{overflow:hidden}
.vibe{position:absolute;inset:0;background:#0C1220;color:#DDE5F2;font-family:Graphik,sans-serif}
.vibe .vl{position:absolute;left:70px;top:130px;width:580px;height:760px}
.vibe .vp{background:#18223A;border-radius:18px;padding:24px 26px;font:500 29px/1.3 Graphik;color:#fff;height:128px}
.vibe .vt{display:block}
.vibe .vcw{position:absolute;left:0;right:0;top:158px;bottom:0;overflow:hidden;-webkit-mask-image:linear-gradient(transparent,#000 12%,#000 80%,transparent);mask-image:linear-gradient(transparent,#000 12%,#000 80%,transparent)}
.vibe .vc{font:500 21px/1.62 ui-monospace,Menlo,monospace;white-space:pre;color:#8FA3C4}
.vibe .vc b{font-weight:500;color:#7DB6FF}.vibe .vc em{font-style:normal;color:#5FD6A8}
.vibe .vbox,#s2 .appc{position:absolute;left:700px;top:130px;width:1100px;height:760px}
.vibe .vdone{position:absolute;left:1420px;top:60px;width:380px;text-align:center;background:#E9F6EA;color:#2B7A30;font:600 30px Graphik;border-radius:999px;padding:14px 0;opacity:0}
.app{position:absolute;inset:0;background:#fff;border-radius:18px;overflow:hidden;color:#0E1726;box-shadow:0 30px 90px rgba(0,0,0,.35)}
.app .ab{height:50px;background:#EEF0F4;display:flex;align-items:center;gap:9px;padding-left:20px}
.app .ab i{width:13px;height:13px;border-radius:50%;background:#CDD3DD}
.app .ab span{margin-left:18px;background:#fff;border-radius:8px;padding:5px 16px;font:500 17px Graphik;color:#6A7486}
.app .am{position:absolute;left:0;right:0;top:50px;bottom:0;display:flex}
.app aside{width:240px;background:#F5F6F9;padding:30px 26px}
.app aside b{display:block;font:600 24px Graphik;margin-bottom:30px}
.app aside u{display:block;text-decoration:none;font:500 21px Graphik;color:#5B6678;padding:11px 0}
.app main{flex:1;padding:30px 36px}
.app h5{font:600 38px Graphik;margin-bottom:24px}
.app .ast{display:flex;gap:18px;margin-bottom:26px}
.app .ast div{flex:1;border:1.5px solid #E4E7ED;border-radius:12px;padding:16px 18px}
.app .ast small{display:block;font:500 17px Graphik;color:#6A7486;margin-bottom:8px}
.app .ast b{font:600 40px Graphik}
.app .ar{display:flex;align-items:center;font:500 20px Graphik;border-top:1.5px solid #E4E7ED;padding:18px 4px}
.app .ar span:nth-child(1){flex:1.5}.app .ar span:nth-child(2){flex:1.1;color:#6A7486}.app .ar span:nth-child(3){flex:.8}
.app .ar span:nth-child(4){flex:.7;color:#2B7A30}
/* v18 · S2: prototype stopped at the production gate */
#s2 .appc{transform-origin:0 0}
#s2 .stamp{position:absolute;left:50%;top:48%;transform:translate(-50%,-50%) rotate(-7deg);font:600 118px/1 Graphik;letter-spacing:.04em;color:#B85C00;background:#FFF4E5;border:9px solid #E8953A;border-radius:22px;padding:24px 46px;box-shadow:0 18px 50px rgba(184,92,0,.22)}
#s2 .sw{position:absolute;left:0;top:0;width:100%;height:100%}
#s2 .gate{position:absolute;left:1046px;top:212px;width:560px;height:712px}
#s2 .cio{left:1440px!important}
#s2 .glabel{position:absolute;left:1120px;top:120px;font:600 60px Graphik;letter-spacing:.05em;color:var(--ink)}
#s2 .gaps{position:absolute;left:130px;top:775px;display:flex;gap:18px}
#s2 .gaps span{background:#FDECEE;border:2px solid #EFA9B2;color:#B3263A;font:600 28px Graphik;padding:13px 24px;border-radius:999px}
/* v18 · S2t: the SDLC as calendar pages */
#s2t #tiles{position:absolute;left:0;right:0;top:520px;display:flex;justify-content:center;gap:34px}
#s2t .cal{position:relative;width:330px;height:262px;border-radius:22px;background:#fff;overflow:hidden;text-align:center;color:#0E1726}
#s2t .cal:before{content:"";display:block;height:44px;background:#DCE5F3}
#s2t .cal b{display:block;font:600 112px/1 Graphik;letter-spacing:-.02em;margin-top:22px}
#s2t .cal small{display:block;font:600 21px Graphik;letter-spacing:.13em;color:#6A7486;margin-top:14px}
#s2t #mpill{position:absolute;left:50%;top:826px;transform:translateX(-50%);white-space:nowrap;font:600 26px Graphik;letter-spacing:.13em;color:#B85C00;background:#FFF4E5;border:2px solid #F5B66B;border-radius:999px;padding:14px 40px}
/* v18 · S3 brand arrives on its own name */
#s3 .brandp{display:flex;align-items:center;gap:22px;font:500 34px Graphik;color:#fff;margin-bottom:30px}
#s3 .brandp .plate{background:#fff;border-radius:14px;padding:12px 20px;display:flex}
#s3 .brandp img{height:38px;display:block}
/* v18 · S4: crop to the chat that is reading the BRD */
#s4a .browser{left:790px;top:110px;width:1060px;height:854px}
#s4a .lb{left:790px;top:58px}
#s4a .browser video{left:0;top:44px;width:1920px;height:1080px;object-fit:fill;transform-origin:0 0;transform:scale(2.4) translate(-4px,-352px);filter:contrast(1.35) brightness(.96)}
/* v18 · S5 */
#s5 .title em{font-style:normal;color:#7DB6FF}
#s5 .pr{position:absolute;left:0;bottom:0;height:7px;width:100%;background:var(--accent);transform-origin:0 50%}
/* v18 · S6 */
#s6 .say .big{display:block;font:600 86px/1 Graphik;letter-spacing:-.02em;color:#C92A40;margin-bottom:24px}
/* v18 · S7 readers */
#readers{position:absolute;left:120px;top:280px;display:flex;gap:16px}
#readers span{display:flex;align-items:center;gap:12px;background:#fff;border-radius:999px;padding:13px 26px 13px 14px;font:600 32px Graphik;box-shadow:0 14px 34px rgba(31,80,160,.16)}
#heroN{position:absolute;left:120px;top:170px;font:600 70px/1.05 Graphik;letter-spacing:-.02em;opacity:0}
/* v18 · S10v */
#s10v{z-index:4}
#s10v .lv{left:440px;top:170px}
#s10v .vcard{position:absolute;left:440px;top:220px;width:1040px;background:#fff;border-radius:24px;box-shadow:0 30px 80px rgba(31,80,160,.14);padding:34px 44px 22px}
#s10v .vhead{display:flex;align-items:center;justify-content:space-between;font:500 34px Graphik;color:#5B6678;margin-bottom:18px}
#s10v .vhead b{font:600 32px Graphik;color:#0E1726;background:#EEF4FD;border-radius:999px;padding:12px 30px}
#s10v .vrow{display:flex;align-items:center;justify-content:space-between;border-top:2px solid #E9EEF6;padding:26px 0}
#s10v .vrow h6{font:600 46px Graphik;color:#0E1726}
#s10v .vrow small{display:block;font:500 25px Graphik;color:#6A7486;margin-top:6px}
#s10v .tick{width:52px;height:52px}
#s10v .tick:after{left:18px;top:9px;width:12px;height:24px;border-width:0 5px 5px 0}
/* v18 · S11 and end */
#s11 .pop{top:448px;width:240px;height:196px;margin-left:-120px}
#s11 .pop .im{height:196px}
#s11 .pop b{display:none}
#s11 .tl{width:262px;margin-left:-131px;font-size:25px}
#end .tg{font:600 76px/1.2 Graphik;width:1780px}
#end .r3{display:flex;justify-content:center;column-gap:.26em}
#end .lk{margin-top:54px}
'''
R('#cap{position:absolute;left:0;right:0;bottom:44px',css+'#cap{position:absolute;left:0;right:0;bottom:44px')

# ---------- markup
S('<!-- S1 · text-as-mask','<!-- S2 · problem -->','''<!-- S1 · text-as-mask: the word is the door, a generic vibe-coding tool is inside -->
  <section id="s1" class="layer" data-om-id="s1-mask">
    <svg class="glowsvg" id="s1glow"></svg><div id="maskWrap"><div id="counter"><div class="motion"></div></div></div>
    <svg class="glowsvg" id="s1edge"></svg><div id="cover"><div class="motion"></div></div>
  </section>

  ''')
half=lambda i:f'<div class="half" id="{i}"><div class="appc"><div class="sw"></div><div class="stamp">PROTOTYPE</div></div><div class="gaps"><span>✕ No roles</span><span>✕ No approvals</span><span>✕ No audit trail</span></div><img class="gate" src="assets/img/gate.png" alt=""><div class="glabel">PRODUCTION</div><img class="cast cio" src="assets/cast/cio.png" alt=""><div class="tear"></div></div>'
S('<div class="half" id="hL">','<div id="seam">',half('hL')+'\n    '+half('hR')+'\n    ')
R('<div class="ttl" id="s3t" data-om-id="s3-title">Seven steps. <em>Every one run by agents.</em></div>','<div class="ttl" id="s3t" data-om-id="s3-title"><div class="brandp"><span class="plate"><img src="assets/img/kissflow-logo.svg" alt="Kissflow"></span><span>Agentic App Builder</span></div><div id="s3tt">Seven steps.<br><em>Every one run<br>by agents.</em></div></div>')
S('<div class="ln" id="l1"','</div></div></section>\n\n  <!-- S4a','''<div class="ln" id="l1" style="top:190px"></div>
    <div class="ln" id="l2" style="top:330px"><span class="w2">SDLC</span> <span id="kw"><span class="base">g<span id="oo">o</span>vernance.</span><span class="grad">governance.</span><span class="band">governance.</span></span></div>
    <div id="tiles"><div class="cal"><b>MAR</b><small>REQUIREMENTS</small></div><div class="cal"><b>APR</b><small>DESIGN</small></div><div class="cal"><b>MAY</b><small>SIGN-OFF</small></div><div class="cal"><b>JUN</b><small>TESTING</small></div></div>
    <div id="mpill">MONTHS LATER · STILL NOT IN PRODUCTION</div>
  ''')
R('data-start="17.14" data-duration="3.3" data-media-start="40"','data-start="20.15" data-duration="3.3" data-media-start="40"')
R('<div class="title" id="s5t">Designed in parallel</div>','<div class="title" id="s5t">Specialist agents <em id="s5p">in parallel</em></div>')
def shot(i,src,say,media,st,du,rate=1.5,big=None):
    b=f'<span class="big">{big}</span>' if big else ''
    return f'<div class="shot" id="w{i}"><div class="say"><span class="src">{src}</span>{b}{say}</div><div class="browser"><div class="bar"><i></i><i></i><i></i></div><video class="rec" id="vw{i}" src="assets/rec/tour.mp4" muted playsinline data-start="{st}" data-duration="{du}" data-media-start="{media}" data-playback-rate="{rate}"></video></div></div>'
LOG='AI BUILDER · BUILD LOG'; VER='VERIFIER'
shots=[shot(1,LOG,'Full assembly succeeded. Now running the verifier.',37.0,32.14,2.91,1),
 shot(2,VER+' · ROLES','Can anyone get locked out?',52.2,35.05,.8,1.5,'Lockouts'),
 shot(3,VER+' · WORKFLOW CONDITIONS','Can every step be reached?',44.6,35.85,.81,1.5,'Dead ends'),
 shot(4,VER+' · BUSINESS LOGIC','Possibly missing expressions · 9',39.0,36.66,1.14,1.5,'A bad formula'),
 shot(5,LOG,'Now fixing the terminal-step conditions and the bad formula.',45.9,37.8,1.1,1.5),
 shot(6,LOG,'Now re-running verify.',67.3,38.9,.6,1.5),
 shot(7,LOG,'Verifies clean across all 8 roles.',25.8,39.5,.68,1.5)]
S('<div class="shot" id="w1">','<div class="shot" id="w8">','\n    '.join(shots)+'\n    ')
R('<div id="flag" data-om-id="flag">⚠ Possibly missing expressions · 9<small>flagged for review — not guessed</small></div>','<div id="readers" data-om-id="readers"><span id="rd0"><i class="tick"></i>Business</span><span id="rd1"><i class="tick"></i>IT</span><span id="rd2"><i class="tick"></i>Auditors</span></div><div id="heroN" data-om-id="hero-count">Nine <em style="font-style:normal;color:var(--accent)">documents.</em></div>')
R('<!-- S10 · shared-element morph','''<!-- S10v · every build is a version (rebuilt from the Versions control in c04) -->
  <section id="s10v" class="layer" data-om-id="s10-versions">
    <div class="label lv">Placewell — Broking Operations</div>
    <div class="vcard"><div class="vhead"><span>Versions</span><b>Latest</b></div>
      <div class="vrow" id="vr2"><div><h6>Version 1.2</h6><small>Latest build</small></div><span class="tick"></span></div>
      <div class="vrow" id="vr1"><div><h6>Version 1.1</h6><small>Saved</small></div><span class="tick"></span></div>
      <div class="vrow" id="vr0"><div><h6>Version 1.0</h6><small>Saved</small></div><span class="tick"></span></div></div>
  </section>

  <!-- S10 · shared-element morph''')

# ---------- script: constants + transitions + captions
R("const KIND = { '#s2':'push',","const KIND = { '#s2':'fade', '#s10v':'wipe',")
R("const xf = (a, b, t) =>","const SPLIT = 7.15, Z0 = 15.5, T4 = 20.15, T4B = 23.35, T5 = 25.97;   // v18 picture locks to the new VO (voice.scribe.json)\nconst xf = (a, b, t) =>")
i=h.index('const VO = [['); j=h.index('\n',i)
vo=[(.35,'Vibe coding can build you an app in minutes.',2.3),(2.85,"But what you get is a prototype.",1.8),(4.85,"And prototypes don't belong in production.",2.3),(7.35,'Enterprise software demands SDLC governance: requirements, design, sign-off, testing.',6.7),(14.2,'That process takes months.',1.7),(15.9,"Kissflow's Agentic App Builder runs that entire process, in a fraction of the time.",4.4),(20.4,'It starts with your requirements. Agents read the BRD and map every role, rule, and journey.',5.9),(26.2,'Specialist agents design the data, the workflows, the permissions, and the screens. In parallel.',5.8),(32.3,'After every step, a verifier tries to break it. Lockouts. Dead ends. A bad formula. It fixes them — and checks again.',7.6),(43.1,"What you get isn't just an app. It's a Blueprint.",2.9),(47,'Nine documents your business, IT, and auditors can read — before a single screen exists.',5.2),(53.8,'Every decision is logged. Every open question is asked. Nothing gets built until you say so.',6.2),(62.4,'Then it builds — in your own Kissflow development environment, with your permissions — and tests every journey, for every role.',7.4),(73.1,'Every build is a version. Nothing reaches production on its own.',3.8),(79.6,'Rigorous, yet remarkably fast.',2.2),(82.3,'You write the spec. The agents build enterprise-grade software with governance built right in.',5.2)]
import json
h=h[:i]+'const VO = '+json.dumps(vo,ensure_ascii=False)+';'+h[j:]

# ---------- S1 script
s1=r'''// ================= S1 · text-as-mask (0 – 2.85): a generic vibe-coding tool, no Kissflow UI =================
tl.addLabel('scene:hook', 0);
const APP = `<div class="app"><div class="ab"><i></i><i></i><i></i><span>localhost:3000</span></div><div class="am"><aside class="ap"><b>Brokerage App</b><u>Dashboard</u><u>Policies</u><u>Clients</u><u>Claims</u></aside><main><h5 class="ap">Policies</h5><div class="ast"><div class="ap"><small>Active policies</small><b>128</b></div><div class="ap"><small>Renewals due</small><b>14</b></div><div class="ap"><small>Open claims</small><b>6</b></div></div><div class="ar ap"><span>Harbor Logistics</span><span>Marine cargo</span><span>$12,400</span><span>Active</span></div><div class="ar ap"><span>Bluepeak Foods</span><span>Property</span><span>$8,950</span><span>Active</span></div><div class="ar ap"><span>Cedar Health</span><span>Liability</span><span>$21,300</span><span>Active</span></div><div class="ar ap"><span>Atlas Freight</span><span>Fleet</span><span>$6,700</span><span>Active</span></div></main></div></div>`;
const CODE = ["<b>export default function</b> Policies() {","  <b>const</b> [rows, setRows] = useState([]);","  useEffect(() =&gt; {","    fetch(<em>'/api/policies'</em>)","      .then(r =&gt; r.json()).then(setRows);","  }, []);","  <b>return</b> (","    &lt;Layout title=<em>\"Policies\"</em>&gt;","      &lt;Stats items={stats} /&gt;","      &lt;Table rows={rows} columns={cols} /&gt;","    &lt;/Layout&gt;","  );","}","","<b>const</b> cols = [<em>'Client'</em>, <em>'Line'</em>, <em>'Premium'</em>];","<b>const</b> stats = [","  { label: <em>'Active policies'</em>, value: 128 },","  { label: <em>'Renewals due'</em>, value: 14 },","  { label: <em>'Open claims'</em>, value: 6 },","];","","app.get(<em>'/api/policies'</em>, <b>async</b> (req, res) =&gt; {","  res.json(<b>await</b> db.policies.all());","});","","<b>export const</b> schema = {","  client: <em>'text'</em>, premium: <em>'number'</em>,","};","","app.listen(3000);"].join('\n');
$$('#s1 .motion').forEach((m) => m.innerHTML = `<div class="vibe"><div class="vl"><div class="vp"><span class="vt">Build me an insurance brokerage app</span></div><div class="vcw"><div class="vc">${CODE}</div></div></div><div class="vbox">${APP}</div><div class="vdone">✓ Built in minutes</div></div>`);
$$('#s2 .sw').forEach((s) => s.innerHTML = APP);
{
'''
S("// ================= S1 · text-as-mask (0 – 6.43)","  const word = V.maskWord, fs = 470;",s1)
R("""    .to(st, { e: 1, duration: T1 - D1, ease: bz(.4, 0, .2, 1), onUpdate: upd }, D1)
    .to('#s1tag', { opacity: 0, duration: .45, ease: 'none' }, D1);""","""    .to(st, { e: 1, duration: T1 - D1, ease: bz(.4, 0, .2, 1), onUpdate: upd }, D1);""")
S("  // home screen → punch into the prompt card","// ================= S2 · problem (6.43","""  // prompt types, code streams, the app assembles itself
  gsap.set('.vibe .ap', { opacity: 0 });
  const ty = { p: 0 }, tp = () => $$('.vibe .vt').forEach((e) => e.style.clipPath = `inset(0 ${(1 - ty.p) * 100}% 0 0)`); tp();
  tl.to(ty, { p: 1, duration: .75, ease: 'none', onUpdate: tp }, .2)
    .fromTo('.vibe .vc', { y: 0 }, { y: -560, duration: 2.5, ease: 'none', immediateRender: false }, .35);
  $$('.vibe').forEach((v) => tl.fromTo(v.querySelectorAll('.ap'), { opacity: 0, y: 14 }, { opacity: 1, y: 0, duration: .16, stagger: .085, ease: 'power2.out', immediateRender: false }, 1.2));
  tl.fromTo('.vibe .vdone', { opacity: 0, y: 12, scale: .92 }, { opacity: 1, y: 0, scale: 1, duration: .28, ease: 'back.out(2.4)', immediateRender: false }, 1.96);
  for (let k = 0; k < 9; k++) OM.sfx('type', .2 + k * .08, { gain: .22, dur: .06 });
  for (let k = 0; k < 6; k++) OM.sfx('pop', 1.25 + k * .15, { gain: .1, note: k + 1 });
  OM.sfx('pop', 1.96, { gain: .3, note: 5 });
}

""")

# ---------- S2 + S2t
s2=r'''// ================= S2 · problem (2.85 – 7.15): prototype stopped at the production gate =================
tl.addLabel('scene:problem', 2.85);
xf('#s1', '#s2', 2.85);
// cast cut-outs start hidden (their entrances are fromTo with immediateRender:false — without this they flash in, vanish, re-enter)
gsap.set(['#s2 .cio', '#s4an', '#s8cio'], { opacity: 0 });
gsap.set(['#s2 .stamp', '#s2 .gate', '#s2 .glabel', '#s2 .gaps span'], { opacity: 0 });
tl.fromTo('#s2 .appc', { x: 0, y: 0, scale: 1 }, { x: -570, y: 40, scale: .73, duration: .75, ease: 'power3.inOut', immediateRender: false }, 2.95)
  .fromTo('#s2 .stamp', { opacity: 0, scale: 1.9 }, { opacity: 1, scale: 1, duration: .16, ease: 'power3.in', immediateRender: false }, 3.72)
  .fromTo('#s2 .appc', { rotate: 0 }, { keyframes: [{ rotate: -.7, duration: F(2) }, { rotate: .4, duration: F(2) }, { rotate: 0, duration: F(3) }], ease: 'none', immediateRender: false }, 3.88)
  .fromTo(['#s2 .gate', '#s2 .glabel'], { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: .4, ease: 'expo.out', immediateRender: false }, 4.8)
  .fromTo('#s2 .cio', { x: 90, opacity: 0 }, { x: 0, opacity: 1, duration: .8, ease: 'power3.out', snap: { x: 1 }, immediateRender: false }, 4.95)
  .to('#s2 .appc', { x: -440, duration: 1.15, ease: 'power2.in' }, 5.2)
  .to('#s2 .appc', { x: -490, duration: .4, ease: 'power3.out' }, 6.35)
  .fromTo('#s2 .gate', { filter: 'drop-shadow(0 0 0px rgba(201,42,64,0))' }, { filter: 'drop-shadow(0 0 22px rgba(201,42,64,.95))', duration: .1, ease: 'none', immediateRender: false }, 6.35)
  .fromTo('#s2 .gate', { x: 0 }, { keyframes: [{ x: 9, duration: F(2) }, { x: -5, duration: F(2) }, { x: 0, duration: F(3) }], ease: 'none', immediateRender: false }, 6.35);
$$('#s2 .half').forEach((H) => [...H.querySelectorAll('.gaps span')].forEach((e, i) => tl.fromTo(e, { opacity: 0, y: 14 }, { opacity: 1, y: 0, duration: .22, ease: 'back.out(2)', immediateRender: false }, 6.42 + i * .17)));
OM.sfx('whoosh', 3.0, { gain: .2 }); OM.sfx('thud', 3.88, { gain: .5 }); OM.sfx('whoosh', 5.5, { gain: .18 }); OM.sfx('impact', 6.35, { gain: .4 });
[0, 1, 2].forEach((i) => OM.sfx('glitch', 6.42 + i * .17, { gain: .14, pitch: 1 + i * .08 }));

// ---- page-turn-transitions · barn-door-split: the gate tears open, the line takes its place ----
'''
S("// ================= S2 · problem (6.43","const SPLIT = 9.3;\n",s2)
h=h.replace("const SPLIT = 9.3;\n","",1)
R("// ---- S2t: lead-word zoom + drift-assembly · gradient-word-sweep on \"process.\" ----","// ---- S2t: lead-word zoom + drift-assembly · gradient sweep on \"governance\", then the SDLC as calendar pages ----")
R("immediateRender: false }, SPLIT + .12);","immediateRender: false }, SPLIT + .2);")
R("immediateRender: false }, SPLIT + .5 + i * .018));","immediateRender: false }, SPLIT + .65 + i * .018));")
R("OM.sfx('whoosh', SPLIT + .5, { gain: .22 });","OM.sfx('whoosh', SPLIT + .65, { gain: .22 });")
R("const KW = 10.85;","const KW = 9.72;\n  gsap.set(['#s2t .cal', '#mpill'], { opacity: 0 });")
R("tl.fromTo('#l2 .w2', { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: .35, stagger: .08, ease: 'expo.out', immediateRender: false }, KW - .25)","tl.fromTo('#l2 .w2', { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: .35, stagger: .08, ease: 'expo.out', immediateRender: false }, 9.05)")
R("""  OM.sfx('thud', KW, { gain: .4 });
""","""  OM.sfx('thud', KW, { gain: .4 });
  // each stage lands on its spoken word; "months" turns the row into the wait
  [10.72, 11.68, 12.48, 13.22].forEach((t, i) => { tl.fromTo($$('#s2t .cal')[i], { opacity: 0, y: 46, rotateX: -50 }, { opacity: 1, y: 0, rotateX: 0, duration: .36, ease: 'back.out(1.6)', immediateRender: false }, t); OM.sfx('paper', t, { gain: .24 }); });
  tl.fromTo('#mpill', { opacity: 0, y: 14 }, { opacity: 1, y: 0, duration: .25, ease: 'back.out(2)', immediateRender: false }, 15.2);
  OM.sfx('tick', 15.2, { gain: .4 });
""")
R("const Z0 = 12.4, ZD = .95, ZMAX = 75,","const ZD = .95, ZMAX = 75,")
R("immediateRender: false, onUpdate: zpaint, onStart: zpaint }, KW)","immediateRender: false, onUpdate: zpaint, onStart: zpaint }, Z0 - .4)")

# ---------- S3
R("// ================= S3 · steep-tilt-glide (12.86 – 17.14)","// ================= S3 · steep-tilt-glide (15.5 – 20.15)")
R("tl.addLabel('scene:spine', BAR(7));","tl.addLabel('scene:spine', Z0);")
R("#s3 .anchor{position:absolute;left:40%;","#s3 .anchor{position:absolute;left:46%;")
R("#s3 .ttl{position:absolute;left:120px;top:110px;font:600 64px/1.1 Graphik;color:#fff;width:820px}","#s3 .ttl{position:absolute;left:100px;top:90px;font:600 52px/1.14 Graphik;color:#fff;width:560px}")
R("lxAt = (f) => lerp(glide(clamp01(f / 120)), 60, -4100);","lxAt = (f) => lerp(glide(clamp01(f / 136)), 60, -4800);")
R("drive(12.4, 139, (f) =>","drive(Z0, 140, (f) =>")
R("tl.fromTo('#s3t', { opacity: 0, x: -30 }, { opacity: 1, x: 0, duration: .5, ease: 'expo.out', immediateRender: false }, BAR(7) + .5);\n  OM.sfx('whoosh', BAR(7) + .2, { gain: .4, dur: 1.2 });",
  "gsap.set(['#s3 .brandp', '#s3tt'], { opacity: 0 });\n  tl.fromTo('#s3 .brandp', { opacity: 0, x: -30 }, { opacity: 1, x: 0, duration: .45, ease: 'expo.out', immediateRender: false }, 15.95)\n    .fromTo('#s3tt', { opacity: 0, x: -30 }, { opacity: 1, x: 0, duration: .5, ease: 'expo.out', immediateRender: false }, 17.4);\n  OM.sfx('whoosh', Z0 + .25, { gain: .4, dur: 1.2 });")

# ---------- S4
S("// ================= S4 · requirements (17.14","{ // beat-step list from 20.35","""// ================= S4 · requirements (20.15 – 25.97) =================
tl.addLabel('scene:requirements', T4);
xf('#s3', '#s4a', T4);
tl.fromTo('#s4br', { y: 60, scale: .96 }, { y: 0, scale: 1, duration: .7, ease: 'expo.out', immediateRender: false }, T4)
  .fromTo('#s4an', { x: -140, opacity: 0 }, { x: 0, opacity: 1, duration: .8, ease: 'expo.out', immediateRender: false }, T4 + .2)
  .to('#s4br', { scale: 1.03, duration: 2.4, ease: 'none' }, T4 + .7);
OM.sfx('whoosh', T4 - .1, { gain: .3 });
""")
R("{ // beat-step list from 20.35 (bar 10.5)\n  const S = 20.35,","{ // beat-step list: all six land before the wipe\n  const S = T4B,")
R("{ p: '#4AA147', bg: '#14261A' }];","{ p: '#4AA147', bg: '#14261A' }, { p: '#CF2C91', bg: '#2A1426' }];")
R("PRE = B(1) * FPS, NB = 4;","PRE = B(1) * FPS, NB = 5;")
R("drive(S, Math.round((BAR(12) - S) * FPS), (f) => { const beat","drive(S, Math.round((T5 - S) * FPS), (f) => { const beat")

# ---------- S5: truly parallel
S("// ================= S5 · bento light-up","// ================= S6 · verify montage",r'''// ================= S5 · parallel agents (25.97 – 32.14) =================
tl.addLabel('scene:design', T5);
xf('#s4b', '#s5', T5);
{
  const CELLS = [['Data model', 'c11-bp-Data_Model'], ['Data & fields', 'c12-bp-Data_Fields'], ['Business logic', 'c13-bp-Business_Logic'], ['Workflows', 'c14-bp-Workflows'], ['Roles & permissions', 'c15-bp-Roles_Permissions'], ['Pages & nav', 'c16-bp-Pages_Nav']];
  const cells = CELLS.map(([name, ms], i) => { const col = i % 3, row = Math.floor(i / 3), x = 196 + col * 524, y = 228 + row * 374;
    const d = document.createElement('div'); d.className = 'cell'; d.style.left = x + 'px'; d.style.top = y + 'px';
    d.innerHTML = `<div class="cardc"><div class="im" style="background-image:url(assets/img/${ms}.png)"></div><b>${name}</b><i class="pr"></i></div><svg width="480" height="330" viewBox="0 0 480 330"><rect x="2" y="2" width="476" height="326" rx="14" fill="none" stroke="#F58220" stroke-width="5" pathLength="100" stroke-dasharray="100"/></svg>`;
    $('#wall').appendChild(d); return { im: d.querySelector('.im'), pr: d.querySelector('.pr'), card: d.querySelector('.cardc'), rect: d.querySelector('rect'), svg: d.querySelector('svg') }; });
  // every lane starts together on "Specialist" and finishes together on "parallel"; the outline follows the words
  const fr = (t) => (t - T5) * FPS, A = fr(26.36), Z = fr(30.98), POW = [.75, 1.35, .9, 1.6, 1.1, .8], WORD = [27.72, 27.72, 28.36, 28.36, 29.04, 29.8].map(fr), bk = bz(.3, 1.4, .5, 1), push = bz(.33, 0, .2, 1);
  drive(T5, Math.round((BAR(16) - T5) * FPS), (f) => { cells.forEach((c, i) => { const p = clamp01((f - A) / (Z - A)) ** POW[i], w = WORD[i];
      c.im.style.clipPath = `inset(0 ${(1 - p) * 100}% 0 0)`; c.pr.style.transform = `scaleX(${p})`; c.pr.style.background = p >= 1 ? 'var(--pass)' : 'var(--accent)';
      const draw = itp(f, w, w + 8, 0, 1, E.outCubic), fade = itp(f, w + 12, w + 30, 1, 0, E.outQuad); c.rect.style.strokeDashoffset = 100 * (1 - draw); c.rect.style.opacity = fade; c.svg.style.display = draw > 0 && fade > 0 ? 'block' : 'none';
      const rise = itp(f, Z, Z + 9, 0, 1, bk), ty = 16 * Math.sin(Math.PI * clamp01(rise)); c.card.style.transform = `translateY(${-ty}px)`; c.card.style.opacity = itp(f, 0, A, .25, 1); });
    $('#wall').style.transform = `scale(${itp(f, Z, Z + 25, 1, 1.03, push)})`; $('#s5p').style.opacity = itp(f, Z - 6, Z + 2, 0, 1); });
  [27.72, 28.36, 29.04, 29.8].forEach((t, i) => OM.sfx('pop', t, { gain: .28, note: i + 1 }));
  OM.sfx('hit', 30.98, { gain: .35 });
}

''')

# ---------- S6
S("  const beats = [3, 2, 2, 2, 2, 2, 2, 3], verdict","  // gate pill: one continuous entrance",r'''  // shots land on the spoken words: Lockouts · Dead ends · A bad formula · fixes · checks again
  const TS = [BAR(16), 35.05, 35.85, 36.66, 37.8, 38.9, 39.5, 40.18, 40.9], verdict = ['scan', 'x', 'x', 'x', 'scan', 'scan', 'ok', ''];
  verdict.forEach((vd, i) => { const el = `#w${i + 1}`, t = TS[i], d = TS[i + 1] - t; tl.set(el, { opacity: 1 }, t); if (i) tl.set(`#w${i}`, { opacity: 0 }, t);
    if (i < 7) tl.fromTo(`${el} .browser`, { scale: 1.12, x: 50 }, { scale: 1, x: 0, duration: d, ease: 'power2.out', immediateRender: false }, t);
    if (i < 7) tl.fromTo(`${el} .say`, { x: -30 }, { x: 0, duration: .3, ease: 'expo.out', immediateRender: false }, t);
    tl.set('#slot', { attr: { class: 'slot ' + vd } }, t).fromTo('#slot', { scale: .5 }, { scale: 1, duration: .25, ease: 'back.out(3)', immediateRender: false }, t);
    if (i < 7) OM.sfx(vd === 'x' ? 'glitch' : 'hit', t, { gain: .35, pitch: 1 + i * .04 }); });
''')
R("  const G = t - B(3);\n","  const G = 40.18;\n")

# ---------- S7
R("""  tl.set('#scan', { opacity: 1, z: 30 }, BAR(23) - .2).to('#scan', { z: -3 * D - 10, duration: 1.2, ease: 'power2.inOut' }, BAR(23))
    .fromTo('#flag', { opacity: 0, x: 30 }, { opacity: 1, x: 0, duration: .35, ease: 'back.out(2)', immediateRender: false }, BAR(23) + 1.2)
    .to('#scan', { z: -8 * D - 10, duration: 1.6, ease: 'power2.inOut' }, BAR(23) + 2.6).to(['#scan', '#flag'], { opacity: 0, duration: .3 }, 51.2);
  OM.sfx('whoosh', BAR(23), { gain: .3 }); OM.sfx('tick', BAR(23) + 1.2, { gain: .45 });""","""  tl.set('#scan', { opacity: 1, z: 30 }, BAR(23) - .2).to('#scan', { z: -8 * D - 10, duration: 3.0, ease: 'power2.inOut' }, BAR(23)).to('#scan', { opacity: 0, duration: .3 }, 50.6);
  OM.sfx('whoosh', BAR(23), { gain: .3 });
  // "Nine documents", then each reader lands on their word
  gsap.set(['#rd0', '#rd1', '#rd2'], { opacity: 0 });
  tl.to('#heroT', { opacity: 0, duration: .22 }, 46.9).fromTo('#heroN', { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: .4, ease: 'expo.out', immediateRender: false }, 47.05).to(['#heroN', '#readers'], { opacity: 0, duration: .3 }, 50.9);
  [47.94, 48.66, 49.2].forEach((t, i) => { tl.fromTo('#rd' + i, { opacity: 0, y: 14, scale: .9 }, { opacity: 1, y: 0, scale: 1, duration: .28, ease: 'back.out(2.4)', immediateRender: false }, t); OM.sfx('tick', t, { gain: .4 }); });""")
R(".to('#heroT', { opacity: 0, duration: .3 }, 50.6);",";")
R("immediateRender: false }, 45.0);","immediateRender: false }, 44.95);")

# ---------- S8a words
R("const WORDS = ['Logged', 'Reviewed', 'Approved'], SL = [[0, .36], [.32, .68], [.64, 1]]","const WORDS = ['Logged', 'Asked', 'Until you say so'], SL = [[0, .36], [.36, .68], [.68, 1]]")
R("sh = seg(t, t0 + .05, t0 + .2, E.outQuad), sw = seg(t, t0 + .08, t0 + .26, E.inOutCubic), wh = seg(t, t0 + .27, t0 + .34, E.outQuad);","sh = seg(t, t0 + .01, t0 + .06, E.outQuad), sw = seg(t, t0 + .02, t0 + .13, E.inOutCubic), wh = seg(t, t0 + .13, t0 + .19, E.outQuad);")

# ---------- S10: version first, then the production gate
R("xf('#s9t', '#s10', BAR(35));\n{\n  const S = BAR(35),","""xf('#s9t', '#s10v', BAR(35));
{ const rows = ['#vr0', '#vr1', '#vr2']; gsap.set(rows, { opacity: 0 });
  [73.1, 73.5, 73.92].forEach((t, i) => { tl.fromTo(rows[i], { opacity: 0, y: 26 }, { opacity: 1, y: 0, duration: .3, ease: 'expo.out', immediateRender: false }, t); OM.sfx('tick', t, { gain: .4 }); }); }
xf('#s10v', '#s10', 74.75);
{
  const S = 74.75,""")

# ---------- S11: all seven at once
S("  const GAP = 1400, X0 = 960,","  $('#tworld').innerHTML = h;",r'''  const GAP = 262, X0 = 174;
  let h = `<div class="axis" style="left:0;width:1920px"></div>`;
  STAGES.forEach(([n, img], i) => { const x = X0 + i * GAP; h += `<div class="tk" style="left:${x}px"></div><div class="tl" style="left:${x}px">${n}</div><div class="pop" style="left:${x}px"><div class="im" style="background-image:url(assets/img/${img}.png);background-size:900px auto;background-position:-216px -72px"></div></div>`; });
''')
S("  const camX = (f) =>","// ================= END ·",r'''  const POP = STAGES.map((_, i) => 6 + i * (N - 30) / 6);
  drive(BAR(38), N, (f) => { cards.forEach((c, i) => { const k = f - POP[i]; if (k < 0) { c.style.display = 'none'; return; } const s = k >= 26 ? 1 : springA(k / 30 * 1.3, 11, 160, .9); Object.assign(c.style, { display: 'block', transform: `scaleY(${s}) scaleX(${.6 + .4 * s})`, opacity: Math.min(1, s * 2) }); }); });
  POP.forEach((p) => OM.sfx('tick', BAR(38) + F(p), { gain: .3 }));
}

''')

# ---------- END: the card says what the voice says
S("  const words = ['You', 'write',","  const press = bz(",r'''  const rows = [[['You', 82.54], ['write', 82.62], ['the', 82.86], ['spec.', 83.02]], [['The', 83.76], ['agents', 83.94], ['build', 84.3], ['enterprise-grade', 84.54], ['software', 85.26]], [['with', 85.68], ['governance', 85.84], ['built', 86.34], ['right', 86.56], ['in.', 86.78]]];
  const TW = rows.flat().map((w) => w[1] - .08);
  $('#tg').innerHTML = rows.map((r, n) => `<div class="r${n + 1}">${r.map(([w]) => `<span class="wd${n === 2 && w !== 'with' ? ' ac' : ''}">${w}</span>`).join('')}</div>`).join('');
''')
R("W.forEach((w, i) => tl.fromTo(w, { opacity: 0, scale: 1.28, filter: 'blur(7px)' }, { opacity: 1, scale: 1, filter: 'blur(0px)', duration: F(9), ease: press, immediateRender: false }, END + .2 + F(4 + i * 4)));\n  const U = END + .2 + F(4 + 9 * 4);","W.forEach((w, i) => tl.fromTo(w, { opacity: 0, scale: 1.28, filter: 'blur(7px)' }, { opacity: 1, scale: 1, filter: 'blur(0px)', duration: F(8), ease: press, immediateRender: false }, TW[i]));\n  const U = 87.05;")
R("W.forEach((_, i) => OM.sfx('type', END + .2 + F(4 + i * 4) + F(6), { gain: .06, dur: .05 }));","TW.forEach((t) => OM.sfx('type', t + F(6), { gain: .06, dur: .05 }));")

# ---------- foley + scene whooshes
S("{ // hook footage (build.mp4, frame-checked)","  OM.sfx('click', 59.0 + (77.67","{\n")
R("[BAR(4), BAR(9), 20.35, BAR(12), BAR(16),","[2.85, T4, T4B, T5, BAR(16),")
R("BAR(30), BAR(32), BAR(35), BAR(38)].forEach","BAR(30), BAR(32), BAR(35), 74.75, BAR(38)].forEach")
open(p,'w').write(h)
print('ok',len(h))
