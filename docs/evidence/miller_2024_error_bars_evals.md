Source: https://arxiv.org/pdf/2411.00640 (Evan Miller, Anthropic, Nov 2024) + https://www.anthropic.com/research/statistical-approach-to-model-evals
Title: Adding Error Bars to Evals: A Statistical Approach to Language Model Evaluations
Fetched-via: r.jina.ai on the arXiv PDF and the Anthropic post, 2026-08-16
Fetch-status: verbatim from full PDF text (math notation mangled by the PDF-to-markdown pass; prose is clean)
Used-by: refs/llm_judges.md (repeat draws, temperature, paired differences)

# Adding Error Bars to Evals (excerpts)

## The five recommendations, verbatim from Section 1

> Our specific recommendations to researchers include: 1. Computing standard errors of the mean using the Central Limit Theorem 2. When questions are drawn in related groups, computing clustered standard errors 3. Reducing variance by resampling answers and by analyzing next-token probabilities 4. When two models are being compared, conducting statistical inference on the question-level paired differences, rather than the population-level summary statistics 5. Using power analysis to determine whether an eval (or a random subsample) is capable of testing a hypothesis of interest

The framing that makes the rest work, from Section 2:

> Suppose that the questions in an eval do not represent all possible questions, but instead were drawn at random from a (hypothetical, infinite, unseen) super-population of questions. This simple supposition lets us jump "through the looking glass" of the specific questions that appear in an eval in order to study the underlying skill that the eval is attempting to measure.

Reporting practice, from the Table 2 caption:

> We suggest two new reporting practices: including the number of questions in each eval, and the standard error of each estimate in parentheses (fictional models and numbers).

## Section 3.1: repeat draws help, with diminishing returns

The worked binary-score example with uniformly distributed question difficulty:

> Going from K = 1 (no resampling of answers) to K = 2, the total variance is reduced by 1/3. Increasing to K = 4, we have a variance reduction of 1/2, and setting K = 6, we reduce variance by 5/9. The upper limit on variance reduction via resampling in this example is 2/3. Note that computing a pooled standard error across all KN answers will be inconsistent, as multiple answers to the same question would violate the assumption of independent draws.

So the draws only ever remove the response-level (conditional) variance. Question-difficulty
variance is the floor, and only more questions moves it.

## Section 3.3: "Don't touch the thermostat!"

> It may be tempting to reduce the "sampling temperature" of the model in order to reduce (or eliminate) the conditional variance. However, we advise against this practice, unless the purpose is to study the model at the new temperature. Besides altering the model's behavior, adjusting the sampling temperature may simply shift the conditional variance (which can be mitigated using the two techniques above) into the variance of the conditional means (which cannot), or else reduce conditional variance by injecting bias into the estimator.

The first worked counter-example, a single-token true/false eval with difficulty x ~ U[0,1]:

> As in Section 3.1, Var(x_T=1) = 1/12. But at T = 0, x_T=0 = 1{x_T=1 > 0.5} and the uniform distribution is "rounded" into a Bernoulli distribution with p = 1/2. So Var(x_T=0) = 1/4. In this case, reducing the sampling temperature, and thereby eliminating the conditional variance, has inadvertently tripled the minimum variance in the score data from 1/12 to 1/4.

The second, where the mean moves too, with difficulty x ~ U[1/3, 1]:

> Then E[x_T=1] = 2/3 < E[x_T=0] = 3/4 and Var(x_T=1) = 1/27 << Var(x_T=0) = 3/16; that is, not only has the temperature change shifted the expected score, but the variance of the conditional means has increased approximately five-fold.

The closing rule of the section:

> When next-token probabilities are not available, or the answer requires a chain of thought or other complex interaction, choose a K such that E[sigma_i^2]/K << Var(x) and compute the standard error across question-level mean scores. In neither case should the sampling temperature be adjusted for the sake of reducing variance in the scores.

## Section 4.2: paired differences

> The naive comparison above misses an opportunity to reduce the standard error when two models evaluate the same set of questions.

The Anthropic post gives the size of the effect in practice:

> Since the question list is shared across models, conducting a paired-differences test lets us eliminate the variance in question difficulty and focus on the variance in responses. [...] In practice, we find the correlation of question scores on popular evals between frontier models to be substantial - between 0.3 and 0.7 on a scale of -1 to +1. Put another way, frontier models have an overall tendency to get the same questions right and wrong. Paired-difference analysis thus represents a "free" variance reduction technique that is very well suited for AI model evals.

And it names an existing implementation of the resampling recommendation:

> If an eval uses chain-of-thought reasoning, we recommend resampling answers from the same model several times, and using the question-level averages as the question scores fed into the Central Limit Theorem. We note that the Inspect framework correctly computes standard errors in this way via its _epochs_ parameter.

epistemic context: arXiv stat.AP preprint by an Anthropic author, with a first-party company post
summarising it. Not peer reviewed, but the statistics are textbook (CLT, clustered SEs, paired
t-test, power analysis) rather than novel claims, and the recommendations are now visible in
tooling (Inspect epochs). The variance-reduction fractions above are all from one worked
uniform-difficulty toy example, not measured on a real eval; treat the direction as general and
the numbers as illustrative.
