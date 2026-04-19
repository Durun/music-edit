"""Generate test fixture MIDI files. Run manually: uv run python tests/fixtures/build_fixtures.py"""

from pathlib import Path

from music21 import chord, meter, stream, tempo
from music21.note import Note


def build_test_score() -> stream.Score:
    """Build a 4-measure I-V-vi-IV progression with melody in 4/4 at 120bpm."""
    score = stream.Score()
    part = stream.Part()

    part.append(meter.TimeSignature("4/4"))
    part.append(tempo.MetronomeMark(number=120))

    # I-V-vi-IV: C major - G major - A minor - F major
    chord_data = [
        (["C4", "E4", "G4"], "C4"),   # I:  C major, melody C
        (["G3", "B3", "D4"], "D4"),   # V:  G major, melody D
        (["A3", "C4", "E4"], "E4"),   # vi: A minor, melody E
        (["F3", "A3", "C4"], "C4"),   # IV: F major, melody C
    ]

    for chord_pitches, _melody_pitch in chord_data:
        measure = stream.Measure()
        # Whole-note chord
        c = chord.Chord(chord_pitches, quarterLength=4.0)
        measure.append(c)
        part.append(measure)

    # Add melody as a second part
    melody_part = stream.Part()
    melody_part.append(meter.TimeSignature("4/4"))

    for _, melody_pitch in chord_data:
        measure = stream.Measure()
        n = Note(melody_pitch, quarterLength=4.0)
        measure.append(n)
        melody_part.append(measure)

    score.append(part)
    score.append(melody_part)
    return score


if __name__ == "__main__":
    out_path = Path(__file__).parent / "test_score.mid"
    score = build_test_score()
    score.write("midi", fp=str(out_path))
    print(f"Written: {out_path} ({out_path.stat().st_size} bytes)")
