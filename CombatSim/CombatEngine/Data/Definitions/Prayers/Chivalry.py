from CombatSim.CombatEngine.Domain.Prayer import Prayer
from CombatSim.CombatEngine.Data.Registries.PrayerRegistry import PrayerRegistry

CHIVALRY = Prayer(
    name="Chivalry",
    label="Chivalry",
    attack_multiplier=1.15,
    strength_multiplier=1.18,
    defence_multiplier=1.20,
    aliases=["chivalry"],
)
PrayerRegistry.register(CHIVALRY)
