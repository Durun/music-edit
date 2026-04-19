# 設計決定事項

元の設計書: 設計書v3 (LLM向け楽譜操作MCP)

> **v3の変更点**: Phase 5 API から `xml_path?` 引数を削除。§4.2「MusicXMLは揮発」方針と不整合だったため。

---

## 1. プロジェクト目的

**目的**: Claude Codeから対話的に楽譜（MIDI）を操作し、DAW作曲を支援する。作業の高速化が目的であり、ユーザーの創造性を代替するものではない。

### 想定ユースケース

- コード進行をボイシング込みで添削
- 白玉コードを数パターンのアルペジオとして提示
- メロディーとコードの衝突検出・代替メロディー提示

いずれも**往復を前提とした対話**。MIDIを部分的に書き出して指定し、バリエーションを提示させるなど。

### システム境界と責務分担

| 担当 | 責務 |
|---|---|
| **ユーザー** | DAWでMIDI書き出し／Claude Codeへの指示とファイルパスの提示／DAWで再読み込み操作／再生確認 |
| **Claude (LLM)** | 自然言語の解釈／MCPツール呼び出し／ABC編集／エラー自己修正 |
| **MCPサーバ** | ファイルI/O／MIDI⇄MusicXML⇄ABC変換／構文・音楽的バリデーション／エラー構造化 |
| **DAW** | MIDI書き出し・再読み込み・再生（**システム側からの操作は一切しない**） |

---

## 2. ユーザー操作サイクル

### セットアップ（初回のみ）

1. MCPサーバを起動し、Claude Codeに登録する（`.claude/mcp_config.json`）
2. DAWで作業を開始し、必要に応じてMIDIを書き出す

### 通常の操作サイクル

```
[1] DAWでMIDI書き出し (ユーザー操作)
          ↓
[2] Claude Codeに自然言語で指示 (ユーザー操作)
    例: 「~/scores/verse.mid のコード進行を
         4パターンのアルペジオにして」
          ↓
[3] LLMがMCPツールでMIDIを読み込み → ABC変換 (自動)
          ↓
[4] LLMがABCを編集 → MCPがMIDIに書き戻し (自動)
          ↓
[5] DAWでMIDI再読み込み (ユーザー操作: ボタン押下等)
          ↓
[6] 再生確認 (ユーザー操作)
          ↓
   (必要に応じて [2] に戻り往復)
```

ユーザーの手が入るのは **[1][2][5][6] の4点のみ**。[3][4] はLLMとMCPが自動処理。

### 運用の前提

| 事項 | 取り決め |
|---|---|
| **MIDIファイルの場所** | 固定ディレクトリは設けない。ユーザーが指示ごとにパスをClaude Codeに伝える |
| **DAW再読み込み** | 手動。ユーザーがDAWのリロードボタン等を操作する。システムからDAWに通知しない |
| **ファイル数** | システムは規定しない。ユーザーとの会話から都度対象ファイルを特定して読み込む |
| **粒度の指示** | 「ピアノトラックだけ編集して」はユーザーがトラック単位で書き出したMIDIを指すことで実現 |

---

## 3. システムアーキテクチャ

### データフロー

```
[DAW] ←MIDI(n files)→ [MCP Server] ←操作形式→ [LLM (Claude Code)]
                           │
                           └─ MIDI ⇄ MusicXML ⇄ ABC (music21経由)
```

### コンポーネント役割

| コンポーネント | 役割 | 位置づけ |
|---|---|---|
| **MCP Server** | ファイルI/O、フォーマット変換、バリデーション、エラー構造化 | 中核 |
| **Skill** | 楽譜編集ワークフローの規約・few-shot例を注入 | 補助 |
| **Hook** | `PostToolUse` でMIDI書き出し後の自動バリデーション等 | 補助 |

---

## 4. フォーマット選定

### 各フォーマットの位置づけ

| 役割 | フォーマット | 根拠 |
|---|---|---|
| **Source of Truth** | MIDI | DAW互換性が正 |
| **中間形式（揮発）** | MusicXML | 最大の表現力。ボイシング・声部・調号を保持 |
| **LLM操作形式（基本）** | ABC | トークン効率、LLM学習データの豊富さ |
| **LLM操作形式（将来）** | 差し替え可能（LilyPond等） | Phase 6で対応 |

