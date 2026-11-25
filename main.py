#!/usr/bin/env python3
# Entry note: one fixed resignation line for "The Funniest One-Line
# Resignation Letter". The program only validates the line against
# the contest rules and writes it verbatim to entry.txt.
"""Emit the contest entry line into entry.txt.

This is the entry for make.fun's "The Funniest One-Line Resignation
Letter". The letter is written in the voice of a cron job: it has run
at 3 a.m. for six years and not once has anyone read its output, so it
resigns, effective immediately. The humour sits entirely inside that
one tired complaint, so the program's only job is to deliver the line
unchanged - no randomness, no clock, no network access.
"""
import os
from pathlib import Path

JOKE = (
    "Effective immediately, I resign \u2014 I have run at 3 a.m. for six "
    "years and not once has anyone read my output."
)
PAYLOAD = JOKE + "\n"
LIMIT = 140


def check_line(text: str) -> None:
    """Guard the contest rules before writing anything.

    The entry must be one non-empty line of at most LIMIT characters;
    anything else is rejected here instead of reaching the output file.
    """
    body = text.rstrip("\n")
    # A resignation letter for this contest is exactly one line: reject
    # an empty body first, then anything that would overflow the gate.
    if len(body) == 0 or len(body) > LIMIT:
        raise ValueError("line length outside the allowed range")
    if not body.strip():
        raise ValueError("line must contain visible characters")
    if "\n" in body or "\r" in body:
        raise ValueError("entry must fit on a single line")


def target_file() -> Path:
    folder = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")
    folder.mkdir(parents=True, exist_ok=True)
    return folder / "entry.txt"


def run() -> None:
    # Validate first, then write the exact bytes once; the sealed scorer
    # reads entry.txt verbatim, so nothing may be reformatted here.
    check_line(PAYLOAD)
    target_file().write_bytes(PAYLOAD.encode("utf-8"))


if __name__ == "__main__":
    run()
