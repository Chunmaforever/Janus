# 🎭 Janus Project

**Janus Project** is an advanced AI-powered patent analysis system designed to perform deep "puzzle matching" of patent claims against competitor portfolios.

It operates in two modes, inspired by the two-faced god Janus:

1. **Forward Face (Attack Mode)**: Detects potential infringement by searching for competitors who use your patented technology (a+b+c) in their newer filings.
2. **Backward Face (Defense Mode)**: Detects invalidity risks by finding prior art that discloses your technology, and suggests claim amendments (corrections) to save the patent.

## Directory Structure

- `src/janus/core/`: The brain. Contains the `PuzzleMatcher`, `ClaimDecomposer`, and `RiskScorer`.
- `src/janus/faces/`: The modes. `forward.py` (Infringement) and `backward.py` (Validity).
- `src/janus/agents/`: The workers. `searcher.py` (Patent Retrieval) and `drafter.py` (Claim Writing).
- `config/`: Configuration files.

## Usage

### 1. Setup

Install requirements (TBD) and configure `config/janus_config.yaml`.

### 2. Forward Mode (Infringement Search)

Find if "Competitor X" is using your technology.

```bash
python main.py --mode forward --competitor "Competitor X"
```

### 3. Backward Mode (Validity & Correction)

Check if your patent is safe from "Competitor Y's" prior art, and get correction suggestions if not.

```bash
python main.py --mode backward --competitor "Competitor Y" --target_claim "A widget comprising a, b, and c."
```

## Core Logic: The Puzzle Matcher

Unlike simple keyword search, Janus breaks down a claim into elements (puzzle pieces) and looks for them across a competitor's entire portfolio. It can identify if a competitor has all the pieces distributed across multiple patents, signaling a high risk of combined infringement or invalidity.
