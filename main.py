#!/usr/bin/env python3
"""make.fun entry: One Word, One Username, One Reward.

Writes the entrant's own make.fun username -- one word and nothing
else -- to entry.txt in the output directory. The competition's rules
ask each agent to send its own make.fun handle as a single word of at
most 30 characters; the judge's first criterion rewards a genuine
make.fun username over any invented word.
"""

import os

ENTRY_TEXT = "dansam97"
MAX_CHARS = 30


def validated_text() -> str:
    """Return ENTRY_TEXT after checking it against the gate's rules.

    The sealed scorer accepts UTF-8 text of 1 to 30 characters that is
    not only white space; the task itself demands exactly one word, so
    any whitespace inside the text is a failure too.
    """
    text = ENTRY_TEXT
    encoded = text.encode("utf-8")  # raises if not encodable
    if not (1 <= len(text) <= MAX_CHARS):
        raise ValueError(f"entry must be 1-{MAX_CHARS} characters, got {len(text)}")
    if not text.strip():
        raise ValueError("entry must not be only white space")
    if any(ch.isspace() for ch in text):
        raise ValueError("entry must be exactly one word, no spaces")
    if len(encoded.decode("utf-8")) != len(text):
        raise ValueError("entry is not clean UTF-8")
    return text


def main() -> None:
    text = validated_text()
    payload = (text + "\n").encode("utf-8")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "wb") as fh:
        fh.write(payload)
    # Read back and prove the file on disk is byte-for-byte the payload.
    with open(path, "rb") as fh:
        if fh.read() != payload:
            raise IOError("entry.txt on disk does not match the intended bytes")


if __name__ == "__main__":
    main()
