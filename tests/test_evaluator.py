import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../src"))

from evaluator import compute_confusion_matrix, print_confusion_matrix, compute_precision, compute_recall


def test_basic():
    """
    Test the basic functionality of the evaluator.
    """
    true_labels = ["suspicious", "suspicious", "safe", "safe", "suspicious"]
    predicted_labels = ["suspicious", "safe", "suspicious", "safe", "suspicious"]

    # Expected: TP=2, FP=1, TN=1, FN=1
    matrix = compute_confusion_matrix(true_labels, predicted_labels)
    print_confusion_matrix(matrix)

    assert matrix["TP"] == 2, f"TP should be 2, but got {matrix['TP']}"
    assert matrix["FP"] == 1, f"FP should be 1, but got {matrix['FP']}"
    assert matrix["TN"] == 1, f"TN should be 1, but got {matrix['TN']}"
    assert matrix["FN"] == 1, f"FN should be 1, but got {matrix['FN']}"

    print("✅test_basic passed!")


def test_all_suspicious():
    """
    Test edge case where all ads are predicted as suspicious.
    """
    true_labels = ["suspicious", "safe", "suspicious", "safe"]
    predicted_labels = ["suspicious"] * len(true_labels)

    # Expected: TP=2, FP=2, TN=0, FN=0
    matrix = compute_confusion_matrix(true_labels, predicted_labels)
    print_confusion_matrix(matrix)

    assert matrix["TP"] == 2, f"TP should be 2, but got {matrix['TP']}"
    assert matrix["FP"] == 2, f"FP should be 2, but got {matrix['FP']}"
    assert matrix["TN"] == 0, f"TN should be 0, but got {matrix['TN']}"
    assert matrix["FN"] == 0, f"FN should be 0, but got {matrix['FN']}"

    print("✅test_all_suspicious passed!")

def test_all_safe():
    """
    Test edge case where all ads are predicted as safe.
    """
    true_labels = ["suspicious", "safe", "suspicious", "safe"]
    predicted_labels = ["safe"] * len(true_labels)

    # Expected: TP=0, FP=0, TN=2, FN=2
    matrix = compute_confusion_matrix(true_labels, predicted_labels)
    print_confusion_matrix(matrix)

    assert matrix["TP"] == 0, f"TP should be 0, but got {matrix['TP']}"
    assert matrix["FP"] == 0, f"FP should be 0, but got {matrix['FP']}"
    assert matrix["TN"] == 2, f"TN should be 2, but got {matrix['TN']}"
    assert matrix["FN"] == 2, f"FN should be 2, but got {matrix['FN']}"

    print("✅test_all_safe passed!")


def test_length_mismatch():
    """
    Test edge case where the length of true and predicted labels do not match.
    """
    true_labels = ["suspicious", "safe", "suspicious"]
    predicted_labels = ["suspicious"]

    # Expected: ValueError
    try:
        compute_confusion_matrix(true_labels, predicted_labels)
        print("❌test_length_mismatch failed!")
    except ValueError as e:
        print(f"✅test_length_mismatch passed! {e}")


def test_precision_recall_basic():
    """
    Test the basic functionality of the precision and recall.
    """
    matrix = {"TP": 2, "FP": 1, "TN": 1, "FN": 1}

    precision = compute_precision(matrix)
    recall = compute_recall(matrix)

    # Expected: precision=2/3, recall=2/3
    assert abs(precision - 2/3) < 1e-6, f"Expected precision {2/3:.6f}, but got {precision:.6f}"
    assert abs(recall - 2/3) < 1e-6, f"Expected recall {2/3:.6f}, but got {recall:.6f}"

    print("✅test_precision_recall_basic passed!")


def test_all_suspicious_metrics():
    """
    Test edge case where all ads are predicted as suspicious.
    Recall should be 1.0, precision depends on class balance.
    """
    matrix = {"TP": 2, "FP": 2, "TN": 0, "FN": 0}

    precision = compute_precision(matrix)
    recall = compute_recall(matrix)

    # Expected: precision=0.5, recall=1.0
    assert abs(precision - 0.5) < 1e-6, f"Expected precision 0.5, but got {precision:.6f}"
    assert abs(recall - 1.0) < 1e-6, f"Expected recall 1.0, but got {recall:.6f}"

    print("✅test_all_suspicious_metrics passed!")


def test_zero_division():
    """
    Test that zero division is handled gracefully.
    """
    # No predicted suspicious at all -> precision denominator is 0
    matrix_no_pred_suspicious = {"TP": 0, "FP": 0, "TN": 3, "FN": 2}
    precision = compute_precision(matrix_no_pred_suspicious)
    assert precision == 0.0

    # No actual suspicious ads -> recall denominator is 0
    matrix_no_actual_suspicious = {"TP": 0, "FP": 1, "TN": 2, "FN": 0}
    recall = compute_recall(matrix_no_actual_suspicious)
    assert recall == 0.0

    print("✅test_zero_division passed!")


if __name__ == "__main__":
    test_basic()
    test_all_suspicious()
    test_all_safe()
    test_length_mismatch()
    test_precision_recall_basic()
    test_all_suspicious_metrics()
    test_zero_division()