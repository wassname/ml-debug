# AGENTS.md

<!-- Template from ml-debug. Budget: under 150 lines. This file is read at the start of every
session, so each line must earn its place: it contradicts what an agent would do by default, or
its absence already cost a day. Date every entry. Delete an entry when it stops being true;
history goes in the journal. Agents may add entries, signed; the user's quotes stay verbatim. -->

## Goal

<!-- The user's own words, from an interview: ask until you can say what they will be shown when
it works. Quote, fix spelling only, date. No paraphrase by an agent in this section. -->

> "<what the user wants, in their words>" -- <user>, <date>

Not the goal (what agents drift into):

> "<e.g. we are not trying to X; X is only a baseline>" -- <user>, <date>

## Status (5 lines at most)

- Mode: exploring (nothing works yet) | confirming (it works; controls and seeds now).
- Best so far and the baseline to beat: <one line each, with the run folder, so nobody reruns them>.
- What is being tried now, and where its spec is.

## Names

<!-- The ten names used most, taken from the latest one or two reference papers and their code.
Full list in docs/JARGON.md. Long enough to signpost. -->

| say | not | from |
|---|---|---|
| <token-edit pair> | <twin> | <paper or user, date> |

## Key concepts

<!-- Quoted from the reference papers and code as generous blocks, with file and line. Include the
facts about the baseline that agents keep getting wrong, each checked against the reference code. -->

> "<two to four sentences from the paper, the key one in bold>" -- [<paper>:<line>](docs/papers/<file>.md)

## Gotchas and lessons

<!-- One line each: what went wrong, what to do, date, who said it. Only what would bite again. -->

- <e.g. each method is read at its own dose, never at the same dose number> -- <user>, <date>

## How a result is shown

<!-- The fixed results table (rows, columns, order) and the demo rules. Agents may not change it. -->

## Commands and limits

- Smoke test (under 3 minutes, foreground): `<command>`
- A run and its evaluation (under 30 minutes): `<command>`
- Queue, GPU and disk rules; files that must not be edited.

## Read first

| what | where |
|---|---|
| the current spec | <path> |
| lab notes, every run: search here before you propose a method | <path> |
| reference code to compare with | <path> |
