from CombatSim.CombatEngine.Domain.Spell import Spell
from CombatSim.CombatEngine.Data.Registries.SpellRegistry import SpellRegistry

ICE_BARRAGE = Spell(
    name="Ice Barrage",
    label="Ice Barrage",
    base_max=30,
    aliases=["ice barrage", "ice"],
)
SpellRegistry.register(ICE_BARRAGE)
