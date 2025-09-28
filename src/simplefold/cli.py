#
# For licensing see accompanying LICENSE file.
# Copyright (c) 2025 Apple Inc. Licensed under MIT License.
#

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent))
import argparse
from simplefold import __version__
from simplefold.inference import predict_structures_from_fastas


def main():
    parser = argparse.ArgumentParser(
        prog="simplefold",
        description="Folding proteins with SimpleFold."
    )
    parser.add_argument("--simplefold_model", type=str, default="simplefold_100M", help="Name of the model to load.")
    parser.add_argument("--ckpt_dir", type=str, default="artifacts", help="Directory to save the checkpoint.")
    parser.add_argument("--output_dir", type=str, default="artifacts/debug_samples", help="Directory to save the output structure.")
    parser.add_argument("--num_steps", type=int, default=500, help="Number of steps in inference.")
    parser.add_argument("--tau", type=float, default=0.1, help="Diffusion coefficient scaling factor.")
    parser.add_argument("--no_log_timesteps", action="store_true", help="Disable logarithmic timesteps.")
    parser.add_argument("--fasta_path", required=True, type=str, help="Path to the input FASTA file/directory.")
    parser.add_argument("--nsample_per_protein", type=int, default=1, help="Number of samples to generate per protein.")
    parser.add_argument("--plddt", action="store_true", help="Enable pLDDT prediction.")
    parser.add_argument("--output_format", type=str, default="mmcif", choices=["pdb", "mmcif"], help="Output file format.")
    parser.add_argument("--backend", type=str, default='torch', choices=['torch', 'mlx'], help="Backend to run inference either torch or mlx")
    # Polyreactivity prediction flags
    parser.add_argument("--polyreact", action="store_true", help="Enable polyreactivity scoring.")
    parser.add_argument("--polyreact_weights", type=str, default=None, help="Path to polyreactivity model.joblib artifact.")
    parser.add_argument("--polyreact_backend", type=str, default=None, choices=["descriptors", "plm", "concat"], help="Polyreact feature backend override.")
    parser.add_argument("--polyreact_plm_model", type=str, default=None, help="PLM model name for polyreact backend (if applicable).")
    parser.add_argument("--polyreact_cache_dir", type=str, default=None, help="Cache dir for PLM embeddings.")
    parser.add_argument("--polyreact_heavy_only", action="store_true", help="Score only heavy chain (VH) from colon-separated VH:VL.")
    # AbMelt scoring flags (optional; Hydra also supports these via model.abmelt)
    parser.add_argument("--abmelt", action="store_true", help="Enable AbMelt scoring sidecar.")
    parser.add_argument("--abmelt_weights", type=str, default=None, help="Path to AbMelt model artifact (joblib or pkl).")
    parser.add_argument("--abmelt_endpoint", type=str, default="tm", choices=["tm","tmon","tagg"], help="AbMelt endpoint.")
    parser.add_argument("--abmelt_target_direction", type=str, default="maximize", choices=["maximize","minimize"], help="Optimization direction.")
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}"
    )
    args = parser.parse_args()

    print(f"Running protein folding with SimpleFold ...")
    predict_structures_from_fastas(args)
