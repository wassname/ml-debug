"""Offline regression checks through both production examples. -- PI/OpenAI"""
import asyncio
import json
import math
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import AsyncMock, patch

import httpx
from inspect_ai import eval as inspect_eval
from inspect_ai.log import read_eval_log
from inspect_ai.model import ChatCompletionChoice, ChatMessageAssistant, ChatMessageUser, ContentReasoning, ContentText, GenerateConfig, ModelOutput, get_model
from openai.types.chat import ChatCompletion

import judge_inspect as evidence
import judge_jev as jev

PAIR = {"id": "fair", "context": "Return a useful answer.", "response_a": "GOOD response", "response_b": "BAD response"}


def jev_response(request):
    state = request["state"]
    preferred = "A" if state["answer_A"] == "GOOD response" else "B"
    if state["context"] == "position-biased":
        preferred = "A"
    elif state["context"] == "option-biased":
        preferred = next(iter(request["questions"]["preference"]["criteria"]))
    elif state["answer_A"] == state["answer_B"]:
        preferred = "tie"
    answers = {}
    for name, question in request["questions"].items():
        if question["type"] == "score":
            index = 0 if preferred == "A" else 4 if preferred == "B" else 2
            answers[name] = {"type": "score", "score": index + (0.01 if preferred == "tie" else 0), "confidence": 1,
                             "probabilities": {str(i): float(i == index) for i in range(5)}, "legend": dict(enumerate(question["criteria"]))}
        else:
            if name == "debug_word":
                if state["context"] == "word option bias":
                    label = next(iter(question["criteria"]))
                else:
                    label = "none" if state["context"] == "clear setup" else "ambiguity"
            else:
                label = preferred if name == "preference" else "no"
            answers[name] = {"type": "choice", "choice": label, "confidence": 1,
                             "probabilities": {key: float(key == label) for key in question["criteria"]}}
    return {"model": jev.MODEL, "answers": answers, "usage": {"cost": 0.001}}


