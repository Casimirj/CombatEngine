from combat_engine.Domain.Prayer import Prayer
from combat_engine.Data.Registries.PrayerRegistry import PrayerRegistry

CHIVALRY = Prayer(
    name="Chivalry",
    label="Chivalry",
    attack_multiplier=1.15,
    strength_multiplier=1.18,
    defence_multiplier=1.20,
    aliases=["chivalry"],
)
PrayerRegistry.register(CHIVALRY)
