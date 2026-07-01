from app.GameDefinitions.Prayer import Prayer
from app.Registries.PrayerRegistry import PrayerRegistry
NONE = Prayer(name="None", label="None", aliases=["none", "no prayer"])
PrayerRegistry.register(NONE)
