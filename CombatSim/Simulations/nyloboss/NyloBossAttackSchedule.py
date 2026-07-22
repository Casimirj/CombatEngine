from dataclasses import dataclass, field
from enum import Enum
from typing import List, Type

from CombatSim.CombatEngine.Domain.Weapon import Weapon

from CombatSim.Simulations.shared.AttackSchedule import Attack, AttackSchedule, Setup
from CombatSim.Simulations.nyloboss.phases import NyloBossPhase
from CombatSim.Simulations.nyloboss.NyloRoomState import NyloRoomState

from CombatSim.CombatEngine.Data.Definitions.Weapons.Scythe import Scythe
from CombatSim.CombatEngine.Data.Definitions.Weapons.Bgs import Bgs
from CombatSim.CombatEngine.Data.Definitions.Weapons.DragonClaws import DragonClaws
from CombatSim.CombatEngine.Data.Definitions.Weapons.TwistedBow import TwistedBow
from CombatSim.CombatEngine.Data.Definitions.Weapons.EyeOfAyak import EyeOfAyak
from CombatSim.CombatEngine.Data.Definitions.Weapons.ToxicBlowpipe import ToxicBlowpipe
from CombatSim.CombatEngine.Data.Definitions.Weapons.ZaryteCrossbow import ZaryteCrossbow


class NyloRole(Enum):
    BGS = "bgs"
    CLAWS = "claws"
    BACKUP_BGS = "backup_bgs"


# ── Phase Setups ────────────────────────────────────────────────────────────

MELEE_SETUP = Setup(
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

RANGED_TBOW_SETUP = Setup(
    pieces=[
        'Void ranger helm',
        "Dizana's quiver",
        'Necklace of anguish',
        'Elite void top',
        'Elite void robe',
        'Void knight gloves',
        'Dragon arrows',
    ],
    prayer="rigour",
    boosts=["bastion"],
)

RANGED_BLOWPIPE_SETUP = Setup(
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

MAGE_SETUP = Setup(
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


# ── Rotation definitions ────────────────────────────────────────────────────

_BGS_FIRST_MELEE = [
    Attack(Bgs, setup=MELEE_SETUP, use_special_attack=True),
    Attack(Scythe),
]

_CLAWS_FIRST_MELEE = [
    Attack(DragonClaws, setup=MELEE_SETUP, use_special_attack=True),
    Attack(Scythe),
]

_BACKUP_BGS_CHECK_MELEE = [
    Attack(Bgs, setup=MELEE_SETUP, use_special_attack=True),
    Attack(Scythe),
]

_REPEAT_MELEE = [
    Attack(Scythe, setup=MELEE_SETUP),
    Attack(Scythe),
]

_FIRST_RANGED = [
    Attack(ZaryteCrossbow, setup=RANGED_TBOW_SETUP, use_special_attack=True),
    Attack(TwistedBow),
]

_REGULAR_RANGED = [
    Attack(TwistedBow, setup=RANGED_TBOW_SETUP),
    Attack(TwistedBow),
]

_RANGED_AFTER_MAGE = [
    Attack(ToxicBlowpipe, setup=RANGED_BLOWPIPE_SETUP),
    Attack(ToxicBlowpipe),
    Attack(ToxicBlowpipe),
    Attack(TwistedBow, setup=RANGED_TBOW_SETUP),
]

_MAGE = [
    Attack(EyeOfAyak, setup=MAGE_SETUP),
    Attack(EyeOfAyak),
    Attack(EyeOfAyak),
]


@dataclass
class NyloBossAttackSchedule(AttackSchedule):
    """Per-player attack schedule that dynamically updates based on the boss phase."""

    role: NyloRole
    name: str = field(default="NyloBoss", init=False)
    rotation: List[Attack] = field(default_factory=list, init=False)

    def __post_init__(self):
        pass

    def update_rotation(self, room_state: NyloRoomState) -> None:
        """Rebuild the rotation for the current boss phase and room state."""
        phase = room_state.phase

        if phase == NyloBossPhase.MELEE:
            if room_state.first_melee:
                if self.role == NyloRole.BGS:
                    self.rotation = _BGS_FIRST_MELEE
                elif self.role == NyloRole.CLAWS:
                    self.rotation = _CLAWS_FIRST_MELEE
                elif self.role == NyloRole.BACKUP_BGS:
                    if room_state.boss_defense >= 30:
                        self.rotation = _BACKUP_BGS_CHECK_MELEE
                    else:
                        self.rotation = _REPEAT_MELEE
                else:
                    self.rotation = _REPEAT_MELEE
            else:
                self.rotation = _REPEAT_MELEE
        elif phase == NyloBossPhase.RANGED:
            if room_state.first_ranged:
                self.rotation = _FIRST_RANGED
            elif room_state.prev_phase == NyloBossPhase.MAGE:
                self.rotation = _RANGED_AFTER_MAGE
            else:
                self.rotation = _REGULAR_RANGED
        else:
            self.rotation = _MAGE
