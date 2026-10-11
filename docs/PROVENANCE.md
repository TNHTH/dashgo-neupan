# Provenance

Date: 2026-10-12

- Upstream repository: https://github.com/hanruihua/NeuPAN
- Upstream commit: `579e7afa239cd7ff61f7f63fbd4aaaecbb136d3b`
- Paper: NeuPAN, IEEE TRO 2025, arXiv:2403.06828. The identifiers are the ones printed in the upstream README badges.
- Canonical branch: `main` at `b844d36978e796f1068cd25916cd62e752de44b3`
- Local remote to keep: `git remote add upstream https://github.com/hanruihua/NeuPAN.git`

The `neupan/` tree OID equals that upstream commit. README, `pyproject.toml`, `requirements.txt`, and `LICENSE` blobs match. No upstream path is missing. Local additions are `AGENTS.md`, `example/dashgo_d1/`, `example/model/dashgo_d1/model_5000.pth`, `example/animation/corridor_diff_ani.gif`, and a `.gitignore` change.

Fidelity: F1. The planner package is unchanged. The DashGo differential-drive files are an example and training wrapper. `test` at `11842f9ac1435a33e45762ce1d4040f2cae16e50` only deletes files and is not the canonical adaptation. Isaac and robot runs were not rerun here: V0.
