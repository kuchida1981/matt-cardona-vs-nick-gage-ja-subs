"""en.srt に、音声確認の結果を字幕番号指定で反映する。元の文字列が一致しない場合は何もしない。"""
import re, sys
FIXES = {  # 字幕番号: (元の文字列, 新しい文字列)
    63:  ("death mat Russell", "death match wrestler"),
    74:  ("to give me back", "to get me back"),
    76:  ("NBK's", "MDK's"),
    93:  ("same role.", "same world."),
    219: ("I wasn't right away with successful wrestling.", "I wasn't right away with successful wrestling. [?]"),
    272: ("This is the outside.", "This is the outsider."),
    273: ("Nick Gage is the outside.", "Nick Gage is the outsider."),
    281: ("mack cardona", "matt cardona"),
    308: ("Zach Ryder", "Zack Ryder"),
    346: ("have it cold or", "have it called or"),
    402: ("They fucking love Mickie and they", "who fucking loves Nick Gage and they"),
    409: ("Oh, Lexus Gage through the glass.", "Oh, suplexes Gage through the glass. [?]"),
    439: ("Slavski! Ravski! Ravski! Ravski! Ravski!", "[Crowd chanting] [?]"),
    444: ("GCW champion, are you good?", "GCW champion, are you good? [?]"),
    446: ("Good, oh, whoa.", "Good, oh, whoa. [?]"),
    460: ("He looked like he was mad at us.", "He looked like he was mad at us. [?]"),
    461: ("He looked like he was in a battle", "He looked like he was in a battle [?]"),
    467: ("He has a fucking trunk.", "He gets a fucking chunk."),
    468: ("Here's two.", "Here's two. [?]"),
    471: ("I'm so worried.", "I was so worried."),
    474: ("Hi, love you.", "I love you."),
    475: ("Wanna see the belt?", "Want to see the belt?"),
    476: ("Love you.", "Yes."),
    478: ("John Carlyle.", "I got to call my, uh,"),
    479: ("When was the last time you played, did this before?", "When was the last time you played, did this match?"),
    507: ("You know, it's just kind of scary", "You know, which is kind of scary."),
    508: ("They walk it out", "Like walking out,"),
    509: ("Like there were people in my face then whether they walk would have those finite security",
          "like there were people in my face and they wouldn't let me walk, whatever. It was fine. I had security."),
    510: ("But they're just like throwing shit like who knows what they're gonna throw next",
          "But when they're just like throwing fucking, like, who knows what they're going to throw next?"),
    527: ("proresentees.com slash macrotown", "prowrestlingtees.com/merch"),
    540: ("I'm drawing this.", "I'm drawing this. [?]"),
    594: ("scream in the show.", "scream in the shower."),
    624: ("Warrant Out, man,", "Warrant Out, man, [?]"),
}
path = sys.argv[1]
blocks = re.split(r"\n\s*\n", open(path, encoding="utf-8").read().strip())
n = 0
for i, b in enumerate(blocks):
    l = b.split("\n"); num = int(l[0])
    if num in FIXES:
        old, new = FIXES[num]; text = "\n".join(l[2:])
        if old in text:
            blocks[i] = "\n".join(l[:2] + [text.replace(old, new)]); n += 1
        else:
            print(f"SKIP #{num}: 元の文字列が一致しない: {text!r}")
out = "\n\n".join(blocks) + "\n"
out, k = re.subn(r"\b(?:fdj|FDJ|mdj|MDJ|NBK)\b", "MDK", out)
open(path, "w", encoding="utf-8").write(out)
print(f"applied {n}/{len(FIXES)} fixes, {k} acronym replacements")
