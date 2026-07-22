from dataclasses import dataclass, field
from typing import List, Type

from CombatSim.CombatEngine.Domain.Weapon import Weapon

from CombatSim.Simulations.shared.AttackSchedule import Attack, AttackSchedule, Setup
from CombatSim.Simulations.nyloboss.phases import NyloBossPhase
from CombatSim.Simulations.nyloboss.NyloRoomState import NyloRoomState
from CombatSim.Simulations.nyloboss.NyloRole import NyloRole

from CombatSim.CombatEngine.Data.Definitions.Weapons.Scythe import Scythe
from CombatSim.CombatEngine.Data.Definitions.Weapons.Bgs import Bgs
from CombatSim.CombatEngine.Data.Definitions.Weapons.DragonClaws import DragonClaws
from CombatSim.CombatEngine.Data.Definitions.Weapons.TwistedBow import TwistedBow
from CombatSim.CombatEngine.Data.Definitions.Weapons.EyeOfAyak import EyeOfAyak
from CombatSim.CombatEngine.Data.Definitions.Weapons.ToxicBlowpipe import ToxicBlowpipe
from CombatSim.CombatEngine.Data.Definitions.Weapons.ZaryteCrossbow import ZaryteCrossbow


# ── Phase Setups ────────────────────────────────────────────────────────────

MELEE_SETUP = Setup(
    pieces=[
        'Torva full helm',
        'Infernal cape',
        'Amulet of rancour',
        'Oathplate body',
        'Oathplate legs',
        'Ferocious gloves',
        'Avernic treads',
        'Ultor ring',
    ],
    prayer="piety",
    boosts=["super_combat"],
)

RANGED_TBOW_SETUP = Setup(
    pieces=[
        'Void ranger helm',
        "Dizana's quiver",
        'Necklace of rupture',
        'Elite void top',
        'Elite void robe',
        'Void knight gloves',
        'Avernic treads',
        'Venator ring',
        'seeking dragon arrows',
    ],
    prayer="rigour",
    boosts=["bastion"],
)

RANGED_BLOWPIPE_SETUP = Setup(
    pieces=[
        'Void ranger helm',
        "Dizana's quiver",
        'Necklace of rupture',
        'Elite void top',
        'Elite void robe',
        'Void knight gloves',
        'Avernic treads',
        'Venator ring',
        'Dragon darts',
    ],
    prayer="rigour",
    boosts=["bastion"],
)

MAGE_SETUP = Setup(
    pieces=[
        'Ancestral hat',
        'Imbued saradomin cape',
        'Occult necklace',
        'Ancestral robe top',
        'Ancestral robe bottom',
        'Confliction gauntlets',
        'Avernic treads',
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

_BACKUP_BGS_MELEE = [
    Attack(Scythe, setup=MELEE_SETUP),
    Attack(Bgs, use_special_attack=True),
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


@dataclass(kw_only=True)
class NyloBossAttackSchedule(AttackSchedule):
    """Per-player attack schedule that dynamically updates based on the boss phase."""

    role: NyloRole
    name: str = "NyloBoss"
    rotation: List[Attack] = field(default_factory=list)

    def update_rotation(self, room_state: NyloRoomState) -> None:
        """Rebuild the rotation for the current boss phase and room state."""
        phase = room_state.phase

        if phase == NyloBossPhase.MELEE:
            if room_state.first_melee:
                if self.role == NyloRole.BGS:
                    self.rotation = list(_BGS_FIRST_MELEE)
                elif self.role == NyloRole.CLAWS:
                    self.rotation = list(_CLAWS_FIRST_MELEE)
                elif self.role == NyloRole.BACKUP_BGS:
                    self.rotation = list(_BACKUP_BGS_MELEE)
                else:
                    self.rotation = list(_REPEAT_MELEE)
            else:
                self.rotation = list(_REPEAT_MELEE)
        elif phase == NyloBossPhase.RANGED:
            if room_state.first_ranged:
                self.rotation = list(_FIRST_RANGED)
            elif room_state.prev_phase == NyloBossPhase.MAGE:
                self.rotation = list(_RANGED_AFTER_MAGE)
            else:
                self.rotation = list(_REGULAR_RANGED)
        else:
            self.rotation = list(_MAGE)
