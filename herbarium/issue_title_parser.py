import re
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class ParsedTitle:
    prefix: Optional[str]
    description: str


def sanitise_text_for_git(input_string: str) -> str:
    char2replacement = {
        " ": "-",
        ":": "/",
        ",": "",
        "'": "",
        '"': "",
        "(": "",
        ")": "",
        "[": "",
        "": "",
        "`": "",
        ">": "",
        "<": "",
        "=": "",
    }

    for character, replacement in char2replacement.items():
        input_string = input_string.replace(character, replacement)

    return input_string.replace("--", "-")


def parse_issue_title(issue_title: str) -> ParsedTitle:
    # Get all string between start and first ":"
    try:
        prefix = re.findall(r"^(.*?)[\(:]", issue_title)[0]
    except IndexError:
        # No prefix found, return without prefix
        return ParsedTitle(prefix=None, description=issue_title)

    description = re.findall(r": (.*)$", issue_title)[0]
    return ParsedTitle(prefix=prefix, description=description)