class JevTests(unittest.IsolatedAsyncioTestCase):
    async def test_views_cache_and_bias_diagnostics(self):
        calls = []

        async def respond(request):
            body = json.loads(request.content)
            calls.append(body)
            return httpx.Response(200, json=jev_response(body))

        pairs = [PAIR, PAIR | {"id": "position", "context": "position-biased"}, PAIR | {"id": "options", "context": "option-biased"},
                 PAIR | {"id": "same", "response_b": "GOOD response"}]
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            async with httpx.AsyncClient(transport=httpx.MockTransport(respond)) as client:
                results = await jev.judge(pairs, client, output)
                self.assertEqual(len(calls), 14)
                self.assertEqual(results[0]["preference"], {"A": 1, "tie": 0, "B": 0})
                self.assertFalse(results[0]["response_order_flip"])
                self.assertTrue(results[1]["response_order_flip"])
                self.assertEqual(results[1]["response_order_discrepancy"], 2)
                self.assertEqual(results[2]["option_order_discrepancy"], 2)
                self.assertIsNone(results[3]["response_order_flip"])
                self.assertIsNone(results[3]["response_order_discrepancy"])
                self.assertEqual(results[3]["change"], 0)
                self.assertEqual(await jev.judge(pairs, client, output), results)
                self.assertEqual(len(calls), 14)
                await jev.judge([PAIR], client, output, criterion="Which response is more concise?")
                self.assertEqual(len(calls), 18)
            self.assertIn('"probabilities"', (output / "run.md").read_text())
            self.assertIn('"response_text"', (output / "requests.jsonl").read_text())
        self.assertEqual(set(calls[0]["state"]), {"context", "answer_A", "answer_B"})
        self.assertEqual(len(calls[0]["questions"]), 10)

    async def test_debug_word_is_unscored_cached_and_inside_the_scoring_request(self):
        calls = []
        words = ["ambiguity", "truncated", "✂️"]

        async def respond(request):
            body = json.loads(request.content)
            calls.append(body)
            return httpx.Response(200, json=jev_response(body))

        pair = PAIR | {"candidate_a": "better", "candidate_b": "worse"}
        pairs = [pair, pair | {"id": "clear", "context": "clear setup"}]
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            async with httpx.AsyncClient(transport=httpx.MockTransport(respond)) as client:
                baseline = await jev.judge(pairs, client, Path(directory) / "base")
                n_base = len(calls)
                rows = await jev.judge(pairs, client, output, debug_words=words)
                self.assertEqual(len(calls) - n_base, n_base)  # same number of requests: the word adds none
                strip = lambda row: {k: v for k, v in row.items() if k not in ("debug", "views")}
                self.assertEqual([strip(row) for row in rows], [strip(row) for row in baseline])
                self.assertEqual(jev.bradley_terry(rows), jev.bradley_terry(baseline))
                self.assertEqual([row["debug"]["word"] for row in rows], ["ambiguity", "none"])
                self.assertTrue(all(row["debug"]["unscored"] and not row["debug"]["option_order_disagreement"] for row in rows))
                n = len(calls)
                self.assertEqual(await jev.judge(pairs, client, output, debug_words=words), rows)
                self.assertEqual(len(calls), n)  # cached
        for body in calls[n_base:]:
            options = body["questions"]["debug_word"]["criteria"]
            self.assertLessEqual(len(options), 255)
            self.assertEqual(set(options), {"none", "idk", *words})

    async def test_debug_word_option_disagreement_and_invalid_vocabulary(self):
        pair = PAIR | {"context": "word option bias"}
        views = [{**{"key": str(i)}, "response": jev_response(jev.pair_request(pair, order, reverse, debug_words=["ambiguity", "context"])),
                  "order": order} for i, (order, reverse) in enumerate([("AB", False), ("AB", True), ("BA", False), ("BA", True)])]
        self.assertTrue(jev.summarize(pair, views)["debug"]["option_order_disagreement"])
        for words in (["context", "context"], ["two words"], ["none"], ["w" + str(i) for i in range(254)]):
            with self.assertRaises(AssertionError):
                jev.debug_options(words)

    async def test_transient_retry_and_permanent_failure(self):
        attempts = []

        def respond(request):
            attempts.append(request)
            return httpx.Response(529) if len(attempts) == 1 else httpx.Response(200, json=jev_response(json.loads(request.content)))

        with tempfile.TemporaryDirectory() as directory, patch("judge_jev.asyncio.sleep", new=AsyncMock()):
            async with httpx.AsyncClient(transport=httpx.MockTransport(respond)) as client:
                await jev.decide(client, jev.pair_request(PAIR, "AB", False), Path(directory) / "trace.jsonl")
            self.assertEqual(len(attempts), 2)
            async with httpx.AsyncClient(transport=httpx.MockTransport(lambda request: httpx.Response(400))) as client:
                with self.assertRaises(httpx.HTTPStatusError):
                    await jev.decide(client, jev.pair_request(PAIR, "AB", False), Path(directory) / "trace.jsonl")

    def test_option_order_is_part_of_cache_identity(self):
        normal = jev.pair_request(PAIR, "AB", False)
        reversed_options = jev.pair_request(PAIR, "AB", True)
        self.assertNotEqual(jev.request_key(normal), jev.request_key(reversed_options))
        self.assertEqual(normal["questions"]["change"], reversed_options["questions"]["change"])

    def test_bradley_terry_ranking_and_disconnected_groups(self):
        rows = [{"candidate_a": "better", "candidate_b": "worse", "preference": {"A": 1, "tie": 0, "B": 0}}]
        ranking = jev.bradley_terry(rows)
        self.assertEqual(ranking[0]["candidate"], "better")
        self.assertTrue(all(math.isfinite(row["strength"]) for row in ranking))
        reversed_rows = [{"candidate_a": "worse", "candidate_b": "better", "preference": {"A": 0, "tie": 0, "B": 1}}]
        self.assertEqual(jev.bradley_terry(reversed_rows), ranking)
        with self.assertRaisesRegex(AssertionError, "disconnected"):
            jev.bradley_terry(rows + [{"candidate_a": "other", "candidate_b": "another", "preference": {"A": 0, "tie": 1, "B": 0}}])


