# 進捗・決定ログ

## 2026-04-19: 環境構築 (Phase 0)

### 完了事項

- `music-edit-mcp/` ディレクトリを `uv init --lib --python 3.12` で初期化
- `pyproject.toml` に以下を設定:
  - 依存: `mcp[cli]>=1.0.0`, `music21>=9.0.0`, `pydantic>=2.0.0`
  - dev依存: `mypy>=1.0.0`, `ruff>=0.8.0`, `pytest>=8.0.0`
  - `[tool.mypy]`: `strict = true`
  - `[tool.ruff]`: `target-version = "py312"`, 主要ルール有効化
  - `[tool.pytest.ini_options]`: `testpaths = ["tests"]`
- パッケージ構造を設計書通りに作成:
  - `src/music_edit_mcp/server.py` (空のFastMCPサーバ)
  - `src/music_edit_mcp/models.py` (HealthResponseのみ)
  - `src/music_edit_mcp/converters.py` (スタブ)
  - `src/music_edit_mcp/errors.py` (スタブ)
- `tests/fixtures/` ディレクトリ作成
- `.claude/` にプロジェクトコンテキストを文書化

### 確認済み

- `uv sync --dev` が通る
- `uv run ruff check` がクリーン
- `uv run mypy src/` がクリーン

### 次のアクション (Phase 1)

1. 動作確認用MIDIファイルを `tests/fixtures/` に配置
2. `converters.py` に `read_score(midi_path) → musicxml_string` を実装
3. `server.py` に MCPツールとして公開
4. `.claude/mcp_config.json` で Claude Code に登録
5. 完了条件: 「最初の和音は何？」に正しく答えられる
