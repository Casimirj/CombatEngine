from CombatSim.CombatEngine.Domain.Loadout import Loadout
from CombatSim.CombatEngine.Data.Registries.LoadoutRegistry import LoadoutRegistry
from CombatSim.CombatEngine.Data.Registries.PotionRegistry import PotionRegistry
from CombatSim.CombatEngine.Data.Registries.PrayerRegistry import PrayerRegistry
from CombatSim.CombatEngine.Domain.Player import Player
from CombatSim.CombatEngine.Domain.Stats import Stats


class VoidRangedQuiverAnguish(Loadout):
    name = "VoidRangedQuiverAnguish"
    aliases = ['void range', 'void ranged', 'void anguish']

    def build(self):
        loadout = Loadout(gear_names=[
            'Void ranger helm',
            "Dizana's quiver",
            'Necklace of anguish',
            'Elite void top',
            'Elite void robe',
            'Void knight gloves',
        ], name=self.name)
        levels = Stats({"hp_level": 99, "attack_level": 99, "strength_level": 99,
                        "def_level": 99, "magic_level": 99, "ranged_level": 99, "prayer_level": 99})
        level_dict = {k: v for k, v in vars(levels).items() if k in Stats.LEVEL_KEYS}
        return Player(
            stats=level_dict,
            loadout=loadout,
            boosts=[PotionRegistry.get("SUPER_COMBAT")],
            prayer=PrayerRegistry.get("PIETY"),
        )


LoadoutRegistry.register(VoidRangedQuiverAnguish())
