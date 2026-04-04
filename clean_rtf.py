#!/usr/bin/env python3
"""
Clean text extracted from an RTF document:
  1. Remove trailing blanks from each line.
  2. Replace blank-only lines with empty lines.
  3. Join lines within paragraphs (consecutive non-empty lines).
  4. Collapse each sequence of blanks into a single blank.

  Usage:
  cd ~/ntry/words
  .venv/bin/python clean_rtf.py input.rtf          # prints to stdout
  .venv/bin/python clean_rtf.py input.rtf -o out.txt  # writes to file

"""

import argparse
import re
import sys
from striprtf.striprtf import rtf_to_text


def clean_text(text: str) -> str:
    """Apply the four cleaning steps to the extracted text."""
    lines = text.split("\n")

    # 1. Remove trailing blanks
    lines = [line.rstrip() for line in lines]

    # 2. Replace blank-only lines with empty lines (already handled by rstrip,
    #    but be explicit: any line that was only whitespace is now "")

    # 3. Join lines within paragraphs: consecutive non-empty lines are merged
    #    into a single line, separated by a space.
    paragraphs: list[str] = []
    current: list[str] = []

    for line in lines:
        if line == "":
            if current:
                paragraphs.append(" ".join(current))
                current = []
            paragraphs.append("")
        else:
            current.append(line)

    if current:
        paragraphs.append(" ".join(current))

    # 4. Collapse sequences of blanks into a single blank
    paragraphs = [re.sub(r" {2,}", " ", p) for p in paragraphs]

    return "\n".join(paragraphs)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Extract and clean text from an RTF file."
    )
    parser.add_argument("rtf_file", help="Path to the input RTF file")
    parser.add_argument(
        "-o", "--output",
        help="Output file (default: stdout)",
    )
    args = parser.parse_args()

    try:
        with open(args.rtf_file, "r", encoding="utf-8") as f:
            rtf_content = f.read()
    except FileNotFoundError:
        print(f"Error: file not found: {args.rtf_file}", file=sys.stderr)
        sys.exit(1)

    text = rtf_to_text(rtf_content)
    cleaned = clean_text(text)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(cleaned)
    else:
        print(cleaned)


if __name__ == "__main__":
    main()
