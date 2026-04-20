# music-edit-mcp

> 日本語版はこちら → [docs/README.ja.md](./docs/README.ja.md)

Ask Claude to edit your DAW tracks in plain English — no notation software needed.

## What it does

Export a MIDI file from your DAW, tell Claude what to change, and get an updated MIDI file back.

**Example:**
> "The chord in measure 3 sounds muddy. Spread the voicing out and save to `song_v2.mid`."

Claude reads your score, makes the edit, and writes the new MIDI file. You re-import it into your DAW and listen.

## Requirements

- Python 3.12 or higher
- [uv](https://docs.astral.sh/uv/) — a Python package manager
- [Claude Code](https://claude.ai/code)

## Setup

### 1. Install

```bash
git clone https://github.com/durun/music-edit.git
cd music-edit/music-edit-mcp
uv sync
```

### 2. Add to Claude Code

Edit your Claude Code MCP config and add the following entry. Replace `/absolute/path/to/music-edit` with the actual path where you cloned the repo.

```json
{
  "mcpServers": {
    "music-edit-mcp": {
      "command": "uv",
      "args": [
        "run",
        "--project",
        "/absolute/path/to/music-edit/music-edit-mcp",
        "music-edit-mcp"
      ]
    }
  }
}
```

Restart Claude Code. `music-edit-mcp` should appear in the connected tools list.

## Usage

Export a MIDI file from your DAW, then ask Claude anything about it:

**Inspect your score:**
- "Read `~/Desktop/song.mid` and tell me the chord progression."
- "What key is `~/Desktop/song.mid` in? Are there any notes that clash with the chords?"

**Edit and save:**
- "Transpose the melody in `song.mid` up a fifth and save the result to `song_v2.mid`."
- "The bass in measures 5–8 clashes with the harmony. Fix it and overwrite the file."
- "Add a passing tone on beat 3 of measure 2."

Claude will read, edit, and write the MIDI file automatically. Re-import into your DAW to hear the result.

## Troubleshooting

**"File not found" error**
Use the full path (e.g. `/Users/yourname/Music/song.mid`, not `~/Music/song.mid`).

**The edit doesn't sound right**
Just ask Claude to try again with a different approach, or describe what you want more specifically.

**"Couldn't write the file" error**
Make sure the destination folder already exists before asking Claude to save there.

## License

MIT — see [LICENSE](../LICENSE)
