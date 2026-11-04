import re,subprocess
subprocess.check_call(['python3','tools/patch_v18.py'])
p='index.html'; h=open(p).read(); X=112/30
def R(a,b):
    global h
    assert a in h,a[:60]
    h=h.replace(a,b)
R("T4 = 20.15, T4B = 23.35, T5 = 25.97;","T4 = 20.15, T4L = 25.0, T4B = 27.2, T5 = 25.97, X = 112 / 30;   // X = inserted time (two repeated music phrases' worth), S5 onward moves by X")
R("KIND = { '#s2':'fade',","KIND = { '#s4h':'wipe', '#s2':'fade',")
# v17 live-build framing returns
h=re.sub(r"/\* v18 · S4: crop to the chat that is reading the BRD \*/\n.*?\n.*?\n.*?\n","/* v19 · S4h: the real requirements flow */\n#s4h{background:#EDF5FE}\n#s4h #p4,#s4h .seg{position:absolute;inset:0}\n#s4h #p4{transform-origin:960px 300px}\n#s4h video{position:absolute;inset:0;width:1920px;height:1080px;object-fit:cover}\n#s4h #h4b,#s4h #h4c,#s4h #h4d{opacity:0}\n",h,count=1,flags=re.S)
vid=lambda i,st,du,me,ra:f'<div class="seg" id="h4{i}"><video class="rec" id="vh{i}" src="assets/rec/build.mp4" muted playsinline data-start="{st}" data-duration="{du}" data-media-start="{me}" data-playback-rate="{ra}"></video></div>'
sec='<!-- S4h · the real requirements flow: prompt, BRD, Start building, Express -->\n  <section id="s4h" class="layer" data-om-id="s4-flow"><div id="p4">'+vid('a',20.15,2.12,3.9,1.95)+vid('b',22.27,.9,8.3,1.2)+vid('c',23.17,.75,11.3,1.1)+vid('d',23.92,1.1,16.6,2.4)+'</div></section>\n\n  '
R('<!-- S4a · requirements: the live build reading the BRD -->',sec+'<!-- S4a · requirements: the live build reading the BRD -->')
R('data-start="20.15" data-duration="3.3" data-media-start="40"','data-start="25" data-duration="2.5" data-media-start="40"')
# everything from S5 on moves by X: videos here, tweens via shiftChildren, sfx via wrapper
def sv(m):
    s=float(m.group(2))
    return m.group(1)+f'data-start="{round(s+X,3)}"' if s>=30 else m.group(0)
h=re.sub(r'(<video class="rec" id="v[^"]*" src="[^"]*" muted playsinline )data-start="([\d.]+)"',sv,h)
R('data-start="0" data-duration="90" data-track-index="8"','data-start="0" data-duration="93.733" data-track-index="8"')
R('data-start="0" data-duration="90" data-track-index="9"','data-start="0" data-duration="93.733" data-track-index="9"')
# move S4 block to after the shift
i=h.index('// ================= S4 · requirements'); j=h.index('// ================= S5 ·')
s4=h[i:j]; h=h[:i]+"const _sfx = OM.sfx; OM.sfx = (n, t, o) => _sfx.call(OM, n, t + X, o);   // S5 onward sits X later\n"+h[j:]
R("xf('#s4b', '#s5', T5);\n","")
R("[2.85, T4, T4B, T5, BAR(16),","[T5, BAR(16),")
s4=s4.split("{ // beat-step list",1)[1]
s4="{ // beat-step list"+s4
s4=s4.replace("BL = B(1) * FPS, PRE = B(1) * FPS, NB = 5;","BL = 13.6, PRE = 10, NB = 5;")
s4=s4.replace("drive(S, Math.round((T5 - S) * FPS)","drive(S, Math.round((T5 + X - S) * FPS)")
s4=s4.replace("OM.sfx('tick', S + B(1) * k, { gain: .4 })","OM.sfx('tick', S + F(PRE + (k - 1) * BL), { gain: .4 })")
new=r'''// ---------- v19: open X seconds before S5, then lay the real requirements flow into the gap ----------
tl.shiftChildren(X, true, 25); OM.sfx = _sfx;
// ================= S4h · prompt → BRD → Start building → Express (20.15 – 25.0) =================
tl.addLabel('scene:requirements', T4);
xf('#s3', '#s4h', T4);
tl.fromTo('#p4', { scale: 1 }, { scale: 1.42, duration: .6, ease: 'power2.inOut', immediateRender: false }, 20.65)
  .fromTo('#p4', { scale: 1.42 }, { scale: 1.48, duration: 23.92 - 21.25, ease: 'none', immediateRender: false }, 21.25)
  .set('#h4a', { opacity: 0 }, 22.27).set('#h4b', { opacity: 1 }, 22.27)
  .set('#h4b', { opacity: 0 }, 23.17).set('#h4c', { opacity: 1 }, 23.17)
  .set('#h4c', { opacity: 0 }, 23.92).set('#h4d', { opacity: 1 }, 23.92).set('#p4', { scale: 1 }, 23.92);
for (let k = 0; k < 9; k++) OM.sfx('type', 20.71 + k * .137, { gain: .22, dur: .06 });
OM.sfx('click', 22.73, { gain: .35 }); OM.sfx('pop', 22.85, { gain: .2 }); OM.sfx('click', 23.8, { gain: .45 }); OM.sfx('click', 24.71, { gain: .3 });
// ================= S4a · live build, v17 framing (25.0 – 27.2) =================
xf('#s4h', '#s4a', T4L);
tl.fromTo('#s4br', { y: 60, scale: .96 }, { y: 0, scale: 1, duration: .7, ease: 'expo.out', immediateRender: false }, T4L)
  .fromTo('#s4an', { x: -140, opacity: 0 }, { x: 0, opacity: 1, duration: .8, ease: 'expo.out', immediateRender: false }, T4L + .2)
  .to('#s4br', { scale: 1.03, duration: 1.5, ease: 'none' }, T4L + .7);
[2.85, T4, T4L, T4B].forEach((t, i) => OM.sfx('whoosh', t - .12, { gain: .22, pan: i % 2 ? .25 : -.25 }));
'''+s4+"xf('#s4b', '#s5', T5 + X);\n\n"
R("window.__timelines['film'] = tl;",new+"window.__timelines['film'] = tl;")
h=h.replace('the SDLC behind the speed (v18)','the SDLC behind the speed (v19)')
open(p,'w').write(h); print('ok',len(h))
