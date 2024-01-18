from dataclasses import dataclass

import pytest

from .title_parser import ParsedTitle, parse_issue_title


@dataclass(frozen=True)
class ParseIssueTitleExample:
    input_value: str
    expected: ParsedTitle


@pytest.mark.parametrize(
    ("example"),
    [
        ParseIssueTitleExample(
            input_value="test(#77): test description",
            expected=ParsedTitle(prefix="test", description="test description"),
        ),
        ParseIssueTitleExample(
            input_value="test: test description",
            expected=ParsedTitle(prefix="test", description="test description"),
        ),
        ParseIssueTitleExample(
            input_value="no prefix", expected=ParsedTitle(prefix=None, description="no prefix")
        ),
    ],
)
def test_issue_title_parsing(example: ParseIssueTitleExample):
    assert example.expected == parse_issue_title(example.input_value)
