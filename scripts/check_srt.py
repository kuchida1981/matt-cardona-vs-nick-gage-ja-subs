import re, sys, collections
txt = open(sys.argv[1], encoding="utf-8").read().strip()
blocks = re.split(r"\n\s*\n", txt)
def t(s):
    h, m, r = s.split(":"); sec, ms = r.split(",")
    return int(h)*3600 + int(m)*60 + int(sec) + int(ms)/1000
cues = []
for b in blocks:
    l = b.split("\n")
    m = re.match(r"(\S+) --> (\S+)", l[1])
    cues.append((int(l[0]), t(m[1]), t(m[2]), " ".join(l[2:]).strip()))
print("cues:", len(cues), "first:", cues[0][1], "last end:", cues[-1][2])
print("numbering ok:", [c[0] for c in cues] == list(range(1, len(cues)+1)))
print("overlaps:", sum(1 for a, b in zip(cues, cues[1:]) if b[1] < a[2] - 0.001))
print("zero/neg dur:", sum(1 for c in cues if c[2] <= c[1]))
print("dur>8s:", sum(1 for c in cues if c[2]-c[1] > 8), " >42 chars:", sum(1 for c in cues if len(c[3]) > 42))
gaps = [(b[1]-a[2], a[2]) for a, b in zip(cues, cues[1:])]
print("gaps>10s:", [(round(g,1), round(e)) for g, e in gaps if g > 10])
cnt = collections.Counter(c[3] for c in cues)
print("repeated >=4:", [(k, v) for k, v in cnt.most_common(8) if v >= 4])
words = " ".join(c[3] for c in cues)
for w in ["Cardona","Gage","GCW","Zack","Ryder","MDK","Homecoming","pizza","Gauge","Cardonna","Kardona","Nick Gauge","GC W"]:
    print(w, len(re.findall(re.escape(w), words, re.I)), end=" | ")
