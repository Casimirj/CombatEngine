from app.Domain.Loadout import Loadout
from app.Data.Registries.LoadoutRegistry import LoadoutRegistry


class OathTorvaRancour(Loadout):
    name = "OathTorvaRancour"
    aliases = ['torva rancour', 'oath torva']

    def build(self):
        return Loadout(gear_names=[
            'Torva full helm',
            'Infernal cape',
            'Amulet of rancour',
            'Torva platebody',
            'Torva platelegs',
            'Ferocious gloves',
            'Primordial boots',
            'Berserker ring (i)',
            'Avernic defender',
        ], name=self.name).build()


LoadoutRegistry.register(OathTorvaRancour())
