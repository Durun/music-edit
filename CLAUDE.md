# CLAUDE.md

このリポジトリは `music-edit-mcp` — DAW作曲支援のためのLLM楽譜操作MCPサーバ。

## 重要ドキュメント

- `.claude/project.md` — プロジェクト概要・セットアップ手順
- `.claude/design.md` — 設計決定事項の要約

## memory/ ディレクトリ

`memory/` はセッションをまたいで覚えておくべきことを自由にメモする場所。

- `memory/progress.md` — フェーズ進捗・決定ログ
- 新しく覚えておきたいことができたら `memory/` 配下に追加してよい
- 作業後は必ずコミット＆プッシュして永続化すること

## 作業前に必ず確認

1. ブランチ: `claude/implement-next-phase-aFiVp` で作業
2. Claude Code Cloud: セッション終了でファイルが消える → チェックポイントごとにコミット＆プッシュ
3. 作業ディレクトリ: `music-edit-mcp/` 配下

## 作業完了時のルール

- タスクが完了したら必ず PR を作成すること

## クイックスタート

```bash
cd music-edit-mcp
uv sync --dev
uv run ruff check src/ && uv run mypy src/ && uv run pytest
```
