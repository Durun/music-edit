"""Tests for music_edit_mcp.converters."""

from pathlib import Path

import pytest

from music_edit_mcp.converters import read_score

FIXTURE_MIDI = Path(__file__).parent / "fixtures" / "test_score.mid"


def test_read_score_returns_xml_string() -> None:
    result = read_score(str(FIXTURE_MIDI))
    assert isinstance(result, str)
    assert result.startswith("<?xml")
    assert "<score-partwise" in result


def test_read_score_contains_expected_pitches() -> None:
    result = read_score(str(FIXTURE_MIDI))
    # C major chord (I) contains C, E, G
    assert "C" in result
    assert "E" in result
    assert "G" in result


def test_read_score_missing_file_raises() -> None:
    with pytest.raises(FileNotFoundError):
        read_score("/nonexistent/path/to/file.mid")


def _abc_bars(abc: str, section_index: int) -> list[str]:
    """Extract bar tokens from an ABC section (0-indexed)."""
    section = abc.strip().split("\n\n")[section_index]
    bar_line = section.splitlines()[-1]
    return [b for b in bar_line.split("|") if b]


def test_read_score_abc_chord_pitches_and_positions() -> None:
    """Part 1 bars match I-V-vi-IV chord progression with correct octaves."""
    result = read_score(str(FIXTURE_MIDI), format="abc")
    bars = _abc_bars(result, section_index=0)
    # Fixture: C major (C4 E4 G4), G major (G3 B3 D4), A minor (A3 C4 E4), F major (F3 A3 C4)
    assert bars[0] == "[CEG]4"    # I:  C4 E4 G4 — whole note
    assert bars[1] == "[G,B,D]4"  # V:  G3 B3 D4 — commas = octave below 4
    assert bars[2] == "[A,CE]4"   # vi: A3 C4 E4
    assert bars[3] == "[F,A,C]4"  # IV: F3 A3 C4


def test_read_score_abc_melody_pitches_and_positions() -> None:
    """Part 2 bars match melody C4 D4 E4 C4 in correct measure order."""
    result = read_score(str(FIXTURE_MIDI), format="abc")
    bars = _abc_bars(result, section_index=1)
    assert bars[0] == "C4"  # measure 1
    assert bars[1] == "D4"  # measure 2
    assert bars[2] == "E4"  # measure 3
    assert bars[3] == "C4"  # measure 4
