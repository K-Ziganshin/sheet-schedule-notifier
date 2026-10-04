from schedule_notifier import build_schedule, find_row


def test_schedule():
    rows = [["x"], ["name", "1.10", "2.10"], ["Ivan", "D", ""]]
    row = find_row(rows, "Ivan")
    assert build_schedule(rows[1], row) == ["name - Ivan", "1.10 - D"]


def test_missing_person():
    assert find_row([["a"]], "Nobody") is None
