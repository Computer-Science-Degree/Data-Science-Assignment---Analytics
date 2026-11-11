"""
PART 1 — Python Foundations for Data Work                         (10 points)
==============================================================================
Course topics: 02 Python Fundamentals, 03 Data Structures, 04 Control Flow,
               05 Functions, 06 Error Handling, 07 File Handling

Scenario
--------
A small electronics shop ("Makola Gadgets") exported its inventory to
``data/inventory.json``. The export is a bit messy: some prices are "N/A",
one stock value is "unknown", and one product has no ratings yet.

Your job is to write small, reusable functions that load, clean and
summarise this file using ONLY the Python standard library
(``json``, ``csv``, ``pathlib``). Do NOT use pandas or numpy in this part.

Run your code:      python -m assignment.part1_python_foundations
Run the tests:      pytest tests/test_part1_python_foundations.py -v
"""
import csv  # noqa: F401  (you will need this)
import json  # noqa: F401  (you will need this)
from pathlib import Path  # noqa: F401  (you will need this)

from assignment.paths import INVENTORY_JSON, OUTPUT_DIR


def load_inventory(path=INVENTORY_JSON):
    """Read the inventory JSON file and return it as a Python dict.

    Requirements
    - Use a ``with`` block to open the file.
    - If the file does not exist, raise ``FileNotFoundError`` with a helpful
      message that includes the path.

    Example
    >>> data = load_inventory()
    >>> data["store"]
    'Makola Gadgets'
    """
    # TODO: implement
    raise NotImplementedError


def safe_float(value, default=None):
    """Convert ``value`` to a float. Return ``default`` if conversion fails.

    Use try/except (catch ``ValueError`` and ``TypeError``).

    Examples
    >>> safe_float("3.5")
    3.5
    >>> safe_float("N/A") is None
    True
    >>> safe_float(None, default=0.0)
    0.0
    """
    # TODO: implement
    raise NotImplementedError


def average_rating(ratings):
    """Return the mean of a list of ratings rounded to 2 decimal places.

    Return ``None`` for an empty list (do not divide by zero!).

    >>> average_rating([4, 5, 5, 4])
    4.5
    >>> average_rating([]) is None
    True
    """
    # TODO: implement
    raise NotImplementedError


def clean_products(products):
    """Return a NEW list of cleaned product dicts (do not mutate the input).

    For each product dict produce a dict with exactly these keys:
        sku, name, category, price, stock, avg_rating

    - ``price``: float, or ``None`` if it cannot be converted (use safe_float)
    - ``stock``: int, or ``None`` if it cannot be converted
    - ``avg_rating``: result of ``average_rating(product["ratings"])``
    """
    # TODO: implement
    raise NotImplementedError


def inventory_value(products):
    """Return the total value of stock on hand: sum(price * stock).

    ``products`` is a list of CLEANED products. Skip any product whose price
    or stock is ``None``. Round the result to 2 decimal places.
    """
    # TODO: implement
    raise NotImplementedError


def products_by_category(products):
    """Group product names by category.

    Return a dict mapping category -> alphabetically sorted list of names.

    >>> products_by_category([{"name": "B", "category": "X"},
    ...                       {"name": "A", "category": "X"}])
    {'X': ['A', 'B']}
    """
    # TODO: implement
    raise NotImplementedError


def low_stock(products, threshold=10):
    """Return a sorted list of SKUs whose stock is known AND below ``threshold``.

    Products with ``stock`` of ``None`` are NOT low stock — they are unknown.
    """
    # TODO: implement
    raise NotImplementedError


def write_summary_csv(products, path=OUTPUT_DIR / "inventory_summary.csv"):
    """Write cleaned products to a CSV file using ``csv.DictWriter``.

    - Header row must be: sku,name,category,price,stock,avg_rating
    - ``None`` values should be written as empty cells.
    - Create the parent folder if it does not exist.
    - Return the path as a ``pathlib.Path``.
    """
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    inventory = load_inventory()
    cleaned = clean_products(inventory["products"])
    print(f"Store: {inventory['store']} ({len(cleaned)} products)")
    print("Inventory value:", inventory_value(cleaned), inventory["currency"])
    print("By category:", products_by_category(cleaned))
    print("Low stock:", low_stock(cleaned))
    print("Saved:", write_summary_csv(cleaned))
