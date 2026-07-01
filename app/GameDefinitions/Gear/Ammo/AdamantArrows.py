from app.GearItem import Gear
from app.Enums.gear_slot import GearSlot
from app.Registries.GearRegistry import GearRegistry


class AdamantArrows(Gear):
    name = "Adamant arrows"
    slot = GearSlot.AMMO
    aliases = ["adamant arrows", "adamant arrow", "addy arrows", "add arrows"]
    ammo_category = "arrows"

    def build(self) -> dict:
        return {
            "ranged_strength_bonus": 31,
        }


GearRegistry.register(AdamantArrows())
