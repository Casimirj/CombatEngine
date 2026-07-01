from pydantic import BaseModel, ConfigDict, Field


class GearInput(BaseModel):
    """Gear configuration for a custom loadout."""

    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    pieces: list[str] = Field(alias="Pieces")
