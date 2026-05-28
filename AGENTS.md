# AGENTS.md

## Scope
- This file applies to `/home/gwh/NeuPAN`.
- Follow the parent `/home/gwh/AGENTS.md` rules for persistent recording and environment changes.

## Local Task Record
- Current reproduction/training log:
  `/home/gwh/文档/Obsidian Vault/03_项目记录/NEUOAB/NeuPAN论文代码复现与训练启动_2026-04-27_17-54_2026-04-27_17-53.md`
- Append substantial clone, setup, training, error, and verification steps to that note with `$HOME/tools/codex-obsidian-log.sh`.

## Environment Rules
- Prefer a dedicated Conda environment for NeuPAN dependency work.
- Keep generated training data, checkpoints, and runtime logs in explicit project subdirectories.
- Do not overwrite upstream examples unless the user asks for a repo-level change.

## Paper Upstream And DashGo Boundary
- NeuPAN paper official repository is `https://github.com/hanruihua/NeuPAN`; this local repository is `/home/gwh/NeuPAN`.
- For DUNE, LON, planner configuration, IR-SIM examples, model loading, or evaluation behavior, treat the official repository implementation as the source of truth.
- The user has requested future NeuPAN work to follow the original repository as closely as possible; the only required adaptation is connecting to the current DashGo robot.
- Keep upstream semantics for planner/model behavior by default. Put DashGo-specific changes in separate configs, adapters, launch files, or scripts for robot geometry, ROS 2 topics, `cmd_vel/odom/scan/tf`, and differential-drive constraints.
