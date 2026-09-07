# Proposed ml-debug section: common mistakes

Draft for wassname to review. Source is his own list, given in chat on 2026-08-25. Spelling fixed,
his wording and his terms kept. Tone is a senior kindly telling a junior what the common student
mistakes are, rather than a warning label. Drafted by CLAUDE, so check that it sounds like you
before it goes in.

Open question for wassname, marked in the text below: the threshold item says what not to do but
not what to do instead. I do not want to invent your method, so tell me how you actually pick one.

---

## Common mistakes

Everyone makes these, and I have made most of them myself. They come up so often with AI agents
that they are worth naming, so you can catch yourself early rather than after a week of work.

Be careful about being overconfident. It is easy to write a diagnosis in the tone of a fact. Before
you commit to one, ask what you saw that a competing explanation could not also explain. If nothing,
then "I do not know, and here is what would tell me" is a good answer and not a failure.

Do not quit after the first change and call the negative real. One failed attempt is much more
likely to be a bug in your implementation than a refutation of the idea. This is the expensive
mistake, because the idea gets thrown away and nobody goes back to it. Look for the bug first.

Try not to stop at the first idea you come up with. It arrives with no competition, so it wins by
default rather than on merit. Write down two more, and say what observation would separate them. If
you cannot name a test that distinguishes them, you have a preference and not a hypothesis.

Watch out for getting obsessed with the legible hyperparameters. Learning rate, batch size and
warmup are easy to name and easy to change, so they attract more attention than they deserve. More
often the cause is in the data, a sign, a mask, an index, or a metric that answers a different
question from the one you asked.

Please read the data. Print the first full training sample, chosen and rejected, with the special
tokens and the loss mask showing. Look at it with your own eyes. Most formatting bugs are obvious in
the first sample and invisible in every aggregate.

Please read the log. Not the last twenty lines, the log. Find the first line where the run stopped
matching what you expected, quote it, and start from there.

Be wary of reaching for a cosine probe instead of building the training script with metrics. A
cosine similarity is quick to compute and hard to interpret, and across different subspaces or bases
it is correlational at best. Building the real thing and running it takes longer and answers the
question.

Do not fix on an arbitrary metric threshold before you have any idea what a fair or good threshold
is. Saying the metric must clear 0.8 means nothing until you know what counts as good here.
[wassname: how do you actually work out a fair threshold? I did not want to invent your method.]

Two of these do most of the damage: not reading the log, and not looking for your own bug. Start
there when you are not sure where to start.
