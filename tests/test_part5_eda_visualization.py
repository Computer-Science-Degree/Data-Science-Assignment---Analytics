"""Autograder tests for Part 5. DO NOT EDIT."""
import pandas as pd
import pytest
from matplotlib.figure import Figure

from assignment import part5_eda_visualization as p5


@pytest.fixture(scope="module")
def titanic():
    return p5.load_titanic()


def assert_labelled(ax):
    assert ax.get_title().strip(), "every chart needs a title"
    assert ax.get_xlabel().strip(), "every chart needs an x-axis label"
    assert ax.get_ylabel().strip(), "every chart needs a y-axis label"


def data_axes(fig):
    """Axes that hold data (ignores colour-bar axes)."""
    return [ax for ax in fig.axes if ax.get_label() != "<colorbar>"]


def test_load_titanic(titanic):
    assert titanic.shape == (891, 12)


def test_survival_rate_by_sex(titanic):
    result = p5.survival_rate_by(titanic, "Sex")
    assert result["female"] == pytest.approx(74.2)
    assert result["male"] == pytest.approx(18.89)


def test_survival_rate_by_class(titanic):
    result = p5.survival_rate_by(titanic, "Pclass")
    assert list(result.index) == [1, 2, 3]
    assert result[1] == pytest.approx(62.96)
    assert result[3] == pytest.approx(24.24)


def test_add_age_group(titanic):
    result = p5.add_age_group(titanic)
    assert "AgeGroup" not in titanic.columns, "the input DataFrame must not be modified"
    counts = result["AgeGroup"].value_counts()
    assert counts["Young Adult"] == 358
    assert counts["Child"] == 69
    assert counts["Senior"] == 22
    assert result["AgeGroup"].isna().sum() == 177


def test_plot_age_distribution(titanic, tmp_path):
    path = tmp_path / "age.png"
    fig = p5.plot_age_distribution(titanic, save_path=path)
    assert isinstance(fig, Figure)
    ax = data_axes(fig)[0]
    assert_labelled(ax)
    assert len(ax.patches) == 30, "use 30 bins"
    assert path.exists()


def test_plot_survival_by_class(titanic):
    fig = p5.plot_survival_by_class(titanic)
    assert isinstance(fig, Figure)
    ax = data_axes(fig)[0]
    assert_labelled(ax)
    heights = sorted(round(p.get_height(), 1) for p in ax.patches if p.get_height() > 0)
    assert heights == [24.2, 47.3, 63.0]


def test_plot_fare_by_class(titanic):
    fig = p5.plot_fare_by_class(titanic)
    assert isinstance(fig, Figure)
    assert_labelled(data_axes(fig)[0])


def test_plot_age_vs_fare(titanic):
    fig = p5.plot_age_vs_fare(titanic)
    assert isinstance(fig, Figure)
    ax = data_axes(fig)[0]
    assert_labelled(ax)
    assert ax.collections, "expected scatter points"
    assert ax.get_legend() is not None, "add a legend for Survived"


def test_plot_correlation_heatmap(titanic):
    fig = p5.plot_correlation_heatmap(titanic)
    assert isinstance(fig, Figure)
    ax = data_axes(fig)[0]
    assert_labelled(ax)
    tick_labels = {t.get_text() for t in ax.get_xticklabels()}
    assert "PassengerId" not in tick_labels
    assert {"Survived", "Pclass", "Fare"} <= tick_labels
    assert len(ax.texts) >= 36, "use annot=True"


def test_create_dashboard(titanic, tmp_path):
    path = tmp_path / "dash" / "dashboard.png"
    fig = p5.create_dashboard(titanic, save_path=path)
    assert isinstance(fig, Figure)
    axes = data_axes(fig)
    assert len(axes) == 4, "use a 2 x 2 grid"
    for ax in axes:
        assert_labelled(ax)
    assert fig._suptitle is not None and fig._suptitle.get_text().strip()
    assert path.exists()
    assert isinstance(titanic, pd.DataFrame)
