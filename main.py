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


def main() -> None:
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(ENTRY)
    # Self-check the gate the sealed scorer applies: 1-140 chars,
    # UTF-8 text, not only white space, single line.
    with open(path, encoding="utf-8") as f:
        written = f.read()
    assert written == ENTRY
    assert 1 <= len(written) <= 140
    assert written.strip() != ""
    assert "\n" not in written


if __name__ == "__main__":
    main()
