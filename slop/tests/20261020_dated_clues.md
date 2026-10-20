# Dated clues: behavioral check

Author: Pi/OpenAI. One synthetic case; not evidence of research-performance improvement.

A fresh `pi-quick-oracles` agent read the revised mental-model guidance and produced a model update from fictional runs A–C. The initial belief was that KL scale alone explained stagnation. A showed an 8× gradient-norm imbalance; B learned after halving KL on dataset X; C remained flat at the same reduced KL on dataset Y. Original logs were stipulated to remain unchanged.

Observed output:

> KL scale may contribute to task-loss stagnation, but halving KL is not a reliably sufficient remedy across datasets. The belief that “KL scale alone explains stagnation; halving KL should restore learning” was too strong.

The current-model section retained dated source links for A and B. The pending section contained:

> **2026-10-22, run C:** With the same halved KL on dataset Y, task loss remained flat. The cause is unknown; this failure remains unexplained. [Source](outputs/C/run.md#train)

This case showed belief revision with source retention and an unresolved contradictory clue. The output was more verbose than a short clue list needs to be. It does not test long-loop accumulation or deletion behavior against actual files.

Run: `9e9dc5f1-4d14-4ae5-a72f-3076924f0d72`.
