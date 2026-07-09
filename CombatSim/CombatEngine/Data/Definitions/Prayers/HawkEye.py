from CombatSim.CombatEngine.Domain.Prayer import Prayer
from CombatSim.CombatEngine.Data.Registries.PrayerRegistry import PrayerRegistry

HAWK_EYE = Prayer(
    name="Hawk Eye",
    label="Hawk Eye",
    ranged_attack_multiplier=1.10,
    ranged_strength_multiplier=1.10,
    aliases=["hawk eye"],
)
PrayerRegistry.register(HAWK_EYE)
