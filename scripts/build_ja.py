"""ja/*.txt の訳文と en.srt のタイムコードから ja.srt を組み立て、読みやすさを検査する。
訳文ファイルの形式: 「#番号」の行のあとに1〜2行の訳、空行で区切る。「# 」で始まる行はコメント。
usage: python3 -I scripts/build_ja.py en.srt ja ja.srt"""
import glob, re, sys, unicodedata
def width(s):  # 全角=1, 半角=0.5
    return sum(1 if unicodedata.east_asian_width(c) in "WFA" else 0.5 for c in s)
def parse(p):
    out = {}
    for b in re.split(r"\n\s*\n", open(p, encoding="utf-8").read().strip()):
        l = b.split("\n"); out[int(l[0])] = (l[1], l[2:])
    return out
en = parse(sys.argv[1]); ja = {}
for p in sorted(glob.glob(sys.argv[2] + "/*.txt")):
    for b in re.split(r"\n\s*\n", open(p, encoding="utf-8").read().strip()):
        lines = [x for x in b.split("\n") if x.strip() and not x.startswith("# ")]
        if not lines: continue
        m = re.fullmatch(r"#(\d+)", lines[0].strip())
        if not m: print(f"形式エラー: {p}: {lines[0]!r}"); continue
        n = int(m[1])
        if n in ja: print(f"重複: #{n}")
        if n not in en: print(f"en.srt にない番号: #{n}"); continue
        ja[n] = lines[1:]
def sec(tc):
    h, m, r = tc[:12].split(":"); s, ms = r.split(","); return int(h)*3600 + int(m)*60 + int(s) + int(ms)/1000
warn = 0
for n in sorted(ja):
    tc = en[n][0]; d = sec(tc.split(" --> ")[1]) - sec(tc.split(" --> ")[0]); L = ja[n]
    msgs = []
    if len(L) > 2: msgs.append("3行以上")
    if any(width(x) > 22 for x in L): msgs.append("1行が22字超")
    cps = sum(width(x) for x in L) / max(d, .1)
    if cps > 9: msgs.append(f"{cps:.1f}字/秒")
    if msgs: warn += 1; print(f"警告 #{n} ({d:.1f}s): {', '.join(msgs)} | {' / '.join(L)}")
with open(sys.argv[3], "w", encoding="utf-8") as f:
    f.write("\n".join(f"{n}\n{en[n][0]}\n" + "\n".join(ja[n]) + "\n" for n in sorted(ja)))
print(f"訳済み {len(ja)} / {len(en)} 件, 警告 {warn} 件 -> {sys.argv[3]}")
