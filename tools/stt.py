import json,os,re,sys,subprocess,uuid,urllib.request
key=os.environ.get('ELEVENLABS_API_KEY') or re.search(r'ELEVENLABS_API_KEY=["\']?([^"\'\s]+)',open(os.path.expanduser('~/.zshrc')).read()).group(1)
b=uuid.uuid4().hex
body=b''
for k,v in [('model_id','scribe_v1'),('language_code','en'),('tag_audio_events','false')]:
    body+=f'--{b}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode()
body+=f'--{b}\r\nContent-Disposition: form-data; name="file"; filename="v.wav"\r\nContent-Type: audio/wav\r\n\r\n'.encode()+open('assets/voice.wav','rb').read()+f'\r\n--{b}--\r\n'.encode()
r=urllib.request.Request('https://api.elevenlabs.io/v1/speech-to-text',body,{'xi-api-key':key,'Content-Type':f'multipart/form-data; boundary={b}'})
d=json.load(urllib.request.urlopen(r,timeout=170))
w=[[x['text'],round(x['start'],2),round(x['end'],2)] for x in d['words'] if x['type']=='word']
json.dump(w,open('assets/voice.scribe.json','w'))
print(' '.join(f"{t}@{s}" for t,s,e in w))
