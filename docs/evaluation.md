# Evaluation

```mermaid
flowchart LR
    PRED[Predicted structures] --> FOLD[analyze_folding.py]
    TGT[Target mmCIF] --> FOLD
    FOLD --> MET1[Folding metrics]

    PRED2[Predicted PDBs] --> TS[analyze_two_state.py]
    TGT2[Two-state targets] --> TS
    TM[TMsore binary] --> TS
    TS --> MET2[Two-state metrics]
    %% Clickable code links
    click FOLD "../src/simplefold/evaluation/analyze_folding.py" "Folding evaluation script" _blank
    click TS "../src/simplefold/evaluation/analyze_two_state.py" "Two-state evaluation script" _blank
```

Use OpenStructure 2.9.1 docker for folding tasks, and compiled TM-score for two-state tasks.

### Code citations

- Folding evaluation: [src/simplefold/evaluation/analyze_folding.py](../src/simplefold/evaluation/analyze_folding.py)
- Two-state evaluation: [src/simplefold/evaluation/analyze_two_state.py](../src/simplefold/evaluation/analyze_two_state.py)


