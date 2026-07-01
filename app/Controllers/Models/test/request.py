from typing import Optional

from pydantic import BaseModel, ConfigDict

from ..calculate_hit.gear import GearInput
from ..calculate_hit.monster import MonsterInput


class TestInput(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    loadout: str = "OathTorvaRancour"
    weapon: str = "Scythe of Vitur"
    monster: MonsterInput = MonsterInput(
        Name="Bloat",
        ReduceDefense=False,
    )
    scale: int = 5
    gear_input: Optional[GearInput] = None
    player_levels: Optional[dict] = None
