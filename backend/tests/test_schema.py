import pytest
from pydantic import ValidationError

from app.schemas import DecodedBrief


def valid_payload():
    return {
        "summary": "Landing page request",
        "goals": ["Explain product"],
        "deliverables": ["Landing page"],
        "constraints": ["Two weeks"],
        "risks": [{"risk": "Scope creep", "severity": "medium", "reason": "Several outputs requested"}],
        "clarifying_questions": ["Who approves copy?"],
        "recommended_next_action": "Confirm scope",
    }


def test_decoded_brief_accepts_valid_payload():
    decoded = DecodedBrief.model_validate(valid_payload())
    assert decoded.risks[0].severity == "medium"


def test_decoded_brief_rejects_missing_required_fields():
    with pytest.raises(ValidationError):
        DecodedBrief.model_validate({"summary": "Only summary"})


def test_decoded_brief_rejects_invalid_severity():
    payload = valid_payload()
    payload["risks"][0]["severity"] = "urgent"
    with pytest.raises(ValidationError):
        DecodedBrief.model_validate(payload)
