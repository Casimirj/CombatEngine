from CombatSim.CombatEngine.Domain.Enums.AmmoType import AmmoType
from CombatSim.CombatEngine.Domain.GearItem import Gear
from CombatSim.CombatEngine.Domain.Enums.GearSlot import GearSlot
from CombatSim.CombatEngine.Data.Registries.GearRegistry import GearRegistry


class DragonSeekingArrows(Gear):
    name = "Seeking dragon arrows"
    slot = GearSlot.AMMO
    aliases = ["seeking dragon arrows", "seeking dragon arrow",
               "dragon seeking arrows", "dragon seeking arrow",
               "dseeking", "dseeking arrows"]
    ammo_category = AmmoType.ARROWS
    min_hit = 3

    def build(self) -> dict:
        return {
            "ranged_attack_bonus": 20,
            "ranged_strength_bonus": 60,
        }


GearRegistry.register(DragonSeekingArrows())
