"""Autograder tests for Part 2. DO NOT EDIT."""
import numpy as np
import pytest

from assignment import part2_numpy as p2

TEMPS = [24.5, 26.1, 27.8, 25.0, 29.4, 31.2, 30.0]
SCORES = [[78, 85, 90], [88, 92, 79], [65, 70, 72]]


def test_to_array():
    arr = p2.to_array([1, 2, 3])
    assert isinstance(arr, np.ndarray)
    assert arr.dtype == np.float64
    assert p2.to_array(SCORES).shape == (3, 3)


def test_summary_stats():
    stats = p2.summary_stats(np.array(TEMPS))
    assert stats == {"mean": 27.71, "median": 27.8, "std": 2.41, "min": 24.5, "max": 31.2}
    assert all(type(v) is float for v in stats.values())


def test_min_max_scale():
    scaled = p2.min_max_scale(np.array([10.0, 20.0, 30.0]))
    np.testing.assert_allclose(scaled, [0.0, 0.5, 1.0])
    np.testing.assert_allclose(p2.min_max_scale(np.array([5.0, 5.0])), [0.0, 0.0])


def test_z_scores():
    z = p2.z_scores(np.array(TEMPS))
    assert z.mean() == pytest.approx(0, abs=1e-9)
    assert z.std() == pytest.approx(1)


def test_filter_above():
    np.testing.assert_allclose(p2.filter_above(np.array(TEMPS), 28), [29.4, 31.2, 30.0])


def test_count_in_range():
    result = p2.count_in_range(np.array(TEMPS), 25, 30)
    assert result == 5
    assert isinstance(result, int)


def test_daily_change():
    np.testing.assert_allclose(p2.daily_change(np.array([1.0, 4.0, 2.0])), [3.0, -2.0])


def test_column_means_and_row_totals():
    m = np.array(SCORES, dtype=float)
    np.testing.assert_allclose(p2.column_means(m), [77.0, 82.333333, 80.333333], rtol=1e-5)
    np.testing.assert_allclose(p2.row_totals(m), [253, 259, 207])


def test_top_student():
    assert p2.top_student(np.array(SCORES, dtype=float), ["Ama", "Kofi", "Esi"]) == "Kofi"
