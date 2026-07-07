from combat_engine.Domain.Loadout import Loadout
from combat_engine.Data.Registries.LoadoutRegistry import LoadoutRegistry


class VoidRangedQuiverAnguish(Loadout):
    name = "VoidRangedQuiverAnguish"
    aliases = ['void range', 'void ranged', 'void anguish']

    def build(self):
        return Loadout(gear_names=[
            'Void ranger helm',
            "Dizana's quiver",
            'Necklace of anguish',
            'Elite void top',
            'Elite void robe',
            'Void knight gloves',
        ], name=self.name).build()


LoadoutRegistry.register(VoidRangedQuiverAnguish())