### 情報損失の非対称性への対応 (MusicXML揮発の原則)

MIDIはMusicXMLが表現する情報（異名同音・声部・調号など）を完全には持たない。

- **MusicXMLの付加情報は永続化しない**（ステートレス設計）
- MusicXMLはセッション中のみ派生生成される揮発データとして扱う
- サイドカーファイル・MIDI埋め込みは採用しない
- **この方針はAPIシグネチャにも反映**: ファイルパスを受け取るのはMIDIのみ

### フォーマット比較（評価済み）

| フォーマット | ボイシング制御 | 複数声部 | 複数トラック | LLM生成品質 | トークン効率 |
|---|---|---|---|---|---|
| ABC | △（プロンプトで補完可） | ○ | △ | ◎ | ◎ |
| LilyPond | ◎ | ◎ | ◎ | ○ | △ |
| MusicXML | ◎ | ◎ | ◎ | △ | ✕ |

---

## 5. 実装フェーズ

Phase 1〜4が本体、Phase 5〜6はoptional。各フェーズは動作確認ができ次第クイックに進める。

### Phase 1: MusicXML view only

- **機能**: `read_score(midi_path) → musicxml_string`
- **完了条件**: Claude CodeからMIDIを読み込み、和音・メロディーに関する質問に正しく答えられる
- **留意**: 冗長さは受容。動作確認用MIDIは短く作る

### Phase 2: ABC出力追加

- **機能**: `read_score(midi_path, format="musicxml"|"abc")`
- **完了条件**: ABC出力がMusicXMLの20%以下のトークン数。実曲サイズ（2〜3分）が読み込める
- **留意**: 書き込みはまだサポートしない

### Phase 3: ステートレス書き込み

- **機能**: `write_score(abc_string, midi_path) → {success, errors}`
- **完了条件**: read → LLM編集 → write の往復で再生可能なMIDIが出力される。ユースケース①が完結
- **山場**: ABCパーサのエラー情報の構造化
- **注意**: このAPIはPhase 5で置き換えになる前提。互換性を守ろうとしない

### Phase 4: エラー表現の充実

- **機能**: LLMの自己修正に最適化された構造化エラー
- **完了条件**: 典型的な構文エラーが1〜2回のフィードバックループでLLMが自己修正できる
- **可視性ポリシー**:
  - エラー自己修正はLLM↔MCPの**内部ループ**で完結し、基本的にユーザーには見えない
  - LLMが自己修正を諦めた場合（一定回数失敗、致命的エラー等）のみユーザーへ通知
- **エラー形式例**:
  ```json
  {
    "type": "measure_duration_mismatch",
    "location": {"measure": 3, "voice": 1},
    "expected": "4 beats (4/4 time)",
    "actual": "3.5 beats",
    "hint": "Add a rest or extend the last note"
  }
  ```

### Phase 5 (optional): ステートフル編集

差分編集プロトコル導入。詳細は §6 参照。

### Phase 6 (optional): フォーマット拡充

LilyPond等をエクスポータとして追加。

---

## 6. 差分編集プロトコル (Phase 5)

### 差分表現形式: 音楽ドメインDSL

テキストdiff・XPath・JSON Patchを却下。理由：LLMに構文を書かせる負担が大きく、意味検証ができない。

**DSL例**:
```
modify_pitch @n_p1_m3_b2_v1_i0 to=E4
insert_note at=(measure=4, beat=1, voice=1) pitch=C4 duration=quarter
```

### 操作プリミティブ（最小集合）

| 操作 | 引数 |
|---|---|
| `modify_pitch` | `@id`, `to_pitch` |
| `modify_duration` | `@id`, `to_duration` |
| `modify_voice` | `@id`, `to_voice` |
| `insert_note` | `at=(measure,beat,voice)`, `pitch`, `duration` |
| `remove_note` | `@id` |
| `insert_measure` | `at=measure_index`, `time_sig?`, `key_sig?` |
| `modify_key_signature` | `at=measure`, `to_key` |
| `modify_tempo` | `at=measure`, `to_bpm` |

和音は「同時刻の複数ノート」として個別ノート操作で表現。

### 安定ID戦略

- 初期読込時にMCPが全ノートへID採番（例: `n_p1_m3_b2_v1_i0`）
- ノート追加後も既存IDは不変、追加ノートには新IDを採番
- LLM向けビュー（ABC等）にもIDをアノテーションで埋め込む
- インデックスずれ問題を回避

