import re
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class IssueTitle:
    prefix: Optional[str]
    content: str

    def __str__(self) -> str:
        if self.prefix:
            return f"{self.prefix}: {self.content}"
        return f"{self.content}"


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


def parse_issue_title(issue_title: str) -> IssueTitle:
    # Get all string between start and first ":"
    try:
        prefix = re.findall(r"^(.*?)[\(:]", issue_title)[0]
    except IndexError:
        # No prefix found, return without prefix
        return IssueTitle(prefix=None, content=issue_title)

    description = re.findall(r": (.*)$", issue_title)[0]
    return IssueTitle(prefix=prefix, content=description)
