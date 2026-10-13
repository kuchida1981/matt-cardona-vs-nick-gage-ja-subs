import re, difflib, sys
def t(s):
    h,m,r=s.split(":");sec,ms=r.split(",");return int(h)*3600+int(m)*60+int(sec)+int(ms)/1000
def parse(p):
    out=[]
    for b in re.split(r"\n\s*\n",open(p,encoding="utf-8").read().strip()):
        l=b.split("\n");m=re.match(r"(\S+) --> (\S+)",l[1]);out.append((t(m[1]),t(m[2])," ".join(l[2:]).strip()))
    return out
def norm(s): return re.findall(r"[a-z0-9']+",s.lower())
def tl(c):  # words with approximate times, spread evenly in cue
    out=[]
    for s,e,x in c:
        w=norm(x)
        for i,wd in enumerate(w): out.append((wd,s+(e-s)*(i+0.5)/max(len(w),1)))
    return out
A=tl(parse(sys.argv[1])); B=tl(parse(sys.argv[2]))
sm=difflib.SequenceMatcher(None,[w for w,_ in A],[w for w,_ in B],autojunk=False)
diffs=[]
for op,i1,i2,j1,j2 in sm.get_opcodes():
    if op=="equal": continue
    a=" ".join(w for w,_ in A[i1:i2]); b=" ".join(w for w,_ in B[j1:j2])
    ts=(A[i1][1] if i1<len(A) else A[-1][1])
    diffs.append((ts,a,b))
# merge diffs closer than 3s
merged=[]
for d in diffs:
    if merged and d[0]-merged[-1][0]<3: merged[-1]=(merged[-1][0],merged[-1][1]+" | "+d[1],merged[-1][2]+" | "+d[2])
    else: merged.append(d)
print(f"raw diff hunks: {len(diffs)}, merged: {len(merged)}")
with open(sys.argv[3],"w",encoding="utf-8") as f:
    f.write("# en.srt (large-v3) と en_turbo.srt (large-v3-turbo) の差分\n\n時刻は en.srt 基準。左: large-v3 / 右: turbo\n\n")
    for ts,a,b in merged:
        f.write(f"- [{int(ts)//60:02d}:{int(ts)%60:02d}] `{a or '∅'}` ⇄ `{b or '∅'}`\n")
