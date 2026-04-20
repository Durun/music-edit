# music-edit-mcp

> 日本語版はこちら → [docs/README.ja.md](./docs/README.ja.md)

MCP server for LLM-driven music score editing, designed to accelerate DAW composition with Claude.

## Overview

music-edit-mcp bridges your DAW and Claude Code. Export a MIDI file, describe what you want to change in natural language, and get an updated MIDI file back — no notation software required.

**Workflow:**

| Step | Who | What |
|------|-----|------|
| 1 | You | Export MIDI from your DAW |
| 2 | You | Give Claude a natural language instruction |
| 3 | Claude | Reads the score, edits it in ABC notation |
| 4 | Claude | Writes the result back to a MIDI file |
| 5 | You | Re-import MIDI into your DAW and play back |

Steps 3 and 4 happen automatically — you only touch steps 1, 2, and 5.

## Prerequisites

- Python 3.12 or higher
- [uv](https://docs.astral.sh/uv/) package manager
- [Claude Code](https://claude.ai/code) (CLI or desktop app)

## Installation

```bash
git clone https://github.com/durun/music-edit.git
cd music-edit/music-edit-mcp
uv sync
```

## Configuration

Add the server to your Claude Code MCP configuration. In Claude Code, run:

```
/mcp add music-edit-mcp
```

Or edit `~/.claude/claude_desktop_config.json` (desktop) / `~/.claude.json` (CLI) manually:

```json
{
  "mcpServers": {
    "music-edit-mcp": {
      "command": "uv",
      "args": [
        "run",
        "--project",
        "/path/to/music-edit/music-edit-mcp",
        "music-edit-mcp"
      ]
    }
  }
}
```

Replace `/path/to/music-edit` with the actual path to your clone.

To verify the server starts:

```bash
cd music-edit-mcp
uv run music-edit-mcp
```

## Tools Reference

### `read_score`

Read a MIDI file and return its score as text.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `midi_path` | string | — | Path to the `.mid` file |
| `format` | `"musicxml"` \| `"abc"` | `"musicxml"` | Output format |

- **`"musicxml"`** — Full structural detail; best for inspecting the score
- **`"abc"`** — Compact notation; best for editing

**Example prompt:**
> Read `/Users/me/song.mid` and tell me the chord progression.

### `write_score`

Convert ABC notation back to a MIDI file.

| Parameter | Type | Description |
|-----------|------|-------------|
| `abc_str` | string | ABC notation string (edited score) |
| `midi_path` | string | Destination path for the output `.mid` file |

The parent directory of `midi_path` must already exist. Existing files are overwritten.

**Example prompt:**
> Change the chord in measure 2 to Dm and save the result to `/Users/me/song_edited.mid`.

## ABC Notation Quick Reference

The server uses ABC notation as its editing format. Here are the basics:

### Score structure

```
X:1          % Part index (increment for each part)
M:4/4        % Time signature
L:1/4        % Unit note length (quarter note = no suffix)
Q:1/4=120    % Tempo in BPM (optional)
K:C          % Key signature
|C E G2|     % Measures delimited by |
```

### Pitches

| ABC | Note |
|-----|------|
| `C` | C4 (middle C) |
| `c` | C5 |
| `C,` | C3 |
| `^C` | C♯4 |
| `_C` | C♭4 |
| `=C` | C♮4 (natural) |

### Durations (`L:1/4` baseline)

| ABC | Duration |
|-----|----------|
| `C` | Quarter note |
| `C2` | Half note |
| `C4` | Whole note |
| `C/2` | Eighth note |
| `C3/2` | Dotted quarter |

### Chords and rests

| ABC | Meaning |
|-----|---------|
| `[CEG]4` | C major whole-note chord |
| `z` | Quarter rest |
| `z4` | Whole rest |

### Multi-part scores

Separate parts with a blank line, each starting with `X:`:

```
X:1
M:4/4
L:1/4
K:C
|[CEG]4|[GBD]4|[ACE]4|[FAC]4|

X:2
M:4/4
L:1/4
K:C
|C4|D4|E4|C4|
```

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|-------------|-----|
| `FileNotFoundError` | MIDI path is wrong | Use an absolute path; verify the file exists |
| `parse_error` in result | Invalid ABC syntax | Ask Claude to fix the notation and retry |
| `write_error` in result | Output directory missing | Create the destination directory first |

## Development

```bash
cd music-edit-mcp
uv sync --dev
uv run ruff check src/     # Lint
uv run ruff format src/    # Format
uv run mypy src/           # Type check
uv run pytest              # Test
```

## License

MIT — see [LICENSE](../LICENSE)
