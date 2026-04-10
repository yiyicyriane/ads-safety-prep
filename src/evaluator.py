import logging

logger = logging.getLogger(__name__)


def compute_confusion_matrix(true_labels: list, predicted_labels: list) -> dict:
    """
    Compute the confusion matrix for the given true and predicted labels.

    Args:
        true_labels: list of true labels(human labeled), either "suspicious" or "safe"
        predicted_labels: list of system predicted labels, either "suspicious" or "safe"

    Returns:
        {
            "TP": int,
            "FP": int,
            "TN": int,
            "FN": int
        }
    
    Exception:
        ValueError: If two lists are not of the same length.
    """
    if len(true_labels) != len(predicted_labels):
        raise ValueError(
            f"Length not match: true_labels has {len(true_labels)} labels, but predicted_labels has {len(predicted_labels)} labels"
        )
    
    TP = 0
    FP = 0
    TN = 0
    FN = 0

    for true, predicted in zip(true_labels, predicted_labels):
        if true == "suspicious" and predicted == "suspicious":
            TP += 1
        elif true == "suspicious" and predicted == "safe":
            FN += 1
        elif true == "safe" and predicted == "safe":
            TN += 1
        elif true == "safe" and predicted == "suspicious":
            FP += 1
        else:
            logger.warning(f"Unexpected label: true={true}, predicted={predicted}")
    
    return {
        "TP": TP,
        "FP": FP,
        "TN": TN,
        "FN": FN
    }


def print_confusion_matrix(matrix: dict) -> None:
    """
    Print the confusion matrix in a readable format.

    Args:
        matrix: the return value from compute_confusion_matrix()
    """
    TP = matrix["TP"]
    FP = matrix["FP"]
    TN = matrix["TN"]
    FN = matrix["FN"]

    print("\n=== Confusion Matrix ===")
    print("-" * 40)
    print(f"{'':20} {'Predicted: suspicious':>10} {'Predicted: safe':>10}")
    print(f"{'True: suspicious':20} {TP:>10} {FN:>10}")
    print(f"{'True: safe':20} {FP:>10} {TN:>10}")
    print("-" * 40)
    print(f"TP={TP}  FP={FP}  TN={TN}  FN={FN}")
    print()