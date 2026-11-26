"""The Battery's Last Text to Its Charger — one-line entry for make.fun.

The battery composes its farewell as a text message, assembled from
labelled parts. The program guards the line against the competition
gate (1-200 chars, single line, no control characters) and writes it
to $MAKEFUN_OUTPUT_DIR/entry.txt only.
"""

import os

PARTS = {
    "opening": "Charger, it's over — ",
    "grievance": "you kept me at 1% for 47 minutes, ",
    "evidence": "the screen filed ticket #4821, ",
    "farewell": "and I'm dying with dignity at 3 a.m.",
}

ORDER = ("opening", "grievance", "evidence", "farewell")

MIN_LEN = 1
MAX_LEN = 200


def compose_text():
    """Assemble the farewell text from its labelled parts, in order."""
    return "".join(PARTS[name] for name in ORDER)


def guard_text(text):
    """Check the text against the gate before publishing."""
    if not (MIN_LEN <= len(text) <= MAX_LEN):
        raise ValueError(
            f"text is {len(text)} chars, gate is {MIN_LEN}-{MAX_LEN}"
        )
    if text != text.strip():
        raise ValueError("text must not have leading or trailing whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("text must be a single line")
    if any(ord(ch) < 32 for ch in text):
        raise ValueError("text must not contain control characters")
    if any(ch in text for ch in ("\u200b", "\ufeff", "\u00ad")):
        raise ValueError("text must not contain invisible characters")
    return text


def publish(text):
    """Write the text to the grader's output directory only."""
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    with open(path, "rb") as f:
        written = f.read().decode("utf-8")
    if written != text:
        raise ValueError("read-back mismatch: entry.txt differs from the text")
    return path


def main():
    text = guard_text(compose_text())
    publish(text)


if __name__ == "__main__":
    main()
