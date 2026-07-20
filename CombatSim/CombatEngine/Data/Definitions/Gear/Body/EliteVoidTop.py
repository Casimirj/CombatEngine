from CombatSim.CombatEngine.Domain.GearItem import Gear
from CombatSim.CombatEngine.Domain.Enums.GearSlot import GearSlot
from CombatSim.CombatEngine.Data.Registries.GearRegistry import GearRegistry


class EliteVoidTop(Gear):
    name = "Elite void top"
    slot = GearSlot.BODY
    aliases = ["elite void top", "void top", "elite void body"]

    def build(self) -> dict:
        return {
            "stab_attack_bonus":  0,
            "slash_attack_bonus":  0,
            "crush_attack_bonus":  0,
            "magic_attack_bonus":  0,
            "ranged_attack_bonus":  0,
            "melee_strength_bonus":  0,
            "ranged_strength_bonus":  0,
            "magic_strength_bonus":  0,
            "stab_def":  45,
            "slash_def":  45,
            "crush_def":  45,
            "magic_def":  45,
            "ranged_def_light":  45,
            "ranged_def_med":  45,
            "prayer_bonus": 3,
            "ranged_def_heavy":  45}


GearRegistry.register(EliteVoidTop())

