from CombatSim.CombatEngine.Domain.Prayer import Prayer
from CombatSim.CombatEngine.Data.Registries.PrayerRegistry import PrayerRegistry

DEADEYE = Prayer(
    name="Deadeye",
    label="Deadeye",
    ranged_attack_multiplier=1.18,
    ranged_strength_multiplier=1.18,
    aliases=["deadeye"],
)
PrayerRegistry.register(DEADEYE)
