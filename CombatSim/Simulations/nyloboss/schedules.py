from typing import List, Tuple, Type

from CombatSim.CombatEngine.Domain.Weapon import Weapon
from CombatSim.Simulations.nyloboss.phases import NyloBossPhase


class NyloAttackSchedule:
    """A named sequence of (weapon_class, use_special) pairs for a boss phase."""

    name: str
    rotation: List[Tuple[Type[Weapon], bool]]

    def __init__(self, name: str, rotation: List[Tuple[Type[Weapon], bool]]):
        if not name:
            raise ValueError("AttackSchedule name cannot be empty")
        if not rotation:
            raise ValueError("AttackSchedule rotation cannot be empty")
        self.name = name
        self.rotation = rotation

    def __len__(self) -> int:
        return len(self.rotation)

    def __getitem__(self, index: int) -> Tuple[Type[Weapon], bool]:
        return self.rotation[index]

    def __repr__(self) -> str:
        return f"NyloAttackSchedule(name={self.name!r}, len={len(self.rotation)})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, NyloAttackSchedule):
            return NotImplemented
        return self.name == other.name and self.rotation == other.rotation


# ── Concrete Attack Schedules ───────────────────────────────────────────────

from CombatSim.CombatEngine.Data.Definitions.Weapons.Scythe import Scythe
from CombatSim.CombatEngine.Data.Definitions.Weapons.Bgs import Bgs
from CombatSim.CombatEngine.Data.Definitions.Weapons.TwistedBow import TwistedBow
from CombatSim.CombatEngine.Data.Definitions.Weapons.EyeOfAyak import EyeOfAyak

FIRST_MELEE = NyloAttackSchedule("First Melee", [
    (Bgs, True),
    (Scythe, False),
])

MELEE = NyloAttackSchedule("Melee", [
    (Scythe, False),
    (Scythe, False),
])

RANGED = NyloAttackSchedule("Ranged", [
    (TwistedBow, False),
    (TwistedBow, False),
])

MAGE = NyloAttackSchedule("Mage", [
    (EyeOfAyak, False),
    (EyeOfAyak, False),
    (EyeOfAyak, False),
])


def schedule_for_phase(phase: NyloBossPhase, first_melee: bool) -> NyloAttackSchedule:
    """Return the appropriate attack schedule for the given phase."""
    if phase == NyloBossPhase.MELEE:
        return FIRST_MELEE if first_melee else MELEE
    elif phase == NyloBossPhase.RANGED:
        return RANGED
    else:
        return MAGE
