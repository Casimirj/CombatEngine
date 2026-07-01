from app.Loadout import Loadout
from app.Registries.LoadoutRegistry import LoadoutRegistry


class OathTorvaSalve(Loadout):
    name = "OathTorvaSalve"
    aliases = ['torva salve', 'oath torva salve']

    def build(self):
        return Loadout(gear_names=['Torva full helm', 'Infernal cape', 'Salve (e)', 'Torva platebody', 'Torva platelegs', 'Ferocious gloves', 'Primordial boots', 'Berserker ring (i)', 'Avernic defender'], name=self.name).build()


LoadoutRegistry.register(OathTorvaSalve())
