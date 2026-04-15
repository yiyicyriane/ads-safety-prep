# Ads Safety Prep

## Overview

A multi-agent ads safety pipeline that classifies shopping 
advertisements as suspicious or safe, using a combination of 
price anomaly detection and LLM-based content analysis.

Built as a learning project simulating real-world content 
moderation systems, with evaluation metrics and design 
documentation included.

---

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

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Language | Python 3.x |
| LLM | Gemini API |
| Data processing | pandas |
| Environment | python-dotenv |

---

## Getting Started

### Prerequisites

- Python 3.10+
- Git
- A Gemini API key

### Installation

```bash
git clone https://github.com/your-username/ads-safety-prep.git
cd ads-safety-prep
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Setup

\```bash
cp .env.example .env
#  Add GEMINI_API_KEY in .env file
\```

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

---

## Documentation

| Document | Description |
|----------|-------------|
| [Design Doc](./design_doc.md) | Architecture, design decisions, and detection logic |
| [Evaluation Report](./evaluation.md) | Evaluation results and error analysis |

---

## Design Highlights
1. **Modular architecture**: Each agent handles a single responsibility
2. **LLM integration**: Agents can leverage LLMs for flexible reasoning
3. **Structured output validation**: Ensures LLM responses conform to strict JSON schema
4. **Extensibility**: New agents (e.g., ScamAgent, PolicyAgent) can be added easily
5. **Separation of concerns**: Clear distinction between data loading, analysis, and output
6. **Evaluation-driven development**: System quality measured with Precision and Recall on a manually labeled dataset

---

## Limitations
- Requires a valid Gemini API key — the system cannot run offline
- Text-only: image content in ads is not analyzed
- Not designed for production or distributed environments
- LLM outputs are non-deterministic; results may vary across runs

---

## Future Improvements
1. Add retry + fallback mechanisms for LLM calls
2. Introduce JSON schema validation and auto-repair
3. Implement caching to reduce API cost
4. Add more agents (e.g., ScamAgent, ComplianceAgent)
5. Build a feedback loop for continuous improvement

---

## Summary
This project demonstrates the transition from a simple rule-based pipeline to a scalable multi-agent system for ads safety detection, combining deterministic logic with LLM-based reasoning.