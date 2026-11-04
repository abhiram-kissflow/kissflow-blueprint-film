import json,os,re,base64,urllib.request
key=os.environ.get('ELEVENLABS_API_KEY') or re.search(r'ELEVENLABS_API_KEY=["\']?([^"\'\s]+)',open(os.path.expanduser('~/.zshrc')).read()).group(1)
text="But what you get is a prototype. And prototypes don't belong in production. Enterprise software demands SDLC governance: requirements, design, sign-off, testing. That process takes months."
body={"text":text,"model_id":"eleven_multilingual_v2","previous_text":"Vibe coding can build you an app in minutes.","next_text":"Kissflow's Agentic App Builder runs that entire process.","voice_settings":{"stability":0.45,"similarity_boost":0.8,"style":0.0,"use_speaker_boost":True}}
r=urllib.request.Request("https://api.elevenlabs.io/v1/text-to-speech/mnztdMnkPU71C39L0hTx/with-timestamps",json.dumps(body).encode(),{"xi-api-key":key,"Content-Type":"application/json"})
d=json.load(urllib.request.urlopen(r,timeout=120))
open('assets/vo3/opening.mp3','wb').write(base64.b64decode(d['audio_base64']))
a=d['alignment'];w=[];cur='';s=None
for c,st,en in zip(a['characters'],a['character_start_times_seconds'],a['character_end_times_seconds']):
    if c==' ':
        if cur:w.append([cur,round(s,3),round(e,3)]);cur=''
        continue
    if not cur:s=st
    cur+=c;e=en
if cur:w.append([cur,round(s,3),round(e,3)])
json.dump(w,open('assets/vo3/opening.words.json','w'))
print(w)
