# music-edit-mcp

[🇯🇵 日本語版はこちら](docs/README.ja.md)

An MCP server for LLM-driven music score editing — edit your DAW's MIDI files using natural language in Claude Code.

## What You Can Do

- Review chord progressions and voice leading in your MIDI
- Change or transpose chord progressions
- Expand chords into arpeggios or rhythmic patterns
- Detect melody–chord conflicts and fix them

## Workflow

```
[1] Export MIDI from DAW
[2] Tell Claude Code what to change
[3] Claude reads, edits, and overwrites the MIDI
[4] Re-import the MIDI into your DAW and verify
```

---

## Prerequisites

- **Python 3.12+**
- **[uv](https://docs.astral.sh/uv/)** — Python package manager
- **[Claude Code](https://claude.ai/code)** — CLI or web version

---

## Installation

```bash
git clone https://github.com/durun/music-edit.git
cd music-edit/music-edit-mcp
uv sync
```

---

## Register with Claude Code

Run the following command, replacing `/absolute/path/to` with the actual path on your machine:

```bash
claude mcp add music-edit-mcp -- uv run --directory /absolute/path/to/music-edit/music-edit-mcp music-edit-mcp
```

Verify registration:

```bash
claude mcp list
# music-edit-mcp should appear in the list
```

> **Tip:** The path must be absolute (not relative). You can get the full path by running `pwd` inside the `music-edit-mcp` directory.

---

## Usage

### Basic workflow

1. Export a MIDI file from your DAW (e.g., `~/projects/song/verse.mid`).
2. Open Claude Code and describe what you want to change.
3. Claude Code will call `read_score` and `write_score` automatically.
4. Re-import the updated MIDI into your DAW.

### Example prompts

```
Check the chord progression in ~/projects/song/verse.mid
```

```
Change the chord progression in verse.mid to Am → G → F → G and save it.
```

```
Expand the whole-note chords in verse.mid into eighth-note arpeggios.
```

```
Read verse.mid and write a version with a capo on the 2nd fret to ~/projects/song/verse_capo2.mid
```

### Try with the included sample

The repository includes a 4-measure I–V–vi–IV chord progression as a test fixture:

```bash
# From the music-edit-mcp directory
uv run python tests/fixtures/build_fixtures.py  # regenerate if needed
```

Then in Claude Code:

```
Read music-edit-mcp/tests/fixtures/test_score.mid and show me the chord progression.
```

---

## Tool Reference

These MCP tools are called automatically by Claude — you don't need to invoke them directly.

| Tool | Parameters | Description |
|------|-----------|-------------|
| `read_score` | `midi_path`, `format` | Read a MIDI file and return its score as text |
| `write_score` | `abc_str`, `midi_path` | Convert ABC notation to a MIDI file |

### `read_score`

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `midi_path` | string | — | Path to the `.mid` file |
| `format` | `"musicxml"` \| `"abc"` | `"musicxml"` | Output format |

- **`"abc"`** — Compact ABC notation, efficient for LLM editing
- **`"musicxml"`** — Full MusicXML, preserves all structural detail

### `write_score`

| Parameter | Type | Description |
|-----------|------|-------------|
| `abc_str` | string | ABC notation string (single or multi-part) |
| `midi_path` | string | Destination path for the `.mid` file |

Returns a result indicating success or failure. On error, a type (`parse_error` or `write_error`) and a message are provided so Claude can self-correct.

### ABC notation basics

```abc
X:1
M:4/4
L:1/4
K:C
|[CEG]4|[G,B,D]4|[A,CE]4|[F,A,C]4|
```

- `[CEG]4` — C major chord (whole note)
- `G,` — G in the octave below middle C
- `4` / `2` / `/2` — whole / half / eighth note (relative to `L:1/4`)

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `uv sync` fails | Check that Python 3.12+ is installed: `python --version` |
| MCP not recognized in Claude Code | Confirm the path is absolute; run `claude mcp list` |
| MIDI write fails | Ensure the destination directory exists before writing |
| `read_score` returns garbled output | The MIDI may use non-standard encoding; try exporting again from your DAW |

---

## License

MIT — see [LICENSE](../LICENSE).
Third-party notices: [THIRD_PARTY_NOTICES.md](../THIRD_PARTY_NOTICES.md).
