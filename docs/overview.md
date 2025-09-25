# SimpleFold: How it works (Overview)

This page gives a high-level view of how data, models, and utilities interact across training and inference.

```mermaid
flowchart TD
    subgraph Inference
        CLI[CLI: simplefold] --> Args[Parse args]
        Args --> IFM[initialize_folding_model]
        Args --> IPL[initialize_plddt_module]
        Args --> IESM[initialize_esm_model]
        Args --> IOth[initialize_others (Tokenizer/Featurizer/Processor/Sampler)]
        Args --> FASTA[process_fastas + cache utilities]
        FASTA --> Strs[structures/*.npz]
        Strs --> Proc[process_one_inference_structure]
        Proc --> Samp[sampler.sample(model, flow, noise, batch)]
        Samp --> Post[processor.postprocess]
        Post --> Save[save_structure -> PDB/mmCIF]
    end

    subgraph Training
        Hydra[Hydra configs] --> Submit[submit_run]
        Submit --> Extras[extras/create_folders]
        Extras --> Train[train(cfg)]
        Train --> Mdl[instantiate model]
        Train --> Data[instantiate datamodule]
        Train --> CB[instantiate callbacks]
        Train --> Loggers[instantiate loggers]
        Train --> Tr[instantiate trainer]
        Tr --> Fit[trainer.fit]
    end

    subgraph Evaluation
        EvalFold[analyze_folding.py] --> MetricsF[folding metrics]
        EvalTS[analyze_two_state.py] --> MetricsTS[two-state metrics]
    end

    Save -. inputs .-> EvalFold
    Save -. inputs .-> EvalTS

    %% Clickable links to source code
    click CLI "../src/simplefold/cli.py" "CLI entrypoint" _blank
    click Args "../src/simplefold/cli.py" "Argument parser" _blank
    click IFM "../src/simplefold/inference.py" "initialize_folding_model" _blank
    click IPL "../src/simplefold/inference.py" "initialize_plddt_module" _blank
    click IESM "../src/simplefold/inference.py" "initialize_esm_model" _blank
    click IOth "../src/simplefold/inference.py" "initialize_others" _blank
    click FASTA "../src/simplefold/utils/fasta_utils.py" "FASTA utilities" _blank
    click Proc "../src/simplefold/utils/datamodule_utils.py" "process_one_inference_structure" _blank
    click Samp "../src/simplefold/model/torch/sampler.py" "Sampler (Torch)" _blank
    click Post "../src/simplefold/processor/protein_processor.py" "ProteinDataProcessor.postprocess" _blank
    click Save "../src/simplefold/utils/boltz_utils.py" "save_structure" _blank

    click Hydra "../configs" "Hydra configs" _blank
    click Submit "../src/simplefold/train.py" "submit_run" _blank
    click Extras "../src/simplefold/utils/utils.py" "extras/create_folders" _blank
    click Train "../src/simplefold/train.py" "train(cfg)" _blank
    click CB "../src/simplefold/utils/instantiators.py" "instantiate_callbacks" _blank
    click Loggers "../src/simplefold/utils/instantiators.py" "instantiate_loggers" _blank
    click Tr "../src/simplefold/utils/instantiators.py" "instantiate_trainer" _blank

    click EvalFold "../src/simplefold/evaluation/analyze_folding.py" "Folding evaluation" _blank
    click EvalTS "../src/simplefold/evaluation/analyze_two_state.py" "Two-state evaluation" _blank
```

### Code citations

- CLI main: [src/simplefold/cli.py](../src/simplefold/cli.py)
- Inference core (initializers): [src/simplefold/inference.py](../src/simplefold/inference.py)
- Inference data prep: [src/simplefold/utils/datamodule_utils.py](../src/simplefold/utils/datamodule_utils.py), [src/simplefold/processor/protein_processor.py](../src/simplefold/processor/protein_processor.py)
- Flow and samplers: [src/simplefold/model/flow.py](../src/simplefold/model/flow.py), [src/simplefold/model/torch/sampler.py](../src/simplefold/model/torch/sampler.py), [src/simplefold/model/mlx/sampler.py](../src/simplefold/model/mlx/sampler.py)
- Writers: [src/simplefold/utils/boltz_utils.py](../src/simplefold/utils/boltz_utils.py)
- Training entrypoints: [src/simplefold/train.py](../src/simplefold/train.py), [src/simplefold/utils/instantiators.py](../src/simplefold/utils/instantiators.py)
- Configs: [configs/](../configs/)

See also:

- Inference details: [inference.md](./inference.md)
- Training details: [training.md](./training.md)
- Data pipeline: [data-pipeline.md](./data-pipeline.md)
- Model backends: [model-backends.md](./model-backends.md)
- Evaluation: [evaluation.md](./evaluation.md)


