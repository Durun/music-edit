# music-edit-mcp: プロジェクトコンテキスト

## 概要

DAW作曲支援を目的とした、LLMが楽譜を読み書きするためのMCPサーバ。
Claude Code Cloudセッションで動作することを前提に設計。

## リポジトリ構成

```
music-edit/                  # リポジトリルート
├── .claude/                 # Claude Codeコンテキスト (このディレクトリ)
│   ├── project.md           # プロジェクト全体概要 (このファイル)
│   ├── design.md            # 設計決定事項の要約
│   └── progress.md          # フェーズ進捗・決定ログ
└── music-edit-mcp/          # MCPサーバ本体
    ├── pyproject.toml       # uv管理、mypy/ruff/pytest設定
    ├── src/music_edit_mcp/
    │   ├── server.py        # MCPサーバエントリポイント
    │   ├── models.py        # pydanticモデル
    │   ├── converters.py    # music21ラッパー
    │   └── errors.py        # エラー構造化
    └── tests/
        └── fixtures/        # 回帰テスト用MIDI + 期待出力

```

## 開発環境

- **Python**: 3.12+ (uv管理)
- **パッケージマネージャ**: uv
- **ブランチ**: `claude/setup-python-music-mcp-HGo0L`

## セットアップ手順

```bash
cd music-edit-mcp
uv sync --dev
uv run music-edit-mcp  # サーバ起動
```

## 主要コマンド

```bash
# 依存インストール
uv sync --dev

# lint
uv run ruff check src/

# format
uv run ruff format src/

# 型検査
uv run mypy src/

# テスト
uv run pytest

# サーバ起動
uv run music-edit-mcp
```

## Claude Code Cloud 固有の注意事項

- セッションをまたぐとファイルが消える。作業チェックポイントで必ずコミット＆プッシュ
- コンテキストは `.claude/` 配下にドキュメント化し随時更新
- `CLAUDE.md` はリポジトリルートに置くとClaude Codeが自動読み込みする

## 重要な設計判断

詳細は `design.md` 参照。要点のみ:

1. **MIDIが正 (Source of Truth)** — MusicXMLは揮発的中間形式
2. **ステートレス優先** — セッション管理はPhase 5 (optional)
3. **LLM操作形式はABC** — トークン効率重視
4. **エラー自己修正はユーザーから隠す** — 失敗時のみ通知
