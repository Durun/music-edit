"""music21 wrappers for MIDI <-> MusicXML <-> ABC conversion."""

import fractions
from pathlib import Path
from typing import Literal, cast

from music21 import converter, key, note, pitch, stream, tempo
from music21.chord import Chord
from music21.meter.base import TimeSignature
from music21.musicxml.m21ToXml import GeneralObjectExporter

from music_edit_mcp.models import WriteError, WriteResult

ScoreFormat = Literal["musicxml", "abc"]


def _pitch_to_abc(p: pitch.Pitch) -> str:
    """Convert a music21 Pitch to an ABC pitch string (no duration)."""
    acc = p.accidental
    acc_str = ""
    if acc is not None:
        mod = acc.modifier
        if mod == "#":
            acc_str = "^"
        elif mod == "##":
            acc_str = "^^"
        elif mod == "-":
            acc_str = "_"
        elif mod == "--":
            acc_str = "__"
        elif mod == "n":
            acc_str = "="

    oct_num = p.octave if p.octave is not None else 4
    step = p.step  # "A"-"G"
    if oct_num >= 6:
        return acc_str + step.lower() + "'" * (oct_num - 5)
    elif oct_num == 5:
        return acc_str + step.lower()
    elif oct_num == 4:
        return acc_str + step
    else:
        return acc_str + step + "," * (4 - oct_num)


def _ql_to_abc(quarter_length: float) -> str:
    """Convert a quarter-length duration to an ABC duration modifier (L:1/4 baseline)."""
    r = fractions.Fraction(quarter_length).limit_denominator(64)
    if r == fractions.Fraction(1):
        return ""
    elif r.denominator == 1:
        return str(r.numerator)
    elif r.numerator == 1:
        return f"/{r.denominator}"
    return f"{r.numerator}/{r.denominator}"


def _element_to_abc(el: note.GeneralNote) -> str:
    """Convert a music21 Note, Chord, or Rest to an ABC token."""
    dur = _ql_to_abc(el.duration.quarterLength)
    if isinstance(el, note.Rest):
        return "z" + dur
    if isinstance(el, Chord):
        pitches = "".join(_pitch_to_abc(p) for p in el.pitches)
        return f"[{pitches}]{dur}"
    if isinstance(el, note.Note):
        return _pitch_to_abc(el.pitch) + dur
    return ""


def _score_to_abc(score: stream.Score) -> str:
    """Serialize a music21 Score to ABC notation (multi-part, L:1/4 baseline)."""
    sections: list[str] = []

    for idx, part in enumerate(score.parts, start=1):
        lines: list[str] = [f"X:{idx}"]

        ts: TimeSignature | None = (
            part.recurse().getElementsByClass(TimeSignature).first()
            or score.recurse().getElementsByClass(TimeSignature).first()
        )
        lines.append(f"M:{ts.numerator}/{ts.denominator}" if ts else "M:4/4")
        lines.append("L:1/4")

        mm: tempo.MetronomeMark | None = (
            score.recurse().getElementsByClass(tempo.MetronomeMark).first()
        )
        if mm is not None:
            lines.append(f"Q:1/4={int(mm.number)}")

        ks: key.KeySignature | None = (
            part.recurse().getElementsByClass(key.KeySignature).first()
            or score.recurse().getElementsByClass(key.KeySignature).first()
        )
        if ks is not None:
            k = ks.asKey()
            mode_suffix = "" if k.mode == "major" else k.mode[0]
            lines.append(f"K:{k.tonic.name}{mode_suffix}")
        else:
            lines.append("K:C")

        measures = list(part.getElementsByClass(stream.Measure))
        bars: list[str] = []
        for measure in measures:
            tokens = [_element_to_abc(el) for el in measure.notesAndRests]
            bars.append(" ".join(t for t in tokens if t))

        lines.append("|" + "|".join(bars) + "|")
        sections.append("\n".join(lines))

    return "\n\n".join(sections) + "\n"


def _abc_to_score(abc_str: str) -> stream.Score:
    """Parse an ABC string into a music21 Score.

    Multi-tune ABC (multiple X: sections) is merged into a single Score via
    Opus.mergeScores() so all parts are preserved.

    Raises:
        ValueError: If the parsed result cannot be converted to a Score.
    """
    parsed: stream.Score | stream.Part | stream.Opus = converter.parse(
        abc_str, format="abc"
    )
    if isinstance(parsed, stream.Opus):
        return cast(stream.Score, parsed.mergeScores())  # type: ignore[no-untyped-call]
    if isinstance(parsed, stream.Part):
        score = stream.Score()
        score.append(parsed)  # type: ignore[no-untyped-call]
        return score
    return parsed


def write_score(abc_str: str, midi_path: str) -> WriteResult:
    """Convert an ABC notation string to a MIDI file.

    Args:
        abc_str:   ABC notation string (single or multi-part, L:1/4 baseline).
        midi_path: Destination path for the .mid file. Parent directory must exist.

    Returns:
        WriteResult(success=True, errors=[]) on success, or
        WriteResult(success=False, errors=[WriteError(...)]) on failure.
        Error types: "parse_error" or "write_error".
    """
    try:
        score = _abc_to_score(abc_str)
    except Exception as exc:
        return WriteResult(
            success=False,
            errors=[WriteError(type="parse_error", message=str(exc))],
        )

    try:
        score.write("midi", fp=midi_path)  # type: ignore[no-untyped-call]
    except OSError as exc:
        return WriteResult(
            success=False,
            errors=[WriteError(type="write_error", message=str(exc))],
        )

    return WriteResult(success=True, errors=[])


def read_score(midi_path: str, format: ScoreFormat = "musicxml") -> str:
    """Parse a MIDI file and return its score as a string (MusicXML or ABC)."""
    path = Path(midi_path)
    if not path.exists():
        raise FileNotFoundError(f"MIDI file not found: {midi_path}")

    result = converter.parse(str(path))

    if not isinstance(result, stream.Score):
        raise ValueError(f"Expected Score, got {type(result).__name__}")

    if format == "musicxml":
        xml_bytes: bytes = GeneralObjectExporter(result).parse()
        return xml_bytes.decode("utf-8")

    return _score_to_abc(result)
