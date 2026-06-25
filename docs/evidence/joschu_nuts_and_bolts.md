Source: http://joschu.net/docs/nuts-and-bolts.pdf
Title: Nuts and Bolts of Deep RL Research - John Schulman (2016)
Fetched-via: clean transcript of the slide deck (prior markitdown PDF extract was OCR-garbled with `(cid:73)` bullet glyphs; replaced with hand-pasted text)
Fetch-status: verbatim (clean paste)

# The Nuts and Bolts of Deep RL Research

John Schulman, December 9th, 2016

## Outline

- Approaching New Problems
- Ongoing Development and Tuning
- General Tuning Strategies for RL
- Policy Gradient Strategies
- Q-Learning Strategies
- Miscellaneous Advice

## Approaching New Problems

New Algorithm? Use Small Test Problems
- Run experiments quickly
- Do hyperparameter search
- Interpret and visualize learning process: state visitation, value function, etc.
- Counterpoint: don't overfit algorithm to contrived problem
- Useful to have medium-sized problems that you're intimately familiar with (Hopper, Atari Pong)

New Task? Make It Easier Until Signs of Life
- Provide good input features
- Shape reward function

POMDP Design
- Visualize random policy: does it sometimes exhibit desired behavior?
- Human control
- Atari: can you see game features in downsampled image?
- Plot time series for observations and rewards. Are they on a reasonable scale?
- hopper.py in gym: reward = 1.0 - 1e-3 * np.square(a).sum() + delta x / delta t
- Histogram observations and rewards

Run Your Baselines
- Don't expect them to work with default parameters
- Recommended:
  - Cross-entropy method[^1]
  - Well-tuned policy gradient method[^2]
  - Well-tuned Q-learning + SARSA method

Run with More Samples Than Expected
- Early in tuning process, may need huge number of samples
- Don't be deterred by published work
- Examples:
  - TRPO on Atari: 100K timesteps per batch for KL= 0.01
  - DQN on Atari: update freq=10K, replay buffer size=1M

## Ongoing Development and Tuning

It Works! But Don't Be Satisfied
- Explore sensitivity to each parameter
- If too sensitive, it doesn't really work, you just got lucky
- Look for health indicators
  - VF fit quality
  - Policy entropy
  - Update size in output space and parameter space
  - Standard diagnostics for deep networks

Continually Benchmark Your Code
- If reusing code, regressions occur
- Run a battery of benchmarks occasionally

Always Use Multiple Random Seeds

Always Be Ablating
- Different tricks may substitute
- Especially whitening
- "Regularize" to favor simplicity in algorithm design space
- As usual, simplicity → generalization

Automate Your Experiments
- Don't spend all day watching your code print out numbers
- Consider using a cloud computing platform (Microsoft Azure, Amazon EC2, Google Compute Engine)

## General Tuning Strategies for RL

Whitening / Standardizing Data
- If observations have unknown range, standardize
- Compute running estimate of mean and standard deviation
- x' = clip((x − μ)/σ, −10, 10)
- Rescale the rewards, but don't shift mean, as that affects agent's will to live
- Standardize prediction targets (e.g., value functions) the same way

Generally Important Parameters
- Discount
  - Return_t = r_t + γr_{t+1} + γ²r_{t+2} + . . .
  - Effective time horizon: 1 + γ + γ² + · · · = 1/(1 − γ)
  - I.e., γ = 0.99 ⇒ ignore rewards delayed by more than 100 timesteps
  - Low γ works well for well-shaped reward
  - In TD(λ) methods, can get away with high γ when λ < 1
- Action frequency
  - Solvable with human control (if possible)
  - View random exploration

General RL Diagnostics
- Look at min/max/stdev of episode returns, along with mean
- Look at episode lengths: sometimes provides additional information
- Solving problem faster, losing game slower

## Policy Gradient Strategies

Entropy as Diagnostic
- Premature drop in policy entropy ⇒ no learning
- Alleviate by using entropy bonus or KL penalty

KL as Diagnostic
- Compute KL [π_old(· | s), π(· | s)]
- KL spike ⇒ drastic loss of performance
- No learning progress might mean steps are too large
- batchsize=100K converges to different result than batchsize=20K.

Baseline Explained Variance
- explained variance = 1 − Var[empirical return − predicted value] / Var[empirical return]

Policy Initialization
- More important than in supervised learning: determines initial state visitation
- Zero or tiny final layer, to maximize entropy

## Q-Learning Strategies

- Optimize memory usage carefully: you'll need it for replay buffer
- Learning rate schedules
- Exploration schedules
- Be patient. DQN converges slowly
- On Atari, often 10-40M frames to get policy much better than random

Thanks to Szymon Sidor for suggestions

## Miscellaneous Advice

- Read older textbooks and theses, not just conference papers
- Don't get stuck on problems—can't solve everything at once
- Exploration problems like cart-pole swing-up
- DQN on Atari vs CartPole

[^1]: István Szita and András Lőrincz (2006). "Learning Tetris using the noisy cross-entropy method". In: Neural computation.
[^2]: https://github.com/openai/rllab
