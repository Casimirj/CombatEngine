from app.GearItem import Gear
from app.Enums.gear_slot import GearSlot
from app.Registries.GearRegistry import GearRegistry


class AdamantDarts(Gear):
    name = "Adamant darts"
    slot = GearSlot.AMMO
    aliases = ["adamant darts", "adamant dart", "addy darts", "add darts"]
    ammo_category = "darts"

    def build(self) -> dict:
        return {
            "ranged_strength_bonus": 17,
        }


GearRegistry.register(AdamantDarts())
