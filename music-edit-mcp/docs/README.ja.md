# music-edit-mcp

> English version → [../README.md](../README.md)

DAWのトラックをClaudeに自然言語で編集してもらえるツールです。楽譜ソフトは不要です。

## できること

DAWからMIDIファイルをエクスポートして、Claudeにやりたいことを伝えるだけ。編集済みのMIDIファイルが返ってきます。

**例：**
> 「3小節目のコードが濁って聞こえる。ボイシングを広げて `song_v2.mid` に保存して。」

ClaudeがMIDIを読み込み、編集して、新しいファイルを書き出します。あとはDAWに再インポートして聴くだけです。

## 必要なもの

- Python 3.12 以上
- [uv](https://docs.astral.sh/uv/) — Pythonパッケージマネージャ
- [Claude Code](https://claude.ai/code)

## セットアップ

### 1. インストール

```bash
git clone https://github.com/durun/music-edit.git
cd music-edit/music-edit-mcp
uv sync
```

### 2. Claude Codeに登録する

Claude CodeのMCP設定ファイルに以下を追加します。`/absolute/path/to/music-edit` の部分は、クローンした実際のパスに書き換えてください。

```json
{
  "mcpServers": {
    "music-edit-mcp": {
      "command": "uv",
      "args": [
        "run",
        "--project",
        "/absolute/path/to/music-edit/music-edit-mcp",
        "music-edit-mcp"
      ]
    }
  }
}
```

Claude Codeを再起動すると、接続済みツールの一覧に `music-edit-mcp` が表示されます。

## 使い方

DAWからMIDIファイルをエクスポートして、Claudeに話しかけるだけです。

**楽譜を確認する：**
- 「`~/Desktop/song.mid` を読んでコード進行を教えて。」
- 「`~/Desktop/song.mid` は何調？コードと音がぶつかっているところはある？」

**編集して保存する：**
- 「`song.mid` のメロディを5度上にトランスポーズして `song_v2.mid` に保存して。」
- 「5〜8小節目のベースラインがハーモニーと合っていない。直してファイルを上書きして。」
- 「2小節目の3拍目に経過音を追加して。」

ClaudeがMIDIの読み込み・編集・書き出しを自動でやってくれます。DAWに再インポートして確認しましょう。

## うまくいかないとき

**「ファイルが見つからない」と言われる**
フルパスを使ってください（例：`~/Music/song.mid` ではなく `/Users/yourname/Music/song.mid`）。

**編集結果が思い通りでない**
もう少し具体的に言い直すか、「別のアプローチで試して」と頼んでみてください。

**「ファイルを書き込めない」と言われる**
保存先のフォルダがあらかじめ存在しているか確認してください。

## ライセンス

MIT — [LICENSE](../../LICENSE) を参照
