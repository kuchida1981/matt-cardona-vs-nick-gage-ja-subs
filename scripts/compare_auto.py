"""YouTube「文字起こし」パネルのコピー(work/yt_auto_en.txt)と en.srt を単語単位で突き合わせ、食い違いを出力する。"""
import re, sys, difflib
LINE = re.compile(r"^(\d+):(\d{2})(\d+(?: 分(?: \d+ 秒)?| 秒))(.*)$")
def load_auto(p):
    out = []
    for raw in open(p, encoding="utf-8"):
        raw = raw.rstrip("\n")
        if raw.startswith("チャプター") or not raw.strip(): continue
        m = LINE.match(raw)
        if m: out.append((int(m[1]) * 60 + int(m[2]), m[4]))
    return out
def t(s):
    h, m, r = s.split(":"); sec, ms = r.split(",")
    return int(h) * 3600 + int(m) * 60 + int(sec) + int(ms) / 1000
def load_srt(p):
    out = []
    for b in re.split(r"\n\s*\n", open(p, encoding="utf-8").read().strip()):
        l = b.split("\n"); m = re.match(r"(\S+) --> (\S+)", l[1]); out.append((t(m[1]), t(m[2]), " ".join(l[2:])))
    return out
MASK = {"fuck", "fucking", "fucked", "shit", "bitch", "ass", "damn", "bullshit", "motherfucker", "fuckin"}
FILL = {"uh", "um", "like", "you", "know", "so", "oh", "yeah", "well", "just", "i", "mean", "okay", "right", "the", "a", "and", "that", "it", "to", "of", "is"}
EXP = {"wanna": "want to", "gonna": "going to", "gotta": "got to", "kinda": "kind of", "cuz": "because"}
def words(text, srt=False):
    text = re.sub(r"\[[^\]]*\]", " ", text)           # [music] [cheering] [ __ ]
    text = text.lower().replace("’", "'")
    for k, v in EXP.items(): text = re.sub(rf"\b{k}\b", v, text)
    ws = re.findall(r"[a-z0-9']+", text)
    return [w for w in ws if w not in MASK]            # 伏せ字は両側から除く
auto = load_auto(sys.argv[2]); srt = load_srt(sys.argv[1])
A, Atime = [], []
for ts, tx in auto:
    for w in words(tx): A.append(w); Atime.append(ts)
S, Stime = [], []
for s, e, tx in srt:
    ws = words(tx)
    for i, w in enumerate(ws): S.append(w); Stime.append(s + (e - s) * (i + .5) / max(len(ws), 1))
sm = difflib.SequenceMatcher(None, S, A, autojunk=False)
rows = []
for op, i1, i2, j1, j2 in sm.get_opcodes():
    if op == "equal": continue
    a = [w for w in S[i1:i2]]; b = [w for w in A[j1:j2]]
    if [w for w in a if w not in FILL] == [w for w in b if w not in FILL]: continue   # 言いよどみだけの差
    if [w.rstrip("s") for w in a if w not in FILL] == [w.rstrip("s") for w in b if w not in FILL]: continue
    ts = Stime[i1] if i1 < len(S) else Stime[-1]
    rows.append((ts, " ".join(a), " ".join(b)))
merged = []
for r in rows:
    if merged and r[0] - merged[-1][0] < 3: merged[-1] = (merged[-1][0], (merged[-1][1] + " | " + r[1]).strip(" |"), (merged[-1][2] + " | " + r[2]).strip(" |"))
    else: merged.append(r)
print(f"auto lines: {len(auto)}, words: srt={len(S)} auto={len(A)}, ratio={sm.ratio():.3f}, hunks={len(rows)}, merged={len(merged)}")
with open(sys.argv[3], "w", encoding="utf-8") as f:
    f.write("# en.srt と YouTube 自動字幕の差分\n\n時刻は en.srt 基準。左: en.srt (Whisper) / 右: YouTube 自動字幕。言いよどみ・伏せ字・表記ゆれは除外済み。\n\n")
    for ts, a, b in merged: f.write(f"- [{int(ts)//60:02d}:{int(ts)%60:02d}] `{a or '∅'}` ⇄ `{b or '∅'}`\n")
