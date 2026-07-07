from combat_engine.Domain.Loadout import Loadout
from combat_engine.Data.Registries.LoadoutRegistry import LoadoutRegistry


class OathFireSalve(Loadout):
    name = "OathFireSalve"
    aliases = ['fire salve', 'infernal salve']

    def build(self):
        return Loadout(gear_names=[
            'Oathplate helm',
            'Fire cape',
            'Salve (e)',
            'Oathplate body',
            'Oathplate legs',
            'Ferocious gloves',
            'Primordial boots',
            'Berserker ring (i)',
            'Avernic defender',
        ], name=self.name).build()


LoadoutRegistry.register(OathFireSalve())
