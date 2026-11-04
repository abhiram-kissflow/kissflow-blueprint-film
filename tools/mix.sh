#!/bin/bash
# Final mix: Bria voice + effects (om sound) + ElevenLabs SFX (gate confirm, end reveal, paper press) + the v9 ElevenLabs bed ducked under the voice.
set -euo pipefail
cd "$(dirname "$0")/.."
FILM="$1"; OUT="$2"
GATE=43913; END=85733; PRESS=86083
ffmpeg -loglevel error -y -i assets/voice.wav -i assets/sound.wav -i assets/music/bed-v19.wav \
  -i assets/sfx-el/gate-confirm.mp3 -i assets/sfx-el/end-reveal.mp3 -i assets/sfx-el/paper-press.mp3 -filter_complex "\
[0:a]aresample=48000,volume=3dB,asplit=2[v][key];\
[1:a]aresample=48000,volume=8dB,acompressor=threshold=0.1:ratio=3:attack=2:release=80[fx];\
[3:a]aresample=48000,volume=-9dB,adelay=${GATE}:all=1[s1];\
[4:a]aresample=48000,volume=-8dB,adelay=${END}:all=1[s2];\
[5:a]aresample=48000,volume=-14dB,adelay=${PRESS}:all=1[s3];\
[2:a]aresample=48000,volume=-12dB,volume='if(lt(t,5.2),0.55,1)':eval=frame,afade=t=out:st=89.44:d=4.0[bed0];\
[bed0][key]sidechaincompress=threshold=0.03:ratio=5:attack=25:release=400:makeup=1[bed];\
[v][fx][s1][s2][s3][bed]amix=inputs=6:normalize=0,alimiter=limit=0.89[mix]" -map "[mix]" -t 93.733 tools/mix-pre.wav
ffmpeg -loglevel error -y -i tools/mix-pre.wav -af loudnorm=I=-14:TP=-1.5:LRA=7:print_format=summary -ar 48000 tools/mix.wav 2>/dev/null
ffmpeg -loglevel error -y -i "$FILM" -i tools/mix.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest "$OUT"
ffmpeg -nostats -i "$OUT" -af ebur128 -f null - 2>&1 | grep -E "^\s+I:" | tail -1
