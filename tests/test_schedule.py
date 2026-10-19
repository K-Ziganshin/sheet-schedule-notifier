from unittest.mock import MagicMock

import pytest

from schedule_notifier import build_schedule, fetch_rows, find_row, format_message

ROWS = [
    ["Shifts, October"],
    ["Name", "1.10", "2.10", "3.10"],
    ["Ivanov Ivan", "D", "", "N"],
    ["Ivanova Anna", "", "D", ""],
]


def test_schedule_skips_name_column_and_empty_days():
    row = find_row(ROWS[2:], "Ivanov Ivan")
    assert build_schedule(ROWS[1], row, "Ivanov Ivan") == ["1.10 - D", "3.10 - N"]


def test_exact_match_beats_partial_match():
    # "Ivanov" is a substring of "Ivanova" - the exact cell must win
    assert find_row(ROWS[2:], "ivanov  ivan") == ROWS[2]
    assert find_row(ROWS[2:], "Ivanova Anna") == ROWS[3]


def test_partial_match_fallback_and_missing_person():
    assert find_row(ROWS[2:], "Anna") == ROWS[3]
    assert find_row([["a"]], "Nobody") is None


@pytest.mark.parametrize(
    ("lines", "expected"), [(["1.10 - D"], "Schedule for X:\n1.10 - D"), ([], "No shifts for X in the current sheet.")]
)
def test_format_message(lines, expected):
    assert format_message("X", lines) == expected


def test_fetch_rows_parses_csv():
    session = MagicMock()
    session.get.return_value.content = b"a,b\n1,2\n"
    assert fetch_rows("SHEET", session) == [["a", "b"], ["1", "2"]]
    assert "SHEET/export?format=csv" in session.get.call_args.args[0]
