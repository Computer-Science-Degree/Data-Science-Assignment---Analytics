"""Autograder tests for Part 6. DO NOT EDIT."""
import numpy as np
import pandas as pd
import pytest
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.utils.validation import check_is_fitted

from assignment import part6_machine_learning as p6
from assignment.paths import TITANIC_CSV


@pytest.fixture(scope="module")
def titanic():
    return pd.read_csv(TITANIC_CSV)


@pytest.fixture(scope="module")
def prepared(titanic):
    X, y = p6.prepare_features(titanic)
    X_train, X_test, y_train, y_test = p6.split_data(X, y)
    X_train_s, X_test_s, scaler = p6.scale_features(X_train, X_test)
    models = p6.train_models(X_train_s, y_train)
    return dict(X=X, y=y, X_train=X_train, X_test=X_test, y_train=y_train, y_test=y_test,
                X_train_s=X_train_s, X_test_s=X_test_s, scaler=scaler, models=models)


def test_prepare_features(titanic, prepared):
    X, y = prepared["X"], prepared["y"]
    assert list(X.columns) == p6.FEATURE_COLUMNS
    assert X.shape == (891, 10)
    assert X.isna().sum().sum() == 0
    assert set(X["Sex"].unique()) == {0, 1}
    assert X["Sex"].sum() == 314  # number of female passengers
    assert X["FamilySize"].max() == 11
    assert X["IsAlone"].sum() == 537
    assert X["Embarked_S"].sum() == 646  # 644 + 2 filled with the mode
    assert all(pd.api.types.is_numeric_dtype(X[c]) and X[c].dtype != bool for c in X.columns)
    assert y.name == "Survived" and len(y) == 891
    assert titanic["Age"].isna().sum() == 177, "the input DataFrame must not be modified"


def test_split_data(prepared):
    assert len(prepared["X_train"]) == 712
    assert len(prepared["X_test"]) == 179
    assert prepared["y_train"].mean() == pytest.approx(prepared["y"].mean(), abs=0.01), "stratify by y"


def test_scale_features(prepared):
    X_train_s, X_test_s = np.asarray(prepared["X_train_s"]), np.asarray(prepared["X_test_s"])
    np.testing.assert_allclose(X_train_s.mean(axis=0), 0, atol=1e-7)
    np.testing.assert_allclose(prepared["scaler"].mean_, prepared["X_train"].mean().values)
    assert X_test_s.shape == (179, 10)


def test_train_models(prepared):
    models = prepared["models"]
    assert set(models) == {"logistic_regression", "knn", "decision_tree"}
    assert isinstance(models["logistic_regression"], LogisticRegression)
    assert isinstance(models["knn"], KNeighborsClassifier) and models["knn"].n_neighbors == 5
    assert isinstance(models["decision_tree"], DecisionTreeClassifier) and models["decision_tree"].max_depth == 4
    for model in models.values():
        check_is_fitted(model)


def test_evaluate_classifier(prepared):
    result = p6.evaluate_classifier(prepared["models"]["logistic_regression"], prepared["X_test_s"], prepared["y_test"])
    assert set(result) == {"accuracy", "precision", "recall", "f1", "confusion_matrix"}
    assert result["accuracy"] >= 0.78
    cm = result["confusion_matrix"]
    assert isinstance(cm, list) and len(cm) == 2
    assert sum(map(sum, cm)) == 179
    assert cm[0][0] + cm[0][1] == 110  # actual negatives in test set
    fp, fn, tp = cm[0][1], cm[1][0], cm[1][1]
    assert result["precision"] == pytest.approx(tp / (tp + fp), abs=1e-4)
    assert result["recall"] == pytest.approx(tp / (tp + fn), abs=1e-4)


def test_compare_models(prepared):
    table = p6.compare_models(prepared["models"], prepared["X_test_s"], prepared["y_test"])
    assert list(table.columns) == ["accuracy", "precision", "recall", "f1"]
    assert set(table.index) == {"logistic_regression", "knn", "decision_tree"}
    assert table["f1"].is_monotonic_decreasing


def test_cross_validated_accuracy(prepared):
    score = p6.cross_validated_accuracy(LogisticRegression(max_iter=1000), prepared["X"], prepared["y"])
    assert 0.75 <= score <= 0.85
    assert score == round(score, 4)


def test_tree_depth_experiment(prepared):
    table = p6.tree_depth_experiment(prepared["X_train"], prepared["X_test"], prepared["y_train"], prepared["y_test"])
    assert list(table.index) == [1, 2, 4, 8, 16]
    assert list(table.columns) == ["train_accuracy", "test_accuracy"]
    assert table["train_accuracy"].is_monotonic_increasing
    assert table.loc[16, "train_accuracy"] > 0.95
    gap = table["train_accuracy"] - table["test_accuracy"]
    assert gap.loc[16] > gap.loc[1], "deeper trees should overfit more"


def test_regression_metrics():
    result = p6.regression_metrics([3, 5, 7], [2, 5, 9])
    assert result == {"mae": 1.0, "mse": 1.6667, "rmse": 1.291, "r2": 0.375}


def test_fit_fare_regression(titanic):
    model, metrics = p6.fit_fare_regression(titanic)
    check_is_fitted(model)
    assert model.coef_[0] < 0, "higher class number -> cheaper fare"
    assert metrics["r2"] == pytest.approx(0.3099, abs=0.001)
    assert metrics["rmse"] == pytest.approx(32.6788, abs=0.01)
