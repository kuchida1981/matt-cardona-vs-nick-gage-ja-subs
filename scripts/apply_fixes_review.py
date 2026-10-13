"""review_list.md の F-3 / F-4 の回答を en.srt に反映する。文字列で照合し、一致が1件でない場合は何もしない。"""
import re, sys
FIXES = [  # (元の文字列, 新しい文字列, 正規表現か)
    ("same world. [?]", "same world.", False),
    ("I got to call my, uh, [?]", "John Carlo.", False),
    ("did this match?", "did this before?", False),
    ("The fucking star! [?]", "The fucking Scottish!", False),
    ("The nose is fine. [?]", "Those are fine.", False),
    (r"\brink\b", "ring", True),
    ("I wasn't right away with successful wrestling. [?]", "It wasn't, I know it was successful in wrestling. [?]", False),
]
path = sys.argv[1]
text = open(path, encoding="utf-8").read()
for old, new, rx in FIXES:
    cnt = len(re.findall(old, text)) if rx else text.count(old)
    if cnt != 1:
        print(f"SKIP ({cnt}件): {old}"); continue
    text = re.sub(old, new, text) if rx else text.replace(old, new)
    print(f"ok: {old} -> {new}")
open(path, "w", encoding="utf-8").write(text)
