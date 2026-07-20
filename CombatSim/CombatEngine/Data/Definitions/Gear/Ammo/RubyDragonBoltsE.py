from CombatSim.CombatEngine.Domain.Enums.AmmoType import AmmoType
from CombatSim.CombatEngine.Domain.GearItem import Gear
from CombatSim.CombatEngine.Domain.Enums.GearSlot import GearSlot
from CombatSim.CombatEngine.Data.Registries.GearRegistry import GearRegistry


class RubyDragonBoltsE(Gear):
    name = "Ruby dragon bolts (e)"
    slot = GearSlot.AMMO
    aliases = ["ruby dragon bolts (e)", "ruby bolts (e)", "ruby dragon bolts e", "ruby bolts e"]
    ammo_category = AmmoType.BOLTS

    def build(self) -> dict:
        return {
            "ranged_strength_bonus": 122,
        }


GearRegistry.register(RubyDragonBoltsE())
