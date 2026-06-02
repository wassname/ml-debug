# The 37 Implementation Details of Proximal Policy Optimization

Authors: Huang, Shengyi; Dossa, Rousslan Fernand Julien; Raffin, Antonin; Kanervisto, Anssi; Wang, Weixun.
Source: ICLR Blog Track, 2022-03-25 — https://iclr-blog-track.github.io/2022/03/25/ppo-implementation-details/
Code: https://github.com/vwxyzjn/ppo-implementation-details ; CleanRL: https://github.com/vwxyzjn/cleanrl

Excerpt cached for the ML-debugging skill (the full post is long; key framing passages below, verbatim).

---

> Instead of doing ablation studies and making recommendations on which details matter, this blog post takes a step back and focuses on reproductions of PPO's results in all accounts.

> During our re-implementation, we have compiled an implementation checklist containing 37 details as follows. For each implementation detail, we display the permanent link to its code (which is not done in academic papers) and point out its literature connection.

The 37 details break down as:
- 13 core implementation details
- 9 Atari-specific implementation details
- 9 implementation details for robotics tasks (continuous action spaces)
- 5 LSTM implementation details
- 1 `MultiDiscrete` action-spaces implementation detail
- (plus 4 situational details not used in the official implementation)

> Our ultimate purpose is to help people understand the PPO implementation through and through, reproduce past results with high fidelity, and facilitate customization for new research.

Context: the official PPO implementation (`openai/baselines`, `ppo2`) has undergone several refactorings, so "it is important to recognize *which version* of the official implementation is worth studying." Libraries that match `ppo2`'s details closely (Stable-Baselines3, CleanRL) reproduce similar results; others report more diverse (worse) results.
