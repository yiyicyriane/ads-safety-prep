# Responsible for: load opt-125m, apply LoRA, train on our labeled ads data,
# save the fine-tuned model weights

import os
import json
import torch
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    TrainingArguments,
    Trainer,
    DataCollatorForSeq2Seq,
)
from peft import LoraConfig, get_peft_model, TaskType
from datasets import Dataset

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ── Configuration ──────────────────────────────────────────────
MODEL_NAME = "facebook/opt-125m"
TRAIN_PATH = os.path.join(BASE_DIR, "../data/finetune/train.jsonl")
VAL_PATH   = os.path.join(BASE_DIR, "../data/finetune/val.jsonl")
OUTPUT_DIR = os.path.join(BASE_DIR, "../output/finetune")
MAX_LENGTH = 256   #    Maximum number of tokens per training sample
EPOCHS     = 3     # Number of training epochs
# ────────────────────────────────────────────────────────


def load_jsonl(path: str) -> list:
    """
    Load a .jsonl file and return a list of dicts.

    Args:
        path: path to the .jsonl file

    Returns:
        list of dicts
    """
    with open(path, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def format_prompt(sample: dict) -> str:
    """
    Format a training sample into a single prompt string.

    The format is:
        ### Instruction:
        <instruction>

        ### Input:
        <input>

        ### Response:
        <output>

    Args:
        sample: dict with keys 'instruction', 'input', 'output'

    Returns:
        formatted prompt string
    """
    return (
        f"### Instruction:\n{sample['instruction']}\n\n"
        f"### Input:\n{sample['input']}\n\n"
        f"### Response:\n{sample['output']}"
    )


def tokenize(sample: dict, tokenizer) -> dict:
    """
    Tokenize a single training sample.

    Args:
        sample: dict with keys 'instruction', 'input', 'output'
        tokenizer: the model's tokenizer

    Returns:
        dict with 'input_ids', 'attention_mask', 'labels'
    """
    prompt = format_prompt(sample)
    result = tokenizer(
        prompt,
        truncation=True,
        max_length=MAX_LENGTH,
        padding="max_length",
    )
    result["labels"] = result["input_ids"].copy()
    return result


def main():
    print(f"[Setup] Loading tokenizer and model: {MODEL_NAME}")
    print("[Setup] This may take a few minutes on first run (downloading model)...")

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    tokenizer.pad_token = tokenizer.eos_token

    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        torch_dtype=torch.float32,   # Use float32 for CPU
    )

    # ── Add LoRA layers to the model ──────────────────────────────
    print("[LoRA] Applying LoRA configuration...")
    lora_config = LoraConfig(
        task_type=TaskType.CAUSAL_LM,
        r=8,                    # rank, control the size of the LoRA matrix
        lora_alpha=16,          # scaling factor, usually set to 2 * rank
        lora_dropout=0.05,      # dropout, to prevent overfitting
        target_modules=["q_proj", "v_proj"],  # on which layers to add LoRA
    )
    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()
    # ────────────────────────────────────────────────────

    # ── Load and process data ──────────────────────────────────
    print("[Data] Loading training and validation data...")
    train_raw = load_jsonl(TRAIN_PATH)
    val_raw   = load_jsonl(VAL_PATH)

    train_dataset = Dataset.from_list(train_raw)
    val_dataset   = Dataset.from_list(val_raw)

    print("[Data] Tokenizing datasets...")
    train_dataset = train_dataset.map(
        lambda x: tokenize(x, tokenizer),
        remove_columns=train_dataset.column_names,
    )
    val_dataset = val_dataset.map(
        lambda x: tokenize(x, tokenizer),
        remove_columns=val_dataset.column_names,
    )
    # ────────────────────────────────────────────────────

    # ── Training configuration ────────────────────────────────────────
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    training_args = TrainingArguments(
        output_dir=OUTPUT_DIR,
        num_train_epochs=EPOCHS,
        per_device_train_batch_size=2,
        per_device_eval_batch_size=2,
        eval_strategy="epoch",
        save_strategy="epoch",
        logging_steps=5,
        learning_rate=2e-4,
        fp16=False,             # CPU does not support fp16
        report_to="none",       # not report to wandb or other platforms
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
        data_collator=DataCollatorForSeq2Seq(
            tokenizer, model=model, padding=True
        ),
    )
    # ────────────────────────────────────────────────────

    print(f"[Train] Starting training for {EPOCHS} epochs...")
    trainer.train()

    print(f"[Save] Saving fine-tuned model to {OUTPUT_DIR}...")
    model.save_pretrained(OUTPUT_DIR)
    tokenizer.save_pretrained(OUTPUT_DIR)

    print("\n[Done] Fine-tuning complete.")
    print(f"  Model saved to: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()