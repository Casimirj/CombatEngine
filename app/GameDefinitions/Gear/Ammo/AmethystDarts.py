from app.GearItem import Gear
from app.Enums.gear_slot import GearSlot
from app.Registries.GearRegistry import GearRegistry


class AmethystDarts(Gear):
    name = "Amethyst darts"
    slot = GearSlot.AMMO
    aliases = ["amethyst darts", "amethyst dart", "ame darts"]
    ammo_category = "darts"

    def build(self) -> dict:
        return {
            "ranged_strength_bonus": 28,
        }


GearRegistry.register(AmethystDarts())
