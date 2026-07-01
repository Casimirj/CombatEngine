from app.GearItem import Gear
from app.Enums.gear_slot import GearSlot
from app.Registries.GearRegistry import GearRegistry


class AmethystArrows(Gear):
    name = "Amethyst arrows"
    slot = GearSlot.AMMO
    aliases = ["amethyst arrows", "amethyst arrow", "ame arrows"]
    ammo_category = "arrows"

    def build(self) -> dict:
        return {
            "ranged_strength_bonus": 55,
        }


GearRegistry.register(AmethystArrows())
