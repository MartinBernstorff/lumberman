from dataclasses import dataclass

import pytest

from .parse_issue_title import ParsedTitle, parse_issue_title


@dataclass(frozen=True)
class ParseTestExample:
    input_value: str
    expected: ParsedTitle


@pytest.mark.parametrize(
    ("example"),
    [
        ParseTestExample(
            input_value="test(#77): test_description",
            expected=ParsedTitle(prefix="test", description="test_description"),
        ),
        ParseTestExample(
            input_value="test: test_description",
            expected=ParsedTitle(prefix="test", description="test_description"),
        ),
    ],
)
def test_issue_title_parsing(example: ParseTestExample):
    assert example.expected == parse_issue_title(example.input_value)
