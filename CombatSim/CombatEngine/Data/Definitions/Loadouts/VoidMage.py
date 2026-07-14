from CombatSim.CombatEngine.Domain.Loadout import Loadout
from CombatSim.CombatEngine.Data.Registries.LoadoutRegistry import LoadoutRegistry
from CombatSim.CombatEngine.Data.Registries.PotionRegistry import PotionRegistry
from CombatSim.CombatEngine.Data.Registries.PrayerRegistry import PrayerRegistry
from CombatSim.CombatEngine.Domain.Player import Player
from CombatSim.CombatEngine.Domain.Stats import Stats


class VoidMage(Loadout):
    name = "VoidMage"
    aliases = ['void mage', 'void magic']

    def build(self):
        loadout = Loadout(gear_names=[
            'Void mage helm',
            'Imbued saradomin cape',
            'Occult necklace',
            'Elite void top',
            'Elite void robe',
            'Void knight gloves',
            'Ward of elidinis (f)',
            'Magus ring',
        ], name=self.name)
        levels = Stats({"hp_level": 99, "attack_level": 99, "strength_level": 99,
                        "def_level": 99, "magic_level": 99, "ranged_level": 99, "prayer_level": 99})
        level_dict = {k: v for k, v in vars(levels).items() if k in Stats.LEVEL_KEYS}
        return Player(
            stats=level_dict,
            loadout=loadout,
            boosts=[PotionRegistry.get("IMBUED_HEART")],
            prayer=PrayerRegistry.get("AUGURY"),
        )


LoadoutRegistry.register(VoidMage())
