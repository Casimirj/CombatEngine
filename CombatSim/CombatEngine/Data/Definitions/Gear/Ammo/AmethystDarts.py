from CombatSim.CombatEngine.Domain.Enums.AmmoType import AmmoType
from CombatSim.CombatEngine.Domain.GearItem import Gear
from CombatSim.CombatEngine.Domain.Enums.GearSlot import GearSlot
from CombatSim.CombatEngine.Data.Registries.GearRegistry import GearRegistry


class AmethystDarts(Gear):
    name = "Amethyst darts"
    slot = GearSlot.AMMO
    aliases = ["amethyst darts", "amethyst dart", "ame darts"]
    ammo_category = AmmoType.DARTS

    def build(self) -> dict:
        return {
            "ranged_strength_bonus": 28,
        }


GearRegistry.register(AmethystDarts())
