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

### 次のアクション (Phase 2)

- ABC出力対応 (`convert_to_abc`) — Phase 2 スコープ

---

## 2026-04-19: Phase 1 — MusicXML view only

### 完了事項

- `converters.py` に `read_score(midi_path: str) -> str` を実装
  - `FileNotFoundError` (未存在パス) / `ValueError` (Score以外) を送出
  - `GeneralObjectExporter` で MusicXML bytes → UTF-8 文字列化
- `server.py` に `@mcp.tool()` で `read_score` を公開
  - docstring がツール説明として露出
- `tests/fixtures/build_fixtures.py` で I-V-vi-IV (C-G-Am-F) 4小節のMIDIを生成
- `tests/fixtures/test_score.mid` (228 bytes) をコミット
- `tests/test_converters.py` で3テストが全パス

### 確認済み

- `uv run ruff check src/ tests/` クリーン
- `uv run mypy src/` クリーン (strict)
- `uv run pytest` 3 passed
