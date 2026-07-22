from CombatSim.CombatEngine.Domain.Enums.AmmoType import AmmoType
from CombatSim.CombatEngine.Domain.GearItem import Gear
from CombatSim.CombatEngine.Domain.Enums.GearSlot import GearSlot
from CombatSim.CombatEngine.Data.Registries.GearRegistry import GearRegistry


class SeekingAmethystArrows(Gear):
    name = "Seeking amethyst arrows"
    slot = GearSlot.AMMO
    aliases = ["seeking amethyst arrows", "seeking amethyst arrow",
               "s amethyst", "seeking ame", "seeking ame arrows"]
    ammo_category = AmmoType.ARROWS
    min_hit = 3

    def build(self) -> dict:
        return {
            "ranged_attack_bonus": 20,
            "ranged_strength_bonus": 55,
        }


GearRegistry.register(SeekingAmethystArrows())
