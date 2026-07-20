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


# ── Phase Setup ─────────────────────────────────────────────────────────────

from dataclasses import dataclass, field


@dataclass
class Setup:
    """Bundles gear pieces, prayer, and boosts for a single phase."""
    pieces: List[str]
    prayer: str
    boosts: List[str] = field(default_factory=list)


# ── Weapons ─────────────────────────────────────────────────────────────────

from CombatSim.CombatEngine.Data.Definitions.Weapons.Scythe import Scythe
from CombatSim.CombatEngine.Data.Definitions.Weapons.Bgs import Bgs
from CombatSim.CombatEngine.Data.Definitions.Weapons.DragonClaws import DragonClaws
from CombatSim.CombatEngine.Data.Definitions.Weapons.TwistedBow import TwistedBow
from CombatSim.CombatEngine.Data.Definitions.Weapons.EyeOfAyak import EyeOfAyak
from CombatSim.CombatEngine.Data.Definitions.Weapons.ToxicBlowpipe import ToxicBlowpipe
from CombatSim.CombatEngine.Data.Definitions.Weapons.ZaryteCrossbow import ZaryteCrossbow


# ── Phase Setups ────────────────────────────────────────────────────────────

melee_setup = Setup(
    pieces=[
        'Torva full helm',
        'Infernal cape',
        'Salve (e)',
        'Torva platebody',
        'Torva platelegs',
        'Ferocious gloves',
        'Primordial boots',
        'Berserker ring (i)',
        'Avernic defender',
    ],
    prayer="piety",
    boosts=["super_combat"],
)

ranged_setup = Setup(
    pieces=[
        'Void ranger helm',
        "Dizana's quiver",
        'Necklace of anguish',
        'Elite void top',
        'Elite void robe',
        'Void knight gloves',
        'Amethyst arrows',
    ],
    prayer="rigour",
    boosts=["bastion"],
)

ranged_after_mage_setup = Setup(
    pieces=[
        'Void ranger helm',
        "Dizana's quiver",
        'Necklace of anguish',
        'Elite void top',
        'Elite void robe',
        'Void knight gloves',
        'Dragon darts',
    ],
    prayer="rigour",
    boosts=["bastion"],
)

mage_setup = Setup(
    pieces=[
        'Void mage helm',
        'Imbued saradomin cape',
        'Occult necklace',
        'Elite void top',
        'Elite void robe',
        'Void knight gloves',
        'Ward of elidinis (f)',
        'Magus ring',
    ],
    prayer="augury",
    boosts=["imbued_heart"],
)


# ── Attack Schedules ────────────────────────────────────────────────────────

FIRST_MELEE = NyloAttackSchedule("First Melee", [
    (Bgs, True),
    (Scythe, False),
    (Scythe, False),
])

MELEE = NyloAttackSchedule("Melee", [
    (Scythe, False),
    (Scythe, False),
])

FIRST_RANGED = NyloAttackSchedule("First Ranged (ZCB)", [
    (ZaryteCrossbow, True),
    (TwistedBow, False),
])

RANGED = NyloAttackSchedule("Ranged", [
    (TwistedBow, False),
    (TwistedBow, False),
])

RANGED_AFTER_MAGE = NyloAttackSchedule("Ranged (after mage)", [
    (ToxicBlowpipe, False),
    (ToxicBlowpipe, False),
    (ToxicBlowpipe, False),
    (TwistedBow, False),
])

MAGE = NyloAttackSchedule("Mage", [
    (EyeOfAyak, False),
    (EyeOfAyak, False),
    (EyeOfAyak, False),
])

# ── Claws-first variants ────────────────────────────────────────────────────

FIRST_MELEE_CLAWS = NyloAttackSchedule("First Melee (Claws)", [
    (DragonClaws, True),
    (Scythe, False),
    (Scythe, False),
])

MELEE_CLAWS = NyloAttackSchedule("Melee (Claws)", [
    (Scythe, False),
    (Scythe, False),
])


# ── Schedule-Dispatch Functions ─────────────────────────────────────────────

def schedule_for_phase(
    phase: NyloBossPhase,
    first_melee: bool,
    prev_phase: "NyloBossPhase | None" = None,
    first_ranged: bool = True,
) -> NyloAttackSchedule:
    """Return the BGS-first attack schedule for the given phase."""
    if phase == NyloBossPhase.MELEE:
        return FIRST_MELEE if first_melee else MELEE
    elif phase == NyloBossPhase.RANGED:
        if first_ranged:
            return FIRST_RANGED
        if prev_phase == NyloBossPhase.MAGE:
            return RANGED_AFTER_MAGE
        return RANGED
    else:
        return MAGE


def schedule_for_phase_claws(
    phase: NyloBossPhase,
    first_melee: bool,
    prev_phase: "NyloBossPhase | None" = None,
    first_ranged: bool = True,
) -> NyloAttackSchedule:
    """Return the Claws-first attack schedule for the given phase."""
    if phase == NyloBossPhase.MELEE:
        return FIRST_MELEE_CLAWS if first_melee else MELEE_CLAWS
    elif phase == NyloBossPhase.RANGED:
        if first_ranged:
            return FIRST_RANGED
        if prev_phase == NyloBossPhase.MAGE:
            return RANGED_AFTER_MAGE
        return RANGED
    else:
        return MAGE
