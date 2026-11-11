"""
PART 6 — Data Preparation, First ML Models & Evaluation           (20 points)
==============================================================================
Course topics: 15 ML Foundations (supervised learning, ML workflow),
               16 Data Preparation (train/test split, encoding, scaling),
               17 First ML Models (linear & logistic regression, KNN,
               decision trees), 18 Model Evaluation (accuracy, precision,
               recall, F1, confusion matrix, regression metrics,
               overfitting, cross-validation)

Scenario
--------
Predict whether a Titanic passenger survived (``Survived`` = 1) from their
ticket class, sex, age, family and fare. Follow the ML workflow:

    prepare features -> split -> scale -> train -> evaluate -> compare

Use scikit-learn. Always pass ``random_state=42`` where it is accepted so your
results are reproducible.

Run your code:      python -m assignment.part6_machine_learning
Run the tests:      pytest tests/test_part6_machine_learning.py -v
"""
import numpy as np  # noqa: F401
import pandas as pd  # noqa: F401
from sklearn.linear_model import LogisticRegression  # noqa: F401
from sklearn.metrics import (  # noqa: F401
    accuracy_score,
    confusion_matrix,
    f1_score,
    mean_absolute_error,
    mean_squared_error,
    precision_score,
    r2_score,
    recall_score,
)
from sklearn.model_selection import cross_val_score, train_test_split  # noqa: F401
from sklearn.neighbors import KNeighborsClassifier  # noqa: F401
from sklearn.preprocessing import StandardScaler  # noqa: F401
from sklearn.tree import DecisionTreeClassifier  # noqa: F401

from assignment.paths import TITANIC_CSV

FEATURE_COLUMNS = [
    "Pclass", "Sex", "Age", "SibSp", "Parch", "Fare",
    "FamilySize", "IsAlone", "Embarked_Q", "Embarked_S",
]


def prepare_features(df):
    """Turn the raw Titanic DataFrame into a feature matrix X and target y.

    Steps (do NOT modify the input DataFrame):
      1. Age      : fill missing values with the median Age
      2. Embarked : fill missing values with the mode
      3. Sex      : encode male -> 0, female -> 1
      4. FamilySize = SibSp + Parch + 1
      5. IsAlone    = 1 if FamilySize == 1 else 0
      6. One-hot encode Embarked with ``pd.get_dummies(..., drop_first=True)``
         so you get Embarked_Q and Embarked_S (C is the dropped baseline).
         Make sure these columns are integers (0/1), not booleans.

    Return ``(X, y)`` where X has exactly the columns in FEATURE_COLUMNS
    (in that order) and y is the ``Survived`` Series.
    """
    # TODO: implement
    raise NotImplementedError


def split_data(X, y, test_size=0.2, random_state=42):
    """Split into train and test sets, STRATIFIED by y.

    Return ``X_train, X_test, y_train, y_test``.
    """
    # TODO: implement
    raise NotImplementedError


def scale_features(X_train, X_test):
    """Standardise features with ``StandardScaler``.

    IMPORTANT: fit the scaler on the TRAINING data only, then transform both
    (fitting on test data would leak information).

    Return ``X_train_scaled, X_test_scaled, scaler``.
    """
    # TODO: implement
    raise NotImplementedError


def train_models(X_train, y_train):
    """Train three classifiers and return them in a dict:

        "logistic_regression": LogisticRegression(max_iter=1000)
        "knn":                 KNeighborsClassifier(n_neighbors=5)
        "decision_tree":       DecisionTreeClassifier(max_depth=4, random_state=42)

    Every model must be fitted.
    """
    # TODO: implement
    raise NotImplementedError


def evaluate_classifier(model, X_test, y_test):
    """Return a dict with:

        accuracy, precision, recall, f1   — floats rounded to 4 decimals
        confusion_matrix                  — a nested list [[TN, FP], [FN, TP]]
    """
    # TODO: implement
    raise NotImplementedError


def compare_models(models, X_test, y_test):
    """Evaluate every model in ``models`` and return a DataFrame indexed by
    model name with columns accuracy, precision, recall, f1, sorted by f1
    descending."""
    # TODO: implement
    raise NotImplementedError


def cross_validated_accuracy(model, X, y, cv=5):
    """Return the MEAN accuracy from ``cross_val_score`` with ``cv`` folds,
    rounded to 4 decimals."""
    # TODO: implement
    raise NotImplementedError


def tree_depth_experiment(X_train, X_test, y_train, y_test, depths=(1, 2, 4, 8, 16)):
    """Detect overfitting: train a DecisionTreeClassifier(max_depth=d,
    random_state=42) for each depth and record train and test accuracy.

    Return a DataFrame indexed by depth with columns ``train_accuracy`` and
    ``test_accuracy``. (Watch how the gap between train and test accuracy
    grows as the tree gets deeper: that gap is overfitting.)
    """
    # TODO: implement
    raise NotImplementedError


def regression_metrics(y_true, y_pred):
    """Return a dict of regression metrics, each rounded to 4 decimals:

        mae, mse, rmse, r2
    """
    # TODO: implement
    raise NotImplementedError


def fit_fare_regression(df):
    """Simple linear regression: predict ``Fare`` from ``Pclass`` only.

    Use ``train_test_split(test_size=0.2, random_state=42)`` (no stratify),
    fit a ``LinearRegression`` and return ``(model, metrics)`` where metrics
    is ``regression_metrics`` on the TEST set.
    """
    # TODO: implement (hint: from sklearn.linear_model import LinearRegression)
    raise NotImplementedError


if __name__ == "__main__":
    titanic = pd.read_csv(TITANIC_CSV)
    X, y = prepare_features(titanic)
    X_train, X_test, y_train, y_test = split_data(X, y)
    X_train_s, X_test_s, _ = scale_features(X_train, X_test)
    models = train_models(X_train_s, y_train)
    print(compare_models(models, X_test_s, y_test))
    print("CV accuracy (logistic):",
          cross_validated_accuracy(LogisticRegression(max_iter=1000), X, y))
    print(tree_depth_experiment(X_train, X_test, y_train, y_test))
    print("Fare regression:", fit_fare_regression(titanic)[1])
