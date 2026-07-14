from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class GearInput(BaseModel):
    """Gear configuration for a custom loadout."""

    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    pieces: list[str] = Field(alias="Pieces")
    prayer: Optional[str] = Field(default=None, alias="Prayer")
    boosts: Optional[list[str]] = Field(default=None, alias="Boosts")
