# music-edit-mcp

> English version → [../README.md](../README.md)

DAW作曲をClaudeで加速するための、LLM駆動の楽譜編集MCPサーバです。

## 概要

music-edit-mcpはDAWとClaude Codeをつなぐブリッジです。MIDIファイルをエクスポートし、自然言語で編集内容を指示するだけで、更新されたMIDIファイルが返ってきます。楽譜ソフトは不要です。

**ワークフロー:**

| ステップ | 担当 | 内容 |
|---------|------|------|
| 1 | あなた | DAWからMIDIをエクスポート |
| 2 | あなた | Claudeに自然言語で指示 |
| 3 | Claude | 楽譜を読み込み、ABC記譜法で編集 |
| 4 | Claude | 編集結果をMIDIファイルに書き出し |
| 5 | あなた | DAWにMIDIを再インポートして再生確認 |

ステップ3・4は自動で行われます。あなたが操作するのはステップ1・2・5のみです。

## 必要な環境

- Python 3.12 以上
- [uv](https://docs.astral.sh/uv/) パッケージマネージャ
- [Claude Code](https://claude.ai/code)（CLIまたはデスクトップアプリ）

## インストール

```bash
git clone https://github.com/durun/music-edit.git
cd music-edit/music-edit-mcp
uv sync
```

## 設定

Claude CodeのMCP設定にサーバを追加します。Claude Code内で次のコマンドを実行してください:

```
/mcp add music-edit-mcp
```

または設定ファイルを直接編集します（デスクトップアプリ: `~/.claude/claude_desktop_config.json`、CLI: `~/.claude.json`）:

```json
{
  "mcpServers": {
    "music-edit-mcp": {
      "command": "uv",
      "args": [
        "run",
        "--project",
        "/path/to/music-edit/music-edit-mcp",
        "music-edit-mcp"
      ]
    }
  }
}
```

`/path/to/music-edit` はクローンした実際のパスに置き換えてください。

サーバが起動するか確認するには:

```bash
cd music-edit-mcp
uv run music-edit-mcp
```

## ツールリファレンス

### `read_score`

MIDIファイルを読み込み、楽譜をテキストとして返します。

| パラメータ | 型 | デフォルト | 説明 |
|-----------|---|-----------|------|
| `midi_path` | string | — | `.mid` ファイルのパス |
| `format` | `"musicxml"` \| `"abc"` | `"musicxml"` | 出力フォーマット |

- **`"musicxml"`** — 詳細な構造情報。楽譜の内容確認に最適
- **`"abc"`** — コンパクトな記譜法。編集に最適

**プロンプト例:**
> `/Users/me/song.mid` を読み込んでコード進行を教えて。

### `write_score`

ABC記譜法をMIDIファイルに変換します。

| パラメータ | 型 | 説明 |
|-----------|---|------|
| `abc_str` | string | ABC記譜法の文字列（編集後の楽譜） |
| `midi_path` | string | 出力先の `.mid` ファイルのパス |

`midi_path` の親ディレクトリはあらかじめ存在している必要があります。既存ファイルは上書きされます。

**プロンプト例:**
> 2小節目のコードをDmに変えて、`/Users/me/song_edited.mid` に保存して。

## ABC記譜法クイックリファレンス

このサーバはABC記譜法を編集フォーマットとして使用します。基本を以下にまとめます。

### スコアの構造

```
X:1          % パートのインデックス（パートごとにインクリメント）
M:4/4        % 拍子
L:1/4        % 基準音符（四分音符 = 修飾子なし）
Q:1/4=120    % テンポ（BPM、省略可）
K:C          % 調号
|C E G2|     % 小節（| で区切る）
```

### 音高

| ABC | 音 |
|-----|---|
| `C` | C4（中央ド） |
| `c` | C5 |
| `C,` | C3 |
| `^C` | C♯4 |
| `_C` | C♭4 |
| `=C` | C♮4（ナチュラル） |

### 音符の長さ（`L:1/4` 基準）

| ABC | 長さ |
|-----|-----|
| `C` | 四分音符 |
| `C2` | 二分音符 |
| `C4` | 全音符 |
| `C/2` | 八分音符 |
| `C3/2` | 付点四分音符 |

### 和音と休符

| ABC | 意味 |
|-----|-----|
| `[CEG]4` | Cメジャーの全音符コード |
| `z` | 四分休符 |
| `z4` | 全休符 |

### 複数パートのスコア

パートをブランク行で区切り、それぞれ `X:` から始めます:

```
X:1
M:4/4
L:1/4
K:C
|[CEG]4|[GBD]4|[ACE]4|[FAC]4|

X:2
M:4/4
L:1/4
K:C
|C4|D4|E4|C4|
```

## トラブルシューティング

| 症状 | 原因 | 対処 |
|------|------|------|
| `FileNotFoundError` | MIDIファイルのパスが間違っている | 絶対パスを使い、ファイルの存在を確認する |
| 結果に `parse_error` | ABC記譜法の構文エラー | Claudeに記譜法の修正を依頼してリトライ |
| 結果に `write_error` | 出力先ディレクトリが存在しない | 出力先ディレクトリを先に作成する |

## 開発

```bash
cd music-edit-mcp
uv sync --dev
uv run ruff check src/     # リント
uv run ruff format src/    # フォーマット
uv run mypy src/           # 型チェック
uv run pytest              # テスト
```

## ライセンス

MIT — [LICENSE](../../LICENSE) を参照
