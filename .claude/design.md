# 設計決定事項 (要約)

元の設計書: 設計書v3 (LLM向け楽譜操作MCP)

## データフロー

```
[DAW] ←MIDI→ [MCP Server] ←→ [LLM (Claude Code)]
                  │
                  └─ MIDI ⇄ MusicXML ⇄ ABC (music21経由)
```

## フォーマット役割

| 役割 | フォーマット |
|---|---|
| Source of Truth | MIDI |
| 中間形式 (揮発) | MusicXML |
| LLM操作形式 | ABC |

## 実装フェーズ

| Phase | 機能 | 状態 |
|---|---|---|
| 1 | `read_score(midi_path) → musicxml_string` | 未着手 |
| 2 | `read_score(..., format="abc")` | 未着手 |
| 3 | `write_score(abc_string, midi_path)` | 未着手 |
| 4 | 構造化エラー・LLM自己修正 | 未着手 |
| 5 | ステートフル差分編集 (optional) | 未着手 |
| 6 | LilyPond等フォーマット拡充 (optional) | 未着手 |

## 技術スタック

| 要素 | 採用 |
|---|---|
| 言語 | Python 3.12+ |
| 環境管理 | uv |
| 楽譜処理 | music21 |
| MCPプロトコル | mcp[cli] (FastMCP) |
| 型定義 | pydantic v2 |
| 静的検査 | mypy --strict |
| lint/format | ruff |
| テスト | pytest |

## MusicXML揮発の原則

- MusicXMLはセッション中のみ派生生成される揮発データ
- ファイルパスはMIDIのみ。MusicXMLパスをAPIに露出しない
- サイドカーファイル・MIDI埋め込みは採用しない

## APIシグネチャ方針

- `load_score(midi_path)` / `save_score(session_id, midi_path)` — MIDIパスのみ
- MusicXMLはセッション内に閉じた揮発データ (Phase 5以降)
- Phase 3までのAPIは捨て前提、互換性を守って歪めない

## ユーザー操作サイクル

ユーザーが手を触れるのは以下の4点のみ:
1. DAWでMIDI書き出し
2. Claude Codeに自然言語で指示
3. DAWでMIDI再読み込み (手動)
4. 再生確認

[3][4]の自動化はしない。DAWへの介入は行わない。
