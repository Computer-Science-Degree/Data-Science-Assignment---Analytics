"""Autograder tests for Part 3. DO NOT EDIT."""
import pandas as pd
import pytest

from assignment import part3_pandas_analysis as p3


@pytest.fixture(scope="module")
def sales():
    return p3.load_sales()


def test_load_sales(sales):
    assert isinstance(sales, pd.DataFrame)
    assert sales.shape == (5000, 18)
    assert pd.api.types.is_datetime64_any_dtype(sales["Date"])
    assert sales["Date"].min().year == 2011


def test_dataset_overview(sales):
    info = p3.dataset_overview(sales)
    assert info["rows"] == 5000
    assert info["columns"] == 18
    assert info["missing_total"] == 0
    assert info["numeric_columns"] == [
        "Day", "Year", "Customer_Age", "Order_Quantity", "Unit_Cost",
        "Unit_Price", "Profit", "Cost", "Revenue",
    ]
    assert set(info["categorical_columns"]) == {
        "Month", "Age_Group", "Customer_Gender", "Country", "State",
        "Product_Category", "Sub_Category", "Product",
    }
    assert "Date" not in info["categorical_columns"]


def test_revenue_by_country(sales):
    result = p3.revenue_by_country(sales)
    assert isinstance(result, pd.Series)
    assert list(result.index[:3]) == ["United States", "Australia", "United Kingdom"]
    assert result.iloc[0] == pytest.approx(1204130, abs=1)
    assert result.is_monotonic_decreasing


def test_top_products_by_profit(sales):
    result = p3.top_products_by_profit(sales)
    assert len(result) == 5
    assert result.index[0] == "Mountain-200 Black, 38"
    assert result.iloc[0] == pytest.approx(61247, abs=1)
    assert len(p3.top_products_by_profit(sales, n=3)) == 3


def test_monthly_revenue(sales):
    result = p3.monthly_revenue(sales, 2015)
    assert list(result.index) == list(range(1, 13))
    assert result[1] == pytest.approx(20949, abs=1)
    assert result[12] == pytest.approx(168582, abs=1)


def test_monthly_revenue_fills_missing_months(sales):
    tiny = sales[sales["Date"].dt.month == 3]
    result = p3.monthly_revenue(tiny, 2015)
    assert len(result) == 12
    assert result[1] == 0


def test_category_summary(sales):
    result = p3.category_summary(sales)
    assert list(result.columns) == ["orders", "revenue", "profit", "margin"]
    assert list(result.index) == ["Bikes", "Accessories", "Clothing"]
    assert result.loc["Accessories", "orders"] == 3093
    assert result.loc["Accessories", "margin"] == pytest.approx(58.75)
    assert result.loc["Bikes", "margin"] == pytest.approx(33.32)


def test_high_value_orders(sales):
    assert len(p3.high_value_orders(sales)) == 567
    france = p3.high_value_orders(sales, min_revenue=2000, country="France")
    assert len(france) == 46
    assert (france["Country"] == "France").all()
    assert len(p3.high_value_orders(sales, min_revenue=5000)) < 567


def test_describe_column(sales):
    stats = p3.describe_column(sales["Revenue"])
    expected = {
        "mean": 748.61, "median": 218.0, "mode": 25.0, "range": 11734.0,
        "variance": 1669029.44, "std": 1291.91, "q1": 65.0, "q3": 784.25,
        "iqr": 719.25, "skew": 3.39,
    }
    assert set(stats) == set(expected)
    for key, value in expected.items():
        assert stats[key] == pytest.approx(value, abs=0.011), key
        assert type(stats[key]) is float


def test_skew_direction():
    assert p3.skew_direction(pd.Series([1, 1, 1, 2, 2, 3, 20])) == "right-skewed"
    assert p3.skew_direction(pd.Series([-20, 1, 2, 2, 3, 3, 3])) == "left-skewed"
    assert p3.skew_direction(pd.Series([1, 2, 3, 4, 5])) == "approximately symmetric"
