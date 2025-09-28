#
# For licensing see accompanying LICENSE file.
# Copyright (c) 2025 Apple Inc. Licensed under MIT License.
#

import sys
import os
import shutil
import argparse
import subprocess
from pathlib import Path


def _ensure_abmelt_on_path() -> Path:
    """Append the local AbMelt repo to sys.path if present; return its root."""
    try:
        import AbMelt  # type: ignore  # noqa: F401
    except Exception:
        pass
    src_dir = Path(__file__).resolve().parents[1]
    abmelt_root = src_dir / "hfs-abmelt" / "AbMelt"
    if abmelt_root.exists():
        if str(abmelt_root) not in sys.path:
            sys.path.append(str(abmelt_root))
    return abmelt_root


def main() -> None:
    _ = _ensure_abmelt_on_path()

    parser = argparse.ArgumentParser(
        prog="simplefold-abmelt-train",
        description=(
            "Train an AbMelt regressor and export a unified artifact under "
            "src/hfs-abmelt/artifacts/model.joblib so SimpleFold inference can consume it."
        ),
    )
    parser.add_argument("--endpoint", type=str, default="tm", choices=["tm", "tmon", "tagg"], help="Thermostability endpoint to model")
    parser.add_argument("--train", type=str, required=False, default=None, help="Path to training CSV (features + target). If omitted, AbMelt defaults are used.")
    parser.add_argument("--save-to", type=str, default="src/hfs-abmelt/artifacts/model.joblib", help="Path to write the unified artifact (joblib)")
    parser.add_argument("--report-to", type=str, default="src/hfs-abmelt/artifacts", help="Directory to copy metrics/plots")
    parser.add_argument("--mode", type=str, default="efs", help="AbMelt selector mode (afs|rfs|efs)")
    parser.add_argument("--scoring", type=str, default="r2", help="Model selection scoring metric")
    parser.add_argument("--cv-splits", type=int, default=5)
    parser.add_argument("--cv-repeats", type=int, default=3)
    parser.add_argument("--bopt-iters", type=int, default=50)
    parser.add_argument("--bopt-points", type=int, default=4)
    args, extra = parser.parse_known_args()

    # Resolve important paths
    repo_root = Path(__file__).resolve().parents[1]
    abmelt_repo = repo_root / "hfs-abmelt" / "AbMelt"
    artifacts_dir = Path(args.report_to)
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    # Build base command to run AbMelt predictors module in its repo
    cmd = [
        sys.executable,
        "-m",
        "train_test_predictors.predictors",
        "-mode",
        args.mode,
        "-scoring",
        args.scoring,
        "-cv_splits",
        str(args.cv_splits),
        "-cv_repeats",
        str(args.cv_repeats),
        "-bopt_iters",
        str(args.bopt_iters),
        "-bopt_points",
        str(args.bopt_points),
    ]

    # If user provides a CSV, pass it directly; otherwise rely on AbMelt repo defaults
    if args.train is not None:
        cmd.extend(["-input", args.train])

    # Run training inside AbMelt repo working directory so outputs are created in expected subfolders
    print(f"[AbMelt] Running training in {abmelt_repo} ...")
    env = os.environ.copy()
    abmelt_cwd = str(abmelt_repo)
    result = subprocess.run(cmd, cwd=abmelt_cwd, env=env)
    if result.returncode != 0:
        raise SystemExit(result.returncode)

    # Locate best estimator and metrics and place them under artifacts/
    models_dir = abmelt_repo / "models"
    best_candidates = sorted(models_dir.glob(f"{args.mode}_best_*.pkl"))
    if not best_candidates:
        # Try endpoint-aware folders if present
        endpoint_dir = abmelt_repo / "models" / args.endpoint
        best_candidates = sorted(endpoint_dir.glob("*.pkl")) if endpoint_dir.exists() else []
    if not best_candidates:
        print("[AbMelt] No trained model found under AbMelt/models. Skipping artifact export.")
        raise SystemExit(1)

    best_model = best_candidates[0]
    save_to = Path(args.save_to)
    save_to.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(best_model, save_to)
    print(f"[AbMelt] Exported model artifact to {save_to}")

    # Copy CV summary if available
    cv_dir = abmelt_repo / "cv"
    cv_best = cv_dir / f"{args.mode}_best_p.csv"
    if cv_best.exists():
        shutil.copy2(cv_best, artifacts_dir / "metrics.csv")
        print(f"[AbMelt] Copied CV metrics to {artifacts_dir / 'metrics.csv'}")

    raise SystemExit(0)


if __name__ == "__main__":
    main()


