# **Design Doc: Mini Shopping Ads Safety System**

**Author:** Yiyi Wang
**Date:** 04/13/2026
**Status:** Draft

---

## **1. Overview**

This system simulates a simplified Google Ads Safety pipeline. It adopts a multi-agent architecture to classify shopping ads as either *suspicious* or *safe*, based on price anomalies and textual content.

In addition, a LoRA fine-tuning experiment was conducted to evaluate whether task-specific fine-tuning can improve classification performance compared to prompt-only baselines.

---

## **2. Problem Statement**

Ads safety is a critical problem for online platforms for two main reasons:

* **Regulatory compliance:** Platforms must prevent misleading, illegal, or restricted advertisements to comply with laws and policies.
* **User trust and experience:** Low-quality or fraudulent ads reduce platform credibility and can harm users.

This system focuses on a specific subproblem:
**determining whether a shopping ad is suspicious based on its price and textual description.**

Specifically, the system aims to detect:

* Unreasonable or anomalous pricing (e.g., luxury goods sold at extremely low prices)
* Illegal or restricted products
* Exaggerated or misleading descriptions

---

## **3. Goals / Non-Goals**

### **Goals**

* Detect whether the advertised product price is reasonable
* Identify illegal or suspicious products based on text
* Improve classification accuracy through fine-tuning

### **Non-Goals**

* Detect suspicious content in images (no vision model is used)
* Provide real-time classification at production scale

---

## **4. Design Decisions**

### **Decision 1: Why use a multi-agent system instead of a single agent?**

* **Option A:** A single large agent handles all classification logic
* **Option B:** Multiple specialized agents + a JudgeAgent for aggregation

We chose **Option B** for the following reasons:

* Better **separation of concerns**
* Easier **debugging and error attribution**
* Improved **modularity and extensibility**

**Trade-off:**

* Higher cost due to multiple API calls per ad

---

### **Decision 2: Why is Recall prioritized over Precision?**

In an ads safety system:

* A **false negative** (missing a suspicious ad) can directly harm users and damage platform trust
* A **false positive** (flagging a safe ad) is less severe and can be corrected via manual review

Therefore, we prioritize **high Recall**, even at the cost of lower Precision.

---

### **Decision 3: Why use Gemini API instead of a local model?**

Gemini API was selected for the following reasons:

* No need for local GPU infrastructure
* Strong zero-shot reasoning capabilities
* Reduced need for large labeled datasets in early-stage prototyping

For a project of this scale, API cost is acceptable.

**Future direction:**
In production, this would likely be replaced with a **fine-tuned lightweight model** (e.g., BERT-based classifier) to reduce cost and latency.

---

## **5. System Architecture**

### **5.1 Pipeline Overview**

```
Input CSV
    ↓
loader.py       → reads CSV, validates columns, returns pd.DataFrame
    ↓
PriceAgent      → detects price anomalies based on title and price
IllegalAgent    → detects illegal or restricted content from title and description
    ↓
JudgeAgent      → aggregates agent outputs and determines final label
    ↓
writer.py       → writes results to output CSV files
```

The pipeline follows a modular multi-agent design. Each agent is responsible for a specific dimension of ad safety, enabling better extensibility, testability, and maintainability.

---

### **5.2 Agent Responsibilities**

| Agent        | Input                        | Output                                    | Responsibility                                 |
| ------------ | ---------------------------- | ----------------------------------------- | ---------------------------------------------- |
| PriceAgent   | title, price                 | {"price_suspicious": bool, "reason": str} | Detect whether the price is suspicious         |
| IllegalAgent | title, description           | {"illegal_flag": bool, "reason": str}     | Detect illegal or restricted content           |
| JudgeAgent   | price_result, illegal_result | {"label": str, "reason": str}             | Aggregate results and determine final decision |

---
### **5.3 Data Flow**

| Stage | Data Format |
|-------|-------------|
| Input | CSV file with columns: id, title, price, description |
| After Loader | pd.DataFrame, validated and cleaned |
| After PriceAgent | Dict: {"price_suspicious": bool, "reason": str} |
| After IllegalAgent | Dict: {"illegal_flag": bool, "reason": str} |
| After JudgeAgent | Dict: {"label": "suspicious"/"safe", "reason": str} |
| Output | CSV file with original columns + label + reason |
---

## **6. Detection Logic**
### Price-based Detection
1. Flag ads with unusually low prices
2. Combine price with brand signals for stronger detection
### Content-based Detection
1. Identify illegal or restricted keywords from ad text
2. Extendable to policy-based moderation rules
### Final Decision
1. Combine signals from multiple agents
2. Produce a unified label and explanation

---

## **7. Evaluation Plan**

### **Metrics**

* **Precision:** Of all ads flagged as suspicious, what fraction are truly suspicious?
* **Recall:** Of all truly suspicious ads, what fraction did the system successfully detect?

---

### **Why Recall is prioritized**

In ads safety systems, missing harmful content is significantly more costly than over-flagging safe content. Therefore, Recall is the primary optimization target.

---

### **Evaluation approach**
We will manually label a dataset of N ads as ground truth, then compare system output against ground truth to compute precision and recall.

---

## **8. Limitations & Risks**

1. **LLM reliability:** Outputs may be inconsistent or not strictly follow the expected JSON format
2. **No learning loop:** The system does not improve from feedback
3. **Limited policy coverage:** Only basic rules and prompts are implemented
4. **Small-scale design:** Not suitable for distributed or production environments
5. **No human-in-the-loop:** No moderation or review pipeline is implemented

---

## **9. Future Work**

To better align with industry practices, the system can be extended as follows:

* Introduce a **rule-based filtering layer** (e.g., regex patterns, keyword blacklists) as a first-stage filter
* Fine-tune **internal classification models** (e.g., BERT-based models) for each agent using domain-specific data
* Use these fine-tuned models as the primary classifiers for improved efficiency
* Route uncertain cases to **LLMs or human reviewers** for final decision-making

This hybrid approach balances **efficiency, scalability, and accuracy**, and is commonly used in production-level ads safety systems.


