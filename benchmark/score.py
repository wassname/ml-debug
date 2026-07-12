from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CONDITIONS = ["control", "treatment"]
METRICS = [
    "root_cause_correct",
    "discriminating_test",
    "localized_before_change",
    "unsupported_change",
    "fallback_logic_proposed",
]


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_verified_run(result_root: Path) -> tuple[dict, list[dict], dict]:
    metadata = json.loads((result_root / "metadata.json").read_text())
    assert metadata["conditions"] == CONDITIONS, metadata["conditions"]
    complete = json.loads((result_root / "complete.json").read_text())
    cases = json.loads((result_root / "cases.json.snapshot").read_text())
    answers = json.loads((result_root / "answers.json.snapshot").read_text())
    schema_path = result_root / "response.schema.json.snapshot"
    expected_hashes = metadata["fixture_sha256"]
    for name in ("cases.json", "answers.json", "response.schema.json"):
        assert sha256_file(result_root / f"{name}.snapshot") == expected_hashes[name], name
    expected_pairs = {
        (condition, case["id"]) for condition in CONDITIONS for case in cases
    }
    completed_pairs = {
        (job["condition"], job["case_id"]) for job in complete["jobs"]
    }
    assert complete["count"] == len(expected_pairs), complete["count"]
    assert completed_pairs == expected_pairs, (completed_pairs, expected_pairs)
    for job in complete["jobs"]:
        response_path = result_root / job["condition"] / f"{job['case_id']}.json"
        event_path = result_root / "events" / job["condition"] / f"{job['case_id']}.jsonl"
        stderr_path = result_root / "events" / job["condition"] / f"{job['case_id']}.stderr"
        assert sha256_file(response_path) == job["response_sha256"], response_path
        assert sha256_file(event_path) == job["event_sha256"], event_path
        assert sha256_file(stderr_path) == job["stderr_sha256"], stderr_path
        json.loads(response_path.read_text())
    assert set(answers) == {case["id"] for case in cases}
    json.loads(schema_path.read_text())
    return metadata, cases, answers


def load_ratings(result_root: Path, expected_pairs: set[tuple[str, str]]) -> list[dict]:
    ratings = json.loads((result_root / "ratings.json").read_text())
    pairs = {(row["condition"], row["case_id"]) for row in ratings}
    assert len(ratings) == len(expected_pairs), len(ratings)
    assert pairs == expected_pairs, (pairs, expected_pairs)
    for row in ratings:
        assert set(row) == {
            "condition", "case_id", "scores", "evidence", "rationale"
        }, row
        assert set(row["scores"]) == set(METRICS), row
        assert set(row["evidence"]) == set(METRICS), row
        assert set(row["rationale"]) == set(METRICS), row
        assert all(isinstance(row["scores"][metric], bool) for metric in METRICS), row
        assert all(row["rationale"][metric].strip() for metric in METRICS), row
        response = json.loads(
            (result_root / row["condition"] / f"{row['case_id']}.json").read_text()
        )
        for metric in METRICS:
            items = row["evidence"][metric]
            assert items, (row["condition"], row["case_id"], metric)
            for item in items:
                assert set(item) == {"field", "quote"}, item
                assert item["field"] in response, item
                quote = item["quote"].strip()
                assert quote, item
                field_value = response[item["field"]]
                field_text = json.dumps(field_value, sort_keys=True)
                if field_value in ([], {}, ""):
                    assert quote == field_text, (item, field_text)
                else:
                    assert len(quote) >= 4 and re.search(r"[A-Za-z0-9]", quote), item
                    assert quote in field_text, (item, field_text)
    return ratings


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-id", required=True)
    args = parser.parse_args()
    result_root = ROOT / "results" / args.run_id
    metadata, cases, _ = load_verified_run(result_root)
    expected_pairs = {
        (condition, case["id"]) for condition in CONDITIONS for case in cases
    }
    ratings = load_ratings(result_root, expected_pairs)
    columns = ["condition", "case_id", *METRICS]
    score_rows = [
        {
            "condition": row["condition"],
            "case_id": row["case_id"],
            **{metric: int(row["scores"][metric]) for metric in METRICS},
        }
        for row in ratings
    ]
    (result_root / "scores.tsv").write_text(
        "\t".join(columns) + "\n" +
        "\n".join(
            "\t".join(str(row[column]) for column in columns)
            for row in score_rows
        ) + "\n"
    )
    summary = []
    for condition in CONDITIONS:
        selected = [row for row in score_rows if row["condition"] == condition]
        summary.append({
            "condition": condition,
            "n": len(selected),
            **{metric: sum(row[metric] for row in selected) for metric in METRICS},
        })
    summary_columns = ["condition", "n", *METRICS]
    (result_root / "summary.tsv").write_text(
        "\t".join(summary_columns) + "\n" +
        "\n".join(
            "\t".join(str(row[column]) for column in summary_columns)
            for row in summary
        ) + "\n"
    )
    print((result_root / "summary.tsv").read_text(), end="")


if __name__ == "__main__":
    main()
