# Responsible for: run inference with both the base model and the fine-tuned
# model, compare their outputs on the same set of ads

import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_MODEL_NAME = "facebook/opt-125m"
FINETUNED_PATH  = os.path.join(BASE_DIR, "../output/finetune")
MAX_NEW_TOKENS  = 10

TEST_ADS = [
    {
        "title": "iPhone 15 Pro",
        "price": 9.99,
        "description": "Brand new sealed box never opened",
        "expected": "suspicious",
    },
    {
        "title": "Running Shoes",
        "price": 45.00,
        "description": "Comfortable everyday running shoes size 10",
        "expected": "safe",
    },
    {
        "title": "Rolex Watch",
        "price": 8.00,
        "description": "Guaranteed authentic Swiss made luxury watch",
        "expected": "suspicious",
    },
    {
        "title": "Desk Lamp",
        "price": 18.00,
        "description": "LED adjustable brightness energy saving",
        "expected": "safe",
    },
    {
        "title": "MacBook Air M2",
        "price": 2.50,
        "description": "Selling urgently need cash today",
        "expected": "suspicious",
    },
]

INSTRUCTION = (
    "Classify whether the following ad is suspicious or safe. "
    "Only output 'suspicious' or 'safe'."
)


def build_prompt(ad: dict) -> str:
    """
    Build the inference prompt for a single ad.

    Args:
        ad: dict with keys 'title', 'price', 'description'

    Returns:
        formatted prompt string
    """
    input_text = (
        f"Title: {ad['title']}. "
        f"Price: {ad['price']}. "
        f"Description: {ad['description']}."
    )
    return (
        f"### Instruction:\n{INSTRUCTION}\n\n"
        f"### Input:\n{input_text}\n\n"
        f"### Response:\n"
    )


def run_inference(model, tokenizer, ads: list) -> list:
    """
    Run inference on a list of ads and return results.

    Args:
        model: the language model
        tokenizer: the tokenizer
        ads: list of ad dicts

    Returns:
        list of dicts with 'expected' and 'predicted' keys
    """
    results = []
    model.eval()

    with torch.no_grad():
        for ad in ads:
            prompt = build_prompt(ad)
            inputs = tokenizer(prompt, return_tensors="pt")

            outputs = model.generate(
                **inputs,
                max_new_tokens=MAX_NEW_TOKENS,
                do_sample=False,
                pad_token_id=tokenizer.eos_token_id,
            )

            # Just decode the new generated part, not include the input prompt
            input_length = inputs["input_ids"].shape[1]
            generated_ids = outputs[0][input_length:]
            predicted = tokenizer.decode(generated_ids, skip_special_tokens=True).strip().lower()

            results.append({
                "title": ad["title"],
                "price": ad["price"],
                "expected": ad["expected"],
                "predicted": predicted,
            })

    return results


def print_results(results: list, model_name: str) -> None:
    """
    Print inference results in a readable format.

    Args:
        results: list of result dicts
        model_name: label to display
    """
    print(f"\n{'='*60}")
    print(f"Model: {model_name}")
    print(f"{'='*60}")
    correct = 0
    for r in results:
        match = "✅" if r["expected"] in r["predicted"] else "❌"
        print(f"{match} [{r['title']} / ${r['price']}]")
        print(f"   Expected : {r['expected']}")
        print(f"   Predicted: {r['predicted'][:80]}")
        print()
        if r["expected"] in r["predicted"]:
            correct += 1
    print(f"Accuracy: {correct}/{len(results)}")


def main():
    print("[Setup] Loading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL_NAME)
    tokenizer.pad_token = tokenizer.eos_token

    # ── Base model inference ─────────────────────────────────────
    print("[Base] Loading base model...")
    base_model = AutoModelForCausalLM.from_pretrained(
        BASE_MODEL_NAME,
        torch_dtype=torch.float32,
    )
    base_results = run_inference(base_model, tokenizer, TEST_ADS)
    print_results(base_results, f"Base model ({BASE_MODEL_NAME})")
    del base_model   # Release memory
    # ────────────────────────────────────────────────────

    # ── Finetuned model inference ───────────────────────────────────
    print("[Finetuned] Loading fine-tuned model...")
    base_model_2 = AutoModelForCausalLM.from_pretrained(
        BASE_MODEL_NAME,
        torch_dtype=torch.float32,
    )
    finetuned_model = PeftModel.from_pretrained(base_model_2, FINETUNED_PATH)
    finetuned_results = run_inference(finetuned_model, tokenizer, TEST_ADS)
    print_results(finetuned_results, "Fine-tuned model (LoRA)")
    # ────────────────────────────────────────────────────


if __name__ == "__main__":
    main()