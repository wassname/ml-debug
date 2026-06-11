Source: https://github.com/stas00/ml-engineering — training/instabilities/README.md, training/instabilities/training-loss-patterns.md, debug/README.md (master branch)
Title: "Machine Learning Engineering Open Book" — Stas Bekman (BLOOM-176B / IDEFICS-80B training lead at HF, ex-PyTorch)
Fetched-via: curl of raw markdown from github, 2026-06-11
Fetch-status: verbatim excerpts

# ML Engineering Open Book — instabilities and loss patterns (excerpts)

From "Understanding Training Loss Patterns":

> Training loss plot is similar to the heart beat pattern - there is the good, the bad and you-should-worry one. After studying many training loss trajectories one develops an intuition to explain various loss behaviors during one's training and how to act on those.

> I warn you that the "Understanding" in the title of this section is overloaded since very often we don't really understand why certain types of spikes happen. Here "understanding" refers to recognizing various patterns. We then usually have techniques to overcome the bad patterns and bring the training successfully to the finish line.

> Thus you will find here a gallery of training loss patterns sometimes with real explanations, but more often than not educated guesses to what might be happening.

The pre-BLOOM 104B failure story ("A very failed training"):

> Prior to starting BLOOM-176B training we did multiple experiments with the 104B model. We failed to figure out how to not diverge very early on. [...] As you can see many attempts were made, many techniques were applied (see chronicles). We think the 2 main obstacles were using fp16 and data that had a lot of garbage in it. For BLOOM-176B we switched to bf16, used much cleaner data and also added an embedding layer-norm and that made all the difference.

On loss spikes ("Main types of loss spikes"):

> In general there are 3 types of loss spikes: 1. Fast recovering spikes 2. Slow recovering spikes 3. Not fully recovering spikes
>
> The spikes usually happen because of a bad data pocket, either due to badly shuffled data or because it hasn't been cleaned from some garbage scraped from the websites.

From "Avoiding, Recovering From and Understanding Instabilities" — the init-std story:

> Correctly initializing the initial distribution of the tensors can have a tremendous impact on training's stability. The `std` value isn't fixed and depends on the hidden dimension size.
>
> This proved to be a very crucial setting in our pre-BLOOM 104B experiments and we couldn't break past the first few thousands iterations until we figured out that the 0.02 default `--init-method-std` in Megatron-LM was a way too big for our model.

(They settled on the 530B paper's `sqrt(1/(NHIDDEN*3))`: "for NHIDDEN=14336 the math was sqrt(1/(14336*3)) = 0.00482 and that's what we used. It surely wasn't the only reason why we had no stability issues during BLOOM-176B training, but I think it was one of the crucial ones.")

On PaLM's spikes ("'Bad' combination of data batch and model parameter state"):

> PaLM team observed dozens of loss spikes at "highly irregular intervals" when training larger models. While they were not able to track down the root cause, they mitigated the issue by restarting from an earlier checkpoint and skipping potentially problematic data batches.

On reading training logbooks:

> The best learning is to read Publicly available training LLM/VLM logbooks because there you can see exactly what happened and how the problem has been overcome.

Debug section index (debug/README.md) — guides for: Debugging PyTorch programs; Diagnosing Hangings and Deadlocks in Multi-Node Multi-GPU Python Programs; Network Debug; Troubleshooting NVIDIA GPUs; Underflow and Overflow Detection; plus tools (torch-distributed-gpu-test.py, NicerTrace).
