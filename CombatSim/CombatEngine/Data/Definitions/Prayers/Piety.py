from CombatSim.CombatEngine.Domain.Prayer import Prayer
from CombatSim.CombatEngine.Data.Registries.PrayerRegistry import PrayerRegistry

PIETY = Prayer(
    name="Piety",
    label="Piety",
    attack_multiplier=1.20,
    strength_multiplier=1.23,
    defence_multiplier=1.25,
    aliases=["piety"],
)
PrayerRegistry.register(PIETY)
