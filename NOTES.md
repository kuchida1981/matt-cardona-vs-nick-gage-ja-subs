# 作業ログ

あとから振り返れるように、とったステップ・コマンド・判断・つまずきを時系列で残す。
新しい作業は末尾に追記する。

---

## 2026-10-13

### 1. 準備

- リポジトリ名を `matt-cardona-vs-nick-gage-ja-subs` に決定。README を作成し、GitHub に private で作成して push。
- 環境: Apple Silicon (arm64)、メモリ 32GB。`ffmpeg` と `yt-dlp` は導入済み。
- 音声: `yt-dlp` で取得済みの mp3 (約38分42秒、28MB)。動画ではなく音声のみ。

### 2. YouTube 自動字幕の取得 (失敗)

- 目的: Whisper の出力と突き合わせる第2の意見にする。
- コマンド: `yt-dlp --write-auto-subs --sub-langs en --skip-download <URL>`
- 結果: `HTTP Error 429: Too Many Requests`。`--sleep-subtitles 5` を付けても変わらず。
- 切り分け:
  - 別の動画の字幕は取得できた。→ アカウントや IP 全体の遮断ではなく、この動画の字幕取得だけが制限されている。
  - `PATH` 上の `yt-dlp` (Homebrew版 2025.06.30) は古く、`--js-runtimes` を受け付けない。`venv/bin/yt-dlp` (2026.08.19) を使う。
  - JS ランタイムの警告は `--js-runtimes node` で回避できるが、429 の原因ではない。
- 手動字幕はなく、自動字幕のみであることをメタデータで確認。
- 保留: 時間を置いて再試行する。`--cookies-from-browser` は、ブラウザの認証情報を読むため、使うならユーザーが判断する。

### 3. 用語集の作成

- 動画の説明文とチャプター名 (14個) をメタデータから取得し、`glossary.md` の初版を作成。
- メタデータの取得: `yt-dlp --js-runtimes node --skip-download --dump-single-json <URL>`
- `MDK`、`pizza cutter spot` の訳語は未確定 (要確認)。

### 4. 英語の書き起こし (Whisper large-v3)

- 導入: `venv` に `mlx-whisper` (0.4.3) をインストール。
- 作業用の音声は `work/audio.mp3` にコピー。
- コマンド:

  ```
  ./venv/bin/mlx_whisper work/audio.mp3 \
    --model mlx-community/whisper-large-v3-mlx \
    --language en --output-format srt --word-timestamps True \
    --condition-on-previous-text False \
    --initial-prompt "Matt Cardona, Zack Ryder, Nick Gage, GCW, ..." \
    -o work --output-name en_raw
  ```

- 指定の意図:
  - `--language en`: 言語の自動判定による誤りを防ぐ。
  - `--initial-prompt`: 固有名詞を渡して誤認識を減らす。
  - `--condition-on-previous-text False`: 長い音声での繰り返し (幻覚) を減らす。
- 所要時間: モデルのダウンロードを含めて約6分。
- 出力: `work/en_raw.srt` (755件、0:12〜38:41)。

### 5. 出力の検査

- 検査スクリプト: `scripts/check_srt.py` (件数、連番、時刻の重なり、長さ、40文字超の件数、10秒以上の隙間、頻出行、固有名詞の出現数)。
- 結果:
  - 連番、時刻の重なり、長さ 0 以下: 問題なし。
  - 固有名詞: `Cardona` 28、`Gage` 30、`GCW` 36。`Gauge` などの誤綴りは 0。
  - 42文字を超える字幕が278件 (約37%)。翻訳後に分割・調整する方針。
  - 10秒以上の隙間が11か所。

### 6. 隙間の調査

