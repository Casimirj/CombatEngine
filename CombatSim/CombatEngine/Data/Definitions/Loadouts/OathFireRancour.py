from CombatSim.CombatEngine.Domain.Loadout import Loadout
from CombatSim.CombatEngine.Data.Registries.LoadoutRegistry import LoadoutRegistry


class OathFireRancour(Loadout):
    name = "OathFireRancour"
    aliases = ['fire rancour', 'infernal rancour']

    def build(self):
        return Loadout(gear_names=[
            'Oathplate helm',
            'Fire cape',
            'Amulet of rancour',
            'Oathplate body',
            'Oathplate legs',
            'Ferocious gloves',
            'Primordial boots',
            'Berserker ring (i)',
            'Avernic defender',
        ], name=self.name).build()


LoadoutRegistry.register(OathFireRancour())
