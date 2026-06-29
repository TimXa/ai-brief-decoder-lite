import json

from pydantic import ValidationError
from sqlalchemy.orm import Session

from .config import Settings
from .models import RunStatus
from .providers import ProviderError, get_provider
from .repository import create_run
from .schemas import DecodeRequest, DecodeResponse, DecodedBrief, SafeError


def decode_brief(db: Session, payload: DecodeRequest, settings: Settings) -> DecodeResponse:
    provider = get_provider(settings)

    try:
        provider_result = provider.decode(payload.text, payload.mode)
    except ProviderError:
        run = create_run(
            db,
            input_text=payload.text,
            status=RunStatus.failed,
            error_code="provider_error",
            error_message="Provider could not decode the brief",
        )
        return DecodeResponse(
            run_id=run.id,
            status=run.status,
            error=SafeError(code=run.error_code or "provider_error", message=run.error_message or ""),
        )

    try:
        data = json.loads(provider_result.raw)
    except json.JSONDecodeError:
        run = create_run(
            db,
            input_text=payload.text,
            status=RunStatus.failed,
            raw_provider_output=provider_result.raw,
            error_code="invalid_json",
            error_message="Provider returned malformed JSON",
        )
        return DecodeResponse(run_id=run.id, status=run.status, error=SafeError(code="invalid_json", message=run.error_message or ""))

    try:
        structured = DecodedBrief.model_validate(data)
    except ValidationError:
        run = create_run(
            db,
            input_text=payload.text,
            status=RunStatus.failed,
            raw_provider_output=provider_result.raw,
            error_code="invalid_structure",
            error_message="Provider response did not match the expected schema",
        )
        return DecodeResponse(
            run_id=run.id,
            status=run.status,
            error=SafeError(code="invalid_structure", message=run.error_message or ""),
        )

    run = create_run(
        db,
        input_text=payload.text,
        status=RunStatus.completed,
        structured_result=structured.model_dump(mode="json"),
        raw_provider_output=provider_result.raw,
    )
    return DecodeResponse(run_id=run.id, status=run.status, result=structured)
