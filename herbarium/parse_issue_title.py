import re
from dataclasses import dataclass


@dataclass(frozen=True)
class ParsedIssue:
    prefix: str
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


def parse_issue_title(issue_title: str) -> ParsedIssue:
    # Get all string between start and first ":"
    prefix = re.findall(r"^(.*?)[:\(]", issue_title)[0]
    description = re.findall(r": (.*)$", issue_title)[0]

    return ParsedIssue(
        prefix=sanitise_text_for_git(input_string=prefix),
        description=sanitise_text_for_git(input_string=description),
    )


def sanitise_text_for_bash(input_string: str) -> str:
    char_to_remove = ["`"]
    for character in char_to_remove:
        input_string = input_string.replace(character, "")
    return input_string
