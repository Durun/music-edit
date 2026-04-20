# music-edit-mcp

[🇺🇸 English version](../README.md)

DAW の MIDI ファイルを Claude Code から自然言語で編集するための MCP サーバです。

## できること

- MIDI のコード進行・ボイシングを確認する
- コード進行を変更・転調する
- コードをアルペジオやリズムパターンに展開する
- メロディとコードの音程衝突を検出・修正する

## ワークフロー

```
[1] DAW から MIDI をエクスポート
[2] Claude Code に変更内容を伝える
[3] Claude が MIDI を読んで編集し上書きする
[4] DAW で MIDI を再インポートして確認
```

---

## 前提条件

- **Python 3.12 以上**
- **[uv](https://docs.astral.sh/uv/)** — Python パッケージマネージャ
- **[Claude Code](https://claude.ai/code)** — CLI または Web 版

---

## インストール

```bash
git clone https://github.com/durun/music-edit.git
cd music-edit/music-edit-mcp
uv sync
```

---

## Claude Code への登録

以下のコマンドを実行してください。`/絶対パス` は実際のパスに置き換えてください。

```bash
claude mcp add music-edit-mcp -- uv run --directory /絶対パス/music-edit/music-edit-mcp music-edit-mcp
```

登録確認:

```bash
claude mcp list
# music-edit-mcp が一覧に表示されれば OK
```

> **ヒント:** パスは絶対パスで指定してください（相対パス不可）。`music-edit-mcp` ディレクトリ内で `pwd` を実行するとフルパスを確認できます。

---

## 使い方

### 基本フロー

1. DAW から MIDI をエクスポートする（例: `~/projects/song/verse.mid`）
2. Claude Code を開いて変更したい内容を日本語で伝える
3. Claude Code が自動的に `read_score` と `write_score` を呼び出して編集する
4. 更新された MIDI を DAW に再インポートして確認する

### 指示の例

```
~/projects/song/verse.mid のコード進行を確認して
```

```
verse.mid のコード進行を Am → G → F → G に変えて保存して
```

```
verse.mid の全音符コードを8分音符のアルペジオに展開して
```

```
verse.mid を読んで、カポ2フレット相当に転調したものを ~/projects/song/verse_capo2.mid に書き出して
```

### 付属サンプルで試す

リポジトリには 4 小節の I–V–vi–IV コード進行のテスト用 MIDI が含まれています。

```bash
# music-edit-mcp ディレクトリ内で
uv run python tests/fixtures/build_fixtures.py  # 必要に応じて再生成
```

Claude Code での使用例:

```
music-edit-mcp/tests/fixtures/test_score.mid のコード進行を教えて
```

---

## ツールリファレンス

以下の MCP ツールは Claude が自動的に呼び出します。直接操作する必要はありません。

| ツール | パラメータ | 説明 |
|--------|-----------|------|
| `read_score` | `midi_path`, `format` | MIDI を読んでテキスト形式のスコアを返す |
| `write_score` | `abc_str`, `midi_path` | ABC 記法から MIDI ファイルを生成する |

### `read_score`

| パラメータ | 型 | デフォルト | 説明 |
|-----------|------|---------|------|
| `midi_path` | string | — | `.mid` ファイルのパス |
| `format` | `"musicxml"` \| `"abc"` | `"musicxml"` | 出力フォーマット |

- **`"abc"`** — コンパクトな ABC 記法（LLM 編集向け、トークン効率が良い）
- **`"musicxml"`** — 完全な MusicXML（すべての構造情報を保持）

### `write_score`

| パラメータ | 型 | 説明 |
|-----------|------|------|
| `abc_str` | string | ABC 記法の文字列（単一・複数パート対応） |
| `midi_path` | string | 出力する `.mid` ファイルのパス |

成功・失敗を示す結果を返します。エラー時は種別（`parse_error` または `write_error`）とメッセージが返るため、Claude が自己修正できます。

### ABC 記法の基本

```abc
X:1
M:4/4
L:1/4
K:C
|[CEG]4|[G,B,D]4|[A,CE]4|[F,A,C]4|
```

| 記法 | 意味 |
|------|------|
| `[CEG]4` | C メジャーコード（全音符） |
| `G,` | 中央 C より 1 オクターブ低い G |
| `g` | 中央 C より 1 オクターブ高い G |
| `4` / `2` / `/2` | 全音符 / 2 分音符 / 8 分音符（`L:1/4` 基準） |
| `^C` / `_C` | C# / Cb |

---

## トラブルシューティング

| 問題 | 対処方法 |
|------|----------|
| `uv sync` が失敗する | Python 3.12 以上がインストールされているか確認: `python --version` |
| Claude Code で MCP が認識されない | パスが絶対パスか確認。`claude mcp list` で登録状況を確認 |
| MIDI の書き出しが失敗する | 出力先ディレクトリが存在するか確認 |
| `read_score` の出力が文字化けする | DAW から MIDI を再エクスポートして試す |

---

## ライセンス

MIT — [LICENSE](../../LICENSE) 参照。  
サードパーティライセンス: [THIRD_PARTY_NOTICES.md](../../THIRD_PARTY_NOTICES.md)
