"""Tests for music_edit_mcp.converters."""

import os
import tempfile
from pathlib import Path

import pytest

from music_edit_mcp.converters import read_score, write_score
from music_edit_mcp.models import WriteResult

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


# ── write_score tests ─────────────────────────────────────────────────────────

WRITE_ROUNDTRIP_CASES = [
    pytest.param(
        "X:1\nM:4/4\nL:1/4\nK:C\n|[CEG]4|[G,B,D]4|[A,CE]4|[F,A,C]4|\n",
        0,
        ["[CEG]4", "[G,B,D]4", "[A,CE]4", "[F,A,C]4"],
        id="chord-progression-I-V-vi-IV",
    ),
    pytest.param(
        "X:1\nM:4/4\nL:1/4\nK:C\n|C4|D4|E4|C4|\n",
        0,
        ["C4", "D4", "E4", "C4"],
        id="melody-whole-notes",
    ),
    pytest.param(
        "X:1\nM:4/4\nL:1/4\nK:C\n|C2 E2|G4|\n",
        0,
        ["C2 E2", "G4"],
        id="mixed-durations",
    ),
]


@pytest.mark.parametrize("abc,section,expected_bars", WRITE_ROUNDTRIP_CASES)
def test_write_score_roundtrip(abc: str, section: int, expected_bars: list[str]) -> None:
    """write → re-read で各小節の音符が保たれる。"""
    with tempfile.NamedTemporaryFile(suffix=".mid", delete=False) as f:
        out_path = f.name
    try:
        result = write_score(abc, out_path)
        assert result.success, result.errors
        bars = _abc_bars(read_score(out_path, format="abc"), section_index=section)
        assert bars == expected_bars
    finally:
        os.unlink(out_path)


WRITE_ERROR_CASES = [
    pytest.param(
        "GARBAGE ###$$$",
        str(Path(tempfile.gettempdir()) / "out_never_written.mid"),
        "parse_error",
        id="invalid-abc",
    ),
    pytest.param(
        "X:1\nM:4/4\nL:1/4\nK:C\n|C4|\n",
        "/nonexistent/dir/out.mid",
        "write_error",
        id="bad-path",
    ),
]


@pytest.mark.parametrize("abc,path,expected_type", WRITE_ERROR_CASES)
def test_write_score_failure(abc: str, path: str, expected_type: str) -> None:
    """失敗ケースは success=False と適切な error type を返す。"""
    result = write_score(abc, path)
    assert isinstance(result, WriteResult)
    assert not result.success
    assert result.errors[0].type == expected_type
