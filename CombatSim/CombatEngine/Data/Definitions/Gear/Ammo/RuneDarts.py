from CombatSim.CombatEngine.Domain.Enums.AmmoType import AmmoType
from CombatSim.CombatEngine.Domain.GearItem import Gear
from CombatSim.CombatEngine.Domain.Enums.GearSlot import GearSlot
from CombatSim.CombatEngine.Data.Registries.GearRegistry import GearRegistry


class RuneDarts(Gear):
    name = "Rune darts"
    slot = GearSlot.AMMO
    aliases = ["rune darts", "rune dart"]
    ammo_category = AmmoType.DARTS

    def build(self) -> dict:
        return {
            "ranged_strength_bonus": 26,
        }


GearRegistry.register(RuneDarts())
