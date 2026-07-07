from combat_engine.Domain.Prayer import Prayer
from combat_engine.Data.Registries.PrayerRegistry import PrayerRegistry

AUGURY = Prayer(
    name="Augury",
    label="Augury",
    defence_multiplier=1.25,
    magic_attack_multiplier=1.25,
    magic_damage_bonus=0.04,
    aliases=["augury"],
)
PrayerRegistry.register(AUGURY)
