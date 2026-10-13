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

### 7. 進行中・次の作業

- 進行中: `large-v3-turbo` で全体を書き起こし (`work/en_turbo.srt`)。`en.srt` との差分を取り、食い違い箇所の一覧を作る。
- 次: 差分一覧のうち、固有名詞・意味が変わる箇所を音声で確認 → `en.srt` を確定 → 日本語訳。
- 保留: YouTube 自動字幕の再取得。

### つまずき・メモ

- 同じ指示をシェルの `for` で書いたところ、zsh の単語分割の違いで失敗した。複雑な処理は Python スクリプトにする。
- バックグラウンドの完了通知は、起動用シェルの終了を知らせるだけの場合がある。実際に出力ファイルができたか、プロセスが残っていないかを確認する。
