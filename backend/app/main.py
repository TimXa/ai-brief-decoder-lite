from uuid import UUID

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from .config import Settings, get_settings
from .database import Base, engine, get_db
from .repository import get_run
from .schemas import DecodeRequest, DecodeResponse, RunResponse
from .service import decode_brief

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Brief Decoder Lite")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/v1/briefs/decode", response_model=DecodeResponse)
def decode(
    payload: DecodeRequest,
    db: Session = Depends(get_db),
    settings: Settings = Depends(get_settings),
) -> DecodeResponse:
    return decode_brief(db, payload, settings)


@app.get("/v1/briefs/runs/{run_id}", response_model=RunResponse)
def read_run(run_id: UUID, db: Session = Depends(get_db)) -> RunResponse:
    run = get_run(db, run_id)
    if run is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Run not found")
    return RunResponse.model_validate(run)
