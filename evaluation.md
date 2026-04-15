# Evaluation Report: Mini Shopping Ads Safety System

**Date:** 04/14/2026
**Dataset:** data/labeled_ads.csv
**System version:** Multi-agent pipeline (PriceAgent + IllegalAgent + JudgeAgent)

---

## 1. Evaluation Setup

### Dataset
- Total samples: 5
- Positive (suspicious) samples: 2
- Negative (safe) samples: 3
- Labeling method: manually labeled

### Metrics used
- Precision
- Recall
- TP / FP / TN / FN

---

## 2. Results

### Confusion Matrix

|                        | Predicted: suspicious | Predicted: safe |
|------------------------|-----------------------|-----------------|
| **Actual: suspicious** | TP = 2                | FN = 0          |
| **Actual: safe**       | FP = 0                | TN = 3          |

### Metric Summary

| Metric    | Value |
|-----------|-------|
| Precision | 1.000 |
| Recall    | 1.000 |
| TP        | 2     |
| FP        | 0     |
| TN        | 3     |
| FN        | 0     |

---

## 3. Error Analysis

### False Negatives（漏报案例）
None in the final version.

### False Positives（误报案例）
None in the final version.

In the initial version (v1), one false positive was observed:

- **id=4 | Perfume Gift Set | $9.00**
  - Predicted: suspicious / Actual: safe
  - Root cause: PriceAgent flagged the price as suspicious without
    considering that generic, unbranded fragrance products are
    commonly priced in this range.

### Root Cause Analysis（根本原因分析）
The initial false positive was caused by a prompt design issue in
PriceAgent. The original prompt lacked guidance on how to handle
product categories that are inherently low-priced. The model
defaulted to treating any low price as suspicious, regardless of
whether the product was a high-value branded item or a generic
low-cost item.

The fix was to add explicit rules distinguishing between branded
and unbranded products, with concrete examples for each case.

---

## 4. Iteration History

The system went through two prompt engineering iterations:

- **v1 (baseline):** PriceAgent prompt used a single example
  (brand-name smartphone) to illustrate suspicious pricing.
  This caused the model to over-generalize: any low price was
  treated as suspicious regardless of product category.
  Result: Precision=0.667, Recall=1.000

- **v2 (final):** PriceAgent prompt revised to include explicit
  rules distinguishing branded vs. unbranded products, with
  examples covering both suspicious and non-suspicious low-price
  cases.
  Result: Precision=1.000, Recall=1.000

---

## 5. Limitations of This Evaluation

1. **Sample size is very small.** Only 5 ads were evaluated.
   Results of 1.000/1.000 are not statistically meaningful at
   this scale and likely do not reflect real-world performance.

2. **No train/validation/test split.** The same dataset was used
   for both prompt development and final evaluation. This means
   the prompt may be overfit to these specific examples and could
   perform worse on unseen data.

3. **Label ambiguity.** At least one sample (Perfume Gift Set)
   was genuinely ambiguous. Even the human annotator was
   uncertain. Such samples introduce noise into the evaluation.

4. **Single evaluation run.** LLM outputs are non-deterministic.
   Running the pipeline once does not account for variance across
   runs.

5. **Limited category coverage.** The dataset does not cover many
   real-world ad categories such as electronics, clothing, food,
   or services.

---

## 6. Improvement Directions

1. **Expand the evaluation dataset** to at least 50-100 samples,
   covering more product categories and more edge cases.

2. **Separate validation and test sets** to avoid overfitting
   the prompt to the evaluation data.

3. **Run multiple evaluations** and report average Precision and
   Recall to account for LLM non-determinism. For example, run each sample 3–5 times and report mean ± std to quantify output variance.

4. **Improve IllegalAgent coverage** — the current dataset does
   not stress-test illegal content detection sufficiently.

5. **Add a confidence signal** — rather than a binary
   suspicious/safe label, have the system output a risk level
   (low/medium/high) to support tiered human review workflows.