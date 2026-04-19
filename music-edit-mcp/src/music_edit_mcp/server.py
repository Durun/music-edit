"""MCP server entry point. Tools will be implemented in Phase 1+."""

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("music-edit-mcp")


@mcp.tool()
def read_score(midi_path: str) -> str:
    """Read a MIDI file and return its MusicXML representation.

    Pass the absolute or relative path to a .mid file.
    The returned MusicXML string can be used to answer questions about
    pitches, chords, rhythm, time signature, tempo, and structure.
    """
    from music_edit_mcp.converters import read_score as _read_score

    return _read_score(midi_path)


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
