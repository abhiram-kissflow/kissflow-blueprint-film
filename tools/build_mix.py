# Builds mix/index.html: HyperFrames mix of picture + Bria + ElevenLabs bed (carved) + real SFX.
import json, html
D='/Users/abhiram/Documents/kissflow-blueprint-film'
hits=json.load(open(f'{D}/tools/hits.json')); peaks=json.load(open(f'{D}/mix/peaks.json')); starts=json.load(open(f'{D}/mix/assets/vo/starts.json'))
B=60/112; BAR=lambda n:(n-1)*4*B
MAP={'whoosh':('whoosh',.32),'tick':('tick',.22),'pop':('pop',.28),'paper':('paper',.28),'hit':('hit',.32),'thud':('thud',.34),
     'click':('click',.45),'glitch':('glitch',.16),'chime':('chime',.32),'subdrop':('subdrop',.38),'sparkle':('sparkle',.32)}
dur={'chime':2.0,'click':1.04,'glitch':1.02,'hit':.57,'impact-drop':4.06,'impact-hook':1.22,'paper':.45,'pop':.48,'riser':4.81,'shimmer':3.0,'sparkle':2.33,'subdrop':1.1,'thud':.59,'tick':.17,'whoosh':.78,'whoosh2':1.27}
q=lambda o:html.escape(json.dumps(o,separators=(',',':')),quote=True)
clips=[]; n=0; wsw=0; lanes=[]
def lane(st,en):
    for i,e in enumerate(lanes):
        if e<=st: lanes[i]=en; return 3+i
    lanes.append(en); return 3+len(lanes)-1
def add(f,at,vol,align=True):
    global n; n+=1; st=max(0,at-(peaks[f] if align else 0)); clips.append(f'<audio id="sfx-{n:03d}" src="assets/sfx/{f}.wav" data-audio-group="sfx" data-start="{st:.3f}" data-duration="{dur[f]:.2f}" data-track-index="{lane(st,st+dur[f])}" data-volume="{min(1,vol):.2f}"></audio>')
for h in hits:
    nm=h['name']; g=h.get('gain',.4)
    if nm=='type': continue
    if nm=='impact': add('impact-hook' if h['at']<10 else 'impact-drop', h['at'], .5 if h['at']<10 else .6); continue
    if nm=='sparkle' and h['at']>80: add('shimmer',h['at'],.42); continue
    f,base=MAP[nm]
    if f=='whoosh': wsw+=1; f='whoosh' if wsw%2 else 'whoosh2'
    add(f,h['at'],base*max(.6,min(1.4,g/.35)))
# one real keyboard take over the typing (build.mp4 5.0–7.4 s at 3.5x → film 1.43–2.11 s)
n+=1; clips.append(f'<audio id="sfx-{n:03d}" src="assets/sfx/keyboard.wav" data-audio-group="sfx" data-start="1.43" data-duration="0.70" data-media-start="2.0" data-track-index="{lane(1.43,2.13)}" data-volume="0.30"></audio>')
# riser that ends on the Blueprint drop (bar 21)
n+=1; clips.append(f'<audio id="sfx-{n:03d}" src="assets/sfx/riser.wav" data-audio-group="sfx" data-start="{BAR(21)-4.81:.3f}" data-duration="4.81" data-track-index="{lane(BAR(21)-4.81,BAR(21))}" data-volume="0.22"></audio>')
import subprocess
vd=lambda k: float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f'{D}/mix/assets/vo/{k}.mp3'],capture_output=True,text=True).stdout)
vo=''.join(f'<audio id="vo-{k.lower()}" src="assets/vo/{k}.mp3" data-audio-group="voiceover" data-start="{s}" data-duration="{vd(k):.3f}" data-track-index="1" data-volume="1"></audio>\n' for k,s in starts.items())
bedauto={'version':1,'lanes':[{'target':'volume','points':[{'t':0,'v':.5},{'t':5.2,'v':.5},{'t':5.45,'v':1},{'t':85.68,'v':1},{'t':85.84,'v':0}]}]}
master={'version':1,'nodes':[{'type':'compressor','id':'m1','label':'Glue','params':{'threshold':-20,'ratio':2,'attack':10,'release':150}},{'type':'truepeak','id':'m2','label':'Delivery ceiling','params':{'ceiling':-2}}]}
sfxbus={'version':1,'nodes':[{'type':'highpass','id':'s1','label':'Remove Rumble','params':{'frequency':70,'q':0.707}}]}
voxbus={'version':1,'nodes':[{'type':'highpass','id':'v1','label':'Remove Rumble','params':{'frequency':80,'q':0.707}},{'type':'compressor','id':'v2','label':'Evenness','params':{'threshold':-20,'ratio':2.5,'attack':8,'release':120}}]}
page=f'''<!doctype html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=1920, height=1080"><title>Kissflow Blueprint film — final mix</title>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<style>body{{margin:0;background:#000}}#root{{position:relative;width:100%;height:100%;overflow:hidden}}#pic{{position:absolute;inset:0;width:100%;height:100%}}</style></head>
<body>
<div id="root" data-composition-id="mix" data-start="0" data-width="1920" data-height="1080" data-duration="90" data-fx-chain="{q(master)}">
<video id="pic" src="assets/picture.mp4" muted data-start="0" data-duration="90" data-track-index="0"></video>
<hf-audio-group id="voiceover" data-label="Bria narration" data-volume="1" data-fx-chain="{q(voxbus)}"></hf-audio-group>
<hf-audio-group id="sfx" data-label="Real SFX" data-volume="0.9" data-fx-chain="{q(sfxbus)}"></hf-audio-group>
{vo}<audio id="music-bed" src="assets/music-bed.wav" data-audio-group="music" data-start="0" data-duration="90" data-track-index="2" data-volume="0.55" data-automation="{q(bedauto)}"></audio>
{chr(10).join(clips)}
</div>
<script>const tl = gsap.timeline({{ paused: true }}); tl.to({{}}, {{ duration: 90 }}); window.__timelines["mix"] = tl;</script>
</body></html>'''
open(f'{D}/mix/index.html','w').write(page); print('clips',len(clips))
