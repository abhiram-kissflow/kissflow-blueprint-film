#!/usr/bin/env python3
"""v18 voice track: V1 + new opening take (assets/vo3) + V4–V14 at the v18 starts. Writes assets/voice.wav"""
import subprocess,json
OPEN='assets/vo3/opening.mp3'
# source file, trim in, trim out, start time (s), gain dB
X=112/30
C=[('assets/vo2/V1.mp3',0,None,.35,0),
 (OPEN,0,4.62,2.85,0),(OPEN,4.85,12.1,7.115,0),(OPEN,12.25,None,14.0,0),
 ('assets/vo3/V4.mp3',0,4.5,15.9,0),('assets/vo/V5.mp3',0,1.85,20.4,0),('assets/vo/V5.mp3',1.85,None,24.29,0),('assets/vo/V6.mp3',0,None,26.2+X,0)]
C+= [(f'assets/vo/V{n}.mp3',0,None,s,0) for n,s in [(7,32.3+X),(8,43.1+X),(9,47.0+X),(10,53.8+X),(11,62.4+X),(12,73.1+X)]]
C+= [('assets/vo2/V13.mp3',0,None,79.6+X,0),('assets/vo2/V14.mp3',0,None,82.3+X,0)]
import sys
inp=[];fl=[]
for i,(f,a,b,s,g) in enumerate(C):
    inp+=['-i',f]
    tr=f"atrim={a}"+(f":{b}" if b else '')
    fl.append(f"[{i}:a]{tr},asetpts=PTS-STARTPTS,aresample=48000,afade=t=in:d=0.01,volume={g}dB,adelay={int(s*1000)}:all=1[a{i}]")
mix=''.join(f"[a{i}]" for i in range(len(C)))+f"amix=inputs={len(C)}:normalize=0,apad,atrim=0:93.733,aformat=channel_layouts=mono[o]"
subprocess.check_call(['ffmpeg','-v','error','-y',*inp,'-filter_complex',';'.join(fl+[mix]),'-map','[o]','-c:a','pcm_s16le','-ar','48000',sys.argv[1] if len(sys.argv)>1 else 'assets/voice.wav'])
