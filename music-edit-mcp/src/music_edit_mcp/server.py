"""MCP server entry point."""

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("music-edit-mcp")


@mcp.tool()
def read_score(midi_path: str, format: str = "musicxml") -> str:
    """Read a MIDI file and return its score representation.

    Args:
        midi_path: Absolute or relative path to a .mid file.
        format: Output format — "musicxml" (default) or "abc".
                Use "abc" for compact LLM-friendly notation.
                Use "musicxml" for full structural detail.

    The returned string can be used to answer questions about
    pitches, chords, rhythm, time signature, tempo, and structure.
    """
    from music_edit_mcp.converters import read_score as _read_score

    if format not in ("musicxml", "abc"):
        raise ValueError(f"Invalid format: {format!r}. Choose 'musicxml' or 'abc'.")

    return _read_score(midi_path, format=format)  # type: ignore[arg-type]


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
