# NeuPAN DashGo D1 Example

created: 2026-04-30

This directory is the formal DashGo D1 adapter layer for the upstream NeuPAN repository.
It does not modify `/home/gwh/NeuPAN/neupan/**`.

## Files

- `dune_train_dashgo_d1.yaml`: DashGo D1 geometry and DUNE training config.
- `planner_dashgo_d1.yaml`: DashGo D1 planner config that points to `example/model/dashgo_d1/model_5000.pth`.
- `env_static.yaml`: no-GUI IR-SIM shadow scene with DashGo-size robot and static obstacles.
- `train_dashgo_dune.py`: wrapper around upstream `neupan.init_from_yaml(...).train_dune()`.
- `eval_dashgo_irsim.py`: no-GUI IR-SIM shadow evaluation using `neupan.forward(state, points)`.
- `../model/dashgo_d1/model_5000.pth`: DUNE checkpoint copied from the 2026-04-30 DashGo D1 training run for local demo use.

## Commands

```bash
cd /home/gwh/NeuPAN
.venv/bin/python example/dashgo_d1/train_dashgo_dune.py --dry-run
.venv/bin/python example/dashgo_d1/eval_dashgo_irsim.py --dry-run --json-out /tmp/neupan_dashgo_eval_dry_run.json
.venv/bin/python example/dashgo_d1/eval_dashgo_irsim.py --json-out /tmp/neupan_dashgo_eval.json
```

Long DUNE training and behavior evaluation are not started automatically by Codex.
