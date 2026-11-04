#!/bin/bash
# picture (huashu-motion, silent) → HyperFrames mix (Bria + carved bed + real SFX) → loudness master
set -euo pipefail
D=/Users/abhiram/Documents/kissflow-blueprint-film
OUT=${1:-v9}
cd "$D"
rm -f index-*.png
/Users/abhiram/.claude/skills/huashu-motion/bin/om render . --silent > tools/render-picture.log 2>&1
PIC=$(ls -t out/kissflow-blueprint-film-v*.mp4 | grep -v -e social -e final -e hf | head -1)
echo "picture $PIC"
ffmpeg -loglevel error -y -i "$PIC" -an -c:v copy mix/assets/picture.mp4
cd mix
npx hyperframes render -q delivery -o "../out/kissflow-blueprint-film-$OUT-hf.mp4" > ../tools/render-mix.log 2>&1
cd "$D/out"
IN="kissflow-blueprint-film-$OUT-hf.mp4"
J=$(ffmpeg -nostats -i "$IN" -af loudnorm=I=-16:TP=-1.5:LRA=7:print_format=json -f null - 2>&1 | sed -n "/^{/,/^}/p")
read I TP LRA TH OFF < <(echo "$J" | python3 -c "import sys,json;d=json.load(sys.stdin);print(d['input_i'],d['input_tp'],d['input_lra'],d['input_thresh'],d['target_offset'])")
ffmpeg -loglevel error -y -i "$IN" -c:v copy -af "loudnorm=I=-16:TP=-1.5:LRA=7:measured_I=$I:measured_TP=$TP:measured_LRA=$LRA:measured_thresh=$TH:offset=$OFF:linear=true,aresample=48000" -c:a aac -b:a 192k "kissflow-blueprint-film-$OUT-final.mp4"
ffmpeg -nostats -i "kissflow-blueprint-film-$OUT-final.mp4" -af ebur128=peak=true -f null - 2>&1 | grep -E "^\s+(I|LRA|Peak):"
echo "DONE $D/out/kissflow-blueprint-film-$OUT-final.mp4"
