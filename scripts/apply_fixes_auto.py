"""YouTube 自動字幕との突き合わせ結果を en.srt に反映する(字幕番号は反映前の en.srt のもの)。
元の文字列が一致しない場合は何もしない。新規字幕は時刻指定で挿入し、番号を振り直す。"""
import re, sys
FIXES = {
    53:  ("Look at that camera, right here.", "Put that camera right here."),
    76:  ("the MDK's all about", "MDK is all about"),
    93:  ("same world.", "same world. [?]"),
    125: ("my version.", "my guard."),
    163: ("Let's be real.", "Let's be real. Pookie."),
    190: ("That's what I'm talking about.", "That's my mother. [?]"),
    222: ("You had to be six with six, 250 pounds.", "You had to be, uh, 6'6\", 250 pounds."),
    351: ("Feel the show", "Steal the show"),
    375: ("The fucking Scottish!", "The fucking star! [?]"),
    408: ("there's Carduno in the light tube", "there's Cardona with the light tube"),
    444: ("GCW champion, are you good? [?]", "GCW champion, how you feel?"),
    478: ("I got to call my, uh,", "I got to call my, uh, [?]"),
    527: ("prowrestlingtees.com/merch.", "prowrestlingtees.com/mackro. [?]"),
    545: ("Those are fine.", "The nose is fine. [?]"),
    618: ("You know like it's a genre now it's good to will well respected a little bit now.",
          "You know, like, it's a genre now. It's a little well respected, a little bit now."),
    624: ("me and GCW and Warrant Out, man, [?]", "me and GCW, man,"),
    626: ("with this shit back on the map.", "to put this shit back on the map."),
    628: ("All the guys had passed away", "For all the guys that passed away"),
    745: ("streaming it illegally.", "streaming it illegally, not even paying for it."),
}
INSERT = [  # (開始, 終了, テキスト)  秒
    (87.00, 87.80, "Champion, how you feel?"),
    (492.72, 494.00, "He's got some black pants and shoes already."),
    (495.22, 495.60, "Roll."),
    (495.60, 497.00, "I got to put some knee pads on under here though, just in case."),
    (1047.12, 1054.00, "I just told him, I told him he made an announcement, and I just told him [?]"),
]
EXTEND = {745: 2308.70}  # 字幕番号 -> 新しい終了時刻(秒)
def t(s):
    h, m, r = s.split(":"); sec, ms = r.split(","); return int(h)*3600 + int(m)*60 + int(sec) + int(ms)/1000
def f(x):
    ms = round(x*1000); return f"{ms//3600000:02d}:{ms//60000%60:02d}:{ms//1000%60:02d},{ms%1000:03d}"
cues = []
for b in re.split(r"\n\s*\n", open(sys.argv[1], encoding="utf-8").read().strip()):
    l = b.split("\n"); m = re.match(r"(\S+) --> (\S+)", l[1]); cues.append([int(l[0]), t(m[1]), t(m[2]), "\n".join(l[2:])])
n = 0
for c in cues:
    if c[0] in FIXES:
        old, new = FIXES[c[0]]
        if old in c[3]: c[3] = c[3].replace(old, new); n += 1
        else: print(f"SKIP #{c[0]}: 一致しない: {c[3]!r}")
    if c[0] in EXTEND: c[2] = EXTEND[c[0]]
for s, e, tx in INSERT: cues.append([0, s, e, tx])
cues.sort(key=lambda c: c[1])
k = 0
for c in cues:
    new = c[3].replace("Giancarlo", "John Carlo")
    if new != c[3]: k += 1; c[3] = new
open(sys.argv[1], "w", encoding="utf-8").write("\n".join(f"{i}\n{f(c[1])} --> {f(c[2])}\n{c[3]}\n" for i, c in enumerate(cues, 1)))
print(f"fixes {n}/{len(FIXES)}, inserted {len(INSERT)}, Giancarlo->John Carlo {k}, total {len(cues)}")