class InspectTests(unittest.TestCase):
    def test_real_inspect_execution_reasoning_replay_and_cache(self):
        calls, replayed = [], []

        async def respond(input, tools, tool_choice, config):
            calls.append(config)
            text = input[0].text
            options = config.response_schema.json_schema.properties["preference"].enum
            self.assertEqual(options, ["B", "tie", "A"] if "in this order: B" in text else ["A", "tie", "B"])
            self.assertEqual(config.extra_body["provider"], evidence.PROVIDER)
            if len(input) == 1:
                return ModelOutput(model="mockllm", choices=[ChatCompletionChoice(message=ChatMessageAssistant(content=[ContentReasoning(reasoning="Read both responses.")]), stop_reason="max_tokens")])
            replayed.append([part.reasoning for part in input[-2].content if isinstance(part, ContentReasoning)])
            self.assertEqual(config.extra_body["reasoning"], {"enabled": False})
            a = text.split("Response A:\n", 1)[1].split("\n\nResponse B:\n", 1)[0]
            b = text.split("Response B:\n", 1)[1]
            good_a = a == "GOOD response"
            judgment = {"explanation": "The GOOD response is more useful.",
                        "response_A": {"quotes": [a], "quality": 3 if good_a else 0, "refusal": not good_a, "incoherence": False, "repetition": False, "off_topic": False},
                        "response_B": {"quotes": [b], "quality": 0 if good_a else 3, "refusal": good_a, "incoherence": False, "repetition": False, "off_topic": False},
                        "preference": "A" if good_a else "B", "judge_note": ""}
            return ModelOutput(model="mockllm", choices=[ChatCompletionChoice(message=ChatMessageAssistant(content=[ContentText(text=json.dumps(judgment))]), stop_reason="stop")])

        with tempfile.TemporaryDirectory() as directory, patch.dict(os.environ, {"INSPECT_CACHE_DIR": directory + "/cache"}):
            model = get_model("mockllm/model", custom_outputs=respond)
            log = inspect_eval(evidence.judgments([PAIR], passes=2, model=model), log_dir=directory + "/logs", display="none")[0]
            self.assertEqual(log.status, "success", log.error)
            full = read_eval_log(log.location)
            rows = evidence.summarize(full, [PAIR], 2, Path(directory) / "summary")
            self.assertEqual(rows[0]["preference"], {"A": 1, "tie": 0, "B": 0})
            self.assertEqual(rows[0]["quality_change"], -3)
            self.assertEqual(rows[0]["failures"]["refusal_a"], 0)
            self.assertEqual(rows[0]["failures"]["refusal_b"], 1)
            self.assertEqual(rows[0]["option_order_discrepancy"], 0)
            self.assertEqual(replayed, [["Read both responses."]] * 8)
            self.assertEqual(len(calls), 16)
            trace = (Path(directory) / "summary/run.md").read_text()
            self.assertIn("Read both responses.", trace)
            self.assertIn('"events"', trace)
            self.assertIn('"response_schema"', trace)
            inspect_eval(evidence.judgments([PAIR], passes=2, model=model), log_dir=directory + "/logs", display="none")
            self.assertEqual(len(calls), 16)

    def test_provider_adapter_transmits_constraints_and_records_routing(self):
        async def exercise():
            api = get_model(evidence.MODEL, api_key="offline-fixture").api
            requests = []

            async def respond(**request):
                requests.append(request)
                return ChatCompletion.model_validate({"id": "fixture", "created": 0, "object": "chat.completion", "model": evidence.MODEL_ID,
                                                       "provider": "DeepInfra", "choices": [{"index": 0, "finish_reason": "stop", "message": {"role": "assistant", "content": "{}"}}]})

            with patch.object(api.client.chat.completions, "create", new=respond):
                result = await api.generate(input=[ChatMessageUser(content="Return JSON.")], tools=[], tool_choice="none",
                                            config=GenerateConfig(extra_body=evidence.OPTIONS, response_schema=evidence.schema(False)))
            output, _ = result
            self.assertEqual(requests[0]["extra_body"]["provider"], evidence.PROVIDER)
            self.assertEqual(output.metadata["provider"], "DeepInfra")
            self.assertEqual(output.metadata["eligible_quantizations"], ["fp8"])
        asyncio.run(exercise())

    def test_unquoted_evidence_fails(self):
        judgment = {"quotes": ["invented"], "quality": 0, "refusal": False, "incoherence": False, "repetition": False, "off_topic": False}
        rating = evidence.PairJudgment(explanation="", response_A=judgment, response_B=judgment, preference="tie", judge_note="")
        with self.assertRaisesRegex(AssertionError, "exact span"):
            evidence.validate_quotes(rating, PAIR, "AB")

    def test_standalone_scripts_have_no_sibling_imports(self):
        for filename in ("judge_jev.py", "judge_inspect.py"):
            with tempfile.TemporaryDirectory() as directory:
                destination = Path(directory) / filename
                shutil.copyfile(Path(__file__).parent / filename, destination)
                result = subprocess.run([sys.executable, str(destination), "--help"], capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn("--pairs", result.stdout)


if __name__ == "__main__":
    unittest.main()
