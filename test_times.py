import pytest
import yaml
from times import time_range, compute_overlap_time


with open("fixture.yaml", "r") as f:
    fixtures = yaml.load(f, Loader=yaml.FullLoader)  # 允许 !!python/tuple


param_data = []
for case in fixtures:
    for name, content in case.items():
        t1 = content["time_range_1"]
        t2 = content["time_range_2"]
        expected = content["expected"]
        param_data.append(
            pytest.param(
                time_range(*t1),
                time_range(*t2),
                expected,
                id=name,
            )
        )


@pytest.mark.parametrize("range1, range2, expected", param_data)
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


