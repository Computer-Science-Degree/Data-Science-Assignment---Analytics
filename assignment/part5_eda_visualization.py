"""
PART 5 — Exploratory Data Analysis & Visualisation                (15 points)
==============================================================================
Course topics: 12 EDA Workflow (overview, univariate, bivariate, multivariate),
               13 Matplotlib (line/bar/hist/scatter, subplots, customisation),
               14 Seaborn (distributions, box/violin, heatmaps)

Scenario
--------
Use ``data/titanic.csv`` to answer: *who survived the Titanic disaster, and
why?* You will compute grouped survival rates and build charts.

Rules for every plotting function
---------------------------------
- Create the figure yourself: ``fig, ax = plt.subplots(...)`` and draw on ``ax``
  (for seaborn pass ``ax=ax``).
- Every axes must have a non-empty title, x-label and y-label.
- RETURN the ``matplotlib.figure.Figure`` (do not call ``plt.show()``).
- If ``save_path`` is given, save the figure there with ``fig.savefig``.

Run your code:      python -m assignment.part5_eda_visualization
                    (charts are written to the outputs/ folder)
Run the tests:      pytest tests/test_part5_eda_visualization.py -v
"""
import matplotlib

matplotlib.use("Agg")  # draw to files, not to a window (needed for CI)

import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402,F401
import seaborn as sns  # noqa: E402,F401

from assignment.paths import OUTPUT_DIR, TITANIC_CSV  # noqa: E402


def load_titanic(path=TITANIC_CSV):
    """Load the Titanic dataset into a DataFrame."""
    # TODO: implement
    raise NotImplementedError


def survival_rate_by(df, column):
    """Survival rate (%) for each group in ``column``.

    Return a Series indexed by the group values (sorted by index), values are
    the mean of ``Survived`` * 100, rounded to 2 decimals.

    Example: survival_rate_by(df, "Sex") -> female ~74.2, male ~18.89
    """
    # TODO: implement
    raise NotImplementedError


def add_age_group(df):
    """Return a copy of ``df`` with a new ``AgeGroup`` column created with
    ``pd.cut`` using these bins and labels:

        bins   = [0, 12, 18, 35, 60, 120]
        labels = ["Child", "Teen", "Young Adult", "Adult", "Senior"]

    Passengers with missing Age get a missing AgeGroup.
    """
    # TODO: implement
    raise NotImplementedError


def plot_age_distribution(df, save_path=None):
    """Histogram of passenger Age (drop missing ages first), 30 bins."""
    # TODO: implement
    raise NotImplementedError


def plot_survival_by_class(df, save_path=None):
    """Bar chart of survival rate (%) for each Pclass (exactly 3 bars).

    Bonus (not graded): add value labels on top of each bar.
    """
    # TODO: implement
    raise NotImplementedError


def plot_fare_by_class(df, save_path=None):
    """Seaborn box plot of Fare (y) for each Pclass (x)."""
    # TODO: implement
    raise NotImplementedError


def plot_age_vs_fare(df, save_path=None):
    """Scatter plot of Age (x) vs Fare (y), coloured by Survived.

    Include a legend so the reader knows which colour means survived.
    """
    # TODO: implement
    raise NotImplementedError


def plot_correlation_heatmap(df, save_path=None):
    """Seaborn heatmap of the correlation matrix of the NUMERIC columns
    (excluding PassengerId), annotated with values (``annot=True``).

    Note: a heatmap's axes have no x/y-label by default; set them anyway,
    e.g. "Feature".
    """
    # TODO: implement
    raise NotImplementedError


def create_dashboard(df, save_path=OUTPUT_DIR / "eda_dashboard.png"):
    """Build ONE figure with a 2 x 2 grid of subplots summarising the data:

        [0, 0] Age histogram          [0, 1] Survival rate by Sex (bar)
        [1, 0] Survival rate by Pclass [1, 1] Fare box plot by Pclass

    - Give the whole figure a title with ``fig.suptitle(...)``.
    - Every subplot needs a title, x-label and y-label.
    - Call ``fig.tight_layout()``.
    - Save to ``save_path`` (create the folder if needed) and return the Figure.
    """
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    titanic = load_titanic()
    print(survival_rate_by(titanic, "Sex"))
    print(survival_rate_by(titanic, "Pclass"))
    print(survival_rate_by(add_age_group(titanic), "AgeGroup"))

    OUTPUT_DIR.mkdir(exist_ok=True)
    plot_age_distribution(titanic, OUTPUT_DIR / "age_distribution.png")
    plot_survival_by_class(titanic, OUTPUT_DIR / "survival_by_class.png")
    plot_fare_by_class(titanic, OUTPUT_DIR / "fare_by_class.png")
    plot_age_vs_fare(titanic, OUTPUT_DIR / "age_vs_fare.png")
    plot_correlation_heatmap(titanic, OUTPUT_DIR / "correlation_heatmap.png")
    create_dashboard(titanic)
    plt.close("all")
    print("Charts saved to", OUTPUT_DIR)
