from CombatSim.CombatEngine.Domain.GearItem import Gear
from CombatSim.CombatEngine.Domain.Enums.GearSlot import GearSlot
from CombatSim.CombatEngine.Data.Registries.GearRegistry import GearRegistry


class InfernalCape(Gear):
    name = "Infernal cape"
    slot = GearSlot.CAPE
    aliases = ["infernal cape", "inferno cape", "inf cape"]

    def build(self) -> dict:
        return {
            "stab_attack_bonus":  4,
            "slash_attack_bonus":  4,
            "crush_attack_bonus":  4,
            "magic_attack_bonus":  1,
            "ranged_attack_bonus":  1,
            "melee_strength_bonus":  8,
            "ranged_strength_bonus":  0,
            "magic_strength_bonus":  0,
            "stab_def":  12,
            "slash_def":  12,
            "crush_def":  12,
            "magic_def":  12,
            "ranged_def_light":  12,
            "ranged_def_med":  12,
            "prayer_bonus": 2,
            "ranged_def_heavy":  12}


GearRegistry.register(InfernalCape())

