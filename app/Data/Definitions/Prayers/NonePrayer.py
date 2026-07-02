from app.Domain.Prayer import Prayer
from app.Data.Registries.PrayerRegistry import PrayerRegistry

NONE = Prayer(
    name="None",
    label="None",
    aliases=["none", "no prayer"],
)
PrayerRegistry.register(NONE)
