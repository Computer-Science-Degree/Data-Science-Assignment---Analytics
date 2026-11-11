"""Autograder tests for Part 1. DO NOT EDIT."""
import copy
import csv

import pytest

from assignment import part1_python_foundations as p1


@pytest.fixture
def raw_products():
    return p1.load_inventory()["products"]


@pytest.fixture
def cleaned(raw_products):
    return p1.clean_products(raw_products)


def test_load_inventory():
    data = p1.load_inventory()
    assert isinstance(data, dict)
    assert data["store"] == "Makola Gadgets"
    assert len(data["products"]) == 8


def test_load_inventory_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        p1.load_inventory(tmp_path / "does_not_exist.json")


@pytest.mark.parametrize("value,expected", [("3.5", 3.5), (2, 2.0), ("N/A", None), (None, None), ("", None)])
def test_safe_float(value, expected):
    assert p1.safe_float(value) == expected


def test_safe_float_default():
    assert p1.safe_float("oops", default=0.0) == 0.0


def test_average_rating():
    assert p1.average_rating([4, 5, 5, 4]) == 4.5
    assert p1.average_rating([5, 4, 3]) == 4.0
    assert p1.average_rating([1, 2]) == 1.5
    assert p1.average_rating([]) is None


def test_clean_products_structure(raw_products, cleaned):
    assert len(cleaned) == len(raw_products)
    for item in cleaned:
        assert set(item) == {"sku", "name", "category", "price", "stock", "avg_rating"}


def test_clean_products_values(cleaned):
    by_sku = {p["sku"]: p for p in cleaned}
    assert by_sku["P-301"]["price"] is None
    assert by_sku["P-201"]["stock"] is None
    assert by_sku["P-102"]["avg_rating"] is None
    assert by_sku["P-200"]["avg_rating"] == 4.4
    assert isinstance(by_sku["P-100"]["price"], float)
    assert isinstance(by_sku["P-100"]["stock"], int)


def test_clean_products_does_not_mutate(raw_products):
    original = copy.deepcopy(raw_products)
    p1.clean_products(raw_products)
    assert raw_products == original


def test_inventory_value(cleaned):
    assert p1.inventory_value(cleaned) == pytest.approx(60010.0)


def test_products_by_category(cleaned):
    result = p1.products_by_category(cleaned)
    assert result["Accessories"] == ["Laptop Stand", "USB-C Cable", "Wireless Mouse"]
    assert result["Audio"] == ["Bluetooth Speaker", "Earbuds"]
    assert set(result) == {"Accessories", "Audio", "Phones", "Power"}


def test_low_stock(cleaned):
    assert p1.low_stock(cleaned) == ["P-102", "P-300"]
    assert p1.low_stock(cleaned, threshold=40) == ["P-101", "P-102", "P-200", "P-300"]


def test_write_summary_csv(cleaned, tmp_path):
    out = p1.write_summary_csv(cleaned, tmp_path / "nested" / "summary.csv")
    assert out.exists()
    with open(out, newline="") as f:
        rows = list(csv.DictReader(f))
    assert list(rows[0].keys()) == ["sku", "name", "category", "price", "stock", "avg_rating"]
    assert len(rows) == 8
    feature_phone = next(r for r in rows if r["sku"] == "P-301")
    assert feature_phone["price"] == ""
