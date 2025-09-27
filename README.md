
<h1 align="center"><strong>SimpleFold: Folding Proteins is Simpler than You Think</strong></h1>


<div align="center">

This github repository accompanies the research paper, [*SimpleFold: Folding Proteins is Simpler than You Think*](https://arxiv.org/abs/2509.18480) (Arxiv 2025).

*Yuyang Wang, Jiarui Lu, Navdeep Jaitly, Joshua M. Susskind, Miguel Angel Bautista*

[[`Paper`](https://arxiv.org/abs/2509.18480)]  [[`BibTex`](#citation)]

<img src="assets/intro.png" width="750">

</div>


## Model family

- **simplefold_100M**: ~94M params, ~66.5 forward GFLOPs
- **simplefold_360M**: ~360M params, ~189.9 forward GFLOPs
- **simplefold_700M**: ~687M params, ~310.4 forward GFLOPs
- **simplefold_1.1B**: ~1.11B params, ~496.0 forward GFLOPs
- **simplefold_1.6B**: ~1.58B params, ~750.0 forward GFLOPs
- **simplefold_3B**: ~2.86B params, ~1382.4 forward GFLOPs

These names match the `--simplefold_model` argument in the CLI. Larger models generally yield stronger accuracy; smaller models are optimized for speed and memory.

## Introduction

We introduce SimpleFold, the first flow-matching based protein folding model that solely uses general purpose transformer layers. SimpleFold does not rely on expensive modules like triangle attention or pair representation biases, and is trained via a generative flow-matching objective. We scale SimpleFold to 3B parameters and train it on more than 8.6M distilled protein structures together with experimental PDB data. To the best of our knowledge, SimpleFold is the largest scale folding model ever developed. On standard folding benchmarks, SimpleFold-3B model achieves competitive performance compared to state-of-the-art baselines. Due to its generative training objective, SimpleFold also demonstrates strong performance in ensemble prediction. SimpleFold challenges the reliance on complex domain-specific architectures designs in folding, highlighting an alternative yet important avenue of progress in protein structure prediction.

</div>


## Installation

To install `simplefold` package from github repository, run
```
git clone https://github.com/apple/ml-simplefold.git
cd ml-simplefold
conda create -n simplefold python=3.10
python -m pip install -U pip build; pip install -e .
```
If you want to use MLX backend on Apple silicon: 
```
pip install mlx==0.28.0
pip install git+https://github.com/facebookresearch/esm.git
```

## Example 

We provide a jupyter notebook [`sample.ipynb`](sample.ipynb) to predict protein structures from example protein sequences. 

## How it works


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

## Inference

Once you have `simplefold` package installed, you can predict the protein structure from target fasta file(s) via the following command line. We provide support for both [PyTorch](https://pytorch.org/) and [MLX](https://mlx-framework.org/) (recommended for Apple hardware) backends in inference. 
```
simplefold \
    --simplefold_model simplefold_100M \  # specify folding model in simplefold_100M/360M/700M/1.1B/1.6B/3B
    --num_steps 500 --tau 0.01 \        # specify inference setting
    --nsample_per_protein 1 \           # number of generated conformers per target
    --plddt \                           # output pLDDT
    --polyreact \                       # enable polyreact scoring (VH:VL aware)
    --polyreact_weights src/hfs-polyreactivity/artifacts/model.joblib \
    --polyreact_backend plm \
    --polyreact_plm_model facebook/esm1v_t33_650M_UR90S_1 \
    --polyreact_heavy_only \
Polyreact training (artifacts aligned with inference):

```
simplefold-polyreact-train \
  --config src/hfs-polyreactivity/configs/default.yaml \
  --train src/hfs-polyreactivity/data/processed/boughter_counts.csv \
  --eval src/hfs-polyreactivity/data/processed/jain.csv \
         src/hfs-polyreactivity/data/processed/shehata_curated.csv \
         src/hfs-polyreactivity/data/processed/harvey.csv \
  --save-to src/hfs-polyreactivity/artifacts/model.joblib \
  --report-to src/hfs-polyreactivity/artifacts \
  --backend plm --plm-model facebook/esm1v_t33_650M_UR90S_1 --heavy-only
```
    --fasta_path [FASTA_PATH] \         # path to the target fasta directory or file
    --output_dir [OUTPUT_DIR] \         # path to the output directory
    --backend [mlx, torch]              # choose from MLX and PyTorch for inference backend 
```

## Evaluation

We provide predicted structures from SimpleFold of different model sizes:
```
https://ml-site.cdn-apple.com/models/simplefold/cameo22_predictions.zip # predicted structures of CAMEO22
https://ml-site.cdn-apple.com/models/simplefold/casp14_predictions.zip  # predicted structures of CASP14
https://ml-site.cdn-apple.com/models/simplefold/apo_predictions.zip     # predicted structures of Apo
https://ml-site.cdn-apple.com/models/simplefold/codnas_predictions.zip  # predicted structures of Fold-switch (CoDNaS)
```
We use the docker image of [openstructure](https://git.scicore.unibas.ch/schwede/openstructure/) 2.9.1 to evaluate generated structures for folding tasks (i.e., CASP14/CAMEO22). Once having the docker image enabled, you can run evaluation via:
```
python src/simplefold/evaluation/analyze_folding.py \
    --data_dir [PATH_TO_TARGET_MMCIF] \
    --sample_dir [PATH_TO_PREDICTED_MMCIF] \
    --out_dir [PATH_TO_OUTPUT] \
    --max-workers [NUMBER_OF_WORKERS]
```
To evaluate results of two-state prediction (i.e., Apo/CoDNaS), one need to compile the [TMsore](https://zhanggroup.org/TM-score/TMscore.cpp) and then run evaluation via:
```
python src/simplefold/evaluation/analyze_two_state.py \ 
    --data_dir [PATH_TO_TARGET_DATA_DIRECTORY] \
    --sample_dir [PATH_TO_PREDICTED_PDB] \
    --tm_bin [PATH_TO_TMscore_BINARY] \
    --task apo \ # choose from apo and codnas
    --nsample 5
```

## Train

You can also train or tune SimpleFold on your end. Instructions below include details for SimpleFold training. 

### Data preparation

#### Training targets

SimpleFold training uses a mixture of experimental PDB structures and distilled structure predictions. We follow the cutoff and filtering described in the paper:

- **PDB (experimental)**: ~160K structures with PDB cutoff date of **May 1, 2020**.
- **AFDB SwissProt (distilled)**: ~270K filtered structures with average pLDDT > 85 and pLDDT std < 15.
- **AFESM representatives (distilled)**: ~1.9M cluster representative structures filtered at pLDDT > 0.8.
- Total for models up to 1.6B: ~2M structures (PDB + SwissProt + AFESM representatives).
- **AFESM-E (extended) for 3B**: up to 10 members per cluster with average pLDDT > 80, totaling ~8.6M distilled structures (used together with PDB + SwissProt for the 3B model).

Notes:
- During pre-training we cap sequence length at 256; during finetuning we allow up to 512 residues.
- You can swap in your own datasets; see configs under `configs/data/` and the mmCIF processing script below.

Target lists used in our training can be found:
```
https://ml-site.cdn-apple.com/models/simplefold/swissprot_list.csv # list of filted SwissProt (~270K targets)
https://ml-site.cdn-apple.com/models/simplefold/afesm_list.csv # list of filted AFESM targets (~1.9M targets)
https://ml-site.cdn-apple.com/models/simplefold/afesme_dict.json # list of filted extended AFESM (AFESM-E) (~8.6M targets)
```
In `afesme_dict.json`, the data is stored in the following structure:
```
{
    cluster 1 ID: {"members": [protein 1 ID, protein 2 ID, ...]},
    cluster 2 ID: {"members": [protein 1 ID, protein 2 ID, ...]},
    ...
}
```

Of course, one can use own customized datasets to train or tune SimpleFold models. Instructions below list how to process the dataset for SimpleFold training. 

#### Process mmcif structures

To process downloaded mmcif files, you need [Redis](https://redis.io/docs/latest/operate/oss_and_stack/install/archive/install-redis/) installed and launch the Redis server:
```
wget https://boltz1.s3.us-east-2.amazonaws.com/ccd.rdb
redis-server --dbfilename ccd.rdb --port 7777
```
You can then process mmcif files to input format for SimpleFold:
```
python src/simplefold/process_mmcif.py \
    --data_dir [MMCIF_DIR]   # directory of mmcif files
    --out_dir [OUTPUT_DIR]   # directory of processed targets
    --use-assembly
```

### Training

The configuration of model is based on [`Hydra`](https://hydra.cc/docs/intro/). An example training configuration can be found in `configs/experiment/train`. To change dataset and model settings, one can refer to config files in `configs/data` and `configs/model`. To initiate SimpleFold training:
```
python train experiment=train
```
To train SimpleFold with FSDP strategy:
```
python train_fsdp.py experiment=train_fsdp
```

### LDDT loss and pLDDT confidence module

- During folding model training, we add an LDDT loss in addition to the flow-matching objective. In pre-training we set `α(t) = 1` (LDDT active across all timesteps). In finetuning we increase its weight near clean data with `α(t) = 1 + 8·ReLU(t - 0.5)`.
- After the folding model is fully trained (pre-train + finetune), we train a separate pLDDT confidence module with the folding model frozen. This module has 4 Transformer layers (no adaptive layers) and predicts per-residue pLDDT (0–100) by classifying into 50 bins with cross-entropy. During this stage, structures are generated on the fly (200 steps, `τ = 0.3`), fed back at `t = 1` to extract the final residue tokens used by the pLDDT head.
- At inference, enable pLDDT output with the CLI flag `--plddt`.

## Citation
If you found this code useful, please cite the following paper:
```
@article{simplefold,
  title={SimpleFold: Folding Proteins is Simpler than You Think},
  author={Wang, Yuyang and Lu, Jiarui and Jaitly, Navdeep and Susskind, Josh and Bautista, Miguel Angel},
  journal={arXiv preprint arXiv:2509.18480},
  year={2025}
}
```

## Acknowledgements
Our codebase is built using multiple opensource contributions, please see [ACKNOWLEDGEMENTS](ACKNOWLEDGEMENTS) for more details. 

## License
Please check out the repository [LICENSE](LICENSE) before using the provided code and
[LICENSE_MODEL](LICENSE_MODEL) for the released models.
