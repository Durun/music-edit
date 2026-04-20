# 進捗・決定ログ

## 完了: Phase 3 — stateless write

- `write_score(abc_str, midi_path) -> WriteResult` 実装済み
- ABC → Score → MIDI 変換 (music21: converter.parse + Opus.mergeScores)
- MCP tool として公開 (server.py)
- テーブル駆動テスト追加 (10 tests all passed)

## 作業ルール

- **作業が終わったら必ずPRを作成すること**

## 次のアクション: Phase 4 — エラー表現の充実

- LLMの自己修正に最適化された構造化エラー
- 典型的な構文エラーが 1〜2 回のフィードバックループで自己修正できる
- `errors.py` を実装 (現在はプレースホルダー)
