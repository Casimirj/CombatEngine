from CombatSim.CombatEngine.Domain.Enums.AmmoType import AmmoType
from CombatSim.CombatEngine.Domain.GearItem import Gear
from CombatSim.CombatEngine.Domain.Enums.GearSlot import GearSlot
from CombatSim.CombatEngine.Data.Registries.GearRegistry import GearRegistry


class RuneArrows(Gear):
    name = "Rune arrows"
    slot = GearSlot.AMMO
    aliases = ["rune arrows", "rune arrow"]
    ammo_category = AmmoType.ARROWS

    def build(self) -> dict:
        return {
            "ranged_strength_bonus": 49,
        }


GearRegistry.register(RuneArrows())
