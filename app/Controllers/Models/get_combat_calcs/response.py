from pydantic import BaseModel, ConfigDict


class PlayerStats(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    attack_level: int
    strength_level: int
    defence_level: int
    ranged_level: int
    magic_level: int
    hitpoints_level: int

    stab_attack_bonus: int
    slash_attack_bonus: int
    crush_attack_bonus: int
    magic_attack_bonus: int
    ranged_attack_bonus: int

    melee_strength_bonus: int
    ranged_strength_bonus: int
    magic_strength_bonus: int

    stab_defence_bonus: int
    slash_defence_bonus: int
    crush_defence_bonus: int
    magic_defence_bonus: int


class PlayerGear(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    weapon_name: str
    weapon_attack_style: str
    weapon_attack_type: str


class PlayerSetup(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    prayer: str
    boosts: list[str]
    wearing_salve: bool


class PlayerInfo(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    stats: PlayerStats
    gear: PlayerGear
    setup: PlayerSetup


class GetCombatCalcsOutput(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    player: PlayerInfo
    effective_attack_level: int
    effective_strength_level: int
    effective_defence_level: int
    effective_ranged_attack_level: int
    effective_ranged_strength_level: int
    effective_magic_level: int
    max_hit: int
    player_attack_roll: int
    player_defence_roll: int
    npc_defence_roll: int
    hit_chance: float
