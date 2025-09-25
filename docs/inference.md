# Inference flow

Core functions live in `src/simplefold/inference.py` and entrypoint is `src/simplefold/cli.py`.

```mermaid
sequenceDiagram
    participant U as User
    participant CLI as simplefold (CLI)
    participant INF as inference.py
    participant FS as FASTA utils
    participant ESM as ESM utils
    participant M as Folding Model
    participant P as Processor/Sampler
    participant W as Writers

    U->>CLI: simplefold --fasta_path ...
    CLI->>INF: predict_structures_from_fastas(args)
    INF->>INF: initialize_folding_model(args)
    INF->>INF: initialize_plddt_module(args)
    INF->>INF: initialize_esm_model(args)
    INF->>INF: initialize_others(args)
    INF->>FS: download_fasta_utilities/cache
    INF->>FS: process_fastas
    FS-->>INF: structures/*.npz, records/*.json
    loop For each structure
        INF->>P: process_one_inference_structure(...)
        INF->>P: sampler.sample(model, flow, noise, batch)
        P-->>INF: out_dict (denoised_coords)
        INF->>P: processor.postprocess(...)
        alt pLDDT enabled
            INF->>M: plddt_latent_module(...)
            M-->>INF: latent
            INF->>M: plddt_out_module(latent)
            M-->>INF: pLDDT scores
        end
        INF->>W: save_structure(..., output_format)
    end
```

Clickable nodes:

```mermaid
%% Mermaid click bindings
click CLI "../src/simplefold/cli.py" "CLI entrypoint" _blank
click INF "../src/simplefold/inference.py" "Inference core" _blank
click FS "../src/simplefold/utils/fasta_utils.py" "FASTA helpers" _blank
click ESM "../src/simplefold/utils/esm_utils.py" "ESM utils" _blank
click P "../src/simplefold/processor/protein_processor.py" "Processor & sampling glue" _blank
click W "../src/simplefold/utils/boltz_utils.py" "Writers (PDB/mmCIF)" _blank
```

### Code citations

- initialize_folding_model/initialize_plddt_module/initialize_esm_model/initialize_others: [src/simplefold/inference.py](../src/simplefold/inference.py)
- process_one_inference_structure: [src/simplefold/utils/datamodule_utils.py](../src/simplefold/utils/datamodule_utils.py)
- ProteinDataProcessor.preprocess_inference/postprocess: [src/simplefold/processor/protein_processor.py](../src/simplefold/processor/protein_processor.py)
- EMSampler (Torch/MLX): [src/simplefold/model/torch/sampler.py](../src/simplefold/model/torch/sampler.py), [src/simplefold/model/mlx/sampler.py](../src/simplefold/model/mlx/sampler.py)
- Flow path (LinearPath): [src/simplefold/model/flow.py](../src/simplefold/model/flow.py)
- Writers (process_structure/save_structure): [src/simplefold/utils/boltz_utils.py](../src/simplefold/utils/boltz_utils.py)

Key modules:

- Tokenization/featurization: `BoltzTokenizer`, `BoltzFeaturizer`
- Flow path: `LinearPath`
- Sampler: `EMSampler` (Torch) or `EMSampler` (MLX)
- ESM: `esm_registry["esm2_3B"]()`, mapped to MLX backend when needed


