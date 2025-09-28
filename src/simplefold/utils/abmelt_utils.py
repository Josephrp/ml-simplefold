"""
Utilities to score structures/sequences with the AbMelt regressors bundled under
`src/hfs-abmelt`. Outputs align with SimpleFold sidecar JSON conventions.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, Optional

import joblib


def _ensure_abmelt_on_path() -> None:
    """Append the local AbMelt repo to sys.path if not importable."""
    try:
        import train_test_predictors  # noqa: F401
        return
    except Exception:
        pass

    this_file = Path(__file__).resolve()
    # repo/src/simplefold/utils/abmelt_utils.py → repo/src/hfs-abmelt/AbMelt
    src_dir = this_file.parents[2]
    abmelt_dir = src_dir / "hfs-abmelt" / "AbMelt"
    if abmelt_dir.exists():
        sys.path.append(str(abmelt_dir))


def score_abmelt(
    *,
    record_id: str,
    features_row: Any = None,
    weights: str = "src/hfs-abmelt/artifacts/model.joblib",
    endpoint: str = "tm",
    target_direction: str = "maximize",
) -> Dict[str, Any]:
    """Score a pre-computed feature row with an AbMelt regressor.

    Note: AbMelt models are trained on MD-derived descriptors; in SimpleFold we
    provide a hook to pass a surrogate feature row. For now, this function
    simply loads the joblib regressor and calls `.predict` on `features_row`.
    """
    _ensure_abmelt_on_path()

    model = joblib.load(weights)
    # Expect features_row to be a 2D array-like shape (1, n_features)
    try:
        import numpy as np
        X = np.asarray(features_row).reshape(1, -1)
    except Exception:
        X = [features_row]
    y_pred = float(model.predict(X)[0])

    return {
        "id": record_id,
        "endpoint": endpoint,
        "score": y_pred,
        "target_direction": target_direction,
    }


def save_abmelt_json(*, output_dir: Path, record_id: str, payload: Dict[str, Any]) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    out_path = output_dir / f"abmelt_{record_id}.json"
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    return out_path


