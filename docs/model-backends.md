# Model backends (Torch vs MLX)

```mermaid
flowchart TB
    CLI[--backend flag] -->|torch| T[Torch path]
    CLI -->|mlx| M[MLX path]

    subgraph Torch path
        TA[configs/model/architecture/*.yaml] --> HY[Hydra instantiate]
        HY --> TM[src/simplefold/model/torch/*]
        TM --> RUN[Model forward/sampler]
    end

    subgraph MLX path
        MA[Load YAML as text] --> REPL[replace 'torch' -> 'mlx']
        REPL --> HY2[Hydra instantiate]
        HY2 --> MM[src/simplefold/model/mlx/*]
        MM --> RUN2[Model forward/sampler]
    end

    ESM[ESM2 (Torch)] --> MAP[map_torch_to_mlx]
    MAP --> MM
    %% Clickable code links
    click T "../src/simplefold/model/torch" "Torch model code" _blank
    click M "../src/simplefold/model/mlx" "MLX model code" _blank
    click TA "../configs/model/architecture" "Architectures" _blank
    click HY "../src/simplefold/inference.py" "Hydra instantiation in inference" _blank
    click HY2 "../src/simplefold/inference.py" "Hydra instantiation in inference (MLX)" _blank
    click MAP "../src/simplefold/utils/mlx_utils.py" "Mapping utilities" _blank
```

ESM weights are loaded in Torch, then converted to MLX arrays when `--backend mlx` is used.

### Code citations

- Torch models: [src/simplefold/model/torch](../src/simplefold/model/torch)
- MLX models: [src/simplefold/model/mlx](../src/simplefold/model/mlx)
- Architecture configs: [configs/model/architecture](../configs/model/architecture)
- Inference backend selection and instantiation: [src/simplefold/inference.py](../src/simplefold/inference.py)

