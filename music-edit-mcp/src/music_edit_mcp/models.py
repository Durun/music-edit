"""Pydantic models for MCP API input/output types. Populated in Phase 1+."""

from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str = "ok"
    version: str
