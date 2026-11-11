"""Autograder tests for Part 4. DO NOT EDIT."""
import numpy as np
import pandas as pd
import pytest

from assignment import part4_data_cleaning as p4


@pytest.fixture(scope="module")
def raw():
    return p4.load_raw()


@pytest.fixture(scope="module")
def clean():
    return p4.clean_pipeline(save_to=None)


def test_load_raw(raw):
    assert raw.shape == (126, 10)


def test_missing_report(raw):
    report = p4.missing_report(raw)
    assert list(report.columns) == ["missing_count", "missing_pct"]
    assert report.index[0] == "MonthlySalary"
    assert report.loc["MonthlySalary", "missing_count"] == 11
    assert report.loc["Education", "missing_pct"] == pytest.approx(2.38)
    assert "EmployeeID" not in report.index
    assert report["missing_count"].is_monotonic_decreasing


def test_remove_duplicates(raw):
    result = p4.remove_duplicates(raw)
    assert len(result) == 120
    assert not result.duplicated().any()
    assert list(result.index) == list(range(120))
    assert len(raw) == 126, "the input DataFrame must not be modified"


def test_standardize_text():
    df = pd.DataFrame({
        "Name": ["  KOFI MENSAH ", "ama owusu", np.nan],
        "City": [" accra", "KUMASI  ", np.nan],
        "Department": [" hr", "Sales", " marketing"],
    })
    result = p4.standardize_text(df)
    assert result["Name"].tolist()[:2] == ["Kofi Mensah", "Ama Owusu"]
    assert pd.isna(result.loc[2, "Name"])
    assert result["City"].tolist()[:2] == ["Accra", "Kumasi"]
    assert pd.isna(result.loc[2, "City"])
    assert result["Department"].tolist() == ["HR", "Sales", "Marketing"]
    assert df.loc[0, "Name"] == "  KOFI MENSAH ", "the input DataFrame must not be modified"


def test_fix_invalid_values():
    df = pd.DataFrame({"Age": [-4, 18, 45, 70, 230], "PerformanceScore": [50, 145, -10, 0, 100]})
    result = p4.fix_invalid_values(df)
    assert result["Age"].isna().tolist() == [True, False, False, False, True]
    assert result["PerformanceScore"].isna().tolist() == [False, True, True, False, False]


def test_iqr_bounds():
    lower, upper = p4.iqr_bounds(pd.Series([1, 2, 3, 4, 5, 6, 7, 8, np.nan]))
    assert lower == pytest.approx(-2.5)
    assert upper == pytest.approx(11.5)
    assert isinstance(lower, float)


def test_cap_outliers():
    df = pd.DataFrame({"x": [1, 2, 3, 4, 5, 6, 7, 100, np.nan]})
    result = p4.cap_outliers(df, "x")
    _, upper = p4.iqr_bounds(df["x"])
    assert result["x"].max() == pytest.approx(upper)
    assert result["x"].isna().sum() == 1
    assert df["x"].max() == 100, "the input DataFrame must not be modified"


def test_fill_missing():
    df = pd.DataFrame({
        "Age": [30, np.nan, 40, 50],
        "PerformanceScore": [60, 70, np.nan, 90],
        "MonthlySalary": [1000, np.nan, 5000, 7000],
        "Department": ["Sales", "Sales", "Finance", "Sales"],
        "City": ["Accra", np.nan, "Tamale", "Accra"],
        "Education": ["BSc", "BSc", np.nan, "MSc"],
    })
    result = p4.fill_missing(df)
    assert result.isna().sum().sum() == 0
    assert result.loc[1, "Age"] == 40
    assert result.loc[2, "PerformanceScore"] == 70
    assert result.loc[1, "MonthlySalary"] == 4000  # median of Sales salaries 1000 & 7000
    assert result.loc[1, "City"] == "Unknown"
    assert result.loc[2, "Education"] == "BSc"


def test_convert_types():
    df = pd.DataFrame({"JoinDate": ["2020-01-05"], "Age": [34.6], "Education": ["MSc"]})
    result = p4.convert_types(df)
    assert pd.api.types.is_datetime64_any_dtype(result["JoinDate"])
    assert pd.api.types.is_integer_dtype(result["Age"])
    assert result.loc[0, "Age"] == 35
    assert isinstance(result["Education"].dtype, pd.CategoricalDtype)
    assert result["Education"].cat.ordered
    assert list(result["Education"].cat.categories) == ["BSc", "MSc", "PhD"]


def test_clean_pipeline_result(clean):
    assert clean.shape == (120, 10)
    assert clean.isna().sum().sum() == 0
    assert clean["Age"].between(18, 70).all()
    assert clean["PerformanceScore"].between(0, 100).all()
    assert clean["MonthlySalary"].max() < 10000
    assert set(clean["Department"]) == {"Engineering", "Finance", "HR", "Marketing", "Sales"}
    assert set(clean["City"]) == {"Accra", "Cape Coast", "Kumasi", "Takoradi", "Tamale", "Unknown"}
    assert (clean["Name"] == clean["Name"].str.strip().str.title()).all()


def test_clean_pipeline_saves_csv(tmp_path):
    out = tmp_path / "out" / "clean.csv"
    p4.clean_pipeline(save_to=out)
    assert out.exists()
    assert len(pd.read_csv(out)) == 120
