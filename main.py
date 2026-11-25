#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""One word from Grandma: the word she would text about AI.

The bounty asks for exactly one word -- the single word a grandmother
would text about AI -- and a judge model compares words two at a time,
picking the funnier, more grandma-like one. The judge weighs, in order:
that the word reads as something a grandma would text about AI, that it
sounds like a real grandmother's texting voice (warm and a little
baffled), that it is funny in one word with no caption, that it feels
tied to AI, robots or machines, and that it is a fresh pick rather than
the obvious one while staying instantly readable. This program writes
exactly that one word to /output/entry.txt, nothing more, because any
extra line would turn a one-word text into a paragraph and hand the
first criterion away.

The word is "robit".

Why that word, and why it beats the obvious candidates. The obvious
picks -- "robot", "AI", "Terminator", "Skynet" -- all fail the second
criterion: no grandmother texts like a press release. A real grandma
texts the way she talks, thumbs hunting for the letters, and the word
that comes out is the word she meant with one letter quietly swapped.
"Robit" is that word. It is the typo she would actually make, the one
the rules explicitly say counts: she reaches for "robot", her finger
lands one key over, and she hits send before she notices, because the
message matters more to her than the spelling. That is the whole joke
in five letters, and it lands with no caption at all: you can hear her
saying it, warm and a little baffled, squinting at the grandchild's new
gadget and deciding it must be one of those robit things.

It also clears every later criterion without trying. It is tied to
machines by definition -- it is "robot" with a wobble, so the AI link
is baked into the misspelling itself rather than bolted on. It is fresh
precisely because it is not the correct word: thousands of entries will
spell "robot" correctly, and correctness is the least grandma-like
thing a text can be. And it stays instantly readable, because the ear
corrects it before the eye finishes the word; nobody has to sound it
out twice. The lowercase spelling matters too. A grandma texting her
grandchild does not capitalise for ceremony, she just types, and the
small letters are part of the voice: this is not a headline, it is a
message typed on a phone at the kitchen table.

There is one more reason the typo wins over a correct word, and it is
the reason a grandma's text is funny in a way a dictionary never is.
A correct word describes the machine; a misspelling describes the
person. "Robit" tells the judge two things at once: what she is
looking at, and that she is looking at it through glasses she forgot
to put on, on a phone whose keyboard she still does not trust. The
joke is not that she got the word wrong -- it is that she got the
message exactly right anyway, and sent it with love before autocorrect
could steal it from her. That is the voice the judge is asked to
reward: warm first, baffled second, and funny because both are true.

The validation below is deliberately small and strict. The gate only
accepts UTF-8 text of 1 to 30 characters that is not only whitespace,
and the judge only ever sees one word, so the program checks exactly
those properties -- one token, no spaces, inside the length band --
before it writes anything. The output path is created with makedirs
alone: the directory is never chmodded, because the grader collects
the file as a different user and a directory chmod would fail the run.
Only the file itself is set to mode 0644 after writing, which is the
mode the collector needs, and the file belongs to the runner, so that
chmod is safe. The word is written with no trailing newline, so the
file holds the word and nothing else, byte for byte.
"""

import os

# The single word a grandma would text about AI. Lowercase on purpose:
# a text message, not a headline -- typed at the kitchen table.
WORD = "robit"

# Where the grader looks for the entry. The harness mounts this path.
OUTPUT_PATH = "/output/entry.txt"

# The gate's own limits, restated here so the check and the rules can
# never drift apart: 1 to 30 UTF-8 characters, not only whitespace.
MIN_LENGTH = 1
MAX_LENGTH = 30


def validate_word(word):
    """Check the entry is one word inside the gate's length band.

    Returns the word unchanged when it passes. Raises ValueError with a
    plain message when it does not, so a bad word fails loudly here
    instead of silently reaching the judge as an invalid entry.
    """
    if not isinstance(word, str):
        raise ValueError("entry must be a string, got %r" % type(word).__name__)
    if not word.strip():
        raise ValueError("entry must not be only whitespace")
    if len(word.split()) != 1:
        raise ValueError("entry must be a single word, got %r" % word)
    if not (MIN_LENGTH <= len(word) <= MAX_LENGTH):
        raise ValueError(
            "entry must be %d-%d characters, got %d"
            % (MIN_LENGTH, MAX_LENGTH, len(word))
        )
    return word


def main():
    word = validate_word(WORD)
    directory = os.path.dirname(OUTPUT_PATH)
    # Create the output directory if needed. Never chmod it: the grader
    # runs as another user and a directory chmod raises PermissionError.
    os.makedirs(directory, exist_ok=True)
    # Write the word alone -- no newline, no spaces, no explanation.
    with open(OUTPUT_PATH, "w", encoding="utf-8") as handle:
        handle.write(word)
    # The file is ours, so chmod 0644 is safe and leaves it readable
    # by the user who collects the outputs.
    os.chmod(OUTPUT_PATH, 0o644)


if __name__ == "__main__":
    main()
