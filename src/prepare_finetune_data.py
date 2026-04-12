# Responsible for: read the labeled ads data, transform it to instruction-tuning format, split it with 80% for training and 20% for validation, output two .jsonl files

import os
import json
import pandas as pd
from sklearn.model_selection import train_test_split

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

INSTRUCTION = (
    "Classify whether the following ad is suspicious or safe. "
    "Only output 'suspicious' or 'safe'."
)

def load_labeled_data(input_path: str) -> pd.DataFrame:
    """
    Load the labeled ads data from a CSV file into a pandas dataframe.

    Args:
        input_path: the path to the labeled ads data
    
    Returns:
        A dataframe containing the labeled ads data.
    """
    try:
        df = pd.read_csv(input_path)
    except FileNotFoundError as e:
        print(f"[Loader] Error - file not found: {e}")
        raise
    
    required_columns = {"title", "price", "description", "label"}
    missing = required_columns - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    
    return df


def convert_to_instruction_tuning_format(row: pd.Series) -> dict:
    """
    Convert a row of labeled ads data to instruction-tuning format.

    Args:
        row: a row of labeled ads data
    
    Returns:
        A dictionary containing the instruction-tuning format for that row.
        {
            "instruction": str,
            "input": str,
            "output": str
        }
    """
    input_text = (
        f"Title: {row['title']}. "
        f"Price: {row['price']}. "
        f"Description: {row['description']}."
    )
    return {
        "instruction": INSTRUCTION,
        "input": input_text,
        "output": str(row["label"]).strip().lower()
    }



def save_jsonl(data: list, output_path: str) -> None:
    """
    Save a list of dictionaries to a JSONL file.

    Args:
        data: a list of dictionaries to save
        output_path: the path to the output file
    
    Returns:
        None
    """
    with open(output_path, "w", encoding="utf-8") as f:
        for item in data:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")
    print(f"[Writer] Successfully wrote {len(data)} items to {output_path}")


def main():
    # Load the labeled ads data
    print("[Loader] Loading labeled ads data from CSV file...")
    input_path = os.path.join(BASE_DIR, "../data/labeled_ads.csv")
    df = load_labeled_data(input_path)
    print(f"[Loader] Loaded {len(df)} labeled ads")

    # Transform it to instruction-tuning format
    print("[Converter] Transforming labeled ads data to instruction-tuning format...")
    samples = [convert_to_instruction_tuning_format(row) for _, row in df.iterrows()]

    # Split it with 80% for training and 20% for validation
    print("[Splitter] Splitting data into 80% training and 20% validation sets...")
    train_data, val_data = train_test_split(
        samples,
        test_size=0.2,
        random_state=42,
    )
    print(f"[Splitter] Split into {len(train_data)} training samples and {len(val_data)} validation samples")

    # Output two .jsonl files
    train_output_path = os.path.join(BASE_DIR, "../data/finetune/train.jsonl")
    val_output_path = os.path.join(BASE_DIR, "../data/finetune/val.jsonl")
    os.makedirs(os.path.dirname(train_output_path), exist_ok=True)
    save_jsonl(train_data, train_output_path)
    save_jsonl(val_data, val_output_path)

    print("\n[Writer] Successfully wrote training and validation data to train.jsonl and val.jsonl")
    print(f"   Training data: {train_output_path}")
    print(f"   Validation data: {val_output_path}")


if __name__ == "__main__":
    main()