### 楽観ロック

```
apply_patch(
  session_id="sess_abc",
  base_version=42,
  patches=[...]
) → {new_version: 43, diagnostics: []}
```

LLMが古いビューを見て書いた差分の誤適用を防止。ロールバック・リプレイが可能。

### MCP API (Phase 5 全体像)

```python
load_score(midi_path)
  → { session_id, version: 0, view_formats: ["abc", "lilypond"] }

get_view(session_id, format="abc", with_ids=True)
  → { content, version }

apply_patch(session_id, base_version, patches)
  → { new_version, diagnostics, applied, rejected }

validate(session_id)
  → { errors, warnings }

save_score(session_id, midi_path)
  → { saved_path }

rollback(session_id, to_version)
  → { new_version }
```

- セッション中はMusicXMLをインメモリ保持（`music21.stream.Score`）
- `load_score`/`save_score` が扱うのはMIDIパスのみ
- MusicXMLはセッション内に閉じた揮発データ。ファイルパスとして一切露出しない
- `apply_patch` は部分失敗を許容、拒否理由をLLMが参照して再試行

---

## 7. 技術スタック

### 採用技術

| 要素 | 採用技術 | 用途 |
|---|---|---|
| 言語 | Python 3.12+ | 実装言語 |
| 環境管理 | uv | Pythonバージョン・venv・依存の一元管理 |
| 楽譜処理 | music21 | MIDI/MusicXML/ABC相互変換（事実上の標準） |
| プロトコル | MCP公式SDK (Python) | MCPサーバ実装 |
| 型定義 | pydantic v2 | I/O型定義、実行時バリデーション |
| 静的検査 | mypy --strict | 型安全性の担保 |
| lint/format | ruff | コード品質 |
| テスト | pytest | 回帰テスト |

### 選定根拠

`music21` が他言語に代替がないほど成熟しているため、MIDI↔MusicXML↔ABC変換をカバーするにはPython一択。現代のツールチェイン（uv + mypy strict + pydantic）により、伝統的なPythonの弱点（環境依存・動的型）はほぼ解消される。

### 却下した選択肢

| 選択肢 | 却下理由 |
|---|---|
| **Pure Go** | MusicXML/ABCの成熟ライブラリが存在しない。パーサ自前実装は趣味プロジェクトの射程外 |
| **ハイブリッド（Go MCP + Python CLI）** | Python起動コスト、言語境界エラー伝搬、依存の二重管理。Phase 1〜4ではオーバーエンジニアリング |

### 将来の逃げ道

Phase 5でパフォーマンスが必要になった場合、**差分適用エンジンのみGoバイナリに切り出す**ことは可能。MCPサーバ本体はPythonのまま維持。必要性が実証されてから着手。

---

## 8. テスト戦略

pytest導入までは不要。手作りMIDI 3〜5個 + 期待出力テキストを `tests/fixtures/` に置き、フェーズ跨ぎの回帰確認に使う。

---

## 9. 設計原則

1. **MIDIを正、MusicXMLを派生**: DAW連携の単純さを優先
2. **ステートレス優先、ステートフルはoptional**: セッション管理の本質的でない複雑さを先送り
3. **中間形式は常に正、LLM操作形式は読み取りビュー + 差分パッチ**: 操作形式を差し替えても中間形式の情報を保全
4. **フォーマットは「まず動くもの」から**: Phase 1は生のMusicXML、効率化はPhase 2以降
5. **APIは置き換え前提で設計**: Phase 3のAPIはPhase 5で捨てる。互換性を守って歪めない
6. **DAWへの介入は行わない**: システムからDAWを操作しない。再読み込みは常にユーザーの手動操作
7. **内部ループはユーザーから隠す**: LLMの自己修正は不可視、失敗時のみ可視化
8. **創造性を代替しない**: 作業の高速化が目的。提示するのはバリエーションであり、選択と判断はユーザーに委ねる
9. **趣味プロジェクトの射程を守る**: オーバーエンジニアリングを避け、Pure Pythonで最短経路
10. **設計方針はAPIシグネチャにも一貫して反映する**: 「MusicXML揮発」はパス引数を露出しないことで表現する、のように
