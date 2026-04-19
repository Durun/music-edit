"""Pydantic models for MCP API input/output types. Populated in Phase 1+."""

from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str = "ok"
    version: str


class WriteError(BaseModel):
    type: str  # "parse_error" | "write_error"
    message: str


class WriteResult(BaseModel):
    success: bool
    errors: list[WriteError]
