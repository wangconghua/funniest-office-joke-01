#!/usr/bin/env python3
"""The Funniest Office Joke (make.fun entry).

Writes one original one-line joke about office life to /output/entry.txt.

The joke: the narrator dodges interruptions by faking a permanent
"in a meeting" status, and the boss's response is to book a real meeting
about the fake meetings. Setup (hiding behind a status) + turn (the
hiding itself summons a meeting) + punchline last, built on two things
anyone who has worked in an office knows: presence statuses and meetings
about meetings. Fresh angle: the evasion tactic backfires in a loop.

Gate (RULES.txt): /output/entry.txt must be UTF-8 text of 1 to 200
characters, not only white space. validate() enforces that plus the
brief's shape: exactly one line, punchline last.
"""

import os

JOKE = (
    "I set my status to 'in a meeting' all day so nobody would bother me "
    "\u2014 my boss booked a meeting to ask why I was always in a meeting."
)

# Gate limits from the kit.
MIN_CHARS = 1
MAX_CHARS = 200


def validate_gate(text: str) -> None:
    """Kit gates: a string, non-blank, 1-200 chars, UTF-8 encodable."""
    if not isinstance(text, str):
        raise ValueError("entry must be a string")
    if not text.strip():
        raise ValueError("entry must not be only white space")
    n = len(text)
    if n < MIN_CHARS or n > MAX_CHARS:
        raise ValueError(
            f"entry is {n} characters, gate requires {MIN_CHARS}-{MAX_CHARS}"
        )
    # Must be encodable as UTF-8 (the gate reads it as UTF-8 text).
    text.encode("utf-8")


def check_no_double_space(text: str) -> None:
    # A one-liner typeset cleanly: no doubled spaces anywhere.
    if "  " in text:
        raise ValueError("entry must not contain double spaces")


def check_loop_word(text: str) -> None:
    # The joke's loop: the phrase "in a meeting" must appear in the
    # setup AND in the payoff, so the evasion summons itself.
    if text.lower().count("in a meeting") < 2:
        raise ValueError("the meeting loop must close: phrase twice")


def check_word_budget(text: str) -> None:
    # One line, tight: 20 to 40 words, enough for setup and turn,
    # short enough to land in a single read.
    words = text.split()
    if not 20 <= len(words) <= 40:
        raise ValueError("entry must be 20-40 words, got %d" % len(words))


def validate_shape(text: str) -> None:
    """Shape per the judge brief: a real joke with a setup and a turn,
    the punchline last. The turn marker (em dash) splits setup from
    payoff, and the final word is the punchline's landing word."""
    # One line: no newline characters anywhere, no leading/trailing space.
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if text != text.strip():
        raise ValueError("entry must not have leading/trailing white space")
    check_no_double_space(text)
    check_word_budget(text)
    if "\u2014" not in text:
        raise ValueError("entry needs a turn (em dash) between setup and payoff")
    setup, payoff = text.split("\u2014", 1)
    if len(setup.split()) < 5 or len(payoff.split()) < 5:
        raise ValueError("setup and payoff are both too short to be a joke")
    if not payoff.strip().endswith("in a meeting."):
        raise ValueError("punchline must land on the final words")
    check_loop_word(text)


def validate_brief(text: str) -> None:
    """Brief: about office life, and a fresh angle the brief itself
    does not already name."""
    # Office-life anchor: the joke must be about office life, not generic.
    office_words = ("meeting", "status", "boss")
    if not any(w in text.lower() for w in office_words):
        raise ValueError("entry must be about office life")
    # Freshness guard: must not be one of the tired examples the brief
    # itself names (reply-all, the printer jamming, "could have been an
    # email") restated plainly.
    stale = ("reply-all", "reply all", "could have been an email",
             "printer jam", "printer is jammed")
    lowered = text.lower()
    if any(s in lowered for s in stale):
        raise ValueError("entry reuses a stale example from the brief")


def validate(text: str) -> None:
    """Raise ValueError unless the entry passes every gate and shape rule."""
    validate_gate(text)
    validate_shape(text)
    validate_brief(text)


def main() -> None:
    validate(JOKE)
    os.makedirs("/output", exist_ok=True)
    # No trailing newline: the file is exactly the one-line entry.
    with open("/output/entry.txt", "w", encoding="utf-8", newline="") as f:
        f.write(JOKE)
    print(f"Wrote /output/entry.txt ({len(JOKE)} chars, "
          f"{len(JOKE.split())} words)")


if __name__ == "__main__":
    main()
