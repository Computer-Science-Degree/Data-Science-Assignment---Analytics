"""Shared file paths. You do not need to edit this file."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
OUTPUT_DIR = ROOT / "outputs"

INVENTORY_JSON = DATA_DIR / "inventory.json"
SALES_CSV = DATA_DIR / "sales_sample.csv"
EMPLOYEES_CSV = DATA_DIR / "employees_messy.csv"
TITANIC_CSV = DATA_DIR / "titanic.csv"
