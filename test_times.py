import pytest
from times import time_range, compute_overlap_time



@pytest.mark.parametrize(
    "range1, range2, expected",
    [
        pytest.param(
            time_range("2010-01-12 10:00:00", "2010-01-12 12:00:00"),
            time_range("2010-01-12 10:30:00", "2010-01-12 10:45:00", 2, 60),
            [
                ("2010-01-12 10:30:00", "2010-01-12 10:37:00"),
                ("2010-01-12 10:38:00", "2010-01-12 10:45:00"),
            ],
            id="given_input",
        ),
        pytest.param(
            time_range("2010-01-12 08:00:00", "2010-01-12 09:00:00"),
            time_range("2010-01-12 10:00:00", "2010-01-12 11:00:00"),
            [],
            id="non_overlapping",
        ),
        pytest.param(
            time_range("2010-01-12 09:00:00", "2010-01-12 10:00:00"),
            time_range("2010-01-12 10:00:00", "2010-01-12 11:00:00"),
            [],
            id="touching",
        ),
    ],
)
def test_compute_overlap(range1, range2, expected):
    result = compute_overlap_time(range1, range2)
    assert result == expected



def test_multiple_intervals_each():
    first = time_range("2010-01-12 09:00:00", "2010-01-12 11:00:00", 2, 30)
    second = time_range("2010-01-12 10:00:00", "2010-01-12 12:00:00", 2, 30)
    result = compute_overlap_time(first, second)
    assert len(result) > 0
    for start, end in result:
        assert start >= "2010-01-12 10:00:00"
        assert end <= "2010-01-12 11:00:00"



def test_time_range_backwards_raises():
    with pytest.raises(ValueError, match="must be after"):
        time_range("2010-01-12 12:00:00", "2010-01-12 10:00:00")
