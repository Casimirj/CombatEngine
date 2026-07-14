from CombatSim.CombatEngine.Domain.Spell import Spell
from CombatSim.CombatEngine.Data.Registries.SpellRegistry import SpellRegistry

BLOOD_BARRAGE = Spell(
    name="Blood Barrage",
    label="Blood Barrage",
    base_max=29,
    aliases=["blood barrage", "blood"],
)
SpellRegistry.register(BLOOD_BARRAGE)
