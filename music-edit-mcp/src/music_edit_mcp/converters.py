"""music21 wrappers for MIDI <-> MusicXML <-> ABC conversion. Implemented in Phase 1+."""

from pathlib import Path

from music21 import converter, stream
from music21.musicxml.m21ToXml import GeneralObjectExporter


def read_score(midi_path: str) -> str:
    """Parse a MIDI file and return its MusicXML representation as a string."""
    path = Path(midi_path)
    if not path.exists():
        raise FileNotFoundError(f"MIDI file not found: {midi_path}")

    result = converter.parse(str(path))

    if not isinstance(result, stream.Score):
        raise ValueError(f"Expected Score, got {type(result).__name__}")

    xml_bytes: bytes = GeneralObjectExporter(result).parse()
    return xml_bytes.decode("utf-8")
