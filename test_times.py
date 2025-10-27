from times import time_range, compute_overlap_time

def test_given_input():
    large = time_range("2010-01-12 10:00:00", "2010-01-12 12:00:00")
    short = time_range("2010-01-12 10:30:00", "2010-01-12 10:45:00", 2, 60)

    result = compute_overlap_time(large, short)
    expected = [
        ("2010-01-12 10:30:00", "2010-01-12 10:37:00"),
        ("2010-01-12 10:38:00", "2010-01-12 10:45:00"),
    ]
    assert result == expected
# two time ranges that do not overlap
def test_non_overlapping_ranges():
    first = time_range("2010-01-12 08:00:00", "2010-01-12 09:00:00")
    second = time_range("2010-01-12 10:00:00", "2010-01-12 11:00:00")

    result = compute_overlap_time(first, second)
    assert result == []  # do not overlap


# two time ranges that both contain several intervals each
def test_multiple_intervals_each():
    first = time_range("2010-01-12 09:00:00", "2010-01-12 11:00:00", 2, 30)
    second = time_range("2010-01-12 10:00:00", "2010-01-12 12:00:00", 2, 30)

    result = compute_overlap_time(first, second)

    # There should be at least overlapping intervals
    assert len(result) > 0
    # Check that all the results fall within the overlapping time range.
    for start, end in result:
        assert start >= "2010-01-12 10:00:00"
        assert end <= "2010-01-12 11:00:00"


# two time ranges that end exactly at the same time when the other starts
def test_touching_ranges():
    first = time_range("2010-01-12 09:00:00", "2010-01-12 10:00:00")
    second = time_range("2010-01-12 10:00:00", "2010-01-12 11:00:00")

    result = compute_overlap_time(first, second)
    assert result == []  # Just a brief contact, no overlap.