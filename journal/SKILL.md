---
name: ml-debug-journal
description: "Appends a dated entry to RESEARCH_JOURNAL.md: a run result, an analysis, a plan or decision, or a reading note. Use when the user types /arj or /ml-debug-journal, asks to log a result or write a lab note, or when a run or an analysis changes a belief. A result entry holds the evidence copied from the log with its source, each number beside its value under a null, and the competing explanations with a credence each. Replaces arj. Sub-skill of ml-debug."
---

# Research journal entry

<!-- Written by PI/Claude, 2026-11-17, from wassname's arj skill, the lab report in ml-debug, and his annoy-less skill. Tested old against new on three past results; the test is kept with the private arj stub. -->

The reader is wassname in a month, or an agent with no memory of this session. They read the entry to decide how much to trust a result and what to run next. They know the field. They do not know this week's names, the job numbers, or what was said in chat.

The entry records what was observed and what you believe, so that the reader can disagree with you. It does not argue for a conclusion.

## A result

For a run that finished or crashed, do the steps of that row in the `ml-debug` skill first. The entry records what those steps gave.

````markdown
## 2026-03-01 12:05 -- answer-only loss mask: small gain in exact match, not separable from seed variance

<One to three sentences in words: what was tested, against what, and what was observed.>

Context. Commit, job id, command, model, evaluation size. Exploring or confirming.

Prediction, written before the run: "<quoted from the job label, run.md or the plan entry>"

Evidence.

| run                         | exact match | answer loss |
|:----------------------------|------------:|------------:|
| answer-only mask            |       0.470 |        0.41 |
| full-sequence loss (job 37) |       0.445 |        0.48 |
| base model                  |       0.215 |        2.41 |

Source: `outputs/20260301T1140_answer_mask_s0/run.md`, section "Result". I read 20 of the 200
replies, sampled with seed 0. One of them: "<the reply, quoted>".

Interpretation (mine, Claude). To explain: <the observation, in one sentence>.
- <NN>% <explanation>. For: "<quote or number, with its source>". Against: "<quote>" | untested.
- <NN>% a bug or an unintended setting in my code or in the metric: <which one>. For: ... Against: ...
- <NN>% variance between seeds or items: <what is known about its size>.
- <NN>% a cause that is not in this list.
Test that separates the first two: <command>, and the result that each predicts.
Credence that <the claim>: <NN>% before the run, <NN>% now.

Decision (wassname): "<his words>". Next: job 42, `why: ...; resolve: ...`.

-- PI/Claude
````

A complete example: [examples/toolkit/lab_report.md](../examples/toolkit/lab_report.md).

Evidence:

- Copy the table or the log lines, and give one source: the path, with the section or the line. For a mean or a ratio, quote the rows that it was computed from. Do not write a number that is in no file. Write "not measured" and put the measurement under Next.
- Put each main number beside its value under a null in the same table: the base model, chance, or a shuffled or random control.
- When the result depends on generated text or on a judge's score, quote one or two outputs and state how you chose them.
- In a sentence, give the conclusion in words, then the number with the value it is compared with: "0.470 against 0.445 for full-sequence loss, 5 problems of 200". Leave the values for each dose and each item in the table or in the log.

Interpretation:

- Write it in the first person, under its own label, with your model's name.
- List the explanations when the entry says that something works, fails, or is better than or equal to something else, or when a decision depends on it. That is most results.
- A run that failed shows that this implementation did not work. It does not show that the method fails.
- Before you write that an added part did not help (more data, a new loss, a new module), quote the measurement that shows the part took effect: the loss on the added data fell, its parameters moved, or the output changes when it is removed. If nothing measured this, the result is "not tested" and the measurement is the next run.
- If no prediction was recorded before the run, write "No prediction was recorded." Do not write one after the result.

Words:

- State what a thing does, then its project name: "the model that scores whether a reply shows the trait (the reply judge)". Use that name each time afterwards. Use the field's term from papers. Give a metric the name it has in the code, in backticks.
- Use the literal word: "method" or "variant" for "arm", "parameter" for "knob", "early check" for "canary". Delete words that claim a quality or tell the reader how to react: "striking", "promising", "clean", "robust", "honest", "notably".
- Leave out counts of work done (tests passed, rows processed, review rounds) unless the count is the result.
- Use ASCII punctuation in prose: no em dash, and "to" in place of an arrow.
- For the other prose rules, use the `annoy-less` skill.

## Other entries

- Plan or decision, before a run. State the question that the run answers in one sentence, and the run it is compared with. Give the decision and who made it, in their words. Give your credence now and the credence you would move to for each outcome. Give the action for each outcome.
- Reading note or design idea. Write one paragraph: what the source says, quoted with its location, then your reading, labelled as yours, with a credence. Do not add a table or headings.

An entry grows with its evidence. Do not add parts to make a short note look like a report. Most result entries in wassname's research journals have 300 to 500 words outside their tables. Leave the values for each dose and each item in the run report, and link it.

## Check before you append

List each project name, abbreviation and metric in the entry. Beside each, copy the sentence from the entry that says in plain words what it is. For a metric, that sentence names what it is computed from, what it is an error against, and the axis each mean or sum runs over. Where there is no such sentence, add one or remove the name. Keep the list in your working notes, not in the entry.

## Write it

- The journal is `RESEARCH_JOURNAL.md` in the repository root, or in `docs/`. If neither exists, ask.
- Entries are oldest first. Append at the end. Get the time from `date '+%Y-%m-%d %H:%M'`.
- The heading states the result in words, so that a reader of the headings alone learns it. Refer to an earlier entry with a Markdown link to its heading.
- Do not edit an earlier entry. A correction is a new entry that links to the entry it corrects.
- When the user gives no detail, the session is the material. Find the job id, the log path and the commit yourself. Ask only for what no file holds.

```bash
cat >> RESEARCH_JOURNAL.md <<'EOF'

## 2026-03-01 12:05 -- The result in words

Entry text.
EOF
tail -n 20 RESEARCH_JOURNAL.md
```
