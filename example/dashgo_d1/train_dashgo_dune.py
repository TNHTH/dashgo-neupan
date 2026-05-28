#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

import yaml


SCRIPT_DIR = Path(__file__).resolve().parent
NEUPAN_ROOT = SCRIPT_DIR.parents[1]
DEFAULT_CONFIG = SCRIPT_DIR / "dune_train_dashgo_d1.yaml"


def main() -> int:
    parser = argparse.ArgumentParser(description="Train NeuPAN DUNE for DashGo D1 geometry.")
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--model-name", default="dashgo_d1")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    config_path = args.config.resolve()
    if args.dry_run:
        payload = yaml.safe_load(config_path.read_text(encoding="utf-8"))
        print(
            json.dumps(
                {
                    "status": "dry_run_ok",
                    "config": str(config_path),
                    "robot": payload.get("robot", {}),
                    "train": payload.get("train", {}),
                    "expected_model_dir": str(NEUPAN_ROOT / "example" / "model" / args.model_name),
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0

    if str(NEUPAN_ROOT) not in sys.path:
        sys.path.insert(0, str(NEUPAN_ROOT))
    os.chdir(str(NEUPAN_ROOT))
    from neupan import neupan  # pylint: disable=import-outside-toplevel

    planner = neupan.init_from_yaml(str(config_path))
    planner.robot.name = args.model_name
    if planner.dune_train_kwargs is not None:
        planner.dune_train_kwargs["model_name"] = args.model_name
    planner.train_dune()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
