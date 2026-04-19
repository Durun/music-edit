"""MCP server entry point."""

from typing import Literal

from mcp.server.fastmcp import FastMCP

from music_edit_mcp.models import WriteResult

mcp = FastMCP("music-edit-mcp")


@mcp.tool()
def read_score(midi_path: str, format: Literal["musicxml", "abc"] = "musicxml") -> str:
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

    return _read_score(midi_path, format=format)


@mcp.tool()
def write_score(abc_str: str, midi_path: str) -> WriteResult:
    """Write an ABC notation string to a MIDI file.

    Args:
        abc_str:   ABC notation string. Supports single-part and multi-part
                   (multiple X: sections, one per part, L:1/4 baseline).
                   Typically the output of read_score(..., format="abc")
                   after LLM edits have been applied.
        midi_path: Destination path for the .mid file. The parent directory
                   must already exist. Overwrites any existing file.

    Returns WriteResult with success=True and empty errors on success, or
    success=False with one WriteError describing the failure.
    Error types:
      - "parse_error": The ABC string could not be parsed.
      - "write_error": The MIDI file could not be written (bad path, permissions).
    """
    from music_edit_mcp.converters import write_score as _write_score

    return _write_score(abc_str, midi_path)


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
