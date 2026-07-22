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

SETUPS = {
    "melee": Setup(
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
    ),
    "ranged_tbow": Setup(
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
    ),
    "ranged_blowpipe": Setup(
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
    ),
    "mage": Setup(
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
    ),
}



# ── Rotation definitions ────────────────────────────────────────────────────

ROTATIONS = {
    "bgs_first_melee": [
        Attack(Bgs, setup=SETUPS["melee"], use_special_attack=True),
        Attack(Scythe),
    ],
    "claws_first_melee": [
        Attack(DragonClaws, setup=SETUPS["melee"], use_special_attack=True),
        Attack(Scythe),
    ],
    "backup_bgs_melee": [
        Attack(Scythe, setup=SETUPS["melee"]),
        Attack(Bgs, use_special_attack=True),
    ],
    "repeat_melee": [
        Attack(Scythe, setup=SETUPS["melee"]),
        Attack(Scythe),
    ],
    "first_ranged": [
        Attack(ZaryteCrossbow, setup=SETUPS["ranged_tbow"], use_special_attack=True),
        Attack(TwistedBow),
    ],
    "regular_ranged": [
        Attack(TwistedBow, setup=SETUPS["ranged_tbow"]),
        Attack(TwistedBow),
    ],
    "ranged_after_mage": [
        Attack(ToxicBlowpipe, setup=SETUPS["ranged_blowpipe"]),
        Attack(ToxicBlowpipe),
        Attack(ToxicBlowpipe),
        Attack(TwistedBow, setup=SETUPS["ranged_tbow"]),
    ],
    "mage": [
        Attack(EyeOfAyak, setup=SETUPS["mage"]),
        Attack(EyeOfAyak),
        Attack(EyeOfAyak),
    ],
}


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
                    self.rotation = list(ROTATIONS["bgs_first_melee"])
                elif self.role == NyloRole.CLAWS:
                    self.rotation = list(ROTATIONS["claws_first_melee"])
                elif self.role == NyloRole.BACKUP_BGS:
                    self.rotation = list(ROTATIONS["backup_bgs_melee"])
                else:
                    self.rotation = list(ROTATIONS["repeat_melee"])
            else:
                self.rotation = list(ROTATIONS["repeat_melee"])
        elif phase == NyloBossPhase.RANGED:
            if room_state.first_ranged:
                self.rotation = list(ROTATIONS["first_ranged"])
            elif room_state.prev_phase == NyloBossPhase.MAGE:
                self.rotation = list(ROTATIONS["ranged_after_mage"])
            else:
                self.rotation = list(ROTATIONS["regular_ranged"])
        else:
            self.rotation = list(ROTATIONS["mage"])
