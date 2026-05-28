#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

import numpy as np
import yaml


SCRIPT_DIR = Path(__file__).resolve().parent
NEUPAN_ROOT = SCRIPT_DIR.parents[1]
DEFAULT_ENV = SCRIPT_DIR / "env_static.yaml"
DEFAULT_PLANNER = SCRIPT_DIR / "planner_dashgo_d1.yaml"


def _dist(a, b) -> float:
    return float(np.linalg.norm(np.asarray(a, dtype=float).reshape(-1)[0:2] - np.asarray(b, dtype=float).reshape(-1)[0:2]))


def run_episode(env_file: Path, planner_file: Path, max_steps: int) -> dict:
    if str(NEUPAN_ROOT) not in sys.path:
        sys.path.insert(0, str(NEUPAN_ROOT))
    import irsim  # pylint: disable=import-outside-toplevel
    from neupan import neupan  # pylint: disable=import-outside-toplevel

    env = irsim.make(str(env_file), display=False)
    planner = neupan.init_from_yaml(str(planner_file))
    start = np.asarray(env.get_robot_state()).reshape(-1)
    goal = np.asarray(getattr(env.robot, "goal", [2.0, 0.0, 0.0])).reshape(-1) if hasattr(env, "robot") else np.array([2.0, 0.0, 0.0])
    path_length = 0.0
    last = start.copy()
    termination = "time_out"
    min_distance = math.inf
    step = -1

    for step in range(max_steps):
        state = env.get_robot_state()
        scan = env.get_lidar_scan()
        points = planner.scan_to_point(state, scan)
        action, info = planner.forward(state, points)
        env.step(action)
        current = np.asarray(env.get_robot_state()).reshape(-1)
        path_length += _dist(current, last)
        last = current.copy()
        min_distance = min(min_distance, float(getattr(planner, "min_distance", math.inf)))
        if info.get("arrive"):
            termination = "reach_goal"
            break
        if info.get("stop"):
            termination = "safety_stop"
            break
        if env.done():
            termination = "env_done"
            break
    env.end()

    end_distance = _dist(last, goal)
    start_distance = max(_dist(start, goal), 1.0e-6)
    progress = max(start_distance - end_distance, 0.0)
    return {
        "termination_reason": termination,
        "steps": step + 1,
        "elapsed_time": (step + 1) * 0.1,
        "start_distance": start_distance,
        "end_distance": end_distance,
        "path_length": path_length,
        "path_efficiency": progress / max(path_length, 1.0e-6),
        "net_progress_ratio": progress / start_distance,
        "min_distance": min_distance if math.isfinite(min_distance) else None,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run a no-GUI IR-SIM shadow evaluation for NeuPAN DashGo D1.")
    parser.add_argument("--env", type=Path, default=DEFAULT_ENV)
    parser.add_argument("--planner", type=Path, default=DEFAULT_PLANNER)
    parser.add_argument("--max-steps", type=int, default=300)
    parser.add_argument("--json-out", type=Path, required=True)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if args.dry_run:
        env_cfg = yaml.safe_load(args.env.read_text(encoding="utf-8"))
        planner_cfg = yaml.safe_load(args.planner.read_text(encoding="utf-8"))
        payload = {
            "status": "dry_run_ok",
            "env": str(args.env.resolve()),
            "planner": str(args.planner.resolve()),
            "robot_shape": env_cfg.get("robot", [{}])[0].get("shape"),
            "dune_checkpoint": planner_cfg.get("pan", {}).get("dune_checkpoint"),
        }
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0

    scene = run_episode(args.env.resolve(), args.planner.resolve(), args.max_steps)
    success = scene["termination_reason"] == "reach_goal"
    collision = scene["termination_reason"] == "env_done"
    timeout = scene["termination_reason"] == "time_out"
    metrics = {
        "success_rate": 1.0 if success else 0.0,
        "collision_rate": 1.0 if collision else 0.0,
        "timeout_rate": 1.0 if timeout else 0.0,
        "time_to_goal": scene["elapsed_time"] if success else 0.0,
        "path_efficiency": scene["path_efficiency"],
        "progress_stall_rate": 1.0 if scene["net_progress_ratio"] < 0.2 else 0.0,
        "total_episodes": 1,
        "completed_episodes": 1,
    }
    payload = {
        "status": "completed",
        "environment": "IR-SIM DashGo D1 geometry",
        "request": {
            "env": str(args.env.resolve()),
            "planner": str(args.planner.resolve()),
            "max_steps": args.max_steps,
        },
        "metrics": metrics,
        "scenes": [scene],
    }
    args.json_out.parent.mkdir(parents=True, exist_ok=True)
    args.json_out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
