from dataclasses import dataclass

import pytest

from .issue_title_parser import ParsedTitle, parse_issue_title


@dataclass(frozen=True)
class ParseTestExample:
    input_value: str
    expected: ParsedTitle


@pytest.mark.parametrize(
    ("example"),
    [
        ParseTestExample(
            input_value="test(#77): test description",
            expected=ParsedTitle(prefix="test", description="test description"),
        ),
        ParseTestExample(
            input_value="test: test description",
            expected=ParsedTitle(prefix="test", description="test description"),
        ),
    ],
)
def test_issue_title_parsing(example: ParseTestExample):
    assert example.expected == parse_issue_title(example.input_value)
