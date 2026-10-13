"""ja/*.txt の訳文と en.srt のタイムコードから ja.srt を組み立て、読みやすさを検査する。
訳文ファイルの形式: 「#番号」の行のあとに1〜2行の訳、空行で区切る。「# 」で始まる行はコメント。
タイミング指示 (「#番号」の直後に書く。時刻は MM:SS.s または H:MM:SS.s):
  @start T   開始時刻を変える
  @end T     終了時刻を変える
  @until M   終了時刻を en.srt の M 番の終わりにする (結合。M 番側は @drop にする)
  @drop      この字幕を出力しない
「#番号+」は同じ番号の字幕を時間で分けた2つ目 (話者が変わる場合など)。@start が必須。
そのほか、表示時間が短い字幕は次の字幕の直前まで自動で延長する (開始時刻は動かさない)。
usage: python3 -I scripts/build_ja.py en.srt ja ja.srt"""
import glob, re, sys, unicodedata
GAP = 0.04      # 次の字幕との最小の隙間 (秒)
MIN_DUR = 1.0   # 最短の表示時間
CPS = 7.0       # 自動延長の目安 (字/秒)
MAX_DUR = 7.0
def width(s):  # 全角=1, 半角=0.5
    return sum(1 if unicodedata.east_asian_width(c) in "WFA" else 0.5 for c in s)
def parse(p):
    out = {}
    for b in re.split(r"\n\s*\n", open(p, encoding="utf-8").read().strip()):
        l = b.split("\n"); out[int(l[0])] = (l[1], l[2:])
    return out
def sec(tc):
    p = tc.strip().replace(",", ".").split(":")
    t = 0.0
    for x in p: t = t * 60 + float(x)
    return t
def ts(t):
    t = round(t * 1000); h, r = divmod(t, 3600000); m, r = divmod(r, 60000); s, ms = divmod(r, 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"
en = parse(sys.argv[1]); ent = {}
for n, (tc, _) in en.items():
    a, b = tc.split(" --> "); ent[n] = (sec(a), sec(b))
ja = {}
for p in sorted(glob.glob(sys.argv[2] + "/*.txt")):
    for b in re.split(r"\n\s*\n", open(p, encoding="utf-8").read().strip()):
        lines = [x for x in b.split("\n") if x.strip() and not x.startswith("# ")]
        if not lines: continue
        m = re.fullmatch(r"#(\d+)(\+\d*)?", lines[0].strip())
        if not m: print(f"形式エラー: {p}: {lines[0]!r}"); continue
        n = int(m[1]); key = (n, m[2] or "")
        if key in ja: print(f"重複: #{n}{key[1]}")
        if n not in en: print(f"en.srt にない番号: #{n}"); continue
        text = []; opt = {}
        for x in lines[1:]:
            if x.startswith("@"):
                k, _, v = x[1:].partition(" "); opt[k] = v.strip()
            else: text.append(x)
        ja[key] = (text, opt)
cues = []  # [start, end, text, key]
for key in sorted(ja):
    n = key[0]; text, opt = ja[key]
    if "drop" in opt: continue
    s, e = ent[n]
    if key[1]:
        if "start" not in opt: print(f"@start が必要: #{n}{key[1]}"); continue
        e = ent[n][1]
    if "start" in opt: s = sec(opt["start"])
    if "until" in opt: e = ent[int(opt["until"])][1]
    if "end" in opt: e = sec(opt["end"])
    cues.append([s, e, text, key])
cues.sort(key=lambda c: (c[0], c[3]))
# 分割元の終了時刻を、分割後の開始時刻までに詰める
for i, c in enumerate(cues[:-1]):
    nx = cues[i + 1]
    if nx[3][0] == c[3][0] and nx[3][1] and c[1] > nx[0]: c[1] = nx[0]
# 短い字幕を延長する
ext = 0
for i, c in enumerate(cues):
    w = sum(width(x) for x in c[2])
    need = min(MAX_DUR, max(MIN_DUR, w / CPS))
    lim = cues[i + 1][0] - GAP if i + 1 < len(cues) else c[0] + need
    new = min(c[0] + need, lim)
    if new > c[1] + 1e-6: c[1] = new; ext += 1
warn = 0
for i, (s, e, L, key) in enumerate(cues, 1):
    d = e - s; msgs = []
    if len(L) > 2: msgs.append("3行以上")
    if any(width(x) > 22 for x in L): msgs.append("1行が22字超")
    if d < 0.5: msgs.append(f"表示{d:.2f}秒")
    cps = sum(width(x) for x in L) / max(d, .1)
    if cps > 9: msgs.append(f"{cps:.1f}字/秒")
    if msgs: warn += 1; print(f"警告 #{key[0]}{key[1]} ({d:.1f}s): {', '.join(msgs)} | {' / '.join(L)}")
with open(sys.argv[3], "w", encoding="utf-8") as f:
    f.write("\n".join(f"{i}\n{ts(s)} --> {ts(e)}\n" + "\n".join(L) + "\n" for i, (s, e, L, k) in enumerate(cues, 1)))
done = {k[0] for k in ja}
miss = [n for n in en if n not in done]
if miss: print(f"訳がない en.srt の番号: {miss[:20]}")
print(f"出力 {len(cues)} 件 (延長 {ext} 件), 警告 {warn} 件 -> {sys.argv[3]}")
