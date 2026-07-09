from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator


class MonsterInput(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    name: str = Field(alias="Name")
    reduce_defense: bool = Field(alias="ReduceDefense")
    defense: Optional[int] = Field(default=None, alias="Defense")

    @model_validator(mode="after")
    def validate_defense(self) -> "MonsterInput":
        if self.reduce_defense and self.defense is None:
            raise ValueError("Defense is required when ReduceDefense is true")
        return self
