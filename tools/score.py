# Generates the om-score (ABC) on the film's 112 BPM / 42-bar grid.
CH={'A':['A','c','e','a'],'Fm':['F','A','c','f'],'D':['D','F','A','d'],'E':['E','G','B','e'],
    'Bm':['B,','D','F','B'],'C#':['C','^E','G','c']}
BASS={'A':'A,,','Fm':'F,,','D':'D,,','E':'E,,','Bm':'B,,,','C#':'C,,'}
PAD={'A':'[Ace]','Fm':'[FAc]','D':'[DFA]','E':'[EGB]','Bm':'[B,DF]','C#':'[C^EG]'}
bars=['A','A','D', 'Fm','D','E', 'A','E', 'A','Fm','D', 'A','E','Fm','D',
      'Fm','D','Bm','C#', 'E', 'A','Fm','D','E','A', 'D','A','E','A', 'A','E', 'Fm','D','E',
      'A','D','E', 'Fm','D','E', 'A','A']
marks={1:'hook',4:'problem',7:'spine',9:'requirements',12:'design',16:'verify',20:'stop',21:'blueprint',
       26:'signoff',30:'build',32:'test',35:'version',38:'resolve',41:'end'}
dyn={1:'!mf!',4:'!p!',7:'!mf!',16:'!f!',21:'!ff!',26:'!mf!',30:'!mf!',38:'!mp!',41:'!mf!'}
dense=set(range(1,4))|set(range(16,20))|set(range(21,26))|set(range(30,35))
MA=[];MB=[];PN=[];ST=[];PZ=[];DR=[]
for i,c in enumerate(bars,1):
    t=CH[c]; pre=(f'!mark:{marks[i]}! ' if i in marks else '')+dyn.get(i,'')
    if i==20:
        MA.append(pre+'z16');MB.append('z16');PN.append('z16');ST.append('!pp!'+PAD[c]+'16');PZ.append('z16');DR.append('z16');continue
    if i in (41,42):  # motif A C# E A as the sonic logo
        MA.append(pre+(' A2c2e2a2 a8' if i==41 else ' e2c2A4 A8'));MB.append('z16');
        PN.append('[A,EAc]16');ST.append(PAD[c]+'16');PZ.append(BASS[c]+'8 z8');DR.append('z16');continue
    if i in dense:
        seq=[t[0],t[1],t[2],t[3],t[2],t[1],t[0],t[1],t[2],t[3],t[2],t[1],t[2],t[3],t[2],t[1]]
        MA.append(pre+' '+''.join(seq))
        seqb=[t[1],t[2],t[3],t[2]]*4; MB.append(''.join(n+'' for n in seqb))
    else:
        MA.append(pre+' '+''.join(n+'2' for n in [t[0],t[1],t[2],t[3],t[2],t[1],t[2],t[3]]))
        MB.append('z2'+''.join(n+'2' for n in [t[2],t[1],t[3],t[2],t[1],t[2]])+'z2')
    # motif on station ticks (first bar of each scene) in piano
    PN.append(('A2c2e2a2 '+PAD[c]+'8') if i in marks and i not in (1,) else PAD[c]+'16')
    ST.append(PAD[c].replace('[','[').replace(']',']')+'16' if i>=7 else 'z16')
    PZ.append((BASS[c]+'4 z4 '+BASS[c]+'4 z4') if i>=9 else 'z16')
    if 16<=i<=19: DR.append('[C,,^F,,]^F,,^F,,^F,, [^C,,^F,,]^F,,^F,,^F,, [C,,^F,,]^F,,^F,,^F,, [^C,,^F,,]^F,,^F,,^F,,')
    elif 21<=i<=25 or 30<=i<=34: DR.append('C,,4 z4 C,,4 z4')
    else: DR.append('z16')
def voice(h,b): return h+'\n'+' | '.join(b)+' |]\n'
abc='X:1\nT:Kissflow AI Builder · the SDLC behind the speed\nM:4/4\nL:1/16\nQ:1/4=112\nK:A\n'
abc+=voice('V:MA inst=marimba gain=0.62 role=melody',MA)+voice('V:MB inst=marimba gain=0.42',MB)+voice('V:PN inst=piano gain=0.42',PN)
abc+=voice('V:ST inst=strings gain=0.34',ST)+voice('V:PZ inst=pizz gain=0.55',PZ)+voice('V:DR inst=drums kit=acoustic gain=0.45',DR)
abc=abc.replace('!mark:blueprint! !ff!','!mark:blueprint! !ff! !hit!')
open('tools/score.abc','w').write(abc); print(len(bars),'bars')
