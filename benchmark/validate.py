from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def validate() -> tuple[list[dict], dict]:
    cases = json.loads((ROOT / "cases.json").read_text())
    answers = json.loads((ROOT / "answers.json").read_text())
    assert 8 <= len(cases) <= 12, len(cases)
    case_ids = [case["id"] for case in cases]
    assert len(case_ids) == len(set(case_ids)), case_ids
    assert all(re.fullmatch(r"case_\d{2}", case_id) for case_id in case_ids), case_ids
    assert set(case_ids) == set(answers), (case_ids, sorted(answers))
    for case in cases:
        assert set(case) == {"id", "prompt"}, case
        assert len(case["prompt"]) >= 120, case["id"]
    for case_id, answer in answers.items():
        assert set(answer) == {
            "root_cause", "discriminating_test", "requires_localization"
        }, case_id
        assert len(answer["root_cause"]) >= 40, case_id
        assert len(answer["discriminating_test"]) >= 30, case_id
        assert isinstance(answer["requires_localization"], bool), case_id
    schema = json.loads((ROOT / "response.schema.json").read_text())
    assert schema["additionalProperties"] is False
    print(f"benchmark validate: PASS ({len(cases)} neutral paired cases, hidden answer IDs match)")
    return cases, answers


if __name__ == "__main__":
    validate()
