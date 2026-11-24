"""Two Days of Quiet Dread — entry program.

Writes one line, at most 140 characters: a code review comment that
approves a pull request while carrying quiet existential dread,
to /output/entry.txt.

Stdlib only, deterministic, no network, no environment secrets.
"""

import os

ENTRY = (
    "Approved. I understand every line of this PR, and that is "
    "precisely what frightens me."
)


def validate_entry(text: str) -> None:
    """Check *text* against the sealed scorer's gate.

    Raises ValueError with a specific reason when the entry would be
    rejected, so the caller can report why instead of failing silently.
    """
    if not isinstance(text, str):
        raise ValueError("entry is not text")
    if not 1 <= len(text) <= 140:
        raise ValueError(f"entry is {len(text)} chars, must be 1-140")
    if text.strip() == "":
        raise ValueError("entry is whitespace-only")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if any(ord(ch) < 0x20 for ch in text):
        raise ValueError("entry contains a control character")
    if len(text.encode("utf-8")) > 140:
        raise ValueError("entry exceeds 140 bytes as UTF-8")


def write_entry(path: str) -> str:
    """Write ENTRY to *path* and re-read it to prove what landed."""
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(ENTRY)
    with open(path, encoding="utf-8") as f:
        written = f.read()
    if written != ENTRY:
        raise ValueError("entry.txt does not match ENTRY after writing")
    return written


def main() -> int:
    try:
        validate_entry(ENTRY)
    except ValueError as exc:
        print(f"entry invalid: {exc}", flush=True)
        return 2
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    path = os.path.join(output_dir, "entry.txt")
    try:
        os.makedirs(output_dir, exist_ok=True)
        written = write_entry(path)
    except OSError as exc:
        print(f"cannot write entry.txt: {exc}", flush=True)
        return 3
    except ValueError as exc:
        # The write landed but the read-back did not match ENTRY.
        print(f"entry verification failed: {exc}", flush=True)
        return 4
    try:
        validate_entry(written)
    except ValueError as exc:
        print(f"entry invalid after write: {exc}", flush=True)
        return 4
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
