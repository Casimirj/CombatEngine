"""NyloBoss attack schedule variant that uses Tumeken's Shadow on mage phase.

Compared to the standard Ayak schedule:
  - Mage phase:  2× Tumeken's Shadow instead of 3× Eye of Ayak
  - Ranged (after mage): falls straight to regular TBow → TBow (no blowpipe switch)
  - All other phases (melee, first ranged ZCB→TBow, regular ranged) are identical.
"""

from dataclasses import dataclass, field
from typing import List

from CombatSim.Simulations.shared.AttackSchedule import Attack, AttackSchedule, Setup, DynamicAttack
from CombatSim.Simulations.nyloboss.phases import NyloBossPhase
from CombatSim.Simulations.nyloboss.NyloRoom import NyloRoom
from CombatSim.Simulations.nyloboss.NyloRole import NyloRole

from CombatSim.CombatEngine.Data.Definitions.Weapons.Scythe import Scythe
from CombatSim.CombatEngine.Data.Definitions.Weapons.Bgs import Bgs
from CombatSim.CombatEngine.Data.Definitions.Weapons.DragonClaws import DragonClaws
from CombatSim.CombatEngine.Data.Definitions.Weapons.TwistedBow import TwistedBow
from CombatSim.CombatEngine.Data.Definitions.Weapons.ZaryteCrossbow import ZaryteCrossbow
from CombatSim.CombatEngine.Data.Definitions.Weapons.TumekensShadow import TumekensShadow


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
    "mage_shadow": Setup(
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


# ── Defense threshold for backup BGS to Claws switch ────────────────────────


_BACKUP_BGS_DEFENSE_THRESHOLD = 20


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
        DynamicAttack(),
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
    "mage": [
        Attack(TumekensShadow, setup=SETUPS["mage_shadow"]),
        Attack(TumekensShadow),
    ],
}


@dataclass(kw_only=True)
class NyloBossShadowAttackSchedule(AttackSchedule):
    """NyloBoss attack schedule variant that uses Shadow on mage.

    Compared to the standard Ayak schedule:
      - Mage phase:  2× Tumeken's Shadow instead of 3× Eye of Ayak
      - No special ranged-after-mage phase — goes straight to regular TBow→TBow
      - All other phases (melee, first ranged, regular ranged) are identical.
    """

    role: NyloRole
    name: str = "NyloBossShadow"
    rotation: List[Attack] = field(default_factory=list)

    def update_rotation(self, room: NyloRoom) -> None:
        phase = room.phase

        if phase == NyloBossPhase.MELEE:
            if room.first_melee:
                if self.role == NyloRole.BGS:
                    self.rotation = list(ROTATIONS["bgs_first_melee"])
                elif self.role == NyloRole.CLAWS:
                    self.rotation = list(ROTATIONS["claws_first_melee"])
                elif self.role == NyloRole.BACKUP_BGS:
                    self.rotation = list(ROTATIONS["backup_bgs_melee"])
                else:
                    self.rotation = list(ROTATIONS["repeat_melee"])
            else:
                if self.role == NyloRole.BACKUP_BGS:
                    self.rotation = list(ROTATIONS["backup_bgs_melee"])
                else:
                    self.rotation = list(ROTATIONS["repeat_melee"])
        elif phase == NyloBossPhase.RANGED:
            if room.first_ranged:
                self.rotation = list(ROTATIONS["first_ranged"])
            else:
                self.rotation = list(ROTATIONS["regular_ranged"])
        else:
            self.rotation = list(ROTATIONS["mage"])

    def get_next_attack(self, idx: int, room: NyloRoom) -> Attack:
        attack = self.rotation[idx]

        if not isinstance(attack, DynamicAttack):
            return attack

        if self.role == NyloRole.BACKUP_BGS and idx == 1:
            if room.boss_defense > _BACKUP_BGS_DEFENSE_THRESHOLD:
                return Attack(Bgs, setup=SETUPS["melee"], use_special_attack=True)
            else:
                return Attack(DragonClaws, setup=SETUPS["melee"], use_special_attack=True)

        return attack
