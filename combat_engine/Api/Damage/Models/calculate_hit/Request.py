from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from .GearInput import GearInput
from .MonsterInput import MonsterInput


class CalculateHitInput(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    loadout: str = Field(alias="Loadout")
    weapon: str = Field(alias="Weapon")
    monster: MonsterInput = Field(alias="Monster")
    scale: int = Field(alias="Scale")
    gear_input: Optional[GearInput] = Field(default=None, alias="Gear")
    player_levels: Optional[dict] = Field(default=None, alias="PlayerLevels")
    always_hit: bool = Field(default=False, alias="AlwaysHit")
