# /// script
# requires-python = ">=3.13"
# ///
from xml.etree import ElementTree
from functools import reduce
from operator import iconcat
from typing import Generator
import zipfile
import sys
import re


def replace_punctuation(text: str) -> str:
    """Replace unicode punctuation marks (‘’´“”–-) with ASCII aproximations"""
    return text.translate(
        dict([(ord(a), ord(b)) for a, b in zip("‘’´“”–-", "'''\"\"--")])
    )


def remove_trailing_slide_number(text: str) -> str:
    """Remove one or more numbers at the end of a line"""
    return re.sub(r"\d{1,}$", r"", text)


def get_slide_num(filename: str) -> int:
    """Get the slide number from a powerpoint XML file name"""
    return int("".join([c for c in filename if c.isnumeric()]))


def get_notes(filename: str) -> Generator[tuple[int, str], None, None]:
    """Extract note text from all slides powerpoint.
    Return the slide number of the note slide and its filename
    """
    with zipfile.ZipFile(filename, "r") as ppt_file:
        # Get only notes slide from the list of files in the PPT archive
        # Slides are not listed in order; sort by slide number
        for file in sorted(
            filter(
                lambda f: f.startswith("ppt/notesSlides/notesSlide"),
                ppt_file.namelist(),
            ),
            key=get_slide_num,
        ):
            with ppt_file.open(file) as note:
                yield (get_slide_num(file), note.read().decode("utf-8"))


def get_text(note: str) -> str:
    """Extract text from a PowerPoint notes slide"""
    root = ElementTree.fromstring(note)
    tags = root.findall(".//{*}t")
    text = "".join(reduce(iconcat, map(lambda x: x.text, tags), []))

    # Clean text
    text = replace_punctuation(text)
    text = remove_trailing_slide_number(text)

    return text


def main() -> None:
    if len(sys.argv) == 1:
        print("No file provided")
        print('Usage: \tpython extract_notes "My PowerPoint Presentation.pptx"')
        sys.exit(1)

    file = sys.argv[1]
    for slide_number, note in get_notes(file):
        print(f"# {slide_number}")
        print(get_text(note))
        print()


if __name__ == "__main__":
    main()
