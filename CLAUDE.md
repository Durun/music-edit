# CLAUDE.md

このリポジトリは `music-edit-mcp` — DAW作曲支援のためのLLM楽譜操作MCPサーバ。

## 重要ドキュメント

- `.claude/project.md` — プロジェクト概要・セットアップ手順
- `.claude/design.md` — 設計決定事項の要約
- `.claude/progress.md` — フェーズ進捗・決定ログ

## 作業前に必ず確認

1. ブランチ: `claude/setup-python-music-mcp-HGo0L` で作業
2. Claude Code Cloud: セッション終了でファイルが消える → チェックポイントごとにコミット＆プッシュ
3. 作業ディレクトリ: `music-edit-mcp/` 配下

## クイックスタート

```bash
cd music-edit-mcp
uv sync --dev
uv run ruff check src/ && uv run mypy src/ && uv run pytest
```
