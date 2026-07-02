from pydantic import BaseModel, ConfigDict


class TestOutput(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    message: str
    monster_alive: bool
    hits_to_kill: int
    final_damage: int
