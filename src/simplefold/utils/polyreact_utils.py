"""
Utilities to score sequences with the polyreactivity predictor bundled under
`src/hfs-polyreactivity` and to persist results next to generated structures.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, Optional, Tuple


def _ensure_polyreact_on_path() -> None:
    """Append the local polyreact package to sys.path if not importable."""
    try:
        import polyreact  # noqa: F401
        return
    except Exception:
        pass

    this_file = Path(__file__).resolve()
    # repo/src/simplefold/utils/polyreact_utils.py → repo/src
    src_dir = this_file.parents[2]
    polyreact_dir = src_dir / "hfs-polyreactivity"
    if polyreact_dir.exists():
        sys.path.append(str(polyreact_dir))


def _parse_heavy_light(sequence: str, heavy_only: bool = True) -> Tuple[str, str]:
    """Split a colon-separated multi-chain sequence into heavy/light.

    Falls back to treating the entire sequence as heavy when light is absent
    or when heavy_only=True.
    """
    parts = (sequence or "").split(":")
    heavy = parts[0] if parts else ""
    if heavy_only:
        return heavy, ""
    light = parts[1] if len(parts) > 1 else ""
    return heavy, light


def score_polyreact(
    *,
    record_id: str,
    sequence: str,
    weights: str,
    backend: Optional[str] = None,
    plm_model: Optional[str] = None,
    device: Optional[str] = None,
    cache_dir: Optional[str] = None,
    heavy_only: bool = True,
) -> Dict[str, Any]:
    """Compute polyreactivity score for a single sequence using local package.

    Returns a dict with fields: id, score, pred, heavy_len, light_len.
    """
    _ensure_polyreact_on_path()
    from polyreact import api as poly_api  # type: ignore

    heavy, light = _parse_heavy_light(sequence, heavy_only=heavy_only)
    records = [{"id": record_id, "heavy_seq": heavy, "light_seq": light}]
    df = poly_api.predict_batch(
        records,
        backend=backend,
        plm_model=plm_model,
        weights=weights,
        heavy_only=heavy_only,
        device=device,
        cache_dir=cache_dir,
    )
    row = df.iloc[0]
    score_val = float(row["score"])  # type: ignore[arg-type]
    pred_val = int(row["pred"])  # type: ignore[arg-type]
    return {
        "id": record_id,
        "score": score_val,
        "pred": pred_val,
        "heavy_len": len(heavy),
        "light_len": len(light),
    }


def save_polyreact_json(
    *, output_dir: Path, record_id: str, payload: Dict[str, Any]
) -> Path:
    """Write polyreactivity payload to JSON file and return the path."""
    output_dir.mkdir(parents=True, exist_ok=True)
    out_path = output_dir / f"polyreact_{record_id}.json"
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    return out_path


