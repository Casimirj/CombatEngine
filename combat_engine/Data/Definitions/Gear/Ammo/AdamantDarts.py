from combat_engine.Domain.Enums.AmmoType import AmmoType
from combat_engine.Domain.GearItem import Gear
from combat_engine.Domain.Enums.GearSlot import GearSlot
from combat_engine.Data.Registries.GearRegistry import GearRegistry


class AdamantDarts(Gear):
    name = "Adamant darts"
    slot = GearSlot.AMMO
    aliases = ["adamant darts", "adamant dart", "addy darts", "add darts"]
    ammo_category = AmmoType.DARTS

    def build(self) -> dict:
        return {
            "ranged_strength_bonus": 17,
        }


GearRegistry.register(AdamantDarts())
