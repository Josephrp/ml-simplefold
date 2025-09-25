# Data pipeline (Boltz)

Key locations under `src/simplefold/boltz_data_pipeline/`.

```mermaid
flowchart LR
    FASTA[FASTA/A3M/CSV/YAML] -->|parse| PARSE[parse/*]
    PARSE --> TOK[tokenize/BoltzTokenizer]
    TOK --> FEAT[feature/BoltzFeaturizer]
    FEAT --> CROP[crop/*]
    CROP --> FILTs[filter/static + filter/dynamic]
    FILTs --> OUT[write/{mmcif,pdb}]

    subgraph Inference Helpers
        OUT --> Proc[processor/ProteinDataProcessor]
        Proc --> Utils[utils/{boltz_utils,fasta_utils}]
    end
    %% Clickable code links
    click PARSE "../src/simplefold/boltz_data_pipeline/parse" "Parsers" _blank
    click TOK "../src/simplefold/boltz_data_pipeline/tokenize/boltz_protein.py" "BoltzTokenizer" _blank
    click FEAT "../src/simplefold/boltz_data_pipeline/feature/featurizer.py" "BoltzFeaturizer" _blank
    click CROP "../src/simplefold/boltz_data_pipeline/crop" "Cropping" _blank
    click FILTs "../src/simplefold/boltz_data_pipeline/filter" "Filters" _blank
    click OUT "../src/simplefold/boltz_data_pipeline/write" "Writers" _blank
    click Proc "../src/simplefold/processor/protein_processor.py" "ProteinDataProcessor" _blank
    click Utils "../src/simplefold/utils" "Utils" _blank
```

mmCIF preprocessing for training data is handled by `src/simplefold/process_mmcif.py`.

### Code citations

- Tokenizer: [src/simplefold/boltz_data_pipeline/tokenize/boltz_protein.py](../src/simplefold/boltz_data_pipeline/tokenize/boltz_protein.py)
- Featurizer: [src/simplefold/boltz_data_pipeline/feature/featurizer.py](../src/simplefold/boltz_data_pipeline/feature/featurizer.py)
- Processor: [src/simplefold/processor/protein_processor.py](../src/simplefold/processor/protein_processor.py)
- Writers: [src/simplefold/boltz_data_pipeline/write](../src/simplefold/boltz_data_pipeline/write)
- mmCIF processing script: [src/simplefold/process_mmcif.py](../src/simplefold/process_mmcif.py)