- `ffmpeg -af silencedetect=noise=-40dB:d=3` で無音を調べた。隙間と重なる無音はなく、音はあるが書き起こされていない区間だった。
- 11か所を、前後2秒を加えて切り出し、閾値を緩めて再度書き起こした (`--no-speech-threshold 0.9`、`--logprob-threshold -2.0`)。
- 結果: 隙間の大半は試合映像の歓声や効果音で、話し言葉はごくわずか。時刻を指定して統合を試みたが、有効な追加は無かった。
- 再書き起こしで見えた誤認識・食い違い:
  - `Nick Cage` → `Nick Gage` (`en.srt` で置換済み)
  - `Modona` は `Cardona` の誤認識 (`en.srt` には入っていない)
  - 21:23 付近: `Mickie` と `me, Gilles` で食い違い。**要・音声確認**。
- 成果物: `en.srt` (755件)。`work/en_raw.srt` は生出力として残す。

### 7. 別モデル (large-v3-turbo) との比較

- 照合用の第2の意見として、`mlx-community/whisper-large-v3-turbo` で全体を書き起こした (`work/en_turbo.srt`、718件)。条件は large-v3 と同じ。
- 単語単位で `en.srt` と比較し、3秒以内の差分をまとめて160か所。`like`、`you know` などの言いよどみ、`wanna`/`want to` のような表記の違いを除くと、意味に関わるものは104か所。
- 比較の結果:
  - 固有名詞では `nbk's`/`mdk's`、`mack`/`matt`、`zach`/`zack` のように、turbo のほうが妥当と見える箇所が複数ある。
  - turbo には、37:39 付近で同じ文を延々と繰り返す暴走 (hallucination) があった。この箇所は large-v3 を採用する。
  - turbo だけが拾った発話が数か所ある (08:09、13:36、17:35)。
- 確認が必要な箇所を `review_list.md` にまとめた (A: 固有名詞、B: 意味が変わる箇所、C: turbo だけが拾った発話、D: 信頼できない出力、E: 統一してよいもの)。
- 差分の生データは `work/diff_v3_turbo.md`。

### 8. 音声確認の結果を反映

- `review_list.md` の A・B をユーザーが音声と YouTube 自動字幕で確認 (結果欄を記入済み)。
- `scripts/apply_fixes.py` で `en.srt` に33件を反映。字幕番号と元の文字列を照合してから置換する。
- 反映の方針: ユーザーが明示した表記を優先。聞き取れなかった箇所は残して末尾に `[?]` を付けた。
- 確認でわかったこと:
  - `MDK` は Nick Gage 側の「ギャング」を指す語 (動画内で `MDK gang`、`MDK Jelly` と言っている)。チャント (`MDK! MDK! MDK!`) もある。展開形 (`Murder Death Kill`) は未確認。
  - YouTube 自動字幕は、ふつうの語彙 (`get`、`outsider`、`called`、`shower`、`world`) で Whisper の取り違えを正しく直せていた。固有名詞は Whisper と同程度で、サイト名 (`prowrestlingtees.com`) は自動字幕も確実ではなかった。
  - 自動字幕は、Whisper 2モデルの食い違いを裁く「第3の意見」として有効。
- 未解決 (`[?]` を付けた): 23:33 のチャント、23:48、24:30、27:21、31:12 の `Warrant Out`、11:15 の `successful wrestling`、22:01 の `suplexes` (推測)、25:07 付近の会話。

### 9. 次の作業

- YouTube の「文字起こし」パネルから自動字幕の全文を取得し、`en.srt` と機械的に突き合わせる (API が 429 のため手動コピーを想定)。
- `[?]` の残りを確認 → `en.srt` を確定 → `glossary.md` を更新 → 日本語訳。
- 保留: YouTube 自動字幕の再取得。

### つまずき・メモ

- 同じ指示をシェルの `for` で書いたところ、zsh の単語分割の違いで失敗した。複雑な処理は Python スクリプトにする。
- バックグラウンドの完了通知は、起動用シェルの終了を知らせるだけの場合がある。実際に出力ファイルができたか、プロセスが残っていないかを確認する。
