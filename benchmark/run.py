from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from validate import validate

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
BASE_INSTRUCTION = """Diagnose this machine-learning failure from the supplied evidence. Return only the requested JSON. Separate observations from inferences. The first_action field is the next action you would take. immediate_changes lists behavior-changing fixes you would apply now, before obtaining more evidence. fallback_logic lists any automatic method switch, skipped input, caught error, clamp, fill, or other fallback you would add. Use empty arrays when none are justified.

CASE:
"""


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_job(job: tuple[str, dict], args: argparse.Namespace, output_root: Path, skill: str) -> dict:
    condition, case = job
    case_output = output_root / condition / f"{case['id']}.json"
    event_output = output_root / "events" / condition / f"{case['id']}.jsonl"
    stderr_output = output_root / "events" / condition / f"{case['id']}.stderr"
    assert not case_output.exists(), case_output
    case_output.parent.mkdir(parents=True, exist_ok=True)
    event_output.parent.mkdir(parents=True, exist_ok=True)
    prompt = BASE_INSTRUCTION + case["prompt"]
    if condition == "treatment":
        prompt = f"<ml_debug_skill>\n{skill}\n</ml_debug_skill>\n\n" + prompt
    with tempfile.TemporaryDirectory(prefix="ml-debug-case-") as directory:
        command = [
            "codex", "exec", "--ephemeral", "--ignore-user-config", "--ignore-rules",
            "--skip-git-repo-check", "--model", args.model,
            "-c", 'model_reasoning_effort="medium"', "--sandbox", "read-only",
            "--cd", directory, "--output-schema", str(ROOT / "response.schema.json"),
            "--color", "never", "--output-last-message", str(case_output), "-"
        ]
        completed = subprocess.run(command, input=prompt, text=True, capture_output=True)
    event_output.write_text(completed.stdout)
    stderr_output.write_text(completed.stderr)
    assert completed.returncode == 0, (
        condition, case["id"], completed.returncode, completed.stderr[-2000:]
    )
    response = json.loads(case_output.read_text())
    required = json.loads((ROOT / "response.schema.json").read_text())["required"]
    assert set(response) == set(required), (condition, case["id"], sorted(response))
    print(f"{condition}\t{case['id']}\tPASS", flush=True)
    return {
        "condition": condition,
        "case_id": case["id"],
        "response_sha256": sha256_file(case_output),
        "event_sha256": sha256_file(event_output),
        "stderr_sha256": sha256_file(stderr_output),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--workers", type=int, default=4)
    args = parser.parse_args()
    cases, _ = validate()
    output_root = ROOT / "results" / args.run_id
    assert not output_root.exists(), output_root
    output_root.mkdir(parents=True)
    skill = (REPO / "SKILL.md").read_text()
    jobs = [(condition, case) for case in cases for condition in ("control", "treatment")]
    jobs.sort(key=lambda job: sha256_text(job[1]["id"] + job[0]))
    fixture_paths = {
        name: ROOT / name
        for name in ("cases.json", "answers.json", "response.schema.json")
    }
    for name, path in fixture_paths.items():
        (output_root / f"{name}.snapshot").write_bytes(path.read_bytes())
    metadata = {
        "run_id": args.run_id,
        "model": args.model,
        "workers": args.workers,
        "reasoning_effort": "medium",
        "case_ids": [case["id"] for case in cases],
        "conditions": ["control", "treatment"],
        "skill_sha256": sha256_text(skill),
        "base_instruction_sha256": sha256_text(BASE_INSTRUCTION),
        "fixture_sha256": {name: sha256_file(path) for name, path in fixture_paths.items()},
        "codex_version": subprocess.check_output(["codex", "--version"], text=True).strip(),
        "git_commit": subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=REPO, text=True
        ).strip(),
        "job_order": [f"{condition}/{case['id']}" for condition, case in jobs],
    }
    (output_root / "metadata.json").write_text(json.dumps(metadata, indent=2) + "\n")
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        completed_jobs = list(
            executor.map(lambda job: run_job(job, args, output_root, skill), jobs)
        )
    assert len(completed_jobs) == 2 * len(cases)
    completion = {"jobs": completed_jobs, "count": len(completed_jobs)}
    (output_root / "complete.json").write_text(json.dumps(completion, indent=2) + "\n")


if __name__ == "__main__":
    main()
