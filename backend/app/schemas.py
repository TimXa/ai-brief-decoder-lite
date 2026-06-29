from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from .models import RunStatus


Severity = Literal["low", "medium", "high"]


class DecodeRequest(BaseModel):
    text: str = Field(min_length=20, max_length=12000)
    mode: Literal["normal", "malformed_json", "missing_fields", "bad_severity", "provider_failure"] = "normal"


class Risk(BaseModel):
    risk: str = Field(min_length=1)
    severity: Severity
    reason: str = Field(min_length=1)


class DecodedBrief(BaseModel):
    summary: str = Field(min_length=1)
    goals: list[str] = Field(min_length=1)
    deliverables: list[str] = Field(min_length=1)
    constraints: list[str] = Field(default_factory=list)
    risks: list[Risk] = Field(default_factory=list)
    clarifying_questions: list[str] = Field(default_factory=list)
    recommended_next_action: str = Field(min_length=1)


class SafeError(BaseModel):
    code: str
    message: str


class DecodeResponse(BaseModel):
    run_id: UUID
    status: RunStatus
    result: DecodedBrief | None = None
    error: SafeError | None = None


class RunResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    status: RunStatus
    input_text: str
    structured_result: dict | None
    raw_provider_output: str | None
    error_code: str | None
    error_message: str | None
    created_at: datetime
    updated_at: datetime
