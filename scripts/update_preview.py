"""docs/index.html に埋め込んだ字幕 (srt-data) を ja.srt の内容で差し替える。
usage: python3 -I scripts/update_preview.py"""
import re
p = "docs/index.html"; h = open(p, encoding="utf-8").read()
srt = open("ja.srt", encoding="utf-8").read().strip()
assert "</script" not in srt
new, n = re.subn(r'(<script type="text/plain" id="srt-data">).*?(</script>)', lambda m: m[1] + srt + "\n" + m[2], h, count=1, flags=re.S)
assert n == 1; open(p, "w", encoding="utf-8").write(new)
