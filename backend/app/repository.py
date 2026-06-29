from uuid import UUID

from sqlalchemy.orm import Session

from .models import DecodeRun, RunStatus


def create_run(
    db: Session,
    *,
    input_text: str,
    status: RunStatus,
    structured_result: dict | None = None,
    raw_provider_output: str | None = None,
    error_code: str | None = None,
    error_message: str | None = None,
) -> DecodeRun:
    run = DecodeRun(
        input_text=input_text,
        status=status,
        structured_result=structured_result,
        raw_provider_output=raw_provider_output,
        error_code=error_code,
        error_message=error_message,
    )
    db.add(run)
    db.commit()
    db.refresh(run)
    return run


def get_run(db: Session, run_id: UUID) -> DecodeRun | None:
    return db.get(DecodeRun, run_id)
