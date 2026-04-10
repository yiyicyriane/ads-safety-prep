import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../src"))

from evaluator import compute_confusion_matrix, print_confusion_matrix


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


if __name__ == "__main__":
    test_basic()
    test_all_suspicious()
    test_all_safe()
    test_length_mismatch()