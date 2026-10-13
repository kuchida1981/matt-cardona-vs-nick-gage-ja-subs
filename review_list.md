# 音声で確認する箇所

`en.srt` (large-v3) と `work/en_turbo.srt` (large-v3-turbo) を比べて、意味・固有名詞に関わる食い違いを選んだ。
時刻は mm:ss。`mpv` なら `mpv --start=MM:SS work/audio.mp3` で該当箇所から再生できる。
確認したら、結果欄に正しい表記を書く。

## A. 固有名詞・団体名 (優先)

| 時刻 | large-v3 | turbo | 見立て | 結果 |
|------|----------|-------|--------|------|
| 02:56 | gcw | bcw | 文脈次第。GCW か別の団体か | |
| 03:57 | russell | trustee | 人名の可能性 | |
| 04:36 | nbk's | mdk's | turbo が妥当 (MDK) | |
| 04:48 | fdj ×3 | mdj ×3 | MDK のチャントか。要確認 | |
| 14:17 | mack | matt | turbo が妥当 | |
| 15:23 | zach | zack | Zack Ryder の綴りは zack | |
| 21:24 | love mickie | loved mickey | 人名 (Mickie か Mickey か) | |
| 22:01 | lexus | the flexes | 人名・語句か。要確認 | |
| 23:33 | slavski ravski… | krasnowski… | 人名のチャントか。綴り要確認 | |
| 25:14 | john carlyle | (なし) | 人名か。turbo は拾っていない | |
| 26:54 | proresentees | prowrestlingtees | 商品名・店名。turbo が妥当か | |
| 31:12 | gcw … warrant | g c darby … roller | 意味が大きく違う。要確認 | |
| 34:35 | atlantic | lake | 場所の名前。要確認 | |

## B. 意味が変わる箇所

| 時刻 | large-v3 | turbo |
|------|----------|-------|
| 04:29 | give | get |
| 05:41 | role i mean | house |
| 11:15 | away with | no way he was … in |
| 13:46 | outside | outsider |
| 16:49 | do cold do | called |
| 23:48 | are / good | how / killed |
| 24:30 | mad at us | battling this time |
| 24:43 | trunk here's | chunk he has |
| 26:16 | then whether … those finite … shit | and … wouldn't let me … everyone was behind |
| 27:21 | i'm drawing | you're growing |
| 29:21 | show | shower |

## C. turbo だけが拾った発話 (large-v3 は空白)

| 時刻 | turbo の出力 (要約) |
|------|---------------------|
| 08:09 | 装備の準備をしている会話 (knee pads などの語) |
| 13:36 | 悪態を含む短い発話 |
| 17:35 | 「全員に話した」といった内容の長めの発話 |
| 38:33 | treading worldwide (末尾付近。large-v3 にもあり。表記要確認) |

## D. 信頼できないと判断したもの

- turbo の 37:39 付近: 同じ文の暴走的な繰り返し (hallucination)。**large-v3 を採用**。
- 繰り返しの掛け声 (`Get out of my house!` が large-v3 に5回、23:04 付近): turbo は拾っていない。実際に何回言っているか確認。

## E. 機械的に統一してよいもの (確認不要)

`wanna`/`want to`、`gonna`/`going to`、`1800`/`1 800`、`cuz`/`because`、`headfirst`/`head first`、`showboat`/`show boat`、`break`/`brake` (文脈で判断)。
