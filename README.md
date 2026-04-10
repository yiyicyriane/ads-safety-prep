# Ads Safety Prep

## Overview

A modular ads safety pipeline built in Python. The system reads advertisement
data from a CSV file, applies multi-agent detection logic, and outputs flagged results.

This project evolves from a rule-based pipeline into a multi-agent architecture,
designed to simulate real-world content moderation systems.

## Project Structure

```
ads-safety-prep/
    data/
        ads.csv ← input advertisement data
    src/
        main.py ← pipeline entry point: CLI arguments, logging, orchestration
        loader.py ← load CSV data, validate required columns
        writer.py ← write results to output CSV files
        llm_client.py ← wrapper for LLM API calls
        agents/
            init.py
            price_agent.py ← detects suspicious pricing
            illegal_agent.py ← detects illegal or restricted content
            judge_agent.py ← aggregates results from multiple agents
            safety_agent.py ← optional combined safety logic (legacy / extension)
    tests/
        test_price_agent.py
        test_illegal_agent.py
        test_api.py
    output/
        completed_results.csv ← full analysis results (generated)
        suspicious_results.csv ← flagged ads only (generated)
    README.md
```

## Getting Started

### Prerequisites

- Python 3.10+
- Git

### Installation

```bash
git clone https://github.com/your-username/ads-safety-prep.git
cd ads-safety-prep
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Running the Pipeline

Default input and output paths:

```bash
python3 src/main.py
```

Custom input and output paths:

```bash
python3 src/main.py --input data/ads.csv --output output/
```

View all available options:

```bash
python3 src/main.py --help
```

## Pipeline Design

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

The pipeline follows a modular multi-agent design. Each agent is responsible for a specific dimension of ad safety, enabling better extensibility, testability, and separation of concerns.

## Agent Responsibilities

| Agent        | Input                        | Output                                    | Responsibility                                 |
| ------------ | ---------------------------- | ----------------------------------------- | ---------------------------------------------- |
| PriceAgent   | title, price                 | {"price_suspicious": bool, "reason": str} | Detect whether the price is suspicious         |
| IllegalAgent | title, description           | {"illegal_flag": bool, "reason": str}     | Detect illegal or restricted content           |
| JudgeAgent   | price_result, illegal_result | {"label": str, "reason": str}             | Aggregate results and determine final decision |

## Design Highlights
1. **Modular architecture**: Each agent handles a single responsibility
2. **LLM integration**: Agents can leverage LLMs for flexible reasoning
3. **Structured output validation**: Ensures LLM responses conform to strict JSON schema
4. **Extensibility**: New agents (e.g., ScamAgent, PolicyAgent) can be added easily
5. **Separation of concerns**: Clear distinction between data loading, analysis, and output

## Detection Logic
### Price-based Detection
1. Flag ads with unusually low prices
2. Combine price with brand signals for stronger detection
### Content-based Detection
1. Identify illegal or restricted keywords from ad text
2. Extendable to policy-based moderation rules
### Final Decision
1. Combine signals from multiple agents
2. Produce a unified label and explanation

## Limitations
1. **LLM reliability**: Model outputs may be inconsistent or malformed
2. **No training loop**: The system does not learn from feedback
3. **Limited policy coverage**: Only basic rules and prompts are implemented
4. **Small scale**: Designed for local execution, not distributed systems
5. **No human review loop**: No feedback or moderation pipeline yet

## Future Improvements
1. Add retry + fallback mechanisms for LLM calls
2. Introduce JSON schema validation and auto-repair
3. Implement caching to reduce API cost
4. Add more agents (e.g., ScamAgent, ComplianceAgent)
5. Build a feedback loop for continuous improvement

## Summary
This project demonstrates the transition from a simple rule-based pipeline to a scalable multi-agent system for ads safety detection, combining deterministic logic with LLM-based reasoning.