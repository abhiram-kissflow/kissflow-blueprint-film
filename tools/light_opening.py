# Light, gradient opening with a neon green→blue glow around the BUILD letterforms.
P = '/Users/abhiram/Documents/kissflow-blueprint-film/index.html'
s = open(P).read()

# 1 · ground: light AI Builder blue with soft green / blue light pools
old_bg = "#s1{background:var(--night);opacity:1}"
new_bg = ("#s1{opacity:1;background:radial-gradient(900px 620px at 18% 22%,rgba(34,227,160,.20),transparent 62%),"
          "radial-gradient(1100px 760px at 86% 78%,rgba(31,128,255,.26),transparent 62%),"
          "radial-gradient(700px 500px at 60% 10%,rgba(207,44,145,.07),transparent 70%),"
          "linear-gradient(135deg,#F8FBFF 0%,#EDF5FE 55%,#E2EEFC 100%)}\n"
          "#s1 .glowsvg{position:absolute;inset:0;width:1920px;height:1080px;overflow:visible;pointer-events:none}")
assert old_bg in s; s = s.replace(old_bg, new_bg)

# tag reads on light ground
s = s.replace("color:rgba(255,255,255,.78)}\n#s1 .tag .plate{background:#fff;border-radius:14px;padding:12px 20px;display:flex}",
              "color:rgba(14,23,38,.72)}\n#s1 .tag .plate{background:#fff;border-radius:14px;padding:12px 20px;display:flex;box-shadow:0 8px 24px rgba(31,80,160,.14)}")

# 2 · glow layer behind the mask, gradient rim above it
old_html = '<div id="maskWrap">'
new_html = '<svg class="glowsvg" id="s1glow"></svg><div id="maskWrap">'
assert old_html in s; s = s.replace(old_html, new_html, 1)
old_cover = '<div id="cover"><div class="motion">'
new_cover = '<svg class="glowsvg" id="s1edge"></svg><div id="cover"><div class="motion">'
assert old_cover in s; s = s.replace(old_cover, new_cover, 1)

# 3 · build the SVG text in JS with the exact mask metrics; scale with the mask; fade on takeover
old_js = "  ['#maskWrap', '#counter'].forEach((s) => $(s).style.transformOrigin = origin);"
new_js = old_js + """
  const txt = (extra) => `<text x='960' y='700' font-size='${fs}' font-weight='900' letter-spacing='-6' text-anchor='middle' font-family='Helvetica Neue,Helvetica,Arial,sans-serif' ${extra}>${word}</text>`;
  const grad = `<defs><linearGradient id='ng' x1='0' y1='0' x2='1' y2='0'><stop offset='0' stop-color='#22E3A0'/><stop offset='.5' stop-color='#19C2E6'/><stop offset='1' stop-color='#1F80FF'/></linearGradient><filter id='gl' x='-20%' y='-40%' width='140%' height='180%'><feGaussianBlur stdDeviation='16'/></filter><filter id='gl2' x='-20%' y='-40%' width='140%' height='180%'><feGaussianBlur stdDeviation='5'/></filter></defs>`;
  $('#s1glow').innerHTML = grad + txt("fill='none' stroke='url(#ng)' stroke-width='34' filter='url(#gl)' opacity='.85'") + txt("fill='none' stroke='url(#ng)' stroke-width='10' filter='url(#gl2)'");
  $('#s1edge').innerHTML = grad.replace(/id='ng'/, "id='ng2'") + txt("fill='none' stroke='url(#ng2)' stroke-width='3'");
  ['#s1glow', '#s1edge'].forEach((q) => $(q).style.transformOrigin = origin);"""
assert old_js in s; s = s.replace(old_js, new_js, 1)

old_upd = "$('#cover').style.opacity = clamp01((e - .25) / .65); };"
new_upd = ("$('#cover').style.opacity = clamp01((e - .25) / .65);\n"
           "    const g = 1 - clamp01(e / .45); ['#s1glow', '#s1edge'].forEach((q) => { $(q).style.transform = `scale(${ms})`; $(q).style.opacity = g; });\n"
           "    $('#s1glow').style.filter = `hue-rotate(${lerp(st.d, -12, 12)}deg)`; };")
assert old_upd in s; s = s.replace(old_upd, new_upd, 1)

open(P, 'w').write(s)
print('ok')
