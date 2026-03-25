# Ads Safety Prep

## Overview

A rule-based ads safety pipeline built in Python. The system reads advertisement
data from a CSV file, applies suspicious detection rules, and outputs flagged results.

Built as part of a structured preparation program for a Google Ads Safety
engineering internship.

## Project Structure

```
ads-safety-prep/
  data/
    ads.csv           ← input advertisement data
  src/
    main.py           ← pipeline entry point: CLI arguments, logging, exception handling
    loader.py         ← load CSV data, validate required columns
    analyzer.py       ← detect suspicious ads using rule-based logic
    writer.py         ← write full results and suspicious ads to output CSV files
  output/
    completed_results.csv   ← full analysis results (generated)
    suspicious_results.csv  ← flagged ads only (generated)
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
loader.py     → reads CSV, validates columns, returns pd.DataFrame
    ↓
analyzer.py   → applies detection rules, adds is_suspicious column, returns pd.DataFrame
    ↓
writer.py     → writes completed_results.csv and suspicious_results.csv to output/
```

Each module has a single responsibility and can be tested independently.

## Detection Rules

| Rule                       | Condition                                              | Flag       |
| -------------------------- | ------------------------------------------------------ | ---------- |
| Low price                  | Price < $20.00                                         | suspicious |
| Luxury keyword + low price | Title contains luxury brand keyword AND price < $50.00 | suspicious |

Luxury brand keywords: `rolex`, `gucci`, `louis vuitton`, `iphone`, `macbook`,
`airpods`, `playstation`

## Limitations

1. **Rule coverage**: Detection is based on price thresholds and a small fixed
   keyword list. Real-world ads require far more complex signals.
2. **No ML-based detection**: The system uses only hard-coded rules. It cannot
   learn from new patterns or adapt to evolving fraud tactics.
3. **English only**: Keyword matching does not support non-English ad titles.
4. **Small scale**: The pipeline reads the entire dataset into memory.
   It is not designed for large-scale data.
5. **No human review loop**: Flagged ads go directly to output with no
   mechanism for human review or feedback.
