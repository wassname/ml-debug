# Evidence reading guide

Local source copies behind the [debugging skill](../../SKILL.md) and [folklore quotes](../../README.md). Use this page to choose a source by topic; use [references/](../../references/) for the operational guidance drawn from them.

Files include full articles, selected excerpts, paper conversions, slides, captions, and secondary notes. Check each file's source URL and `Fetch-status` before quoting. A cached source supports what its author observed or argued; its presence here does not mean every recommendation has been tested.
<!-- Drafted by PI/OpenAI. -->

## Start here

- Training a neural network: [Karpathy, *A Recipe for Training Neural Networks*](karpathy_recipe_training_nn_2019.md). Inspect data, establish a baseline, overfit a small batch, then add complexity.
- Debugging RL: [Andy Jones, *Debugging RL, Without the Agonizing Pain*](andyljones_rl_debugging.md). Isolate failures with small environments and agents; investigate anomalies before tuning.
- Choosing experiments: [Google's *Deep Learning Tuning Playbook*](google_tuning_playbook.md). Separate useful questions from tuning details and make expensive runs informative.
- Developing research judgment: [Neel Nanda, *How to Become a Mechanistic Interpretability Researcher*](nanda_how_to_mech_interp.md) and [research-process guide](nanda_research_process_explore_understand_distill.md). Skepticism, exploration, understanding, and communicating evidence.

## General debugging and training

For a procedure, use [PLAYBOOK.md](../../PLAYBOOK.md), [diagnostics](../../references/diagnostics.md), or the [checklist](../../references/checklist.md).

- [Agans, *Debugging: The 9 Indispensable Rules*](agans_debugging_9_rules.md): general software/hardware debugging, instrumentation, isolation, and checking the repair. Selected book material, not the complete book.
- [Goodfellow, Bengio and Courville, ch. 11](goodfellow_ch11_practical_methodology.md): practical methodology; interacting components can compensate for bugs. [Ch. 15](goodfellow_ch15_representation_learning.md) covers representation learning.
- [Stanford CS231n](cs231n_neural_networks_3.md), [CS229 advice](cs229_ml_advice.md), and [Full Stack Deep Learning lecture 7](fsdl_spring2021_lecture7.md): training checks and troubleshooting.
- [Victor Sanh](sanh_simple_considerations_hf_2021.md), [Karpathy's common mistakes](karpathy_common_mistakes_tweet_2018.md), and [Karpathy's diagnostics lecture](karpathy_nn_zero_to_hero_lec4_diagnostics.md): silent implementation errors and inspecting training internals.
- [Slav Ivanov's 37 reasons](slavv_37_reasons_nn.md) and its [Reddit discussion](reddit_37_reasons_nn_6pfsyk.md): candidate causes to investigate, not a diagnosis by checklist.
- [McCandlish et al., large-batch training](mccandlish_2018_large_batch.md): batch-size scaling and gradient noise.

## Data, labels, leakage, and evaluation

For LLM-based evaluation, start with [judge guidance](../../references/llm_judges.md); for controlled comparisons, use [sweeps](../../references/sweeps.md).

- [Andrew Ng, *Machine Learning Yearning*, error-analysis chapters](ng_ml_yearning_error_analysis.md): categorize real errors before deciding what to improve.
- [Vincent Warmerdam, *Bad Labels*](koaning_bad_labels.md): inspect label errors, including validation labels.
- [Michael Lones, *How to avoid machine learning pitfalls*](lones_2021_ml_pitfalls.md) and [Pedro Domingos, *A Few Useful Things to Know about Machine Learning*](domingos_2012_few_useful_things.md): experimental design, overfitting, contamination, and common methodological errors.
- [Evan Miller, *Adding Error Bars to Evals*](miller_2024_error_bars_evals.md): repeat draws, paired comparisons, and sources of evaluation uncertainty. PDF-derived equations need checking against the original.
- [LLM judge biases](llm_judge_biases.md): mixed paper excerpts and practitioner notes on position, verbosity, self-preference, and related biases. Read its provenance warning; it is not one primary source. More recent source discussion is in the [judge literature review](../../references/llm_judge_litreview.md).
- [Gwern, *The Neural Net Tank Legend*](gwern_tank.md): a warning about appealing shortcut-learning stories whose historical evidence is weak.

## Reinforcement learning

Use [rl/SKILL.md](../../rl/SKILL.md) for probe environments, policy/value diagnostics, and reference-implementation checks.

- [Andy Jones](andyljones_rl_debugging.md) and [Joshua Achiam, *Spinning Up as a Deep RL Researcher*](spinningup_researcher.md): why apparently running RL code can still be broken; how to localize faults.
- [Matthew Rahtz, *Lessons Learned Reproducing a Deep RL Paper*](amid_fish_reproducing_deep_rl.md): implementation bugs, reference comparisons, and thinking carefully between costly runs.
- [John Schulman's clean slide transcript](joschu_nuts_and_bolts.md): *Nuts and Bolts of Deep RL Research*, December 2016. The [2017 Bootcamp captions](schulman_nuts_bolts_deeprl_bootcamp_2017_subtitles.md) are a related talk, with auto-caption errors. [Falcon's notes](williamfalcon_deeprl_hacks.md) are a secondary account.
- [Henderson et al., *Deep Reinforcement Learning that Matters*](henderson_2018_deep_rl_matters.md) and [Alex Irpan, *Deep Reinforcement Learning Doesn't Work Yet*](alexirpan_rl_hard.md): seeds, implementation sensitivity, and limits on interpreting failed runs.
- [Huang et al., *The 37 Implementation Details of PPO*](cleanrl_37_ppo_details.md): implementation details linked to reference code.
- Practitioner discussions: [debugging tips](reddit_rl_debugging_tips_9sh77q.md), [practical tips](reddit_rl_practical_tips_7s8px9.md), and [roadblocks](reddit_rl_roadblocks_bzg3l2.md). These are community reports, not controlled studies. Other Reddit files collect talk/resource discussions.

## Transformers, fine-tuning, and steering

Start with [transformer/LLM guidance](../../references/transformers.md), including its activation-steering section. The cache is stronger on training failures than on steering: some steering papers are linked from that reference but are not stored here.

- [Hugging Face, debugging the training pipeline](hf_llm_course_ch8_4_debugging_pipeline.md): walk through data, tokenization, batches, and the training loop.
- [Unsloth troubleshooting](unsloth_troubleshooting_faqs.md), [Axolotl debugging](axolotl_debugging.md), and [Axolotl stability](axolotl_training_stability.md): chat templates, label masks, caches, learning rate, and training diagnostics. Version-dependent practitioner documentation.
- [Karpathy's nanochat experiment log](karpathy_nanochat_experiments.md): actual changes, comparisons, and failures while developing a transformer. A development log, not a controlled benchmark of every choice.
- [Bekman's underflow/overflow debugger](bekman_debug_utils_transformers.md) and [ML Engineering instability notes](bekman_ml_engineering_instabilities.md): numerical failures and the steps preceding a loss spike.
- [Phil Wang's x-transformers README](lucidrains_x_transformers_readme.md): implementation recipes, normalization, and stability techniques.

## Disclosed model-training recipes

The [reports/](reports/) directory contains model-team reports. Use them to recover concrete recipes and compare implementations; final benchmark scores alone do not validate a recipe for a different model or budget.

- [OLMo 3](reports/olmo3_technical_report.md): model stages, data, evaluation, and the released training flow. [OLMo-core README](reports/code/olmo_core_readme.md) describes its implementation project.
- [MAI-Thinking-1](reports/mai_thinking_1_technical_report.md): reasoning-model development, RL, infrastructure, and system-level trade-offs.
- [Hermes 4](reports/hermes4_technical_report.md): data curation, reasoning control, and evaluation. [Atropos README](reports/code/nous_atropos_readme.md) describes the LLM RL framework.
- [DeepSeek-V3](reports/deepseek_v3_technical_report.md): architecture, numerical precision, infrastructure, and the training schedule.
- [Qwen3](reports/qwen3_technical_report.md): pretraining/post-training, thinking modes, data filtering, and on-policy distillation.
- [Llama 3](reports/llama3_herd_technical_report.md) and [OPT-175B](reports/opt175b_technical_report.md): large-run engineering, interruptions, and instability/recovery experience.

The files under `reports/code/` are cached repository READMEs, not vendored training implementations. PDF/HTML conversions can damage equations or tables; check the linked original before copying a formula or number.

## Research practice and engineering judgment

Use [research_taste.md](../../references/research_taste.md) for the source-led guide.

- Nanda: [explore, understand, distill](nanda_research_process_explore_understand_distill.md), [key mindsets](nanda_research_process_key_mindsets.md), [research taste](nanda_research_process_research_taste.md), and [paper writing](nanda_highly_opinionated_ml_paper_writing.md). The [shared draft](nanda_research_process_shared_draft.md) contains expanded material; distinguish it from the published posts.
- [Chris Olah, *Research Taste Exercises*](olah_research_taste_exercises.md) and [Jacob Steinhardt, *Research as a Stochastic Decision Process*](steinhardt_research_stochastic_decision_process.md): developing judgment and choosing research actions.
- [Patrick Kidger, *Just Know Stuff*](kidger_just_know_stuff.md), [Ulisse Mini on programming](ulisse_how_to_get_good_at_programming.md), and [John Wentworth on gears-level models](wentworth_gears_level_models.md): understanding systems rather than accumulating fixes.
- [Sculley et al., *Hidden Technical Debt in Machine Learning Systems*](sculley_2015_hidden_technical_debt.md): entanglement, hidden dependencies, and maintenance costs.
- [Gwern, *Unseeing*](gwern_unseeing.md): why familiarity makes mistakes hard to notice. [Catherine Olsson and 80,000 Hours](olsson_80000hours_ml_engineering_ai_safety.md) covers research-engineering skills for AI safety.

## Time-series forecasting

Use [time-series guidance](../../references/time_series.md) for temporal evaluation and leakage checks.

[fpp3/](fpp3/) contains chapter-level copies of Hyndman and Athanasopoulos's *Forecasting: Principles and Practice*, third edition, plus its preface, appendices, and back matter. Useful entry points:

- [Graphics](fpp3/02-time-series-graphics.md), [decomposition](fpp3/03-time-series-decomposition.md), and [features](fpp3/04-time-series-features.md): inspect the series before modeling.
- [The forecaster's toolbox](fpp3/05-forecasters-toolbox.md): baselines, accuracy measures, and rolling-origin evaluation.
- [Regression](fpp3/07-time-series-regression.md), [exponential smoothing](fpp3/08-exponential-smoothing.md), [ARIMA](fpp3/09-arima-models.md), and [dynamic regression](fpp3/10-dynamic-regression.md): reference methods.
- [Practical issues](fpp3/13-practical-issues.md): missing data and other complications; distinguish retrospective repair from information available at forecast time.
