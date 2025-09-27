#
# For licensing see accompanying LICENSE file.
# Copyright (c) 2025 Apple Inc. Licensed under MIT License.
#

import sys
from pathlib import Path


def _ensure_polyreact_on_path() -> None:
    try:
        import polyreact  # noqa: F401
        return
    except Exception:
        pass
    # repo/src/simplefold/cli_polyreact.py → repo/src
    src_dir = Path(__file__).resolve().parents[1]
    polyreact_dir = src_dir / "hfs-polyreactivity"
    if polyreact_dir.exists():
        sys.path.append(str(polyreact_dir))


def main() -> None:
    _ensure_polyreact_on_path()
    from polyreact import train as poly_train  # type: ignore

    # Forward CLI args, but inject defaults so outputs match inference expectations
    args = list(sys.argv[1:])

    # If not provided, set defaults to src/hfs-polyreactivity/artifacts/
    if "--save-to" not in args:
        args.extend(["--save-to", "src/hfs-polyreactivity/artifacts/model.joblib"])
    if "--report-to" not in args:
        args.extend(["--report-to", "src/hfs-polyreactivity/artifacts"])

    # Delegate to upstream training entrypoint
    code = poly_train.main(args)
    # poly_train.main returns int; exit code accordingly
    raise SystemExit(code)


if __name__ == "__main__":
    main()


