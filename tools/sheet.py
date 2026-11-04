import subprocess,sys,glob,re
fs=sorted(glob.glob(sys.argv[1]+'/index-*.png'),key=lambda f:float(re.findall(r'-([\d.]+)s',f)[0]))
n=len(fs);cols=4;w=480;h=270
args=[];[args.extend(['-i',f]) for f in fs]
fc=''.join(f'[{i}:v]scale={w}:{h}[s{i}];' for i in range(n))+''.join(f'[s{i}]' for i in range(n))+f'xstack=inputs={n}:layout='+'|'.join(f'{(i%cols)*w}_{(i//cols)*h}' for i in range(n))
subprocess.run(['ffmpeg','-loglevel','error','-y',*args,'-filter_complex',fc,sys.argv[2]],check=True)
print(n)
