# 音声で確認する箇所

`en.srt` (large-v3) と `work/en_turbo.srt` (large-v3-turbo) を比べて、意味・固有名詞に関わる食い違いを選んだ。
時刻は mm:ss。`mpv` なら `mpv --start=MM:SS work/audio.mp3` で該当箇所から再生できる。
確認したら、結果欄に正しい表記を書く。

## A. 固有名詞・団体名 (優先)

| 時刻 | large-v3 | turbo | 見立て | 結果 |
|------|----------|-------|--------|------|
| 02:56 | gcw | bcw | 文脈次第。GCW か別の団体か | GCW です|
| 03:57 | russell | trustee | 人名の可能性 | 自己紹介している. "wrestler" だと思う |
| 04:36 | nbk's | mdk's | turbo が妥当 (MDK) | MDK ですね. "Murder Death Kill" の略で Nick Gage のこと? |
| 04:48 | fdj ×3 | mdj ×3 | MDK のチャントか。要確認 | ただしい. "MDK" のチャント |
| 14:17 | mack | matt | turbo が妥当 | "matt" です (matt cardona のmatt)|
| 15:23 | zach | zack | Zack Ryder の綴りは zack | あってる. zack です |
| 21:24 | love mickie | loved mickey | 人名 (Mickie か Mickey か) | "who fucking **loves nick** gage and they wanted to see him kill me." たぶんこうです |
| 22:01 | lexus | the flexes | 人名・語句か。要確認 | "plexes GAGE through the glass." といってると思う. 人名・固有名詞ではない気がするが…… |
| 23:33 | slavski ravski… | krasnowski… | 人名のチャントか。綴り要確認 | わからんなあ... matt へのhateを表すチャントっぽい. なんだと思う? 該当する登場人物ではないように思う|
| 25:14 | john carlyle | (なし) | 人名か。turbo は拾っていない | 後述するのを見てください. YouTube自動生成字幕の書き起こし |
| 26:54 | proresentees | prowrestlingtees | 商品名・店名。turbo が妥当か | たぶん "prowrestlings" といってる. "i have new merch on prowrestlings.com/merch." と字幕がでてました |
| 31:12 | gcw … warrant | g c darby … roller | 意味が大きく違う。要確認 | たぶん GCW |
| 34:35 | atlantic | lake | 場所の名前。要確認 | "that room is um **linked** to GCW" こうかな? 字幕書き起こし|

### 25:07-25:14

Oh my gosh, I was so worried.
Yeah, I'm I'm fucking up, but I'm okay.
I love you.
Want to see the belt?
Yes.
Oh, yeah.
I got to call my uh
(被せ気味に) When was the last time you um played did ths match?

## B. 意味が変わる箇所

| 時刻 | large-v3 | turbo | 結果 |
|------|----------|-------|------|
| 04:29 | give | get | "give" に聞こえるが自動生成字幕は "get". "in my life to uh get me back to where I'm at now"|
| 05:41 | role i mean | house | "There was no reason for Matt Cardona and Nick Gage to occupy the same world. I mean, that's exactly what people needed to see it." 前後含め, このような字幕が生成されていた|
| 11:15 | away with | no way he was … in | 前後の字幕含め "Success, uh I didn't know success in wrestling. I was I know way to successful in wrestling, you know. It was very hard to get in the WWE. It's very hard to be successful."|
| 13:46 | outside | outsider | "outsider" |
| 16:49 | do cold do | called | "You want to have it have it called you want to have it done?" |
| 23:48 | are / good | how / killed | うーん 不明... |
| 24:30 | mad at us | battling this time | 聞き取れない...|
| 24:43 | trunk here's | chunk he has | "He gets a fuck chunk." に聞こえる |
| 26:16 | then whether … those finite … shit | and … wouldn't let me … everyone was behind | うまく聞き取れないが前後の字幕 "You know, which is kind of scary. Like walking out like there were people in my face and they wouldn't let me walk, whatever. It was fine. I had security. But when they're just like throwing fucking like who knows what they're going to throw next?"|
| 27:21 | i'm drawing | you're growing | 不明. |
| 29:21 | show | shower | "I know. All right. I'm going to scream in the shower." 字幕より|

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

