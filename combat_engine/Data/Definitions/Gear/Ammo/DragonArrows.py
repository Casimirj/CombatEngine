from combat_engine.Domain.Enums.AmmoType import AmmoType
from combat_engine.Domain.GearItem import Gear
from combat_engine.Domain.Enums.GearSlot import GearSlot
from combat_engine.Data.Registries.GearRegistry import GearRegistry


class DragonArrows(Gear):
    name = "Dragon arrows"
    slot = GearSlot.AMMO
    aliases = ["dragon arrows", "dragon arrow"]
    ammo_category = AmmoType.ARROWS

    def build(self) -> dict:
        return {
            "ranged_strength_bonus": 60,
        }


GearRegistry.register(DragonArrows())
