# 🎭 Janus Project

**Janus Project** is an advanced AI-powered patent analysis system designed to perform deep "puzzle matching" of patent claims against competitor portfolios.

It operates in two modes, inspired by the two-faced god Janus:

1. **Forward Face (Attack Mode)**: Detects potential infringement by searching for competitors who use your patented technology (a+b+c) in their newer filings.
2. **Backward Face (Defense Mode)**: Detects invalidity risks by finding prior art that discloses your technology, and suggests claim amendments (corrections) to save the patent.

## Directory Structure

- `src/janus/core/`: The brain. Contains `PuzzleMatcher`, `ClaimDecomposer`, `RiskScorer`, and `AIIntelligence`.
- `src/janus/faces/`: The modes. `forward.py` (Infringement) and `backward.py` (Validity).
- `src/janus/agents/`: The workers. `searcher.py` (Global Retrieval) and `drafter.py` (Claim Writing).
- `src/janus/reporters/`: The storytellers. `report_generator.py` and premium HTML templates.

## ✨ Key Features

- **Semantic Puzzle Matcher**: TF-IDF based matching of claim elements across competitor portfolios.
- **Global Search Engine**: Direct integration with PatentsView (US) and EPO OPS (90+ countries including KR, JP).
- **AI Expert Reasoning**: Internal (No-API) reasoning agent that provides professional attorney-like opinions and strategies.
- **Premium Dashboard**: Glassmorphism-styled interactive HTML reports for visual risk assessment.

## Usage

### 1. Setup

Install requirements and configure `config/janus_config.yaml`.

```bash
export JANUS_API_KEY="your_api_key_optional"
```

### 2. Run Analysis

```bash
python main.py --mode forward --assignee "CompetitorName" --claim "target_claim_text"
```

## Verification

All core components are verified via:

- `tests/test_global_search.py`
- `tests/test_ai_intelligence.py`
- `tests/test_dashboard.py`

---
*Powered by Janus AI - See Both Sides of the Patent.*