## F. 自動字幕の全文との突き合わせ (`work/diff_srt_auto.md`)

### F-1. 反映済み (自動字幕のほうが明らかに正しい、または Whisper の抜け)

- `Put that camera right here` (03:27)、`I think that is my guard` (06:58)、`6'6", 250 pounds` (11:20)、`Steal the show` (17:39)、`Cardona with the light tube` (21:57)、`MDK is all about` (04:32)
- `GCW champion, how you feel?` (23:43)。直前の 01:21 の `Champion, how you feel?` とも一致
- 31:12 付近: `me and GCW, man, we made a plan when I was in prison to put this shit back on the map`。`Warrant Out` は Whisper の誤認識だった
- `John Carlo` に統一 (Whisper の `Giancarlo` を置換。5:22 では Whisper も `John Carlo`)
- Whisper が拾っていなかった発話を追加: `Champion, how you feel?` (01:27)、`He's got some black pants and shoes already. Roll. I got to put some knee pads on under here though, just in case.` (08:12)、`..., not even paying for it.` (38:28)

### F-2. Whisper のほうが正しかった (自動字幕は誤り・不採用)

`BCW` (02:56。正しくは GCW)、`an engage match` (05:22)、`Murder Death Joe Gang` (09:58。正しくは **Murder Death Kill**。`MDK` の展開形がこれで確定)、`Saboo` (27:40。正しくは Sabu)、`masses garden` (34:01。正しくは Madison Square Garden)、`grim mode` (10:35。`grind` のはず)

### F-3. 要再確認: 記入いただいた内容と、自動字幕ファイルの内容が食い違う箇所

記入時の「自動字幕」の記憶と、`work/yt_auto_en.txt` の内容が違っていました。**再度聞いて決めてください。**

| 時刻 | 記入内容 | `yt_auto_en.txt` | 現在の `en.srt` |
|------|----------|------------------|-----------------|
| 05:41 | `same world` | `same role` (Whisper も `role`) | `same world. [?]` (`room` の可能性もある) |
| 21:23 | `who fucking loves Nick Gage` | `love Mickey` (Whisper 2モデルも `Mickey/Mickie`) | `who fucking loves Nick Gage` (文脈上は妥当) |
| 25:11 | `I got to call my uh` | `Oh yeah, John Car.` (`John Carlo` は動画内で3回登場する人物) | `I got to call my, uh, [?]` |
| 25:15 | `did this match?` | `did this before?` (Whisper も `before`) | `did this match?` |
| 26:56 | `prowrestlings.com/merch` | `pros.com/mackro` (Whisper は `... slash macrotown`) | `prowrestlingtees.com/mackro. [?]` |

### F-4. 未決 (自動字幕と Whisper が割れている、またはどちらも怪しい)

- 10:04: `That's what I'm talking about.` ⇄ `That's my mother.` (後者を `[?]` 付きで採用)
- 19:21: `The fucking Scottish!` ⇄ `star` (後者を `[?]` 付きで採用)
- 24:30: `he was mad at us` ⇄ `he was awesome`。24:42 の `chunk` 周辺 (`chunks too`?)
- 27:30: `Those are fine.` ⇄ `The nose are fine.` (後者を `[?]` 付きで採用)
- 22:01: `suplexes` (推測) ⇄ 自動字幕 `flex his gauge`
- 11:14: `successful wrestling` の前後。自動字幕は `It wasn't I know it was successful in wrestling`
- 08:45: `rink` ⇄ `rank`。おそらく `ring`
- 23:07: `Get out of my house` ×5 は自動字幕にない (観客の声で拾えていない可能性)
