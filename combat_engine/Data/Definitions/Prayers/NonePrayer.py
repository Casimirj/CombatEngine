from combat_engine.Domain.Prayer import Prayer
from combat_engine.Data.Registries.PrayerRegistry import PrayerRegistry

NONE = Prayer(
    name="None",
    label="None",
    aliases=["none", "no prayer"],
)
PrayerRegistry.register(NONE)
