from pydantic import BaseModel, ConfigDict


class CalculateHitOutput(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    damage: int
    monster_defense: int
