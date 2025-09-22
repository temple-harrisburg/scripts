# /// script
# requires-python = ">=3.13"
# dependencies = [
#   "chardet>=5.0.0",
# ]
# ///
import sys
import re

# from enum import Flag, auto
from chardet.universaldetector import UniversalDetector

VTT_TS = re.compile(r"\d{2}:\d{2}.\d{3} --> \d{2}:\d{2}.\d{3}")
SRT_TS = re.compile(r"\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}")
SRT_ID = re.compile(r"^\d*$")

# class SubType(Flag):
#     UNK = auto()
#     VTT = auto()
#     SRT = auto()


def detect_encoding(filename: str) -> str:
    detector = UniversalDetector()
    for line in open(filename, "rb"):
        detector.feed(line)
        if detector.done:
            break
    detector.close()
    return detector.result["encoding"]


def text_from_sub(filename: str) -> str:
    # type_flag: SubType = SubType.UNK
    transcript: list[str] = []
    encoding: str = detect_encoding(filename)
    with open(filename, "r", encoding=encoding) as sub_file:
        for line in sub_file.readlines():
            if line == "WEBVTT":
                # type_flag = SubType.VTT
                continue

            if VTT_TS.match(line):
                # type_flag = SubType.VTT
                continue

            if SRT_TS.match(line):
                # type_flag = SubType.SRT
                continue

            if SRT_ID.match(line):
                # type_flag = SubType.SRT
                continue

            if line == "\n":
                continue

            else:
                transcript.append(line.strip())

    return " ".join(transcript)


def main() -> None:
    files = sys.argv[1:]
    for file in files:
        transcript = text_from_sub(file)
        sys.stdout.write(f"{transcript}\n")


if __name__ == "__main__":
    main()
