#!/usr/bin/env python3
"""Columns added to parse_cbj.py's tables, computed from the same one-frame-per-second OCR.

  attempts.gameplay_frames  frames recognised as gameplay between the attempt's start_t and end_t
  attempts.banner_frames    those of them with a banner ad at the bottom of the screen
  offers.decide_seconds     seconds from the first fail screen of a time-out to the last one, both frames included
  levels.label              difficulty label shown for the level on the home screen or the pre-level popup

These functions need the OCR frames, which are not published. Their results are written into the
published tables, so the published checks need only the tables.
"""
import re

from parse_cbj import frame_info  # noqa: F401  (callers parse frames with it)


def banner_frames(frames, attempt):
    """(gameplay frames, gameplay frames with a banner) in [start_t, end_t) of one attempt."""
    s, e = int(attempt["start_t"]), int(attempt["end_t"])
    g = [f for f in frames if s <= f["t"] < e and f["screen"] == "gameplay"]
    return len(g), sum(1 for f in g if f["banner"])


def decide_seconds(frames, offer):
    """Same rule as the scorecard: fail screens with gaps of up to 3 frames belong to one episode."""
    i = next(k for k, f in enumerate(frames) if f["t"] == int(offer["t"]))
    last = i
    for k in range(i, min(len(frames), i + 60)):
        if frames[k]["screen"].startswith("fail_"):
            last = k
        elif k - last > 3:
            break
    return frames[last]["t"] - frames[i]["t"] + 1


def labels(frames):
    """{level: label} for frames that show a level number and a difficulty label together."""
    out = {}
    for f in frames:
        m = re.search(r"(?:^|\| )(?:Level|LEVEL) (\d{1,3})(?: \||$)", f["text"])
        if not m:
            continue
        for lab in ("SUPER HARD", "VERY HARD", "HARD"):
            if re.search(r"(^|\| )" + lab + r"( \||$)", f["text"]):
                out.setdefault(int(m.group(1)), lab)
                break
    return out
