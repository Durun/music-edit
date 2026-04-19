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
